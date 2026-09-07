#!/usr/bin/env bash
# Launch script for Octopus React Dashboard & FastAPI Backend

set -e
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"

echo "🐙 Starting Octopus React Fairness Dashboard Suite..."

# 1. Start FastAPI Backend on port 8000
echo "--> Starting Backend API on http://localhost:8000 ..."
$PYTHON -m uvicorn dashboard.backend:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# 2. Start Vite React Dev Server on port 5173
echo "--> Starting React Dashboard on http://localhost:5173 ..."
cd "$PROJECT_DIR/dashboard-react"
npm run dev -- --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true" EXIT

echo "✅ Both services running! Open http://localhost:5173 in your browser."
wait
