# Google Ads API セットアップガイド

非エンジニアでも、コードから自社の Google 広告キャンペーンを操作・分析できる状態を構築します。
**MCC アカウント作成 → Basic Access 承認 → OAuth → CLI 疎通** までを 11 ステップで網羅。
（実際にこのガイドの手順をなぞって 2026-04-26〜04-28 の3日間で `Ai Agent Camp` 案件で構築完了したログそのままです）

---

## 概要

| 項目 | 内容 |
|------|------|
| 認証方式 | OAuth 2.0 + Developer Token |
| 対応サービス | Google Ads API v21（キャンペーン CRUD / レポート / 入札） |
| 無料枠 | API リクエスト 1日 15,000 ops（Basic Access） |
| 必要時間 | 初回 30 分 + 承認待ち 1〜3 営業日 |
| 最終形 | `~/google-ads.yaml` を読み込んだ Python CLI で `list-campaigns` / `create-campaign` 実行可 |

---

## できるようになること

```bash
# キャンペーン一覧取得
python scripts/gtm/manage_google_ads.py list-campaigns --customer-id 248-723-3509

# 新規キャンペーンを dry-run で検証 → 本番作成
python scripts/gtm/manage_google_ads.py create-campaign \
  --customer-id 248-723-3509 \
  --name "AIAC Search Test" --budget 3000 \
  --channel SEARCH --bid-strategy MAXIMIZE_CONVERSIONS \
  --dry-run
```

---

## 前提

| ツール | バージョン | 用途 |
|---|---|---|
| Python | 3.10+ | google-ads SDK |
| `google-ads` (PyPI) | 30.x | API クライアント |
| `google-auth-oauthlib` | 1.x | OAuth フロー |
| `gh` (GitHub CLI) | 2.x | Secrets 設定 |
| macOS Keychain (`security`) | 同梱 | 秘密情報の保管 |

```bash
python3 -m venv ~/.venvs/gads
~/.venvs/gads/bin/pip install google-ads google-auth-oauthlib pyyaml
```

---

## 全体フロー

```
1. MCC アカウント作成 (Web UI)
2. 既存広告アカウントを MCC 配下にリンク
3. APIセンターで開発者トークン取得 → Test Access が即発行
4. Basic Access へ昇格申請 → 承認 (1〜3営業日)
5. GCP プロジェクトで OAuth クライアント作成 (Desktop type)
6. OAuth Consent flow で refresh_token 取得 (CLI)
7. 秘密情報を macOS Keychain に保存
8. ~/google-ads.yaml を Keychain から動的生成
9. API 疎通確認 (list_accessible_customers)
10. dry-run キャンペーン作成
11. GitHub Secrets に登録 (CI 用)
```

---

## ステップ1: MCC アカウント作成

[https://ads.google.com/home/tools/manager-accounts/](https://ads.google.com/home/tools/manager-accounts/) で「マネージャーアカウントを作成」。

| 項目 | 値 |
|---|---|
| アカウント名 | 例: `AI BRAIN PARTNERS` |
| 主な用途 | **「自社のアカウントを管理する」** |
| 請求先国 | 日本 |
| タイムゾーン | (GMT+09:00) 日本標準時 |
| 通貨 | JPY (¥) |

完了すると 10 桁の **Manager Customer ID**（例: `973-949-4807`）が発行される。

**MCC かどうかの確認**: そのアカウントで <https://ads.google.com/aw/apicenter> にアクセスして APIセンター画面が開けば MCC、開けなければ通常アカウント。

---

## ステップ2: 既存アカウントを MCC 配下にリンク

1. MCC にログイン → **管理 → サブアカウント → ＋**
2. 「**既存のアカウントをリンク**」を選択
3. リンク対象の Customer ID を入力
4. 招待送信 → 既存アカウント側でベル通知から承認

API 疎通後の確認クエリ:

```python
ga = client.get_service("GoogleAdsService")
query = """
SELECT customer_client.id, customer_client.descriptive_name,
       customer_client.manager, customer_client.level, customer_client.status
FROM customer_client
"""
for row in ga.search(customer_id="<MCC_ID>", query=query):
    print(row.customer_client)
```

期待出力: MCC (level=0) + サブアカウント (level=1) が `ENABLED`。

---

## ステップ3: 開発者トークン取得（Test Access）

1. MCC にログイン → **ツールと設定 → セットアップ → APIセンター**
2. 申請フォームを記入:
   - 連絡先（氏名・メール・電話）
   - 会社情報（会社名・URL・業種）
   - **API 用途**: *自社の Google 広告キャンペーンを管理・レポート分析*
   - 想定リクエスト数/日: 控えめに（例: `< 1,000`）
3. 申請送信 → **Test Access のトークン**（22文字程度の英数字）が即発行

| アクセスレベル | 発行 | 操作可能対象 |
|---|---|---|
| Test Access | 即時 | テストアカウントのみ |
| Basic Access | 申請+承認 (1-3営業日) | 本番アカウント (1日 15,000 ops) |
| Standard Access | 別申請 | 本番アカウント (制限大幅緩和) |

⚠️ **本番アカウントを操作するには Basic Access 以上が必要**。

---

## ステップ4: Basic Access 申請 → 承認

APIセンター画面の「アクセスレベルをアップグレード」から申請。
申請文サンプル:

> We need Basic Access to manage our own Google Ads accounts (campaign creation,
> keyword management, performance reporting) programmatically. We do not provide
> tools to third parties. Daily request volume is expected to be under 1,000.

承認の通知メールは `no-reply@google.com` から件名 `[XXXX-XXXX-XXXX] Your Google Ads API Basic Access Application` で届く。

---

## ステップ5: GCP プロジェクトで OAuth クライアント作成

1. [Google Cloud Console](https://console.cloud.google.com/) でプロジェクトを作成（例: `aibrain-ads-api`）
2. **APIs & Services → ライブラリ** → "Google Ads API" を有効化
3. **APIs & Services → OAuth consent screen** を構成:
   - **外部** ユーザータイプ
   - アプリ名・サポートメール・連絡先入力
   - スコープは追加不要（後から SDK が `https://www.googleapis.com/auth/adwords` を要求）
   - **テストユーザー** に MCC を作成した Google アカウントを追加
4. **Credentials → ＋ 認証情報を作成 → OAuth クライアントID**:
   - **アプリケーションの種類: デスクトップアプリ**
   - 名前: `ads-cli` 等
5. JSON をダウンロード → `~/.config/google-ads/oauth_client.json` に保存

```bash
mkdir -p ~/.config/google-ads
mv ~/Downloads/client_secret_*.apps.googleusercontent.com.json \
   ~/.config/google-ads/oauth_client.json
chmod 600 ~/.config/google-ads/oauth_client.json
```

---

## ステップ6: refresh_token 取得 (CLI)

`~/.config/google-ads/run_oauth.py`:

```python
"""Run OAuth flow and save refresh_token."""
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

OUT = Path.home() / ".config/google-ads/refresh_token.txt"
CLIENT = Path.home() / ".config/google-ads/oauth_client.json"

flow = InstalledAppFlow.from_client_secrets_file(
    str(CLIENT),
    scopes=["https://www.googleapis.com/auth/adwords"],
)
creds = flow.run_local_server(
    port=9876, prompt="consent", access_type="offline", open_browser=True,
    success_message="OAuth 認可完了。ターミナルに戻ってください。",
)
OUT.write_text(creds.refresh_token)
OUT.chmod(0o600)
print(f"saved: {OUT} (length={len(creds.refresh_token)})")
```

実行:

```bash
~/.venvs/gads/bin/python ~/.config/google-ads/run_oauth.py
```

ブラウザで **MCC を作成した Google アカウント** を選択して承認。
「未確認のアプリ」警告が出たら「**詳細 → アプリ名(安全ではないページ)に移動**」→ Continue → Allow。

⚠️ **`prompt='consent', access_type='offline'`** を必ず指定する。これがないと `refresh_token` が返ってこない。

---

## ステップ7: 秘密情報を macOS Keychain に保存

```bash
# 1) Developer Token (22 文字)
security add-generic-password -a "$USER" -s GOOGLE_ADS_DEVELOPER_TOKEN -U -w
# プロンプトで貼り付け → Enter → 再入力 → Enter

# 2) OAuth Client ID
CID=$(python3 -c "import json; print(json.load(open('$HOME/.config/google-ads/oauth_client.json'))['installed']['client_id'])")
security add-generic-password -a "$USER" -s GOOGLE_ADS_CLIENT_ID -w "$CID" -U

# 3) OAuth Client Secret
CSEC=$(python3 -c "import json; print(json.load(open('$HOME/.config/google-ads/oauth_client.json'))['installed']['client_secret'])")
security add-generic-password -a "$USER" -s GOOGLE_ADS_CLIENT_SECRET -w "$CSEC" -U

# 4) Refresh Token
RT=$(cat ~/.config/google-ads/refresh_token.txt)
security add-generic-password -a "$USER" -s GOOGLE_ADS_REFRESH_TOKEN -w "$RT" -U

# 5) MCC Customer ID
security add-generic-password -a "$USER" -s GOOGLE_ADS_LOGIN_CUSTOMER_ID -w "9739494807" -U
```

取り出し:

```bash
security find-generic-password -a "$USER" -s GOOGLE_ADS_DEVELOPER_TOKEN -w
```

---

## ステップ8: `~/google-ads.yaml` を生成

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

⚠️ `~/google-ads.yaml` は **必ず .gitignore に追加**してコミットしないこと。

---

## ステップ9: API 疎通確認

```python
from google.ads.googleads.client import GoogleAdsClient
client = GoogleAdsClient.load_from_storage("~/google-ads.yaml", version="v21")
svc = client.get_service("CustomerService")
res = svc.list_accessible_customers()
for rn in res.resource_names:
    print(rn)
```

期待出力:

```
customers/2487233509   # Ai Agent Camp
customers/9739494807   # MCC
```

---

## ステップ10: dry-run キャンペーン作成

`scripts/gtm/manage_google_ads.py` を使って予算 + キャンペーンを **atomic** に検証:

```bash
~/.venvs/gads/bin/python scripts/gtm/manage_google_ads.py create-campaign \
    --customer-id 2487233509 \
    --name "AIAC Search Test" \
    --budget 3000 \
    --channel SEARCH \
    --bid-strategy MAXIMIZE_CONVERSIONS \
    --keywords "AIエージェント,AI自動化,AI業務効率化" \
    --dry-run
```

期待出力:

```
📦 batch: budget ¥3000/d + campaign 'AIAC Search Test' (SEARCH/MAXIMIZE_CONVERSIONS) [DRY-RUN]
✅ DRY-RUN PASSED — nothing was persisted.
```

ポイント:

- **`GoogleAdsService.mutate`** で予算とキャンペーンを 1 リクエストで送ると、`-1` の一時 resource_name で相互参照できる
- `validate_only=True` で本番には何も書き込まれない
- 本番作成は `--no-dry-run`、必ず `PAUSED` 状態で生成 → Web UI で確認後に有効化

---

## ステップ11: GitHub Secrets に登録（CI 連携）

```bash
for k in GOOGLE_ADS_DEVELOPER_TOKEN GOOGLE_ADS_CLIENT_ID GOOGLE_ADS_CLIENT_SECRET \
         GOOGLE_ADS_REFRESH_TOKEN GOOGLE_ADS_LOGIN_CUSTOMER_ID; do
  v=$(security find-generic-password -a "$USER" -s "$k" -w)
  printf '%s' "$v" | gh secret set "$k" -b-
done
printf '%s' "2487233509" | gh secret set GOOGLE_ADS_CUSTOMER_ID -b-

gh secret list | grep GOOGLE_ADS
```

GitHub Actions ワークフロー側で `~/google-ads.yaml` を CI で自動生成:

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
    chmod 600 $HOME/google-ads.yaml
```

---

## トラブルシュート

| 症状 | 原因 | 対処 |
|---|---|---|
| `User doesn't have permission to access customer` | `login_customer_id` が誤り or サブアカウント未リンク | yaml の `login_customer_id` を MCC ID に / ステップ2を実施 |
| `DeveloperTokenError DEVELOPER_TOKEN_NOT_APPROVED` | Test Access のまま本番アカウントにアクセス | Basic Access 承認待ち or テストアカウント使用 |
| `OAuth consent screen` でループ | `prompt='consent', access_type='offline'` 未指定 | ステップ6のスクリプトを確認 |
| `Address already in use` (port 9876) | 前回の OAuth プロセス残存 | `pkill -f run_oauth` 後に再実行 |
| `contains_eu_political_advertising REQUIRED` | 2024 規制で必須化されたフィールド未設定 | `EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING` をセット |
| `campaign_budget RESOURCE_NOT_FOUND` (dry-run) | Budget と Campaign を別呼び出しで dry-run | `GoogleAdsService.mutate` で同一バッチ送信に変更 |

---

## セキュリティ注意事項

- **`developer_token` / `client_secret` / `refresh_token` を Git にコミットしない**
- ローカルでは macOS Keychain、CI では GitHub Secrets を使用
- `~/google-ads.yaml` は `chmod 600`、`.gitignore` で除外
- ⚠️ refresh_token は **6ヶ月以上未使用で失効** する。失効したらステップ6を再実行

---

## 関連ガイド

- [Google OAuth セットアップ](GOOGLE_OAUTH_SETUP.md) — Gmail / Drive / Calendar の認証
- [GitHub Secrets セットアップ](GITHUB_SECRETS_SETUP.md) — CI 用シークレット管理

## 公式リソース

- [Google Ads API Documentation](https://developers.google.com/google-ads/api/docs/start)
- [API バージョン履歴](https://developers.google.com/google-ads/api/docs/release-notes)
- [google-ads-python (GitHub)](https://github.com/googleads/google-ads-python)
