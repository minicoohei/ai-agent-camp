---
name: narration-qa
description: "ElevenLabsで生成したナレーション音声の品質を自動検証するスキル。 「ナレーションチェック」「音声確認」「発音チェック」等のリクエストで発動。"
triggers:
  - ナレーションチェック
  - 音声確認
  - 発音チェック
  - narration-qa
  - ナレーション品質検証
  - TTS検証
---

# Narration QA Skill

ElevenLabsで生成したナレーション音声の品質を自動検証するスキル。
**ナレーション生成時は必ずこのスキルのフローに従うこと。**

## トリガー

- ナレーション生成後の品質チェック依頼
- 「ナレーションチェック」「音声確認」「発音チェック」
- **ナレーション生成を含むすべてのMV制作タスク**（自動適用）

---

## Step 0: TTS入力テキストのルール（生成前に必ず適用）

### 英語IT用語の日本語化ルール

英語をそのまま残すとElevenLabsが誤読する。**全英語を日本語表記に変換してから生成する。**

| ルール | 例 |
|------|-----|
| 定着カタカナがあればそれを使う | GitHub→ギットハブ, Slack→スラック, Gmail→ジーメール, Google Drive→グーグルドライブ |
| カタカナ音写が不自然→日本語に意訳 | TODO→タスク, workflow→ワークフロー |
| ブランド名はカタカナ | Claude Code→クロードコード（中黒なし）, LINE→ライン |
| 略語はひらがな読み | AI→えーあい, PMO→ぴーえむおー, PPTX→パワーポイント |
| 固有名詞が誤読される場合→一般語に置換 | Claude Code→AIエージェント, GitHub Actions→自動ワークフロー |

### ⚠️ 過剰ひらがな化の禁止（重要）

**全文ひらがな化はTTSモデルを壊す。** PersonalPMODemo v3の実験で、以下が確認された:
- `ぴーえむおー` → ElevenLabsが「ピアノ」と発音
- `えーあい` → 「Eoi」と発音
- 全ひらがな文 → リズム崩壊、意味不明な発音

**正しいアプローチ**: 自然な漢字かな混じり文をベースに、**既知の誤読漢字のみ**をひらがな化する。

### 漢字のひらがな化ルール（選択的に適用）

ElevenLabs eleven_multilingual_v2 は特定の漢字を誤読する。**以下のパターンに該当する漢字のみ**ひらがなに置換する。それ以外の漢字はそのまま残す。

| 誤読パターン | 原因 | 対策 |
|------------|------|------|
| 返信→阪神 | 音が近い漢字に化ける | 「へんしん」にひらがな化 |
| 受信→閉める | 漢字誤読 | 「届いた」等の平易な表現に言い換え |
| 議事録→石立 | 漢字誤読 | 「ぎじろく」にひらがな化 |
| 各→夫は | 単漢字の誤読 | 「それぞれの」に言い換え |
| 即座に→危機座に | 漢字誤読 | 「すぐに」に言い換え |
| 承認→チョンキン | 中国語発音混入 | 「しょうにん」にひらがな化 |
| 税理士→推理師 | 中国語発音混入 | 「ぜいりし」にひらがな化 |
| 成果→成功 | 類似音 | 「せいか」にひらがな化 |
| マッキンゼー→松銀瀬 | 固有名詞の崩壊 | 「コンサル」等の一般語に言い換え |

**原則**: 上記テーブルに該当する漢字のみひらがな化。それ以外は自然な漢字かな混じり文のまま残す。自然な漢字かな混じり文 > 安全のために全ひらがな化（TTSモデルが壊れるため）。

### ひらがな化すべきか？ — 決定木

```
漢字を見つけた
→ 上記の誤読リストに該当する → ひらがな化する
→ リストにないが不安
  → ElevenLabsで1クリップだけテスト生成 → Gemini検証
    → 誤読あり → ひらがな化 or 平易な表現に言い換え → リストに追記
    → 問題なし → 漢字のまま残す
→ リストにない＋一般的な漢字 → 漢字のまま残す（過剰ひらがな化しない）
```

### 数字の展開ルール

数字は全てひらがなで書く:
- `7つの` → `ななつの`
- `8種類` → `はっしゅるい`
- `12,800円` → `いちまんにせんはっぴゃくえん`
- `95%` → `きゅうじゅうごパーセント`

### 避けるべきパターン

| NG | 理由 | OK |
|----|------|-----|
| 英語をそのまま残す | ElevenLabsが誤読 | 全てカタカナ/ひらがな化 |
| 「トゥードゥー」「クロード・コード」 | 日本語として不自然 | 「タスク」「クロードコード」 |
| 同一用語の表記揺れ | 混乱 | 統一表記 |
| 1文が長すぎる | 早口/尺超過 | 7文字/秒を目安に分割 |

---

## Step 1: 原稿の事前チェック（生成前）

### 1a. Step 0のルール適用確認

原稿テキストに以下がないことを確認:
- [ ] 英語のまま残っている単語
- [ ] 誤読リスクのある漢字（上記テーブル参照）
- [ ] 展開されていない数字
- [ ] 同一用語の表記揺れ

### 1b. 尺チェック

- 各セグメントのテキスト文字数から推定発話時間を算出（目安: 日本語7文字/秒）
- シーン尺（end - start）と比較
- **atempo 1.35x を超える場合は原稿を短縮**すること（それ以上の加速は不自然）
- 略語をフル読み（えーあい等）にすると尺が伸びる → 短い窓のシーンは特に注意

### 1c. 文体統一チェック

- 「です・ます」調で統一されているか
- 体言止めが混在していないか（Openingのキャッチコピーは例外OK）
- 主語の省略が自然か

---

## Step 2: 音声生成

### ElevenLabs設定

```python
voice_settings = {
    "stability": 0.70,       # 0.75以上だと棒読み感
    "similarity_boost": 0.80,
    "style": 0.10,            # 0.15以上だと抑揚過多
    "use_speaker_boost": True
}
model_id = "eleven_multilingual_v2"
```

### 生成後の尺チェック

```bash
# 各セグメントの尺を確認
for f in data/narration/s*.mp3; do
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  echo "$f: ${dur}s"
done
```

- `ratio = audio_duration / scene_window` を計算
- ratio > 1.35 → **原稿を短縮して再生成**（atempo で無理に収めない）
- ratio <= 1.35 → `ffmpeg -af "atempo={ratio}"` で速度調整

---

## Step 3: Gemini Flash 書き起こし検証（必須）

**生成後、必ず全セグメントをGemini Flashで書き起こし検証する。省略不可。**

### 実行コード

```python
from google import genai
import json, os, time

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

with open("data/narration_script.json") as f:
    segments = json.load(f)

results = []
for seg in segments:
    sid = seg["id"]
    audio_file = client.files.upload(file=f"data/narration/{sid}.mp3")
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[
            "この日本語音声を正確に書き起こしてください。句読点も含めて。テキストのみ返してください。",
            audio_file
        ]
    )
    transcription = response.text.strip()
    # 原稿と照合
    print(f"{sid}:")
    print(f"  Script: {seg['text']}")
    print(f"  Heard:  {transcription}")
    results.append({"id": sid, "script": seg["text"], "heard": transcription})
    time.sleep(1)

# 結果をJSONに保存
with open("data/narration_qa_results.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\nQA results saved to data/narration_qa_results.json")
```

**モデル選択**: `gemini-3-flash-preview` を使用（2.0/2.5 Flash より日本語音声認識精度が大幅に向上）。

### NG判定基準

| 深刻度 | 条件 | 対処 |
|--------|------|------|
| **Critical** | 意味が完全に変わる（返信→阪神、議事録→石立） | 原稿のひらがな化 → 再生成 → 再検証 |
| **Major** | 固有名詞が別の単語に化ける（クロードコード→黒度思うこと） | 表現を言い換え → 再生成 |
| **Minor** | 音は近いが漢字表記が異なる（同期→登記、成果物→性格物） | Gemini STTの限界。人間の耳で許容範囲なら**OK** |
| **Pass** | 書き起こしと原稿の意味が一致 | そのまま使用 |

### 再生成ループ — 決定木

```
Gemini検証でNGが出た
→ Critical（意味が変わる）
  → 原稿のひらがな化 or 言い換え → 再生成 → 再検証
  → 2回目もNG → 文章構造自体を大幅に書き直す → 再生成 → 再検証
  → 3回目もNG → そのセグメントを削除 or シーンからナレーションを外す
→ Major（固有名詞崩壊）
  → 一般語に置換（例: クロードコード→AIエージェント）→ 再生成 → 再検証
→ Minor（漢字表記が異なるだけ）
  → Gemini STTの限界の可能性あり。実音声を聴いて許容範囲なら Pass とする（自動Passにしない）
→ Pass → そのまま使用
```

**最大3ラウンド**。3回でもCriticalが残るなら該当セグメントのナレーションを諦める。

---

## Step 4: 音量バランス調整 & 最終ミックス

### 音量ルール

| トラック | volume | 備考 |
|---------|--------|------|
| ナレーション | **1.5** | メインコンテンツ。BGMより明確に大きく |
| BGM | **0.06** | ナレーションの邪魔をしない。存在感は感じる程度 |
| BGM (ナレーションなし区間) | 0.15 - 0.20 | Opening/Closingなどナレーションがない区間はBGMを上げてOK |

**判定**: 実音量比でナレーションがBGMの4倍以上であること。

### ⚠️ amix禁止 — amerge+pan を使う

`ffmpeg amix` は入力をN分割して正規化するため、volume設定が無視される。
**必ず `amerge + pan` を使うこと。**

```bash
# ナレーション全体をタイミング配置
# (adelay で各セグメントを配置 → amerge で結合)

# 動画 + BGM + ナレーションを一発ミックス (amerge + pan)
ffmpeg -y \
  -i out/video.mp4 \
  -i data/bgm.mp3 \
  -i data/narration_mix.mp3 \
  -filter_complex "\
    [1:a]volume=0.06,afade=t=out:st={total-4}:d=4[bgm];\
    [2:a]volume=1.5[narr];\
    [bgm][narr]amerge=inputs=2,pan=stereo|c0=c0+c2|c1=c1+c3[out]" \
  -map 0:v -map "[out]" -c:v copy -shortest \
  out/video_narrated.mp4
```

**amix vs amerge の違い**:
- `amix=inputs=2`: 各入力を ÷2 に正規化 → BGM 0.06×0.5=0.03, ナレーション 1.5×0.5=0.75 → 比率は保つが全体音量が低下
- `amerge + pan`: 正規化なし。volume値がそのまま反映される → 意図通りの音量バランス

---

## Step 5: QA結果の報告

### 報告フォーマット

```
| Seg | Script (先頭30字) | Gemini書き起こし (先頭30字) | 判定 | 対処 |
|-----|-------------------|---------------------------|------|------|
| s00 | えーあい パーソナル... | AIパーソナル... | Pass | — |
| s03 | メッセージからタスクを... | メッセージからタスクを... | Pass | — |
| s06 | 閉めるを確認し... | 届いたメールを確認し... | NG | ひらがな化→再生成 |
```

---

### トレードオフ判断基準

- 原稿を短くして尺に収める > atempo 1.35倍超で無理に収める（不自然な早口になる）
- 既知の誤読漢字のみひらがな化 > 安全のため全文ひらがな化（TTSが壊れる）
- amerge+panで正確な音量制御 > amixで手軽にミックス（音量が崩壊する）
- Gemini検証でMinor判定をPassにする > 完璧を求めて再生成ループを回し続ける（3回が上限）

---

## Tone（QA報告時）

- 検証結果は事実ベースで簡潔に。「Script」「Heard」「判定」の3列テーブルで報告
- NGの場合は「原因 → 対処」を1行で添える（例: 「承認→チョンキン: 中国語発音混入 → しょうにんにひらがな化」）
- 全セグメントPassの場合も省略せずテーブルを出す（確認の証跡として）

---

## 多言語ナレーション対応（EN/ES）

AgentCampOnboarding v11o で確立。日本語以外のナレーション生成時のルール。

### ボイス選択

| 言語 | Voice | Voice ID | 備考 |
|------|-------|----------|------|
| JP | Masa | `StTDrGrPSyfaHGmzwXbj` | 日本語専用 |
| EN | Chris | `iP95p4xoKVk53GoZ742B` | 英語・多言語対応 |
| ES | Chris | `iP95p4xoKVk53GoZ742B` | スペイン語も同ボイスで自然 |

### Voice ID の注意事項
- **Voice ID は完全な文字列を使う**: `iP95p4xoKVk5`（切り詰め）→ 404 エラー。必ず `iP95p4xoKVk53GoZ742B`（完全版）を使用
- 不明な場合は `client.voices.get_all()` で一覧取得して確認

### EN/ES テキスト作成のコツ
- **具体的金額を避ける**: 「One flat monthly fee」のように一般表現にすると、価格変更時にナレーション再生成が不要
- **Step 0 ルールは JP 専用**: EN/ES では英語IT用語のカタカナ化や漢字ひらがな化は不要
- **atempo 調整**: EN/ES は JP より発話速度が速いため、atempo 不要なケースが多い。1.0-1.2 の範囲なら自然

### EN/ES の Gemini QA
- **全クリップ必須**: EN/ES でも省略しない。ElevenLabs multilingual_v2 は英語でも稀に誤読する
- **判定基準は同じ**: 意味が変わったら Critical、固有名詞崩壊は Major、表記違いは Minor
- **Gemini モデル**: `gemini-3-flash-preview` を使用（EN/ES 認識精度も高い）

---

## 自律ループ運用（推奨）

このスキルは **自律的に繰り返し実行** して品質を収束させることを前提に設計されている。

### 自律ループフロー

```
[Round 1]
  Step 0: テキストルール適用
  Step 2: ElevenLabs 全クリップ生成
  Step 3: Gemini QA 全クリップ検証
    → Critical/Major NG が出た場合 ↓

[Round 2]
  NG クリップのテキストを修正（ひらがな化 / 言い換え）
  対象クリップのみ再生成
  Gemini QA 対象クリップのみ再検証
    → まだ NG があれば ↓

[Round 3]
  文章構造自体を大幅に書き直す
  再生成 → 再検証
    → まだ NG → そのセグメントのナレーションを諦める（ユーザーに報告）
```

### 運用のポイント

- **Round 2以降は NG クリップだけ再生成**: 全クリップ再生成は時間とAPI費用の無駄
- **Minor 判定は自動 Pass にしない**: 実音声を聴いて許容範囲か判断してから Pass（ただし3回ループ後は妥協してよい）
- **motion-review と連携**: ナレーション確定後に motion-review の Render & Review Loop に入る。ナレーションが未確定のままレンダリングしない
- **多言語版は言語ごとに独立ループ**: JP → EN → ES の順で実行。JP の教訓（誤読パターン等）を EN/ES に活かす

### トリガーワード（自律ループ起動）
- `ナレーション生成してQAして` → 生成 + Gemini QA + NG 修正ループを自律実行
- `narration full loop` → 同上（英語指示でも起動）
- `ナレーションQAだけ` → 既存の mp3 に対して Gemini QA のみ実行

---

## 依存

- **ElevenLabs API**: `ELEVENLABS_API_KEY` in `.env`
- **Gemini API**: `GEMINI_API_KEY` in `.env`
- **ffmpeg**: 音声処理用
- **pip**: `google-generativeai` パッケージ（`pip install --user --break-system-packages google-generativeai`）

## ファイル構成

```
data/
  narration_script.json    # ナレーション原稿（タイミング付き）
  narration/s00.mp3        # 各セグメントの生成音声
  narration/s00_fit.mp3    # 速度調整済み音声
  narration_mix.mp3        # ナレーション全体ミックス
  audio_final.mp3          # BGM + ナレーション最終ミックス
  bgm.mp3 / bgm_extended.mp3  # BGM
  narration_qa_results.json    # Gemini検証結果ログ
  gen_narration_en.py      # EN ナレーション生成スクリプト
  gen_narration_es.py      # ES ナレーション生成スクリプト
  narration_en_results.json    # EN QA結果
  narration_es_results.json    # ES QA結果
```
