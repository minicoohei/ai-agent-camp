#!/usr/bin/env python3
"""スキル管理ツール - スキルの一覧表示・同期・更新・外部プラグイン管理を行うCLI。

サブコマンド:
    list            ローカル/グローバルのスキル一覧と差分を表示
    plugin-list     外部プラグインレジストリからスキル一覧を表示
    plugin-install  外部プラグインからスキルをインストール
    plugin-update   インストール済み外部スキルを更新
    plugin-clean    プラグインキャッシュを削除
    sync-global     プロジェクトスキルを ~/.claude/skills/ にコピー
    sync-project    プロジェクトスキルを別プロジェクトにコピー
    update-upstream upstream から最新スキルを取り込み
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from log_utils import setup_logger

logger = setup_logger("skill_manager")

# --- 定数 ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROJECT_SKILLS_DIR = PROJECT_ROOT / "skills"
GLOBAL_SKILLS_DIR = Path.home() / ".claude" / "skills"
UPSTREAM_URL = "https://github.com/minicoohei/ai-agent-camp.git/"
REGISTRY_FILE = PROJECT_ROOT / "external-plugins.yaml"
CACHE_DIR = Path.home() / ".cache" / "aiagent-base" / "plugins"


# --- ユーティリティ ---


def parse_skill_frontmatter(skill_dir: Path) -> dict:
    """SKILL.md のフロントマターから name と description を取得する。"""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return {"name": skill_dir.name, "description": "(SKILL.md なし)"}

    try:
        text = skill_md.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return {"name": skill_dir.name, "description": f"(読み込み失敗: {exc})"}
    # --- で囲まれたフロントマターを正規表現でパース
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {"name": skill_dir.name, "description": "(フロントマター未検出)"}

    fm = m.group(1)
    name = skill_dir.name
    description = ""
    source = ""
    for line in fm.splitlines():
        kv = line.split(":", 1)
        if len(kv) == 2:
            key = kv[0].strip()
            val = kv[1].strip()
            if key == "name":
                name = val
            elif key == "description":
                description = val
            elif key == "source":
                source = val
    return {"name": name, "description": description, "source": source}


def list_skills(skills_dir: Path) -> list[dict]:
    """指定ディレクトリ内のスキルを一覧取得する。"""
    if not skills_dir.is_dir():
        return []
    result = []
    for d in sorted(skills_dir.iterdir()):
        if d.is_dir() and not d.name.startswith("."):
            info = parse_skill_frontmatter(d)
            info["dir"] = d
            result.append(info)
    return result


def print_skills_table(skills: list[dict], label: str) -> None:
    """スキル一覧をテーブル形式で表示する。"""
    print(f"\n{'=' * 60}")
    print(f"  {label} ({len(skills)} 個)")
    print(f"{'=' * 60}")
    if not skills:
        print("  (なし)")
        return
    # 列幅計算
    max_name = max(len(s["name"]) for s in skills)
    max_name = max(max_name, 6)  # 最低幅
    for s in skills:
        desc = s["description"][:50] + "..." if len(s["description"]) > 50 else s["description"]
        source = s.get("source", "")
        ext_mark = " (ext)" if source.startswith("github.com/") else ""
        print(f"  {s['name']:<{max_name}}  {desc}{ext_mark}")


# --- サブコマンド実装 ---


def cmd_list(args: argparse.Namespace) -> None:
    """ローカル/グローバルのスキル一覧 + 差分を表示する。"""
    project_skills = list_skills(PROJECT_SKILLS_DIR)
    global_skills = list_skills(GLOBAL_SKILLS_DIR)

    print_skills_table(project_skills, f"プロジェクトスキル ({PROJECT_SKILLS_DIR})")
    print_skills_table(global_skills, f"グローバルスキル ({GLOBAL_SKILLS_DIR})")

    # 差分
    proj_names = {s["name"] for s in project_skills}
    glob_names = {s["name"] for s in global_skills}

    only_project = sorted(proj_names - glob_names)
    only_global = sorted(glob_names - proj_names)

    if only_project or only_global:
        print(f"\n{'=' * 60}")
        print("  差分")
        print(f"{'=' * 60}")
        if only_project:
            print(f"  プロジェクトのみ: {', '.join(only_project)}")
        if only_global:
            print(f"  グローバルのみ:   {', '.join(only_global)}")
    else:
        print("\n  差分なし（プロジェクトとグローバルは同一セット）")
    print()


def cmd_plugin_guide(args: argparse.Namespace) -> None:
    """anthropics/skills プラグイン導入手順を表示する。"""
    guide = """\
============================================================
  anthropics/skills プラグイン導入ガイド
============================================================

anthropics/skills リポジトリには Claude Code 公式のスキルプラグインが
公開されています。以下の手順で導入できます。

1. リポジトリを確認
   https://github.com/anthropics/skills

2. 必要なスキルをダウンロード
   ────────────────────────────────────────
   # リポジトリをクローン
   git clone https://github.com/anthropics/skills.git /tmp/anthropics-skills

   # 必要なスキルをプロジェクトにコピー
   cp -r /tmp/anthropics-skills/<skill-name> .claude/skills/
   ────────────────────────────────────────

3. グローバルにインストール（全プロジェクトで利用）
   ────────────────────────────────────────
   mkdir -p ~/.claude/skills
   cp -r /tmp/anthropics-skills/<skill-name> ~/.claude/skills/
   ────────────────────────────────────────

4. 動作確認
   ────────────────────────────────────────
   uv run python tools/skill_manager.py list
   ────────────────────────────────────────

注意:
  - anthropics/skills の各スキルには個別の README.md があります
  - 依存パッケージがある場合は各スキルの指示に従ってください
  - 公式スキルの更新は git pull で取得できます
"""
    print(guide)


def cmd_sync_global(args: argparse.Namespace) -> None:
    """プロジェクトスキルを ~/.claude/skills/ にコピーする。"""
    target_dir = Path(args.target) if args.target else GLOBAL_SKILLS_DIR
    _sync_skills(PROJECT_SKILLS_DIR, target_dir, args.skills, args.force)


def cmd_sync_project(args: argparse.Namespace) -> None:
    """プロジェクトスキルを別プロジェクトの .claude/skills/ にコピーする。"""
    project_path = Path(args.project).resolve()
    if not project_path.is_dir():
        logger.error("プロジェクトディレクトリが見つかりません: %s", project_path)
        sys.exit(1)
    target_dir = project_path / ".claude" / "skills"
    _sync_skills(PROJECT_SKILLS_DIR, target_dir, args.skills, args.force)


def _sync_skills(
    src_dir: Path,
    dst_dir: Path,
    skill_names: list[str] | None,
    force: bool,
) -> None:
    """スキルを src_dir から dst_dir にコピーする共通処理。"""
    if not src_dir.is_dir():
        logger.error("ソースディレクトリが見つかりません: %s", src_dir)
        sys.exit(1)

    # ディレクトリ名 / フロントマター名 → Path のマッピングを構築
    all_dirs = sorted(
        d for d in src_dir.iterdir() if d.is_dir() and not d.name.startswith(".")
    )
    name_to_dir: dict[str, Path] = {}
    dir_names = {d.name for d in all_dirs}
    for d in all_dirs:
        name_to_dir[d.name] = d
    for d in all_dirs:
        fm_name = parse_skill_frontmatter(d).get("name", d.name)
        if fm_name != d.name and fm_name not in dir_names:
            name_to_dir[fm_name] = d

    # コピー対象の決定
    if skill_names:
        dirs_to_copy = []
        for name in skill_names:
            resolved = name_to_dir.get(name)
            if resolved is None:
                logger.warning("スキル '%s' が見つかりません。スキップします。", name)
            elif resolved not in dirs_to_copy:
                dirs_to_copy.append(resolved)
    else:
        dirs_to_copy = all_dirs

    if not dirs_to_copy:
        print("コピー対象のスキルがありません。")
        return

    # コピー先ディレクトリ作成
    dst_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    skipped = 0
    for skill_dir in dirs_to_copy:
        dest = dst_dir / skill_dir.name
        if dest.exists() and not force:
            print(f"  スキップ: {skill_dir.name} (既存 — --force で上書き)")
            skipped += 1
            continue
        try:
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(skill_dir, dest)
        except OSError as exc:
            logger.error("%s のコピーに失敗しました: %s", skill_dir.name, exc)
            skipped += 1
            continue
        print(f"  コピー:   {skill_dir.name} → {dest}")
        copied += 1

    print(f"\n完了: {copied} 個コピー, {skipped} 個スキップ (コピー先: {dst_dir})")


# --- 外部プラグイン管理 ---


def load_registry() -> dict:
    """external-plugins.yaml をロードして返す。"""
    if not REGISTRY_FILE.exists():
        logger.error("レジストリファイルが見つかりません: %s", REGISTRY_FILE)
        sys.exit(1)
    try:
        with open(REGISTRY_FILE, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except (OSError, yaml.YAMLError) as exc:
        logger.error("レジストリの読み込みに失敗: %s", exc)
        sys.exit(1)
    if not isinstance(data, dict) or "plugins" not in data:
        logger.error("レジストリの形式が不正です。")
        sys.exit(1)
    return data


def resolve_skill_path(
    skill_pattern: str,
    skill_name: str,
    plugin: str = "",
    domain: str = "",
) -> str:
    """skill_pattern のプレースホルダーを解決してリポジトリ内のスキルパスを返す。"""
    return (
        skill_pattern.replace("{skill}", skill_name)
        .replace("{plugin}", plugin)
        .replace("{domain}", domain)
    )


def _get_recommended_skills(plugin_config: dict) -> list[tuple[str, str, str]]:
    """推奨スキルを (skill_name, plugin, domain) のリストで返す。"""
    skills = []
    for group in plugin_config.get("recommended", []):
        plugin_name = group.get("plugin", "")
        domain_name = group.get("domain", "")
        for skill_name in group.get("skills", []):
            skills.append((skill_name, plugin_name, domain_name))
    return skills


def _get_all_skills(plugin_config: dict) -> list[tuple[str, str, str]]:
    """推奨 + オプションスキルを全て返す。"""
    skills = _get_recommended_skills(plugin_config)
    for group in plugin_config.get("optional", []):
        plugin_name = group.get("plugin", "")
        domain_name = group.get("domain", "")
        for skill_name in group.get("skills", []):
            skills.append((skill_name, plugin_name, domain_name))
    return skills


def _verify_commit_sha(cache_path: Path, expected_sha: str, repo: str) -> bool:
    """クローン/フェッチ後のHEADコミットSHAを検証する。"""
    git = _resolve_git()
    ret = subprocess.run(
        [git, "rev-parse", "HEAD"],
        capture_output=True, text=True, cwd=cache_path,
    )
    if ret.returncode != 0:
        logger.error("%s のコミットSHA取得に失敗しました", repo)
        return False
    actual_sha = ret.stdout.strip()
    if not actual_sha.startswith(expected_sha[:12]):
        logger.error(
            "%s のコミットSHA不一致: expected=%s, actual=%s (サプライチェーン攻撃の可能性)",
            repo, expected_sha[:12], actual_sha[:12],
        )
        return False
    return True


def _ensure_repo_cached(repo: str, ref: str, force_update: bool = False,
                        pinned_sha: str | None = None) -> Path | None:
    """リポジトリの shallow clone をキャッシュに作成/更新する。失敗時は None。"""
    git = _resolve_git()
    repo_name = repo.replace("/", "--")
    cache_path = CACHE_DIR / repo_name

    if force_update and cache_path.exists():
        shutil.rmtree(cache_path)

    if not cache_path.exists():
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        url = f"https://github.com/{repo}.git"
        print(f"  クローン中: {repo} → {cache_path.name}")
        ret = subprocess.run(
            [git, "clone", "--depth", "1", "--branch", ref, url, str(cache_path)],
            capture_output=True,
            text=True,
        )
        if ret.returncode != 0:
            logger.error("%s のクローンに失敗しました: %s", repo, ret.stderr.strip())
            return None
    else:
        # 既存キャッシュを更新
        print(f"  更新中: {repo}")
        subprocess.run(
            [git, "fetch", "--depth", "1", "origin", ref],
            capture_output=True,
            text=True,
            cwd=cache_path,
        )
        subprocess.run(
            [git, "checkout", "FETCH_HEAD"],
            capture_output=True,
            text=True,
            cwd=cache_path,
        )

    # pinned_sha が指定されている場合、コミットSHAを検証
    if pinned_sha and not _verify_commit_sha(cache_path, pinned_sha, repo):
        logger.warning(
            "%s: pinned_sha と不一致。external-plugins.yaml の更新が必要です。"
            " `uv run python tools/skill_manager.py plugin-update` で最新SHAに更新してください。",
            repo,
        )

    return cache_path


def _inject_source_metadata(skill_dir: Path, repo: str, ref: str) -> None:
    """SKILL.md のフロントマターに source フィールドを追加/更新する。"""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return

    text = skill_md.read_text(encoding="utf-8")
    source_value = f"github.com/{repo}@{ref}"

    m = re.match(r"^(---\s*\n)(.*?)(\n---)", text, re.DOTALL)
    if m:
        fm_content = m.group(2)
        # 既に source: がある場合は置換
        if re.search(r"^source:", fm_content, re.MULTILINE):
            fm_content = re.sub(
                r"^source:.*$", f"source: {source_value}", fm_content, flags=re.MULTILINE
            )
        else:
            fm_content += f"\nsource: {source_value}"
        text = m.group(1) + fm_content + m.group(3) + text[m.end():]
    else:
        # フロントマターがない場合は先頭に追加
        text = f"---\nsource: {source_value}\n---\n{text}"

    skill_md.write_text(text, encoding="utf-8")


def _copy_skill_from_cache(
    cache_repo_dir: Path,
    skill_rel_path: str,
    dest_name: str,
    force: bool = False,
) -> bool:
    """キャッシュからスキルを .claude/skills/ にコピーする。成功時 True。"""
    src = cache_repo_dir / skill_rel_path
    if not src.is_dir():
        logger.warning("スキルパスが見つかりません: %s", skill_rel_path)
        return False
    skill_md = src / "SKILL.md"
    if not skill_md.exists():
        logger.warning("SKILL.md がありません: %s", skill_rel_path)
        return False

    dest = PROJECT_SKILLS_DIR / dest_name
    if dest.exists() and not force:
        print(f"  スキップ: {dest_name} (既存 — --force で上書き)")
        return False

    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    return True


def cmd_plugin_list(args: argparse.Namespace) -> None:
    """外部プラグインレジストリからスキル一覧を表示する。"""
    registry = load_registry()
    plugins = registry.get("plugins", {})

    # インストール済みスキルの source を収集
    installed_sources: dict[str, str] = {}
    for skill_info in list_skills(PROJECT_SKILLS_DIR):
        src = skill_info.get("source", "")
        if src:
            installed_sources[skill_info["name"]] = src

    print(f"\n{'=' * 70}")
    print("  外部プラグインレジストリ")
    print(f"{'=' * 70}")

    total_recommended = 0
    for plugin_key, plugin_config in plugins.items():
        repo = plugin_config.get("repo", "")
        desc = plugin_config.get("description", "")
        recommended = _get_recommended_skills(plugin_config)
        total_recommended += len(recommended)

        print(f"\n  {plugin_key}")
        print(f"    リポジトリ: github.com/{repo}")
        print(f"    説明:       {desc}")
        print(f"    推奨スキル: {len(recommended)} 個")

        if getattr(args, "verbose", False):
            all_skills = _get_all_skills(plugin_config)
            for skill_name, plugin_name, domain_name in all_skills:
                is_recommended = (skill_name, plugin_name, domain_name) in recommended
                tag = "[推奨]" if is_recommended else "[任意]"
                # インストール状態チェック
                installed = skill_name in installed_sources
                status = "✓" if installed else " "
                print(f"      {status} {tag} {skill_name}")

    print(f"\n{'=' * 70}")
    print(f"  合計: {len(plugins)} プラグイン, {total_recommended} 推奨スキル")
    print(f"{'=' * 70}\n")


def cmd_plugin_install(args: argparse.Namespace) -> None:
    """外部プラグインからスキルをインストールする。"""
    registry = load_registry()
    plugins = registry.get("plugins", {})

    # 対象プラグインの決定
    if args.plugin:
        if args.plugin not in plugins:
            logger.error("プラグイン '%s' がレジストリにありません。利用可能: %s", args.plugin, ', '.join(plugins.keys()))
            sys.exit(1)
        target_plugins = {args.plugin: plugins[args.plugin]}
    else:
        target_plugins = plugins

    installed = 0
    skipped = 0

    for plugin_key, plugin_config in target_plugins.items():
        repo = plugin_config["repo"]
        ref = plugin_config.get("ref", "main")
        pattern = plugin_config["skill_pattern"]

        # インストール対象スキルの決定
        if args.skill:
            # --skill 指定: 全スキルから名前で検索
            all_skills = _get_all_skills(plugin_config)
            target_skills = [
                (name, plugin_name, domain_name)
                for name, plugin_name, domain_name in all_skills
                if name in args.skill
            ]
            if not target_skills:
                print(f"  警告: プラグイン '{plugin_key}' に指定スキルが見つかりません")
                continue
        elif args.all_recommended:
            target_skills = _get_recommended_skills(plugin_config)
        else:
            # デフォルト: 推奨スキルのみ
            target_skills = _get_recommended_skills(plugin_config)

        if not target_skills:
            continue

        print(f"\n--- {plugin_key} ({repo}) ---")
        pinned_sha = plugin_config.get("pinned_sha")
        cache_dir = _ensure_repo_cached(repo, ref, force_update=False, pinned_sha=pinned_sha)
        if cache_dir is None:
            skipped += len(target_skills)
            continue

        for skill_name, plugin_name, domain_name in target_skills:
            skill_path = resolve_skill_path(pattern, skill_name, plugin_name, domain_name)
            ok = _copy_skill_from_cache(cache_dir, skill_path, skill_name, args.force)
            if ok:
                _inject_source_metadata(
                    PROJECT_SKILLS_DIR / skill_name, repo, ref
                )
                print(f"  インストール: {skill_name}")
                installed += 1
            else:
                skipped += 1

    print(f"\n完了: {installed} 個インストール, {skipped} 個スキップ")


def cmd_plugin_update(args: argparse.Namespace) -> None:
    """インストール済みの外部スキルをレジストリのバージョンに更新する。"""
    registry = load_registry()
    plugins = registry.get("plugins", {})

    # インストール済み外部スキルを検索
    external_skills = []
    for skill_info in list_skills(PROJECT_SKILLS_DIR):
        source = skill_info.get("source", "")
        if source:
            external_skills.append(skill_info)

    if not external_skills:
        print("外部スキルがインストールされていません。")
        return

    print(f"インストール済み外部スキル: {len(external_skills)} 個")

    if getattr(args, "dry_run", False):
        for s in external_skills:
            print(f"  {s['name']}  (source: {s['source']})")
        print("\n--dry-run: 更新は実行されません。")
        return

    updated = 0
    for plugin_key, plugin_config in plugins.items():
        repo = plugin_config["repo"]
        ref = plugin_config.get("ref", "main")
        pattern = plugin_config["skill_pattern"]
        source_prefix = f"github.com/{repo}"

        # フィルタ: 対象プラグイン指定時
        if getattr(args, "plugin", None) and args.plugin != plugin_key:
            continue

        # このプラグイン由来のインストール済みスキルを検索
        matching = [s for s in external_skills if s["source"].startswith(source_prefix)]
        if not matching:
            continue

        print(f"\n--- {plugin_key} ({repo}) ---")
        pinned_sha = plugin_config.get("pinned_sha")
        cache_dir = _ensure_repo_cached(repo, ref, force_update=True, pinned_sha=pinned_sha)
        if cache_dir is None:
            continue

        all_skills = _get_all_skills(plugin_config)
        skill_map = {name: (name, p, d) for name, p, d in all_skills}

        for skill_info in matching:
            skill_name = skill_info["name"]
            if skill_name not in skill_map:
                print(f"  警告: {skill_name} のパスをレジストリから解決できません")
                continue
            _, plugin_name, domain_name = skill_map[skill_name]
            skill_path = resolve_skill_path(pattern, skill_name, plugin_name, domain_name)
            ok = _copy_skill_from_cache(cache_dir, skill_path, skill_name, force=True)
            if ok:
                _inject_source_metadata(
                    PROJECT_SKILLS_DIR / skill_name, repo, ref
                )
                print(f"  更新: {skill_name}")
                updated += 1

    print(f"\n完了: {updated} 個更新")


def cmd_plugin_clean(args: argparse.Namespace) -> None:
    """プラグインキャッシュディレクトリを削除する。"""
    if not CACHE_DIR.exists():
        print("キャッシュディレクトリが存在しません。")
        return
    size = sum(f.stat().st_size for f in CACHE_DIR.rglob("*") if f.is_file())
    size_mb = size / (1024 * 1024)
    shutil.rmtree(CACHE_DIR)
    print(f"キャッシュを削除しました: {CACHE_DIR} ({size_mb:.1f} MB)")


def _resolve_git() -> str:
    """git バイナリの絶対パスを解決する。見つからない場合は終了。"""
    git_path = shutil.which("git")
    if not git_path:
        logger.error("git が見つかりません。")
        sys.exit(1)
    return git_path


def cmd_update_upstream(args: argparse.Namespace) -> None:
    """upstream から最新のスキルを取り込む（git fetch + merge）。"""
    git = _resolve_git()

    # upstream の確認
    result = subprocess.run(
        [git, "remote"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    if result.returncode != 0:
        logger.error("git remote の取得に失敗しました: %s", result.stderr.strip())
        sys.exit(1)
    if "upstream" not in result.stdout.splitlines():
        print("upstream が未設定です。追加します...")
        ret = subprocess.run(
            [git, "remote", "add", "upstream", UPSTREAM_URL],
            cwd=PROJECT_ROOT,
        )
        if ret.returncode != 0:
            logger.error("upstream リモートの追加に失敗しました。")
            sys.exit(1)
        print(f"  upstream を追加しました: {UPSTREAM_URL}")

    # fetch
    print("\nupstream から最新を取得中...")
    ret = subprocess.run(
        [git, "fetch", "upstream"],
        cwd=PROJECT_ROOT,
    )
    if ret.returncode != 0:
        logger.error("git fetch upstream に失敗しました。")
        sys.exit(1)

    # 現在のブランチ名を取得
    result = subprocess.run(
        [git, "branch", "--show-current"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    current_branch = result.stdout.strip()
    if not current_branch:
        logger.error(
            "現在 detached HEAD 状態です。ブランチをチェックアウトしてから再実行してください。例: git checkout main"
        )
        sys.exit(1)
    print(f"現在のブランチ: {current_branch}")

    # merge
    print("upstream/main をマージ中...")
    ret = subprocess.run(
        [git, "merge", "upstream/main"],
        cwd=PROJECT_ROOT,
    )
    if ret.returncode != 0:
        logger.error(
            "マージでコンフリクトが発生しました。手動でコンフリクトを解決し、git add → git commit で完了してください。"
        )
        sys.exit(1)

    print("\n完了: upstream の最新スキル・教材を取り込みました。")


# --- エントリーポイント ---


def main() -> None:
    """CLI エントリーポイント。引数をパースしてサブコマンドを実行する。"""
    parser = argparse.ArgumentParser(
        description="スキル管理ツール — スキルの一覧表示・同期・更新",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--test", action="store_true", help="簡易検証を実行して終了")
    sub = parser.add_subparsers(dest="command", help="サブコマンド")

    # list
    sub.add_parser("list", help="ローカル/グローバルのスキル一覧と差分を表示")

    # plugin-list
    pl = sub.add_parser("plugin-list", help="外部プラグインレジストリからスキル一覧を表示")
    pl.add_argument("--verbose", "-v", action="store_true", help="各スキルの詳細を表示")

    # plugin-install
    pi = sub.add_parser("plugin-install", help="外部プラグインからスキルをインストール")
    pi.add_argument("--plugin", metavar="NAME", help="対象プラグイン名")
    pi.add_argument("--skill", nargs="+", metavar="NAME", help="インストールするスキル名")
    pi.add_argument("--all-recommended", action="store_true", help="全推奨スキルをインストール")
    pi.add_argument("--force", action="store_true", help="既存スキルを上書き")

    # plugin-update
    pu = sub.add_parser("plugin-update", help="インストール済み外部スキルを更新")
    pu.add_argument("--plugin", metavar="NAME", help="対象プラグイン名")
    pu.add_argument("--dry-run", action="store_true", help="更新内容を表示するのみ")

    # plugin-clean
    sub.add_parser("plugin-clean", help="プラグインキャッシュを削除")

    # plugin-guide (後方互換)
    sub.add_parser("plugin-guide", help="(廃止予定: plugin-list を使用してください)")

    # sync-global
    sg = sub.add_parser("sync-global", help="プロジェクトスキルを ~/.claude/skills/ にコピー")
    sg.add_argument("--force", action="store_true", help="既存スキルを上書き")
    sg.add_argument("--skills", nargs="+", metavar="NAME", help="コピーするスキル名（指定しない場合は全て）")
    sg.add_argument("--target", metavar="DIR", help="コピー先ディレクトリ（デフォルト: ~/.claude/skills/）")

    # sync-project
    sp = sub.add_parser("sync-project", help="プロジェクトスキルを別プロジェクトにコピー")
    sp.add_argument("project", help="コピー先プロジェクトのパス")
    sp.add_argument("--force", action="store_true", help="既存スキルを上書き")
    sp.add_argument("--skills", nargs="+", metavar="NAME", help="コピーするスキル名（指定しない場合は全て）")

    # update-upstream
    sub.add_parser("update-upstream", help="upstream から最新を取り込み（git fetch + merge）")

    args = parser.parse_args()

    if args.test:
        try:
            list_skills(PROJECT_SKILLS_DIR)
            list_skills(GLOBAL_SKILLS_DIR)
        except Exception as exc:
            logger.error("テスト失敗: %s", exc)
            sys.exit(1)
        print("OK")
        sys.exit(0)

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    handlers = {
        "list": cmd_list,
        "plugin-list": cmd_plugin_list,
        "plugin-install": cmd_plugin_install,
        "plugin-update": cmd_plugin_update,
        "plugin-clean": cmd_plugin_clean,
        "plugin-guide": cmd_plugin_guide,
        "sync-global": cmd_sync_global,
        "sync-project": cmd_sync_project,
        "update-upstream": cmd_update_upstream,
    }
    handlers[args.command](args)


if __name__ == "__main__":
    main()
