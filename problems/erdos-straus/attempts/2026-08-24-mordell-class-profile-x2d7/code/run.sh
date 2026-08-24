#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 profile.py --limit "${LIMIT:-100000}"
