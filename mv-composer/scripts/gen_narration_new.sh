#!/bin/bash
set -euo pipefail
VOICE="Samantha"
RATE=170
DIR="public/tax/audio/narration"

declare -a NEW=(
  "n01|Just set up Claude Code."
  "n02|Connect to each service through MCP."
  "n03|Automatic classification, registration, and analysis."
  "n04|No programming required."
)

for entry in "${NEW[@]}"; do
  KEY="${entry%%|*}"
  TEXT="${entry#*|}"
  echo "Generating $KEY: $TEXT"
  say -v "$VOICE" -r $RATE -o "$DIR/${KEY}.aiff" "$TEXT"
  ffmpeg -y -i "$DIR/${KEY}.aiff" -ar 44100 -ac 1 -b:a 128k "$DIR/${KEY}.mp3" 2>/dev/null
  rm -f "$DIR/${KEY}.aiff"
done

echo "Done"
ls -la "$DIR"/n0*.mp3
