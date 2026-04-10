#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Prefer uv run if available, fall back to python3
if command -v uv &>/dev/null; then
    uv run python "$SCRIPT_DIR/setup.py" "$@"
else
    python3 "$SCRIPT_DIR/setup.py" "$@"
fi
