#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PID_FILE="logs/.pids"

# ── Colors ─────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
info()  { printf "${GREEN}%s${NC}\n" "$*"; }
warn()  { printf "${YELLOW}%s${NC}\n" "$*"; }

# ── Stop by PID (or fallback to process name) ──────────────────
stop_service() {
  local pid=$1 name=$2 pattern=$3
  if kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null || true
    info "  Stopped $name (PID $pid)"
  fi
  # Fallback: kill any remaining processes matching the pattern
  pkill -f "$pattern" 2>/dev/null || true
}

if [[ -f "$PID_FILE" ]]; then
  while IFS='=' read -r key value; do
    case "$key" in
      BACKEND_PID) stop_service "$value" "backend" "uvicorn app.main" ;;
      FRONTEND_PID) stop_service "$value" "frontend" "next dev" ;;
      INFRA)
        if [[ "$value" == "true" ]]; then
          info "Stopping Docker infrastructure..."
          docker compose -f infra/docker-compose.yml down 2>/dev/null || true
        fi
        ;;
    esac
  done < "$PID_FILE"
  rm -f "$PID_FILE"
else
  warn "No PID file found at $PID_FILE \u2014 attempting fallback..."
  pkill -f "uvicorn app.main" 2>/dev/null || true
  pkill -f "next dev" 2>/dev/null || true
fi

info "All services stopped."
