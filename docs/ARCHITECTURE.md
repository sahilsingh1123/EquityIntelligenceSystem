# AI Equity Intelligence Architecture

Version: 0.1 implementation baseline

## Architecture Philosophy

The platform follows an event-centric intelligence architecture:

```text
Documents -> Events -> Signals -> Intelligence -> Opportunities -> Risks -> Insights
```

The system should reason from structured events whenever possible. LLM outputs are never the source of truth; they are helpers for extraction, summarization, reasoning, and conversational responses through a shared AI gateway.

## Technology Stack

- Backend: Python 3.13, FastAPI, Pydantic v2, SQLAlchemy 2.x
- Data: PostgreSQL, Redis, OpenSearch, object storage
- AI: OpenAI and Anthropic behind a provider-agnostic gateway
- Frontend: Next.js, TypeScript, Tailwind, shadcn-compatible primitives
- Deployment: Docker Compose locally, AWS later

## Backend Modules

- `api`: Versioned HTTP routes. Routes delegate to services.
- `ingestion`: Source adapters for NSE, BSE, news, earnings, macro, and social sources.
- `extraction`: Document-to-event extraction.
- `graph`: Knowledge graph nodes and relationships.
- `intelligence`: Signal, risk, opportunity, and insight engines.
- `rag`: Chunking, retrieval, context building, and citation injection.
- `reports`: Daily intelligence report generation.
- `chat`: Conversational query planning and response generation.
- `services`: Business logic and orchestration.
- `repositories`: Persistence adapters.

## API Surface

- `GET /health`
- `POST /api/v1/companies`
- `POST /api/v1/documents`
- `GET /api/v1/events`
- `GET /api/v1/signals`
- `GET /api/v1/opportunities`
- `GET /api/v1/risks`
- `GET /api/v1/insights`
- `POST /api/v1/chat`
- `GET /api/v1/reports/daily`

## Current Implementation Notes

The first implementation uses an in-memory repository and a deterministic rule-based event extractor. This keeps the product runnable while preserving the service boundaries needed for database persistence, queue workers, and AI extraction.

Next backend milestones:

1. Add SQLAlchemy persistence and Alembic migrations.
2. Implement source-specific ingestion adapters with checkpointing.
3. Add AI gateway with model routing, retries, cost logging, and prompt registry.
4. Add OpenSearch indexing and retrieval.
5. Add JWT auth, rate limiting, and audit logging.

## Engineering Rule

Business logic belongs in services. Routes, schedulers, and workers should orchestrate only.
