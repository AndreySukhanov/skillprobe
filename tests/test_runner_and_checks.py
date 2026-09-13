from pathlib import Path

from fakes import FakeClient, load, text

from skillprobe.cache import Cache
from skillprobe.cases import Expect
from skillprobe.checks import run_checks
from skillprobe.runner import ApiRunner, RunResult
from skillprobe.skills import Skill

SKILL = Skill("commit-message", "Write commit messages.", "Always add a Why: line.", Path("SKILL.md"))
OTHER = Skill("code-review", "Review diffs.", "Find bugs.", Path("SKILL.md"))


def test_skill_body_is_returned_to_the_model_after_load():
    client = FakeClient.script(load("commit-message"), text("fix(auth): reject expired tokens\n\nWhy: logout bug"))
    result = ApiRunner(client, "m").run("commit msg", [SKILL, OTHER])

    assert result.error is None
    assert result.loaded_skills == ["commit-message"]
    assert result.turns == 2
    assert result.output.startswith("fix(auth)")
    second = client.requests[1]["messages"]
    assert second[-1] == {"role": "tool", "tool_call_id": "call_1", "content": "Always add a Why: line."}
    assert "- code-review: Review diffs." in client.requests[0]["messages"][0]["content"]


def test_no_tool_offered_without_skills():
    client = FakeClient.script(text("hello"))
    result = ApiRunner(client, "m").run("hi", [])
    assert "tools" not in client.requests[0]
    assert result.loaded_skills == []


def test_unknown_skill_name_is_reported_back_not_loaded():
    client = FakeClient.script(load("nope"), text("ok"))
    result = ApiRunner(client, "m").run("hi", [SKILL])
    assert result.loaded_skills == []
    assert client.requests[1]["messages"][-1]["content"].startswith("Error: no skill named 'nope'")


def test_max_turns_is_an_error():
    client = FakeClient(lambda kwargs: load("commit-message"))
    result = ApiRunner(client, "m", max_turns=2).run("hi", [SKILL])
    assert result.error and "max_turns" in result.error


def test_api_exception_becomes_error_result():
    def boom(kwargs):
        raise TimeoutError("provider timed out")

    result = ApiRunner(FakeClient(boom), "m").run("hi", [SKILL])
    assert result.error == "TimeoutError: provider timed out"


def test_cost_from_provider_or_from_prices():
    reported = ApiRunner(FakeClient.script(text("a", cost=0.002)), "m").run("hi", [])
    assert reported.usage.cost_usd == 0.002

    priced = ApiRunner(
        FakeClient.script(text("a", prompt_tokens=1_000_000, completion_tokens=500_000)), "m", price_in=1, price_out=4
    ).run("hi", [])
    assert priced.usage.cost_usd == 3.0


def test_cache_hit_skips_api_and_repeats_are_distinct(tmp_path):
    cache = Cache(tmp_path)
    client = FakeClient(lambda kwargs: text("same"))
    runner = ApiRunner(client, "m", cache=cache)

    first = runner.run("hi", [], repeat=0)
    again = runner.run("hi", [], repeat=0)
    other = runner.run("hi", [], repeat=1)

    assert not first.cached and again.cached and not other.cached
    assert len(client.requests) == 2


def test_checks_trigger_regex_contains_and_json():
    result = RunResult(output='```json\n{"ok": true}\n```', loaded_skills=["commit-message"])
    expect = Expect(
        triggered=True,
        contains=['"OK"'],
        not_contains=["error"],
        regex=[r"^\{"],
        json_schema={"type": "object", "required": ["ok"]},
        max_chars=100,
    )
    checks = {c.name.split(" ")[0]: c.passed for c in run_checks(expect, result, "commit-message")}
    assert checks == {
        "triggered": True,
        "contains": True,
        "not_contains": True,
        "regex": True,
        "json_schema": True,
        "max_chars": True,
    }


def test_trigger_check_fails_on_unwanted_load_and_is_skipped_for_baseline():
    result = RunResult(output="x", loaded_skills=["commit-message"])
    [check] = run_checks(Expect(triggered=False), result, "commit-message")
    assert not check.passed
    assert run_checks(Expect(triggered=False), result, None) == []


def test_invalid_json_fails_check():
    [check] = run_checks(Expect(json_schema={"type": "object"}), RunResult(output="not json"), None)
    assert not check.passed and "not JSON" in check.detail
