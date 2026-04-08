#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."
source "$(dirname "$0")/../../.env"

VOICE_ID="StTDrGrPSyfaHGmzwXbj"  # Masa
DIR="public/tax/audio/narration"

SETTINGS='{"stability":0.70,"similarity_boost":0.80,"style":0.10,"use_speaker_boost":true}'

declare -a REGEN=(
  "v4_s16|24時間365日、AIにチャットで質問できます。"
  "v4_s17|複雑な環境構築は、専用アプリで ワンクリックで完了します。"
  "v4_s18|学習用のそろったファイルを、用意しています。"
)

echo "=== Regenerating S16-S18 narration ==="

for entry in "${REGEN[@]}"; do
  KEY="${entry%%|*}"
  TEXT="${entry#*|}"
  OUT="$DIR/${KEY}.mp3"

  if [ -f "$OUT" ]; then
    cp "$OUT" "$DIR/${KEY}_backup.mp3"
  fi

  echo "  GEN $KEY: $TEXT"
  curl -s -X POST \
    "https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}" \
    -H "xi-api-key: ${ELEVENLABS_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "{
      \"text\": \"${TEXT}\",
      \"model_id\": \"eleven_multilingual_v2\",
      \"voice_settings\": ${SETTINGS}
    }" \
    --output "$OUT"

  SIZE=$(stat -f%z "$OUT" 2>/dev/null || stat -c%s "$OUT" 2>/dev/null || echo 0)
  if [ "$SIZE" -lt 1000 ]; then
    echo "    ERROR: ${SIZE} bytes - restoring backup"
    cat "$OUT"; echo
    mv "$DIR/${KEY}_backup.mp3" "$OUT"
  else
    DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUT" 2>/dev/null || echo "?")
    echo "    OK: ${DUR}s"
    rm -f "$DIR/${KEY}_backup.mp3"
  fi
  sleep 0.5
done

echo "=== Done ==="
