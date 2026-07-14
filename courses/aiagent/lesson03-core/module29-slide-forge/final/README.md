# 完成例: slide-forge で生成した提案デッキ

この完成例では、議事録または構成メモから slide-forge で提案デッキを生成し、4形式の成果物を確認します。

## 再現コマンド

検証済みタグを固定して取得し、既存の `.env` / `config.yaml` は上書きしません。

```bash
git clone --depth 1 --branch v0.1.0 https://github.com/minicoohei/slide-forge.git
cd slide-forge
cp -n .env.example .env
cp -n config.default.yaml config.yaml
python cli.py generate --input examples/loop_engineering.md \
  --type ゴールデンサークル --scenario ビジョン駆動 --tone コーポレート・ネイビー \
  --goal 共有して知ってほしい --target 社外・初対面 \
  --tastes navy --formats pptx pdf png html --out ./out/job1
```

## 生成物

標準的な出力先を `./out/job1`、配色を `navy` とした場合、主な生成物は次の場所にできます。

| 形式 | パス例 | 確認すること |
|------|--------|--------------|
| PPTX | `./out/job1/deck/navy/deck.pptx` | PowerPoint / Keynote で開き、見出し・リード・フッター等のテキストが編集できる |
| PDF | `./out/job1/deck/navy/deck.pdf` | ページ数、寸法、余白、固定 chrome の位置が崩れていない |
| PNG | `./out/job1/deck/navy/contact_sheet.png` | 全ページが同じサイズで書き出されている |
| HTML | `./out/job1/deck/navy/deck.html` | ブラウザで固定 chrome の重なりを確認できる |

`navy` は `config.yaml` の palette キーです。

## 確認観点

- 固定 chrome（ヘッダー、フッター、見出し、アクセントバー、ページ番号）が全ページで同じ座標に揃っている
- PPTX の本文テキストが画像化されず、編集可能なテキストボックスとして残っている
- 本文図解だけが画像として配置され、確定テキストは後載せのレイヤーになっている
- PDF と PNG のページ寸法が揃っている
- 入力資料に無い事実、数字、固有名詞が追加されていない

## revise 後の完成状態

`python cli.py revise --out ./out/job1 --tastes navy --instruction "p3をもっと強く"` のように修正した場合は、更新後の `./out/job1/deck/navy/deck.pptx` / `./out/job1/deck/navy/deck.pdf` / `./out/job1/deck/navy/deck.html` / `./out/job1/deck/navy/contact_sheet.png` を再確認します。変更対象のページだけが意図どおり変わり、他のページの固定 chrome が崩れていなければ完成です。
