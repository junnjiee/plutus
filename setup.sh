#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v uv &>/dev/null; then
    echo "Error: uv is required but not installed."
    echo "Install it from https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

uv run python "$SCRIPT_DIR/setup.py" "$@"
