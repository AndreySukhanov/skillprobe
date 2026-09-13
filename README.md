# skillprobe

**Eval harness for agent skills.** Does your `SKILL.md` load when it should, stay out of the way when it shouldn't, and does the model actually follow it? Measured with repeats and confidence intervals, across OpenAI, Qwen, DeepSeek, GLM, Kimi and any OpenAI-compatible model.

![python](https://img.shields.io/badge/python-3.10%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![status](https://img.shields.io/badge/status-alpha-orange)

![skillprobe demo: 150 trials across five models, summary table, a Qwen failure from the report](docs/demo.gif)

<sub>Real output of the bundled example, replayed from the response cache with `--cache-only`.</sub>

## Why

A skill is a prompt with a trigger. Both halves fail quietly:

- **The trigger.** The model only sees the skill's `name` and `description`. A vague description means the skill never loads - or loads for requests it has nothing to do with.
- **The body.** The skill loads, and the model follows half of it. Differently on every run.

Reading a few outputs by eye catches neither. skillprobe runs a fixed set of cases many times per model and reports numbers you can compare between versions of a skill and between models.

## Results on the bundled example

`examples/commit-message` - a skill that enforces a team commit-message convention, plus a `code-review` skill offered as a distractor. 10 cases: 5 requests that must load the skill and follow it, 5 near-misses that must not load it. 3 repeats each, all models through OpenRouter.

| model | pass with skill | pass without skill | trigger precision / recall | flaky cases | cost, 30 trials | avg latency |
|---|---|---|---|---|---|---|
| gpt-5.6-luna | **30/30** (89-100%) | 15/30 | 100% / 100% | 0 | $0.007 | 2.5 s |
| kimi-k3 | **29/30** (83-99%) | incomplete* | 100% / 100% | 1 | $0.194 | 30.4 s |
| qwen3.8-flash | **24/30** (63-90%) | 15/30 | 100% / 100% | 2 | $0.007 | 12.8 s |
| glm-5.3-flash | **23/30** (59-88%) | 15/30 | 100% / 100% | 5 | $0.008 | 17.6 s |
| deepseek-v4.1-flash | **19/30** (46-78%) | 15/30 | 100% / 100% | 4 | $0.011 | 3.2 s |

Brackets are 95% Wilson intervals. *The run was stopped manually before the kimi-k3 baseline finished (15 of 30 trials). Full report: [`examples/commit-message/results/report.md`](examples/commit-message/results/report.md).

What the numbers say:

- **Triggering was the easy part here** - every model loaded the skill exactly when it should. Following it is where they split.
- **Without the skill every model scores 15/30** - only the five near-misses pass. None of the commit requests match the convention on general knowledge, so the gap is the skill's measured effect.
- **Qwen follows the shape but not the details**: it leaves an empty `Refs:` line when there is no ticket and writes `config:` instead of `chore(config):`.
- **GLM and DeepSeek are flaky**: in 5 and 4 of 10 cases the same prompt passed on one repeat and failed on another. A single run would have told a different story each time - that is why repeats are the default, not an option.

Ten cases is a small probe; the point is the method. Treat the ranking as specific to this skill.

## Quick start

```bash
pip install -e .
export OPENROUTER_API_KEY=...      # or put it in a .env next to probe.yaml
skillprobe run examples/commit-message/probe.yaml --repeats 1 --models qwen3.8-flash
```

Useful flags:

| flag | what it does |
|---|---|
| `--baseline` | also run every model with no skills offered - shows what the skill adds |
| `--repeats N` | override repeats for all cases |
| `--models a,b` / `--cases x,y` | run a subset |
| `--cache-only` | never call the API: rebuild the report from cached responses |
| `--fail-under 0.9` | exit 1 if any model's pass rate is lower - for CI |

Every response is cached on disk (`.skillprobe_cache/`), keyed by the full request and the repeat number. Editing checks and re-running costs nothing. `max_cost_usd` in the config stops a run before it overspends.

## How a trial works

```
system: base prompt + list of skills (name: description only)
tools:  load_skill(name)
user:   case prompt + attached files
   |
   v
model calls load_skill?  --yes-->  tool result = SKILL.md body  -->  model answers
   |
   no --> model answers
   |
   v
checks: triggered? contains / not_contains / regex / json_schema / max_chars
```

This mirrors how agent harnesses expose skills: the body stays out of context until the model asks for it. Whether it asks is exactly what the trigger metrics measure.

## Writing a probe

`probe.yaml`:

```yaml
skills:
  - skills/commit-message     # the skill under test
  - skills/code-review        # distractors are offered too
target: commit-message
cases: cases.yaml
repeats: 3
max_cost_usd: 2.0

models:
  - name: qwen3.8-flash
    model: qwen/qwen3.8-flash           # provider defaults to openrouter
  - name: deepseek-direct
    provider: deepseek                  # DEEPSEEK_API_KEY
    model: deepseek-chat
```

`cases.yaml`:

```yaml
- id: ticket-from-branch
  prompt: I'm on branch PAY-482-invoice-pdf. What should I put in git commit for this?
  files: [fixtures/billing_invoice_pdf.diff]
  expect:
    triggered: true
    regex:
      - '\Afeat\(billing\): '
      - '^Refs: PAY-482\s*$'

- id: review-is-not-commit          # near-miss: a diff, but not a commit request
  prompt: Review this diff before I merge it. Anything dangerous?
  files: [fixtures/sql_injection.diff]
  expect:
    triggered: false
    contains: ["injection"]
```

Good probes are mostly near-misses. A skill that loads for "write a haiku" is rare; one that loads for "review this diff" when it is a commit-message skill is common.

## Providers

Built in: `openrouter`, `openai`, `deepseek`, `dashscope` (Qwen), `zai` (GLM), `moonshot` (Kimi), `yandex` (YandexGPT). Each is an OpenAI-compatible base URL plus the name of the environment variable holding the key. Anything else - a local vLLM, a GigaChat proxy, a corporate gateway - is two lines under `providers:`.

The example run uses OpenRouter only; the direct vendor presets follow each vendor's documented OpenAI-compatible API.

## Roadmap

- [x] Skill loading via tool call, deterministic checks, trigger precision/recall, repeats with intervals, flaky detection, cost and latency, response cache, budget cap
- [ ] LLM-as-judge with rubrics, and pairwise comparison of two skill versions
- [ ] Judge calibration against human labels - a judge that disagrees with people is flagged, not trusted
- [ ] Judge panels from different model families, with disagreements reported instead of averaged
- [ ] `skillprobe compare`: what broke between skill v1 and v2, as a GitHub PR comment
- [ ] Adversarial pack: prompt injection through attached files, language switching

## Development

```bash
pip install -e ".[dev]"
pytest
```

Tests use a scripted fake client - no network, no keys.

## License

MIT
