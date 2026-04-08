#!/usr/bin/env python3
"""
Google API Setup Tool for MCP

OAuth 2.0認証フローを実行し、トークンを生成するツール。
MCPサーバー用のGoogle API認証設定をサポートします。

使用方法:
    python google_api_setup.py auth --credentials path/to/credentials.json --scopes gmail,calendar
    python google_api_setup.py validate --credentials path/to/credentials.json
    python google_api_setup.py refresh --token path/to/token.json --credentials path/to/credentials.json
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Google Auth関連のインポート（インストールチェック付き）
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
except ImportError:
    print("Error: Google Auth libraries not found.")
    print("Please install with: pip install google-auth google-auth-oauthlib google-auth-httplib2")
    sys.exit(1)


# スコープ定義
SCOPES = {
    "gmail": [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.modify",
    ],
    "calendar": [
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/calendar.events",
    ],
    "drive": [
        "https://www.googleapis.com/auth/drive",
    ],
    "sheets": [
        "https://www.googleapis.com/auth/spreadsheets",
    ],
}


def validate_credentials(credentials_path: str) -> dict:
    """クレデンシャルJSONファイルを検証します。"""
    path = Path(credentials_path).expanduser()
    
    if not path.exists():
        raise FileNotFoundError(f"Credentials file not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if "installed" in data:
        client_config = data["installed"]
    elif "web" in data:
        client_config = data["web"]
    else:
        raise ValueError("Invalid credentials format. Expected 'installed' or 'web' key.")
    
    required_fields = ["client_id", "client_secret", "auth_uri", "token_uri"]
    missing_fields = [f for f in required_fields if f not in client_config]
    
    if missing_fields:
        raise ValueError(f"Missing required fields: {missing_fields}")
    
    print(f"✅ Credentials validated successfully")
    print(f"   Client ID: {client_config['client_id'][:20]}...")
    print(f"   Type: {'Desktop App' if 'installed' in data else 'Web App'}")
    
    return data


def run_oauth_flow(credentials_path: str, scopes: list, output_dir: str = ".") -> str:
    """OAuth 2.0認証フローを実行し、トークンを保存します。"""
    credentials_path = Path(credentials_path).expanduser()
    output_dir = Path(output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    token_path = output_dir / "token.json"
    creds = None
    
    if token_path.exists():
        print(f"📄 Found existing token: {token_path}")
        creds = Credentials.from_authorized_user_file(str(token_path), scopes)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("🔐 Starting OAuth flow...")
            print("   A browser window will open for authentication.")
            print("")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), scopes
            )
            creds = flow.run_local_server(port=0)
        
        with open(token_path, "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())
        
        print(f"✅ Token saved to: {token_path}")
    else:
        print(f"✅ Token is valid: {token_path}")
    
    return str(token_path)


def generate_mcp_config(token_path: str, scopes: list, output_dir: str = ".") -> str:
    """MCP設定ファイルの例を生成します。"""
    output_dir = Path(output_dir).expanduser()
    config_path = output_dir / "mcp_config.json"
    
    apis_used = []
    for api_name, api_scopes in SCOPES.items():
        if any(s in scopes for s in api_scopes):
            apis_used.append(api_name)
    
    config = {
        "_comment": "MCP設定ファイルの例 - 各MCPサーバーに合わせて編集してください",
        "generated_at": datetime.now().isoformat(),
        "token_path": str(Path(token_path).absolute()),
        "apis_enabled": apis_used,
        "scopes": scopes,
        "example_mcp_config": {
            "mcpServers": {
                "google": {
                    "command": "npx",
                    "args": ["-y", "@anthropic/mcp-google"],
                    "env": {
                        "GOOGLE_TOKEN_PATH": str(Path(token_path).absolute())
                    }
                }
            }
        }
    }
    
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"📝 MCP config example saved to: {config_path}")
    return str(config_path)


def parse_scopes(scope_str: str) -> list:
    """スコープ文字列を解析してスコープリストを返します。"""
    scopes = []
    scope_names = [s.strip().lower() for s in scope_str.split(",")]
    
    for name in scope_names:
        if name in SCOPES:
            scopes.extend(SCOPES[name])
        elif name.startswith("https://"):
            scopes.append(name)
        else:
            print(f"⚠️ Unknown scope: {name}")
    
    return list(set(scopes))


def refresh_token(token_path: str, credentials_path: str, scopes_override: str = None) -> str:
    """token.json をリフレッシュして上書き保存します。"""
    token_file = Path(token_path).expanduser()
    if not token_file.exists():
        raise FileNotFoundError(f"Token file not found: {token_file}")

    with open(token_file, "r", encoding="utf-8") as f:
        token_data = json.load(f)

    if scopes_override:
        scopes = parse_scopes(scopes_override)
        if not scopes:
            raise ValueError("No valid scopes specified for refresh (--scopes).")
    else:
        scopes = token_data.get("scopes")
        if not scopes:
            raise ValueError(
                "Token file does not include scopes. Provide --scopes (e.g. gmail,calendar)."
            )

    # token.json が最低限の情報しか持っていないケースに備え、credentials.json から補完
    # - client_id / client_secret / token_uri が欠けていると refresh に失敗することがある
    if any(k not in token_data for k in ("client_id", "client_secret", "token_uri")):
        creds_json = validate_credentials(credentials_path)
        client_config = creds_json.get("installed") or creds_json.get("web") or {}
        if client_config:
            token_data.setdefault("client_id", client_config.get("client_id"))
            token_data.setdefault("client_secret", client_config.get("client_secret"))
            token_data.setdefault("token_uri", client_config.get("token_uri"))

    creds = Credentials.from_authorized_user_info(token_data, scopes=scopes)
    if not creds.refresh_token:
        raise ValueError(
            "refresh_token not found in token.json. Re-run auth flow to generate a refresh token."
        )

    print("🔄 Refreshing token...")
    creds.refresh(Request())

    with open(token_file, "w", encoding="utf-8") as f:
        f.write(creds.to_json())

    print(f"✅ Token refreshed and saved to: {token_file}")
    return str(token_file)


def main():
    parser = argparse.ArgumentParser(description="Google API Setup Tool for MCP")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # auth コマンド
    auth_parser = subparsers.add_parser("auth", help="Run OAuth authentication flow")
    auth_parser.add_argument("--credentials", "-c", required=True)
    auth_parser.add_argument("--scopes", "-s", required=True)
    auth_parser.add_argument("--output", "-o", default=".")
    
    # validate コマンド
    validate_parser = subparsers.add_parser("validate", help="Validate credentials")
    validate_parser.add_argument("--credentials", "-c", required=True)
    
    # refresh コマンド
    refresh_parser = subparsers.add_parser("refresh", help="Refresh token")
    refresh_parser.add_argument("--token", "-t", required=True)
    refresh_parser.add_argument("--credentials", "-c", required=True)
    refresh_parser.add_argument(
        "--scopes",
        "-s",
        required=False,
        help="Optional scopes (e.g. 'gmail,calendar'). If omitted, uses scopes embedded in token.json.",
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == "validate":
            validate_credentials(args.credentials)
            
        elif args.command == "auth":
            validate_credentials(args.credentials)
            scopes = parse_scopes(args.scopes)
            if not scopes:
                print("❌ No valid scopes specified")
                sys.exit(1)
            
            print(f"\n📋 Requested scopes:")
            for scope in scopes:
                print(f"   - {scope}")
            print("")
            
            token_path = run_oauth_flow(args.credentials, scopes, args.output)
            generate_mcp_config(token_path, scopes, args.output)
            
            print("\n🎉 Setup completed successfully!")
            
        elif args.command == "refresh":
            validate_credentials(args.credentials)
            refresh_token(
                args.token,
                args.credentials,
                scopes_override=getattr(args, "scopes", None),
            )
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()