#!/usr/bin/env python3
"""Google アカウント セットアップスクリプト (スタブ)

このスクリプトは未実装です。
Google Calendar/Drive OAuth 認証セットアップの手順は
.cursor/commands/utility/google-account-setup.md を参照してください。

Usage:
    python scripts/setup_google_account.py --label <アカウント名>
"""
import sys


def main():
    print("=" * 60)
    print("Google アカウント セットアップ (未実装)")
    print("=" * 60)
    print()
    print("このスクリプトはまだ実装されていません。")
    print("手動セットアップの手順:")
    print("  1. Google Cloud Console で OAuth クライアントID を作成")
    print("  2. Gmail API / Calendar API / Drive API を有効化")
    print("  3. gh secret set で GitHub Secrets に登録")
    print()
    print("詳細: .cursor/commands/utility/google-account-setup.md")
    sys.exit(1)


if __name__ == "__main__":
    main()
