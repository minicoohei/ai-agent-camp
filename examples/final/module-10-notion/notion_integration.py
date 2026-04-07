#!/usr/bin/env python3
"""
Notion API 連携スクリプト（Final Example）

Notion APIを使用してページ・データベースの操作を行います。

必要条件:
- Notion API キー（環境変数 NOTION_API_KEY）
- Python 3.9以上
- requests

使用方法:
    python notion_integration.py list-databases
    python notion_integration.py query --database-id <ID>
    python notion_integration.py create-page --database-id <ID> --title "タイトル"
    python notion_integration.py sync-tasks --database-id <ID>
"""

import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("Warning: requests がインストールされていません")


# Notion API設定
NOTION_VERSION = "2022-06-28"
NOTION_BASE_URL = "https://api.notion.com/v1"


class NotionClient:
    """Notion APIクライアント"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("NOTION_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION
        }
    
    def _request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """APIリクエストを実行"""
        if not HAS_REQUESTS:
            return self._mock_response(endpoint)
        
        if not self.api_key:
            return {"error": "NOTION_API_KEY が設定されていません", "mock": True}
        
        url = f"{NOTION_BASE_URL}/{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            return {"error": str(e), "status_code": response.status_code}
        except Exception as e:
            return {"error": str(e)}
    
    def list_databases(self) -> List[Dict]:
        """データベース一覧を取得"""
        result = self._request("POST", "search", {
            "filter": {"property": "object", "value": "database"}
        })
        
        if "results" in result:
            databases = []
            for db in result["results"]:
                databases.append({
                    "id": db["id"],
                    "title": self._get_title(db),
                    "url": db.get("url", ""),
                    "created_time": db.get("created_time", ""),
                    "last_edited_time": db.get("last_edited_time", "")
                })
            return databases
        
        return result.get("mock_databases", [])
    
    def query_database(self, database_id: str, filter_obj: Dict = None, 
                        sorts: List = None) -> List[Dict]:
        """データベースをクエリ"""
        data = {}
        if filter_obj:
            data["filter"] = filter_obj
        if sorts:
            data["sorts"] = sorts
        
        result = self._request("POST", f"databases/{database_id}/query", data)
        
        if "results" in result:
            return [self._parse_page(page) for page in result["results"]]
        
        return result.get("mock_results", [])
    
    def create_page(self, database_id: str, properties: Dict, 
                     content: List[Dict] = None) -> Dict:
        """ページを作成"""
        data = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        
        if content:
            data["children"] = content
        
        result = self._request("POST", "pages", data)
        
        if "id" in result:
            return {
                "success": True,
                "page_id": result["id"],
                "url": result.get("url", "")
            }
        
        return result
    
    def update_page(self, page_id: str, properties: Dict) -> Dict:
        """ページを更新"""
        result = self._request("PATCH", f"pages/{page_id}", {
            "properties": properties
        })
        
        if "id" in result:
            return {"success": True, "page_id": result["id"]}
        
        return result
    
    def get_page(self, page_id: str) -> Dict:
        """ページを取得"""
        result = self._request("GET", f"pages/{page_id}")
        
        if "id" in result:
            return self._parse_page(result)
        
        return result
    
    def _get_title(self, obj: Dict) -> str:
        """タイトルを抽出"""
        try:
            title_prop = obj.get("title", [])
            if title_prop:
                return title_prop[0].get("plain_text", "")
        except:
            pass
        return "Untitled"
    
    def _parse_page(self, page: Dict) -> Dict:
        """ページデータをパース"""
        parsed = {
            "id": page.get("id", ""),
            "url": page.get("url", ""),
            "created_time": page.get("created_time", ""),
            "last_edited_time": page.get("last_edited_time", ""),
            "properties": {}
        }
        
        for key, prop in page.get("properties", {}).items():
            parsed["properties"][key] = self._parse_property(prop)
        
        return parsed
    
    def _parse_property(self, prop: Dict) -> Any:
        """プロパティ値をパース"""
        prop_type = prop.get("type", "")
        
        if prop_type == "title":
            texts = prop.get("title", [])
            return "".join(t.get("plain_text", "") for t in texts)
        
        elif prop_type == "rich_text":
            texts = prop.get("rich_text", [])
            return "".join(t.get("plain_text", "") for t in texts)
        
        elif prop_type == "number":
            return prop.get("number")
        
        elif prop_type == "select":
            select = prop.get("select")
            return select.get("name", "") if select else None
        
        elif prop_type == "multi_select":
            return [s.get("name", "") for s in prop.get("multi_select", [])]
        
        elif prop_type == "date":
            date_obj = prop.get("date")
            if date_obj:
                return {
                    "start": date_obj.get("start"),
                    "end": date_obj.get("end")
                }
            return None
        
        elif prop_type == "checkbox":
            return prop.get("checkbox", False)
        
        elif prop_type == "url":
            return prop.get("url")
        
        elif prop_type == "email":
            return prop.get("email")
        
        elif prop_type == "status":
            status = prop.get("status")
            return status.get("name", "") if status else None
        
        elif prop_type == "people":
            return [p.get("name", "") for p in prop.get("people", [])]
        
        return prop.get(prop_type)
    
    def _mock_response(self, endpoint: str) -> Dict:
        """モックレスポンス"""
        if "search" in endpoint:
            return {
                "mock_databases": [
                    {
                        "id": "abc123",
                        "title": "タスク管理",
                        "url": "https://notion.so/abc123",
                        "created_time": "2025-01-01T00:00:00.000Z"
                    },
                    {
                        "id": "def456",
                        "title": "プロジェクト一覧",
                        "url": "https://notion.so/def456",
                        "created_time": "2025-01-15T00:00:00.000Z"
                    }
                ],
                "note": "モックデータ（API未接続）"
            }
        
        if "query" in endpoint:
            return {
                "mock_results": [
                    {
                        "id": "page1",
                        "properties": {
                            "タスク名": "ドキュメント作成",
                            "ステータス": "進行中",
                            "期限": {"start": "2025-02-10"},
                            "担当者": ["田中"]
                        }
                    },
                    {
                        "id": "page2",
                        "properties": {
                            "タスク名": "レビュー依頼",
                            "ステータス": "未着手",
                            "期限": {"start": "2025-02-15"},
                            "担当者": ["鈴木"]
                        }
                    }
                ],
                "note": "モックデータ"
            }
        
        return {"mock": True, "note": "API未接続のためモックレスポンスを返しています"}


class TaskSync:
    """タスク同期クラス"""
    
    def __init__(self, client: NotionClient):
        self.client = client
    
    def sync_from_slack_tasks(self, database_id: str, tasks: List[Dict]) -> Dict:
        """Slackから抽出したタスクをNotionに同期"""
        results = {"created": 0, "updated": 0, "errors": []}
        
        # 既存タスクを取得
        existing = self.client.query_database(database_id)
        existing_titles = {
            p.get("properties", {}).get("タスク名", ""): p.get("id")
            for p in existing
        }
        
        for task in tasks:
            title = task.get("description", "")[:100]
            
            properties = {
                "タスク名": {
                    "title": [{"text": {"content": title}}]
                },
                "ステータス": {
                    "status": {"name": "未着手"}
                },
                "ソース": {
                    "rich_text": [{"text": {"content": "Slack"}}]
                }
            }
            
            # 期限があれば設定
            if task.get("deadline"):
                properties["期限"] = {
                    "date": {"start": task["deadline"]}
                }
            
            # 担当者（メンション）があれば設定
            if task.get("assignee"):
                properties["担当メモ"] = {
                    "rich_text": [{"text": {"content": task["assignee"]}}]
                }
            
            # 既存タスクがあれば更新、なければ作成
            if title in existing_titles:
                result = self.client.update_page(existing_titles[title], properties)
                if result.get("success"):
                    results["updated"] += 1
                else:
                    results["errors"].append(result)
            else:
                result = self.client.create_page(database_id, properties)
                if result.get("success"):
                    results["created"] += 1
                else:
                    results["errors"].append(result)
        
        return results
    
    def get_overdue_tasks(self, database_id: str) -> List[Dict]:
        """期限切れタスクを取得"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        filter_obj = {
            "and": [
                {
                    "property": "期限",
                    "date": {"before": today}
                },
                {
                    "property": "ステータス",
                    "status": {"does_not_equal": "完了"}
                }
            ]
        }
        
        return self.client.query_database(database_id, filter_obj)
    
    def get_this_week_tasks(self, database_id: str) -> List[Dict]:
        """今週のタスクを取得"""
        today = datetime.now()
        week_end = today + timedelta(days=(6 - today.weekday()))
        
        filter_obj = {
            "and": [
                {
                    "property": "期限",
                    "date": {"on_or_before": week_end.strftime("%Y-%m-%d")}
                },
                {
                    "property": "ステータス",
                    "status": {"does_not_equal": "完了"}
                }
            ]
        }
        
        sorts = [{"property": "期限", "direction": "ascending"}]
        
        return self.client.query_database(database_id, filter_obj, sorts)


def create_property_builders():
    """プロパティビルダー（ヘルパー関数集）"""
    
    def title(text: str) -> Dict:
        return {"title": [{"text": {"content": text}}]}
    
    def rich_text(text: str) -> Dict:
        return {"rich_text": [{"text": {"content": text}}]}
    
    def number(value: float) -> Dict:
        return {"number": value}
    
    def select(name: str) -> Dict:
        return {"select": {"name": name}}
    
    def multi_select(names: List[str]) -> Dict:
        return {"multi_select": [{"name": n} for n in names]}
    
    def date(start: str, end: str = None) -> Dict:
        d = {"date": {"start": start}}
        if end:
            d["date"]["end"] = end
        return d
    
    def checkbox(checked: bool) -> Dict:
        return {"checkbox": checked}
    
    def url(url_str: str) -> Dict:
        return {"url": url_str}
    
    def status(name: str) -> Dict:
        return {"status": {"name": name}}
    
    return {
        "title": title,
        "rich_text": rich_text,
        "number": number,
        "select": select,
        "multi_select": multi_select,
        "date": date,
        "checkbox": checkbox,
        "url": url,
        "status": status
    }


def main():
    parser = argparse.ArgumentParser(description="Notion API連携スクリプト")
    subparsers = parser.add_subparsers(dest="command", help="コマンド")
    
    # list-databases
    subparsers.add_parser("list-databases", help="データベース一覧")
    
    # query
    query_parser = subparsers.add_parser("query", help="データベースクエリ")
    query_parser.add_argument("--database-id", "-d", required=True, help="データベースID")
    query_parser.add_argument("--output", "-o", help="出力ファイル")
    
    # create-page
    create_parser = subparsers.add_parser("create-page", help="ページ作成")
    create_parser.add_argument("--database-id", "-d", required=True, help="データベースID")
    create_parser.add_argument("--title", "-t", required=True, help="タイトル")
    create_parser.add_argument("--status", "-s", default="未着手", help="ステータス")
    create_parser.add_argument("--deadline", help="期限 (YYYY-MM-DD)")
    
    # sync-tasks
    sync_parser = subparsers.add_parser("sync-tasks", help="タスク同期")
    sync_parser.add_argument("--database-id", "-d", required=True, help="データベースID")
    sync_parser.add_argument("--tasks-file", "-f", help="タスクJSONファイル")
    
    # overdue
    overdue_parser = subparsers.add_parser("overdue", help="期限切れタスク")
    overdue_parser.add_argument("--database-id", "-d", required=True, help="データベースID")
    
    # this-week
    week_parser = subparsers.add_parser("this-week", help="今週のタスク")
    week_parser.add_argument("--database-id", "-d", required=True, help="データベースID")
    
    args = parser.parse_args()
    
    client = NotionClient()
    
    if args.command == "list-databases":
        databases = client.list_databases()
        print("\nデータベース一覧:")
        for db in databases:
            print(f"\n  ID: {db.get('id', 'N/A')}")
            print(f"  タイトル: {db.get('title', 'Untitled')}")
            print(f"  URL: {db.get('url', 'N/A')}")
    
    elif args.command == "query":
        results = client.query_database(args.database_id)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"✅ 結果を保存: {args.output}")
        else:
            print(f"\n取得件数: {len(results)}")
            print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif args.command == "create-page":
        props = create_property_builders()
        
        properties = {
            "タスク名": props["title"](args.title),
            "ステータス": props["status"](args.status)
        }
        
        if args.deadline:
            properties["期限"] = props["date"](args.deadline)
        
        result = client.create_page(args.database_id, properties)
        print("\nページ作成結果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "sync-tasks":
        syncer = TaskSync(client)
        
        if args.tasks_file and os.path.exists(args.tasks_file):
            with open(args.tasks_file, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
        else:
            # サンプルタスク
            tasks = [
                {"description": "レポート作成", "deadline": "2025-02-10", "assignee": "tanaka"},
                {"description": "ミーティング準備", "deadline": "2025-02-08"}
            ]
            print("サンプルタスクを使用します")
        
        result = syncer.sync_from_slack_tasks(args.database_id, tasks)
        print("\n同期結果:")
        print(f"  作成: {result['created']}件")
        print(f"  更新: {result['updated']}件")
        if result['errors']:
            print(f"  エラー: {len(result['errors'])}件")
    
    elif args.command == "overdue":
        syncer = TaskSync(client)
        tasks = syncer.get_overdue_tasks(args.database_id)
        
        print(f"\n期限切れタスク: {len(tasks)}件")
        for task in tasks:
            props = task.get("properties", {})
            print(f"  - {props.get('タスク名', 'N/A')} (期限: {props.get('期限', {}).get('start', 'N/A')})")
    
    elif args.command == "this-week":
        syncer = TaskSync(client)
        tasks = syncer.get_this_week_tasks(args.database_id)
        
        print(f"\n今週のタスク: {len(tasks)}件")
        for task in tasks:
            props = task.get("properties", {})
            print(f"  - {props.get('タスク名', 'N/A')} [{props.get('ステータス', 'N/A')}]")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
