---
description: "When the user says /start-18-9 — Module 18 Lesson 18-9: PM - システム構成図 & API設計"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "30分"
category: "lesson"
prerequisites: ["start-18-8", "output/pm/er-diagram.puml"]
level: "intermediate"
tags: ["pm", "architecture", "api", "network"]
---

# 🎓 Lesson 18-9: システム構成図 & API設計

| 項目 | 内容 |
|------|------|
| ゴール | TaskFlowのシステム構成図、ネットワーク構成図（PlantUML）、API仕様書（OpenAPI YAML）を作成する |
| 所要時間 | 約30分 |
| 使うスキル | diagram-generator スキル |
| 前提条件 | Lesson 18-8 完了、output/pm/er-diagram.puml が存在する |
| 教材ページ | [Module 18](https://ai-agent.camp/ja/course/module-18) |

---

## 📍 Step 1: システム構成図（PlantUML）

システム全体のアーキテクチャを図で表現します。TaskFlowのコンポーネント、層構成、依存関係を可視化します。

```json
{
  "type": "AskQuestion",
  "id": "architecture_choice",
  "question": "TaskFlowのアーキテクチャを選んでください",
  "description": "システム全体の設計パターンを決定します。規模、複雑度、スケーラビリティを考慮してください。",
  "options": [
    {
      "label": "モノリス（シンプル）",
      "value": "monolith_simple",
      "description": "フロントエンド、バックエンド、DBが密結合。初期段階向け、開発速度重視"
    },
    {
      "label": "モノリス+外部サービス",
      "value": "monolith_external",
      "description": "メール送信、プッシュ通知など機能を外部SaaS連携。スケーラビリティ改善"
    },
    {
      "label": "マイクロサービス",
      "value": "microservices",
      "description": "認証、タスク、プロジェクト、通知など機能ごとにサービス分離。複雑度高、スケーラビリティ高"
    },
    {
      "label": "サーバーレス",
      "value": "serverless",
      "description": "AWS Lambda、Cloud Functions等を活用。運用コスト低、スケーラビリティ極大"
    }
  ]
}
```

### システム構成図の要素

選択したアーキテクチャに応じて、以下のコンポーネントを描画します：

**共通コンポーネント:**
- **フロントエンド層**: React/Next.js, TypeScript, Tailwind CSS
- **API Gateway / Load Balancer**: リクエスト振り分け、キャッシング
- **バックエンド層**: Node.js/Express, RESTful API, ビジネスロジック
- **データベース層**: PostgreSQL（主DB）、Redis（キャッシュ）
- **認証・認可**: JWT、OAuth2、セッション管理

**オプションコンポーネント（アーキテクチャ別）:**
- モノリス+外部: メール送信（SendGrid/AWS SES）、プッシュ通知（Firebase Cloud Messaging）
- マイクロサービス: Auth Service, Task Service, Project Service, Notification Service, Message Queue（RabbitMQ/Kafka）
- サーバーレス: Lambda Functions, DynamoDB, S3, API Gateway (AWS)

**出力ファイル**: `output/pm/system-architecture.puml`

```plaintext
PlantUML構文例：
@startuml SystemArchitecture
!define AWSPUML https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/v18.0/dist
!include AWSPUML/ApplicationIntegration/APIGateway.puml
!include AWSPUML/ApplicationIntegration/SimpleQueueService.puml
!include AWSPUML/Compute/Lambda.puml
!include AWSPUML/Database/RDS.puml

rectangle "クライアント層" {
  component [Web UI\n(React/Next.js)] as WebUI
  component [Mobile App\n(React Native)] as MobileApp
}

rectangle "API層" {
  component [API Gateway] as Gateway
}

rectangle "ビジネスロジック層" {
  component [Authentication Service] as Auth
  component [Task Service] as TaskSvc
  component [Project Service] as ProjectSvc
  component [Notification Service] as NotifSvc
}

rectangle "データ層" {
  component [PostgreSQL] as MainDB
  component [Redis Cache] as Cache
}

rectangle "外部連携" {
  component [SendGrid\n(Email)] as Email
  component [Firebase Cloud\nMessaging] as FCM
}

WebUI --> Gateway
MobileApp --> Gateway
Gateway --> Auth
Gateway --> TaskSvc
Gateway --> ProjectSvc
Auth --> MainDB
TaskSvc --> MainDB
TaskSvc --> Cache
ProjectSvc --> MainDB
NotifSvc --> Email
NotifSvc --> FCM

@enduml
```

---

## 🚀 Step 2: ネットワーク構成図（PlantUML）

本番環境におけるインフラストラクチャの構成を図で表現します。VPC、サブネット、セキュリティグループ、CDN等を含めます。

```json
{
  "type": "AskQuestion",
  "id": "deployment_env",
  "question": "デプロイ環境を選んでください",
  "description": "本番環境となるクラウドプロバイダーまたはオンプレミスを選択します。各環境でのアーキテクチャが異なります。",
  "options": [
    {
      "label": "AWS",
      "value": "aws",
      "description": "EC2/ECS, RDS, S3, CloudFront, ALB, VPC, Route 53。業界標準、豊富なサービス"
    },
    {
      "label": "GCP",
      "value": "gcp",
      "description": "Compute Engine, Cloud SQL, Cloud Storage, Cloud CDN, Load Balancer, VPC"
    },
    {
      "label": "Azure",
      "value": "azure",
      "description": "Virtual Machines, Azure SQL Database, Blob Storage, Azure CDN, Application Gateway"
    },
    {
      "label": "オンプレミス",
      "value": "onpremise",
      "description": "物理サーバー、自社データセンター。初期投資高、完全な管理権"
    }
  ]
}
```

### ネットワーク構成図の要素

選択した環境に応じて、以下を描画します：

**AWS構成:**
- **インターネットゾーン**: Route 53（DNS）、CloudFront（CDN）
- **VPC**: CIDR 10.0.0.0/16
  - Public Subnet (AZ-a): 10.0.1.0/24 → ALB, NAT Gateway
  - Private Subnet (AZ-a): 10.0.10.0/24 → ECS/EC2
  - Private Subnet (AZ-b): 10.0.11.0/24 → RDS（Multi-AZ）
- **セキュリティグループ**: ALB-SG, App-SG, DB-SG
- **ELB**: Application Load Balancer（80, 443）
- **コンピュート**: ECS on EC2 / EC2 Auto Scaling Group
- **ストレージ**: RDS PostgreSQL（Multi-AZ）, S3（ユーザーファイル、ログ）
- **その他**: CloudWatch, VPC Flow Logs, NAT Gateway

**GCP構成:**
- Cloud Load Balancing（外部）
- VPC Network（default）
  - Public Subnetwork: Cloud NAT, Cloud Router
  - Private Subnetwork: GKE Cluster / Compute Engine
- Cloud SQL（PostgreSQL）
- Cloud Storage（ユーザーファイル）
- Cloud CDN

**Azure構成:**
- Azure Front Door（Global Load Balancer）
- Virtual Network
  - Subnet 1: Application Gateway, NAT Gateway
  - Subnet 2: Virtual Machines / AKS
- Azure SQL Database（PostgreSQL）
- Blob Storage
- Azure CDN

**出力ファイル**: `output/pm/network-diagram.puml`

```plaintext
PlantUML構文例（AWS）:
@startuml NetworkArchitecture
rectangle "インターネット" as Internet

rectangle "AWS Account" {
  rectangle "VPC: 10.0.0.0/16" {
    rectangle "Public Subnet (AZ-a): 10.0.1.0/24" {
      component [ALB (80, 443)] as ALB
      component [NAT Gateway] as NAT
    }

    rectangle "Private Subnet (AZ-a): 10.0.10.0/24" {
      component [ECS Cluster\n(App Servers)] as AppA
    }

    rectangle "Private Subnet (AZ-b): 10.0.11.0/24" {
      component [ECS Cluster\n(App Servers)] as AppB
    }

    rectangle "Private Subnet (AZ-a): 10.0.20.0/24" {
      component [RDS Primary\n(PostgreSQL)] as DBPrimary
    }

    rectangle "Private Subnet (AZ-b): 10.0.21.0/24" {
      component [RDS Standby\n(Multi-AZ)] as DBStandby
    }
  }

  rectangle "S3 & CloudFront" {
    component [S3 Bucket] as S3
    component [CloudFront CDN] as CF
  }

  rectangle "Monitoring" {
    component [CloudWatch] as CW
  }
}

rectangle "Route 53" as R53

Internet --> R53
R53 --> CF
CF --> S3
R53 --> ALB
ALB --> AppA
ALB --> AppB
AppA --> NAT
AppB --> NAT
NAT --> Internet
AppA --> DBPrimary
AppB --> DBPrimary
DBPrimary --> DBStandby
AppA --> CW
AppB --> CW

@enduml
```

---

## ⚠️ Step 3: API一覧・仕様書（OpenAPI/Swagger YAML）

RESTful APIの全エンドポイントを詳細に定義します。リクエスト・レスポンス形式、パラメータ、認証方式、ステータスコード、エラーハンドリングを記述します。

```json
{
  "type": "AskQuestion",
  "id": "api_style",
  "question": "API設計のスタイルを選んでください",
  "description": "異なるAPI設計パラダイムがあります。保守性、クライアント側の実装難度、スケーラビリティを考慮してください。",
  "options": [
    {
      "label": "RESTful",
      "value": "restful",
      "description": "HTTP メソッド（GET/POST/PUT/DELETE）を活用。設計規約明確、キャッシング容易"
    },
    {
      "label": "GraphQL",
      "value": "graphql",
      "description": "クライアント側で必要なデータ指定。オーバーフェッチング削減、複雑な応答スキーマに対応"
    },
    {
      "label": "REST+GraphQLハイブリッド",
      "value": "hybrid",
      "description": "REST主体に、複雑クエリはGraphQL `/graphql` エンドポイント。段階的移行可能"
    }
  ]
}
```

### API仕様書の要素

**OpenAPI 3.0 YAML フォーマット:**
- **基本情報**: title, version, description, servers, info.contact
- **認証**: securitySchemes（JWT Bearer Token, OAuth2）
- **エンドポイント定義**:
  - パス（path）、HTTPメソッド
  - 説明（description）、サマリー（summary）
  - パラメータ（path, query, header, cookie）
  - リクエストボディ（request body schema）
  - レスポンス（status code ごとの schema）
  - セキュリティ要件

### TaskFlow API エンドポイント一覧

**認証（Authentication）**
1. `POST /auth/register` - ユーザー登録
2. `POST /auth/login` - ログイン（JWT発行）
3. `POST /auth/refresh` - トークンリフレッシュ
4. `POST /auth/logout` - ログアウト
5. `POST /auth/password-reset` - パスワードリセット要求

**ユーザー（Users）**
6. `GET /users/me` - 現在のユーザー情報取得
7. `PUT /users/me` - ユーザー情報更新（プロフィール）
8. `DELETE /users/me` - アカウント削除
9. `GET /users/{userId}` - ユーザー詳細取得
10. `GET /users` - ユーザー一覧検索（管理者のみ）

**プロジェクト（Projects）**
11. `GET /projects` - プロジェクト一覧取得（フィルター、ページネーション対応）
12. `POST /projects` - プロジェクト作成
13. `GET /projects/{projectId}` - プロジェクト詳細取得
14. `PUT /projects/{projectId}` - プロジェクト更新
15. `DELETE /projects/{projectId}` - プロジェクト削除
16. `GET /projects/{projectId}/members` - プロジェクトメンバー一覧
17. `POST /projects/{projectId}/members` - メンバー招待
18. `DELETE /projects/{projectId}/members/{userId}` - メンバー削除

**タスク（Tasks）**
19. `GET /tasks` - タスク一覧取得（プロジェクト、ステータス、担当者でフィルター）
20. `POST /tasks` - タスク作成
21. `GET /tasks/{taskId}` - タスク詳細取得
22. `PUT /tasks/{taskId}` - タスク更新（ステータス、期限、説明等）
23. `DELETE /tasks/{taskId}` - タスク削除
24. `POST /tasks/{taskId}/assign` - タスク割り当て
25. `GET /tasks/{taskId}/comments` - コメント一覧
26. `POST /tasks/{taskId}/comments` - コメント追加
27. `POST /tasks/{taskId}/attachments` - ファイル添付

**通知（Notifications）**
28. `GET /notifications` - 通知一覧取得
29. `POST /notifications/{notificationId}/read` - 通知既読
30. `DELETE /notifications/{notificationId}` - 通知削除
31. `PUT /notifications/settings` - 通知設定変更（メール、プッシュ等）

**出力ファイル**: `output/pm/api-spec.yaml`

```yaml
openapi: 3.0.3
info:
  title: TaskFlow API
  description: タスク管理・プロジェクト協業プラットフォーム API
  version: 1.0.0
  contact:
    name: TaskFlow Support
    email: support@taskflow.example.com

servers:
  - url: https://api.taskflow.example.com/v1
    description: Production
  - url: http://localhost:8000/v1
    description: Development

security:
  - bearerAuth: []

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        avatar_url:
          type: string
          format: uri
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    Project:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        description:
          type: string
        owner_id:
          type: string
          format: uuid
        members_count:
          type: integer
        tasks_count:
          type: integer
        status:
          type: string
          enum: [active, archived]
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    Task:
      type: object
      properties:
        id:
          type: string
          format: uuid
        project_id:
          type: string
          format: uuid
        title:
          type: string
        description:
          type: string
        status:
          type: string
          enum: [todo, in_progress, review, done]
        priority:
          type: string
          enum: [low, medium, high, critical]
        assigned_to:
          type: string
          format: uuid
        due_date:
          type: string
          format: date
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    Error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: object

paths:
  /auth/register:
    post:
      summary: ユーザー登録
      description: 新規ユーザーアカウントを作成します
      tags:
        - Authentication
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 8
                name:
                  type: string
              required:
                - email
                - password
                - name
      responses:
        '201':
          description: ユーザー作成成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  user:
                    $ref: '#/components/schemas/User'
                  token:
                    type: string
                    description: JWT access token
        '400':
          description: リクエスト形式エラー
        '409':
          description: ユーザー既に存在

  /auth/login:
    post:
      summary: ログイン
      description: メールアドレスとパスワードでログインし、JWTトークンを取得します
      tags:
        - Authentication
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
              required:
                - email
                - password
      responses:
        '200':
          description: ログイン成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  user:
                    $ref: '#/components/schemas/User'
                  token:
                    type: string
                  refresh_token:
                    type: string
        '401':
          description: 認証失敗（メール or パスワード不正）

  /users/me:
    get:
      summary: 現在のユーザー情報取得
      tags:
        - Users
      responses:
        '200':
          description: ユーザー情報
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '401':
          description: 認証失敗

    put:
      summary: ユーザー情報更新
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                avatar_url:
                  type: string
                  format: uri
      responses:
        '200':
          description: 更新成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: リクエスト形式エラー
        '401':
          description: 認証失敗

  /projects:
    get:
      summary: プロジェクト一覧取得
      tags:
        - Projects
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [active, archived]
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: プロジェクト一覧
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Project'
                  pagination:
                    type: object
                    properties:
                      total:
                        type: integer
                      page:
                        type: integer
                      limit:
                        type: integer

    post:
      summary: プロジェクト作成
      tags:
        - Projects
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                description:
                  type: string
              required:
                - name
      responses:
        '201':
          description: プロジェクト作成成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Project'
        '400':
          description: リクエスト形式エラー

  /tasks:
    get:
      summary: タスク一覧取得
      tags:
        - Tasks
      parameters:
        - name: project_id
          in: query
          schema:
            type: string
            format: uuid
        - name: status
          in: query
          schema:
            type: string
            enum: [todo, in_progress, review, done]
        - name: assigned_to
          in: query
          schema:
            type: string
            format: uuid
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 50
      responses:
        '200':
          description: タスク一覧
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Task'
                  pagination:
                    type: object

    post:
      summary: タスク作成
      tags:
        - Tasks
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                project_id:
                  type: string
                  format: uuid
                title:
                  type: string
                description:
                  type: string
                priority:
                  type: string
                  enum: [low, medium, high, critical]
                due_date:
                  type: string
                  format: date
              required:
                - project_id
                - title
      responses:
        '201':
          description: タスク作成成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          description: リクエスト形式エラー
```

---

## ✅ Step 4: アーキテクチャレビュー

作成したシステム構成図、ネットワーク構成図、API仕様書が実装ニーズに適切であるか、複数の観点からレビューします。

```json
{
  "type": "AskQuestion",
  "id": "review_perspective",
  "question": "レビュー観点を選んでください",
  "description": "以下の観点から、提案するアーキテクチャを評価します。複数選択可能です。",
  "options": [
    {
      "label": "スケーラビリティ",
      "value": "scalability",
      "description": "ユーザー数増加、データ量増加に対応できるか。水平スケーリング、垂直スケーリングの余地"
    },
    {
      "label": "セキュリティ",
      "value": "security",
      "description": "データ暗号化、認証認可、ネットワークセキュリティ。OWASP Top 10 対応、プライバシー（GDPR等）"
    },
    {
      "label": "コスト最適化",
      "value": "cost_optimization",
      "description": "インフラ費用、運用コスト、人員コスト。ROI、初期投資 vs 長期運用コスト"
    },
    {
      "label": "すべて",
      "value": "all",
      "description": "スケーラビリティ、セキュリティ、コスト最適化の全観点から包括的にレビュー"
    }
  ]
}
```

### レビュー項目

**スケーラビリティ観点:**
- [ ] ロードバランサーによる負荷分散が設計されているか
- [ ] データベースレプリケーション / シャーディング戦略が明記されているか
- [ ] キャッシュレイヤー（Redis等）の活用で読み取り性能改善できるか
- [ ] CDNによる静的アセット配信で配信遅延削減できるか
- [ ] APIのレート制限、キューイング機構で トラフィックスパイク対応可能か
- [ ] 非同期処理（Job Queue等）で長時間処理の影響を軽減できるか

**セキュリティ観点:**
- [ ] HTTPS/TLS 1.2以上で全通信暗号化されるか
- [ ] JWT / OAuth2による認証認可が実装されるか
- [ ] パスワードハッシュ化（bcrypt等）、ソルト生成されるか
- [ ] SQLインジェクション対策（プリペアドステートメント）されるか
- [ ] CORS設定が適切か（Origin制限）
- [ ] VPC、セキュリティグループで通信制限されるか
- [ ] データベース暗号化（at-rest）、バックアップ戦略があるか
- [ ] ログ監視、アラート機構（CloudWatch等）が設定されるか
- [ ] レート制限、DDoS対策（AWS Shield等）が有効か

**コスト最適化観点:**
- [ ] クラウドプロバイダーの従量課金制で無駄がないか
- [ ] リザーブドインスタンス・スポットインスタンスの活用可能性あるか
- [ ] CDN、オブジェクトストレージのコスト試算済みか
- [ ] データベース容量、バックアップ保持期間が最適か
- [ ] 監視・ログ保持期間を制限することでコスト削減可能か
- [ ] マネージドサービス活用（RDS、ElastiCache等）で運用コスト削減できるか
- [ ] マルチリージョン展開が必要か、または単一リージョンで十分か

---

## 📊 チェックリスト

以下の成果物が生成されたことを確認してください：

```json
{
  "type": "Checkpoint",
  "items": [
    {
      "item": "システム構成図作成済み",
      "file": "output/pm/system-architecture.puml",
      "validation": "PlantUML構文が正当、コンポーネント図で主要なシステムコンポーネント5個以上描画"
    },
    {
      "item": "ネットワーク構成図作成済み",
      "file": "output/pm/network-diagram.puml",
      "validation": "選択したクラウド環境（AWS/GCP/Azure）のリージョン、サブネット、セキュリティグループが明記"
    },
    {
      "item": "API 10エンドポイント以上定義",
      "file": "output/pm/api-spec.yaml",
      "validation": "OpenAPI 3.0形式で、GET/POST/PUT/DELETEを含む10個以上のpath定義、各エンドポイントにrequestBody、responses定義"
    },
    {
      "item": "OpenAPI YAML valid",
      "file": "output/pm/api-spec.yaml",
      "validation": "YAML構文エラーなし。オンライン validator (swagger.io) で validate可能"
    },
    {
      "item": "全3ファイル生成済み",
      "files": [
        "output/pm/system-architecture.puml",
        "output/pm/network-diagram.puml",
        "output/pm/api-spec.yaml"
      ],
      "validation": "3ファイルすべてが指定ディレクトリに存在し、内容が空でない"
    }
  ]
}
```

---

## 🔧 トラブルシューティング

| 問題 | 解決方法 |
|------|----------|
| PlantUML構文エラー | `@startuml` と `@enduml` で正しく囲む。component, rectangle, arrow構文を確認。オンライン editor (plantuml.com) で検証 |
| OpenAPI YAML 解析エラー | インデントをスペース2個で統一。`components`, `schemas`, `paths` の階層が正しいか確認。https://www.swagger.io/tools/swagger-editor/ で validate |
| アーキテクチャ選択の判断困難 | TaskFlow規模・スケジュール・チーム規模を考慮。初期段階はモノリス推奨（開発速度）→ 成長に応じてマイクロサービス検討 |
| ネットワーク構成 AWS 知識不足 | VPC CIDR (/16), Subnet CIDR (/24), Route Table, Network ACL, Security Group の基本概念を復習。AZとは Availability Zone（障害分離） |
| API設計 REST vs GraphQL 判定困難 | REST: 単純クエリ、キャッシング重視 → RESTful推奨。複雑な応答構造、クライアント多様性 → GraphQL推奨 |
| PlantUML ファイル保存 | .puml ファイルを UTF-8 エンコーディングで保存。パス区切りはスラッシュ `/` を使用 |


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/pm/
└── system-architecture.puml  (システムアーキテクチャ図)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/pm/system-architecture.puml

# 冒頭を確認（最初の30行）
head -30 output/pm/system-architecture.puml
```

> 💡 全文を確認: `cat output/pm/system-architecture.puml` で全文表示できます

---

## ➡️ Next: Lesson 18-10

次のレッスンでは、TaskFlow プロジェクトの **WBS（Work Breakdown Structure）** と **ガントチャート** を作成します。システム構成図、API仕様書をもとに、具体的な開発タスク、リソース割り当て、スケジュール計画を立案します。

- **WBS**: プロジェクトを機能別、モジュール別に分解
- **ガントチャート**: 各タスクの開始日、終了日、依存関係、リソース割り当て（PM、エンジニア等）を可視化
- **マイルストーン**: α版、β版、GA等の重要イベント

→ [Lesson 18-10: WBS & ガントチャート](./start-18-10.md)
