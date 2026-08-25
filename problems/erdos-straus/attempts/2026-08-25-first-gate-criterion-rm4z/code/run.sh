#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 verify_first_gate.py --limit "${LIMIT:-100000}"
