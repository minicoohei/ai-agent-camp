---
title: "Google Ads API を非エンジニアが3日で動かすまでの全ログ — MCC 〜 Basic Access 〜 dry-run 成功まで"
date: 2026-04-28
author: Kohei Nakamura (AI BRAIN PARTNERS / AI Agent Camp)
tags: [Google Ads API, Claude Code, OAuth, GitHub Actions, MCC, AI Agent Camp]
description: "MCC アカウント作成から開発者トークン承認、refresh_token 取得、CLI からのキャンペーン dry-run 成功まで。実際に詰まったポイント・回避策・コードを全部公開します。"
---

# Google Ads API を非エンジニアが3日で動かすまでの全ログ

> 2026-04-26 〜 2026-04-28 の3日間、Claude Code (Opus 4.7) と一緒に AI Agent Camp の Google Ads アカウントを API 経由で動かせる状態にした。途中で詰まった箇所、Google からの審査メール、コードの落とし穴、全部公開します。

---

## TL;DR

| 何を | 結果 |
|---|---|
| MCC（マネージャーアカウント）作成 | ✅ `973-949-4807` (AI BRAIN PARTNERS) |
| 既存広告アカウントを MCC 配下にリンク | ✅ `248-723-3509` (Ai Agent Camp) |
| Developer Token 取得 → Basic Access 承認 | ✅ 申請から **約 50 時間** で承認 |
| OAuth クライアント発行 → refresh_token 取得 | ✅ 1回ハマったけど解決 |
| Python CLI から `list_accessible_customers` | ✅ |
| dry-run でキャンペーン作成検証 | ✅ |
| GitHub Secrets に登録 / CI 連携準備 | ✅ |
| **総作業時間** | ローカル作業 **正味 90 分**＋ Google 審査の待ち時間 |

つまづきは大きく **3 箇所**:

1. 「APIセンターは MCC でしか開けない」を知らずに通常アカウントで申請しかけた
2. OAuth フローで `prompt='consent', access_type='offline'` 指定漏れで refresh_token が空で返ってきた
3. dry-run で `RESOURCE_NOT_FOUND` ＆ `contains_eu_political_advertising REQUIRED` が連続発生

それぞれの詳しい話と回避策を書く。

---

## なぜ Google Ads API を触りたかったか

Ai Agent Camp（非エンジニア向け AI エージェント講座）の集客で、これから本気で Google 広告を回す。**運用は CLI と GitHub Actions に乗せたい**。理由:

- 入札・予算・キーワードの調整を **コードレビュー可能な形** で残したい（履歴 + PR ベース運用）
- 配信レポートを **毎朝 Slack に自動投稿** したい
- A/B テストの結果を BigQuery に流して、他チャネル（Meta / TikTok）と統合分析したい

CLI 化が前提なら、Web UI のスクリーンショット運用ではなく **Google Ads API** を最初から叩ける状態にしておくのが正しい。

---

## 全体フロー（先に俯瞰）

```
1. MCC 作成（Web UI）            ← ここがスタート
2. 既存アカウントを MCC 配下にリンク
3. APIセンター → 開発者トークン申請（Test Access が即発行）
4. Basic Access 昇格申請 → 承認待ち（1〜3 営業日）
5. GCP プロジェクトで OAuth クライアント発行
6. refresh_token を CLI で取得
7. macOS Keychain に秘密情報を保存
8. ~/google-ads.yaml を Keychain から動的生成
9. API 疎通確認（list_accessible_customers）
10. dry-run でキャンペーン作成テスト
11. GitHub Secrets 登録 → CI 連携
```

それぞれ何が起きたか、順番に書く。

---

## Day 1 (2026-04-26)

### MCC ってまず何? — APIセンターは MCC でしか開けない

最初に詰まったのはここ。普通の Google Ads アカウント（Ai Agent Camp）で API センターを開こうとしたら、

> APIセンターは、クライアント センター（MCC）アカウントでのみご利用可能です。

と弾かれた。**Google Ads API を使うには必ず MCC が必要**。これは Google が「個人がいきなり API を叩いて事故るのを防ぐ」ためのゲート。

#### MCC 作成手順

1. <https://ads.google.com/home/tools/manager-accounts/> で「マネージャーアカウントを作成」
2. アカウント名は何でもいい（私は `AI BRAIN PARTNERS` に）
3. 用途: **「自社のアカウントを管理する」**
4. タイムゾーン (GMT+09:00) 日本標準時 / 通貨 JPY

完了すると 10 桁の Manager Customer ID が発行される。私の場合 `973-949-4807`。

#### 既存アカウントを MCC 配下にリンク

MCC にログインした状態で **管理 → サブアカウント → ＋ → 「既存のアカウントをリンク」** で Ai Agent Camp の Customer ID `248-723-3509` を入力 → 既存アカウント側でベルマークから承認。

⚠️ **これを後回しにすると後の `login_customer_id` 設定で混乱する**。先に済ませておくべき。

### 開発者トークンの申請

MCC で **ツールと設定 → セットアップ → APIセンター** へ。フォームに：

- 連絡先（メール・電話）
- 会社情報（会社名・URL・業種）
- API 用途: 「自社のキャンペーンを管理・レポート分析」
- 想定リクエスト数: 1日 1,000 以下（控えめに）

**申請直後に Test Access のトークンが発行される**（22文字程度の英数字）。これだけでテストアカウントなら API が叩ける状態になる。

ただし、本番のアカウントに対しては **Basic Access への昇格** が必要。同じ画面の「アクセスレベルをアップグレード」を押して申請。私が書いた申請文：

> We need Basic Access to manage our own Google Ads accounts (campaign creation,
> keyword management, performance reporting) programmatically. We do not provide
> tools to third parties. Daily request volume is expected to be under 1,000.

これで申請完了。あとは Google からのメールを待つ。

---

## Day 2 (2026-04-27) — OAuth フロー地獄

### Basic Access 申請受付メール

`2026-04-26 02:32` に「`[0-9529000040830] Your Google Ads API Basic Access Application`」というメールが届く。**「申請を受け付けました、混雑しているので少し時間がかかります」** という内容。これは Google の自動返信なので、ここから人手の審査待ち。

### OAuth クライアント作成

GCP コンソールでプロジェクト `aibrain-ads-api` を作成し、

1. APIs & Services → ライブラリ → **Google Ads API** を有効化
2. APIs & Services → OAuth consent screen → 外部 / アプリ名 / サポートメール / 連絡先入力
3. テストユーザーに MCC を作成した Google アカウントを追加（**忘れるとあとで弾かれる**）
4. Credentials → OAuth クライアントID → **デスクトップアプリ**
5. JSON をダウンロード

ダウンロードした JSON は `~/.config/google-ads/oauth_client.json` へ。

```bash
mkdir -p ~/.config/google-ads
mv ~/Downloads/client_secret_*.apps.googleusercontent.com.json \
   ~/.config/google-ads/oauth_client.json
chmod 600 ~/.config/google-ads/oauth_client.json
```

### refresh_token を CLI で取る

ここで 1 回ハマった。最初に書いた CLI スクリプトは:

```python
# ❌ これだと refresh_token が None で返ってくることがある
flow = InstalledAppFlow.from_client_secrets_file(client_file, scopes=SCOPES)
creds = flow.run_local_server(port=0)
print(creds.refresh_token)  # None
```

何度か実行しても `refresh_token` が空。原因は **`prompt` と `access_type` を省略していた**こと。Google は同じ scope に対して既に同意済みのアカウントには refresh_token を再発行しない。

#### 動いた版

```python
flow = InstalledAppFlow.from_client_secrets_file(client_file, scopes=SCOPES)
creds = flow.run_local_server(
    port=9876,
    prompt="consent",          # ← 必ず再同意を促す
    access_type="offline",     # ← refresh_token 発行のため
    open_browser=True,
)
```

これで 103 文字の refresh_token が無事返ってきた。

### macOS Keychain に保管する

「.env に書いておけばいいや」と思ったが、**.env はうっかり Git にコミットすると即詰む**。Mac なら Keychain が標準で入っているし、CLI からも操作できる。

```bash
# Developer Token (プロンプト方式: シェル履歴に値が残らない)
security add-generic-password -a "$USER" -s GOOGLE_ADS_DEVELOPER_TOKEN -U -w
# プロンプト → トークン貼り付け → Enter → 再入力 → Enter

# 残りも同様に各キーで保存
security add-generic-password -a "$USER" -s GOOGLE_ADS_CLIENT_ID -w "$CID" -U
security add-generic-password -a "$USER" -s GOOGLE_ADS_CLIENT_SECRET -w "$CSEC" -U
security add-generic-password -a "$USER" -s GOOGLE_ADS_REFRESH_TOKEN -w "$RT" -U
security add-generic-password -a "$USER" -s GOOGLE_ADS_LOGIN_CUSTOMER_ID -w "9739494807" -U
```

#### Keychain あるある罠

私は最初これを `-w` の後に値を書く形で実行したが、`-U` がパスワード扱いされてしまい dev_token に "U" だけが保存されるバグを踏んだ。**`-w` の後に値を書かない（プロンプト入力）パターンが安全**。

```bash
# ❌ 危険（クォート漏れで -U が値になる）
security add-generic-password -a "$USER" -s NAME -w -U

# ✅ 安全（プロンプトで聞かれる）
security add-generic-password -a "$USER" -s NAME -U -w
```

### `~/google-ads.yaml` を生成

```bash
DEV=$(security find-generic-password -a "$USER" -s GOOGLE_ADS_DEVELOPER_TOKEN -w)
CID=$(security find-generic-password -a "$USER" -s GOOGLE_ADS_CLIENT_ID -w)
CSEC=$(security find-generic-password -a "$USER" -s GOOGLE_ADS_CLIENT_SECRET -w)
RT=$(security find-generic-password -a "$USER" -s GOOGLE_ADS_REFRESH_TOKEN -w)
LCID=$(security find-generic-password -a "$USER" -s GOOGLE_ADS_LOGIN_CUSTOMER_ID -w)

cat > ~/google-ads.yaml <<EOF
developer_token: ${DEV}
client_id: ${CID}
client_secret: ${CSEC}
refresh_token: ${RT}
login_customer_id: ${LCID}
use_proto_plus: true
EOF
chmod 600 ~/google-ads.yaml
```

これで SDK が `GoogleAdsClient.load_from_storage("~/google-ads.yaml")` で読めるようになった。

---

## Day 3 (2026-04-28) — 承認 → 疎通 → dry-run 成功

朝に Basic Access 承認メールが届いた。申請から **約 50 時間** ぐらい。

### 疎通確認

```python
from google.ads.googleads.client import GoogleAdsClient
client = GoogleAdsClient.load_from_storage("~/google-ads.yaml", version="v21")
svc = client.get_service("CustomerService")
res = svc.list_accessible_customers()
for rn in res.resource_names:
    print(rn)
```

```
customers/2487233509   # Ai Agent Camp
customers/9739494807   # MCC
```

✅ 通った。

### dry-run キャンペーン作成 — 2 段階トラップ

ここが最後の難関。`scripts/gtm/manage_google_ads.py` から SEARCH キャンペーンを `validate_only=True` で投げたら、こんなエラーが連続で出た:

```
ERROR: REQUIRED at operations.create.contains_eu_political_advertising
```

#### 罠 1: EU 政治広告開示フィールド

2024 年に Google が追加したコンプラ要件。**新規キャンペーンでは必須**。普通のキャンペーンなら以下を設定するだけで OK:

```python
campaign.contains_eu_political_advertising = (
    enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
)
```

知らないと永遠にエラーで止まる。

#### 罠 2: dry-run で `RESOURCE_NOT_FOUND`

これは構造的な問題。**Budget と Campaign を別の API call で送る** と、dry-run の Campaign 側が「`campaign_budget` resource_name が存在しません」と弾く。validate_only でも resource 存在チェックは走るため。

#### 解決: `GoogleAdsService.mutate` で atomic batch

両方を 1 リクエストで送ると、`-1` の一時 resource_name で相互参照できる:

```python
BUDGET_TEMP = f"customers/{customer_id}/campaignBudgets/-1"

ops = []
mu_op_b = client.get_type("MutateOperation")
budget = mu_op_b.campaign_budget_operation.create
budget.resource_name = BUDGET_TEMP
budget.amount_micros = 3000 * 1_000_000
ops.append(mu_op_b)

mu_op_c = client.get_type("MutateOperation")
campaign = mu_op_c.campaign_operation.create
campaign.campaign_budget = BUDGET_TEMP   # ← 一時参照
campaign.contains_eu_political_advertising = (
    enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
)
# ...
ops.append(mu_op_c)

req = client.get_type("MutateGoogleAdsRequest")
req.customer_id = customer_id
req.mutate_operations.extend(ops)
req.validate_only = True   # dry-run
ga.mutate(request=req)
```

最終的にこれで動いた:

```
📦 batch: budget ¥3000/d + campaign 'AIAC Search Test' (SEARCH/MAXIMIZE_CONVERSIONS) [DRY-RUN]
✅ DRY-RUN PASSED — nothing was persisted.
```

🎉

### GitHub Secrets に登録

CI から呼べるようにすれば、**毎朝のレポート自動化**や **新規キャンペーンを PR ベースで承認制でデプロイ** が可能になる。

```bash
for k in GOOGLE_ADS_DEVELOPER_TOKEN GOOGLE_ADS_CLIENT_ID GOOGLE_ADS_CLIENT_SECRET \
         GOOGLE_ADS_REFRESH_TOKEN GOOGLE_ADS_LOGIN_CUSTOMER_ID; do
  v=$(security find-generic-password -a "$USER" -s "$k" -w)
  printf '%s' "$v" | gh secret set "$k" -b-
done
printf '%s' "2487233509" | gh secret set GOOGLE_ADS_CUSTOMER_ID -b-
```

ワークフローからは:

```yaml
- name: Build google-ads.yaml
  run: |
    cat > $HOME/google-ads.yaml <<EOF
    developer_token: ${{ secrets.GOOGLE_ADS_DEVELOPER_TOKEN }}
    client_id: ${{ secrets.GOOGLE_ADS_CLIENT_ID }}
    client_secret: ${{ secrets.GOOGLE_ADS_CLIENT_SECRET }}
    refresh_token: ${{ secrets.GOOGLE_ADS_REFRESH_TOKEN }}
    login_customer_id: ${{ secrets.GOOGLE_ADS_LOGIN_CUSTOMER_ID }}
    use_proto_plus: true
    EOF
```

---

## 実装したものまとめ

最終的に出来たもの:

```
docs/setup-guides/docs/GOOGLE_ADS_API_SETUP.md   # 詳細手順
scripts/gtm/manage_google_ads.py                  # CLI (199 行)
~/google-ads.yaml                                 # SDK 設定 (Keychain から生成)
~/.config/google-ads/oauth_client.json            # OAuth クライアント
```

CLI でできること:

```bash
# 1) アクセス可能アカウント一覧
$ python scripts/gtm/manage_google_ads.py list-customers
Accessible customers (2):
  - customers/2487233509
  - customers/9739494807

# 2) キャンペーン一覧
$ python scripts/gtm/manage_google_ads.py list-campaigns --customer-id 2487233509

# 3) dry-run キャンペーン作成
$ python scripts/gtm/manage_google_ads.py create-campaign \
    --customer-id 2487233509 \
    --name "AIAC Search Q2" --budget 5000 \
    --channel SEARCH --bid-strategy MAXIMIZE_CONVERSIONS \
    --dry-run
```

---

## 学び

### 1. Google API 系は **「ゲート」が多重に立っている**

MCC → APIセンター → Test Access → Basic Access → OAuth クライアント → refresh_token、と段階的に認可が要求される。**1 個飛ばすと先に進めない**。最初に全体マップを書いておくと迷子にならない。

### 2. **秘密情報のレイヤを分けるのは正しい**

| 用途 | 場所 |
|---|---|
| ローカル開発 | macOS Keychain |
| CI / GitHub Actions | GitHub Secrets |
| 本番運用 (将来) | Google Secret Manager / AWS Secrets Manager |

「`.env` に全部書く」だと Git 事故 1 回でアカウントが乗っ取られる。**Keychain は標準で入っていて無料、CI からは GH Secrets、本番は Secret Manager** という3層構造を最初から作るのが結果的に楽。

### 3. **dry-run は `validate_only=True` でも resource 存在チェックする**

これは知らないとハマる。`GoogleAdsService.mutate` で一時 resource_name (`-1`) を使った atomic batch にしないと、Budget と Campaign を別々に dry-run できない。

### 4. **API バージョンは v21（最新）を使う**

古いサンプルコードが v15 / v16 ベースで書かれていることが多いが、エンドポイントが変わっているので **必ず v21 のドキュメント** を見る。`google-ads-python` は最新 PyPI なら自動で対応している。

### 5. **AI ペアプロは「3 日かかる」を「半日」に縮める**

このログ全体、Claude Code (Opus 4.7) と一緒に進めた。
ハマるたびにエラーログを貼り付けると即座に「これは EU 政治広告フィールド未対応」「dry-run の resource 解決問題」と特定してくれる。
**人間が 1 人で Stack Overflow を彷徨う時間が 0**。

実工数で言うと、ローカル作業の正味時間は 90 分くらい。残りは Google の審査待ちと、ブラウザでの承認操作。

---

## 次にやること

1. 既存の Web UI 上に残っている下書きキャンペーン 4 件の整理
2. 実キャンペーン作成（`--no-dry-run`、PAUSED で作って Web UI で確認後 ENABLE）
3. **GitHub Actions ワークフロー追加** — 毎朝キャンペーン KPI を Slack 投稿
4. BigQuery にレポートを daily で sink → 他チャネルと統合分析

ここまでで「自社の広告アカウントを CLI ＋ PR ベースで運用できる」基盤は完成した。
あとは育てるだけ。

---

## 参考リンク

- [Google Ads API Documentation](https://developers.google.com/google-ads/api/docs/start)
- [google-ads-python (GitHub)](https://github.com/googleads/google-ads-python)
- [v21 Release Notes](https://developers.google.com/google-ads/api/docs/release-notes)
- 関連: [Google Ads API セットアップガイド](../setup-guides/docs/GOOGLE_ADS_API_SETUP.md) — 同じ内容を手順書フォーマットでまとめたもの

---

*この記事は AI Agent Camp（非エンジニア向け AI エージェント講座）の運営側で実際に踏んだ手順のログです。AI Agent Camp については [ai-agent.camp](https://ai-agent.camp) を見てください。*
