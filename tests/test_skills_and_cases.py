from pathlib import Path

import pytest

from skillprobe.cases import load_cases
from skillprobe.skills import SkillError, load_skill

EXAMPLE = Path(__file__).parents[1] / "examples" / "commit-message"


def test_loads_example_skill():
    skill = load_skill(EXAMPLE / "skills" / "commit-message")
    assert skill.name == "commit-message"
    assert "commit message" in skill.description
    assert skill.body.startswith("# Commit message convention")


def test_skill_without_frontmatter_is_rejected(tmp_path):
    (tmp_path / "SKILL.md").write_text("# no frontmatter\n", encoding="utf-8")
    with pytest.raises(SkillError, match="frontmatter"):
        load_skill(tmp_path)


def test_skill_requires_description(tmp_path):
    (tmp_path / "SKILL.md").write_text("---\nname: x\n---\nbody\n", encoding="utf-8")
    with pytest.raises(SkillError, match="description"):
        load_skill(tmp_path)


def test_example_cases_load_and_resolve_files():
    cases = load_cases(EXAMPLE / "cases.yaml")
    assert len(cases) == 10
    assert sum(c.expect.triggered is True for c in cases) == 5
    fix = next(c for c in cases if c.id == "fix-in-auth")
    assert Path(fix.files[0]).is_file()
    assert "--- auth_token_expiry.diff ---" in fix.render_prompt()


def test_single_regex_string_becomes_list(tmp_path):
    (tmp_path / "cases.yaml").write_text("- id: a\n  prompt: hi\n  expect:\n    regex: '^x'\n", encoding="utf-8")
    assert load_cases(tmp_path / "cases.yaml")[0].expect.regex == ["^x"]


def test_duplicate_case_ids_are_rejected(tmp_path):
    (tmp_path / "cases.yaml").write_text("- id: a\n  prompt: x\n- id: a\n  prompt: y\n", encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate"):
        load_cases(tmp_path / "cases.yaml")


def test_unknown_expect_field_is_rejected(tmp_path):
    (tmp_path / "cases.yaml").write_text("- id: a\n  prompt: x\n  expect:\n    trigered: true\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_cases(tmp_path / "cases.yaml")
