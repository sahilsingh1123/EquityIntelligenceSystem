from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl

from app.core.enums import EventType, Market, Sentiment, SignalType, SourceTrustTier, SourceType


class Company(BaseModel):
    company_id: UUID = Field(default_factory=uuid4)
    ticker: str
    name: str
    sector: str
    industry: str
    country: Market = Market.INDIA
    market_cap: float | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Source(BaseModel):
    name: str
    url: HttpUrl | None = None
    trust_tier: SourceTrustTier = SourceTrustTier.TIER_3
    trust_weight: int = Field(default=8, ge=1, le=10)


class DocumentCreate(BaseModel):
    source: Source
    source_type: SourceType
    url: HttpUrl | None = None
    title: str
    content: str
    published_at: datetime
    language: str = "en"
    metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)


class NormalizedDocument(DocumentCreate):
    document_id: UUID = Field(default_factory=uuid4)
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    checksum: str


class Evidence(BaseModel):
    document_id: UUID
    source: str
    title: str
    url: HttpUrl | None = None
    excerpt: str


class Event(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    company_id: UUID | None = None
    company_name: str
    event_type: EventType
    event_date: datetime
    sentiment: Sentiment
    confidence: int = Field(ge=0, le=100)
    importance: int = Field(ge=0, le=100)
    summary: str
    evidence: list[Evidence]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Signal(BaseModel):
    signal_id: UUID = Field(default_factory=uuid4)
    company_id: UUID | None = None
    company_name: str
    signal_type: SignalType
    strength: int = Field(ge=0, le=100)
    confidence: int = Field(ge=0, le=100)
    reason: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Opportunity(BaseModel):
    opportunity_id: UUID = Field(default_factory=uuid4)
    company_id: UUID | None = None
    company_name: str
    score: int = Field(ge=0, le=100)
    confidence: int = Field(ge=0, le=100)
    reason: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Risk(BaseModel):
    risk_id: UUID = Field(default_factory=uuid4)
    company_id: UUID | None = None
    company_name: str
    score: int = Field(ge=0, le=100)
    confidence: int = Field(ge=0, le=100)
    reason: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Insight(BaseModel):
    insight_id: UUID = Field(default_factory=uuid4)
    title: str
    what_happened: str
    why_it_matters: str
    potential_impact: str
    confidence: int = Field(ge=0, le=100)
    importance: int = Field(ge=0, le=100)
    watch_points: list[str]
    evidence: list[Evidence]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ChatQuestion(BaseModel):
    question: str


class ChatAnswer(BaseModel):
    answer: str
    confidence: int = Field(ge=0, le=100)
    citations: list[Evidence]


class DailyReport(BaseModel):
    report_id: UUID = Field(default_factory=uuid4)
    market_summary: str
    top_opportunities: list[Opportunity]
    top_risks: list[Risk]
    major_events: list[Event]
    insights: list[Insight]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
