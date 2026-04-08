#!/usr/bin/env python3
"""
BookIndex生成スクリプト

BookRAG論文に基づく階層的インデックスを構築する。
- 4ワークスペース（infobox, yoake, tokenpocket, fungiblex）を解析
- 3データソース（data, summary, archive）を統合
- チャンネル分類ルールに基づいて階層ツリーを構築
- エンティティ（人物、イベント）を抽出
"""

import json
import re
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Set, Optional, Any

# ベースパス
BASE_DIR = Path(__file__).parent.parent.parent
SLACK_SYNC_DIR = BASE_DIR / "slack-sync"
OUTPUT_DIR = BASE_DIR / "output"
INDEX_DIR = SLACK_SYNC_DIR / "index"

# ワークスペース一覧
WORKSPACES = ["infobox", "yoake", "tokenpocket", "fungiblex"]

# チャンネル分類ルール（プレフィックス -> カテゴリ）
CATEGORY_RULES = [
    (r"^cafe_", "cafe"),
    (r"^times_", "times"),
    (r"^pj_", "project"),
    (r"^pj-", "project"),
    (r"^product_", "product"),
    (r"^product-", "product"),
    (r"^sales_", "sales"),
    (r"^sales-", "sales"),
    (r"^notify_", "notify"),
    (r"^notify-", "notify"),
    (r"^biz-", "business"),
    (r"^biz_", "business"),
    (r"^dev-", "development"),
    (r"^dev_", "development"),
    (r"^corp-", "corporate"),
    (r"^corp_", "corporate"),
    (r"^ex-", "external"),
    (r"^ext-", "external"),
    (r"^shared-", "external"),
    (r"_infobox$", "partner"),
    (r"^x2y2", "x2y2"),
    (r"^sentry", "notify"),
    (r"^ap-", "accounting"),
    (r"^all-", "general"),
    (r"^team-", "team"),
    (r"^topic-", "topic"),
    (r"^record-", "record"),
    (r"^rss-", "rss"),
    (r"^exec-", "executive"),
    # 日付パターン（イベント）
    (r"^\d{4}", "event"),
    (r"^\d{6}_", "event"),
]


def classify_channel(channel_name: str) -> str:
    """チャンネル名からカテゴリを判定"""
    for pattern, category in CATEGORY_RULES:
        if re.search(pattern, channel_name, re.IGNORECASE):
            return category
    return "other"


def extract_participants(content: str) -> Set[str]:
    """Markdownコンテンツから発言者を抽出"""
    participants = set()
    # ### HH:MM - {名前} パターン
    pattern = r"^### \d{2}:\d{2} - (.+?)(?:\s*\[\[Slack\]\])?$"
    for match in re.finditer(pattern, content, re.MULTILINE):
        name = match.group(1).strip()
        if name:
            participants.add(name)
    return participants


def extract_mentions(content: str) -> Set[str]:
    """メンションを抽出"""
    mentions = set()
    # @メンション パターン
    pattern = r"@([A-Za-z0-9_.]+(?:\s+[A-Za-z0-9_.]+)?)"
    for match in re.finditer(pattern, content):
        mention = match.group(1).strip()
        if mention and len(mention) > 2:
            mentions.add(mention)
    return mentions


def extract_dates(content: str) -> tuple[Optional[str], Optional[str]]:
    """最初と最後の日付を抽出"""
    pattern = r"^## (\d{4}-\d{2}-\d{2})$"
    dates = re.findall(pattern, content, re.MULTILINE)
    if dates:
        return dates[-1], dates[0]  # 古い順、新しい順
    return None, None


def extract_topics_from_summary(content: str) -> List[str]:
    """サマリーから主なトピックを抽出"""
    topics = []
    # ## 主なトピック セクションを探す
    pattern = r"## 主なトピック\n([\s\S]*?)(?=\n## |$)"
    match = re.search(pattern, content)
    if match:
        topic_section = match.group(1)
        # - で始まる行を抽出
        for line in topic_section.split("\n"):
            line = line.strip()
            if line.startswith("-"):
                topic = line[1:].strip()
                if topic:
                    topics.append(topic)
    return topics


def count_messages(content: str) -> int:
    """メッセージ数をカウント"""
    pattern = r"^### \d{2}:\d{2} -"
    return len(re.findall(pattern, content, re.MULTILINE))


def parse_channel_file(file_path: Path) -> Dict[str, Any]:
    """チャンネルファイルを解析"""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return {}
    
    participants = extract_participants(content)
    mentions = extract_mentions(content)
    first_date, last_date = extract_dates(content)
    message_count = count_messages(content)
    
    return {
        "participants": list(participants),
        "mentions": list(mentions),
        "first_activity": first_date,
        "last_activity": last_date,
        "message_count": message_count,
    }


def parse_summary_file(file_path: Path) -> Dict[str, Any]:
    """サマリーファイルを解析"""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return {}
    
    topics = extract_topics_from_summary(content)
    
    # 概要を抽出
    overview_pattern = r"## 概要\n([\s\S]*?)(?=\n## |$)"
    overview_match = re.search(overview_pattern, content)
    overview = overview_match.group(1).strip() if overview_match else ""
    
    return {
        "topics": topics,
        "overview": overview,
    }


def build_channel_index(workspace: str) -> Dict[str, Dict]:
    """ワークスペースのチャンネルインデックスを構築"""
    channels = {}
    
    data_dir = SLACK_SYNC_DIR / "data" / workspace
    summary_dir = SLACK_SYNC_DIR / "data" / "summary" / workspace
    archive_dir = SLACK_SYNC_DIR / "data" / "archive" / workspace
    
    # データディレクトリをスキャン
    if data_dir.exists():
        for file_path in data_dir.glob("*.md"):
            channel_name = file_path.stem
            channel_id = f"{workspace}/{channel_name}"
            
            # ファイル解析
            data_info = parse_channel_file(file_path)
            
            # サマリーファイルを探す
            summary_path = summary_dir / f"{channel_name}_summary.md"
            summary_info = {}
            if summary_path.exists():
                summary_info = parse_summary_file(summary_path)
            
            # アーカイブの存在確認
            archive_path = archive_dir / f"{channel_name}.md"
            has_archive = archive_path.exists()
            
            channels[channel_id] = {
                "name": channel_name,
                "workspace": workspace,
                "category": classify_channel(channel_name),
                "paths": {
                    "data": str(file_path.relative_to(BASE_DIR)),
                    "summary": str(summary_path.relative_to(BASE_DIR)) if summary_path.exists() else None,
                    "archive": str(archive_path.relative_to(BASE_DIR)) if has_archive else None,
                },
                "metadata": {
                    "first_activity": data_info.get("first_activity"),
                    "last_activity": data_info.get("last_activity"),
                    "message_count": data_info.get("message_count", 0),
                    "participants": data_info.get("participants", []),
                },
                "topics": summary_info.get("topics", []),
                "overview": summary_info.get("overview", ""),
            }
    
    # アーカイブのみに存在するチャンネルも追加
    if archive_dir.exists():
        for file_path in archive_dir.glob("*.md"):
            channel_name = file_path.stem
            channel_id = f"{workspace}/{channel_name}"
            
            if channel_id not in channels:
                data_info = parse_channel_file(file_path)
                
                # サマリーファイルを探す
                summary_path = summary_dir / f"{channel_name}_summary.md"
                summary_info = {}
                if summary_path.exists():
                    summary_info = parse_summary_file(summary_path)
                
                channels[channel_id] = {
                    "name": channel_name,
                    "workspace": workspace,
                    "category": classify_channel(channel_name),
                    "paths": {
                        "data": None,
                        "summary": str(summary_path.relative_to(BASE_DIR)) if summary_path.exists() else None,
                        "archive": str(file_path.relative_to(BASE_DIR)),
                    },
                    "metadata": {
                        "first_activity": data_info.get("first_activity"),
                        "last_activity": data_info.get("last_activity"),
                        "message_count": data_info.get("message_count", 0),
                        "participants": data_info.get("participants", []),
                    },
                    "topics": summary_info.get("topics", []),
                    "overview": summary_info.get("overview", ""),
                    "archived": True,
                }
    
    return channels


def build_hierarchy_tree(channels: Dict[str, Dict]) -> Dict:
    """チャンネルから階層ツリーを構築"""
    tree = defaultdict(lambda: defaultdict(list))
    
    for channel_id, channel_info in channels.items():
        workspace = channel_info["workspace"]
        category = channel_info["category"]
        tree[workspace][category].append(channel_info["name"])
    
    # defaultdictを通常のdictに変換
    return {
        workspace: {
            category: sorted(channels)
            for category, channels in categories.items()
        }
        for workspace, categories in tree.items()
    }


def extract_entities(channels: Dict[str, Dict]) -> Dict:
    """エンティティ（人物、イベント）を抽出"""
    persons = defaultdict(lambda: {"channels": [], "mention_count": 0, "aliases": set()})
    events = {}
    
    for channel_id, channel_info in channels.items():
        # 人物を抽出
        for participant in channel_info["metadata"].get("participants", []):
            # 名前の正規化
            normalized_name = normalize_person_name(participant)
            persons[normalized_name]["channels"].append(channel_id)
            persons[normalized_name]["aliases"].add(participant)
            persons[normalized_name]["mention_count"] += 1
        
        # イベントを抽出（カテゴリがeventのチャンネル）
        if channel_info["category"] == "event":
            event_name = channel_info["name"]
            events[event_name] = {
                "channel": channel_id,
                "date": channel_info["metadata"].get("first_activity"),
                "participants": channel_info["metadata"].get("participants", []),
                "topics": channel_info.get("topics", []),
            }
    
    # aliasesをリストに変換
    for name in persons:
        persons[name]["aliases"] = list(persons[name]["aliases"])
    
    return {
        "persons": dict(persons),
        "events": events,
    }


def normalize_person_name(name: str) -> str:
    """人物名を正規化"""
    # 括弧内の情報を除去
    name = re.sub(r"\s*[\(（].*?[\)）]", "", name)
    # 末尾の日付情報を除去
    name = re.sub(r"\s*\[\d+/\d+.*?\]", "", name)
    # 前後の空白を除去
    return name.strip()


def build_output_index() -> Dict:
    """outputディレクトリのインデックスを構築"""
    output_index = {}
    
    # Calendar
    calendar_dir = OUTPUT_DIR / "calendar"
    if calendar_dir.exists():
        files = sorted([f.name for f in calendar_dir.glob("*.md")])
        dates = [f.replace("_events.md", "") for f in files]
        output_index["calendar"] = {
            "path": "output/calendar/",
            "files": files,
            "date_range": [dates[0], dates[-1]] if dates else [],
        }
    
    # Gmail
    gmail_dir = OUTPUT_DIR / "gmail"
    if gmail_dir.exists():
        file_count = len(list(gmail_dir.glob("*.md")))
        output_index["gmail"] = {
            "path": "output/gmail/",
            "file_count": file_count,
        }
    
    # Drive
    drive_dir = OUTPUT_DIR / "drive"
    if drive_dir.exists():
        subdirs = [d.name for d in drive_dir.iterdir() if d.is_dir()]
        output_index["drive"] = {
            "path": "output/drive/",
            "subdirs": subdirs,
        }
    
    # Voicememo
    voicememo_dir = OUTPUT_DIR / "voicememo"
    if voicememo_dir.exists():
        file_count = len(list(voicememo_dir.glob("*.md")))
        output_index["voicememo"] = {
            "path": "output/voicememo/",
            "file_count": file_count,
        }
    
    return output_index


def calculate_related_channels(channels: Dict[str, Dict]) -> Dict[str, List[str]]:
    """チャンネル間の関連性を計算"""
    related = defaultdict(list)
    
    channel_ids = list(channels.keys())
    
    for i, channel_a_id in enumerate(channel_ids):
        channel_a = channels[channel_a_id]
        participants_a = set(channel_a["metadata"].get("participants", []))
        topics_a = set(channel_a.get("topics", []))
        
        scores = []
        
        for j, channel_b_id in enumerate(channel_ids):
            if i == j:
                continue
            
            channel_b = channels[channel_b_id]
            participants_b = set(channel_b["metadata"].get("participants", []))
            topics_b = set(channel_b.get("topics", []))
            
            # 共通参加者
            common_participants = len(participants_a & participants_b)
            # 共通トピック
            common_topics = len(topics_a & topics_b)
            # 同じワークスペース・カテゴリボーナス
            same_workspace = 1 if channel_a["workspace"] == channel_b["workspace"] else 0
            same_category = 1 if channel_a["category"] == channel_b["category"] else 0
            
            # スコア計算
            score = (
                0.4 * common_participants +
                0.3 * common_topics +
                0.2 * same_workspace +
                0.1 * same_category
            )
            
            if score > 0:
                scores.append((channel_b_id, score))
        
        # 上位5件を関連チャンネルとして保存
        scores.sort(key=lambda x: x[1], reverse=True)
        related[channel_a_id] = [cid for cid, _ in scores[:5]]
    
    return dict(related)


def build_book_index():
    """BookIndexを構築"""
    print("Building BookIndex...")
    
    # 全チャンネルを収集
    all_channels = {}
    for workspace in WORKSPACES:
        print(f"  Processing workspace: {workspace}")
        channels = build_channel_index(workspace)
        all_channels.update(channels)
    
    print(f"  Total channels: {len(all_channels)}")
    
    # 階層ツリーを構築
    print("  Building hierarchy tree...")
    tree = build_hierarchy_tree(all_channels)
    
    # エンティティを抽出
    print("  Extracting entities...")
    entities = extract_entities(all_channels)
    print(f"    Persons: {len(entities['persons'])}")
    print(f"    Events: {len(entities['events'])}")
    
    # 関連チャンネルを計算
    print("  Calculating related channels...")
    related = calculate_related_channels(all_channels)
    
    # チャンネル情報に関連チャンネルを追加
    for channel_id, related_ids in related.items():
        if channel_id in all_channels:
            all_channels[channel_id]["related_channels"] = related_ids
    
    # outputインデックスを構築
    print("  Building output index...")
    output_index = build_output_index()
    
    # BookIndexを構築
    book_index = {
        "version": "1.0.0",
        "generated_at": datetime.now().isoformat(),
        "workspaces": WORKSPACES,
        "stats": {
            "total_channels": len(all_channels),
            "total_persons": len(entities["persons"]),
            "total_events": len(entities["events"]),
        },
        "tree": tree,
        "channels": all_channels,
        "entities": entities,
        "output_sources": output_index,
    }
    
    # JSONファイルに保存
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    
    output_path = INDEX_DIR / "book_index.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(book_index, f, ensure_ascii=False, indent=2)
    
    print(f"  Saved to: {output_path}")
    print("Done!")
    
    return book_index


if __name__ == "__main__":
    build_book_index()
