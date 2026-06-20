from datetime import UTC, datetime

from app.core.enums import SourceTrustTier, SourceType
from app.models.schemas import DocumentCreate, Source
from app.repositories.memory import IntelligenceRepository
from app.services.pipeline import IntelligencePipeline


def test_pipeline_generates_events_signals_scores_and_insights() -> None:
    pipeline = IntelligencePipeline(IntelligenceRepository())
    payload = DocumentCreate(
        source=Source(name="NSE Filing", trust_tier=SourceTrustTier.TIER_1, trust_weight=10),
        source_type=SourceType.FILING,
        title="TCS reports earnings beat",
        content="TCS delivered strong earnings above estimate and raises guidance.",
        published_at=datetime(2026, 6, 7, tzinfo=UTC),
        metadata={"company": "TCS"},
    )

    document = pipeline.ingest_document(payload)

    assert document.checksum
    assert len(pipeline.list_events()) == 2
    assert len(pipeline.list_signals()) == 2
    assert len(pipeline.list_insights()) == 2
    assert pipeline.list_opportunities()[0].score > 50
    assert pipeline.daily_report().major_events
