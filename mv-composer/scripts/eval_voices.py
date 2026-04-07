import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

base = "public/tax/audio/narration"
expected = "税理士の皆さん、記帳や仕訳、まだ手作業ですか？"

for voice in ["test_shohei", "test_masa", "v3_s01"]:
    label = {"test_shohei": "Shohei(calm)", "test_masa": "Masa(narrative)", "v3_s01": "Hajime(current)"}[voice]
    path = f"{base}/{voice}.mp3"
    audio = genai.upload_file(path)
    resp = model.generate_content([
        audio,
        f"""この日本語ナレーション音声を評価してください:
期待テキスト: {expected}
以下を簡潔に（各1行で）:
1. 書き起こし
2. 発音正確性 (A/B/C)
3. イントネーション自然さ (A/B/C)
4. 落ち着き度 (A=落ち着いている B=普通 C=元気すぎ)
5. 商品紹介ナレーション適性 (A/B/C)
6. 問題点"""
    ])
    print(f"=== {label} ===")
    print(resp.text.strip())
    print()
