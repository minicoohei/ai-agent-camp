#!/usr/bin/env python3
"""
API Setup Wizard - 各種API設定の統合ガイド

Google API / Slack / Fal.AI / Gemini などの設定を一元化し、
対話形式または自動検証で環境変数・トークンをセットアップします。

Notion は OAuth 統一（ncli login + Notion 公式 Hosted MCP）になったため
本ウィザードの対象外です。Notion のセットアップは `/setup-notion` を使ってください。

使用方法:
    uv run python tools/api_setup_wizard.py check              # 全APIの設定状況確認
    uv run python tools/api_setup_wizard.py setup google       # Google API設定
    uv run python tools/api_setup_wizard.py setup slack        # Slack API設定
    uv run python tools/api_setup_wizard.py setup fal          # Fal.AI設定
    uv run python tools/api_setup_wizard.py setup gemini       # Gemini API設定
    uv run python tools/api_setup_wizard.py guide <service>    # 設定手順ガイド表示
"""

import argparse
import getpass
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

# プロジェクトルート
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent))

from runtime_env import load_runtime_env

load_runtime_env(ROOT_DIR)

try:
    from credential_manager import store as cred_store, get as cred_get, _check_keyring
    _HAS_CREDENTIAL_MANAGER = True
except ImportError:
    try:
        from tools.credential_manager import store as cred_store, get as cred_get, _check_keyring
        _HAS_CREDENTIAL_MANAGER = True
    except ImportError:
        _HAS_CREDENTIAL_MANAGER = False

        def _check_keyring():
            return False

        def cred_store(key, value):
            return False

        def cred_get(key):
            return None


# ========== サービス定義 ==========

SERVICES = {
    "google": {
        "name": "Google API",
        "description": "Gmail, Calendar, Drive, Sheets, Slides などの Google Workspace API",
        "env_vars": [
            {"name": "GCP_SA_KEY", "required": False, "description": "サービスアカウントキー (JSON)"},
            {"name": "GOOGLE_WORKSPACE_USER", "required": False, "description": "なりすまし対象ユーザー (Workspace)"},
            {"name": "GMAIL_ACCOUNTS_CONFIG", "required": False, "description": "複数Gmailアカウント設定 (JSON)"},
        ],
        "token_files": [
            {"path": "token.json", "description": "OAuth トークン"},
        ],
        "docs_url": "https://console.cloud.google.com/apis/credentials",
    },
    "slack": {
        "name": "Slack API",
        "description": "Slack ワークスペースのメッセージ取得・送信",
        "env_vars": [
            {"name": "SLACK_USER_TOKEN", "required": False, "description": "メインワークスペース ユーザートークン"},
            # 複数ワークスペースを使う場合は以下のように追加:
            # {"name": "SLACK_USER_TOKEN_WS2", "required": False, "description": "ワークスペース2 ユーザートークン"},
        ],
        "docs_url": "https://api.slack.com/apps",
    },
    "fal": {
        "name": "Fal.AI",
        "description": "画像・動画生成AI (Flux, Fabric, LongCat 等)",
        "env_vars": [
            {"name": "FAL_KEY", "required": True, "description": "Fal.AI APIキー"},
        ],
        "docs_url": "https://fal.ai/dashboard/keys",
    },
    "gemini": {
        "name": "Google Gemini",
        "description": "Gemini Pro / Flash / Vision などの生成AI",
        "env_vars": [
            {"name": "GEMINI_API_KEY", "required": True, "description": "Gemini APIキー"},
        ],
        "docs_url": "https://aistudio.google.com/app/apikey",
    },
    "heygen": {
        "name": "HeyGen",
        "description": "AIアバター動画生成",
        "env_vars": [
            {"name": "HEYGEN_API_KEY", "required": True, "description": "HeyGen APIキー"},
        ],
        "docs_url": "https://app.heygen.com/settings/api",
    },
    "elevenlabs": {
        "name": "ElevenLabs",
        "description": "高品質TTS (Text-to-Speech)",
        "env_vars": [
            {"name": "ELEVENLABS_API_KEY", "required": True, "description": "ElevenLabs APIキー"},
        ],
        "docs_url": "https://elevenlabs.io/app/settings/api-keys",
    },
    "typefully": {
        "name": "Typefully",
        "description": "X (Twitter) 投稿管理",
        "env_vars": [
            {"name": "TYPEFULLY_API_KEY", "required": True, "description": "Typefully APIキー"},
        ],
        "docs_url": "https://typefully.com/settings/api",
    },
}


# ========== ユーティリティ関数 ==========

def check_env_var(var_name: str) -> tuple[bool, Optional[str]]:
    """環境変数の存在と値を確認（process env / Credential Store / .env）"""
    # runtime_env 経由で読み込み済みなので os.getenv で保存元を確認できる
    value = os.getenv(var_name)
    if value:
        # 機密情報はマスク
        if len(value) > 10:
            masked = value[:4] + "..." + value[-4:]
        else:
            masked = "***"
        # 保存場所を特定
        kr_val = cred_get(var_name)
        if kr_val and kr_val == value:
            source = "credential"
        else:
            source = "env"
        return True, f"{masked} ({source})"
    return False, None


def _write_updates_to_dotenv(env_updates: list[tuple[str, str]]) -> Path:
    env_path = ROOT_DIR / ".env"

    existing_lines = []
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            existing_lines = f.readlines()

    updated_vars = set()
    new_lines = []
    for line in existing_lines:
        updated = False
        for name, value in env_updates:
            if line.startswith(f"{name}="):
                new_lines.append(f'{name}="{value}"\n')
                updated_vars.add(name)
                updated = True
                break
        if not updated:
            new_lines.append(line)

    for name, value in env_updates:
        if name not in updated_vars:
            new_lines.append(f'{name}="{value}"\n')

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    os.chmod(env_path, 0o600)
    return env_path


def check_token_file(path: str) -> tuple[bool, Optional[str]]:
    """トークンファイルの存在を確認"""
    full_path = ROOT_DIR / path
    if full_path.exists():
        try:
            with open(full_path, encoding="utf-8") as f:
                data = json.load(f)
            # トークン有効期限などの情報を取得
            expiry = data.get("expiry", "N/A")
            return True, f"expires: {expiry}"
        except Exception:
            return True, "exists (parse error)"
    return False, None


def validate_google_credentials() -> Dict[str, Any]:
    """Google API認証情報の詳細検証"""
    result = {
        "service_account": False,
        "oauth": False,
        "multi_gmail": False,
        "details": []
    }
    
    # サービスアカウント
    sa_key = os.getenv("GCP_SA_KEY")
    if sa_key:
        try:
            if not sa_key.strip().startswith("{"):
                import base64
                sa_key = base64.b64decode(sa_key).decode("utf-8")
            data = json.loads(sa_key)
            if "project_id" in data:
                result["service_account"] = True
                result["details"].append(f"Service Account: {data.get('client_email', 'N/A')}")
        except Exception as e:
            result["details"].append(f"Service Account: Parse error - {e}")
    
    # OAuthトークン
    token_path = ROOT_DIR / "token.json"
    if token_path.exists():
        try:
            with open(token_path, encoding="utf-8") as f:
                data = json.load(f)
            result["oauth"] = True
            result["details"].append(f"OAuth Token: expires {data.get('expiry', 'N/A')}")
        except Exception:
            result["details"].append("OAuth Token: exists but invalid")
    
    # 複数Gmailアカウント設定
    config = os.getenv("GMAIL_ACCOUNTS_CONFIG")
    if config:
        try:
            data = json.loads(config)
            accounts = data.get("accounts", [])
            result["multi_gmail"] = len(accounts) > 0
            result["details"].append(f"Multi Gmail: {len(accounts)} accounts configured")
        except Exception:
            result["details"].append("Multi Gmail: config parse error")
    
    return result


def validate_fal_api() -> Dict[str, Any]:
    """Fal.AI API検証"""
    result = {"valid": False, "details": []}
    
    api_key = os.getenv("FAL_KEY")
    if not api_key:
        result["details"].append("FAL_KEY not set")
        return result
    
    # Fal.AIは認証チェック専用APIがないため、キーの形式のみ確認
    if api_key.startswith("fal_") or len(api_key) > 20:
        result["valid"] = True
        result["details"].append("API key format looks valid")
    else:
        result["details"].append("API key format may be invalid")
    
    return result


def validate_gemini_api() -> Dict[str, Any]:
    """Gemini API検証"""
    result = {"valid": False, "details": []}
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        result["details"].append("GEMINI_API_KEY not set")
        return result
    
    try:
        import requests
        resp = requests.get(
            "https://generativelanguage.googleapis.com/v1/models",
            headers={"x-goog-api-key": api_key},
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            models = [m.get("name", "").split("/")[-1] for m in data.get("models", [])[:5]]
            result["valid"] = True
            result["details"].append(f"Available models: {', '.join(models)}...")
        else:
            result["details"].append(f"API error: {resp.status_code}")
    except ImportError:
        result["details"].append("requests not installed - cannot validate")
    except Exception as e:
        result["details"].append(f"Validation error: {e}")
    
    return result


# ========== コマンド実装 ==========

def cmd_check(args):
    """全APIの設定状況を確認"""
    print("=" * 60)
    print("🔍 API 設定状況チェック")
    print(f"   実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if _check_keyring():
        print("   🔐 Credential Store: 有効")
    else:
        print("   ⚠️ Credential Store: 無効 (pip install keyring)")
    env_path = ROOT_DIR / ".env"
    if env_path.exists():
        print(f"   ⚠️ .env ファイルが存在しています（平文）")
    print("=" * 60)
    
    for service_id, service in SERVICES.items():
        print(f"\n📦 {service['name']}")
        print(f"   {service['description']}")
        print("-" * 50)
        
        all_ok = True
        
        for env_var in service.get("env_vars", []):
            exists, masked = check_env_var(env_var["name"])
            status = "✅" if exists else ("⚠️" if not env_var["required"] else "❌")
            if not exists and env_var["required"]:
                all_ok = False
            
            value_str = f" = {masked}" if exists else ""
            required_str = " (required)" if env_var["required"] else ""
            print(f"   {status} {env_var['name']}{value_str}{required_str}")
            print(f"      └ {env_var['description']}")
        
        for token_file in service.get("token_files", []):
            exists, info = check_token_file(token_file["path"])
            status = "✅" if exists else "⚠️"
            info_str = f" ({info})" if info else ""
            print(f"   {status} {token_file['path']}{info_str}")
            print(f"      └ {token_file['description']}")
        
        # 詳細検証
        if service_id == "google":
            validation = validate_google_credentials()
            for detail in validation.get("details", []):
                print(f"   ℹ️  {detail}")
        elif service_id == "gemini":
            validation = validate_gemini_api()
            for detail in validation.get("details", []):
                print(f"   ℹ️  {detail}")
        elif service_id == "fal":
            validation = validate_fal_api()
            for detail in validation.get("details", []):
                print(f"   ℹ️  {detail}")
    
    print("\n" + "=" * 60)
    print("💡 設定ガイドを表示するには:")
    print("   uv run python tools/api_setup_wizard.py guide <service>")
    print("   例: uv run python tools/api_setup_wizard.py guide google")
    print("=" * 60)


def cmd_guide(args):
    """設定手順ガイドを表示"""
    service_id = args.service.lower()
    
    if service_id not in SERVICES:
        print(f"❌ Unknown service: {service_id}")
        print(f"Available services: {', '.join(SERVICES.keys())}")
        return
    
    service = SERVICES[service_id]
    
    print("=" * 60)
    print(f"📖 {service['name']} 設定ガイド")
    print("=" * 60)
    
    # サービス別の詳細ガイド
    guides = {
        "google": """
## 1. Google Cloud Console でプロジェクトを作成

1. https://console.cloud.google.com/ にアクセス
2. 新しいプロジェクトを作成、または既存プロジェクトを選択
3. APIとサービス > ライブラリ から必要なAPIを有効化:
   - Gmail API
   - Google Calendar API
   - Google Drive API
   - Google Sheets API
   - Google Slides API

## 2. OAuth 同意画面を設定

1. APIとサービス > OAuth 同意画面
2. ユーザータイプ: 「外部」を選択
3. アプリ名、メールアドレスを入力
4. スコープを追加（Gmail, Calendar, Drive 等）
5. テストユーザーに自分のメールアドレスを追加

## 3. 認証情報を作成

### OAuth クライアント ID (個人Gmail用)
1. APIとサービス > 認証情報 > 認証情報を作成
2. OAuth クライアント ID を選択
3. アプリケーションの種類: デスクトップアプリ
4. JSONをダウンロード → credentials.json として保存

### サービスアカウント (Google Workspace用)
1. APIとサービス > 認証情報 > 認証情報を作成
2. サービスアカウント を選択
3. キー > 鍵を追加 > JSON
4. JSONの内容を GCP_SA_KEY 環境変数に設定

## 4. トークン取得

```bash
uv run python tools/google_api_setup.py auth \\
    --credentials credentials.json \\
    --scopes gmail,calendar,drive
```

## 環境変数

```bash
# Credential Store に保存（別ターミナルで実行）
# uv run python tools/credential_manager.py store
GCP_SA_KEY='{"type":"service_account",...}'  # Workspace用
GOOGLE_WORKSPACE_USER="user@company.com"     # なりすまし対象

# 複数Gmailアカウント
GMAIL_ACCOUNTS_CONFIG='{"accounts":[...]}'
```
""",
        "slack": """
## 1. Slack App を作成

1. https://api.slack.com/apps にアクセス
2. 「Create New App」> 「From scratch」
3. アプリ名とワークスペースを選択

## 2. OAuth スコープを設定

1. 「OAuth & Permissions」に移動
2. 「User Token Scopes」に以下を追加:
   - channels:history
   - channels:read
   - groups:history
   - groups:read
   - im:history
   - im:read
   - mpim:history
   - mpim:read
   - users:read

## 3. アプリをインストール

1. 「Install to Workspace」をクリック
2. 権限を確認して「許可する」
3. 「User OAuth Token」をコピー（xoxp-で始まる）

## 環境変数

```bash
# Credential Store に保存（別ターミナルで実行）
# uv run python tools/credential_manager.py store（ワークスペースごと）
SLACK_USER_TOKEN="xoxp-xxxxx"           # メインワークスペース
# 複数ワークスペースを使う場合は以下のように追加:
# SLACK_USER_TOKEN_WS2="xoxp-xxxxx"    # ワークスペース2
```
""",
        "fal": """
## 1. Fal.AI アカウント作成

1. https://fal.ai/ にアクセス
2. サインアップ（GitHub連携推奨）

## 2. APIキーを取得

1. https://fal.ai/dashboard/keys にアクセス
2. 「Create API Key」をクリック
3. キーをコピー

## 環境変数

```bash
# Credential Store に保存（別ターミナルで実行）
# uv run python tools/credential_manager.py store
FAL_KEY="fal_xxxxxxxxxxxxx"
```

## 利用可能なモデル

- flux-pro: 高品質画像生成
- fabric-1.0: AI動画生成
- longcat: 長尺動画生成
""",
        "gemini": """
## 1. Google AI Studio でAPIキーを取得

1. https://aistudio.google.com/app/apikey にアクセス
2. Googleアカウントでログイン
3. 「Create API key」をクリック
4. プロジェクトを選択または新規作成
5. APIキーをコピー

## 環境変数

```bash
# Credential Store に保存（別ターミナルで実行）
# uv run python tools/credential_manager.py store
GEMINI_API_KEY="AIzaSy..."
```

## 利用可能なモデル

- gemini-3-flash-preview: 高速・高性能（推奨）
- gemini-3-pro-preview: 高品質・長文対応
""",
        "heygen": """
## 1. HeyGen アカウント作成

1. https://app.heygen.com/ にアクセス
2. サインアップ

## 2. APIキーを取得

1. https://app.heygen.com/settings/api にアクセス
2. 「Generate API Key」をクリック
3. キーをコピー

## 環境変数

```bash
# Credential Store に保存（別ターミナルで実行）
# uv run python tools/credential_manager.py store
HEYGEN_API_KEY="xxxxxxxx"
```
""",
        "elevenlabs": """
## 1. ElevenLabs アカウント作成

1. https://elevenlabs.io/ にアクセス
2. サインアップ

## 2. APIキーを取得

1. https://elevenlabs.io/app/settings/api-keys にアクセス
2. 「Create API Key」をクリック
3. キーをコピー

## 環境変数

```bash
# Credential Store に保存（別ターミナルで実行）
# uv run python tools/credential_manager.py store
ELEVENLABS_API_KEY="sk_..."
```
""",
        "typefully": """
## 1. Typefully アカウント作成

1. https://typefully.com/ にアクセス
2. サインアップ（Twitter/X連携）

## 2. APIキーを取得

1. https://typefully.com/settings/api にアクセス
2. 「Generate API Key」をクリック
3. キーをコピー

## 環境変数

```bash
# Credential Store に保存（別ターミナルで実行）
# uv run python tools/credential_manager.py store
TYPEFULLY_API_KEY="tf_..."
```
""",
    }
    
    guide_text = guides.get(service_id, "詳細ガイドは準備中です。")
    print(guide_text)
    
    print("-" * 60)
    print(f"📎 公式ドキュメント: {service['docs_url']}")
    print("=" * 60)


def cmd_setup(args):
    """対話形式でサービスをセットアップ"""
    service_id = args.service.lower()
    
    if service_id not in SERVICES:
        print(f"❌ Unknown service: {service_id}")
        print(f"Available services: {', '.join(SERVICES.keys())}")
        return
    
    service = SERVICES[service_id]
    
    print("=" * 60)
    print(f"🔧 {service['name']} セットアップ")
    print("=" * 60)
    
    # まずガイドを表示
    cmd_guide(args)
    
    print("\n" + "=" * 60)
    print("🔐 APIキーの保存")
    print("=" * 60)

    use_keyring = args.storage == "credential-store"
    if use_keyring and not _check_keyring():
        print("❌ OS Credential Store が利用できません。")
        print("   標準手順は Credential Store です。")
        print("   keyring backend を有効にするか、必要なら以下を明示してください:")
        print(f"   uv run python tools/api_setup_wizard.py setup {service_id} --storage dotenv")
        return

    if use_keyring:
        print("保存先: OS Credential Store (暗号化)")
    else:
        print("⚠️ 保存先: .env ファイル（明示フォールバック）")
        print("   標準手順は Credential Store です。平文保存になる点に注意してください。")

    env_updates = []

    for env_var in service.get("env_vars", []):
        exists, masked = check_env_var(env_var["name"])

        if exists:
            print(f"\n✅ {env_var['name']} = {masked}")
            update = input("   更新しますか? [y/N]: ").strip().lower()
            if update != "y":
                continue
        else:
            print(f"\n❌ {env_var['name']} (未設定)")

        print(f"   説明: {env_var['description']}")
        # getpass で非表示入力（APIキーが画面に表示されない）
        value = getpass.getpass(f"   値を入力（非表示）: ").strip()

        if value:
            env_updates.append((env_var["name"], value))

    if env_updates:
        print("\n" + "-" * 60)
        if use_keyring:
            print("以下のキーを OS Credential Store に保存します:")
        else:
            print("以下の環境変数を .env に追加/更新します:")
        for name, value in env_updates:
            masked = value[:4] + "..." + value[-4:] if len(value) > 10 else "***"
            print(f"   {name} = {masked}")

        confirm = input("\n実行しますか? [y/N]: ").strip().lower()
        if confirm == "y":
            if use_keyring:
                failed = []
                for name, value in env_updates:
                    try:
                        if cred_store(name, value):
                            os.environ[name] = value
                        else:
                            failed.append((name, "保存に失敗しました"))
                    except Exception as e:
                        failed.append((name, str(e)))
                if failed:
                    print(f"\n⚠️  一部の保存に失敗しました:")
                    for name, err in failed:
                        print(f"  - {name}: {err}")
                    print("   keyring backend を確認するか、必要なら --storage dotenv を使用してください。")
                else:
                    print("\n✅ Credential Store に保存しました")
            else:
                env_path = _write_updates_to_dotenv(env_updates)
                print(f"\n⚠️ .env に保存しました: {env_path}")
                print("   標準運用に戻す場合は Credential Store へ移行してください。")
        else:
            print("\n⏭️ スキップしました")

    print("\n🎉 セットアップ完了！")
    print("   設定確認: uv run python tools/api_setup_wizard.py check")


def main():
    parser = argparse.ArgumentParser(
        description="API Setup Wizard - 各種API設定の統合ガイド"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # check コマンド
    check_parser = subparsers.add_parser("check", help="全APIの設定状況を確認")
    
    # setup コマンド
    setup_parser = subparsers.add_parser("setup", help="対話形式でサービスをセットアップ")
    setup_parser.add_argument("service", help="サービス名 (google, slack, fal, gemini, heygen, elevenlabs, typefully)")
    setup_parser.add_argument(
        "--storage",
        choices=["credential-store", "dotenv"],
        default="credential-store",
        help="保存先（デフォルト: credential-store）",
    )
    
    # guide コマンド
    guide_parser = subparsers.add_parser("guide", help="設定手順ガイドを表示")
    guide_parser.add_argument("service", help="サービス名 (google, slack, fal, gemini, heygen, elevenlabs, typefully)")
    
    args = parser.parse_args()
    
    if not args.command:
        # デフォルトはcheck
        args.command = "check"
        cmd_check(args)
    elif args.command == "check":
        cmd_check(args)
    elif args.command == "setup":
        cmd_setup(args)
    elif args.command == "guide":
        cmd_guide(args)


if __name__ == "__main__":
    main()
