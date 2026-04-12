---
name: video-playbook
description: "動画分析結果からタイプ別Playbookに知見を蓄積・活用するスキル。 video-analyzerの出力template.jsonを入力として使う。 「Playbook更新」「動画タイプ別知見」「Playbook確認」等で発動。"
triggers:
  - Playbook更新
  - 動画タイプ別の知見
  - Playbookを確認
  - 動画の制作ガイドライン
  - 分析結果を蓄積
  - video-playbook
---

# Video Playbook

動画分析結果（template.json）から動画タイプを判定し、タイプ別Playbookに制作知見を蓄積・活用する。

## 動画タイプ（7種類）

| タイプ | 説明 |
|--------|------|
| `intro` | 紹介・レビュー（商品紹介、サービス紹介、人物紹介） |
| `teaching` | ティーチング・解説（ハウツー、知識共有、tips、ノウハウ） |
| `template` | テンプレート・トレンド（流行りのフォーマット、音源同期、チャレンジ） |
| `meme` | Meme・ネタ（オチ重視、ユーモア、パロディ） |
| `dance` | ダンス・パフォーマンス（振付、BPM同期、カバー） |
| `mv` | MV・シネマティック（音楽映像、エフェクト重視、映画的演出） |
| `clip` | 切り抜き・ハイライト（長尺→短尺、名場面、配信切り抜き） |

## クイックスタート

```bash
# video-analyzerで分析後、Playbookに知見を追加
python skills/video-playbook/scripts/manage_playbook.py \
  --add -t output/templates/video_001/template.json

# タイプ別Playbook一覧
python skills/video-playbook/scripts/manage_playbook.py --list

# 特定タイプのPlaybook表示
python skills/video-playbook/scripts/manage_playbook.py --show teaching

# Markdown形式でエクスポート
python skills/video-playbook/scripts/manage_playbook.py --export teaching
```

## ワークフロー

```
1. video-analyzer で動画分析 → template.json
2. manage_playbook.py --add -t template.json
   → 動画タイプ自動判定
   → タイミング・構成・テロップ等の知見抽出
   → タイプ別playbook JSONに追加
   → 集計データ自動更新
3. manage_playbook.py --show TYPE で蓄積知見を確認
4. 新動画制作時にPlaybookを参照
```

## Playbook蓄積の仕組み

各分析結果から以下の知見を抽出し、タイプ別に蓄積：

- **タイミング**: 平均シーン長、ペーシング、フック長
- **構成**: 構成パターン（hook→problem→solution等）、使用テクニック
- **テロップ**: スタイル、配置、色、密度
- **ビジュアル**: ショットタイプ、バリエーション、解像度
- **音声**: ナレーション有無、密度、シーンあたり文字数

サンプルが増えるほど集計データ（`aggregated`）の精度が上がり、
「このタイプの動画はこう作るべき」という制作ガイドラインが自動生成される。

## コンテンツ生成への活用

Playbookの知見を使って新動画を作る際：

1. `--show TYPE` で対象タイプの知見を確認
2. `--export TYPE` でMarkdownサマリーを生成
3. サマリーをLLMプロンプトに含めて台本・構成案を生成
4. storyboard-generatorにPlaybook知見を反映

## データ保存先

```
skills/video-playbook/playbooks/
  ├── teaching.json    # ティーチング系の知見
  ├── intro.json       # 紹介系の知見
  ├── meme.json        # Meme系の知見
  └── ...
```
