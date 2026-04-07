#!/bin/bash
set -euo pipefail

# ElevenLabs TTS - Japanese narration for TaxAccountantDemo v31
# Voice: Hajime (SOuiRq8aXqyALuq5QIQ8) - energetic Japanese male
# 20 scenes, 73.2s total

cd "$(dirname "$0")/.."
source "$(dirname "$0")/../../.env"

VOICE_ID="SOuiRq8aXqyALuq5QIQ8"
DIR="public/tax/audio/narration"
mkdir -p "$DIR"

# Scene narrations - matched to video content, energetic product-intro style
# Each line fits within the scene duration
declare -a SCENES=(
  # S01 (3.6s) Hook - 書類山積み映像
  "v3_s01|税理士の皆さん、記帳や仕訳、まだ手作業ですか？"
  # S02 (2.4s) Title - AIで全自動へ
  "v3_s02|AIで、全自動へ。"
  # S03 (3.0s) Claude Code Terminal
  "v3_s03|Claude Codeを起動するだけ。"
  # S04 (3.6s) MCP接続
  "v3_s04|MCPプロトコルでfreeeとMoneyForwardに自動接続。"
  # S05 (3.0s) 2大会計ソフト
  "v3_s05|2大会計ソフトを一元管理できます。"
  # S06 (3.0s) レシートスキャン
  "v3_s06|レシートを読み取り、データを瞬時に抽出。"
  # S07 (6.0s) 仕訳分類+freee登録
  "v3_s07|AIが取引を自動で仕訳し、freee MCPで即座に登録します。"
  # S08 (3.6s) freee自動経理
  "v3_s08|全ての取引をAIが自動処理。"
  # S09 (2.4s) テキストブリッジ
  "v3_s09|レポートも書類も、即時生成。"
  # S10 (3.0s) 月次レポート
  "v3_s10|月次損益レポートが数秒で完成します。"
  # S11 (3.0s) チャート3つ
  "v3_s11|営業利益も費目構成比もひと目で把握。"
  # S12 (3.6s) Claude Chat
  "v3_s12|気になったら、その場でClaudeに質問できます。"
  # S13 (3.6s) 請求書生成
  "v3_s13|請求書もその場で自動作成。"
  # S14 (3.0s) 成果数値
  "v3_s14|業務時間69%削減、595件の仕訳を即時処理。"
  # S15 (6.0s) アーキテクチャ+監視
  "v3_s15|1人の税理士がClaude Codeを通じて複数のクライアントに同一品質で対応。全てリアルタイムで監視できます。"
  # S16 (3.6s) 非エンジニアの悩み
  "v3_s16|非エンジニアが悩みがちなポイントも徹底解説。"
  # S17 (3.6s) SafeEnv - AI Tutor
  "v3_s17|24時間365日、AIチューターがサポートします。"
  # S18 (4.2s) コース一覧
  "v3_s18|100以上のコースで、専門知識がなくても安全に始められます。"
  # S19 (4.2s) 価格
  "v3_s19|全て月額12,800円で学べます。"
  # S20 (3.6s) CTA
  "v3_s20|AI Agent Campで、税理士の業務効率化を始めましょう。"
)

echo "=== Generating ${#SCENES[@]} narration clips via ElevenLabs ==="
echo "Voice: Hajime ($VOICE_ID)"

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
      \"voice_settings\": {
        \"stability\": 0.45,
        \"similarity_boost\": 0.78,
        \"style\": 0.35,
        \"use_speaker_boost\": true
      }
    }" \
    --output "$OUT"

  # Check file size (< 1KB = error)
  SIZE=$(stat -f%z "$OUT" 2>/dev/null || echo 0)
  if [ "$SIZE" -lt 1000 ]; then
    echo "    ERROR: output too small (${SIZE} bytes), likely API error"
    cat "$OUT"
    rm -f "$OUT"
  else
    DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUT" 2>/dev/null || echo "?")
    echo "    OK: ${SIZE} bytes, ${DUR}s"
  fi

  sleep 0.3
done

echo ""
echo "=== Generated clips ==="
ls -la "$DIR"/v3_*.mp3 2>/dev/null || echo "(none)"
