# module02-diagram 完成例

## 概要

ビジネスで頻出する3種類の図表（フローチャート、シーケンス図、組織図）をPlantUML/Draw.ioで作成し、画像に変換した完成例です。

## 成果物一覧

### PlantUML ソース

| ファイル | 図表タイプ | 説明 |
|----------|-----------|------|
| `source/sales-flow.puml` | アクティビティ図（フローチャート） | BtoB SaaS 営業プロセス5ステップ |
| `source/system-sequence.puml` | シーケンス図 | ECサイトの商品検索・カート・決済フロー |
| `source/org-chart.drawio` | 組織図（Draw.io XML） | IT企業4部門の組織構造 |

### 生成画像

| ファイル | スタイル | 説明 |
|----------|---------|------|
| `output/sales-flow.png` | minimalist | 営業フローのインフォグラフィック |
| `output/system-sequence.png` | colorful_infographic | ECサイトシーケンス図 |
| `output/org-chart.png` | colorful_infographic | 組織図のインフォグラフィック |

## 各図表の解説

### 営業プロセスフロー（sales-flow.puml）
- 5ステップの営業プロセスをアクティビティ図で表現
- 各ステップに担当者、アクション、ツール情報をノートで付記
- 見込み度による分岐（A/B → 商談継続、C → ナーチャリング）
- 受注/失注の分岐と後続アクションを含む

### ECサイトシーケンス図（system-sequence.puml）
- 6つのアクター/コンポーネント間の通信フローを表現
- 3つのシナリオ: 商品検索、カート追加、決済処理
- Redis キャッシュの利用パターン
- 決済成功/失敗の alt ブロックによる条件分岐

### 組織図（org-chart.drawio）
- CEO 直下に4部門: エンジニアリング、プロダクト、マーケティング、コーポレート
- 各部門に色を割り当て（青、緑、オレンジ、紫）
- 部門下にチーム（計9チーム）と人数を記載

## 使用ツール

- PlantUML 記法による図表ソース作成
- Draw.io XML による組織図作成
- `diagram-generator` スキル（`tools/generate_diagram.py`）による画像生成

## 学習ポイント

1. PlantUML 記法によるフローチャート・シーケンス図の作成手法
2. Draw.io XML によるリッチな組織図の構築
3. 図表の種類に応じた適切な表現形式の選択
4. ノート・分岐・ループなどのUML要素の活用
