"""probe.yaml: which models, which skills, which cases, how many repeats."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator


class Provider(BaseModel):
    model_config = ConfigDict(extra="forbid")

    base_url: str
    api_key_env: str


# OpenAI-compatible endpoints. Only `openrouter` and `openai` are exercised in this repo's
# example runs; the rest follow each vendor's documented OpenAI-compatible API.
BUILTIN_PROVIDERS: dict[str, Provider] = {
    "openrouter": Provider(base_url="https://openrouter.ai/api/v1", api_key_env="OPENROUTER_API_KEY"),
    "openai": Provider(base_url="https://api.openai.com/v1", api_key_env="OPENAI_API_KEY"),
    "deepseek": Provider(base_url="https://api.deepseek.com/v1", api_key_env="DEEPSEEK_API_KEY"),
    "dashscope": Provider(
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1", api_key_env="DASHSCOPE_API_KEY"
    ),
    "zai": Provider(base_url="https://api.z.ai/api/paas/v4", api_key_env="ZAI_API_KEY"),
    "moonshot": Provider(base_url="https://api.moonshot.ai/v1", api_key_env="MOONSHOT_API_KEY"),
    "yandex": Provider(base_url="https://llm.api.cloud.yandex.net/v1", api_key_env="YANDEX_API_KEY"),
}


class ModelSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="Label used in reports.")
    provider: str = "openrouter"
    model: str
    params: dict[str, Any] = Field(default_factory=dict, description="Extra chat.completions kwargs.")
    extra_body: dict[str, Any] = Field(default_factory=dict)
    price_in: float | None = Field(default=None, description="USD per 1M input tokens, if the API does not report cost.")
    price_out: float | None = None


class ProbeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skills: list[str] = Field(min_length=1, description="Skill dirs; all are offered to the model.")
    target: str | None = Field(default=None, description="Skill under test; defaults to the first one.")
    cases: str
    models: list[ModelSpec] = Field(min_length=1)
    providers: dict[str, Provider] = Field(default_factory=dict)
    system_prompt: str = "You are a helpful assistant."
    repeats: int = Field(default=1, ge=1)
    concurrency: int = Field(default=4, ge=1)
    max_turns: int = Field(default=4, ge=1)
    max_cost_usd: float | None = None
    cache_dir: str | None = ".skillprobe_cache"

    base_dir: Path = Field(default=Path("."), exclude=True)

    @model_validator(mode="after")
    def _check_providers(self) -> "ProbeConfig":
        known = {**BUILTIN_PROVIDERS, **self.providers}
        for m in self.models:
            if m.provider not in known:
                raise ValueError(f"model '{m.name}': unknown provider '{m.provider}'")
        names = [m.name for m in self.models]
        if len(names) != len(set(names)):
            raise ValueError("model names must be unique")
        return self

    def provider(self, name: str) -> Provider:
        return {**BUILTIN_PROVIDERS, **self.providers}[name]

    def resolve(self, rel: str) -> Path:
        return (self.base_dir / rel).resolve()


def load_config(path: str | Path) -> ProbeConfig:
    file = Path(path)
    raw = yaml.safe_load(file.read_text(encoding="utf-8")) or {}
    cfg = ProbeConfig.model_validate(raw)
    cfg.base_dir = file.parent.resolve()
    return cfg
