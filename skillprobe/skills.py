"""Loading SKILL.md files: YAML frontmatter (name, description) plus a Markdown body."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

_FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n(.*))?\Z", re.S)


class SkillError(ValueError):
    pass


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    body: str
    path: Path


def load_skill(path: str | Path) -> Skill:
    """Load a skill from a directory containing SKILL.md or from the file itself."""
    p = Path(path)
    file = p / "SKILL.md" if p.is_dir() else p
    if not file.is_file():
        raise SkillError(f"SKILL.md not found: {file}")

    text = file.read_text(encoding="utf-8").replace("\r\n", "\n")
    match = _FRONTMATTER.match(text)
    if not match:
        raise SkillError(f"{file}: missing YAML frontmatter between '---' lines")

    meta = yaml.safe_load(match.group(1)) or {}
    if not isinstance(meta, dict):
        raise SkillError(f"{file}: frontmatter must be a mapping")
    for field in ("name", "description"):
        if not isinstance(meta.get(field), str) or not meta[field].strip():
            raise SkillError(f"{file}: frontmatter field '{field}' is required")

    return Skill(
        name=meta["name"].strip(),
        description=" ".join(meta["description"].split()),
        body=(match.group(2) or "").strip(),
        path=file,
    )
