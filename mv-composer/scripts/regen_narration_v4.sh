#!/bin/bash
set -euo pipefail

# Regenerate only problematic narration clips with phonetic hints
# Voice: Masa (calm Japanese male)

cd "$(dirname "$0")/.."
source "$(dirname "$0")/../../.env"

VOICE_ID="StTDrGrPSyfaHGmzwXbj"  # Masa
DIR="public/tax/audio/narration"

# More stable settings - higher stability to reduce Chinese pronunciation mixing
SETTINGS='{"stability":0.70,"similarity_boost":0.80,"style":0.10,"use_speaker_boost":true}'

# Problematic clips with phonetic hints (kanji → hiragana/katakana)
declare -a REGEN=(
  "v4_s01|ぜいりしの皆さん、きちょうや しわけ、まだ手作業ですか？"
  "v4_s06|レシートを読み取り、データを しゅんじに抽出。"
  "v4_s07|AIが とりひきを自動で しわけ。freee MCPで そくざに登録します。"
  "v4_s08|すべての とりひきを、AIが自動処理。"
  "v4_s09|レポートも書類も、そくじ生成。"
  "v4_s10|月次 そんえきレポートが、すうびょうで完成します。"
  "v4_s14|業務時間 ろくじゅうきゅう パーセント削減。そくじ処理。"
  "v4_s15|ぜいりし1人がクロードコードで、複数クライアントに同一品質で対応。リアルタイム かんし付きです。"
  "v4_s19|すべて月額、いちまん にせん はっぴゃく えんで学べます。"
)

echo "=== Regenerating ${#REGEN[@]} problematic clips ==="
echo "Voice: Masa ($VOICE_ID) - higher stability"

for entry in "${REGEN[@]}"; do
  KEY="${entry%%|*}"
  TEXT="${entry#*|}"
  OUT="$DIR/${KEY}.mp3"

  # Backup original
  if [ -f "$OUT" ]; then
    cp "$OUT" "$DIR/${KEY}_backup.mp3"
  fi

  echo "  REGEN $KEY: $TEXT"
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

echo ""
echo "=== Done ==="
