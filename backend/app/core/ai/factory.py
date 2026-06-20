from app.core.ai.base import BaseAIClient
from app.core.ai.gemini import GeminiClient
from app.core.ai.groq import GroqClient
from app.core.ai.ollama import OllamaClient
from app.core.config import settings


def create_ai_client(provider: str | None = None) -> BaseAIClient:
    provider = provider or settings.ai_provider or "ollama"

    if provider == "ollama":
        return OllamaClient(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
        )
    elif provider == "gemini":
        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is required when ai_provider='gemini'"
            )
        return GeminiClient(
            api_key=settings.gemini_api_key,
            model=settings.gemini_model,
        )
    elif provider == "groq":
        if not settings.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY is required when ai_provider='groq'"
            )
        return GroqClient(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
        )
    else:
        raise ValueError(
            f"Unknown AI provider: {provider}. "
            f"Expected one of: ollama, gemini, groq"
        )
