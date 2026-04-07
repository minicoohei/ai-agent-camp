import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

base = "public/tax/audio/narration"
checks = [
    ("v4_s01", "税理士の皆さん、記帳や仕訳、まだ手作業ですか？"),
    ("v4_s04", "MCPプロトコルで、freeeとマネーフォワードに自動接続します。"),
    ("v4_s07", "AIが取引を自動で仕訳。freee MCPで即座に登録します。"),
    ("v4_s12", "気になったら、その場でクロードに質問できます。"),
    ("v4_s15", "税理士1人がクロードコードで、複数クライアントに同一品質で対応。"),
    ("v4_s20", "AI Agent Campで、税理士の業務効率化を始めましょう。"),
]

for fname, expected in checks:
    path = f"{base}/{fname}.mp3"
    audio = genai.upload_file(path)
    resp = model.generate_content([
        audio,
        f"この音声を書き起こし、期待テキスト「{expected}」と比較。発音(A/B/C)、自然さ(A/B/C)、問題点を各1行で。"
    ])
    print(f"=== {fname} ===")
    print(resp.text.strip())
    print()
