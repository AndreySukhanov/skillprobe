"""A scripted stand-in for openai.OpenAI: returns queued responses and records requests."""

from __future__ import annotations

import json
from typing import Any


def text(content: str, prompt_tokens: int = 10, completion_tokens: int = 5, cost: float | None = None) -> dict:
    usage: dict[str, Any] = {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens}
    if cost is not None:
        usage["cost"] = cost
    return {"choices": [{"message": {"role": "assistant", "content": content}}], "usage": usage}


def load(skill_name: str, call_id: str = "call_1") -> dict:
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": call_id,
                            "type": "function",
                            "function": {"name": "load_skill", "arguments": json.dumps({"name": skill_name})},
                        }
                    ],
                }
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 3},
    }


class _Completions:
    def __init__(self, responder):
        self.responder = responder
        self.requests: list[dict] = []

    def create(self, **kwargs):
        self.requests.append(json.loads(json.dumps(kwargs, default=str)))
        return self.responder(kwargs)


class _Chat:
    def __init__(self, responder):
        self.completions = _Completions(responder)


class FakeClient:
    """`responder(kwargs) -> dict` decides each reply; `script(...)` replays a fixed list."""

    def __init__(self, responder):
        self.chat = _Chat(responder)

    @classmethod
    def script(cls, *responses: dict) -> "FakeClient":
        queue = list(responses)
        return cls(lambda kwargs: queue.pop(0))

    @property
    def requests(self) -> list[dict]:
        return self.chat.completions.requests
