#!/usr/bin/env python3
"""教材コンテンツの差分更新ツール。

プライベートリポジトリ（upstream）からコンテンツパスのみを強制チェックアウトし、
ユーザーファイル（.env, output/, work/ 等）には一切触れない安全な更新を行う。

使い方:
    uv run python tools/content_updater.py                    # 更新実行
    uv run python tools/content_updater.py --dry-run          # 変更内容を事前確認
    uv run python tools/content_updater.py --rollback         # 直前の更新を取り消し
    uv run python tools/content_updater.py --setup            # 初回セットアップ（upstream 追加）
    uv run python tools/content_updater.py --status           # 現在のバージョンと更新状況を表示

前提:
    - gh auth login 済み（GitHub CLI で認証済み）
    - コンテンツリポジトリへのコラボレーター招待を受諾済み
"""

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urlunparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from log_utils import setup_logger

logger = setup_logger("content_updater")

# --- 定数 ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_REMOTE = "upstream"
UPSTREAM_BRANCH = "main"
UPDATE_LOG_FILE = PROJECT_ROOT / "work" / ".update-log.json"
BACKUP_BASE_DIR = PROJECT_ROOT / "work" / ".backup"
DEFAULT_UPSTREAM_URL = os.getenv(
    "AIAGENT_CONTENT_UPSTREAM_URL",
    "https://github.com/TokenPocket/ai-agent-camp.git",
)

# コンテンツ空間: upstream から強制上書きするパス
CONTENT_PATHS = [
    "course/",
    ".claude/skills/",
    ".claude/commands/",
    ".cursor/commands/",
    ".cursor/rules/",
    "tools/",
    "docs/setup-guides/",
    "scripts/",
    "courses/",
    "skills/",
    "CLAUDE.md",
    "requirements.txt",
    "package.json",
    "external-plugins.yaml",
]

# スキルパス: コンフリクト検出対象
SKILL_PATHS = [".claude/skills/", "skills/"]
# スキル以外のコンテンツパス: 強制上書き
NON_SKILL_CONTENT_PATHS = [p for p in CONTENT_PATHS if p not in SKILL_PATHS]

# コンテンツ空間内でもユーザーが変更しうるファイル（バックアップ対象）
BACKUP_BEFORE_UPDATE = [
    "course/exercises/",
]


def _sanitize_url(url: str) -> str:
    """URL から認証情報（PAT やパスワード）を除去して表示用にする。"""
    parsed = urlparse(url)
    if parsed.username or parsed.password:
        clean_netloc = parsed.hostname or ""
        if parsed.port:
            clean_netloc += f":{parsed.port}"
        return urlunparse(parsed._replace(netloc=clean_netloc))
    return url


def run_git(*args: str, check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    """git コマンドを PROJECT_ROOT で実行する。"""
    cmd = ["git", "-C", str(PROJECT_ROOT), *args]
    return subprocess.run(
        cmd,
        capture_output=capture,
        text=True,
        check=check,
    )


def is_git_repo() -> bool:
    """PROJECT_ROOT が git リポジトリかどうか。"""
    result = run_git("rev-parse", "--is-inside-work-tree", check=False)
    return result.returncode == 0


def has_upstream() -> bool:
    """upstream リモートが設定されているか。"""
    result = run_git("remote", check=False)
    if result.returncode != 0:
        return False
    return UPSTREAM_REMOTE in result.stdout.strip().split("\n")


def get_upstream_url() -> str | None:
    """upstream リモートの URL を取得。"""
    if not has_upstream():
        return None
    result = run_git("remote", "get-url", UPSTREAM_REMOTE, check=False)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def get_current_commit() -> str | None:
    """現在の HEAD コミットハッシュ。"""
    result = run_git("rev-parse", "HEAD", check=False)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def get_upstream_commit() -> str | None:
    """upstream/main の最新コミットハッシュ（fetch 後）。"""
    result = run_git("rev-parse", f"{UPSTREAM_REMOTE}/{UPSTREAM_BRANCH}", check=False)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def fetch_upstream() -> bool:
    """upstream から最新を取得。"""
    logger.info("upstream から最新を取得中...")
    result = run_git("fetch", UPSTREAM_REMOTE, check=False)
    if result.returncode != 0:
        logger.error("fetch 失敗: %s", result.stderr.strip())
        return False
    logger.info("fetch 完了")
    return True


def get_changed_files() -> list[str]:
    """upstream/main と現在のコンテンツパスの差分ファイル一覧を取得。"""
    ref = f"{UPSTREAM_REMOTE}/{UPSTREAM_BRANCH}"
    all_changed = []
    for path in CONTENT_PATHS:
        result = run_git(
            "diff", "--name-only", f"HEAD..{ref}", "--", path,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            all_changed.extend(result.stdout.strip().split("\n"))
    return sorted(set(all_changed))


def get_new_files_in_upstream() -> list[str]:
    """upstream にあるが現在のツリーにないファイル（新規追加分）。"""
    ref = f"{UPSTREAM_REMOTE}/{UPSTREAM_BRANCH}"
    all_new = []
    for path in CONTENT_PATHS:
        result = run_git(
            "diff", "--name-only", "--diff-filter=A", f"HEAD..{ref}", "--", path,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            all_new.extend(result.stdout.strip().split("\n"))
    return sorted(set(all_new))


def get_deleted_files_in_upstream() -> list[str]:
    """upstream で削除されたファイル。"""
    ref = f"{UPSTREAM_REMOTE}/{UPSTREAM_BRANCH}"
    all_deleted = []
    for path in CONTENT_PATHS:
        result = run_git(
            "diff", "--name-only", "--diff-filter=D", f"HEAD..{ref}", "--", path,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            all_deleted.extend(result.stdout.strip().split("\n"))
    return sorted(set(all_deleted))


def backup_files(files_to_backup: list[str], timestamp: str) -> Path | None:
    """更新前にバックアップを作成。"""
    backup_dir = BACKUP_BASE_DIR / timestamp
    backed_up = []

    for pattern in BACKUP_BEFORE_UPDATE:
        matching = [f for f in files_to_backup if f.startswith(pattern)]
        for f in matching:
            src = PROJECT_ROOT / f
            if src.exists():
                dst = backup_dir / f
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                backed_up.append(f)

    if backed_up:
        logger.info("バックアップ作成: %s (%d ファイル)", backup_dir, len(backed_up))
        return backup_dir
    return None


def checkout_content() -> tuple[bool, list[str]]:
    """コンテンツパスを upstream/main から強制チェックアウト。

    Returns:
        (success, failed_paths): 成功フラグと失敗したパスのリスト
    """
    ref = f"{UPSTREAM_REMOTE}/{UPSTREAM_BRANCH}"
    logger.info("コンテンツを %s から取得中...", ref)

    # NOTE: tools/ には本スクリプト自体が含まれるが、Python は起動時に
    # バイトコードを読み込んでいるため、実行中の上書きは問題ない。

    success_count = 0
    skipped = []
    failed = []
    for path in CONTENT_PATHS:
        result = run_git("checkout", ref, "--", path, check=False)
        if result.returncode == 0:
            success_count += 1
        else:
            stderr = result.stderr.strip()
            if "did not match any" in stderr or "pathspec" in stderr:
                skipped.append(path)
                logger.debug("パス '%s' は upstream に存在しません（スキップ）", path)
            else:
                failed.append(path)
                logger.error("パス '%s' のチェックアウトに失敗: %s", path, stderr)

    if success_count == 0:
        logger.error("コンテンツのチェックアウトに全て失敗しました")
        return False, failed

    if failed:
        logger.warning(
            "一部パスのチェックアウトに失敗しました (%d 件): %s",
            len(failed), ", ".join(failed),
        )

    logger.info(
        "コンテンツ更新: %d 成功, %d スキップ, %d 失敗",
        success_count, len(skipped), len(failed),
    )
    return len(failed) == 0, failed


# --- スキルコンフリクト処理 ---


def get_merge_base() -> str | None:
    """HEAD と upstream/main のマージベースを取得。"""
    result = run_git(
        "merge-base", "HEAD", f"{UPSTREAM_REMOTE}/{UPSTREAM_BRANCH}",
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def list_skill_dirs(skill_base: str) -> list[str]:
    """スキルベースパス下の個別スキルディレクトリ一覧を返す。

    例: skill_base="skills/" → ["skills/banner-creator/", "skills/nanobanana/", ...]
    upstream 側のスキルも含めるため、両方のツリーを確認する。
    """
    ref = f"{UPSTREAM_REMOTE}/{UPSTREAM_BRANCH}"
    dirs = set()

    # ローカル側
    local_dir = PROJECT_ROOT / skill_base
    if local_dir.is_dir():
        for child in local_dir.iterdir():
            if child.is_dir() and not child.name.startswith("."):
                dirs.add(f"{skill_base}{child.name}/")

    # upstream 側（ls-tree で確認）
    result = run_git("ls-tree", "--name-only", f"{ref}:{skill_base}", check=False)
    if result.returncode == 0 and result.stdout.strip():
        for name in result.stdout.strip().split("\n"):
            name = name.strip()
            if name and not name.startswith("."):
                dirs.add(f"{skill_base}{name}/")

    return sorted(dirs)


def classify_skill_changes(
    skill_base: str,
    merge_base: str | None = None,
) -> dict[str, str]:
    """各スキルの変更状態を merge-base 基準の3方向比較で分類。

    Returns:
        {skill_path: "unchanged"|"upstream_only"|"local_only"|"conflict"}
    """
    ref = f"{UPSTREAM_REMOTE}/{UPSTREAM_BRANCH}"
    if merge_base is None:
        merge_base = get_merge_base()
    if not merge_base:
        # merge-base が取れない場合はすべて upstream_only として扱う
        return {d: "upstream_only" for d in list_skill_dirs(skill_base)}

    result = {}
    for skill_dir in list_skill_dirs(skill_base):
        # ローカル変更: merge_base..HEAD
        local_diff = run_git(
            "diff", "--name-only", f"{merge_base}..HEAD", "--", skill_dir,
            check=False,
        )
        has_local = bool(
            local_diff.returncode == 0 and local_diff.stdout.strip()
        )

        # uncommitted な変更もチェック（unstaged + staged）
        if not has_local:
            for diff_args in [
                ("diff", "--name-only", "--", skill_dir),           # unstaged
                ("diff", "--cached", "--name-only", "--", skill_dir),  # staged
            ]:
                r = run_git(*diff_args, check=False)
                if r.returncode == 0 and r.stdout.strip():
                    has_local = True
                    break

        # upstream 変更: merge_base..upstream/main
        upstream_diff = run_git(
            "diff", "--name-only", f"{merge_base}..{ref}", "--", skill_dir,
            check=False,
        )
        has_upstream = bool(
            upstream_diff.returncode == 0 and upstream_diff.stdout.strip()
        )

        if has_local and has_upstream:
            result[skill_dir] = "conflict"
        elif has_upstream:
            result[skill_dir] = "upstream_only"
        elif has_local:
            result[skill_dir] = "local_only"
        else:
            result[skill_dir] = "unchanged"

    return result


def show_skill_diff(skill_dir: str) -> str:
    """スキルディレクトリの upstream との diff を表示用に返す。"""
    ref = f"{UPSTREAM_REMOTE}/{UPSTREAM_BRANCH}"
    result = run_git("diff", f"HEAD..{ref}", "--", skill_dir, check=False)
    if result.returncode == 0:
        return result.stdout
    return "(差分を取得できませんでした)"


def resolve_skill_conflicts(
    conflicts: dict[str, str],
    strategy: str = "ask",
) -> dict[str, str]:
    """コンフリクトスキルに対するユーザー選択を返す。

    strategy:
        ask — stdin で対話的に選択
        keep-mine — 全て自分のバージョンを維持
        take-upstream — 全て upstream を採用
        keep-both — 全て両方保持

    Returns:
        {skill_dir: "keep_mine"|"take_upstream"|"keep_both"}
    """
    valid = {"ask", "keep-mine", "take-upstream", "keep-both"}
    if strategy not in valid:
        raise ValueError(f"Invalid strategy: {strategy!r}. Must be one of {valid}")

    if strategy != "ask":
        decision = strategy.replace("-", "_")
        return {s: decision for s in conflicts}

    decisions = {}
    for skill_dir in sorted(conflicts):
        skill_name = skill_dir.rstrip("/").split("/")[-1]
        print(f"\n{'=' * 50}")
        print(f"  コンフリクト: {skill_name}")
        print(f"  パス: {skill_dir}")
        print(f"{'=' * 50}")
        print("  ローカルと upstream の両方で変更があります。")
        print()
        print("  a) keep_mine     — 自分のバージョンを維持（upstream をスキップ）")
        print("  b) take_upstream — upstream を採用（自分のを backup）")
        print("  c) keep_both     — 両方保持（自分のを -custom にリネーム）")
        print("  d) show_diff     — diff を表示")
        print()

        while True:
            try:
                choice = input(f"  [{skill_name}] 選択 (a/b/c/d): ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\n中断されました。残りのスキルは keep_mine として扱います。")
                for remaining in sorted(conflicts):
                    if remaining not in decisions:
                        decisions[remaining] = "keep_mine"
                return decisions

            if choice == "a":
                decisions[skill_dir] = "keep_mine"
                print(f"  → {skill_name}: 自分のバージョンを維持")
                break
            elif choice == "b":
                decisions[skill_dir] = "take_upstream"
                print(f"  → {skill_name}: upstream を採用（バックアップ作成）")
                break
            elif choice == "c":
                decisions[skill_dir] = "keep_both"
                print(f"  → {skill_name}: 両方保持")
                break
            elif choice == "d":
                diff_text = show_skill_diff(skill_dir)
                print(diff_text[:3000])
                if len(diff_text) > 3000:
                    print(f"  ... (差分が長いため省略。全 {len(diff_text)} 文字)")
            else:
                print("  a, b, c, d のいずれかを入力してください。")

    return decisions


def apply_skill_decisions(
    decisions: dict[str, str],
    timestamp: str,
) -> tuple[list[str], list[str]]:
    """ユーザー決定を適用する。

    Returns:
        (updated_skills, skipped_skills)
    """
    ref = f"{UPSTREAM_REMOTE}/{UPSTREAM_BRANCH}"
    updated = []
    skipped = []

    for skill_dir, decision in sorted(decisions.items()):
        skill_name = skill_dir.rstrip("/").split("/")[-1]

        if decision == "keep_mine":
            skipped.append(skill_dir)
            logger.info("スキップ: %s（ローカルバージョンを維持）", skill_name)

        elif decision == "take_upstream":
            # バックアップ作成
            backup_dest = BACKUP_BASE_DIR / timestamp / skill_dir
            src = PROJECT_ROOT / skill_dir
            if src.is_dir():
                backup_dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(src, backup_dest)
                logger.info("バックアップ: %s → %s", skill_name, backup_dest)

            # upstream からチェックアウト
            result = run_git("checkout", ref, "--", skill_dir, check=False)
            if result.returncode == 0:
                updated.append(skill_dir)
                logger.info("更新: %s（upstream を採用）", skill_name)
            else:
                skipped.append(skill_dir)
                logger.error("更新失敗: %s — %s", skill_name, result.stderr.strip())

        elif decision == "keep_both":
            # 自分のバージョンをリネーム
            src = PROJECT_ROOT / skill_dir.rstrip("/")
            custom_name = f"{skill_name}-custom-{timestamp}"
            dst = src.parent / custom_name
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
                logger.info("コピー: %s → %s", skill_name, custom_name)

            # upstream からチェックアウト
            result = run_git("checkout", ref, "--", skill_dir, check=False)
            if result.returncode == 0:
                updated.append(skill_dir)
                logger.info("更新: %s（upstream を採用、カスタム版は %s）", skill_name, custom_name)
            else:
                skipped.append(skill_dir)
                logger.error("更新失敗: %s — %s", skill_name, result.stderr.strip())

    return updated, skipped


def checkout_content_paths(paths: list[str]) -> tuple[bool, list[str]]:
    """指定パスを upstream/main から強制チェックアウト。

    checkout_content() のパス指定版。
    """
    ref = f"{UPSTREAM_REMOTE}/{UPSTREAM_BRANCH}"

    success_count = 0
    skipped = []
    failed = []
    for path in paths:
        result = run_git("checkout", ref, "--", path, check=False)
        if result.returncode == 0:
            success_count += 1
        else:
            stderr = result.stderr.strip()
            if "did not match any" in stderr or "pathspec" in stderr:
                skipped.append(path)
            else:
                failed.append(path)
                logger.error("パス '%s' のチェックアウトに失敗: %s", path, stderr)

    if success_count == 0:
        return False, failed

    return len(failed) == 0, failed


def update_skills(
    skill_check: bool = True,
    skill_strategy: str = "ask",
    timestamp: str | None = None,
) -> tuple[list[str], list[str], dict[str, str]]:
    """スキルパスの更新処理。

    Args:
        skill_check: True ならコンフリクト検出、False なら従来の強制上書き
        skill_strategy: コンフリクト時の戦略 (ask|keep-mine|take-upstream|keep-both)
        timestamp: バックアップ用タイムスタンプ

    Returns:
        (updated_skills, skipped_skills, classifications)
    """
    if not timestamp:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")

    if not skill_check:
        # 従来の強制上書き
        success, failed = checkout_content_paths(SKILL_PATHS)
        return (SKILL_PATHS if success else [], failed, {})

    merge_base = get_merge_base()
    all_updated = []
    all_skipped = []
    all_classifications = {}

    for skill_base in SKILL_PATHS:
        classifications = classify_skill_changes(skill_base, merge_base)
        all_classifications.update(classifications)

        # unchanged / local_only はスキップ
        # upstream_only は自動更新
        auto_update = [
            s for s, c in classifications.items() if c == "upstream_only"
        ]
        if auto_update:
            for skill_dir in auto_update:
                result = run_git(
                    "checkout", f"{UPSTREAM_REMOTE}/{UPSTREAM_BRANCH}",
                    "--", skill_dir, check=False,
                )
                if result.returncode == 0:
                    all_updated.append(skill_dir)
                    skill_name = skill_dir.rstrip("/").split("/")[-1]
                    logger.info("自動更新: %s", skill_name)

        # conflict はユーザー判断
        conflicts = {
            s: c for s, c in classifications.items() if c == "conflict"
        }
        if conflicts:
            print(f"\n📋 スキルコンフリクト検出: {len(conflicts)} 件")
            decisions = resolve_skill_conflicts(conflicts, skill_strategy)
            updated, skipped = apply_skill_decisions(decisions, timestamp)
            all_updated.extend(updated)
            all_skipped.extend(skipped)

    return all_updated, all_skipped, all_classifications


def delete_removed_files(deleted_files: list[str]) -> int:
    """upstream で削除されたファイルをローカルからも削除。"""
    count = 0
    for f in deleted_files:
        filepath = PROJECT_ROOT / f
        if filepath.exists():
            filepath.unlink()
            logger.info("削除: %s", f)
            count += 1
    return count


def update_dependencies() -> None:
    """requirements.txt が更新された場合、pip install を実行。"""
    req_file = PROJECT_ROOT / "requirements.txt"
    if not req_file.exists():
        return

    if not shutil.which("uv"):
        logger.info("uv が見つかりません。pip install はスキップします。")
        logger.info("手動で実行してください: uv pip install -r requirements.txt")
        return

    logger.info("依存パッケージを更新中...")
    result = subprocess.run(
        ["uv", "pip", "install", "-r", str(req_file), "-q"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        logger.info("依存パッケージの更新完了")
    else:
        logger.warning("uv pip install に失敗: %s", result.stderr.strip()[:200])
        logger.info("手動で実行してください: uv pip install -r requirements.txt")


def load_update_log() -> list[dict]:
    """更新ログを読み込み。"""
    if UPDATE_LOG_FILE.exists():
        try:
            return json.loads(UPDATE_LOG_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_update_log(log: list[dict]) -> None:
    """更新ログを保存。"""
    UPDATE_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    UPDATE_LOG_FILE.write_text(
        json.dumps(log, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def record_update(
    timestamp: str,
    before_commit: str | None,
    after_commit: str | None,
    changed_files: list[str],
    backup_dir: Path | None,
) -> None:
    """更新ログにエントリを追加。"""
    log = load_update_log()
    log.append({
        "timestamp": timestamp,
        "before_commit": before_commit,
        "after_commit": after_commit,
        "files_updated": len(changed_files),
        "changed_files": changed_files[:50],  # 最大50件
        "backup_dir": str(backup_dir) if backup_dir else None,
    })
    # 最新100件のみ保持
    save_update_log(log[-100:])


# --- メインコマンド ---


def cmd_setup(repo_url: str | None = None) -> int:
    """初回セットアップ: upstream リモートを追加。

    ユーザーは自身の GitHub 認証（gh auth login 済み）でアクセスする。
    リポジトリへのコラボレーター招待を事前に受諾していること。
    """
    if not is_git_repo():
        print("git リポジトリではありません。先にリポジトリをクローンしてください。")
        return 1

    if has_upstream():
        current_url = get_upstream_url()
        logger.info("upstream は既に設定されています: %s", _sanitize_url(current_url or ""))
        logger.info("URL を変更する場合は先に削除してください: git remote remove upstream")
        return 1

    # リポジトリ URL（デフォルト: 教材コンテンツリポ）
    url = repo_url or DEFAULT_UPSTREAM_URL

    # gh auth で認証済みか確認
    gh_check = subprocess.run(
        ["gh", "auth", "status"], capture_output=True, text=True, check=False,
    )
    if gh_check.returncode != 0:
        print("⚠️  GitHub CLI の認証が必要です。以下を実行してください:")
        print("  gh auth login")
        return 1

    # gh auth setup-git で git credential helper を設定
    subprocess.run(
        ["gh", "auth", "setup-git"], capture_output=True, text=True, check=False,
    )

    run_git("remote", "add", UPSTREAM_REMOTE, url)
    logger.info("upstream リモートを追加しました: %s", url)

    # 初回 fetch + checkout
    if not fetch_upstream():
        return 1

    success, failed = checkout_content()
    if failed:
        logger.warning("一部のコンテンツ取得に失敗: %s", ", ".join(failed))
    if not success and not failed:
        # 全パスが存在しない（空のリポジトリ等）
        logger.error("コンテンツの取得に失敗しました")
        return 1

    # ユーザー空間ディレクトリの作成
    for d in ["output", "work", "work/exercises"]:
        (PROJECT_ROOT / d).mkdir(parents=True, exist_ok=True)

    # .env.example → .env（存在しない場合のみ）
    env_example = PROJECT_ROOT / ".env.example"
    env_file = PROJECT_ROOT / ".env"
    if env_example.exists() and not env_file.exists():
        shutil.copy2(env_example, env_file)
        logger.info(".env.example を .env にコピーしました")

    logger.info("セットアップ完了！")
    return 0


def cmd_status() -> int:
    """現在の状態を表示。"""
    if not is_git_repo():
        print("git リポジトリではありません。--setup で初期化してください。")
        return 1

    if not has_upstream():
        print("upstream が設定されていません。--setup で設定してください。")
        return 1

    current = get_current_commit()
    print(f"現在のコミット: {current[:8] if current else '不明'}")

    # fetch して差分確認
    if not fetch_upstream():
        return 1

    upstream = get_upstream_commit()
    print(f"upstream 最新:  {upstream[:8] if upstream else '不明'}")

    if current == upstream:
        print("\n✅ 最新の状態です。更新はありません。")
        return 0

    changed = get_changed_files()
    new_files = get_new_files_in_upstream()
    deleted = get_deleted_files_in_upstream()

    print(f"\n更新可能なファイル: {len(changed)} 件")
    if new_files:
        print(f"  新規追加: {len(new_files)} 件")
    if deleted:
        print(f"  削除予定: {len(deleted)} 件")

    # 最新の更新ログ
    log = load_update_log()
    if log:
        last = log[-1]
        print(f"\n最終更新: {last['timestamp']} ({last['files_updated']} ファイル)")

    return 0


def cmd_dry_run() -> int:
    """変更内容を事前確認（実際の更新は行わない）。"""
    if not has_upstream():
        print("upstream が設定されていません。--setup で設定してください。")
        return 1

    if not fetch_upstream():
        return 1

    changed = get_changed_files()
    new_files = get_new_files_in_upstream()
    deleted = get_deleted_files_in_upstream()

    if not changed and not deleted:
        print("✅ 更新はありません。最新の状態です。")
        return 0

    print("=" * 60)
    print("📋 更新プレビュー（ドライラン）")
    print("=" * 60)

    if changed:
        modified = [f for f in changed if f not in new_files]
        if modified:
            print(f"\n📝 変更されるファイル ({len(modified)} 件):")
            for f in modified[:30]:
                print(f"  M  {f}")
            if len(modified) > 30:
                print(f"  ... 他 {len(modified) - 30} 件")

        if new_files:
            print(f"\n➕ 新規追加されるファイル ({len(new_files)} 件):")
            for f in new_files[:20]:
                print(f"  A  {f}")
            if len(new_files) > 20:
                print(f"  ... 他 {len(new_files) - 20} 件")

    if deleted:
        print(f"\n🗑  削除されるファイル ({len(deleted)} 件):")
        for f in deleted[:10]:
            print(f"  D  {f}")
        if len(deleted) > 10:
            print(f"  ... 他 {len(deleted) - 10} 件")

    # バックアップ対象
    backup_targets = []
    for pattern in BACKUP_BEFORE_UPDATE:
        backup_targets.extend(f for f in changed if f.startswith(pattern))
    if backup_targets:
        print(f"\n💾 バックアップ対象 ({len(backup_targets)} 件):")
        for f in backup_targets[:10]:
            print(f"  B  {f}")

    print("\n" + "=" * 60)
    print("実行するには: uv run python tools/content_updater.py")
    print("=" * 60)
    return 0


def cmd_update(
    skill_check: bool = True,
    skill_strategy: str = "ask",
) -> int:
    """メイン更新処理。

    Args:
        skill_check: スキルコンフリクト検出を有効化（デフォルト: True）
        skill_strategy: コンフリクト時の戦略 (ask|keep-mine|take-upstream|keep-both)
    """
    if not is_git_repo():
        print("git リポジトリではありません。--setup で初期化してください。")
        return 1

    if not has_upstream():
        print("upstream が設定されていません。--setup で設定してください。")
        return 1

    # 1. fetch
    if not fetch_upstream():
        return 1

    # 2. 差分確認
    before_commit = get_current_commit()
    changed = get_changed_files()
    deleted = get_deleted_files_in_upstream()

    if not changed and not deleted:
        print("✅ 最新の状態です。更新はありません。")
        return 0

    print(f"更新対象: {len(changed)} ファイル変更, {len(deleted)} ファイル削除")

    # 3. バックアップ
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    backup_dir = backup_files(changed, timestamp)

    # 4. コンテンツ更新（スキル以外を強制チェックアウト）
    if skill_check:
        success, failed = checkout_content_paths(NON_SKILL_CONTENT_PATHS)
    else:
        success, failed = checkout_content()
    if not success:
        if failed:
            print(f"⚠️  一部のコンテンツ更新に失敗しました: {', '.join(failed)}")
            print("ロールバックするには: uv run python tools/content_updater.py --rollback")
        return 1

    # 5. スキルの更新（コンフリクト検出付き）
    if skill_check:
        updated_skills, skipped_skills, classifications = update_skills(
            skill_check=True,
            skill_strategy=skill_strategy,
            timestamp=timestamp,
        )
        if classifications:
            conflict_count = sum(1 for c in classifications.values() if c == "conflict")
            auto_count = sum(1 for c in classifications.values() if c == "upstream_only")
            local_count = sum(1 for c in classifications.values() if c == "local_only")
            if auto_count or conflict_count or local_count:
                print(f"\n📊 スキル更新: {auto_count} 自動更新, "
                      f"{len(skipped_skills)} スキップ, "
                      f"{conflict_count} コンフリクト処理済み")

    # 6. 削除されたファイルの処理
    if deleted:
        delete_count = delete_removed_files(deleted)
        if delete_count:
            logger.info("%d ファイルを削除しました", delete_count)

    # 7. requirements.txt が変更された場合、pip install
    if any(f == "requirements.txt" for f in changed):
        update_dependencies()

    # 8. 更新ログ記録
    after_commit = get_upstream_commit()
    record_update(timestamp, before_commit, after_commit, changed, backup_dir)

    # 9. 結果表示
    print()
    print("=" * 60)
    print("✅ 教材の更新が完了しました！")
    print("=" * 60)
    print(f"  更新ファイル数: {len(changed)}")
    if deleted:
        print(f"  削除ファイル数: {len(deleted)}")
    if backup_dir:
        print(f"  バックアップ:   {backup_dir}")
    print()
    return 0


def cmd_rollback() -> int:
    """直前の更新をロールバック。"""
    log = load_update_log()
    if not log:
        print("更新ログがありません。ロールバックできません。")
        return 1

    last = log[-1]
    before_commit = last.get("before_commit")
    if not before_commit:
        print("ロールバック先のコミットが不明です。")
        return 1

    print(f"ロールバック先: {before_commit[:8]}")
    print(f"更新日時:       {last['timestamp']}")
    print(f"変更ファイル数: {last['files_updated']}")

    # コンテンツパスを before_commit の状態に戻す
    for path in CONTENT_PATHS:
        result = run_git("checkout", before_commit, "--", path, check=False)
        if result.returncode != 0:
            stderr = result.stderr.strip()
            if "did not match any" not in stderr and "pathspec" not in stderr:
                logger.warning("ロールバック失敗 (%s): %s", path, stderr)

    # バックアップがあれば復元
    backup_dir_str = last.get("backup_dir")
    if backup_dir_str:
        backup_dir = Path(backup_dir_str)
        if backup_dir.exists():
            for src in backup_dir.rglob("*"):
                if src.is_file():
                    rel = src.relative_to(backup_dir)
                    dst = PROJECT_ROOT / rel
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
            logger.info("バックアップから復元しました: %s", backup_dir)

    # ロールバック記録を追加（最後のエントリは保持、typeをrollbackに変更）
    rollback_entry = log.pop()
    rollback_entry["type"] = "rolled_back"
    log.append(rollback_entry)
    save_update_log(log)

    print("\n✅ ロールバック完了")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="教材コンテンツの差分更新ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--setup",
        nargs="?",
        const="",
        metavar="REPO_URL",
        help="初回セットアップ: upstream リモートを追加。gh auth login 済みの認証を使用",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="変更内容を事前確認（更新は実行しない）",
    )
    group.add_argument(
        "--rollback",
        action="store_true",
        help="直前の更新をロールバック",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="現在のバージョンと更新状況を表示",
    )

    # スキルコンフリクト処理オプション（更新時のみ有効）
    parser.add_argument(
        "--no-skill-check",
        action="store_true",
        default=False,
        help="スキルコンフリクト検出を無効化（デフォルト: 有効）",
    )
    parser.add_argument(
        "--skill-strategy",
        choices=["ask", "keep-mine", "take-upstream", "keep-both"],
        default="ask",
        help="スキルコンフリクト時の戦略（デフォルト: ask）",
    )

    args = parser.parse_args()

    if args.setup is not None:
        return cmd_setup(args.setup or None)
    elif args.dry_run:
        return cmd_dry_run()
    elif args.rollback:
        return cmd_rollback()
    elif args.status:
        return cmd_status()
    else:
        return cmd_update(
            skill_check=not args.no_skill_check,
            skill_strategy=args.skill_strategy,
        )


if __name__ == "__main__":
    sys.exit(main())
