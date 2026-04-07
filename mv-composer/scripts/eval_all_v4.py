import google.generativeai as genai
import os

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("Error: GEMINI_API_KEY environment variable is not set")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

base = "public/tax/audio/narration"
scenes = [
    ("v4_s01", "税理士の皆さん、記帳や仕訳、まだ手作業ですか？"),
    ("v4_s02", "AIで、全自動へ。"),
    ("v4_s03", "Claude Codeを起動するだけ。"),
    ("v4_s04", "MCPプロトコルで、freeeとマネーフォワードに自動接続します。"),
    ("v4_s05", "2大会計ソフトを、一元管理できます。"),
    ("v4_s06", "レシートを読み取り、データを瞬時に抽出。"),
    ("v4_s07", "AIが取引を自動で仕訳。freee MCPで即座に登録します。"),
    ("v4_s08", "すべての取引を、AIが自動処理。"),
    ("v4_s09", "レポートも書類も、即時生成。"),
    ("v4_s10", "月次損益レポートが、数秒で完成します。"),
    ("v4_s11", "営業利益も費目構成比も、ひと目で把握。"),
    ("v4_s12", "気になったら、その場でクロードに質問できます。"),
    ("v4_s13", "請求書も、その場で自動作成。"),
    ("v4_s14", "業務時間69パーセント削減。即時処理。"),
    ("v4_s15", "税理士1人がクロードコードで、複数クライアントに同一品質で対応。リアルタイム監視付きです。"),
    ("v4_s16", "24時間365日、AIにチャットで質問できます。"),
    ("v4_s17", "複雑な環境構築は、専用アプリでワンクリックで完了します。"),
    ("v4_s18", "学習用のそろったファイルを、用意しています。"),
    ("v4_s19", "すべて月額、12,800円で学べます。"),
    ("v4_s20", "AI Agent Campで、税理士の業務効率化を始めましょう。"),
]

for fname, expected in scenes:
    path = f"{base}/{fname}.mp3"
    audio = genai.upload_file(path)
    resp = model.generate_content([
        audio,
        f"この日本語音声を正確に書き起こしてください。期待テキスト: 「{expected}」。書き起こし結果と、中国語の発音が混入していないか、読み間違いがあれば指摘（1-2行で簡潔に）。"
    ])
    print(f"S{fname[-2:]}: {resp.text.strip()}")
    print()
