from datetime import UTC, datetime

from app.core.enums import EventType, Sentiment
from app.models.schemas import Event, Evidence, NormalizedDocument


class EventExtractionService:
    """Rule-based extractor used until the AI gateway implementation is connected."""

    positive_keywords = {
        EventType.EARNINGS_BEAT: ["beat", "above estimate", "record profit", "strong earnings"],
        EventType.CONTRACT_WIN: ["contract win", "order win", "wins contract", "large deal"],
        EventType.BUYBACK: ["buyback"],
        EventType.DIVIDEND: ["dividend"],
        EventType.GUIDANCE_UPGRADE: ["raises guidance", "guidance upgrade"],
    }
    negative_keywords = {
        EventType.EARNINGS_MISS: ["miss", "below estimate", "weak earnings"],
        EventType.GUIDANCE_DOWNGRADE: ["cuts guidance", "guidance cut", "lowers guidance"],
        EventType.REGULATORY_ACTION: ["regulatory action", "penalty", "show cause"],
        EventType.LITIGATION: ["litigation", "lawsuit"],
        EventType.DEBT_ISSUE: ["debt increase", "raises debt"],
        EventType.MANAGEMENT_CHANGE: ["resigns", "resignation", "management exit"],
    }

    def extract(self, document: NormalizedDocument) -> list[Event]:
        lowered = f"{document.title} {document.content}".casefold()
        company = self._detect_company(document)
        evidence = [
            Evidence(
                document_id=document.document_id,
                source=document.source.name,
                title=document.title,
                url=document.url,
                excerpt=document.content[:280],
            )
        ]

        events: list[Event] = []
        for event_type, keywords in self.positive_keywords.items():
            if any(keyword in lowered for keyword in keywords):
                events.append(
                    self._build_event(document, company, event_type, Sentiment.POSITIVE, evidence)
                )

        for event_type, keywords in self.negative_keywords.items():
            if any(keyword in lowered for keyword in keywords):
                events.append(
                    self._build_event(document, company, event_type, Sentiment.NEGATIVE, evidence)
                )

        if not events and any(token in lowered for token in ["fed", "oil", "tariff", "yen", "dollar"]):
            events.append(
                self._build_event(document, company, EventType.MACRO_EVENT, Sentiment.UNCERTAIN, evidence)
            )

        return events

    def _build_event(
        self,
        document: NormalizedDocument,
        company_name: str,
        event_type: EventType,
        sentiment: Sentiment,
        evidence: list[Evidence],
    ) -> Event:
        trust_boost = document.source.trust_weight * 5
        confidence = min(95, 45 + trust_boost)
        return Event(
            company_name=company_name,
            event_type=event_type,
            event_date=document.published_at or datetime.now(UTC),
            sentiment=sentiment,
            confidence=confidence,
            importance=min(90, confidence + 5),
            summary=f"{company_name}: {event_type.value.replace('_', ' ').title()} detected from {document.source.name}.",
            evidence=evidence,
        )

    def _detect_company(self, document: NormalizedDocument) -> str:
        metadata_company = document.metadata.get("company")
        if isinstance(metadata_company, str) and metadata_company.strip():
            return metadata_company.strip()

        title_tokens = document.title.replace(":", " ").split()
        return " ".join(title_tokens[:2]) if title_tokens else "Market"
