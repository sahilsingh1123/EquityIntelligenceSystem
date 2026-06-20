from hashlib import sha256

from app.models.schemas import DocumentCreate, NormalizedDocument


class NormalizationService:
    def normalize(self, payload: DocumentCreate) -> NormalizedDocument:
        text = " ".join(payload.content.split())
        checksum_source = f"{payload.source.name}|{payload.title}|{text}".encode()
        data = payload.model_dump()
        data["content"] = text
        return NormalizedDocument(
            **data,
            checksum=sha256(checksum_source).hexdigest(),
        )
