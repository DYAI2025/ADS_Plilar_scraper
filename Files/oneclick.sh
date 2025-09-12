#!/usr/bin/env bash
# One-click start: setup venv, install deps, run setup, open GUI
set -e
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  echo "📦 Creating virtual environment (.venv)..."
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

if [ -f requirements.txt ]; then
  echo "📦 Installing dependencies..."
  pip install -r requirements.txt
fi

echo "🚀 Running setup..."
bash run_setup.sh || true

echo "🖥️ Starting GUI..."
python3 gui_app.py
