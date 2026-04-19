#!/bin/bash
# Generate narration audio clips using macOS say command
set -euo pipefail

OUTDIR="public/tax/audio/narration"
mkdir -p "$OUTDIR"
VOICE="Samantha"
RATE=170

declare -a SCENES=(
  "s01|AI is transforming tax accounting."
  "s02|Start with any receipt."
  "s03|OCR reads every detail automatically."
  "s04|Ninety nine percent accuracy."
  "s05|Transactions classified instantly."
  "s06|Each entry sorted into the right category."
  "s07|Integrated with freee accounting."
  "s08|AI processes all transactions automatically."
  "s09|And MoneyForward Cloud."
  "s10|Journal entries created in seconds."
  "s11|Monthly reports, generated automatically."
  "s12|Complete profit and loss statements."
  "s13|Visual analytics at a glance."
  "s14|AI analyzes every transaction for insights."
  "s15|Seventy percent time saved. Two platforms. Nineteen fifty regulations."
  "s16|AI Agent Camp. Start optimizing your tax practice today."
)

for entry in "${SCENES[@]}"; do
  KEY="${entry%%|*}"
  TEXT="${entry#*|}"
  echo "Generating $KEY: $TEXT"
  say -v "$VOICE" -r $RATE -o "$OUTDIR/${KEY}.aiff" "$TEXT"
  ffmpeg -y -i "$OUTDIR/${KEY}.aiff" -ar 44100 -ac 1 -b:a 128k "$OUTDIR/${KEY}.mp3" 2>/dev/null
  rm -f "$OUTDIR/${KEY}.aiff"
done

echo ""
echo "=== Generated $(ls "$OUTDIR"/*.mp3 | wc -l | tr -d ' ') narration clips ==="
ls -la "$OUTDIR"/*.mp3
