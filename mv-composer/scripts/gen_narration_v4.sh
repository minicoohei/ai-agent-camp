#!/bin/bash
set -euo pipefail

# ElevenLabs TTS - Masa voice (calm Japanese male, narrative)
# TaxAccountantDemo v4 narration

cd "$(dirname "$0")/.."
source "$(dirname "$0")/../../.env"

VOICE_ID="StTDrGrPSyfaHGmzwXbj"  # Masa
DIR="public/tax/audio/narration"
mkdir -p "$DIR"

# Calm, professional settings
SETTINGS='{"stability":0.55,"similarity_boost":0.75,"style":0.15,"use_speaker_boost":true}'

declare -a SCENES=(
  "v4_s01|税理士の皆さん、記帳や仕訳、まだ手作業ですか？"
  "v4_s02|AIで、全自動へ。"
  "v4_s03|Claude Codeを起動するだけ。"
  "v4_s04|MCPプロトコルで、freeeとマネーフォワードに自動接続します。"
  "v4_s05|2大会計ソフトを、一元管理できます。"
  "v4_s06|レシートを読み取り、データを瞬時に抽出。"
  "v4_s07|AIが取引を自動で仕訳。freee MCPで即座に登録します。"
  "v4_s08|すべての取引を、AIが自動処理。"
  "v4_s09|レポートも書類も、即時生成。"
  "v4_s10|月次損益レポートが、数秒で完成します。"
  "v4_s11|営業利益も費目構成比も、ひと目で把握。"
  "v4_s12|気になったら、その場でクロードに質問できます。"
  "v4_s13|請求書も、その場で自動作成。"
  "v4_s14|業務時間69パーセント削減。即時処理。"
  "v4_s15|税理士1人がクロードコードで、複数クライアントに同一品質で対応。リアルタイム監視付きです。"
  "v4_s16|非エンジニアが悩みがちなポイントも、徹底解説します。"
  "v4_s17|24時間365日、AIチューターがサポートします。"
  "v4_s18|100以上のコースで、専門知識がなくても安全に始められます。"
  "v4_s19|すべて月額、12,800円で学べます。"
  "v4_s20|AI Agent Campで、税理士の業務効率化を始めましょう。"
)

echo "=== Generating ${#SCENES[@]} narration clips ==="
echo "Voice: Masa ($VOICE_ID) - calm narrative"

for entry in "${SCENES[@]}"; do
  KEY="${entry%%|*}"
  TEXT="${entry#*|}"
  OUT="$DIR/${KEY}.mp3"

  if [ -f "$OUT" ]; then
    echo "  SKIP $KEY (exists)"
    continue
  fi

  echo "  GEN  $KEY: $TEXT"
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

  SIZE=$(stat -f%z "$OUT" 2>/dev/null || echo 0)
  if [ "$SIZE" -lt 1000 ]; then
    echo "    ERROR: ${SIZE} bytes"
    cat "$OUT"; echo
    rm -f "$OUT"
  else
    DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUT" 2>/dev/null || echo "?")
    echo "    OK: ${DUR}s"
  fi
  sleep 0.3
done

echo ""
echo "=== Results ==="
ls -la "$DIR"/v4_*.mp3 2>/dev/null || echo "(none)"
