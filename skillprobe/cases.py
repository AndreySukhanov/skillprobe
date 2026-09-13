"""Eval cases: a prompt, optional attached files, and what we expect from the answer."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Expect(BaseModel):
    model_config = ConfigDict(extra="forbid")

    triggered: bool | None = Field(
        default=None, description="Whether the target skill must be loaded. None = not checked."
    )
    contains: list[str] = Field(default_factory=list, description="Case-insensitive substrings.")
    not_contains: list[str] = Field(default_factory=list)
    regex: list[str] = Field(default_factory=list, description="Python regexes, each must match (re.search, MULTILINE).")
    json_schema: dict[str, Any] | None = None
    max_chars: int | None = None

    @field_validator("regex", mode="before")
    @classmethod
    def _regex_as_list(cls, v: Any) -> Any:
        return [v] if isinstance(v, str) else v


class Case(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    prompt: str
    files: list[str] = Field(default_factory=list)
    skill: str | None = Field(default=None, description="Target skill for this case; defaults to the probe target.")
    expect: Expect = Field(default_factory=Expect)
    repeats: int | None = Field(default=None, ge=1)
    tags: list[str] = Field(default_factory=list)

    @field_validator("id")
    @classmethod
    def _id_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("case id must not be blank")
        return v

    def render_prompt(self) -> str:
        """The user message: prompt followed by attached files."""
        parts = [self.prompt.strip()]
        for f in self.files:
            path = Path(f)
            content = path.read_text(encoding="utf-8").replace("\r\n", "\n")
            parts.append(f"--- {path.name} ---\n{content.rstrip()}")
        return "\n\n".join(parts)


def load_cases(path: str | Path) -> list[Case]:
    file = Path(path)
    raw = yaml.safe_load(file.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError(f"{file}: expected a YAML list of cases")

    cases = [Case.model_validate(item) for item in raw]
    seen: set[str] = set()
    for case in cases:
        if case.id in seen:
            raise ValueError(f"{file}: duplicate case id '{case.id}'")
        seen.add(case.id)
        resolved = []
        for f in case.files:
            p = (file.parent / f).resolve()
            if not p.is_file():
                raise ValueError(f"{file}: case '{case.id}' file not found: {f}")
            resolved.append(str(p))
        case.files = resolved
    return cases
