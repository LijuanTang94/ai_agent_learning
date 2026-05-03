#!/usr/bin/env bash
# Dependencies live only in this folder's .venv (uv). Do NOT pip install into conda base.
set -euo pipefail
cd "$(dirname "$0")"
exec uv run python server.py
