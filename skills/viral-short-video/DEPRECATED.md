# DEPRECATED: viral-short-video

このスキルは `mv-composer` に統合されました。

## 移行先

| 機能 | 移行先 |
|------|--------|
| 台本生成 | `mv-composer/scripts/generate_viral_script.py` |
| バイラルテクニック知識 | `mv-composer` SKILL.md 内「バイラルテクニック チートシート」 |
| フック分析 | `mv-composer/scripts/generate_viral_script.py --analyze-video` |
| アセットDL | `mv-composer/scripts/download_assets.sh` |
| X研究 | `skills/x-research/`（独立スキルとして既に移行済み） |
| 動画レンダリング | `mv-composer`（Remotion） |

## 理由

- viral-short-video は台本生成のみ（レンダリング機能なし）
- mv-composer は Remotion レンダリングパイプラインを持っている
- 縦型対応 (9:16) を mv-composer に追加し、1スキルで全動画フォーマットをカバー
