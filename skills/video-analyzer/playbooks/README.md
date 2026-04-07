# Video Playbooks

動画タイプ別の制作知見データベース。
video-analyzerで分析した動画から自動的に知見を蓄積する。

## タイプ一覧
- `intro.json` — 紹介・レビュー（商品紹介、サービス紹介、人物紹介）
- `teaching.json` — ティーチング・解説（ハウツー、知識共有、tips）
- `template.json` — テンプレート・トレンド（流行りのフォーマット、音源同期）
- `meme.json` — Meme・ネタ（オチ重視、ユーモア）
- `dance.json` — ダンス・パフォーマンス（振付、BPM同期）
- `mv.json` — MV・シネマティック（音楽映像、エフェクト重視）
- `clip.json` — 切り抜き・ハイライト（長尺→短尺、名場面集）

## 使い方
storyboard-generatorが `--playbook intro` で参照し、そのタイプに最適な構成を適用する。
