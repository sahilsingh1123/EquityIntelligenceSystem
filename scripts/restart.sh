#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Evaluate fnm if available to ensure Node/npm are on the execution PATH
if command -v fnm >/dev/null 2>&1; then
  eval "$(fnm env)"
fi

echo "Restarting AI Equity Intelligence services..."
./scripts/stop.sh
./scripts/start.sh
