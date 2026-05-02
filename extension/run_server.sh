#!/usr/bin/env bash
set -e
echo "Starting Promptify Cloud Backend (via uv)..."
cd "$(dirname "$0")/backend"
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
