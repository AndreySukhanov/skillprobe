"""Deterministic checks of one answer against a case's expectations."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

import jsonschema

from .cases import Expect
from .runner import RunResult

_FENCE = re.compile(r"\A```[a-zA-Z0-9_-]*\n(.*?)\n?```\Z", re.S)


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""


def run_checks(expect: Expect, result: RunResult, target: str | None) -> list[CheckResult]:
    """`target` is None when the run had no skills (baseline) - the trigger check is skipped then."""
    out = result.output
    checks: list[CheckResult] = []

    if expect.triggered is not None and target is not None:
        loaded = target in result.loaded_skills
        checks.append(
            CheckResult(
                "triggered",
                loaded == expect.triggered,
                f"expected {'load' if expect.triggered else 'no load'} of '{target}', loaded={result.loaded_skills}",
            )
        )

    lower = out.lower()
    for s in expect.contains:
        checks.append(CheckResult(f"contains {s!r}", s.lower() in lower))
    for s in expect.not_contains:
        checks.append(CheckResult(f"not_contains {s!r}", s.lower() not in lower))

    for pattern in expect.regex:
        checks.append(CheckResult(f"regex {pattern!r}", re.search(pattern, out, re.M) is not None))

    if expect.json_schema is not None:
        checks.append(_check_json(out, expect.json_schema))

    if expect.max_chars is not None:
        checks.append(CheckResult(f"max_chars {expect.max_chars}", len(out) <= expect.max_chars, f"len={len(out)}"))

    return checks


def _check_json(output: str, schema: dict) -> CheckResult:
    text = output.strip()
    fenced = _FENCE.match(text)
    if fenced:
        text = fenced.group(1)
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return CheckResult("json_schema", False, f"not JSON: {exc}")
    try:
        jsonschema.validate(data, schema)
    except jsonschema.ValidationError as exc:
        return CheckResult("json_schema", False, exc.message)
    return CheckResult("json_schema", True)
