import json
from pathlib import Path

import pytest
from fakes import FakeClient, load, text

from skillprobe.config import ProbeConfig
from skillprobe.engine import ProbeError, run_probe
from skillprobe.report import render_markdown, to_json
from skillprobe.stats import wilson_interval

EXAMPLE = Path(__file__).parents[1] / "examples" / "commit-message"


def make_config(**overrides) -> ProbeConfig:
    raw = {
        "skills": ["skills/commit-message", "skills/code-review"],
        "cases": "cases.yaml",
        "models": [{"name": "fake", "model": "fake-1"}],
        "repeats": 1,
        "cache_dir": None,
        **overrides,
    }
    cfg = ProbeConfig.model_validate(raw)
    cfg.base_dir = EXAMPLE
    return cfg


def perfect_model(kwargs):
    """Loads the skill for commit requests and answers each case correctly."""
    messages = kwargs["messages"]
    user = messages[1]["content"]
    loaded = any(m["role"] == "tool" for m in messages)
    wants_commit = any(k in user.lower() for k in ("commit message", "git commit", "сообщение коммита", "commit msg"))
    wants_commit = wants_commit and "change the message" not in user

    if wants_commit and not loaded and kwargs.get("tools"):
        return load("commit-message")
    if "auth_token_expiry" in user:
        return text("fix(auth): reject tokens right after expiry\n\nWhy: grace minute kept sessions alive after logout")
    if "billing_invoice_pdf" in user and wants_commit:
        return text("feat(billing): add invoice pdf export\n\nWhy: customers need invoices for accountants\nRefs: PAY-482")
    if "readme_install" in user:
        return text("docs: update install steps for python 3.11\n\nWhy: the service now needs tomllib")
    if "config_timeout" in user:
        return text("chore(config): raise payment gateway timeout to 45s\n\nWhy: unknown - ask the author")
    if "sql_injection" in user:
        return text("Yes: this builds SQL from user input, a classic SQL injection.")
    if "change the message" in user:
        return text("Use git commit --amend.")
    return text("Some unrelated answer.")


def test_perfect_model_passes_every_case():
    run = run_probe(make_config(), client_factory=lambda provider: FakeClient(perfect_model))
    summary = run.summary(run.variants[0])
    failed = [(t.case_id, [c.name for c in t.checks if not c.passed], t.result.output) for t in run.trials if not t.passed]
    assert failed == []
    assert summary.passed == summary.total == 10
    assert summary.trigger_precision == 1.0 and summary.trigger_recall == 1.0


def test_model_that_always_loads_the_skill_loses_precision_not_recall():
    def eager(kwargs):
        if kwargs.get("tools") and not any(m["role"] == "tool" for m in kwargs["messages"]):
            return load("commit-message")
        return perfect_model({**kwargs, "tools": None})

    run = run_probe(make_config(), client_factory=lambda provider: FakeClient(eager))
    summary = run.summary(run.variants[0])
    assert summary.trigger_recall == 1.0
    assert summary.trigger_precision == 0.5


def test_baseline_variant_has_no_tools_and_no_trigger_metrics():
    client = FakeClient(perfect_model)
    run = run_probe(make_config(), baseline=True, client_factory=lambda provider: client)
    names = [v.name for v in run.variants]
    assert names == ["fake", "fake (no skills)"]
    base = run.summary(run.variants[1])
    assert base.trigger_precision is None and base.trigger_recall is None


def test_flaky_case_detected_across_repeats():
    calls = {"n": 0}

    def flaky(kwargs):
        if "haiku" in kwargs["messages"][1]["content"]:
            calls["n"] += 1
            if calls["n"] == 2:
                return load("commit-message") if not any(m["role"] == "tool" for m in kwargs["messages"]) else text("x")
        return perfect_model(kwargs)

    cfg = make_config(concurrency=1)
    run = run_probe(cfg, case_ids=["unrelated-haiku"], repeats=3, client_factory=lambda provider: FakeClient(flaky))
    summary = run.summary(run.variants[0])
    assert summary.flaky_cases == ["unrelated-haiku"]
    assert summary.passed == 2 and summary.total == 3


def test_budget_stops_remaining_trials():
    cfg = make_config(concurrency=1, max_cost_usd=0.01)
    run = run_probe(cfg, client_factory=lambda provider: FakeClient(lambda kwargs: text("x", cost=0.02)))
    assert sum(t.skipped for t in run.trials) == 9
    assert run.summary(run.variants[0]).skipped == 9


def test_cache_only_never_calls_api_and_skips_misses(tmp_path):
    cfg = make_config(cache_dir=str(tmp_path), concurrency=1)
    run_probe(cfg, case_ids=["unrelated-haiku"], client_factory=lambda p: FakeClient(perfect_model))

    def forbidden(provider):
        raise AssertionError("cache-only must not build a real client")

    run = run_probe(cfg, cache_only=True, client_factory=forbidden)
    summary = run.summary(run.variants[0])
    assert summary.total == 1 and summary.passed == 1
    assert summary.skipped == 9


def test_unknown_filters_raise():
    with pytest.raises(ProbeError, match="unknown case"):
        run_probe(make_config(), case_ids=["nope"], client_factory=lambda p: FakeClient(perfect_model))
    with pytest.raises(ProbeError, match="unknown model"):
        run_probe(make_config(), models=["nope"], client_factory=lambda p: FakeClient(perfect_model))


def test_report_renders_and_json_round_trips():
    run = run_probe(make_config(), client_factory=lambda provider: FakeClient(lambda kwargs: text("nope")))
    md = render_markdown(run)
    # only the three negatives without content checks pass
    assert "| fake | 3/10 (30%)" in md
    assert "### fake" in md and "`fix-in-auth` #1" in md
    data = json.loads(to_json(run))
    assert data["summary"][0]["passed"] == 3
    assert len(data["trials"]) == 10


def test_wilson_interval_edges():
    assert wilson_interval(0, 0) == (0.0, 0.0)
    lo, hi = wilson_interval(10, 10)
    assert hi == 1.0 and 0.65 < lo < 0.75
