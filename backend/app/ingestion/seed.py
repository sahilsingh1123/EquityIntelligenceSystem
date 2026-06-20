from datetime import UTC, datetime

from app.core.enums import SourceTrustTier, SourceType
from app.models.schemas import DocumentCreate, Source


def seed_documents() -> list[DocumentCreate]:
    return [
        DocumentCreate(
            source=Source(name="NSE Filing", trust_tier=SourceTrustTier.TIER_1, trust_weight=10),
            source_type=SourceType.FILING,
            title="Infosys wins large cloud transformation contract",
            content=(
                "Infosys announced an order win and large deal with a global manufacturer. "
                "Management said the contract improves revenue visibility."
            ),
            published_at=datetime(2026, 6, 7, 10, 30, tzinfo=UTC),
            metadata={"company": "Infosys"},
        ),
        DocumentCreate(
            source=Source(name="BSE Filing", trust_tier=SourceTrustTier.TIER_1, trust_weight=10),
            source_type=SourceType.REGULATORY_UPDATE,
            title="ABC Bank receives regulatory action notice",
            content=(
                "ABC Bank disclosed a regulatory action and show cause notice related to "
                "compliance processes. The bank said it is reviewing the matter."
            ),
            published_at=datetime(2026, 6, 7, 12, 0, tzinfo=UTC),
            metadata={"company": "ABC Bank"},
        ),
        DocumentCreate(
            source=Source(name="Macro Desk", trust_tier=SourceTrustTier.TIER_3, trust_weight=8),
            source_type=SourceType.MACRO_REPORT,
            title="Oil price increase raises pressure on airline margins",
            content=(
                "Oil prices increased after geopolitical supply concerns. Higher crude can "
                "pressure transportation costs and airline margins in India."
            ),
            published_at=datetime(2026, 6, 7, 15, 0, tzinfo=UTC),
            metadata={"company": "Indian Airlines"},
        ),
    ]
