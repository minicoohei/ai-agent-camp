# ECサイト システム設計仕様

## システム構成

### フロントエンド
- **技術**: Next.js (React)
- **役割**: ユーザーインターフェース、SSR/SSG
- **通信**: REST API / GraphQL でバックエンドと通信

### API サーバー
- **技術**: Node.js (Express) / Python (FastAPI)
- **役割**: ビジネスロジック、認証・認可、データ加工
- **エンドポイント**:
  - `GET /api/products` - 商品一覧取得
  - `POST /api/cart` - カート追加
  - `POST /api/orders` - 注文確定
  - `POST /api/payments` - 決済処理

### データベース
- **技術**: PostgreSQL（メイン）+ Redis（キャッシュ）
- **テーブル**: users, products, carts, orders, payments
- **特徴**: 商品検索はElasticsearchと連携

### 外部サービス
- **決済**: Stripe API（クレジットカード決済）
- **メール**: SendGrid（注文確認、配送通知）
- **配送**: ヤマト運輸 API（配送ステータス追跡）

## 主要フロー

### 商品検索フロー
1. ユーザーが検索キーワードを入力
2. フロントエンドが `GET /api/products?q=keyword` を送信
3. API サーバーが Elasticsearch にクエリ送信
4. 検索結果をフロントエンドに返却
5. ユーザーに商品一覧を表示

### カート追加フロー
1. ユーザーが「カートに追加」ボタンをクリック
2. フロントエンドが `POST /api/cart` を送信（商品ID、数量）
3. API サーバーが PostgreSQL のカートテーブルを更新
4. Redis キャッシュを更新
5. カート内容をフロントエンドに返却

### 決済フロー
1. ユーザーが「注文確定」ボタンをクリック
2. フロントエンドが `POST /api/orders` を送信
3. API サーバーが注文レコードを作成
4. Stripe API に決済リクエストを送信
5. 決済結果を API サーバーが受信
6. 注文ステータスを更新
7. SendGrid で注文確認メールを送信
8. ユーザーに完了画面を表示
