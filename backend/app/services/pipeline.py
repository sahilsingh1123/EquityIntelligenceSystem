from app.models.schemas import (
    ChatAnswer,
    Company,
    DailyReport,
    DocumentCreate,
    Event,
    Insight,
    NormalizedDocument,
    Opportunity,
    Risk,
    Signal,
)
from app.repositories.memory import IntelligenceRepository
from app.services.chat import ChatService
from app.services.event_extraction import EventExtractionService
from app.services.insights import InsightService
from app.services.normalization import NormalizationService
from app.services.scoring import OpportunityService, RiskService
from app.services.signals import SignalService


class IntelligencePipeline:
    def __init__(self, repository: IntelligenceRepository) -> None:
        self.repository = repository
        self.normalizer = NormalizationService()
        self.extractor = EventExtractionService()
        self.signal_service = SignalService()
        self.opportunity_service = OpportunityService()
        self.risk_service = RiskService()
        self.insight_service = InsightService()
        self.chat_service = ChatService()

    def ingest_document(self, payload: DocumentCreate) -> NormalizedDocument:
        document = self.normalizer.normalize(payload)
        self.repository.add_document(document)

        for event in self.extractor.extract(document):
            self.repository.add_event(event)
            self.repository.add_signal(self.signal_service.from_event(event))
            self.repository.add_insight(self.insight_service.from_event(event))

        self.refresh_scores()
        return document

    def refresh_scores(self) -> None:
        self.repository.opportunities.clear()
        self.repository.risks.clear()
        for company_name, events in self.repository.list_events_by_company().items():
            self.repository.add_opportunity(self.opportunity_service.score(company_name, events))
            self.repository.add_risk(self.risk_service.score(company_name, events))

    def add_company(self, company: Company) -> Company:
        return self.repository.add_company(company)

    def answer(self, question: str) -> ChatAnswer:
        return self.chat_service.answer(question, self.repository.list_insights())

    def daily_report(self) -> DailyReport:
        insights = self.repository.list_insights()
        events = self.repository.list_events()
        return DailyReport(
            market_summary=(
                f"{len(events)} structured events generated {len(insights)} explainable insights."
            ),
            top_opportunities=self.repository.list_opportunities()[:5],
            top_risks=self.repository.list_risks()[:5],
            major_events=events[:10],
            insights=insights[:10],
        )

    def list_events(self) -> list[Event]:
        return self.repository.list_events()

    def list_signals(self) -> list[Signal]:
        return self.repository.list_signals()

    def list_opportunities(self) -> list[Opportunity]:
        return self.repository.list_opportunities()

    def list_risks(self) -> list[Risk]:
        return self.repository.list_risks()

    def list_insights(self) -> list[Insight]:
        return self.repository.list_insights()
