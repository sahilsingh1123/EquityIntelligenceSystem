from typing import Any

from groq import AsyncGroq
from pydantic import TypeAdapter

from app.core.ai.base import BaseAIClient, T

GROQ_DEFAULT_MODEL = "llama-3.3-70b-versatile"


class GroqClient(BaseAIClient):
    def __init__(
        self,
        api_key: str,
        model: str = GROQ_DEFAULT_MODEL,
    ) -> None:
        self._model = model
        self._client = AsyncGroq(api_key=api_key)

    @property
    def model_name(self) -> str:
        return self._model

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> str:
        model = kwargs.get("model", self._model)
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        completion = await self._client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return completion.choices[0].message.content or ""

    async def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> T:
        model = kwargs.get("model", self._model)
        messages: list[dict[str, str]] = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        format_instruction = (
            "Respond with valid JSON that matches the required schema. "
            "Do not include any text outside the JSON object."
        )
        combined_prompt = f"{prompt}\n\n{format_instruction}"
        messages.append({"role": "user", "content": combined_prompt})

        completion = await self._client.chat.completions.create(
            model=model,
            messages=messages,
            response_format={"type": "json_object"},
        )
        raw = completion.choices[0].message.content or ""
        adapter: TypeAdapter[T] = TypeAdapter(response_model)
        return adapter.validate_json(raw)

    async def chat(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> str:
        model = kwargs.get("model", self._model)
        completion = await self._client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return completion.choices[0].message.content or ""
