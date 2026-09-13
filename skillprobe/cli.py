"""Command line: `skillprobe run probe.yaml`."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from . import __version__
from .config import load_config
from .engine import ProbeError, Trial, run_probe
from .report import render_markdown, summary_table, to_json


def _load_env_file(path: Path) -> None:
    """Minimal KEY=VALUE loader; never overrides variables already set."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def _split(value: str | None) -> list[str] | None:
    return [v.strip() for v in value.split(",") if v.strip()] if value else None


def cmd_run(args: argparse.Namespace) -> int:
    config_path = Path(args.config)
    _load_env_file(Path(args.env_file) if args.env_file else config_path.parent / ".env")
    cfg = load_config(config_path)

    def progress(trial: Trial, done: int, total: int) -> None:
        mark = "skip" if trial.skipped else ("ok" if trial.passed else "FAIL")
        print(f"[{done}/{total}] {trial.variant} {trial.case_id} #{trial.repeat + 1}: {mark}", file=sys.stderr)

    run = run_probe(
        cfg,
        models=_split(args.models),
        case_ids=_split(args.cases),
        repeats=args.repeats,
        baseline=args.baseline,
        use_cache=not args.no_cache,
        cache_only=args.cache_only,
        progress=None if args.quiet else progress,
    )

    out = Path(args.out) if args.out else Path("reports") / datetime.now().strftime("%Y%m%d-%H%M%S")
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.md").write_text(render_markdown(run), encoding="utf-8")
    (out / "results.json").write_text(to_json(run), encoding="utf-8")

    print(summary_table(run))
    print(f"\nReport: {out / 'report.md'}")

    if args.fail_under is not None:
        rates = [run.summary(v).pass_rate or 0.0 for v in run.variants if v.with_skills]
        if rates and min(rates) < args.fail_under:
            print(f"FAIL: pass rate {min(rates):.2f} is below --fail-under {args.fail_under}", file=sys.stderr)
            return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="skillprobe", description="Eval harness for agent skills.")
    parser.add_argument("--version", action="version", version=f"skillprobe {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run a probe and write report.md + results.json.")
    run.add_argument("config", help="Path to probe.yaml")
    run.add_argument("--models", help="Comma-separated model names from the config")
    run.add_argument("--cases", help="Comma-separated case ids")
    run.add_argument("--repeats", type=int, help="Override repeats for every case")
    run.add_argument("--baseline", action="store_true", help="Also run each model with no skills offered")
    run.add_argument("--out", help="Output directory (default: reports/<timestamp>)")
    run.add_argument("--env-file", help="KEY=VALUE file with API keys (default: .env next to the config)")
    run.add_argument("--no-cache", action="store_true", help="Ignore and do not write the response cache")
    run.add_argument(
        "--cache-only",
        action="store_true",
        help="Never call the API: rebuild the report from cached responses, skip trials that are not cached",
    )
    run.add_argument("--fail-under", type=float, help="Exit 1 if any skill variant's pass rate is below this (0-1)")
    run.add_argument("--quiet", action="store_true", help="No per-trial progress")
    run.set_defaults(func=cmd_run)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (ProbeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
