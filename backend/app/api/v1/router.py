from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_pipeline
from app.models.schemas import (
    ChatAnswer,
    ChatQuestion,
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
from app.services.pipeline import IntelligencePipeline

api_router = APIRouter()


@api_router.post("/companies", response_model=Company, tags=["companies"])
async def create_company(
    company: Company,
    pipeline: IntelligencePipeline = Depends(get_pipeline),
) -> Company:
    return pipeline.add_company(company)


@api_router.get("/events", response_model=list[Event], tags=["events"])
async def list_events(pipeline: IntelligencePipeline = Depends(get_pipeline)) -> list[Event]:
    return pipeline.list_events()


@api_router.post("/documents", response_model=NormalizedDocument, tags=["documents"])
async def ingest_document(
    payload: DocumentCreate,
    pipeline: IntelligencePipeline = Depends(get_pipeline),
) -> NormalizedDocument:
    return pipeline.ingest_document(payload)


@api_router.get("/signals", response_model=list[Signal], tags=["signals"])
async def list_signals(pipeline: IntelligencePipeline = Depends(get_pipeline)) -> list[Signal]:
    return pipeline.list_signals()


@api_router.get("/opportunities", response_model=list[Opportunity], tags=["opportunities"])
async def list_opportunities(
    pipeline: IntelligencePipeline = Depends(get_pipeline),
) -> list[Opportunity]:
    return pipeline.list_opportunities()


@api_router.get("/risks", response_model=list[Risk], tags=["risks"])
async def list_risks(pipeline: IntelligencePipeline = Depends(get_pipeline)) -> list[Risk]:
    return pipeline.list_risks()


@api_router.get("/insights", response_model=list[Insight], tags=["insights"])
async def list_insights(pipeline: IntelligencePipeline = Depends(get_pipeline)) -> list[Insight]:
    return pipeline.list_insights()


@api_router.post("/chat", response_model=ChatAnswer, tags=["chat"])
async def chat(
    payload: ChatQuestion,
    pipeline: IntelligencePipeline = Depends(get_pipeline),
) -> ChatAnswer:
    return pipeline.answer(payload.question)


@api_router.get("/reports/daily", response_model=DailyReport, tags=["reports"])
async def daily_report(pipeline: IntelligencePipeline = Depends(get_pipeline)) -> DailyReport:
    return pipeline.daily_report()
