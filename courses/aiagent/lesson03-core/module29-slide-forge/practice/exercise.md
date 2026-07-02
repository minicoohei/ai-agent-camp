# 演習: 自分の議事録から提案デッキを作る

この演習では、自分の議事録または構成メモを1本選び、slide-forge で提案デッキを生成してから、`revise` で1回修正します。流れは `/start-29-2` と `/start-29-3` に対応しています。

## 事前準備

- slide-forge の APIキー不要デモが完了していること
- `OPENAI_API_KEY` と `LLM_BACKEND` を設定済みであること
- `config.yaml` を用意し、必要に応じてブランド名・配色・ロゴを調整していること
- 秘密情報や API キーの値をチャットに貼らないこと

未取得の場合は検証済みタグを固定して取得し、既存設定を上書きしないように準備します。

```bash
git clone --depth 1 --branch v0.1.0 https://github.com/minicoohei/slide-forge.git
cd slide-forge
cp -n .env.example .env
cp -n config.default.yaml config.yaml
```

## 手順

1. 議事録、構成メモ、提案メモのいずれかを1本用意します。
   - ファイル形式は `.md` / `.txt` / `.json` / `.pdf` が使えます。
   - 構成案と議事録が分かれている場合は、構成案を `--outline`、事実ソースを `--input` として扱います。
2. `/start-29-2` を使い、5問を決めます。
   - 型: SCQA / PREP / ゴールデンサークル / TAPS / ホールパート
   - シナリオ: 課題駆動 / ビジョン駆動 / 資本駆動 / 人駆動
   - トーン: ライト / コーポレート・ネイビー / シネマ・ダーク / エディトリアル白
   - 目的: 承認を得たい（提案） / 共有して知ってほしい / ビジョンで動かす
   - ターゲット: 社外・初対面 / 社内・意思決定者 / 既存パートナー
3. 次の例のように `python cli.py generate` を実行します。

   ```bash
   python cli.py generate --input examples/loop_engineering.md \
     --type ゴールデンサークル --scenario ビジョン駆動 --tone コーポレート・ネイビー \
     --goal 共有して知ってほしい --target 社外・初対面 \
     --tastes navy --formats pptx pdf png html --out ./out/job1
   ```

4. 生成された `./out/job1/deck/navy/deck.pptx` / `./out/job1/deck/navy/deck.pdf` / `./out/job1/deck/navy/deck.html` / `./out/job1/deck/navy/contact_sheet.png` を確認します。
5. 1か所だけ修正したい点を決め、`/start-29-3` の流れで `revise` を1回実行します。
   ```bash
   python cli.py revise --out ./out/job1 --tastes navy --instruction "p3をもっと強く"
   ```
6. 修正前後で、変更対象以外のページに不要な変化がないか確認します。

## 確認観点

- PPTX の見出し・リード・フッターが編集可能なテキストボックスになっている
- 固定 chrome（見出し、アクセントバー、フッター、ページ番号）が全ページで同じ座標に揃っている
- 入力資料に無い固有名詞、数字、日付、費用、KPI が推測で追加されていない
- PDF / PNG / HTML / PPTX の4形式が、同じ内容として確認できる
- `revise` 後に、修正指示と関係ないページが不自然に変わっていない

## 提出物

- 生成ジョブの出力フォルダ `./out/job1/deck/navy/`
- 初回生成時の `./out/job1/deck/navy/deck.pptx`
- `revise` 後の `./out/job1/deck/navy/deck.pptx`
- どのページをどう修正したかのメモ
