#!/usr/bin/env python3
"""
図表・フロー図生成スクリプト（Final Example）

このスクリプトを実行すると、各種図表を生成します。

必要条件:
- Gemini APIキー（環境変数 GEMINI_API_KEY）
- Python 3.9以上

使用方法:
    python generate_diagrams.py --all
    python generate_diagrams.py --type flowchart --topic "経費精算フロー"
"""

import os
import sys
import argparse
from pathlib import Path

# プロジェクトルートのtoolsをインポートパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    from tools.generate_diagram import generate_diagram
    HAS_DIAGRAM_GENERATOR = True
except ImportError:
    HAS_DIAGRAM_GENERATOR = False
    print("Warning: generate_diagram モジュールが見つかりません")


# 図表タイプ設定
DIAGRAM_TYPES = {
    "flowchart": {
        "description": "フローチャート",
        "style": "flowchart"
    },
    "sequence": {
        "description": "シーケンス図",
        "style": "sequence"
    },
    "infographic": {
        "description": "インフォグラフィック",
        "style": "infographic"
    },
    "architecture": {
        "description": "システム構成図",
        "style": "architecture"
    }
}

# サンプル図表定義
SAMPLE_DIAGRAMS = {
    "flow-expense-approval": {
        "type": "flowchart",
        "name": "経費精算承認フロー",
        "description": """
経費精算の承認フローを図解:

1. 申請者が経費申請を作成
2. 直属の上司が内容を確認
3. 金額判定: 10万円以上?
   - Yes: 部長承認へ
   - No: 経理部へ
4. 部長が承認/却下を判断
5. 経理部が最終確認
6. 承認されれば振込処理
7. 却下の場合は申請者に差し戻し

判断分岐を明確に、各ステップの担当者も表示
"""
    },
    
    "flow-recruitment": {
        "type": "flowchart",
        "name": "採用選考フロー",
        "description": """
採用選考のフローを図解:

1. 応募書類受付
2. 書類審査
   - 通過: 一次面接へ
   - 不通過: 見送り通知
3. 一次面接（人事担当）
   - 通過: 二次面接へ
   - 不通過: 見送り通知
4. 二次面接（部門責任者）
   - 通過: 最終面接へ
   - 不通過: 見送り通知
5. 最終面接（役員）
   - 通過: 内定通知
   - 不通過: 見送り通知
6. 内定承諾確認
7. 入社手続き

各段階でのフィードバックループも表示
"""
    },
    
    "flow-bug-fix": {
        "type": "flowchart",
        "name": "バグ修正ワークフロー",
        "description": """
バグ修正のワークフローを図解:

1. バグ報告受付
2. トリアージ（優先度判定）
   - Critical: 即時対応
   - High: 24時間以内
   - Medium: 1週間以内
   - Low: バックログ登録
3. 担当者アサイン
4. 原因調査
5. 修正実装
6. コードレビュー
   - 承認: テストへ
   - 却下: 修正へ戻る
7. テスト実施
   - 合格: リリースへ
   - 不合格: 修正へ戻る
8. ステージング環境デプロイ
9. 本番環境デプロイ
10. バグクローズ
"""
    },
    
    "infographic-ai-adoption": {
        "type": "infographic",
        "name": "AI導入統計",
        "description": """
企業のAI導入に関する統計インフォグラフィック:

■ AI導入状況（2025年）
- 導入済み: 45%
- 検討中: 30%
- 未検討: 25%

■ 導入効果（導入企業の報告）
- 業務効率: 30%向上
- コスト: 20%削減
- 従業員満足度: 15%向上
- エラー率: 40%削減

■ 導入分野TOP5
1. カスタマーサポート（65%）
2. データ分析（58%）
3. 文書作成（52%）
4. コード生成（45%）
5. マーケティング（38%）

円グラフ、棒グラフ、アイコンを組み合わせて視覚的に
"""
    }
}

# PlantUML テンプレート
PLANTUML_TEMPLATES = {
    "sequence-api-call": """
@startuml sequence-api-call
title API呼び出しシーケンス

skinparam backgroundColor #FEFEFE
skinparam sequenceArrowThickness 2
skinparam roundcorner 10
skinparam sequenceParticipant underline

actor User as user
participant "Frontend\\n(React)" as fe
participant "API Gateway\\n(Kong)" as gw
participant "Backend\\n(FastAPI)" as be
database "Database\\n(PostgreSQL)" as db

user -> fe: ログインボタンクリック
activate fe

fe -> gw: POST /api/auth/login
activate gw

gw -> be: 認証リクエスト
activate be

be -> db: ユーザー検索
activate db
db --> be: ユーザー情報
deactivate db

be -> be: パスワード検証

alt 認証成功
    be --> gw: JWT Token
    gw --> fe: 200 OK + Token
    fe --> user: ダッシュボード表示
else 認証失敗
    be --> gw: 401 Unauthorized
    gw --> fe: 401 Error
    fe --> user: エラーメッセージ表示
end

deactivate be
deactivate gw
deactivate fe

@enduml
""",
    
    "architecture-system": """
@startuml architecture-system
title システム構成図

skinparam backgroundColor #FEFEFE
skinparam componentStyle rectangle

cloud "Internet" {
    [User Browser] as browser
    [Mobile App] as mobile
}

node "AWS Cloud" {
    node "Edge" {
        [CloudFront] as cf
        [WAF] as waf
    }
    
    node "Application Layer" {
        [ALB] as alb
        
        frame "ECS Cluster" {
            [Frontend Container] as fe
            [Backend Container] as be
            [Worker Container] as worker
        }
    }
    
    node "Data Layer" {
        database "RDS\\n(PostgreSQL)" as rds
        database "ElastiCache\\n(Redis)" as redis
        storage "S3\\n(Assets)" as s3
    }
    
    node "Messaging" {
        queue "SQS" as sqs
    }
}

cloud "External Services" {
    [Slack API] as slack
    [Gmail API] as gmail
}

browser --> cf
mobile --> cf
cf --> waf
waf --> alb
alb --> fe
alb --> be
fe --> be
be --> rds
be --> redis
be --> s3
be --> sqs
sqs --> worker
worker --> slack
worker --> gmail

@enduml
"""
}


def generate_diagram_image(diagram_config: dict, output_dir: Path) -> str:
    """図表画像を生成"""
    name = diagram_config.get("name", "diagram")
    description = diagram_config.get("description", "")
    diagram_type = diagram_config.get("type", "flowchart")
    
    output_path = output_dir / f"{name.replace(' ', '-').lower()}.png"
    
    if HAS_DIAGRAM_GENERATOR:
        # 実際の生成
        result = generate_diagram(
            topic=description,
            style=diagram_type,
            output_path=str(output_path)
        )
        print(f"✅ 生成完了: {output_path}")
        return str(output_path)
    else:
        # プロンプトのみ出力（モック）
        prompt_file = output_dir / f"prompt-{name.replace(' ', '-').lower()}.txt"
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(f"# {name} 生成プロンプト\n\n")
            f.write(f"タイプ: {diagram_type}\n\n")
            f.write("---\n\n")
            f.write(description)
        
        print(f"📝 プロンプト保存: {prompt_file}")
        return str(prompt_file)


def save_plantuml(name: str, content: str, output_dir: Path) -> str:
    """PlantUMLファイルを保存"""
    output_path = output_dir / f"{name}.puml"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ PlantUML保存: {output_path}")
    return str(output_path)


def generate_all(output_dir: Path):
    """全図表を生成"""
    print("=" * 50)
    print("図表一括生成")
    print("=" * 50)
    
    # 画像図表
    print("\n▶ 画像図表の生成")
    for key, config in SAMPLE_DIAGRAMS.items():
        print(f"\n  生成中: {config['name']}")
        try:
            generate_diagram_image(config, output_dir)
        except Exception as e:
            print(f"  ❌ エラー: {e}")
    
    # PlantUML
    print("\n▶ PlantUMLファイルの生成")
    for name, content in PLANTUML_TEMPLATES.items():
        save_plantuml(name, content, output_dir)
    
    print("\n" + "=" * 50)
    print("生成完了")
    print("=" * 50)
    print(f"\nPlantUML表示方法:")
    print(f"  1. https://www.plantuml.com/plantuml/uml/ にアクセス")
    print(f"  2. .puml ファイルの内容を貼り付け")
    print(f"  3. または: plantuml {output_dir}/*.puml")


def main():
    parser = argparse.ArgumentParser(description="図表生成スクリプト")
    parser.add_argument("--all", action="store_true", help="全図表を生成")
    parser.add_argument("--type", choices=DIAGRAM_TYPES.keys(), help="図表タイプ")
    parser.add_argument("--topic", type=str, help="トピック（--type使用時）")
    parser.add_argument("--output", type=str, default=".", help="出力ディレクトリ")
    parser.add_argument("--list", action="store_true", help="サンプル図表一覧を表示")
    
    args = parser.parse_args()
    
    if args.list:
        print("サンプル図表一覧:")
        for key, config in SAMPLE_DIAGRAMS.items():
            print(f"  {key}: {config['name']} ({config['type']})")
        print("\nPlantUMLテンプレート:")
        for name in PLANTUML_TEMPLATES.keys():
            print(f"  {name}")
        return
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.all:
        generate_all(output_dir)
    elif args.type and args.topic:
        config = {
            "type": args.type,
            "name": args.topic,
            "description": args.topic
        }
        generate_diagram_image(config, output_dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
