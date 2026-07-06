#!/usr/bin/env bash
# Start both the Flask ML backend and the React frontend together.
# Usage: ./start.sh
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

# --- 1. Python backend ---------------------------------------------------
if [ ! -x ".venv/bin/python" ]; then
  echo "[setup] Creating virtualenv and installing Python deps..."
  python3 -m venv .venv
  ./.venv/bin/python -m pip install --upgrade pip -q
  ./.venv/bin/python -m pip install -q -r requirements.txt
fi

echo "[start] Flask backend  -> http://localhost:5000"
./.venv/bin/python app.py &
BACKEND_PID=$!

# --- 2. React frontend ---------------------------------------------------
if [ ! -d "node_modules" ]; then
  echo "[setup] Installing npm dependencies..."
  npm install
fi

echo "[start] React frontend -> http://localhost:3000"
BROWSER=none npm start &
FRONTEND_PID=$!

# --- Clean shutdown ------------------------------------------------------
trap "echo; echo '[stop] shutting down...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" INT TERM
wait
