#!/usr/bin/env python3
"""
Slack OAuth Token 取得スクリプト（複数ワークスペース対応）

使い方:
1. 認証URLを生成（TokenPocket）:
   python get_token.py --generate-url

2. 認証URLを生成（Infobox）:
   python get_token.py --generate-url --workspace infobox

3. Tokenを取得:
   python get_token.py --code=コピーしたコード
   python get_token.py --code=コピーしたコード --workspace infobox
"""

import argparse
import os
import sys
import urllib.parse
from pathlib import Path

import requests
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR.parent / ".env")

# ワークスペース設定
WORKSPACES = {
    "tokenpocket": {
        "client_id_env": "SLACK_CLIENT_ID",
        "client_secret_env": "SLACK_CLIENT_SECRET",
        "token_env": "SLACK_USER_TOKEN",
        "display_name": "TokenPocket",
    },
    "infobox": {
        "client_id_env": "SLACK_CLIENT_ID_INFOBOX",
        "client_secret_env": "SLACK_CLIENT_SECRET_INFOBOX",
        "token_env": "SLACK_USER_TOKEN_INFOBOX",
        "display_name": "Infobox",
    },
    "yoake": {
        "client_id_env": "SLACK_CLIENT_ID_YOAKE",
        "client_secret_env": "SLACK_CLIENT_SECRET_YOAKE",
        "token_env": "SLACK_USER_TOKEN_YOAKE",
        "display_name": "YOAKE",
    },
    "fungiblex": {
        "client_id_env": "SLACK_CLIENT_ID_FUNGIBLEX",
        "client_secret_env": "SLACK_CLIENT_SECRET_FUNGIBLEX",
        "token_env": "SLACK_USER_TOKEN_FUNGIBLEX",
        "display_name": "Fungible X",
    },
}

REDIRECT_URI = os.getenv("SLACK_REDIRECT_URI", "https://example.com/callback")


def _mask_token(token: str) -> str:
    """トークンをマスク表示(先頭4文字 + ... + 末尾4文字)"""
    if len(token) > 12:
        return token[:4] + "..." + token[-4:]
    return "****"

# 必要なスコープ
SCOPES = [
    "channels:history",    # パブリックチャンネルの履歴
    "channels:read",       # パブリックチャンネル一覧
    "groups:history",      # プライベートチャンネルの履歴
    "groups:read",         # プライベートチャンネル一覧
    "users:read",          # ユーザー情報（名前解決用）
    "im:history",          # DM履歴（オプション）
    "mpim:history",        # グループDM履歴（オプション）
]


def get_workspace_config(workspace: str) -> dict:
    """ワークスペース設定を取得"""
    if workspace not in WORKSPACES:
        print(f"❌ エラー: 不明なワークスペース '{workspace}'")
        print(f"利用可能: {', '.join(WORKSPACES.keys())}")
        sys.exit(1)
    return WORKSPACES[workspace]


def generate_auth_url(client_id: str) -> str:
    """OAuth認証URLを生成"""
    base_url = "https://slack.com/oauth/v2/authorize"
    params = {
        "client_id": client_id,
        "user_scope": ",".join(SCOPES),
        "redirect_uri": REDIRECT_URI,
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"


def exchange_code_for_token(client_id: str, client_secret: str, code: str) -> dict:
    """認証コードをTokenに交換"""
    url = "https://slack.com/api/oauth.v2.access"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    
    response = requests.post(url, data=data)
    return response.json()


def main():
    parser = argparse.ArgumentParser(
        description="Slack OAuth Token取得ツール（複数ワークスペース対応）"
    )
    parser.add_argument(
        "--workspace", "-w",
        type=str,
        default="tokenpocket",
        choices=list(WORKSPACES.keys()),
        help="対象ワークスペース（デフォルト: tokenpocket）"
    )
    parser.add_argument(
        "--generate-url",
        action="store_true",
        help="認証URLを生成して表示"
    )
    parser.add_argument(
        "--code",
        type=str,
        help="認証後に取得したcodeパラメータ"
    )
    
    args = parser.parse_args()
    
    # ワークスペース設定を取得
    ws_config = get_workspace_config(args.workspace)
    display_name = ws_config["display_name"]
    client_id = os.getenv(ws_config["client_id_env"])
    client_secret = os.getenv(ws_config["client_secret_env"])
    token_env = ws_config["token_env"]
    
    if args.generate_url:
        if not client_id:
            print(f"❌ エラー: {ws_config['client_id_env']} が設定されていません")
            print()
            print("以下のいずれかの方法で設定してください:")
            print(f"1. 環境変数: export {ws_config['client_id_env']}=xxx")
            print(f"2. .envファイル: {ws_config['client_id_env']}=xxx")
            sys.exit(1)
        
        auth_url = generate_auth_url(client_id)
        print("=" * 60)
        print(f"🏢 ワークスペース: {display_name}")
        print("=" * 60)
        print()
        print("📋 以下のURLをブラウザで開いてください:")
        print()
        print(auth_url)
        print()
        print("=" * 60)
        print("📌 手順:")
        print("1. 上のURLをブラウザで開く")
        print("2. Slackで「許可する」をクリック")
        print("3. リダイレクト先のURL（エラーページでOK）から")
        print("   アドレスバーの code=xxxxx の部分をコピー")
        print("4. 以下のコマンドを実行:")
        print(f"   python {sys.argv[0]} --workspace {args.workspace} --code=コピーしたコード")
        print("=" * 60)
        
    elif args.code:
        if not client_id or not client_secret:
            missing = []
            if not client_id:
                missing.append(ws_config['client_id_env'])
            if not client_secret:
                missing.append(ws_config['client_secret_env'])
            print(f"❌ エラー: {', '.join(missing)} が設定されていません")
            sys.exit(1)
        
        print(f"🏢 ワークスペース: {display_name}")
        print("🔄 Tokenを取得中...")
        result = exchange_code_for_token(client_id, client_secret, args.code)
        
        if result.get("ok"):
            user_token = result.get("authed_user", {}).get("access_token")
            if user_token:
                print()
                print("=" * 60)
                print("✅ Token取得成功!")
                print("=" * 60)
                print()
                masked = _mask_token(user_token)
                print(f"🔑 User Token: {masked}")
                print()
                print("=" * 60)
                print("📌 次のステップ:")
                print("1. 以下のコマンドで Credential Store に保存:")
                print(f"   uv run python tools/credential_manager.py store {token_env}")
                print()
                print("2. GitHub Secretsにも登録:")
                print(f"   Name: {token_env}")
                print("   Secret: (上記コマンド実行時に入力したトークン)")
                print("=" * 60)
            else:
                print("❌ User Tokenが見つかりません")
                print("レスポンス:", result)
        else:
            print("❌ エラー:", result.get("error", "Unknown error"))
            if result.get("error") == "invalid_code":
                print("💡 ヒント: codeは一度しか使えません。再度認証URLから取得してください。")
            elif result.get("error") == "code_already_used":
                print("💡 ヒント: このcodeは既に使用済みです。再度認証URLから取得してください。")
    else:
        parser.print_help()
        print()
        print("=" * 60)
        print("📋 ワークスペース一覧:")
        for ws_name, ws_info in WORKSPACES.items():
            token = os.getenv(ws_info["token_env"])
            status = "✅ 設定済み" if token else "❌ 未設定"
            print(f"  - {ws_name}: {ws_info['display_name']} [{status}]")
        print("=" * 60)


if __name__ == "__main__":
    main()
