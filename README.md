# AI Equity Intelligence

An event-centric equity intelligence platform for Indian markets with global context. The system collects market artifacts, normalizes them, extracts structured events, generates signals, scores opportunities and risks, and presents traceable investor intelligence.

This is an intelligence system, not a trading recommendation engine. Every insight is designed to include evidence, confidence, reasoning, and watch points.

## Repository Layout

```text
backend/     FastAPI modular monolith
frontend/    Next.js dashboard and conversational UI
infra/       Docker Compose and service config
docs/        Architecture and product notes
scripts/     Developer utilities
tests/       Backend tests
data/        Local development data
```

## Quick Start

Backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Infrastructure:

```bash
docker compose -f infra/docker-compose.yml up
```

## Core Flow

```text
Documents -> Events -> Signals -> Intelligence -> Opportunities -> Risks -> Insights
```

LLMs are used behind the AI gateway only. Structured documents and events remain the source of truth.
