#!/usr/bin/env python3
"""
Slack検索・タスク抽出スクリプト（Final Example）

Slack APIを使用してメッセージ検索、タスク抽出を行います。

必要条件:
- Slack API トークン（環境変数 SLACK_USER_TOKEN, SLACK_BOT_TOKEN）
- Python 3.9以上
- slack-sdk

使用方法:
    python slack_search.py search --query "プロジェクト進捗"
    python slack_search.py extract-tasks --channel "#general"
    python slack_search.py summarize --channel "#general" --days 7
"""

import os
import sys
import re
import argparse
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    HAS_SLACK = True
except ImportError:
    HAS_SLACK = False
    print("Warning: slack-sdk がインストールされていません")
    print("  インストール: pip install slack-sdk")


# タスク抽出パターン
TASK_PATTERNS = [
    (r"TODO[:：]\s*(.+)", "TODO"),
    (r"タスク[:：]\s*(.+)", "タスク"),
    (r"【依頼】\s*(.+)", "依頼"),
    (r"【確認】\s*(.+)", "確認"),
    (r"お願い[:：]\s*(.+)", "依頼"),
    (r"確認お願い[:：]?\s*(.+)", "確認依頼"),
    (r"(.+)してください[。]?$", "依頼"),
    (r"(.+)をお願いします[。]?$", "依頼"),
    (r"〆切[:：]\s*(.+)", "期限"),
    (r"期限[:：]\s*(.+)", "期限"),
]

# 期限パターン
DEADLINE_PATTERNS = [
    (r"(\d{1,2}/\d{1,2})まで", "date"),
    (r"(\d{4}-\d{2}-\d{2})まで", "date"),
    (r"(\d{4}/\d{1,2}/\d{1,2})まで", "date"),
    (r"(今日中|本日中)", "today"),
    (r"(明日まで|明日中)", "tomorrow"),
    (r"(今週中|今週末まで)", "this_week"),
    (r"(来週まで|来週中)", "next_week"),
    (r"(今月中|月末まで)", "this_month"),
]


class SlackSearcher:
    """Slack検索クラス"""
    
    def __init__(self):
        self.user_token = os.environ.get("SLACK_USER_TOKEN")
        self.bot_token = os.environ.get("SLACK_BOT_TOKEN")
        self.user_client = None
        self.bot_client = None
        
        if HAS_SLACK:
            if self.user_token:
                self.user_client = WebClient(token=self.user_token)
            if self.bot_token:
                self.bot_client = WebClient(token=self.bot_token)
    
    def search_messages(self, query: str, count: int = 50) -> Dict[str, Any]:
        """メッセージを検索"""
        if self.user_client:
            try:
                response = self.user_client.search_messages(
                    query=query,
                    count=count,
                    sort="timestamp",
                    sort_dir="desc"
                )
                
                results = []
                for match in response.get("messages", {}).get("matches", []):
                    results.append({
                        "channel": match.get("channel", {}).get("name", "unknown"),
                        "user": match.get("username", "unknown"),
                        "text": match.get("text", ""),
                        "timestamp": match.get("ts", ""),
                        "permalink": match.get("permalink", ""),
                        "date": self._ts_to_date(match.get("ts", ""))
                    })
                
                return {
                    "query": query,
                    "total": response.get("messages", {}).get("total", 0),
                    "results": results
                }
            except SlackApiError as e:
                return {"error": str(e.response.get("error", "Unknown error"))}
        else:
            return self._get_mock_search_results(query)
    
    def get_channel_history(self, channel_id: str, days: int = 7) -> List[Dict[str, Any]]:
        """チャンネル履歴を取得"""
        if self.bot_client:
            try:
                oldest = (datetime.now() - timedelta(days=days)).timestamp()
                
                response = self.bot_client.conversations_history(
                    channel=channel_id,
                    oldest=str(oldest),
                    limit=200
                )
                
                messages = []
                for msg in response.get("messages", []):
                    messages.append({
                        "user": msg.get("user", "unknown"),
                        "text": msg.get("text", ""),
                        "timestamp": msg.get("ts", ""),
                        "date": self._ts_to_date(msg.get("ts", "")),
                        "reactions": [r["name"] for r in msg.get("reactions", [])]
                    })
                
                return messages
            except SlackApiError as e:
                return [{"error": str(e.response.get("error", "Unknown error"))}]
        else:
            return self._get_mock_channel_history()
    
    def _ts_to_date(self, ts: str) -> str:
        """タイムスタンプを日付文字列に変換"""
        try:
            return datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M")
        except:
            return "unknown"
    
    def _get_mock_search_results(self, query: str) -> Dict[str, Any]:
        """モック検索結果"""
        return {
            "query": query,
            "total": 5,
            "results": [
                {
                    "channel": "general",
                    "user": "tanaka",
                    "text": f"プロジェクトの進捗報告です。{query}に関する作業が80%完了しました。",
                    "timestamp": "1706745600.000100",
                    "permalink": "https://workspace.slack.com/archives/C01234/p1706745600000100",
                    "date": "2025-02-01 10:00"
                },
                {
                    "channel": "general",
                    "user": "suzuki",
                    "text": f"TODO: @tanaka {query}のレビューを明日までにお願いします",
                    "timestamp": "1706745500.000200",
                    "permalink": "https://workspace.slack.com/archives/C01234/p1706745500000200",
                    "date": "2025-02-01 09:58"
                },
                {
                    "channel": "project-alpha",
                    "user": "yamada",
                    "text": f"【確認】{query}の仕様について、MTGで決定した内容を共有します",
                    "timestamp": "1706745400.000300",
                    "permalink": "https://workspace.slack.com/archives/C01234/p1706745400000300",
                    "date": "2025-02-01 09:56"
                }
            ],
            "note": "モックデータ（Slack API未接続）"
        }
    
    def _get_mock_channel_history(self) -> List[Dict[str, Any]]:
        """モックチャンネル履歴"""
        return [
            {"user": "U001", "text": "おはようございます！", "timestamp": "1706745600", "date": "2025-02-01 10:00", "reactions": []},
            {"user": "U002", "text": "TODO: 今週中に資料を完成させてください", "timestamp": "1706745700", "date": "2025-02-01 10:01", "reactions": ["white_check_mark"]},
            {"user": "U001", "text": "【依頼】@suzuki レビューお願いします", "timestamp": "1706745800", "date": "2025-02-01 10:03", "reactions": []},
            {"user": "U003", "text": "明日のMTGは14時からです", "timestamp": "1706745900", "date": "2025-02-01 10:05", "reactions": ["eyes", "+1"]},
            {"user": "U002", "text": "確認お願い: 添付のスプレッドシートをチェックしてください", "timestamp": "1706746000", "date": "2025-02-01 10:06", "reactions": []}
        ]


class TaskExtractor:
    """タスク抽出クラス"""
    
    def extract_tasks(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """メッセージからタスクを抽出"""
        tasks = []
        
        for msg in messages:
            text = msg.get("text", "")
            extracted = self._extract_from_text(text)
            
            for task in extracted:
                task.update({
                    "source_user": msg.get("user", "unknown"),
                    "source_date": msg.get("date", "unknown"),
                    "source_channel": msg.get("channel", "unknown"),
                    "status": "pending"
                })
                tasks.append(task)
        
        return tasks
    
    def _extract_from_text(self, text: str) -> List[Dict[str, Any]]:
        """テキストからタスクを抽出"""
        tasks = []
        
        for pattern, task_type in TASK_PATTERNS:
            matches = re.findall(pattern, text, re.MULTILINE)
            for match in matches:
                task_text = match.strip() if isinstance(match, str) else match[0].strip()
                
                # 短すぎるものは除外
                if len(task_text) < 5:
                    continue
                
                task = {
                    "type": task_type,
                    "description": task_text,
                    "assignee": self._extract_mention(text),
                    "deadline": self._extract_deadline(text)
                }
                tasks.append(task)
        
        return tasks
    
    def _extract_mention(self, text: str) -> Optional[str]:
        """メンションを抽出"""
        mentions = re.findall(r"<@(\w+)>", text)
        return mentions[0] if mentions else None
    
    def _extract_deadline(self, text: str) -> Optional[str]:
        """期限を抽出"""
        for pattern, deadline_type in DEADLINE_PATTERNS:
            match = re.search(pattern, text)
            if match:
                if deadline_type == "today":
                    return datetime.now().strftime("%Y-%m-%d")
                elif deadline_type == "tomorrow":
                    return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                elif deadline_type == "this_week":
                    days_until_friday = (4 - datetime.now().weekday()) % 7
                    return (datetime.now() + timedelta(days=days_until_friday)).strftime("%Y-%m-%d")
                else:
                    return match.group(1)
        return None


def generate_task_report(tasks: List[Dict[str, Any]], output_path: str):
    """タスクレポートを生成"""
    report = f"""# 抽出タスク一覧

生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
総タスク数: {len(tasks)}

---

## タスク一覧

| # | 種類 | タスク内容 | 担当 | 期限 | ステータス |
|---|------|-----------|------|------|------------|
"""
    
    for i, task in enumerate(tasks, 1):
        report += f"| {i} | {task.get('type', '-')} | "
        report += f"{task.get('description', '-')[:50]} | "
        report += f"{task.get('assignee', '-')} | "
        report += f"{task.get('deadline', '-')} | "
        report += f"{task.get('status', 'pending')} |\n"
    
    report += """

---

## 統計

"""
    
    # タイプ別集計
    type_counts = {}
    for task in tasks:
        t = task.get("type", "その他")
        type_counts[t] = type_counts.get(t, 0) + 1
    
    report += "### タイプ別\n\n"
    for t, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        report += f"- {t}: {count}件\n"
    
    # 期限別
    with_deadline = sum(1 for t in tasks if t.get("deadline"))
    report += f"\n### 期限設定\n\n"
    report += f"- 期限あり: {with_deadline}件\n"
    report += f"- 期限なし: {len(tasks) - with_deadline}件\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ レポート生成: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Slack検索・タスク抽出スクリプト")
    subparsers = parser.add_subparsers(dest="command", help="コマンド")
    
    # search
    search_parser = subparsers.add_parser("search", help="メッセージ検索")
    search_parser.add_argument("--query", "-q", required=True, help="検索クエリ")
    search_parser.add_argument("--count", "-c", type=int, default=50, help="取得件数")
    search_parser.add_argument("--output", "-o", help="出力ファイル")
    
    # extract-tasks
    extract_parser = subparsers.add_parser("extract-tasks", help="タスク抽出")
    extract_parser.add_argument("--channel", required=True, help="チャンネルID")
    extract_parser.add_argument("--days", type=int, default=7, help="過去N日分")
    extract_parser.add_argument("--output", "-o", help="出力ファイル")
    extract_parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    
    # summarize
    summarize_parser = subparsers.add_parser("summarize", help="チャンネルサマリー")
    summarize_parser.add_argument("--channel", required=True, help="チャンネルID")
    summarize_parser.add_argument("--days", type=int, default=7, help="過去N日分")
    summarize_parser.add_argument("--output", "-o", help="出力ファイル")
    
    args = parser.parse_args()
    
    searcher = SlackSearcher()
    
    if args.command == "search":
        results = searcher.search_messages(args.query, args.count)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"✅ 検索結果を保存: {args.output}")
        else:
            print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif args.command == "extract-tasks":
        messages = searcher.get_channel_history(args.channel, args.days)
        
        extractor = TaskExtractor()
        tasks = extractor.extract_tasks(messages)
        
        print(f"\n抽出タスク: {len(tasks)}件")
        
        if args.output:
            if args.format == "markdown":
                generate_task_report(tasks, args.output)
            else:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(tasks, f, ensure_ascii=False, indent=2)
                print(f"✅ タスクを保存: {args.output}")
        else:
            for i, task in enumerate(tasks, 1):
                print(f"\n{i}. [{task['type']}] {task['description']}")
                if task.get('deadline'):
                    print(f"   期限: {task['deadline']}")
    
    elif args.command == "summarize":
        messages = searcher.get_channel_history(args.channel, args.days)
        
        summary = {
            "channel": args.channel,
            "period_days": args.days,
            "total_messages": len(messages),
            "unique_users": len(set(m.get("user") for m in messages)),
            "messages_with_reactions": sum(1 for m in messages if m.get("reactions")),
            "sample_messages": messages[:5]
        }
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            print(f"✅ サマリーを保存: {args.output}")
        else:
            print(json.dumps(summary, ensure_ascii=False, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
