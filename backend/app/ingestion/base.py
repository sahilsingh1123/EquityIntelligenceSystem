from abc import ABC, abstractmethod

from app.models.schemas import DocumentCreate


class IngestionSource(ABC):
    @abstractmethod
    async def fetch(self) -> list[DocumentCreate]:
        """Fetch incremental documents from the source."""
