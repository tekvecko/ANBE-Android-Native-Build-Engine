#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "ANBE installer"
echo "=============="
echo

command -v python >/dev/null 2>&1 || {
    echo "[ERROR] Python is required."
    exit 1
}

python -m pip install --upgrade .

echo
echo "[✓] ANBE installed"
echo
echo "Verify with:"
echo "  anbe --version"
echo "  anbe doctor <project>"
