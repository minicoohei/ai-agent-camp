#!/usr/bin/env python3
"""
Slack検索Skillツール

BookRAGに基づく階層的インデックスを活用した
Serena風セマンティック検索を提供する。

使用方法:
    from tools.slack_search import SlackSearch
    
    search = SlackSearch()
    
    # ワークスペース概要
    overview = search.get_workspace_overview()
    
    # チャンネル検索
    results = search.find_channels("DX展示会")
    
    # チャンネル詳細
    detail = search.get_channel_detail("infobox/buyingshift")
    
    # 関連チャンネル
    related = search.find_related_channels("infobox/buyingshift")
    
    # 人物検索
    person = search.find_person("清水")
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from difflib import SequenceMatcher


class SlackSearch:
    """BookRAGインデックスを活用したSlack検索クラス"""
    
    def __init__(self, index_path: Optional[str] = None):
        """
        Args:
            index_path: book_index.jsonのパス（省略時は自動検出）
        """
        if index_path is None:
            # 自動検出
            base_dir = Path(__file__).parent.parent
            index_path = base_dir / "slack-sync" / "index" / "book_index.json"
        
        self.index_path = Path(index_path)
        self._index = None
        self._load_index()
    
    def _load_index(self):
        """インデックスを読み込む"""
        if not self.index_path.exists():
            raise FileNotFoundError(f"Index not found: {self.index_path}")
        
        with open(self.index_path, "r", encoding="utf-8") as f:
            self._index = json.load(f)
    
    def reload_index(self):
        """インデックスを再読み込み"""
        self._load_index()
    
    # =========================================================================
    # 1. ワークスペース概要
    # =========================================================================
    
    def get_workspace_overview(self, workspace: Optional[str] = None) -> Dict[str, Any]:
        """
        ワークスペース全体の概要を取得
        
        Args:
            workspace: 特定のワークスペースに絞る場合（省略時は全体）
        
        Returns:
            ワークスペースの統計情報と階層構造
        """
        if workspace:
            if workspace not in self._index["workspaces"]:
                return {"error": f"Unknown workspace: {workspace}"}
            
            tree = self._index["tree"].get(workspace, {})
            channels = {
                cid: ch for cid, ch in self._index["channels"].items()
                if ch["workspace"] == workspace
            }
            
            return {
                "workspace": workspace,
                "channel_count": len(channels),
                "categories": {
                    cat: len(ch_list) for cat, ch_list in tree.items()
                },
                "tree": tree,
            }
        
        # 全体の概要
        return {
            "version": self._index["version"],
            "generated_at": self._index["generated_at"],
            "stats": self._index["stats"],
            "workspaces": {
                ws: {
                    "categories": {
                        cat: len(ch_list) 
                        for cat, ch_list in self._index["tree"].get(ws, {}).items()
                    }
                }
                for ws in self._index["workspaces"]
            },
            "output_sources": self._index.get("output_sources", {}),
        }
    
    # =========================================================================
    # 2. チャンネル検索（セマンティック検索）
    # =========================================================================
    
    def find_channels(
        self,
        query: str,
        workspace: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        チャンネル名・トピック・概要でセマンティック検索
        
        Args:
            query: 検索クエリ
            workspace: ワークスペースで絞り込み
            category: カテゴリで絞り込み
            limit: 最大結果数
        
        Returns:
            マッチしたチャンネルのリスト（スコア順）
        """
        results = []
        query_lower = query.lower()
        query_tokens = set(query_lower.split())
        
        for channel_id, channel in self._index["channels"].items():
            # フィルタリング
            if workspace and channel["workspace"] != workspace:
                continue
            if category and channel["category"] != category:
                continue
            
            # スコア計算
            score = self._calculate_search_score(query_lower, query_tokens, channel)
            
            if score > 0:
                results.append({
                    "channel_id": channel_id,
                    "name": channel["name"],
                    "workspace": channel["workspace"],
                    "category": channel["category"],
                    "score": score,
                    "overview": channel.get("overview", "")[:200],
                    "topics": channel.get("topics", [])[:5],
                    "paths": channel["paths"],
                })
        
        # スコアでソート
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:limit]
    
    def _calculate_search_score(
        self,
        query_lower: str,
        query_tokens: set,
        channel: Dict
    ) -> float:
        """検索スコアを計算"""
        score = 0.0
        
        name = channel["name"].lower()
        overview = channel.get("overview", "").lower()
        topics = [t.lower() for t in channel.get("topics", [])]
        
        # 名前の完全一致（最高スコア）
        if query_lower == name:
            score += 10.0
        # 名前に含まれる
        elif query_lower in name:
            score += 5.0
        # 名前の類似度
        else:
            similarity = SequenceMatcher(None, query_lower, name).ratio()
            score += similarity * 3.0
        
        # トピックとのマッチ
        for topic in topics:
            if query_lower in topic:
                score += 2.0
            for token in query_tokens:
                if token in topic:
                    score += 0.5
        
        # 概要とのマッチ
        if query_lower in overview:
            score += 1.5
        for token in query_tokens:
            if token in overview:
                score += 0.3
        
        # アクティビティボーナス（最近活動があるチャンネルを優先）
        if channel["metadata"].get("last_activity"):
            try:
                last_date = datetime.fromisoformat(channel["metadata"]["last_activity"])
                days_ago = (datetime.now() - last_date).days
                if days_ago < 30:
                    score += 0.5
                elif days_ago < 90:
                    score += 0.2
            except:
                pass
        
        return score
    
    # =========================================================================
    # 3. チャンネル詳細
    # =========================================================================
    
    def get_channel_detail(self, channel_id: str) -> Dict[str, Any]:
        """
        チャンネルの詳細情報を取得
        
        Args:
            channel_id: チャンネルID（workspace/channel_name形式）
                        または channel_name のみ（自動検索）
        
        Returns:
            チャンネルの詳細情報
        """
        # channel_idを正規化
        if "/" not in channel_id:
            # チャンネル名だけの場合、検索
            for cid, ch in self._index["channels"].items():
                if ch["name"] == channel_id:
                    channel_id = cid
                    break
            else:
                return {"error": f"Channel not found: {channel_id}"}
        
        if channel_id not in self._index["channels"]:
            return {"error": f"Channel not found: {channel_id}"}
        
        channel = self._index["channels"][channel_id]
        
        return {
            "channel_id": channel_id,
            "name": channel["name"],
            "workspace": channel["workspace"],
            "category": channel["category"],
            "overview": channel.get("overview", ""),
            "topics": channel.get("topics", []),
            "metadata": channel["metadata"],
            "paths": channel["paths"],
            "related_channels": channel.get("related_channels", []),
            "archived": channel.get("archived", False),
        }
    
    # =========================================================================
    # 4. 関連チャンネル探索
    # =========================================================================
    
    def find_related_channels(
        self,
        channel_id: str,
        depth: int = 1
    ) -> Dict[str, Any]:
        """
        関連チャンネルを探索（グラフ探索）
        
        Args:
            channel_id: 起点チャンネルID
            depth: 探索の深さ（1=直接関連、2=間接関連）
        
        Returns:
            関連チャンネルのグラフ構造
        """
        # channel_idを正規化
        if "/" not in channel_id:
            for cid, ch in self._index["channels"].items():
                if ch["name"] == channel_id:
                    channel_id = cid
                    break
        
        if channel_id not in self._index["channels"]:
            return {"error": f"Channel not found: {channel_id}"}
        
        visited = {channel_id}
        levels = [{channel_id: self._index["channels"][channel_id]}]
        
        for d in range(depth):
            current_level = {}
            for cid in levels[-1]:
                channel = self._index["channels"].get(cid, {})
                for related_id in channel.get("related_channels", []):
                    if related_id not in visited and related_id in self._index["channels"]:
                        visited.add(related_id)
                        current_level[related_id] = self._index["channels"][related_id]
            
            if current_level:
                levels.append(current_level)
        
        return {
            "origin": channel_id,
            "depth": depth,
            "levels": [
                {
                    cid: {
                        "name": ch["name"],
                        "workspace": ch["workspace"],
                        "category": ch["category"],
                    }
                    for cid, ch in level.items()
                }
                for level in levels
            ],
            "total_related": sum(len(level) for level in levels) - 1,
        }
    
    # =========================================================================
    # 5. 人物検索
    # =========================================================================
    
    def find_person(
        self,
        query: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        人物を検索
        
        Args:
            query: 検索クエリ（名前の一部）
            limit: 最大結果数
        
        Returns:
            マッチした人物のリスト
        """
        results = []
        query_lower = query.lower()
        
        for name, info in self._index["entities"]["persons"].items():
            name_lower = name.lower()
            
            # スコア計算
            score = 0.0
            if query_lower == name_lower:
                score = 10.0
            elif query_lower in name_lower:
                score = 5.0
            else:
                # エイリアスもチェック
                for alias in info.get("aliases", []):
                    if query_lower in alias.lower():
                        score = 3.0
                        break
            
            if score > 0:
                results.append({
                    "name": name,
                    "aliases": info.get("aliases", []),
                    "channel_count": len(info.get("channels", [])),
                    "channels": info.get("channels", [])[:10],
                    "mention_count": info.get("mention_count", 0),
                    "score": score,
                })
        
        results.sort(key=lambda x: (-x["score"], -x["channel_count"]))
        return results[:limit]
    
    # =========================================================================
    # 6. イベント検索
    # =========================================================================
    
    def find_events(
        self,
        query: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        イベントを検索
        
        Args:
            query: 検索クエリ（省略時は全イベント）
            limit: 最大結果数
        
        Returns:
            マッチしたイベントのリスト
        """
        results = []
        
        for name, info in self._index["entities"]["events"].items():
            if query:
                if query.lower() not in name.lower():
                    continue
            
            results.append({
                "name": name,
                "channel": info.get("channel"),
                "date": info.get("date"),
                "participants": info.get("participants", [])[:10],
                "topics": info.get("topics", []),
            })
        
        # 日付でソート（新しい順）
        results.sort(key=lambda x: x.get("date") or "", reverse=True)
        return results[:limit]
    
    # =========================================================================
    # 7. カテゴリ別チャンネル一覧
    # =========================================================================
    
    def list_channels_by_category(
        self,
        category: str,
        workspace: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        カテゴリ別にチャンネルを一覧
        
        Args:
            category: カテゴリ名
            workspace: ワークスペースで絞り込み
        
        Returns:
            チャンネルのリスト
        """
        results = []
        
        for channel_id, channel in self._index["channels"].items():
            if channel["category"] != category:
                continue
            if workspace and channel["workspace"] != workspace:
                continue
            
            results.append({
                "channel_id": channel_id,
                "name": channel["name"],
                "workspace": channel["workspace"],
                "overview": channel.get("overview", "")[:100],
                "message_count": channel["metadata"].get("message_count", 0),
                "last_activity": channel["metadata"].get("last_activity"),
            })
        
        # 最終活動日でソート
        results.sort(key=lambda x: x.get("last_activity") or "", reverse=True)
        return results
    
    # =========================================================================
    # 8. タイムライン（時系列検索）
    # =========================================================================
    
    def get_timeline(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        workspace: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        時系列でアクティビティを取得
        
        Args:
            start_date: 開始日（YYYY-MM-DD形式）
            end_date: 終了日（YYYY-MM-DD形式）
            workspace: ワークスペースで絞り込み
        
        Returns:
            期間内にアクティビティがあったチャンネル
        """
        results = []
        
        for channel_id, channel in self._index["channels"].items():
            if workspace and channel["workspace"] != workspace:
                continue
            
            first = channel["metadata"].get("first_activity")
            last = channel["metadata"].get("last_activity")
            
            if not first or not last:
                continue
            
            # 期間フィルタ
            if start_date and last < start_date:
                continue
            if end_date and first > end_date:
                continue
            
            results.append({
                "channel_id": channel_id,
                "name": channel["name"],
                "workspace": channel["workspace"],
                "category": channel["category"],
                "first_activity": first,
                "last_activity": last,
                "message_count": channel["metadata"].get("message_count", 0),
            })
        
        # 最終活動日でソート
        results.sort(key=lambda x: x["last_activity"], reverse=True)
        
        return {
            "period": {
                "start": start_date,
                "end": end_date,
            },
            "workspace": workspace,
            "channel_count": len(results),
            "channels": results,
        }
    
    # =========================================================================
    # 9. 出力ソース検索（calendar, gmail, drive, voicememo）
    # =========================================================================
    
    def get_output_sources(self) -> Dict[str, Any]:
        """
        出力ソース（calendar, gmail等）の情報を取得
        
        Returns:
            出力ソースの統計情報
        """
        return self._index.get("output_sources", {})


# =========================================================================
# CLI インターフェース
# =========================================================================

def main():
    """CLIからの実行"""
    import sys
    
    search = SlackSearch()
    
    if len(sys.argv) < 2:
        print("Usage: python slack_search.py <command> [args]")
        print("Commands:")
        print("  overview [workspace]     - ワークスペース概要")
        print("  find <query>             - チャンネル検索")
        print("  detail <channel_id>      - チャンネル詳細")
        print("  related <channel_id>     - 関連チャンネル")
        print("  person <name>            - 人物検索")
        print("  events [query]           - イベント検索")
        print("  category <category>      - カテゴリ別一覧")
        print("  timeline [start] [end]   - タイムライン")
        return
    
    command = sys.argv[1]
    
    if command == "overview":
        workspace = sys.argv[2] if len(sys.argv) > 2 else None
        result = search.get_workspace_overview(workspace)
    
    elif command == "find":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        result = search.find_channels(query)
    
    elif command == "detail":
        channel_id = sys.argv[2] if len(sys.argv) > 2 else ""
        result = search.get_channel_detail(channel_id)
    
    elif command == "related":
        channel_id = sys.argv[2] if len(sys.argv) > 2 else ""
        result = search.find_related_channels(channel_id)
    
    elif command == "person":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        result = search.find_person(query)
    
    elif command == "events":
        query = sys.argv[2] if len(sys.argv) > 2 else None
        result = search.find_events(query)
    
    elif command == "category":
        category = sys.argv[2] if len(sys.argv) > 2 else ""
        result = search.list_channels_by_category(category)
    
    elif command == "timeline":
        start = sys.argv[2] if len(sys.argv) > 2 else None
        end = sys.argv[3] if len(sys.argv) > 3 else None
        result = search.get_timeline(start, end)
    
    else:
        print(f"Unknown command: {command}")
        return
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
