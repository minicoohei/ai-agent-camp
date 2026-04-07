#!/bin/bash
set -euo pipefail
source "$(dirname "$0")/../../.env"

DIR="public/tax/audio/narration"
TEXT="税理士の皆さん、記帳や仕訳、まだ手作業ですか？"

# calm/stable settings
SETTINGS='{"stability":0.55,"similarity_boost":0.75,"style":0.15,"use_speaker_boost":true}'

for VOICE_NAME in shohei masa; do
  case $VOICE_NAME in
    shohei) VID="8FuuqoKHuM48hIEwni5e" ;;
    masa)   VID="StTDrGrPSyfaHGmzwXbj" ;;
  esac

  OUT="$DIR/test_${VOICE_NAME}.mp3"
  echo "Generating test with $VOICE_NAME ($VID)..."

  curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/${VID}" \
    -H "xi-api-key: ${ELEVENLABS_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "{\"text\":\"${TEXT}\",\"model_id\":\"eleven_multilingual_v2\",\"voice_settings\":${SETTINGS}}" \
    --output "$OUT"

  SIZE=$(stat -f%z "$OUT" 2>/dev/null || echo 0)
  DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUT" 2>/dev/null || echo "?")
  echo "  $VOICE_NAME: ${SIZE} bytes, ${DUR}s"
done

echo "Done. Listen to:"
echo "  $DIR/test_shohei.mp3"
echo "  $DIR/test_masa.mp3"
