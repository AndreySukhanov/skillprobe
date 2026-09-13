"""Runs one prompt against an OpenAI-compatible chat API with skills exposed as a tool.

Skill loading mirrors how agent harnesses (Claude Code, Codex) handle SKILL.md: the model sees
only each skill's name and description, and must call `load_skill` to get the body. Whether it
calls the tool is exactly what the trigger check measures.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Protocol

from .cache import Cache
from .skills import Skill

LOAD_SKILL_TOOL: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "load_skill",
        "description": "Load the full instructions of a skill by its name.",
        "parameters": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "Skill name."}},
            "required": ["name"],
        },
    },
}


def build_system_prompt(base: str, skills: list[Skill]) -> str:
    if not skills:
        return base
    lines = [
        base,
        "",
        "You have skills: packaged instructions for specific kinds of tasks.",
        "If a skill's description matches the user's request, call load_skill with its name "
        "before answering, then follow the loaded instructions. Do not load skills that do not match.",
        "",
        "Available skills:",
    ]
    lines += [f"- {s.name}: {s.description}" for s in skills]
    return "\n".join(lines)


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float | None = None

    def add(self, other: "Usage") -> None:
        self.input_tokens += other.input_tokens
        self.output_tokens += other.output_tokens
        if other.cost_usd is not None:
            self.cost_usd = (self.cost_usd or 0.0) + other.cost_usd


@dataclass
class RunResult:
    output: str = ""
    loaded_skills: list[str] = field(default_factory=list)
    turns: int = 0
    usage: Usage = field(default_factory=Usage)
    latency_s: float = 0.0
    cached: bool = False
    error: str | None = None


class CacheMiss(RuntimeError):
    """Raised in cache-only mode instead of calling the API."""


class ChatClient(Protocol):
    """The slice of `openai.OpenAI` we use; tests pass a fake."""

    chat: Any


class ApiRunner:
    def __init__(
        self,
        client: ChatClient,
        model: str,
        *,
        system_prompt: str = "You are a helpful assistant.",
        params: dict[str, Any] | None = None,
        extra_body: dict[str, Any] | None = None,
        max_turns: int = 4,
        price_in: float | None = None,
        price_out: float | None = None,
        cache: Cache | None = None,
        cache_only: bool = False,
    ):
        if cache_only and cache is None:
            raise ValueError("cache_only requires a cache")
        self.client = client
        self.model = model
        self.system_prompt = system_prompt
        self.params = params or {}
        self.extra_body = extra_body or {}
        self.max_turns = max_turns
        self.price_in = price_in
        self.price_out = price_out
        self.cache = cache
        self.cache_only = cache_only

    def run(self, prompt: str, skills: list[Skill], repeat: int = 0) -> RunResult:
        by_name = {s.name: s for s in skills}
        tools = [LOAD_SKILL_TOOL] if skills else None
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": build_system_prompt(self.system_prompt, skills)},
            {"role": "user", "content": prompt},
        ]
        result = RunResult(cached=True)

        try:
            for _ in range(self.max_turns):
                response, latency, cached = self._complete(messages, tools, repeat)
                result.turns += 1
                result.latency_s += latency
                result.cached = result.cached and cached
                result.usage.add(self._usage(response))

                message = response["choices"][0]["message"]
                tool_calls = message.get("tool_calls") or []
                if not tool_calls:
                    result.output = (message.get("content") or "").strip()
                    return result

                messages.append(
                    {
                        "role": "assistant",
                        "content": message.get("content"),
                        "tool_calls": [
                            {
                                "id": tc["id"],
                                "type": "function",
                                "function": {
                                    "name": tc["function"]["name"],
                                    "arguments": tc["function"].get("arguments") or "{}",
                                },
                            }
                            for tc in tool_calls
                        ],
                    }
                )
                for tc in tool_calls:
                    messages.append(
                        {"role": "tool", "tool_call_id": tc["id"], "content": self._handle_tool(tc, by_name, result)}
                    )
            result.error = f"no final answer within max_turns={self.max_turns}"
        except CacheMiss:
            raise
        except Exception as exc:  # network, auth, provider-side validation
            result.error = f"{type(exc).__name__}: {exc}"
        return result

    def _handle_tool(self, tool_call: dict[str, Any], skills: dict[str, Skill], result: RunResult) -> str:
        name = tool_call["function"]["name"]
        if name != "load_skill":
            return f"Error: unknown tool '{name}'."
        try:
            args = json.loads(tool_call["function"].get("arguments") or "{}")
        except json.JSONDecodeError:
            return "Error: arguments must be JSON like {\"name\": \"skill-name\"}."
        skill = skills.get(str(args.get("name", "")).strip())
        if skill is None:
            return f"Error: no skill named '{args.get('name')}'. Available: {', '.join(skills)}."
        if skill.name not in result.loaded_skills:
            result.loaded_skills.append(skill.name)
        return skill.body

    def _complete(
        self, messages: list[dict[str, Any]], tools: list[dict[str, Any]] | None, repeat: int
    ) -> tuple[dict[str, Any], float, bool]:
        kwargs: dict[str, Any] = {"model": self.model, "messages": messages, **self.params}
        if tools:
            kwargs["tools"] = tools
        if self.extra_body:
            kwargs["extra_body"] = self.extra_body

        key = None
        if self.cache is not None:
            key = Cache.key({"request": kwargs, "repeat": repeat})
            hit = self.cache.get(key)
            if hit is not None:
                return hit["response"], hit["latency_s"], True
        if self.cache_only:
            raise CacheMiss(self.model)

        started = time.perf_counter()
        response = self.client.chat.completions.create(**kwargs)
        latency = time.perf_counter() - started
        data = response.model_dump() if hasattr(response, "model_dump") else dict(response)

        if self.cache is not None and key is not None:
            self.cache.set(key, {"response": data, "latency_s": latency})
        return data, latency, False

    def _usage(self, response: dict[str, Any]) -> Usage:
        raw = response.get("usage") or {}
        usage = Usage(
            input_tokens=int(raw.get("prompt_tokens") or 0),
            output_tokens=int(raw.get("completion_tokens") or 0),
        )
        if raw.get("cost") is not None:  # OpenRouter reports the billed cost directly
            usage.cost_usd = float(raw["cost"])
        elif self.price_in is not None and self.price_out is not None:
            usage.cost_usd = (usage.input_tokens * self.price_in + usage.output_tokens * self.price_out) / 1e6
        return usage
