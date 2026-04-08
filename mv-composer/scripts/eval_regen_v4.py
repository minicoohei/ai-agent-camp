import google.generativeai as genai
import os

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("Error: GEMINI_API_KEY environment variable is not set")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

base = "public/tax/audio/narration"
checks = [
    ("v4_s01", "税理士の皆さん、記帳や仕訳、まだ手作業ですか？"),
    ("v4_s06", "レシートを読み取り、データを瞬時に抽出。"),
    ("v4_s07", "AIが取引を自動で仕訳。freee MCPで即座に登録します。"),
    ("v4_s08", "すべての取引を、AIが自動処理。"),
    ("v4_s09", "レポートも書類も、即時生成。"),
    ("v4_s10", "月次損益レポートが、数秒で完成します。"),
    ("v4_s14", "業務時間69パーセント削減。即時処理。"),
    ("v4_s15", "税理士1人がクロードコードで、複数クライアントに同一品質で対応。リアルタイム監視付きです。"),
    ("v4_s19", "すべて月額、12,800円で学べます。"),
]

for fname, expected in checks:
    path = f"{base}/{fname}.mp3"
    audio = genai.upload_file(path)
    resp = model.generate_content([
        audio,
        f"この日本語音声を正確に書き起こしてください。期待テキスト: 「{expected}」。書き起こし結果と、中国語の発音が混入していないか、読み間違いがあれば指摘（1-2行で簡潔に）。"
    ])
    print(f"=== {fname} ===")
    print(resp.text.strip())
    print()
