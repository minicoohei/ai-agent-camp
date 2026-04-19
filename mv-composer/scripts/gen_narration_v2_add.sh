#!/bin/bash
set -euo pipefail
VOICE="Samantha"
RATE=170
DIR="public/tax/audio/narration"

declare -a SCENES=(
  "v2_s14|With A.I. Agent Camp, even non-engineers can set up Claude Code safely."
  "v2_s15|An intensive hands-on program for just twelve thousand eight hundred yen."
  "v2_s16|Start automating your tax practice. A.I. Agent Camp."
)

for entry in "${SCENES[@]}"; do
  KEY="${entry%%|*}"
  TEXT="${entry#*|}"
  echo "Generating $KEY: $TEXT"
  say -v "$VOICE" -r $RATE -o "$DIR/${KEY}.aiff" "$TEXT"
  ffmpeg -y -i "$DIR/${KEY}.aiff" -ar 44100 -ac 1 -b:a 128k "$DIR/${KEY}.mp3" 2>/dev/null
  rm -f "$DIR/${KEY}.aiff"
done
echo "Done"
ls -la "$DIR"/v2_s1[456].mp3
