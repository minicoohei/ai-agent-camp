#!/usr/bin/env python3
"""Firebase 連携オンボーディングスクリプト。

Coding Agent（Claude Code CLI）から実行し、以下のフローを自動化する:
1. Firebase ブラウザ認証（Google OAuth → localhost コールバック）
2. GitHub アカウント確認 / 作成案内
3. Cloud Function 呼び出し（Firebase ↔ GitHub 連携 + コラボレーター招待）
4. 招待受諾
5. コンテンツリポジトリのセットアップ + 教材更新

使い方:
    uv run python tools/firebase_onboarding.py onboard          # フルフロー
    uv run python tools/firebase_onboarding.py status           # 状態確認
    uv run python tools/firebase_onboarding.py link-github      # GitHub 連携のみ

前提:
    - Firebase Hosting に auth.html がデプロイ済み
    - Cloud Function (grant-access) がデプロイ済み
"""

import argparse
import http.server
import json
import os
import re
import secrets
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from log_utils import setup_logger

logger = setup_logger("firebase_onboarding")

# --- 定数 ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = PROJECT_ROOT / "work" / ".onboarding-state.json"

DEFAULT_HOSTING_URL = os.getenv(
    "AIAGENT_ONBOARDING_HOSTING_URL",
    "https://ai-tutor-dev-9c015.web.app",
)
# Cloud Function URL はデプロイ後に確定（リージョンはデプロイ設定に依存）
DEFAULT_CLOUD_FUNCTION_URL = os.getenv(
    "AIAGENT_ONBOARDING_FUNCTION_URL",
    "https://asia-northeast1-ai-tutor-dev-9c015.cloudfunctions.net/grant-access",
)
DEFAULT_CONTENT_REPO = os.getenv(
    "AIAGENT_CONTENT_REPO",
    "TokenPocket/ai-agent-camp",
)

JWT_PATTERN = re.compile(r"^[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+$")

INVITATION_POLL_INTERVAL = 3  # 秒
INVITATION_POLL_TIMEOUT = 90  # 秒


# --- ユーティリティ ---


def _find_free_port() -> int:
    """空きポートを取得。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def load_state() -> dict:
    """オンボーディング状態を読み込み。"""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_state(state: dict) -> None:
    """オンボーディング状態を保存。"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    STATE_FILE.write_text(
        json.dumps(state, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def mark_step_completed(step: str) -> None:
    """ステップを完了としてマーク。"""
    state = load_state()
    completed = state.get("steps_completed", [])
    if step not in completed:
        completed.append(step)
    state["steps_completed"] = completed
    save_state(state)


# --- Firebase ブラウザ認証 ---


def firebase_browser_auth(hosting_url: str) -> str | None:
    """ブラウザで Firebase Google OAuth を実行し、ID Token を受け取る。

    gh auth login --web と同じパターン:
    1. ランダムポートで localhost サーバー起動
    2. state パラメータ付きで認証ページを開く（CSRF 対策）
    3. POST コールバックで token を受信（URL パラメータには載せない）
    """
    port = _find_free_port()
    state = secrets.token_urlsafe(32)
    token_holder: dict[str, str] = {}

    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            if self.path != "/callback":
                self.send_error(404)
                return
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(length))
            except (json.JSONDecodeError, ValueError):
                self.send_error(400, "Invalid request body")
                return
            if body.get("state") != state:
                self.send_error(403, "Invalid state")
                return
            token = body.get("token", "")
            if not JWT_PATTERN.match(token):
                self.send_error(400, "Invalid token format")
                return
            token_holder["token"] = token
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", hosting_url)
            self.end_headers()
            self.wfile.write("OK".encode())

        def do_OPTIONS(self):
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", hosting_url)
            self.send_header("Access-Control-Allow-Methods", "POST")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

        def log_message(self, *args):
            pass  # サーバーログ抑制

    server = http.server.HTTPServer(("127.0.0.1", port), CallbackHandler)
    server.timeout = 1.0

    auth_url = f"{hosting_url}/auth.html?port={port}&state={state}"
    print(f"\nブラウザで認証ページを開きます...")
    webbrowser.open(auth_url)
    print("ブラウザで Google ログインを完了してください...")
    print(f"(タイムアウト: 120秒)")

    deadline = time.monotonic() + 120
    while time.monotonic() < deadline and "token" not in token_holder:
        server.handle_request()
    server.server_close()

    token = token_holder.get("token")
    if token:
        logger.info("Firebase 認証トークンを取得しました")
    else:
        logger.error("Firebase 認証がタイムアウトしました")
    return token


# --- GitHub ---


def verify_github_ready() -> bool:
    """GitHub CLI が認証済みかチェック。"""
    result = subprocess.run(
        ["gh", "api", "user", "-q", ".login"],
        capture_output=True, text=True, check=False,
    )
    return result.returncode == 0 and bool(result.stdout.strip())


def get_github_username() -> str | None:
    """認証済み GitHub ユーザー名を取得。"""
    result = subprocess.run(
        ["gh", "api", "user", "-q", ".login"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def guide_github_setup() -> bool:
    """GitHub アカウント作成 + gh auth login を案内。

    Returns: True if successfully set up
    """
    print("\n" + "=" * 50)
    print("  GitHub アカウントのセットアップが必要です")
    print("=" * 50)
    print()
    print("1. GitHub アカウントをお持ちでない場合:")
    print("   ブラウザで https://github.com/signup を開いてアカウントを作成してください。")
    print()
    print("2. GitHub CLI でログイン:")
    print("   以下のコマンドを実行してください:")
    print("   $ gh auth login --web -p https")
    print()

    try:
        input("準備ができたら Enter を押してください... ")
    except (EOFError, KeyboardInterrupt):
        return False

    return verify_github_ready()


# --- Cloud Function ---


def call_cloud_function(
    function_url: str,
    firebase_token: str,
    github_username: str,
) -> dict:
    """Cloud Function を呼び出して GitHub 連携 + コラボレーター招待。"""
    import requests

    try:
        resp = requests.post(
            function_url,
            json={
                "firebase_id_token": firebase_token,
                "github_username": github_username,
            },
            timeout=60,
        )
        return resp.json()
    except requests.RequestException as e:
        return {"error": f"Cloud Function への接続に失敗: {e}"}
    except json.JSONDecodeError:
        return {"error": "Cloud Function から無効なレスポンス"}


# --- 招待受諾 ---


def wait_for_invitation(repo: str) -> int | None:
    """GitHub コラボレーター招待をポーリングで待つ。

    Returns: invitation ID or None if timeout
    """
    print(f"\n招待を確認中...")
    deadline = time.monotonic() + INVITATION_POLL_TIMEOUT

    while time.monotonic() < deadline:
        result = subprocess.run(
            ["gh", "api", "/user/repository_invitations"],
            capture_output=True, text=True, check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            try:
                invitations = json.loads(result.stdout)
                for inv in invitations:
                    if inv.get("repository", {}).get("full_name") == repo:
                        return inv["id"]
            except (json.JSONDecodeError, KeyError, TypeError):
                pass
        time.sleep(INVITATION_POLL_INTERVAL)

    return None


def accept_invitation(invitation_id: int) -> bool:
    """GitHub コラボレーター招待を受諾。"""
    result = subprocess.run(
        ["gh", "api", "-X", "PATCH",
         f"/user/repository_invitations/{invitation_id}"],
        capture_output=True, text=True, check=False,
    )
    return result.returncode == 0


# --- メインコマンド ---


def cmd_onboard(
    hosting_url: str = DEFAULT_HOSTING_URL,
    function_url: str = DEFAULT_CLOUD_FUNCTION_URL,
    content_repo: str = DEFAULT_CONTENT_REPO,
) -> int:
    """フルオンボーディングフロー。"""
    state = load_state()
    completed = state.get("steps_completed", [])

    # Step 1: Firebase 認証
    if "firebase_auth" in completed:
        print("✅ Firebase 認証: 完了済み")
    else:
        print("\n📋 Step 1/5: Firebase 認証")
        token = firebase_browser_auth(hosting_url)
        if not token:
            print("❌ Firebase 認証に失敗しました。再度実行してください。")
            return 1
        state["firebase_token"] = token  # 一時保持（永続化はしない）
        mark_step_completed("firebase_auth")
        print("✅ Firebase 認証完了")

    firebase_token = state.get("firebase_token")

    # Step 2: GitHub チェック
    if "github_auth" in completed:
        print("✅ GitHub 認証: 完了済み")
    else:
        print("\n📋 Step 2/5: GitHub アカウント確認")
        if not verify_github_ready():
            if not guide_github_setup():
                print("❌ GitHub のセットアップを完了してから再度実行してください。")
                return 1
        mark_step_completed("github_auth")
        print("✅ GitHub 認証完了")

    github_username = get_github_username()
    if not github_username:
        print("❌ GitHub ユーザー名の取得に失敗しました。")
        return 1
    state["github_username"] = github_username
    # トークンをステートファイルに書き込まないよう除去してから保存
    state_to_save = {k: v for k, v in state.items() if k != "firebase_token"}
    save_state(state_to_save)
    print(f"  GitHub ユーザー名: {github_username}")

    # Step 3: Cloud Function（Firebase ↔ GitHub 連携）
    if "cloud_function" in completed:
        print("✅ Firebase ↔ GitHub 連携: 完了済み")
    else:
        print("\n📋 Step 3/5: Firebase ↔ GitHub 連携")
        if not firebase_token:
            print("⚠️  Firebase トークンが期限切れです。再認証します...")
            firebase_token = firebase_browser_auth(hosting_url)
            if not firebase_token:
                print("❌ 再認証に失敗しました。")
                return 1
            state["firebase_token"] = firebase_token

        result = call_cloud_function(function_url, firebase_token, github_username)
        if "error" in result:
            print(f"❌ 連携に失敗: {result['error']}")
            detail = result.get("detail", "")
            if detail:
                print(f"  詳細: {detail[:200]}")
            return 1
        mark_step_completed("cloud_function")
        print(f"✅ コラボレーター招待を送信しました ({content_repo})")

    # Step 4: 招待受諾
    if "invitation_accepted" in completed:
        print("✅ 招待受諾: 完了済み")
    else:
        print("\n📋 Step 4/5: 招待の受諾")
        invitation_id = wait_for_invitation(content_repo)
        if invitation_id:
            if accept_invitation(invitation_id):
                mark_step_completed("invitation_accepted")
                print("✅ 招待を受諾しました")
            else:
                print("⚠️  招待の受諾に失敗しました。手動で受諾してください。")
        else:
            # フォールバック: 手動受諾
            print(f"\n⚠️  招待が見つかりません。以下を確認してください:")
            print(f"  1. GitHub のメール通知を確認")
            print(f"  2. https://github.com/{content_repo}/invitations にアクセス")
            print()
            try:
                input("招待を受諾したら Enter を押してください... ")
            except (EOFError, KeyboardInterrupt):
                pass
            mark_step_completed("invitation_accepted")

    # Step 5: コンテンツセットアップ
    if "content_setup" in completed:
        print("✅ コンテンツセットアップ: 完了済み")
    else:
        print("\n📋 Step 5/5: 教材コンテンツのセットアップ")
        import content_updater

        if not content_updater.has_upstream():
            ret = content_updater.cmd_setup()
            if ret != 0:
                print("❌ コンテンツのセットアップに失敗しました。")
                return 1
        else:
            ret = content_updater.cmd_update(skill_check=True, skill_strategy="ask")
            if ret != 0:
                print("⚠️  コンテンツ更新で問題が発生しました。再実行してください。")
                return 1

        mark_step_completed("content_setup")
        print("✅ コンテンツセットアップ完了")

    # 完了後に一時トークンを削除
    state.pop("firebase_token", None)
    save_state(state)

    print()
    print("=" * 50)
    print("  🎉 オンボーディング完了！")
    print("=" * 50)
    print(f"  GitHub: {github_username}")
    print(f"  リポジトリ: {content_repo}")
    print()
    print("  教材を更新するには:")
    print("    uv run python tools/content_updater.py")
    print()
    return 0


def cmd_status() -> int:
    """オンボーディング状態を表示。"""
    state = load_state()
    completed = state.get("steps_completed", [])

    print("📋 オンボーディング状態")
    print()

    steps = [
        ("firebase_auth", "Firebase 認証"),
        ("github_auth", "GitHub 認証"),
        ("cloud_function", "Firebase ↔ GitHub 連携"),
        ("invitation_accepted", "招待受諾"),
        ("content_setup", "コンテンツセットアップ"),
    ]

    for step_id, label in steps:
        status = "✅" if step_id in completed else "⬜"
        print(f"  {status} {label}")

    github = state.get("github_username", "")
    if github:
        print(f"\n  GitHub: {github}")

    last_updated = state.get("last_updated", "")
    if last_updated:
        print(f"  最終更新: {last_updated}")

    return 0


def cmd_link_github(
    hosting_url: str = DEFAULT_HOSTING_URL,
    function_url: str = DEFAULT_CLOUD_FUNCTION_URL,
) -> int:
    """Firebase ↔ GitHub 連携のみ実行（既存ユーザー向け）。"""
    # Firebase 認証
    token = firebase_browser_auth(hosting_url)
    if not token:
        print("❌ Firebase 認証に失敗しました。")
        return 1

    # GitHub ユーザー名
    if not verify_github_ready():
        print("❌ GitHub CLI が認証されていません。先に gh auth login を実行してください。")
        return 1

    github_username = get_github_username()
    if not github_username:
        return 1

    # Cloud Function 呼び出し
    result = call_cloud_function(function_url, token, github_username)
    if "error" in result:
        print(f"❌ 連携に失敗: {result['error']}")
        return 1

    print(f"✅ {github_username} をコラボレーターとして招待しました")
    return 0


def cmd_auth_only(hosting_url: str = DEFAULT_HOSTING_URL) -> int:
    """Firebase ブラウザ認証のみ実行。Agent 主導コマンド用。

    トークンは一時ファイルに保存し、パスを stdout に出力する。
    一時ファイルは呼び出し側が責任を持って削除する。
    """
    import tempfile

    token = firebase_browser_auth(hosting_url)
    if not token:
        print("AUTH_FAILED")
        return 1

    # 一時ファイルにトークンを保存（モード 0o600 で他ユーザー読み取り不可）
    fd, tmp_path = tempfile.mkstemp(prefix=".firebase_token_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(token)
    except Exception:
        os.close(fd)
        print("AUTH_FAILED")
        return 1

    os.chmod(tmp_path, 0o600)
    mark_step_completed("firebase_auth")
    print(f"AUTH_OK:{tmp_path}")
    return 0


def cmd_call_function(
    token_file: str,
    function_url: str = DEFAULT_CLOUD_FUNCTION_URL,
) -> int:
    """Cloud Function を呼び出し。Agent 主導コマンド用。

    token_file: auth-only で生成された一時ファイルパス
    """
    token_path = Path(token_file)
    if not token_path.exists():
        print("ERROR:token_file_not_found")
        return 1

    try:
        token = token_path.read_text().strip()
    finally:
        # 読み取り後に即削除
        token_path.unlink(missing_ok=True)

    github_username = get_github_username()
    if not github_username:
        print("ERROR:github_username_not_found")
        return 1

    result = call_cloud_function(function_url, token, github_username)
    if "error" in result:
        print(f"ERROR:{result['error']}")
        return 1

    mark_step_completed("cloud_function")
    # 状態にユーザー名を保存
    state = load_state()
    state["github_username"] = github_username
    save_state(state)
    print(f"OK:{github_username}")
    return 0


def cmd_check_invitation(repo: str = DEFAULT_CONTENT_REPO) -> int:
    """招待を確認して受諾する。Agent 主導コマンド用。"""
    invitation_id = wait_for_invitation(repo)
    if invitation_id:
        if accept_invitation(invitation_id):
            mark_step_completed("invitation_accepted")
            print(f"ACCEPTED:{invitation_id}")
            return 0
        else:
            print("ERROR:accept_failed")
            return 1
    else:
        print("NOT_FOUND")
        return 1


def cmd_cleanup_token() -> int:
    """残存する一時トークンファイルを削除。"""
    import glob
    import tempfile

    pattern = os.path.join(tempfile.gettempdir(), ".firebase_token_*.tmp")
    removed = 0
    for f in glob.glob(pattern):
        try:
            os.unlink(f)
            removed += 1
        except OSError:
            pass
    if removed:
        print(f"CLEANED:{removed}")
    else:
        print("CLEAN")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Firebase 連携オンボーディング",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    onboard_parser = sub.add_parser("onboard", help="フルオンボーディングフロー")
    onboard_parser.add_argument(
        "--hosting-url", default=DEFAULT_HOSTING_URL,
        help="Firebase Hosting URL",
    )
    onboard_parser.add_argument(
        "--function-url", default=DEFAULT_CLOUD_FUNCTION_URL,
        help="Cloud Function URL",
    )

    sub.add_parser("status", help="オンボーディング状態確認")

    link_parser = sub.add_parser("link-github", help="Firebase ↔ GitHub 連携のみ")
    link_parser.add_argument(
        "--hosting-url", default=DEFAULT_HOSTING_URL,
        help="Firebase Hosting URL",
    )
    link_parser.add_argument(
        "--function-url", default=DEFAULT_CLOUD_FUNCTION_URL,
        help="Cloud Function URL",
    )

    # Agent 主導コマンド用サブコマンド
    auth_parser = sub.add_parser("auth-only", help="Firebase 認証のみ（トークンを一時ファイルに保存）")
    auth_parser.add_argument(
        "--hosting-url", default=DEFAULT_HOSTING_URL,
        help="Firebase Hosting URL",
    )

    cf_parser = sub.add_parser("call-function", help="Cloud Function 呼び出し")
    cf_parser.add_argument("token_file", help="auth-only で生成されたトークンファイルパス")
    cf_parser.add_argument(
        "--function-url", default=DEFAULT_CLOUD_FUNCTION_URL,
        help="Cloud Function URL",
    )

    onboard_parser.add_argument(
        "--content-repo", default=DEFAULT_CONTENT_REPO,
        help="招待・セットアップ対象のコンテンツリポジトリ",
    )

    inv_parser = sub.add_parser("check-invitation", help="招待を確認・受諾")
    inv_parser.add_argument("--repo", default=DEFAULT_CONTENT_REPO, help="リポジトリ")

    sub.add_parser("cleanup-token", help="残存する一時トークンファイルを削除")

    args = parser.parse_args()

    if args.command == "onboard":
        return cmd_onboard(
            hosting_url=args.hosting_url,
            function_url=args.function_url,
            content_repo=args.content_repo,
        )
    elif args.command == "status":
        return cmd_status()
    elif args.command == "link-github":
        return cmd_link_github(
            hosting_url=args.hosting_url,
            function_url=args.function_url,
        )
    elif args.command == "auth-only":
        return cmd_auth_only(hosting_url=args.hosting_url)
    elif args.command == "call-function":
        return cmd_call_function(
            token_file=args.token_file,
            function_url=args.function_url,
        )
    elif args.command == "check-invitation":
        return cmd_check_invitation(repo=args.repo)
    elif args.command == "cleanup-token":
        return cmd_cleanup_token()
    return 1


if __name__ == "__main__":
    sys.exit(main())
