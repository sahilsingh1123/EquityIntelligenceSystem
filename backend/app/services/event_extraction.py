from datetime import UTC, datetime
from concurrent.futures import ThreadPoolExecutor
import asyncio

from pydantic import BaseModel, Field, AliasChoices, field_validator
from app.core.enums import EventType, Sentiment
from app.models.schemas import Event, Evidence, NormalizedDocument
from app.core.ai.factory import create_ai_client


class ExtractedEventItem(BaseModel):
    company_name: str = Field(
        validation_alias=AliasChoices("company_name", "companyName", "company"),
        description="Name of the company/stock impacted, e.g. 'Infosys', 'Reliance', 'TCS'. If it is a global macro event, set it as 'Market' or 'Macro'."
    )
    event_type: EventType = Field(
        validation_alias=AliasChoices("event_type", "eventType", "type", "event"),
        description="Type of the market event."
    )
    sentiment: Sentiment = Field(
        validation_alias=AliasChoices("sentiment"),
        description="Market sentiment associated with this event."
    )
    confidence: int = Field(
        validation_alias=AliasChoices("confidence"),
        description="Confidence percentage (0 to 100).",
        ge=0,
        le=100
    )
    importance: int = Field(
        validation_alias=AliasChoices("importance"),
        description="Importance percentage (0 to 100).",
        ge=0,
        le=100
    )
    summary: str = Field(
        validation_alias=AliasChoices("summary"),
        description="A concise summary of what happened and why it affects the stock/company."
    )

    @field_validator("event_type", mode="before")
    @classmethod
    def normalize_event_type(cls, value: str) -> str:
        if not isinstance(value, str):
            return "MACRO_EVENT"
        val = value.upper().strip().replace(" ", "_")
        valid_types = {e.value for e in EventType}
        if val in valid_types:
            return val
        for vt in valid_types:
            if vt in val or val in vt:
                return vt
        if "EARNINGS" in val:
            return "EARNINGS_BEAT" if "BEAT" in val or "GOOD" in val or "STRONG" in val else "EARNINGS_MISS"
        if "CONTRACT" in val or "ORDER" in val or "WIN" in val:
            return "CONTRACT_WIN"
        if "DIVIDEND" in val:
            return "DIVIDEND"
        if "GUIDANCE" in val:
            return "GUIDANCE_UPGRADE" if "UP" in val or "RAISE" in val or "HIGHER" in val else "GUIDANCE_DOWNGRADE"
        if "MANAGEMENT" in val or "CEO" in val or "RESIGN" in val:
            return "MANAGEMENT_CHANGE"
        if "REGULATORY" in val or "PENALTY" in val or "FINE" in val or "NOTICE" in val:
            return "REGULATORY_ACTION"
        return "MACRO_EVENT"

    @field_validator("sentiment", mode="before")
    @classmethod
    def normalize_sentiment(cls, value: str) -> str:
        if not isinstance(value, str):
            return "NEUTRAL"
        val = value.upper().strip()
        if val in {s.value for s in Sentiment}:
            return val
        if "POS" in val or "BULL" in val or "GOOD" in val:
            return "POSITIVE"
        if "NEG" in val or "BEAR" in val or "BAD" in val:
            return "NEGATIVE"
        if "UNCERTAIN" in val or "RISK" in val:
            return "UNCERTAIN"
        return "NEUTRAL"


class ExtractedEventsList(BaseModel):
    events: list[ExtractedEventItem] = Field(description="List of extracted events from the text.")


def run_sync(coro):
    """Safely executes an async coroutine synchronously, even inside a running event loop."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(lambda: asyncio.run(coro))
            return future.result()
    else:
        return asyncio.run(coro)


class EventExtractionService:
    def __init__(self) -> None:
        try:
            self.ai_client = create_ai_client()
            print(f"[EventExtractionService] Initialized AI Client with model: {self.ai_client.model_name}")
        except Exception as e:
            print(f"[EventExtractionService] Failed to initialize AI client: {e}. Falling back to rule-based.")
            self.ai_client = None

        self.positive_keywords = {
            EventType.EARNINGS_BEAT: ["beat", "above estimate", "record profit", "strong earnings"],
            EventType.CONTRACT_WIN: ["contract win", "order win", "wins contract", "large deal"],
            EventType.BUYBACK: ["buyback"],
            EventType.DIVIDEND: ["dividend"],
            EventType.GUIDANCE_UPGRADE: ["raises guidance", "guidance upgrade"],
        }
        self.negative_keywords = {
            EventType.EARNINGS_MISS: ["miss", "below estimate", "weak earnings"],
            EventType.GUIDANCE_DOWNGRADE: ["cuts guidance", "guidance cut", "lowers guidance"],
            EventType.REGULATORY_ACTION: ["regulatory action", "penalty", "show cause"],
            EventType.LITIGATION: ["litigation", "lawsuit"],
            EventType.DEBT_ISSUE: ["debt increase", "raises debt"],
            EventType.MANAGEMENT_CHANGE: ["resigns", "resignation", "management exit"],
        }

    def extract(self, document: NormalizedDocument) -> list[Event]:
        if self.ai_client:
            try:
                events = run_sync(self._ai_extract(document))
                if events:
                    print(f"[EventExtractionService] Successfully extracted {len(events)} events using AI.")
                    return events
            except Exception as e:
                print(f"[EventExtractionService] AI extraction failed: {e}. Falling back to rules.")

        return self._rule_extract(document)

    async def _ai_extract(self, document: NormalizedDocument) -> list[Event]:
        prompt = (
            f"You are a senior equity intelligence analyst specializing in Indian stock markets.\n"
            f"Analyze the document title and content below, and extract a list of structured events.\n\n"
            f"Document Title: {document.title}\n"
            f"Document Content: {document.content}\n"
        )
        system_prompt = (
            "You extract structured market and corporate events from financial news or filings.\n"
            "Return a list of events matching the required JSON schema. If no events are relevant, "
            "return an empty list."
        )

        extracted: ExtractedEventsList = await self.ai_client.generate_structured(
            prompt=prompt,
            response_model=ExtractedEventsList,
            system_prompt=system_prompt,
        )

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
        for item in extracted.events:
            events.append(
                Event(
                    company_name=item.company_name,
                    event_type=item.event_type,
                    event_date=document.published_at or datetime.now(UTC),
                    sentiment=item.sentiment,
                    confidence=item.confidence,
                    importance=item.importance,
                    summary=item.summary,
                    evidence=evidence,
                )
            )
        return events

    def _rule_extract(self, document: NormalizedDocument) -> list[Event]:
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

