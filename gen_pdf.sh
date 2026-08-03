#!/usr/bin/env bash
# Genera glucemia.pdf a partir de la tabla HTML.
set -euo pipefail

cd "$(dirname "$0")"

python3 gen_tabla.py

CHROME=/opt/pw-browsers/chromium
[ -x "$CHROME" ] || CHROME=$(command -v chromium || command -v google-chrome)

"$CHROME" \
  --headless \
  --disable-gpu \
  --no-sandbox \
  --no-pdf-header-footer \
  --print-to-pdf=glucemia.pdf \
  "file://$PWD/tabla_glucemia.html" 2>/dev/null

echo "glucemia.pdf generado"
