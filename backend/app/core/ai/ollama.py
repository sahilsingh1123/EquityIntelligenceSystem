from typing import Any

import httpx
from pydantic import TypeAdapter

from app.core.ai.base import BaseAIClient, T

OLLAMA_DEFAULT_MODEL = "llama3.2"
OLLAMA_DEFAULT_BASE_URL = "http://localhost:11434"


class OllamaClient(BaseAIClient):
    def __init__(
        self,
        base_url: str = OLLAMA_DEFAULT_BASE_URL,
        model: str = OLLAMA_DEFAULT_MODEL,
        timeout: int = 120,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._timeout = timeout

    @property
    def model_name(self) -> str:
        return self._model

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> str:
        payload: dict[str, Any] = {
            "model": kwargs.get("model", self._model),
            "prompt": prompt,
            "stream": False,
        }
        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(
            base_url=self._base_url, timeout=self._timeout
        ) as client:
            resp = await client.post("/api/generate", json=payload)
            resp.raise_for_status()
            data = resp.json()
        return data.get("response", "")

    async def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> T:
        format_prompt = prompt
        if system_prompt:
            format_prompt = f"{system_prompt}\n\n{prompt}"

        payload: dict[str, Any] = {
            "model": kwargs.get("model", self._model),
            "prompt": format_prompt,
            "format": "json",
            "stream": False,
        }
        if system_prompt and "system" not in payload:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(
            base_url=self._base_url, timeout=self._timeout
        ) as client:
            resp = await client.post("/api/generate", json=payload)
            resp.raise_for_status()
            data = resp.json()

        raw = data.get("response", "")
        adapter: TypeAdapter[T] = TypeAdapter(response_model)
        return adapter.validate_json(raw)

    async def chat(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> str:
        payload: dict[str, Any] = {
            "model": kwargs.get("model", self._model),
            "messages": messages,
            "stream": False,
        }

        async with httpx.AsyncClient(
            base_url=self._base_url, timeout=self._timeout
        ) as client:
            resp = await client.post("/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()

        message = data.get("message", {})
        return message.get("content", "")

    async def embed(self, text: str) -> list[float]:
        payload = {
            "model": self._model,
            "prompt": text,
        }
        async with httpx.AsyncClient(
            base_url=self._base_url, timeout=self._timeout
        ) as client:
            resp = await client.post("/api/embeddings", json=payload)
            resp.raise_for_status()
            data = resp.json()
        return data.get("embedding", [])
