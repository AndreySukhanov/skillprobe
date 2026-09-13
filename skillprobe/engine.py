"""Runs every (variant x case x repeat) trial and aggregates the results."""

from __future__ import annotations

import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable

from .cache import Cache
from .cases import Case, load_cases
from .checks import CheckResult, run_checks
from .config import ModelSpec, ProbeConfig, Provider
from .runner import ApiRunner, CacheMiss, RunResult
from .skills import Skill, load_skill
from .stats import ratio, wilson_interval

ClientFactory = Callable[[Provider], object]


class ProbeError(RuntimeError):
    pass


@dataclass
class Variant:
    name: str
    spec: ModelSpec
    skills: list[Skill]

    @property
    def with_skills(self) -> bool:
        return bool(self.skills)


@dataclass
class Trial:
    variant: str
    case_id: str
    repeat: int
    target: str | None
    expect_triggered: bool | None
    result: RunResult
    checks: list[CheckResult] = field(default_factory=list)
    skipped: bool = False

    @property
    def passed(self) -> bool:
        return not self.skipped and self.result.error is None and all(c.passed for c in self.checks)


@dataclass
class VariantSummary:
    name: str
    with_skills: bool
    passed: int
    total: int
    interval: tuple[float, float]
    trigger_precision: float | None
    trigger_recall: float | None
    flaky_cases: list[str]
    errors: int
    skipped: int
    cost_usd: float | None
    avg_latency_s: float | None

    @property
    def pass_rate(self) -> float | None:
        return ratio(self.passed, self.total)


@dataclass
class ProbeRun:
    target: str
    cases: list[Case]
    variants: list[Variant]
    trials: list[Trial]
    repeats: int
    started_at: str
    finished_at: str = ""

    def trials_for(self, variant: str, case_id: str | None = None) -> list[Trial]:
        return [t for t in self.trials if t.variant == variant and (case_id is None or t.case_id == case_id)]

    def summary(self, variant: Variant) -> VariantSummary:
        trials = [t for t in self.trials_for(variant.name) if not t.skipped]
        passed = sum(t.passed for t in trials)

        tp = fp = fn = 0
        for t in trials:
            if t.expect_triggered is None or t.target is None or t.result.error:
                continue
            loaded = t.target in t.result.loaded_skills
            tp += loaded and t.expect_triggered
            fp += loaded and not t.expect_triggered
            fn += (not loaded) and t.expect_triggered

        flaky = []
        for case in self.cases:
            outcomes = {t.passed for t in trials if t.case_id == case.id}
            if len(outcomes) > 1:
                flaky.append(case.id)

        costs = [t.result.usage.cost_usd for t in trials if t.result.usage.cost_usd is not None]
        latencies = [t.result.latency_s for t in trials if t.result.error is None]  # cache keeps original latency
        return VariantSummary(
            name=variant.name,
            with_skills=variant.with_skills,
            passed=passed,
            total=len(trials),
            interval=wilson_interval(passed, len(trials)),
            trigger_precision=ratio(tp, tp + fp) if variant.with_skills else None,
            trigger_recall=ratio(tp, tp + fn) if variant.with_skills else None,
            flaky_cases=flaky,
            errors=sum(1 for t in trials if t.result.error),
            skipped=sum(1 for t in self.trials_for(variant.name) if t.skipped),
            cost_usd=sum(costs) if costs else None,
            avg_latency_s=sum(latencies) / len(latencies) if latencies else None,
        )


class _OfflineClient:
    """Stands in for the API client in cache-only mode; any real call is a bug."""

    class _Completions:
        def create(self, **kwargs):
            raise CacheMiss("offline client called")

    class _Chat:
        def __init__(self):
            self.completions = _OfflineClient._Completions()

    def __init__(self):
        self.chat = self._Chat()


def default_client_factory(provider: Provider) -> object:
    from openai import OpenAI

    key = os.environ.get(provider.api_key_env)
    if not key:
        raise ProbeError(f"environment variable {provider.api_key_env} is not set")
    return OpenAI(base_url=provider.base_url, api_key=key, timeout=180, max_retries=3)


def run_probe(
    cfg: ProbeConfig,
    *,
    models: list[str] | None = None,
    case_ids: list[str] | None = None,
    repeats: int | None = None,
    baseline: bool = False,
    use_cache: bool = True,
    cache_only: bool = False,
    client_factory: ClientFactory = default_client_factory,
    progress: Callable[[Trial, int, int], None] | None = None,
) -> ProbeRun:
    skills = [load_skill(cfg.resolve(p)) for p in cfg.skills]
    skill_names = {s.name for s in skills}
    target = cfg.target or skills[0].name
    if target not in skill_names:
        raise ProbeError(f"target skill '{target}' is not among loaded skills {sorted(skill_names)}")

    cases = load_cases(cfg.resolve(cfg.cases))
    if case_ids:
        unknown = set(case_ids) - {c.id for c in cases}
        if unknown:
            raise ProbeError(f"unknown case ids: {sorted(unknown)}")
        cases = [c for c in cases if c.id in case_ids]
    for c in cases:
        if c.skill and c.skill not in skill_names:
            raise ProbeError(f"case '{c.id}': skill '{c.skill}' is not loaded")

    specs = cfg.models
    if models:
        unknown = set(models) - {m.name for m in specs}
        if unknown:
            raise ProbeError(f"unknown model names: {sorted(unknown)}")
        specs = [m for m in specs if m.name in models]

    variants: list[Variant] = []
    for spec in specs:
        variants.append(Variant(spec.name, spec, skills))
        if baseline:
            variants.append(Variant(f"{spec.name} (no skills)", spec, []))

    cache = Cache(cfg.resolve(cfg.cache_dir)) if use_cache and cfg.cache_dir else None
    if cache_only:
        if cache is None:
            raise ProbeError("--cache-only needs cache_dir in the config and the cache enabled")
        client_factory = lambda provider: _OfflineClient()  # noqa: E731 - no network, no keys needed
    clients: dict[str, object] = {}
    runners: dict[str, ApiRunner] = {}
    for spec in specs:
        if spec.provider not in clients:
            clients[spec.provider] = client_factory(cfg.provider(spec.provider))
        runners[spec.name] = ApiRunner(
            clients[spec.provider],
            spec.model,
            system_prompt=cfg.system_prompt,
            params=spec.params,
            extra_body=spec.extra_body,
            max_turns=cfg.max_turns,
            price_in=spec.price_in,
            price_out=spec.price_out,
            cache=cache,
            cache_only=cache_only,
        )

    default_repeats = repeats or cfg.repeats
    jobs = [
        (variant, case, r)
        for variant in variants
        for case in cases
        for r in range(repeats or case.repeats or default_repeats)
    ]

    run = ProbeRun(
        target=target,
        cases=cases,
        variants=variants,
        trials=[],
        repeats=default_repeats,
        started_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )

    lock = threading.Lock()
    spent = 0.0

    def execute(variant: Variant, case: Case, repeat: int) -> Trial:
        nonlocal spent
        case_target = (case.skill or target) if variant.with_skills else None
        trial = Trial(variant.name, case.id, repeat, case_target, case.expect.triggered, RunResult())
        with lock:
            if cfg.max_cost_usd is not None and spent >= cfg.max_cost_usd:
                trial.skipped = True
                trial.result.error = "skipped: max_cost_usd reached"
                return trial
        try:
            trial.result = runners[variant.spec.name].run(case.render_prompt(), variant.skills, repeat)
        except CacheMiss:
            trial.skipped = True
            trial.result.error = "skipped: not in cache"
            return trial
        if trial.result.error is None:
            trial.checks = run_checks(case.expect, trial.result, case_target)
        with lock:
            if not trial.result.cached:
                spent += trial.result.usage.cost_usd or 0.0
        return trial

    with ThreadPoolExecutor(max_workers=cfg.concurrency) as pool:
        futures = [pool.submit(execute, *job) for job in jobs]
        for done, future in enumerate(as_completed(futures), start=1):
            trial = future.result()
            run.trials.append(trial)
            if progress:
                progress(trial, done, len(jobs))

    order = {(v.name, c.id): i for i, (v, c) in enumerate((v, c) for v in variants for c in cases)}
    run.trials.sort(key=lambda t: (order[(t.variant, t.case_id)], t.repeat))
    run.finished_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return run
