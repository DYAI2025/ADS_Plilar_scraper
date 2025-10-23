#!/usr/bin/env bash
set -euo pipefail
python -m pip install -r requirements.txt -q
[ -f Files/requirements.txt ] && python -m pip install -r Files/requirements.txt -q || true
python -m compileall Files || true
pytest -q