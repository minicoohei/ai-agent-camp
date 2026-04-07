#!/bin/bash
set -euo pipefail
VOICE="Samantha"
RATE=170
DIR="public/tax/audio/narration"
mkdir -p "$DIR"

declare -a SCENES=(
  "v2_s01|Are you still doing registration, bookkeeping, and checking all by hand?"
  "v2_s02|Let A.I. automate everything."
  "v2_s03|Just launch Claude Code. M.C.P. connects automatically."
  "v2_s04|Connect to freee and MoneyForward through M.C.P."
  "v2_s05|Both platforms, ready at your fingertips."
  "v2_s06|Receipts scanned and extracted instantly."
  "v2_s07|Transactions classified and registered via freee M.C.P."
  "v2_s08|A.I. processes all transactions across both platforms."
  "v2_s09|Reports and documents, generated instantly."
  "v2_s10|Monthly P and L reports in seconds."
  "v2_s11|Invoices created on the spot."
  "v2_s12|Seventy percent time saved. Two platforms. Instant output."
  "v2_s13|Start automating your tax practice. A.I. Agent Camp."
)

for entry in "${SCENES[@]}"; do
  KEY="${entry%%|*}"
  TEXT="${entry#*|}"
  echo "Generating $KEY: $TEXT"
  say -v "$VOICE" -r $RATE -o "$DIR/${KEY}.aiff" "$TEXT"
  ffmpeg -y -i "$DIR/${KEY}.aiff" -ar 44100 -ac 1 -b:a 128k "$DIR/${KEY}.mp3" 2>/dev/null
  rm -f "$DIR/${KEY}.aiff"
done

echo ""
echo "=== Generated $(ls "$DIR"/v2_*.mp3 | wc -l | tr -d ' ') narration clips ==="
ls -la "$DIR"/v2_*.mp3
