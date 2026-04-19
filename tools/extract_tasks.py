#!/usr/bin/env python3
"""
タスク抽出スクリプト

複数のデータソースから自動的にタスクを抽出・優先順位付けします。
- Git状態
- Activity Logger
- SpecStory (仕掛かりタスク)
- Slack-sync (依頼事項)
- Output (カレンダー、Gmail、ボイスメモ)
- Notion (データベース/ページ)
"""

import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, List, Dict

# HowToDo生成モジュール（オプション）
try:
    from howtodo_generator import HowToDoGenerator, generate_shortcuts_yaml, classify_task
    HAS_HOWTODO = True
except ImportError:
    HAS_HOWTODO = False

# Notionモジュール（オプション）
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from src.notion_fetcher import NotionClient, NotionToMarkdown
    HAS_NOTION = True
except ImportError:
    HAS_NOTION = False


class TaskExtractor:
    """複数ソースからタスクを抽出"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.today = datetime.now()
        self.today_str = self.today.strftime("%Y-%m-%d")
    
    # ========================================
    # 1. Git状態の取得
    # ========================================
    def get_git_status(self, do_pull: bool = True) -> dict:
        """git pull実行、最新commit情報を取得"""
        result = {
            "status": "未実行",
            "commit": None,
            "message": None,
            "files_changed": 0,
            "pull_output": None
        }
        
        try:
            if do_pull:
                # git pull --rebase
                pull_result = subprocess.run(
                    ["git", "pull", "--rebase"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=self.project_root
                )
                result["pull_output"] = pull_result.stdout.strip() or pull_result.stderr.strip()
                result["status"] = "完了" if pull_result.returncode == 0 else "エラー"
            else:
                result["status"] = "スキップ"
            
            # 最新commit情報
            log_result = subprocess.run(
                ["git", "log", "-1", "--pretty=format:%h|%s"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_root
            )
            if log_result.returncode == 0 and log_result.stdout:
                parts = log_result.stdout.strip().split("|", 1)
                result["commit"] = parts[0]
                result["message"] = parts[1] if len(parts) > 1 else ""
            
            # 変更ファイル数
            diff_result = subprocess.run(
                ["git", "diff", "--stat", "HEAD~1", "HEAD"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.project_root
            )
            if diff_result.returncode == 0:
                lines = diff_result.stdout.strip().split("\n")
                if lines and "files changed" in lines[-1]:
                    match = re.search(r"(\d+) files? changed", lines[-1])
                    if match:
                        result["files_changed"] = int(match.group(1))
                        
        except Exception as e:
            result["status"] = f"エラー: {str(e)}"
        
        return result
    
    # ========================================
    # 2. Activity Loggerからサマリー抽出
    # ========================================
    def extract_activity_logs(self, days: int = 2) -> list:
        """activity_logger/logs/*.json から作業サマリーを抽出"""
        logs_dir = self.project_root / "activity_logger" / "logs"
        summaries = []
        
        if not logs_dir.exists():
            return summaries
        
        # 直近n日分のログファイルを取得
        target_dates = [
            (self.today - timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(days)
        ]
        
        for date_str in target_dates:
            json_file = logs_dir / f"{date_str}.json"
            if not json_file.exists():
                continue
            
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # ログエントリからアプリとウィンドウ情報を集計
                app_windows = {}
                for log in data.get("logs", []):
                    app = log.get("active_app", "Unknown")
                    window = log.get("window_title", "")
                    if app not in app_windows:
                        app_windows[app] = set()
                    if window:
                        # ウィンドウタイトルを短縮
                        short_window = window[:50] + "..." if len(window) > 50 else window
                        app_windows[app].add(short_window)
                
                # サマリー構築
                summary_items = []
                for app, windows in sorted(app_windows.items(), key=lambda x: -len(x[1])):
                    if len(windows) > 3:
                        windows_list = list(windows)[:3] + [f"... 他{len(windows)-3}件"]
                    else:
                        windows_list = list(windows)
                    summary_items.append({
                        "app": app,
                        "windows": windows_list,
                        "count": len(windows)
                    })
                
                summaries.append({
                    "date": date_str,
                    "entries": len(data.get("logs", [])),
                    "apps": summary_items[:5]  # 上位5アプリ
                })
                
            except Exception as e:
                summaries.append({
                    "date": date_str,
                    "error": str(e)
                })
        
        return summaries
    
    def get_raw_activity_logs(self, days: int = 2) -> list:
        """activity_logger/logs/*.json から生のログデータを取得（LLM推測用）"""
        logs_dir = self.project_root / "activity_logger" / "logs"
        raw_logs = []
        
        if not logs_dir.exists():
            return raw_logs
        
        target_dates = [
            (self.today - timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(days)
        ]
        
        for date_str in target_dates:
            json_file = logs_dir / f"{date_str}.json"
            if not json_file.exists():
                continue
            
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                raw_logs.append({
                    "date": date_str,
                    "logs": data.get("logs", [])
                })
            except Exception as e:
                print(f"⚠️ Activity Log読み込みエラー ({date_str}): {e}")
        
        return raw_logs
    
    # ========================================
    # 2.5 Activity Logからタスクを推測
    # ========================================
    def extract_activity_based_tasks(self, activity_logs: list) -> list:
        """Activity Logから作業中のタスクを推測"""
        tasks = []
        seen_titles = set()
        
        for log in activity_logs:
            for app_info in log.get("apps", []):
                app = app_info.get("app", "")
                windows = app_info.get("windows", [])
                
                for window in windows:
                    task = None
                    
                    # Cursorでの作業 → コーディングタスク
                    if "Cursor" in app:
                        # ファイルパスっぽいものを抽出
                        if "/" in window or "\\" in window:
                            # ファイル名を抽出
                            parts = window.replace("\\", "/").split("/")
                            filename = parts[-1] if parts else window
                            # 拡張子があればコードファイル
                            if "." in filename:
                                task = {
                                    "title": f"コード編集: {filename[:30]}",
                                    "content": f"Cursorで{filename}を編集中",
                                    "source": "activity_logger",
                                    "priority": "B",
                                    "task_type": "work"
                                }
                    
                    # Slack → コミュニケーションタスク
                    elif "Slack" in app:
                        # チャンネル名を抽出
                        if "#" in window:
                            channel_match = re.search(r'#([\w\-_]+)', window)
                            if channel_match:
                                channel = channel_match.group(1)
                                task = {
                                    "title": f"Slack #{channel} 確認",
                                    "content": f"Slackの#{channel}チャンネルを確認",
                                    "source": "activity_logger",
                                    "priority": "B",
                                    "task_type": "reply"
                                }
                    
                    # Chrome/ブラウザ → ブラウザ作業
                    elif "Chrome" in app or "Safari" in app or "Firefox" in app:
                        # 特定のサービス名を検出
                        services = {
                            "freee": ("freee経理作業", "freee"),
                            "GitHub": ("GitHub作業", "github"),
                            "Notion": ("Notion確認", "notion"),
                            "CloudSign": ("CloudSign確認", "cloudsign"),
                        }
                        for service_key, (task_title, task_type) in services.items():
                            if service_key.lower() in window.lower():
                                task = {
                                    "title": task_title,
                                    "content": f"{service_key}での作業",
                                    "source": "activity_logger",
                                    "priority": "B",
                                    "task_type": "browser"
                                }
                                break
                    
                    # 重複チェックして追加
                    if task and task["title"] not in seen_titles:
                        seen_titles.add(task["title"])
                        tasks.append(task)
        
        return tasks[:10]  # 最大10件
    
    # ========================================
    # 3. SpecStoryから仕掛かりタスク抽出
    # ========================================
    def extract_specstory_tasks(self, days: int = 3, use_llm: bool = True, llm_generator=None) -> list:
        """
        直近n日の.specstory/history/*.mdから仕掛かりタスクを抽出
        
        Args:
            days: 対象日数
            use_llm: LLMで完了判定するかどうか
            llm_generator: HowToDoGeneratorインスタンス（LLM判定に使用）
        """
        history_dir = self.project_root / ".specstory" / "history"
        tasks = []
        
        if not history_dir.exists():
            return tasks
        
        # 対象期間の計算
        cutoff_date = self.today - timedelta(days=days)
        
        # すべてのmdファイルを取得し、更新日時でフィルタ
        md_files = []
        for md_file in history_dir.glob("*.md"):
            mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
            if mtime >= cutoff_date:
                md_files.append((md_file, mtime))
        
        # 更新日時でソート（新しい順）
        md_files.sort(key=lambda x: x[1], reverse=True)
        
        for md_file, mtime in md_files[:20]:  # 最大20件
            try:
                # ファイル名からタイトルを抽出
                # 例: 2026-01-08_03-37Z-ai-agent-business-innovation-project-pdf.md
                filename = md_file.stem
                parts = filename.split("-", 3)
                if len(parts) >= 4:
                    title = parts[3].replace("-", " ").title()
                else:
                    title = filename
                
                # ファイル内容から残タスクをパターンマッチ
                content = md_file.read_text(encoding='utf-8', errors='ignore')
                
                # TODOパターンを検出
                todo_patterns = [
                    r'\[ \] (.+)',  # Markdown checkbox未完了
                    r'TODO[:\s]+(.+)',  # TODO: xxx
                    r'残タスク[:\s]+(.+)',
                    r'次のステップ[:\s]+(.+)',
                ]
                
                remaining_tasks = []
                for pattern in todo_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches[:5]:  # 各パターン最大5件
                        task_text = match.strip()[:100]
                        if task_text and task_text not in remaining_tasks:
                            remaining_tasks.append(task_text)
                
                # 最初の見出しから実際のタイトルを取得
                title_match = re.search(r'^# (.+)', content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1).strip()
                    # 日付部分を除去
                    title = re.sub(r'\s*\(\d{4}-\d{2}-\d{2}.*\)$', '', title)
                
                # ==============================
                # 仕掛かり判定（LLM版）
                # ==============================
                has_remaining_todos = len(remaining_tasks) > 0
                
                # 進行中を示すキーワード
                in_progress_keywords = ["進行中", "作業中", "WIP", "実装中", "対応中", "確認中", "TODO"]
                has_in_progress_keyword = any(kw in content for kw in in_progress_keywords)
                
                # 完了を示すキーワード
                completion_keywords = ["完了", "Done", "Completed", "クローズ", "対応済み", "解決済み"]
                has_completion_keyword = any(kw in content for kw in completion_keywords)
                
                # LLM判定を使う場合
                llm_result = None
                if use_llm and llm_generator:
                    # LLMで判定（曖昧なケースを含め全件判定）
                    llm_result = llm_generator.check_task_completion(content[:3000], title)
                    
                    if llm_result:
                        is_in_progress = llm_result.get("is_in_progress", False)
                        llm_remaining = llm_result.get("remaining_work", "")
                        if llm_remaining and llm_remaining not in remaining_tasks:
                            remaining_tasks.insert(0, f"[LLM] {llm_remaining}")
                        
                        if is_in_progress:
                            print(f"  ✅ 仕掛かり: {title[:30]}... ({llm_result.get('reason', '')[:30]})")
                        else:
                            print(f"  ⏭️ 完了判定: {title[:30]}... ({llm_result.get('reason', '')[:30]})")
                            continue  # 完了済みはスキップ
                    else:
                        # LLM判定失敗時はフォールバック
                        is_in_progress = self._fallback_completion_check(
                            has_remaining_todos, has_in_progress_keyword, has_completion_keyword
                        )
                        if not is_in_progress:
                            continue
                else:
                    # LLM未使用時はフォールバック判定
                    is_in_progress = self._fallback_completion_check(
                        has_remaining_todos, has_in_progress_keyword, has_completion_keyword
                    )
                    if not is_in_progress:
                        continue
                
                tasks.append({
                    "file": md_file.name,
                    "title": title,
                    "last_updated": mtime.strftime("%Y-%m-%d %H:%M"),
                    "remaining_tasks": remaining_tasks[:5],
                    "size_kb": md_file.stat().st_size / 1024,
                    "is_in_progress": True,
                    "llm_confidence": llm_result.get("confidence", 0) if llm_result else None
                })
                
            except Exception as e:
                tasks.append({
                    "file": md_file.name,
                    "error": str(e)
                })
        
        return tasks
    
    def _fallback_completion_check(
        self, 
        has_remaining_todos: bool, 
        has_in_progress_keyword: bool, 
        has_completion_keyword: bool
    ) -> bool:
        """
        LLM未使用時のフォールバック完了判定
        
        Returns:
            True: 仕掛かり, False: 完了済み
        """
        if has_remaining_todos:
            # 未完了TODOがあれば、完了キーワードがあっても仕掛かり
            return True
        elif has_in_progress_keyword and not has_completion_keyword:
            # 進行中キーワードがあり、完了キーワードがない場合も仕掛かり
            return True
        else:
            # それ以外は完了済み
            return False
    
    # ========================================
    # 4. Slack-syncから依頼事項抽出
    # ========================================
    def extract_slack_tasks(self, workspaces: list = None) -> dict:
        """slack-sync/data/*/*.md から最新の依頼を抽出"""
        slack_dir = self.project_root / "slack-sync"
        data_dir = slack_dir / "data"
        results = {}
        
        if not data_dir.exists():
            return results
        
        # .last_sync_*.json から更新チャンネルを特定
        sync_files = list(slack_dir.glob(".last_sync_*.json"))
        
        for sync_file in sync_files:
            workspace = sync_file.stem.replace(".last_sync_", "")
            
            # ワークスペースフィルタ
            if workspaces and workspace not in workspaces:
                continue
            
            workspace_dir = data_dir / workspace
            if not workspace_dir.exists():
                continue
            
            try:
                with open(sync_file, 'r', encoding='utf-8') as f:
                    sync_data = json.load(f)
                
                # 各チャンネルの最新メッセージを確認
                channel_updates = []
                for channel_id, channel_info in sync_data.get("channels", {}).items():
                    channel_name = channel_info.get("name", channel_id)
                    latest_ts = channel_info.get("latest_ts", "0")
                    
                    # タイムスタンプを日時に変換
                    try:
                        ts_float = float(latest_ts)
                        msg_date = datetime.fromtimestamp(ts_float)
                        # 直近3日以内のみ
                        if (self.today - msg_date).days <= 3:
                            channel_updates.append({
                                "channel": channel_name,
                                "last_update": msg_date.strftime("%m/%d %H:%M")
                            })
                    except (ValueError, OSError):
                        pass
                
                # 対応するmdファイルから内容を抽出
                md_items = []
                for md_file in workspace_dir.glob("*.md"):
                    mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
                    # 直近3日以内のファイル
                    if (self.today - mtime).days <= 3:
                        try:
                            content = md_file.read_text(encoding='utf-8', errors='ignore')
                            
                            # メンションパターンを検出
                            mention_pattern = r'@\w+'
                            mentions = re.findall(mention_pattern, content)
                            
                            # 最新のメッセージ（日付ヘッダーの下）を取得
                            recent_match = re.search(
                                r'## (\d{4}-\d{2}-\d{2})\s*\n(.+?)(?=\n## |\n---|\Z)',
                                content,
                                re.DOTALL
                            )
                            
                            if recent_match:
                                date = recent_match.group(1)
                                messages = recent_match.group(2).strip()
                                # 最初の200文字
                                preview = messages[:200].replace('\n', ' ')
                                
                                # SlackメッセージへのURLを抽出
                                # パターン: [[Slack]](https://xxx.slack.com/archives/xxx/pxxx)
                                slack_url_match = re.search(
                                    r'\[\[Slack\]\]\((https://[^\s)]+\.slack\.com/archives/[^\s)]+)\)',
                                    messages
                                )
                                slack_url = slack_url_match.group(1) if slack_url_match else None
                                
                                md_items.append({
                                    "channel": md_file.stem,
                                    "date": date,
                                    "preview": preview,
                                    "mentions": list(set(mentions))[:3],
                                    "mtime": mtime.strftime("%m/%d %H:%M"),
                                    "slack_url": slack_url
                                })
                        except Exception:
                            pass
                
                # 更新日時でソート
                md_items.sort(key=lambda x: x.get("mtime", ""), reverse=True)
                
                results[workspace] = {
                    "channel_count": len(channel_updates),
                    "recent_channels": channel_updates[:5],
                    "recent_messages": md_items[:5]
                }
                
            except Exception as e:
                results[workspace] = {"error": str(e)}
        
        return results
    
    # ========================================
    # 5. Outputから予定・メール確認
    # ========================================
    def extract_output_tasks(self) -> dict:
        """output/calendar, gmail, voicememo から本日分を抽出"""
        output_dir = self.project_root / "output"
        result = {
            "calendar": [],
            "gmail": {"count": 0, "recent": []},
            "voicememo": []
        }
        
        # カレンダー
        calendar_dir = output_dir / "calendar"
        if calendar_dir.exists():
            calendar_file = calendar_dir / f"{self.today_str}_events.md"
            if calendar_file.exists():
                try:
                    content = calendar_file.read_text(encoding='utf-8')
                    # イベントを抽出 (複数フォーマットに対応)
                    events = []
                    
                    # パターン1: summary: xxx 形式
                    summary_matches = re.findall(r'^summary:\s*(.+)$', content, re.MULTILINE)
                    events.extend(summary_matches)
                    
                    # パターン2: ## または ### で始まる行（旧形式互換）
                    heading_matches = re.findall(r'^#{2,3}\s+(.+)$', content, re.MULTILINE)
                    events.extend(heading_matches)
                    
                    # パターン3: - **イベント名** 形式
                    bullet_matches = re.findall(r'^-\s+\*\*(.+?)\*\*', content, re.MULTILINE)
                    events.extend(bullet_matches)
                    
                    # 重複除去して保存
                    unique_events = []
                    for e in events:
                        if e not in unique_events:
                            unique_events.append(e)
                    result["calendar"] = unique_events[:10]
                except Exception:
                    pass
        
        # Gmail (直近のメール数とサブジェクト)
        gmail_dir = output_dir / "gmail"
        if gmail_dir.exists():
            # 最新10件のファイルを取得
            gmail_files = sorted(
                gmail_dir.glob("*.md"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )[:10]
            
            result["gmail"]["count"] = len(list(gmail_dir.glob("*.md")))
            
            for gf in gmail_files:
                try:
                    # ファイル名からサブジェクトを取得
                    subject = gf.stem
                    mtime = datetime.fromtimestamp(gf.stat().st_mtime)
                    result["gmail"]["recent"].append({
                        "subject": subject[:50],
                        "date": mtime.strftime("%m/%d")
                    })
                except Exception:
                    pass
        
        # ボイスメモ
        voicememo_dir = output_dir / "voicememo"
        if voicememo_dir.exists():
            memo_files = sorted(
                voicememo_dir.glob("*.md"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )[:5]
            
            for mf in memo_files:
                try:
                    mtime = datetime.fromtimestamp(mf.stat().st_mtime)
                    result["voicememo"].append({
                        "name": mf.stem,
                        "date": mtime.strftime("%m/%d %H:%M")
                    })
                except Exception:
                    pass
        
        return result
    
    # ========================================
    # 6. Notionからタスク抽出
    # ========================================
    def extract_notion_tasks(self, database_id: str = None) -> list:
        """
        Notionデータベースからタスクを抽出
        
        Args:
            database_id: NotionデータベースID（省略時は環境変数から取得）
        
        Returns:
            タスクリスト
        """
        if not HAS_NOTION:
            return []
        
        tasks = []
        
        # データベースIDを決定
        db_id = database_id or os.getenv("NOTION_DATABASE_ID")
        if not db_id:
            return tasks
        
        try:
            client = NotionClient()
            
            # データベースをクエリ（未完了タスクをフィルタ）
            # 一般的なタスク管理DBを想定したフィルタ
            filter_conditions = None
            
            # ステータスプロパティがある場合のフィルタ例
            # filter_conditions = {
            #     "or": [
            #         {"property": "Status", "select": {"equals": "Not started"}},
            #         {"property": "Status", "select": {"equals": "In progress"}}
            #     ]
            # }
            
            pages = client.query_database(db_id, filter=filter_conditions)
            
            for page in pages:
                props = page.get("properties", {})
                
                # タイトルを取得
                title = ""
                for prop_name, prop in props.items():
                    if prop.get("type") == "title":
                        title_arr = prop.get("title", [])
                        title = "".join([t.get("plain_text", "") for t in title_arr])
                        break
                
                if not title:
                    continue
                
                # ステータスを取得
                status = ""
                status_prop = props.get("Status") or props.get("ステータス")
                if status_prop:
                    if status_prop.get("type") == "status":
                        status = status_prop.get("status", {}).get("name", "")
                    elif status_prop.get("type") == "select":
                        status = status_prop.get("select", {}).get("name", "")
                
                # 完了タスクはスキップ
                completed_statuses = ["Done", "完了", "Completed", "Closed"]
                if status in completed_statuses:
                    continue
                
                # 担当者を取得
                assignee = ""
                assignee_prop = props.get("Assignee") or props.get("担当者")
                if assignee_prop and assignee_prop.get("type") == "people":
                    people = assignee_prop.get("people", [])
                    assignee = ", ".join([p.get("name", "") for p in people])
                
                # 期限を取得
                due_date = ""
                date_prop = props.get("Due") or props.get("期限") or props.get("Date")
                if date_prop and date_prop.get("type") == "date":
                    date_val = date_prop.get("date")
                    if date_val:
                        due_date = date_val.get("start", "")
                
                tasks.append({
                    "id": page.get("id", ""),
                    "title": title,
                    "status": status,
                    "assignee": assignee,
                    "due_date": due_date,
                    "url": page.get("url", ""),
                    "source": "notion"
                })
            
            # 期限でソート（期限なしは最後に）
            tasks.sort(key=lambda x: x.get("due_date") or "9999-99-99")
            
        except Exception as e:
            print(f"⚠️ Notion取得エラー: {e}")
        
        return tasks[:20]  # 最大20件
    
    # ========================================
    # 7. 優先順位付け
    # ========================================
    def prioritize_tasks(self, specstory_tasks: list, slack_tasks: dict, notion_tasks: list = None) -> dict:
        """タスクを優先度でソート"""
        prioritized = {
            "A": [],  # 仕掛かり（SpecStory）
            "B": [],  # 新規依頼（Slack）
            "C": [],  # 定期タスク
            "N": []   # Notion タスク
        }
        
        # SpecStoryタスクを優先度Aに
        for task in specstory_tasks:
            if task.get("remaining_tasks"):
                prioritized["A"].append(task)
        
        # Slackタスクを優先度Bに
        for workspace, data in slack_tasks.items():
            if isinstance(data, dict) and "recent_messages" in data:
                for msg in data.get("recent_messages", []):
                    if msg.get("mentions"):  # メンション付きを優先
                        prioritized["B"].append({
                            "workspace": workspace,
                            **msg
                        })
        
        # Notionタスクを追加
        if notion_tasks:
            for task in notion_tasks:
                # 期限が今日以前のものは優先度高
                due_date = task.get("due_date", "")
                if due_date and due_date <= self.today_str:
                    prioritized["A"].append({
                        "title": f"[Notion] {task['title']}",
                        "remaining_tasks": [f"期限: {due_date}", f"ステータス: {task.get('status', 'N/A')}"],
                        "notion_url": task.get("url", ""),
                        "source": "notion"
                    })
                else:
                    prioritized["N"].append(task)
        
        return prioritized
    
    # ========================================
    # 8. 出力生成
    # ========================================
    def generate_report(
        self,
        git_status: dict,
        activity_logs: list,
        specstory_tasks: list,
        slack_tasks: dict,
        output_tasks: dict,
        prioritized: dict,
        notion_tasks: list = None
    ) -> str:
        """Markdown形式のタスク一覧を生成"""
        lines = [
            f"# タスク一覧（{self.today_str}）",
            "",
            "## データソース状態",
            "",
            "| ソース | 期間/状態 | 詳細 |",
            "|--------|-----------|------|",
        ]
        
        # Git状態
        git_detail = f"{git_status.get('commit', 'N/A')}"
        if git_status.get('files_changed'):
            git_detail += f" ({git_status['files_changed']} files changed)"
        lines.append(f"| git | {git_status.get('status', 'N/A')} | {git_detail} |")
        
        # Activity Logger
        if activity_logs:
            dates = [log.get('date', 'N/A') for log in activity_logs]
            entries = sum(log.get('entries', 0) for log in activity_logs)
            lines.append(f"| activity_logger | {'-'.join(dates)} | {entries}エントリ |")
        else:
            lines.append("| activity_logger | - | データなし |")
        
        # SpecStory
        lines.append(f"| .specstory | 直近{len(specstory_tasks)}件 | {len([t for t in specstory_tasks if t.get('remaining_tasks')])}件に残タスクあり |")
        
        # Slack
        workspace_names = list(slack_tasks.keys())
        lines.append(f"| slack-sync | 最新sync | {', '.join(workspace_names) if workspace_names else 'なし'} |")
        
        # Notion
        notion_count = len(notion_tasks) if notion_tasks else 0
        lines.append(f"| notion | タスクDB | {notion_count}件 |")
        
        # Output
        cal_count = len(output_tasks.get('calendar', []))
        gmail_count = output_tasks.get('gmail', {}).get('count', 0)
        lines.append(f"| output | 本日 | calendar: {cal_count}件, gmail: {gmail_count}件 |")
        
        lines.extend(["", "---", ""])
        
        # 優先度A: 仕掛かりタスク
        lines.extend([
            "## 優先度A: 仕掛かりタスク",
            ""
        ])
        
        if prioritized["A"]:
            for i, task in enumerate(prioritized["A"][:5], 1):
                lines.extend([
                    f"### {i}. [{task.get('title', 'Untitled')}]",
                    f"- **ファイル**: {task.get('file', 'N/A')}",
                    f"- **最終更新**: {task.get('last_updated', 'N/A')}",
                    f"- **サイズ**: {task.get('size_kb', 0):.1f} KB",
                ])
                if task.get('remaining_tasks'):
                    lines.append("- **残タスク**:")
                    for rt in task['remaining_tasks']:
                        lines.append(f"  - [ ] {rt}")
                lines.append("")
        else:
            lines.extend(["*仕掛かりタスクはありません*", ""])
        
        lines.extend(["---", ""])
        
        # 優先度B: Slack依頼事項
        lines.extend([
            "## 優先度B: Slack依頼事項",
            ""
        ])
        
        if slack_tasks:
            for workspace, data in slack_tasks.items():
                if isinstance(data, dict) and not data.get("error"):
                    lines.append(f"### {workspace}")
                    for msg in data.get("recent_messages", [])[:3]:
                        channel = msg.get('channel', 'N/A')
                        date = msg.get('date', '')
                        preview = msg.get('preview', '')[:80]
                        mentions = ', '.join(msg.get('mentions', []))
                        lines.append(f"- **{channel}** ({date}): {preview}")
                        if mentions:
                            lines.append(f"  - メンション: {mentions}")
                    lines.append("")
        else:
            lines.extend(["*Slack依頼事項はありません*", ""])
        
        lines.extend(["---", ""])
        
        # Notionタスク
        if prioritized.get("N"):
            lines.extend([
                "## Notionタスク",
                ""
            ])
            for i, task in enumerate(prioritized["N"][:10], 1):
                status = task.get("status", "N/A")
                due = task.get("due_date", "")
                url = task.get("url", "")
                lines.append(f"{i}. **{task['title']}**")
                lines.append(f"   - ステータス: {status}")
                if due:
                    lines.append(f"   - 期限: {due}")
                if url:
                    lines.append(f"   - [Notionで開く]({url})")
                lines.append("")
            lines.extend(["---", ""])
        
        # 優先度C: 定期タスク
        lines.extend([
            "## 優先度C: 定期タスク",
            ""
        ])
        
        # カレンダー
        lines.append("### カレンダー（本日）")
        if output_tasks.get("calendar"):
            for event in output_tasks["calendar"][:5]:
                lines.append(f"- {event}")
        else:
            lines.append("- 予定なし")
        lines.append("")
        
        # Gmail
        lines.append("### メール（最近）")
        if output_tasks.get("gmail", {}).get("recent"):
            for mail in output_tasks["gmail"]["recent"][:5]:
                lines.append(f"- [{mail.get('date', '')}] {mail.get('subject', 'N/A')}")
        else:
            lines.append("- 新着メールなし")
        lines.append("")
        
        # ボイスメモ
        if output_tasks.get("voicememo"):
            lines.append("### ボイスメモ")
            for memo in output_tasks["voicememo"][:3]:
                lines.append(f"- [{memo.get('date', '')}] {memo.get('name', 'N/A')}")
            lines.append("")
        
        lines.extend(["---", ""])
        
        # Activity Logger サマリー
        if activity_logs:
            lines.extend([
                "## Activity Logger サマリー",
                ""
            ])
            for log in activity_logs:
                if "error" in log:
                    lines.append(f"### {log.get('date', 'N/A')} - エラー: {log['error']}")
                else:
                    lines.extend([
                        f"### {log.get('date', 'N/A')} ({log.get('entries', 0)}エントリ)",
                        ""
                    ])
                    for app_info in log.get('apps', []):
                        app = app_info.get('app', 'N/A')
                        count = app_info.get('count', 0)
                        lines.append(f"- **{app}** ({count}件)")
                    lines.append("")
        
        return "\n".join(lines)


def generate_html_dashboard(
    date_str: str,
    prioritized: Dict[str, Any],
    output_tasks: Dict[str, Any]
) -> str:
    """HTMLダッシュボードを生成"""
    
    # テンプレートファイルを読み込む
    template_path = Path(__file__).parent / "templates" / "howtodo_dashboard.html"
    
    if template_path.exists():
        template = template_path.read_text(encoding='utf-8')
    else:
        # テンプレートがない場合はインライン生成
        template = _get_inline_html_template()
    
    # タスクデータを準備
    tasks_with_howtodo = prioritized.get("tasks_with_howtodo", [])
    
    priority_a = [t for t in tasks_with_howtodo if t.get("priority") == "A"]
    priority_b = [t for t in tasks_with_howtodo if t.get("priority") == "B"]
    priority_c = []  # カレンダー等
    
    for event in output_tasks.get("calendar", []):
        priority_c.append({
            "id": f"cal_{hash(event) % 10000}",
            "title": event,
            "source": "calendar",
            "priority": "C",
            "howtodo": {
                "task_type": "meeting",
                "steps": [],
                "estimated_minutes": 60
            }
        })
    
    # JSON データを埋め込む
    tasks_json = json.dumps({
        "date": date_str,
        "priority_a": priority_a,
        "priority_b": priority_b,
        "priority_c": priority_c,
        "task_count": len(priority_a) + len(priority_b) + len(priority_c)
    }, ensure_ascii=False)
    
    # テンプレート内の変数を置換
    html = template.replace("{{ TASKS_JSON }}", tasks_json)
    html = html.replace("{{ DATE }}", date_str)
    html = html.replace("{{ TASK_COUNT }}", str(len(tasks_with_howtodo)))
    
    return html


def _get_inline_html_template() -> str:
    """インラインHTMLテンプレート（フォールバック用）"""
    return '''<!DOCTYPE html>
<html lang="ja" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HowToDo Dashboard - {{ DATE }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --background: 240 10% 3.9%;
            --foreground: 0 0% 98%;
            --card: 240 10% 3.9%;
            --primary: 0 0% 98%;
            --secondary: 240 3.7% 15.9%;
            --muted: 240 3.7% 15.9%;
            --muted-foreground: 240 5% 64.9%;
            --border: 240 3.7% 15.9%;
        }
        body { font-family: 'Inter', sans-serif; }
        .task-card { transition: all 0.2s ease-out; }
        .task-card:hover { background-color: rgb(39 39 42); }
        .chevron-rotate { transform: rotate(180deg); }
    </style>
</head>
<body class="bg-zinc-950 text-zinc-50 min-h-screen">
    <!-- Header -->
    <header class="border-b border-zinc-800 px-6 py-4 sticky top-0 bg-zinc-950/95 backdrop-blur z-10">
        <div class="flex items-center justify-between max-w-5xl mx-auto">
            <div>
                <h1 class="text-xl font-semibold tracking-tight">HowToDo Dashboard</h1>
                <p class="text-sm text-zinc-400" id="header-info">{{ DATE }} · {{ TASK_COUNT }} tasks</p>
            </div>
            <button onclick="location.reload()" class="inline-flex items-center px-4 py-2 rounded-md bg-zinc-800 hover:bg-zinc-700 text-sm font-medium transition-colors">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
                Refresh
            </button>
        </div>
    </header>
    
    <main class="max-w-5xl mx-auto px-6 py-8 space-y-8" id="main-content">
        <!-- Priority A Section -->
        <section id="priority-a-section">
            <div class="flex items-center gap-2 mb-4">
                <span class="w-2 h-2 rounded-full bg-red-500"></span>
                <h2 class="text-lg font-medium">Priority A: 仕掛かりタスク</h2>
                <span class="text-xs text-zinc-500 bg-zinc-800 px-2 py-0.5 rounded-full" id="priority-a-count">0</span>
            </div>
            <div class="space-y-3" id="priority-a-tasks"></div>
        </section>
        
        <!-- Priority B Section -->
        <section id="priority-b-section">
            <div class="flex items-center gap-2 mb-4">
                <span class="w-2 h-2 rounded-full bg-yellow-500"></span>
                <h2 class="text-lg font-medium">Priority B: Slack依頼事項</h2>
                <span class="text-xs text-zinc-500 bg-zinc-800 px-2 py-0.5 rounded-full" id="priority-b-count">0</span>
            </div>
            <div class="space-y-3" id="priority-b-tasks"></div>
        </section>
        
        <!-- Priority C Section -->
        <section id="priority-c-section">
            <div class="flex items-center gap-2 mb-4">
                <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                <h2 class="text-lg font-medium">Priority C: カレンダー予定</h2>
                <span class="text-xs text-zinc-500 bg-zinc-800 px-2 py-0.5 rounded-full" id="priority-c-count">0</span>
            </div>
            <div class="space-y-3" id="priority-c-tasks"></div>
        </section>
    </main>
    
    <!-- Modal -->
    <div id="prompt-modal" class="fixed inset-0 bg-black/80 hidden items-center justify-center z-50">
        <div class="bg-zinc-900 border border-zinc-800 rounded-xl shadow-xl max-w-2xl w-full mx-4 overflow-hidden">
            <div class="px-6 py-4 border-b border-zinc-800 flex items-center justify-between">
                <h3 class="font-semibold" id="modal-title">Prompt</h3>
                <button onclick="closeModal()" class="text-zinc-400 hover:text-zinc-100">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                </button>
            </div>
            <div class="p-6">
                <pre id="prompt-text" class="bg-zinc-950 rounded-lg p-4 text-sm text-zinc-300 overflow-auto max-h-96 whitespace-pre-wrap"></pre>
            </div>
            <div class="px-6 py-4 border-t border-zinc-800 flex justify-end gap-2">
                <button onclick="closeModal()" class="px-4 py-2 rounded-md text-sm font-medium hover:bg-zinc-800 transition-colors">Cancel</button>
                <button onclick="copyAndClose()" class="px-4 py-2 rounded-md bg-zinc-50 text-zinc-900 text-sm font-medium hover:bg-zinc-200 transition-colors">Copy & Close</button>
            </div>
        </div>
    </div>
    
    <!-- Toast -->
    <div id="toast" class="fixed bottom-4 right-4 bg-emerald-600 border border-emerald-500 rounded-lg px-4 py-3 shadow-lg hidden transition-opacity">
        <p class="text-sm font-medium">✓ Copied to clipboard</p>
    </div>

    <script>
        // タスクデータ
        const tasksData = {{ TASKS_JSON }};
        
        // 初期化
        document.addEventListener('DOMContentLoaded', () => {
            renderTasks('priority-a-tasks', tasksData.priority_a, 'priority-a-count');
            renderTasks('priority-b-tasks', tasksData.priority_b, 'priority-b-count');
            renderTasks('priority-c-tasks', tasksData.priority_c, 'priority-c-count');
        });
        
        // タスクカードを生成
        function renderTasks(containerId, tasks, countId) {
            const container = document.getElementById(containerId);
            const countEl = document.getElementById(countId);
            
            countEl.textContent = tasks.length;
            
            if (tasks.length === 0) {
                container.innerHTML = '<p class="text-zinc-500 text-sm py-4">タスクはありません</p>';
                return;
            }
            
            container.innerHTML = tasks.map((task, idx) => createTaskCard(task, idx)).join('');
        }
        
        // タスクカードHTML生成
        function createTaskCard(task, idx) {
            const howtodo = task.howtodo || {};
            const steps = howtodo.steps || [];
            const taskId = task.id || `task-${idx}`;
            
            return `
                <div class="task-card group rounded-lg border border-zinc-800 bg-zinc-900/50">
                    <button onclick="toggleTask('${taskId}')" 
                            class="w-full px-4 py-3 flex items-center justify-between text-left">
                        <div class="flex items-center gap-3 min-w-0">
                            <div class="w-5 h-5 rounded border border-zinc-700 flex-shrink-0 flex items-center justify-center">
                                <svg class="w-3 h-3 text-zinc-500 hidden" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/>
                                </svg>
                            </div>
                            <span class="font-medium truncate">${escapeHtml(task.title)}</span>
                            <span class="text-xs text-zinc-500 bg-zinc-800 px-2 py-0.5 rounded-full flex-shrink-0">${howtodo.task_type || 'work'}</span>
                        </div>
                        <div class="flex items-center gap-2 flex-shrink-0">
                            <span class="text-xs text-zinc-500">${howtodo.estimated_minutes || 5}min</span>
                            <svg class="w-4 h-4 text-zinc-500 transition-transform" id="chevron-${taskId}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                            </svg>
                        </div>
                    </button>
                    
                    <div id="content-${taskId}" class="hidden border-t border-zinc-800 px-4 py-4">
                        ${steps.length > 0 ? `
                            <div class="space-y-2 mb-4">
                                ${steps.map((step, i) => `
                                    <label class="flex items-start gap-3 p-2 rounded hover:bg-zinc-800/50 cursor-pointer">
                                        <input type="checkbox" onchange="saveCheckState('${taskId}', ${i})" 
                                               ${localStorage.getItem(`howtodo_${taskId}_${i}`) === 'true' ? 'checked' : ''}
                                               class="mt-1 rounded border-zinc-700 bg-zinc-800 text-emerald-500 focus:ring-emerald-500/20">
                                        <div class="min-w-0">
                                            <p class="text-sm">${step.order}. ${escapeHtml(step.action)}</p>
                                            <p class="text-xs text-zinc-500">✓ ${escapeHtml(step.check_condition)}</p>
                                        </div>
                                    </label>
                                `).join('')}
                            </div>
                        ` : '<p class="text-sm text-zinc-500 mb-4">手順情報なし</p>'}
                        
                        ${task.remaining_tasks && task.remaining_tasks.length > 0 ? `
                            <div class="mb-4 p-3 bg-zinc-800/50 rounded-lg">
                                <p class="text-xs text-zinc-400 mb-2">残タスク:</p>
                                <ul class="space-y-1">
                                    ${task.remaining_tasks.map(t => `<li class="text-sm text-zinc-300">• ${escapeHtml(t)}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''}
                        
                        <div class="flex gap-2 pt-3 border-t border-zinc-800">
                            ${howtodo.cursor_prompt ? `
                                <button onclick="copyPrompt('${taskId}', '${escapeJs(howtodo.cursor_prompt)}')" 
                                        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-zinc-800 hover:bg-zinc-700 text-xs font-medium transition-colors">
                                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                                    </svg>
                                    Copy Prompt
                                </button>
                            ` : ''}
                            ${howtodo.reply_examples && howtodo.reply_examples.length > 0 ? `
                                <button onclick="openModal('返信例', '${escapeJs(howtodo.reply_examples.join('\\n\\n---\\n\\n'))}')"
                                        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-blue-600 hover:bg-blue-500 text-xs font-medium transition-colors">
                                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                                    </svg>
                                    Reply Examples
                                </button>
                            ` : ''}
                            <button onclick="openModal('Cursor Prompt', '${escapeJs(task.content || task.title)}')"
                                    class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-emerald-600 hover:bg-emerald-500 text-xs font-medium transition-colors">
                                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                                </svg>
                                Open Prompt
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }
        
        // ユーティリティ関数
        function escapeHtml(str) {
            if (!str) return '';
            return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
        }
        
        function escapeJs(str) {
            if (!str) return '';
            return str.replace(/\\\\/g, '\\\\\\\\').replace(/'/g, "\\\\'").replace(/\\n/g, '\\\\n');
        }
        
        // アコーディオン
        function toggleTask(id) {
            const content = document.getElementById(`content-${id}`);
            const chevron = document.getElementById(`chevron-${id}`);
            content.classList.toggle('hidden');
            chevron.classList.toggle('chevron-rotate');
        }
        
        // チェック状態保存
        function saveCheckState(taskId, stepIndex) {
            const key = `howtodo_${taskId}_${stepIndex}`;
            const current = localStorage.getItem(key) === 'true';
            localStorage.setItem(key, !current);
        }
        
        // クリップボードコピー
        async function copyPrompt(id, text) {
            try {
                await navigator.clipboard.writeText(text.replace(/\\\\n/g, '\\n'));
                showToast();
            } catch (e) {
                console.error('Copy failed:', e);
            }
        }
        
        // Toast
        function showToast() {
            const toast = document.getElementById('toast');
            toast.classList.remove('hidden');
            setTimeout(() => toast.classList.add('hidden'), 2000);
        }
        
        // Modal
        let currentPromptText = '';
        function openModal(title, text) {
            currentPromptText = text.replace(/\\\\n/g, '\\n');
            document.getElementById('modal-title').textContent = title;
            document.getElementById('prompt-text').textContent = currentPromptText;
            document.getElementById('prompt-modal').classList.remove('hidden');
            document.getElementById('prompt-modal').classList.add('flex');
        }
        
        function closeModal() {
            document.getElementById('prompt-modal').classList.add('hidden');
            document.getElementById('prompt-modal').classList.remove('flex');
        }
        
        async function copyAndClose() {
            try {
                await navigator.clipboard.writeText(currentPromptText);
                showToast();
                closeModal();
            } catch (e) {
                console.error('Copy failed:', e);
            }
        }
    </script>
</body>
</html>'''


def main():
    parser = argparse.ArgumentParser(
        description="複数データソースからタスクを抽出します"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=3,
        help="SpecStory対象日数（デフォルト: 3）"
    )
    parser.add_argument(
        "--workspaces",
        type=str,
        default="",
        help="Slack対象ワークスペース（カンマ区切り、デフォルト: all）"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="出力ファイルパス（省略時: stdout）"
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["markdown", "json", "html", "shortcuts"],
        default="markdown",
        help="出力形式（デフォルト: markdown）"
    )
    parser.add_argument(
        "--howtodo",
        action="store_true",
        help="各タスクにHowToDo手順を生成（Gemini API必要）"
    )
    parser.add_argument(
        "--git-pull",
        action="store_true",
        default=True,
        help="git pullを実行する（デフォルト: True）"
    )
    parser.add_argument(
        "--no-git-pull",
        action="store_true",
        help="git pullをスキップ"
    )
    parser.add_argument(
        "--project-root",
        type=str,
        default="",
        help="プロジェクトルートパス（デフォルト: スクリプトの親の親ディレクトリ）"
    )
    parser.add_argument(
        "--notion-db",
        type=str,
        default="",
        help="NotionデータベースID（省略時は環境変数NOTION_DATABASE_IDを使用）"
    )
    parser.add_argument(
        "--no-notion",
        action="store_true",
        help="Notion取得をスキップ"
    )
    
    args = parser.parse_args()
    
    # プロジェクトルートの決定
    if args.project_root:
        project_root = Path(args.project_root)
    else:
        # スクリプトの親の親ディレクトリ (tools -> project_root)
        project_root = Path(__file__).parent.parent
    
    # ワークスペースリストの処理
    workspaces = None
    if args.workspaces:
        workspaces = [w.strip() for w in args.workspaces.split(",") if w.strip()]
    
    # git pullの判定
    do_git_pull = args.git_pull and not args.no_git_pull
    
    # HowToDoGeneratorを先に作成（LLM判定に使用）
    generator = None
    if args.howtodo and HAS_HOWTODO:
        generator = HowToDoGenerator()
    
    # タスク抽出
    extractor = TaskExtractor(project_root)
    
    git_status = extractor.get_git_status(do_pull=do_git_pull)
    activity_logs = extractor.extract_activity_logs(days=2)
    
    # Activity Logからタスク推測（キーワードベース）
    activity_tasks = extractor.extract_activity_based_tasks(activity_logs)
    
    # Activity LogからLLM推測（howtodoオプション有効時）
    activity_llm_tasks = []
    if args.howtodo and generator:
        print("🔍 Activity LogからLLMでタスク推測中...")
        raw_activity_logs = extractor.get_raw_activity_logs(days=2)
        activity_llm_tasks = generator.infer_tasks_from_activity(raw_activity_logs)
    
    # SpecStory抽出（howtodoオプション有効時はLLM判定を使用）
    print("🔍 SpecStory仕掛かり判定中...")
    specstory_tasks = extractor.extract_specstory_tasks(
        days=args.days, 
        use_llm=args.howtodo and generator is not None,
        llm_generator=generator
    )
    
    slack_tasks = extractor.extract_slack_tasks(workspaces=workspaces)
    output_tasks = extractor.extract_output_tasks()
    
    # Notion タスク取得
    notion_tasks = []
    if not args.no_notion and HAS_NOTION:
        print("🔍 Notionタスク取得中...")
        notion_db_id = args.notion_db if args.notion_db else None
        notion_tasks = extractor.extract_notion_tasks(database_id=notion_db_id)
        print(f"   → {len(notion_tasks)} 件のNotionタスク")
    
    prioritized = extractor.prioritize_tasks(specstory_tasks, slack_tasks, notion_tasks)
    
    # HowToDo生成（オプション）
    all_tasks_for_howtodo = []
    if args.howtodo and generator:
        
        # 優先度Aタスク（SpecStory仕掛かり）をフラットなリストに変換
        for task in prioritized.get("A", []):
            task_dict = {
                "id": task.get("file", "").replace(".md", ""),
                "title": task.get("title", "Unknown"),
                "content": "\n".join(task.get("remaining_tasks", [])),
                "source": "specstory",
                "priority": "A",
                "last_updated": task.get("last_updated", ""),
                "file": task.get("file", ""),
                "remaining_tasks": task.get("remaining_tasks", [])
            }
            all_tasks_for_howtodo.append(task_dict)
        
        # 優先度Bタスク（Slack依頼）
        for task in prioritized.get("B", []):
            task_dict = {
                "id": f"{task.get('workspace', 'slack')}_{task.get('channel', 'unknown')}",
                "title": f"[{task.get('workspace', '')}] {task.get('channel', '')}",
                "content": task.get("preview", ""),
                "source": "slack",
                "priority": "B",
                "mentions": task.get("mentions", []),
                "date": task.get("date", ""),
                "slack_url": task.get("slack_url")  # SlackメッセージへのURL
            }
            all_tasks_for_howtodo.append(task_dict)
        
        # Activity Logから推測したタスク（キーワードベース）
        for task in activity_tasks:
            task_dict = {
                "id": f"activity_{task.get('title', 'unknown')[:20]}",
                "title": task.get("title", "Activity Task"),
                "content": task.get("content", ""),
                "source": "activity_logger",
                "priority": task.get("priority", "B"),
                "task_type": task.get("task_type", "work")
            }
            all_tasks_for_howtodo.append(task_dict)
        
        # Activity LogからLLM推測したタスク
        for task in activity_llm_tasks:
            task_dict = {
                "id": task.get("id", f"activity_llm_{len(all_tasks_for_howtodo)}"),
                "title": task.get("title", "Activity推測タスク"),
                "content": task.get("content", ""),
                "source": "activity_logger_llm",
                "priority": task.get("priority", "B"),
                "task_type": task.get("task_type", "work"),
                "llm_reason": task.get("llm_reason", "")  # 推測理由
            }
            all_tasks_for_howtodo.append(task_dict)
        
        # HowToDo生成
        all_tasks_for_howtodo = generator.generate_batch(all_tasks_for_howtodo)
        
        # prioritized にHowToDo付きタスクを反映
        prioritized["tasks_with_howtodo"] = all_tasks_for_howtodo
    
    # 出力生成
    if args.format == "json":
        output = json.dumps({
            "date": extractor.today_str,
            "git": git_status,
            "activity_logs": activity_logs,
            "specstory_tasks": specstory_tasks,
            "slack_tasks": slack_tasks,
            "notion_tasks": notion_tasks,
            "output_tasks": output_tasks,
            "prioritized": prioritized
        }, ensure_ascii=False, indent=2)
    elif args.format == "html":
        output = generate_html_dashboard(
            extractor.today_str,
            prioritized,
            output_tasks
        )
    elif args.format == "shortcuts":
        if HAS_HOWTODO and all_tasks_for_howtodo:
            output = generate_shortcuts_yaml(all_tasks_for_howtodo)
        else:
            output = "# ショートカット生成には --howtodo オプションが必要です"
    else:
        output = extractor.generate_report(
            git_status,
            activity_logs,
            specstory_tasks,
            slack_tasks,
            output_tasks,
            prioritized,
            notion_tasks
        )
    
    # 出力
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output, encoding='utf-8')
        print(f"出力完了: {output_path}")
    else:
        print(output)


if __name__ == "__main__":
    main()
