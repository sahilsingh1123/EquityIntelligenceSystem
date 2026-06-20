#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# ── Config ─────────────────────────────────────────────────────
INFRA=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --infra|-i) INFRA=true; shift ;;
    *) echo "Usage: $0 [--infra|-i]"; exit 1 ;;
  esac
done

# ── Colors ─────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
info()  { printf "${GREEN}%s${NC}\n" "$*"; }
warn()  { printf "${YELLOW}%s${NC}\n" "$*"; }
error() { printf "${RED}%s${NC}\n" "$*"; exit 1; }

# ── Prerequisites ──────────────────────────────────────────────
command -v python3 >/dev/null 2>&1 || error "python3 is required"
command -v node    >/dev/null 2>&1 || error "node is required"
command -v npm     >/dev/null 2>&1 || error "npm is required"

PY_VER=$(python3 --version 2>&1 | cut -d' ' -f2)
PY_MAJOR=$(echo "$PY_VER" | cut -d'.' -f1)
PY_MINOR=$(echo "$PY_VER" | cut -d'.' -f2)
[[ $PY_MAJOR -ge 3 && $PY_MINOR -ge 13 ]] || error "Python 3.13+ required (found $PY_VER)"

NODE_VER=$(node --version 2>&1 | cut -d'v' -f2)
NODE_MAJOR=$(echo "$NODE_VER" | cut -d'.' -f1)
[[ $NODE_MAJOR -ge 22 ]] || error "Node 22+ required (found v$NODE_VER)"

mkdir -p logs

# ── Backend setup ──────────────────────────────────────────────
info "Setting up backend..."
cd "$ROOT/backend"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
if [[ ! -f .venv/.installed ]]; then
  .venv/bin/pip install -e ".[dev]" --quiet
  touch .venv/.installed
fi
if [[ ! -f .env ]]; then
  cp .env.example .env
  warn "Created backend/.env \u2014 configure OPENAI_API_KEY / ANTHROPIC_API_KEY if needed"
fi

# ── Frontend setup ─────────────────────────────────────────────
info "Setting up frontend..."
cd "$ROOT/frontend"

if [[ ! -d node_modules ]]; then
  npm install --silent
fi
if [[ ! -f .env.local ]]; then
  cp .env.example .env.local
fi

# ── Start ──────────────────────────────────────────────────────
cd "$ROOT"
rm -f logs/.pids

if $INFRA; then
  command -v docker >/dev/null 2>&1 || error "docker is required for --infra mode"
  info "Starting Docker infrastructure (PostgreSQL + Redis + OpenSearch)..."
  docker compose -f infra/docker-compose.yml up -d
  echo "INFRA=true" >> logs/.pids
fi

info "Starting backend..."
cd "$ROOT/backend"
nohup .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 \
  > "$ROOT/logs/backend.log" 2>&1 &
BACKEND_PID=$!
echo "BACKEND_PID=$BACKEND_PID" >> "$ROOT/logs/.pids"
cd "$ROOT"

info "Starting frontend..."
cd "$ROOT/frontend"
nohup npm run dev > "$ROOT/logs/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo "FRONTEND_PID=$FRONTEND_PID" >> "$ROOT/logs/.pids"
cd "$ROOT"

# ── Health checks ──────────────────────────────────────────────
info "Waiting for services..."

for ((i=0; i<30; i++)); do
  if curl -sf http://localhost:8000/health >/dev/null 2>&1; then
    info "  \u2713 Backend ready  \u2192 http://localhost:8000"
    break
  fi
  if [[ $i -eq 29 ]]; then
    warn "  \u26a0 Backend check timed out \u2014 tail logs/backend.log"
  fi
  sleep 1
done

for ((i=0; i<60; i++)); do
  if curl -sf http://localhost:3000 >/dev/null 2>&1; then
    info "  \u2713 Frontend ready \u2192 http://localhost:3000"
    break
  fi
  if [[ $i -eq 59 ]]; then
    warn "  \u26a0 Frontend check timed out \u2014 tail logs/frontend.log"
  fi
  sleep 1
done

echo ""
info "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501"
info "  AI Equity Intelligence is running"
info "  Frontend : http://localhost:3000"
info "  Backend  : http://localhost:8000"
info "  API Docs : http://localhost:8000/docs"
if $INFRA; then
  info "  Infra    : PostgreSQL :5432 | Redis :6379 | OpenSearch :9200"
fi
info "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501"
echo ""
info "  Stop with:          scripts/stop.sh"
info "  Seed demo data:     source backend/.venv/bin/activate && python scripts/seed_backend.py"
info "  View logs:          tail -f logs/backend.log  |  tail -f logs/frontend.log"
