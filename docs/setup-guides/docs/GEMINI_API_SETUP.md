# Gemini API セットアップガイド

Gemini APIは、画像生成、テキスト分析、マルチモーダル処理など、多くのスキルで使用される必須のAPIです。

---

## 概要

| 項目 | 内容 |
|------|------|
| API名 | Gemini API (Google AI Studio) |
| 用途 | 画像生成、テキスト生成、分析 |
| 無料枠 | 60 RPM / 1500 RPD |
| 料金 | 従量課金（有料プラン） |
| 必要時間 | 約10分 |

---

## ステップ1: Google AI Studio にアクセス

1. [Google AI Studio](https://aistudio.google.com/) にアクセス
2. Googleアカウントでログイン

> **注意**: 組織のGoogle Workspaceアカウントでは利用できない場合があります。
> その場合は個人のGoogleアカウントを使用してください。

---

## ステップ2: APIキーの作成

1. 左メニューの「**Get API Key**」をクリック
2. 「**Create API key**」をクリック
3. プロジェクトを選択（または新規作成）
4. 生成されたAPIキーをコピー

```
例: AIzaSy...（約40文字）
```

> **重要**: APIキーは一度しか表示されません。必ずコピーして安全な場所に保存してください。

---

## ステップ3: 環境変数の設定

### 方法1: Credential Store（推奨）

OSの暗号化ストレージ（macOS Keychain / Windows Credential Locker / Linux SecretService）に安全に保存します。

```bash
# keyring パッケージのインストール（初回のみ）
uv add keyring

# APIキーを保存（入力は画面に表示されません）
uv run python tools/credential_manager.py store GEMINI_API_KEY
```

> **なぜ推奨？** `.env` ファイルは平文でディスクに保存されるため、誤ってコミットしたり他のプロセスから読み取られるリスクがあります。Credential Store はOSレベルで暗号化され、画面ロック時にはアクセスできなくなります。

### 方法2: .env ファイル（フォールバック）

Credential Store が使えない環境（Docker/CI等）では `.env` を使用できます。

```bash
# .env
GEMINI_API_KEY=AIzaSy...your_api_key_here
```

または `GOOGLE_API_KEY` でも動作します：

```bash
# .env
GOOGLE_API_KEY=AIzaSy...your_api_key_here
```

> **注意**: `.env` ファイルは `.gitignore` に含まれていることを必ず確認してください。

### 方法3: シェル環境変数

```bash
# bash / zsh
export GEMINI_API_KEY=AIzaSy...your_api_key_here

# 永続化する場合は ~/.zshrc または ~/.bashrc に追加
echo 'export GEMINI_API_KEY=AIzaSy...' >> ~/.zshrc
source ~/.zshrc
```

### 方法4: GitHub Secrets（CI/CD用）

1. GitHubリポジトリの Settings > Secrets and variables > Actions
2. 「New repository secret」をクリック
3. Name: `GEMINI_API_KEY`
4. Value: APIキーを貼り付け

---

## ステップ4: 動作確認

### Pythonで確認

```python
import os
from google import genai

# APIキーの確認
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
print(f"API Key found: {api_key[:10]}..." if api_key else "API Key not found")

# クライアント作成
client = genai.Client(api_key=api_key)

# テスト生成
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Hello, Gemini!"
)
print(response.text)
```

### コマンドラインで確認

```bash
# 環境変数の確認
echo $GEMINI_API_KEY

# curlでテスト
curl "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY"
```

---

## 利用可能なモデル

| モデル | 用途 | 特徴 |
|--------|------|------|
| `gemini-2.0-flash` | 汎用・高速 | 最もバランスの良いモデル |
| `gemini-2.0-flash-thinking` | 推論・分析 | 思考プロセスを含む |
| `gemini-pro-vision` | 画像分析 | 画像入力対応 |
| `imagen-3.0-generate-002` | 画像生成 | テキストから画像生成 |

---

## 料金と制限

### 無料枠（Free Tier）

| 制限 | 値 |
|------|-----|
| RPM（リクエスト/分） | 60 |
| RPD（リクエスト/日） | 1,500 |
| TPM（トークン/分） | 1,000,000 |

### 有料プラン

- 入力: $0.075 / 100万トークン
- 出力: $0.30 / 100万トークン
- 画像生成: $0.02 / 画像

> 最新の料金は [Google AI Pricing](https://ai.google.dev/pricing) を確認してください。

---

## トラブルシューティング

### APIキーが認識されない

```
Error: GEMINI_API_KEY not found
```

**解決策**:
1. `.env` ファイルの存在を確認
2. `python-dotenv` をインストール
   ```bash
   uv add python-dotenv
   ```
3. コードで明示的に読み込み
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

### Rate Limit エラー

```
429 Resource has been exhausted
```

**解決策**:
1. リクエスト間に待機時間を追加
2. 有料プランへのアップグレードを検討
3. バッチ処理でリクエスト数を削減

### 権限エラー

```
403 Permission denied
```

**解決策**:
1. APIキーが正しいか確認
2. Google AI Studio でAPIが有効化されているか確認
3. 組織の制限がないか確認

---

## 使用するスキル

以下のスキルでGemini APIを使用します：

- `banner-creator` - バナー画像生成
- `nanobanana` - 汎用画像生成/編集
- `diagram-generator` - 図解生成
- `screenshot-analyzer` - スクリーンショット分析
- `tutorial-generator` - チュートリアル生成
- `storyboard-generator` - 絵コンテ生成
- `video-frame-reader` - 動画フレーム分析
- `check-inbox` - メール/Slack分析
- `data-analyst` - データ分析（一部）

---

## 次のステップ

- [SLACK_TOKEN_SETUP.md](./SLACK_TOKEN_SETUP.md) - Slack API設定
- [GOOGLE_OAUTH_SETUP.md](./GOOGLE_OAUTH_SETUP.md) - Google OAuth設定
- [コースサイト](https://ai-agent.camp/ja/course/module-0) - 学習を開始
