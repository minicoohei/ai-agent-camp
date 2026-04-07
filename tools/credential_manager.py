#!/usr/bin/env python3
"""
Credential Manager - OS Credential Store ラッパー

平文の .env / .env.local ファイルを廃止し、OS 標準の暗号化ストレージで
APIキー・トークンを安全に管理する。

対応 OS:
  - macOS: Keychain (AES-256-GCM)
  - Windows: Windows Credential Locker (DPAPI)
  - Linux: SecretService (GNOME Keyring / KWallet)

使用方法:
  # キーを保存（getpass で非表示入力）
  uv run python tools/credential_manager.py store GEMINI_API_KEY

  # .env.local に貼る場所を用意
  uv run python tools/credential_manager.py prepare-dotenv GEMINI_API_KEY

  # .env.local から対象キーだけ移行して削除
  uv run python tools/credential_manager.py import-dotenv GEMINI_API_KEY --delete

  # 保存済みキーの確認（マスク表示）
  uv run python tools/credential_manager.py status

  # .env / .env.local から一括移行
  uv run python tools/credential_manager.py migrate

  # .env / .env.local を安全に削除
  uv run python tools/credential_manager.py cleanup

  # キーを削除
  uv run python tools/credential_manager.py delete GEMINI_API_KEY

セキュリティ設計:
  - 値はログ/stdout に一切出力しない（マスク処理のみ）
  - getpass() で入力時も画面に値が表示されない
  - AI チャットのコンテキストにキーの値が残らない設計
  - keyring 未対応環境ではサイレントスキップ（CI/CD 対応）
"""

import argparse
import getpass
import logging
import os
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

try:
    from i18n_common import setup_gettext
except ImportError:
    try:
        from tools.i18n_common import setup_gettext
    except ImportError:
        def setup_gettext():
            return lambda x: x

_ = setup_gettext()

logger = logging.getLogger(__name__)

# ========== 定数 ==========

SERVICE_NAME = "aiagent-base"

ROOT_DIR = Path(__file__).parent.parent
DEFAULT_PREPARE_ENV_FILE = ROOT_DIR / ".env.local"
DEFAULT_ENV_CANDIDATES = [ROOT_DIR / ".env.local", ROOT_DIR / ".env"]

# 管理対象キー一覧（.env に存在する全キーをカバー）
MANAGED_KEYS = [
    # Google / Gemini
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
    "GOOGLE_CLIENT_ID",
    "GOOGLE_CLIENT_SECRET",
    "GOOGLE_REFRESH_TOKEN",
    "GOOGLE_CLOUD_PROJECT",
    "GCP_SA_KEY",
    "GOOGLE_WORKSPACE_USER",
    "GMAIL_ACCOUNTS_CONFIG",
    "GOG_ACCOUNT",
    "GOG_KEYRING_PASSWORD",
    # Anthropic
    "ANTHROPIC_API_KEY",
    # Slack
    "SLACK_BOT_TOKEN",
    "SLACK_USER_TOKEN",
    "SLACK_USER_TOKEN_INFOBOX",
    "SLACK_USER_TOKEN_YOAKE",
    "SLACK_USER_TOKEN_FUNGIBLEX",
    "SLACK_USER_TOKEN_KOHEI",
    "SLACK_USER_TOKEN_INFOBOX_KOHEI",
    "SLACK_USER_TOKEN_YOAKE_KOHEI",
    "SLACK_USER_TOKEN_FUNGIBLEX_KOHEI",
    "SLACK_CLIENT_ID",
    "SLACK_CLIENT_SECRET",
    "SLACK_CLIENT_ID_INFOBOX",
    "SLACK_CLIENT_SECRET_INFOBOX",
    "SLACK_CLIENT_ID_YOAKE",
    "SLACK_CLIENT_SECRET_YOAKE",
    "SLACK_CLIENT_ID_FUNGIBLEX",
    "SLACK_CLIENT_SECRET_FUNGIBLEX",
    "SLACK_SIGN_SECRET",
    "SLACK_REDIRECT_URI",
    # Notion
    "NOTION_API_KEY",
    "NOTION_DATABASE_ID",
    "NOTION_CLIENT_ID",
    # X (Twitter)
    "X_BEARER_TOKEN",
    "X_API_KEY",
    "X_API_SECRET",
    "X_CLIENT_ID",
    "X_CLIENT_SECRET",
    "X_CONSUMER_KEY",
    "X_CONSUMER_SECRET",
    "X_ACCESS_TOKEN",
    "X_ACCESS_TOKEN_SECRET",
    "X_ACCESS_TOKEN_CURSOR_BOOTCAMP",
    "X_ACCESS_TOKEN_CURSOR_BOOTCAMP_SECRET",
    # AI / 動画生成
    "FAL_KEY",
    "KLING_ACCESS_KEY",
    "KLING_SECRET_KEY",
    "HEYGEN_API_KEY",
    "ELEVENLABS_API_KEY",
    "ELEVEN_API_KEY",  # ELEVENLABS_API_KEY のエイリアス（一部コードで使用）
    # SNS / 投稿管理
    "TYPEFULLY_API_KEY",
    # LINE
    "LINE_CHANNEL_ACCESS_TOKEN",
    "LINE_USER_ID",
    # GitHub
    "GITHUB_TOKEN",
    "GH_TOKEN",
    # Firebase
    "FIREBASE_API_KEY",
    "FIREBASE_PROJECT_ID",
]

PLACEHOLDER_VALUES = {
    "your_gemini_api_key_here",
    "your_api_key_here",
    "your_token_here",
    "",
}


# ========== keyring 可用性チェック ==========

_keyring_available: Optional[bool] = None


def _check_keyring() -> bool:
    """keyring ライブラリが使用可能か確認"""
    global _keyring_available
    if _keyring_available is not None:
        return _keyring_available
    try:
        import keyring as _kr
        # バックエンドが有効かテスト（fail backend でないことを確認）
        backend = _kr.get_keyring()
        backend_name = type(backend).__name__
        # fail backend や chainer の null backend は使用不可とみなす
        if "fail" in backend_name.lower() or "null" in backend_name.lower():
            logger.warning(
                "keyring backend is not usable: %s. "
                "Install a keyring backend for your OS.",
                backend_name,
            )
            _keyring_available = False
        else:
            _keyring_available = True
    except Exception as e:
        logger.warning("keyring is not available: %s", e)
        _keyring_available = False
    return _keyring_available


def _get_keyring():
    """keyring モジュールを取得"""
    import keyring
    return keyring


# ========== マスク処理 ==========


def _mask(value: str) -> str:
    """値をマスク表示用に変換。stdout に平文を出さない。"""
    if not value:
        return "(empty)"
    if len(value) <= 12:
        return "***"
    return value[:4] + "..." + value[-4:]


# ========== コア機能 ==========


def store(key: str, value: str) -> bool:
    """Credential Store にキーを保存

    Args:
        key: 環境変数名（例: GEMINI_API_KEY）
        value: 秘密値

    Returns:
        True if stored successfully
    """
    if not _check_keyring():
        print(_("❌ keyring が利用できません。OS の Credential Store を確認してください。"))
        return False

    kr = _get_keyring()
    try:
        kr.set_password(SERVICE_NAME, key, value)
        print(_("✅ Stored {key} (value: {masked})").format(key=key, masked=_mask(value)))
        return True
    except Exception as e:
        err_str = str(e)
        if "-25244" in err_str:
            print(_("❌ {key} の保存に失敗しました: Keychain の所有権エラー").format(key=key))
            print(_("   同じキー名が別プロセスによって登録済みのため上書きできません。"))
            print(_("   以下のコマンドで既存エントリを削除してから再実行してください:"))
            print(_('     security delete-generic-password -s "{service}" -a "{key}"').format(service=SERVICE_NAME, key=key))
            print(_("   または「キーチェーンアクセス.app」で「{service}」を検索して手動削除").format(service=SERVICE_NAME))
        else:
            print(_("❌ Failed to store {key}: {err}").format(key=key, err=e))
        return False


def get(key: str) -> Optional[str]:
    """Credential Store からキーを取得

    Args:
        key: 環境変数名

    Returns:
        秘密値。未設定の場合は None
    """
    if not _check_keyring():
        return None

    kr = _get_keyring()
    try:
        return kr.get_password(SERVICE_NAME, key)
    except Exception:
        return None


def delete(key: str) -> bool:
    """Credential Store からキーを削除

    Args:
        key: 環境変数名

    Returns:
        True if deleted successfully
    """
    if not _check_keyring():
        print(_("❌ keyring が利用できません。"))
        return False

    kr = _get_keyring()
    try:
        kr.delete_password(SERVICE_NAME, key)
        print(_("✅ Deleted {key}").format(key=key))
        return True
    except Exception as e:
        print(_("❌ Failed to delete {key}: {err}").format(key=key, err=e))
        return False


def inject_to_environ() -> int:
    """Credential Store の全キーを os.environ に注入

    既にシステム環境変数にセットされているキーはスキップ（CI/CD 対応）。
    .env にしか存在しないキーがあれば WARNING を出す。

    Returns:
        注入したキーの数
    """
    if not _check_keyring():
        return 0

    kr = _get_keyring()
    injected = 0

    for key in MANAGED_KEYS:
        # 既にシステム環境変数にセットされていればスキップ（空文字も設定済みとみなす）
        if key in os.environ:
            continue

        try:
            value = kr.get_password(SERVICE_NAME, key)
            if value:
                os.environ[key] = value
                injected += 1
        except Exception as e:
            logger.debug("Failed to load %s from keyring: %s", key, e)

    return injected


def _parse_dotenv(env_path: Path) -> dict[str, str]:
    """.env ファイルをパースしてキーバリューの辞書を返す

    python-dotenv の dotenv_values() が利用可能ならそちらを使用し、
    コメント・export プレフィクス・複数行値等のエッジケースに対応する。
    """
    if not env_path.exists():
        return {}

    try:
        from dotenv import dotenv_values
        raw = dotenv_values(env_path)
        return {k: v for k, v in raw.items() if v}
    except ImportError:
        pass

    # フォールバック: 手動パース
    result = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # export プレフィクスを除去
            if line.startswith("export "):
                line = line[7:]
            match = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)=(.*)$', line)
            if match:
                key = match.group(1)
                value = match.group(2).strip()
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                if value:
                    result[key] = value
    return result


def _resolve_env_file(env_path: Optional[Path] = None, *, for_write: bool = False) -> Path:
    """対象の dotenv ファイルを解決する。"""
    if env_path is not None:
        return env_path

    if for_write:
        return DEFAULT_PREPARE_ENV_FILE

    for candidate in DEFAULT_ENV_CANDIDATES:
        if candidate.exists():
            return candidate

    return DEFAULT_PREPARE_ENV_FILE


def _upsert_dotenv_values(
    env_path: Path,
    values: dict[str, str],
    *,
    preserve_empty: bool = False,
) -> None:
    existing_lines: list[str] = []
    if env_path.exists():
        existing_lines = env_path.read_text(encoding="utf-8").splitlines()

    remaining = dict(values)
    rendered_lines: list[str] = []
    pattern = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$")

    for line in existing_lines:
        match = pattern.match(line)
        if not match:
            rendered_lines.append(line)
            continue

        key = match.group(1)
        if key not in remaining:
            rendered_lines.append(line)
            continue

        value = remaining.pop(key)
        if preserve_empty and value == "":
            rendered_lines.append(f"{key}=")
        else:
            rendered_lines.append(f"{key}={value}")

    for key, value in remaining.items():
        if preserve_empty and value == "":
            rendered_lines.append(f"{key}=")
        else:
            rendered_lines.append(f"{key}={value}")

    content = "\n".join(rendered_lines)
    if rendered_lines:
        content += "\n"
    env_path.write_text(content, encoding="utf-8")


def _remove_dotenv_keys(env_path: Path, keys: list[str]) -> None:
    if not env_path.exists():
        return

    targets = set(keys)
    kept_lines: list[str] = []
    pattern = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$")

    for line in env_path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match and match.group(1) in targets:
            continue
        kept_lines.append(line)

    content = "\n".join(kept_lines)
    if kept_lines:
        content += "\n"
    env_path.write_text(content, encoding="utf-8")


def prepare_dotenv(keys: list[str], env_path: Optional[Path] = None) -> Path:
    """指定キーを貼り付け可能な状態で dotenv に用意する。"""
    target = _resolve_env_file(env_path, for_write=True)
    _upsert_dotenv_values(target, {key: "" for key in keys}, preserve_empty=True)
    return target


def import_from_dotenv(
    keys: list[str],
    env_path: Optional[Path] = None,
    *,
    delete: bool = False,
) -> dict[str, str]:
    """dotenv から指定キーのみを Credential Store に移行する。"""
    source = _resolve_env_file(env_path)

    if not source.exists():
        print(_("❌ dotenv ファイルが見つかりません: {path}").format(path=source))
        return {}

    if not _check_keyring():
        print(_("❌ keyring が利用できません。"))
        return {}

    env_vars = _parse_dotenv(source)
    results: dict[str, str] = {}
    imported: list[str] = []

    for key in keys:
        value = env_vars.get(key)
        if value is None:
            results[key] = "missing"
            continue
        if value.lower() in PLACEHOLDER_VALUES:
            results[key] = "skipped (placeholder)"
            continue
        if store(key, value):
            results[key] = "ok"
            imported.append(key)
        else:
            results[key] = "error"

    if delete and imported:
        _remove_dotenv_keys(source, imported)
        print(_("✅ 移行済みキーを削除しました: {path}").format(path=source))

    return results


def migrate_from_dotenv(env_path: Optional[Path] = None) -> dict[str, str]:
    """dotenv の全キーを Credential Store に移行

    Args:
        env_path: dotenv ファイルのパス。None の場合は .env.local → .env の順に探索

    Returns:
        移行結果の辞書 {key: "ok" | "skipped" | "error message"}
    """
    env_path = _resolve_env_file(env_path)

    if not env_path.exists():
        print(_("❌ dotenv ファイルが見つかりません: {path}").format(path=env_path))
        return {}

    if not _check_keyring():
        print(_("❌ keyring が利用できません。"))
        return {}

    env_vars = _parse_dotenv(env_path)
    results = {}

    migrated = 0
    skipped = 0

    for key, value in env_vars.items():
        if value.lower() in PLACEHOLDER_VALUES:
            results[key] = "skipped (placeholder)"
            skipped += 1
            continue

        if store(key, value):
            results[key] = "ok"
            migrated += 1
        else:
            results[key] = "error"

    print(_("\n📊 移行結果: {migrated} 件保存, {skipped} 件スキップ").format(migrated=migrated, skipped=skipped))
    return results


def cleanup_dotenv(env_path: Optional[Path] = None) -> bool:
    """dotenv を安全に削除（上書き消去）

    Args:
        env_path: dotenv ファイルのパス

    Returns:
        True if cleaned up successfully
    """
    env_path = _resolve_env_file(env_path)

    if not env_path.exists():
        print(_("ℹ️ dotenv ファイルは既に存在しません。"))
        return True

    # まず keyring に全キーが移行済みか確認
    env_vars = _parse_dotenv(env_path)
    missing = []
    unmanaged = []
    for key in env_vars:
        if key in MANAGED_KEYS:
            if not get(key):
                missing.append(key)
        else:
            unmanaged.append(key)

    if unmanaged:
        print(_("⚠️ 以下のキーは MANAGED_KEYS に未登録のため、移行されていません:"))
        for k in unmanaged:
            print(f"   - {k}")
        print(_("これらのキーは dotenv 削除後に失われます。"))
        print(_("続行するには、先に MANAGED_KEYS に追加して 'migrate' を実行するか、"))
        print(_("手動でバックアップしてください。"))
        return False

    if missing:
        print(_("⚠️ 以下のキーが Credential Store に未移行です:"))
        for k in missing:
            print(f"   - {k}")
        print(_("先に 'migrate' を実行してください。"))
        return False

    # 安全削除（上書き消去）
    try:
        file_size = env_path.stat().st_size
        system = platform.system()

        import shutil as _shutil

        if system == "Darwin":
            # macOS: rm -P (3回上書き後削除)
            # 注: SSD + APFS 環境では TRIM により物理的な上書き効果は保証されない
            rm_bin = _shutil.which("rm") or "rm"
            subprocess.run([rm_bin, "-P", "--", str(env_path.resolve())], check=True)
        elif system == "Linux":
            # Linux: shred があれば使う
            shred_bin = _shutil.which("shred")
            if shred_bin:
                subprocess.run(
                    [shred_bin, "-u", "-z", "-n", "3", "--", str(env_path.resolve())], check=True
                )
            else:
                # shred がなければ手動上書き
                with open(env_path, "wb") as f:
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())
                env_path.unlink()
        elif system == "Windows":
            # Windows: cipher /w は dir 単位なので、手動上書き + 削除
            with open(env_path, "wb") as f:
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())
            env_path.unlink()
        else:
            # フォールバック
            with open(env_path, "wb") as f:
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())
            env_path.unlink()

        print(_("✅ dotenv を安全に削除しました: {path}").format(path=env_path))
        return True
    except Exception as e:
        print(_("❌ dotenv の削除に失敗しました: {err}").format(err=e))
        return False


def status(env_path: Optional[Path] = None):
    """各キーの保存場所を表示"""
    env_path = _resolve_env_file(env_path)

    env_vars = _parse_dotenv(env_path) if env_path.exists() else {}
    keyring_ok = _check_keyring()
    env_label = env_path.name

    print("=" * 65)
    print(_("🔐 Credential Status"))
    print("=" * 65)

    if keyring_ok:
        kr = _get_keyring()
        backend_name = type(kr.get_keyring()).__name__
        print(_("Backend: {name}").format(name=backend_name))
    else:
        print(_("Backend: ❌ keyring not available"))

    exists_label = _("exists") if env_path.exists() else _("not found")
    print(f"{env_label}:    {exists_label}")
    print("-" * 65)
    print(f"{_('Key'):<35} {_('Source'):<15} {_('Value')}")
    print("-" * 65)

    for key in MANAGED_KEYS:
        # チェック順: 環境変数 → keyring → .env
        env_val = os.environ.get(key)
        kr_val = get(key) if keyring_ok else None
        dotenv_val = env_vars.get(key)

        if env_val:
            source = "env"
            display = _mask(env_val)
        elif kr_val:
            source = "credential"
            display = _mask(kr_val)
        elif dotenv_val:
            source = f"⚠️ {env_label}"
            display = _mask(dotenv_val)
        else:
            source = "-"
            display = "(not set)"

        print(f"{key:<35} {source:<15} {display}")

    print("-" * 65)

    # dotenv に存在するが MANAGED_KEYS にないキーも表示
    extra_keys = set(env_vars.keys()) - set(MANAGED_KEYS)
    if extra_keys:
        print(_("\n⚠️ {label} にのみ存在するキー（MANAGED_KEYS 未登録）:").format(label=env_label))
        for key in sorted(extra_keys):
            print(f"   {key} = {_mask(env_vars[key])}")

    if env_path.exists():
        print(
            _("\n⚠️ {label} ファイルが存在しています。平文の秘密情報がディスク上にあります。").format(label=env_label)
        )
        print(
            _("   'uv run python tools/credential_manager.py migrate' で Credential Store に移行してください。")
        )


# ========== CLI ==========


def main():
    parser = argparse.ArgumentParser(
        description="OS Credential Store でAPIキー・トークンを安全に管理",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # キーを保存（getpass で非表示入力）
  uv run python tools/credential_manager.py store GEMINI_API_KEY

  # .env.local に貼る場所を用意
  uv run python tools/credential_manager.py prepare-dotenv GEMINI_API_KEY

  # 保存後に .env.local から移行して削除
  uv run python tools/credential_manager.py import-dotenv GEMINI_API_KEY --delete

  # 保存済みキーの確認（マスク表示のみ）
  uv run python tools/credential_manager.py status

  # .env / .env.local から一括移行
  uv run python tools/credential_manager.py migrate

  # .env / .env.local を安全に削除
  uv run python tools/credential_manager.py cleanup
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="コマンド")

    # store
    store_parser = subparsers.add_parser("store", help="キーを保存")
    store_parser.add_argument("key", help="環境変数名 (例: GEMINI_API_KEY)")
    store_parser.add_argument(
        "--value",
        default=None,
        help="値を直接指定（非TTY環境向け。省略時は getpass で非表示入力）",
    )

    # get (マスク表示)
    get_parser = subparsers.add_parser("get", help="キーの存在確認（マスク表示）")
    get_parser.add_argument("key", help="環境変数名")

    # delete
    delete_parser = subparsers.add_parser("delete", help="キーを削除")
    delete_parser.add_argument("key", help="環境変数名")

    # prepare-dotenv
    prepare_parser = subparsers.add_parser(
        "prepare-dotenv",
        help=".env.local にキーの貼り付け場所を用意",
    )
    prepare_parser.add_argument("keys", nargs="+", help="環境変数名")
    prepare_parser.add_argument(
        "--env-file",
        type=Path,
        default=None,
        help="dotenv ファイルのパス（省略時は .env.local）",
    )

    # import-dotenv
    import_parser = subparsers.add_parser(
        "import-dotenv",
        help="dotenv から指定キーだけを Credential Store に移行",
    )
    import_parser.add_argument("keys", nargs="+", help="環境変数名")
    import_parser.add_argument(
        "--env-file",
        type=Path,
        default=None,
        help="dotenv ファイルのパス（省略時は .env.local → .env）",
    )
    import_parser.add_argument(
        "--delete",
        action="store_true",
        help="移行に成功したキーを dotenv から削除",
    )

    # migrate
    migrate_parser = subparsers.add_parser(
        "migrate", help=".env.local / .env から Credential Store に一括移行"
    )
    migrate_parser.add_argument(
        "--env-file", type=Path, default=None, help="dotenv ファイルのパス"
    )

    # cleanup
    cleanup_parser = subparsers.add_parser(
        "cleanup", help=".env.local / .env を安全に削除（上書き消去）"
    )
    cleanup_parser.add_argument(
        "--env-file", type=Path, default=None, help="dotenv ファイルのパス"
    )

    # status
    status_parser = subparsers.add_parser(
        "status", help="全キーの保存場所を表示"
    )
    status_parser.add_argument(
        "--env-file", type=Path, default=None, help=".env ファイルのパス"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "store":
        if not _check_keyring():
            print(_("❌ keyring が利用できません。"))
            print(_("   pip install keyring を実行してください。"))
            sys.exit(1)

        if args.value:
            value = args.value
        else:
            value = getpass.getpass(_("Enter value for {key}: ").format(key=args.key))
        if not value.strip():
            print(_("❌ 空の値は保存できません。"))
            sys.exit(1)
        store(args.key, value.strip())

    elif args.command == "get":
        value = get(args.key)
        if value:
            print(_("✅ {key} = {masked}").format(key=args.key, masked=_mask(value)))
        else:
            print(_("❌ {key} is not stored in Credential Store").format(key=args.key))

    elif args.command == "delete":
        confirm = input(_("⚠️ {key} を削除しますか? [y/N]: ").format(key=args.key)).strip().lower()
        if confirm == "y":
            delete(args.key)
        else:
            print(_("⏭️ スキップしました"))

    elif args.command == "prepare-dotenv":
        prepared = prepare_dotenv(args.keys, args.env_file)
        print(_("✅ 貼り付け先を用意しました: {path}").format(path=prepared))

    elif args.command == "import-dotenv":
        results = import_from_dotenv(args.keys, args.env_file, delete=args.delete)
        ok_count = sum(1 for value in results.values() if value == "ok")
        missing = [key for key, value in results.items() if value == "missing"]
        skipped = [key for key, value in results.items() if value.startswith("skipped")]
        if ok_count:
            print(_("📊 {count} 件を Credential Store に移行しました。").format(count=ok_count))
        if missing:
            print(_("⚠️ dotenv に値が無かったキー:"))
            for key in missing:
                print(f"   - {key}")
        if skipped:
            print(_("ℹ️ プレースホルダーのため移行しなかったキー:"))
            for key in skipped:
                print(f"   - {key}")

    elif args.command == "migrate":
        env_file = args.env_file
        migrate_from_dotenv(env_file)

    elif args.command == "cleanup":
        env_file = args.env_file
        confirm = input(
            _("⚠️ .env ファイルを安全に削除します（上書き消去）。元に戻せません。続行しますか? [y/N]: ")
        ).strip().lower()
        if confirm == "y":
            cleanup_dotenv(env_file)
        else:
            print(_("⏭️ スキップしました"))

    elif args.command == "status":
        status(args.env_file)


if __name__ == "__main__":
    main()
