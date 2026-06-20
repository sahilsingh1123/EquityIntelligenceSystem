from collections import defaultdict
from uuid import UUID

from app.models.schemas import (
    Company,
    Event,
    Insight,
    NormalizedDocument,
    Opportunity,
    Risk,
    Signal,
)


class IntelligenceRepository:
    def __init__(self) -> None:
        self.companies: dict[UUID, Company] = {}
        self.documents: dict[UUID, NormalizedDocument] = {}
        self.events: dict[UUID, Event] = {}
        self.signals: dict[UUID, Signal] = {}
        self.opportunities: dict[UUID, Opportunity] = {}
        self.risks: dict[UUID, Risk] = {}
        self.insights: dict[UUID, Insight] = {}

    def add_company(self, company: Company) -> Company:
        self.companies[company.company_id] = company
        return company

    def list_companies(self) -> list[Company]:
        return sorted(self.companies.values(), key=lambda item: item.name)

    def find_company_by_name(self, name: str) -> Company | None:
        normalized = name.casefold()
        return next(
            (company for company in self.companies.values() if company.name.casefold() == normalized),
            None,
        )

    def add_document(self, document: NormalizedDocument) -> NormalizedDocument:
        self.documents[document.document_id] = document
        return document

    def list_documents(self) -> list[NormalizedDocument]:
        return sorted(self.documents.values(), key=lambda item: item.published_at, reverse=True)

    def add_event(self, event: Event) -> Event:
        self.events[event.event_id] = event
        return event

    def list_events(self) -> list[Event]:
        return sorted(self.events.values(), key=lambda item: item.event_date, reverse=True)

    def list_events_by_company(self) -> dict[str, list[Event]]:
        grouped: dict[str, list[Event]] = defaultdict(list)
        for event in self.events.values():
            grouped[event.company_name].append(event)
        return grouped

    def add_signal(self, signal: Signal) -> Signal:
        self.signals[signal.signal_id] = signal
        return signal

    def list_signals(self) -> list[Signal]:
        return sorted(self.signals.values(), key=lambda item: item.created_at, reverse=True)

    def add_opportunity(self, opportunity: Opportunity) -> Opportunity:
        self.opportunities[opportunity.opportunity_id] = opportunity
        return opportunity

    def list_opportunities(self) -> list[Opportunity]:
        return sorted(self.opportunities.values(), key=lambda item: item.score, reverse=True)

    def add_risk(self, risk: Risk) -> Risk:
        self.risks[risk.risk_id] = risk
        return risk

    def list_risks(self) -> list[Risk]:
        return sorted(self.risks.values(), key=lambda item: item.score, reverse=True)

    def add_insight(self, insight: Insight) -> Insight:
        self.insights[insight.insight_id] = insight
        return insight

    def list_insights(self) -> list[Insight]:
        return sorted(self.insights.values(), key=lambda item: item.importance, reverse=True)


repository = IntelligenceRepository()
