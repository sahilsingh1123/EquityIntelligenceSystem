from typing import Any

from google import genai
from google.genai import types
from pydantic import TypeAdapter

from app.core.ai.base import BaseAIClient, T

GEMINI_DEFAULT_MODEL = "gemini-2.0-flash"


class GeminiClient(BaseAIClient):
    def __init__(
        self,
        api_key: str,
        model: str = GEMINI_DEFAULT_MODEL,
    ) -> None:
        self._model = model
        self._client = genai.Client(api_key=api_key)

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
        contents = prompt
        config = None

        if system_prompt:
            config = types.GenerateContentConfig(system_instruction=system_prompt)

        response = await self._client.aio.models.generate_content(
            model=model,
            contents=contents,
            config=config,
        )
        return response.text or ""

    async def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> T:
        model = kwargs.get("model", self._model)
        config_kwargs: dict[str, Any] = {
            "response_mime_type": "application/json",
            "response_schema": response_model,
        }
        if system_prompt:
            config_kwargs["system_instruction"] = system_prompt

        response = await self._client.aio.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )
        raw = response.text or ""
        adapter: TypeAdapter[T] = TypeAdapter(response_model)
        return adapter.validate_json(raw)

    async def chat(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> str:
        model = kwargs.get("model", self._model)
        history: list[types.Content] = []
        system_instruction: str | None = None

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                system_instruction = content
                continue

            parts = [types.Part.from_text(text=content)]
            role_map = {"user": "user", "assistant": "model"}
            mapped_role = role_map.get(role, "user")
            history.append(types.Content(role=mapped_role, parts=parts))

        config = None
        if system_instruction:
            config = types.GenerateContentConfig(
                system_instruction=system_instruction
            )

        chat_session = self._client.aio.chats.create(
            model=model,
            history=history[:-1] if len(history) > 1 else [],
            config=config,
        )

        last_message = history[-1].parts[0].text if history else ""
        response = await chat_session.send_message(last_message)
        return response.text or ""
