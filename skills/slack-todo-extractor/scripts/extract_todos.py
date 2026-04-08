#!/usr/bin/env python3
"""
Slack TODO抽出スクリプト

Slackの同期データから、特定ユーザー宛のメンションを検索し、
スレッド返信を含めてTODO/タスクを抽出・ステータス判定します。

使い方:
  python extract_todos.py --users "Kohei,minicoohei" --period "2026-01-06:2026-01-08"
  python extract_todos.py --users "Kohei" --workspace yoake --period "2026-01-06:2026-01-08"
  python extract_todos.py --users "Kohei" --period "1/6:8" --use-llm  # LLMで判定
"""

import argparse
import os
import re
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
import json

# .envファイルを読み込む
def load_dotenv(env_path: Path = None):
    """シンプルな.env読み込み"""
    paths_to_try = [
        env_path,
        Path.cwd() / ".env",
        Path(__file__).parent.parent.parent.parent / ".env",
    ]
    for p in paths_to_try:
        if p and p.exists():
            with open(p) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, value = line.partition("=")
                        value = value.strip().strip('"').strip("'")
                        os.environ.setdefault(key.strip(), value)
            break

load_dotenv()

# Gemini API
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


@dataclass
class TodoItem:
    """TODOアイテム"""
    task: str
    requester: str
    date: str
    time: str
    channel: str
    workspace: str
    slack_link: str
    status: str  # "pending", "in_progress", "completed"
    deadline: Optional[str] = None
    response: Optional[str] = None
    response_time: Optional[str] = None
    llm_reason: Optional[str] = None  # LLM判定の理由


# LLM判定用プロンプト
LLM_SYSTEM_PROMPT = """あなたはSlackメッセージからTODO/タスクのステータスを判定するアシスタントです。

以下の情報を分析して、タスクのステータスを判定してください：
- 依頼者: メンションを送った人
- 対象者: メンションされた人（タスクを依頼された人）
- 本文: 依頼内容
- 返信: スレッド返信やチャンネルでの後続メッセージ

## 判定基準

### completed(完了)
- 対象者が「完了しました」「対応しました」「送りました」等の完了報告をしている
- 依頼者が「ありがとう」「確認しました」等で完了を確認している
- タスクの成果物が共有されている

### in_progress(対応中)
- 対象者が「承知」「やります」「見てみます」等で受諾している
- 期限が設定されており、まだその期限前
- 対象者が質問や確認をしている（作業中の兆候）

### pending(未対応)
- 対象者からの返信がない
- 返信があっても関係ない内容

## 出力形式
JSON形式で出力してください：
{
  "status": "pending" | "in_progress" | "completed",
  "deadline": "期限があれば記載（例: 来週月曜、1/13まで）、なければnull",
  "reason": "判定理由を1文で"
}
"""


def determine_status_with_llm(
    mention: dict,
    target_users: list[str],
    subsequent_messages: list[dict] = None
) -> tuple[str, Optional[str], Optional[str], Optional[str]]:
    """
    LLM（Gemini）を使ってステータスを判定
    
    Returns:
        (status, deadline, response, reason)
    """
    if not GENAI_AVAILABLE:
        raise RuntimeError("google-genai がインストールされていません")
    
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY または GOOGLE_API_KEY が設定されていません")
    
    client = genai.Client(api_key=api_key)
    
    # コンテキストを構築
    context_parts = []
    context_parts.append(f"【依頼者】{mention.get('sender', '不明')}")
    context_parts.append(f"【対象者】{', '.join(target_users)}")
    context_parts.append(f"【日時】{mention.get('date', '')} {mention.get('time', '')}")
    context_parts.append(f"【チャンネル】{mention.get('workspace', '')}/{mention.get('channel', '')}")
    context_parts.append(f"\n【本文】\n{mention.get('body', '')}")
    
    # スレッド返信
    thread_replies = mention.get("thread_replies", [])
    if thread_replies and isinstance(thread_replies, list):
        context_parts.append("\n【スレッド返信】")
        for reply in thread_replies:
            if isinstance(reply, dict):
                context_parts.append(f"  {reply.get('time', '')} - {reply.get('sender', '')}: {reply.get('body', '')}")
    
    # 後続メッセージ(同日のチャンネルメッセージ)
    if subsequent_messages and isinstance(subsequent_messages, list):
        mention_time = mention.get("time", "00:00")
        relevant_msgs = [
            m for m in subsequent_messages
            if isinstance(m, dict) and m.get("time", "00:00") > mention_time
        ][:5]  # 最大5件
        
        if relevant_msgs:
            context_parts.append("\n【後続のチャンネルメッセージ】")
            for msg in relevant_msgs:
                if isinstance(msg, dict):
                    context_parts.append(f"  {msg.get('time', '')} - {msg.get('sender', '')}: {msg.get('body', '')[:100]}")
    
    context = "\n".join(context_parts)
    
    # LLMに問い合わせ
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[LLM_SYSTEM_PROMPT, f"\n---\n\n{context}\n\n---\n\nこのタスクのステータスを判定してください。"],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1
            )
        )
        
        result = json.loads(response.text)
        return (
            result.get("status", "pending"),
            result.get("deadline"),
            result.get("reason", ""),
            result.get("reason", "")
        )
    except json.JSONDecodeError as e:
        print(f"    ⚠️ JSON解析エラー: {e}")
        return "pending", None, None, f"JSON解析エラー"
    except Exception as e:
        import traceback
        print(f"    ⚠️ LLM判定エラー: {type(e).__name__}: {e}")
        # traceback.print_exc()  # デバッグ時にコメントアウト解除
        return "pending", None, None, f"エラー: {e}"


# ステータス判定キーワード

# 依頼者からの完了確認(タスク完了とみなす)
REQUESTER_COMPLETION_KEYWORDS = [
    "ありがとう", "確認します", "確認させて", "助かります", "感謝"
]

# 対象ユーザーからの完了報告(タスク完了とみなす)
DONE_KEYWORDS = [
    "完了", "対応しました", "やりました", "できました", "終わりました",
    "送りました", "作りました", "更新しました", "修正しました"
]

# 対象ユーザーからの受諾(対応中とみなす、完了ではない)
ACCEPTANCE_KEYWORDS = [
    "承知", "了解", "やります", "対応します", "見てみます", "見ます",
    "確認します", "検討します", "作ります", "送ります",
    "OK", "おk", "おけ", "りょ", "わかりました"
]

DEADLINE_PATTERNS = [
    r"(\d{1,2}/\d{1,2})まで",
    r"(\d{1,2}日)まで",
    r"来週の?(月|火|水|木|金|土|日)曜",
    r"今週中",
    r"今日中",
    r"明日まで",
]


def parse_date_range(period: str) -> tuple[datetime, datetime]:
    """期間文字列をパース"""
    # "2026-01-06:2026-01-08" or "1/6〜8" or "1/6-8"
    
    # YYYY-MM-DD形式をチェック
    iso_pattern = r"(\d{4}-\d{2}-\d{2})[:\-〜~](\d{4}-\d{2}-\d{2})"
    iso_match = re.match(iso_pattern, period)
    if iso_match:
        start = datetime.strptime(iso_match.group(1), "%Y-%m-%d")
        end = datetime.strptime(iso_match.group(2), "%Y-%m-%d")
        return start, end
    
    # 1/6〜8 or 1/6-8 or 1/6:8 形式
    period = period.replace("〜", ":").replace("~", ":")
    
    # 1/6-8 形式(月/日-日)
    short_pattern = r"(\d{1,2})/(\d{1,2})[\-:](\d{1,2})"
    short_match = re.match(short_pattern, period)
    if short_match:
        year = datetime.now().year
        month = int(short_match.group(1))
        start_day = int(short_match.group(2))
        end_day = int(short_match.group(3))
        start = datetime(year, month, start_day)
        end = datetime(year, month, end_day)
        return start, end
    
    # 1/6:1/8 形式
    full_pattern = r"(\d{1,2})/(\d{1,2})[:\-〜~](\d{1,2})/(\d{1,2})"
    full_match = re.match(full_pattern, period)
    if full_match:
        year = datetime.now().year
        start = datetime(year, int(full_match.group(1)), int(full_match.group(2)))
        end = datetime(year, int(full_match.group(3)), int(full_match.group(4)))
        return start, end
    
    raise ValueError(f"日付形式を解析できません: {period}")


def find_mentions_in_file(
    file_path: Path,
    users: list[str],
    start_date: datetime,
    end_date: datetime
) -> list[dict]:
    """ファイル内でユーザーへのメンションを検索"""
    mentions = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 日付セクションごとに分割
    date_sections = re.split(r"^## (\d{4}-\d{2}-\d{2})$", content, flags=re.MULTILINE)
    
    current_date = None
    for i, section in enumerate(date_sections):
        # 日付ヘッダー
        if re.match(r"^\d{4}-\d{2}-\d{2}$", section):
            current_date = datetime.strptime(section, "%Y-%m-%d")
            continue
        
        if current_date is None:
            continue
        
        # 期間チェック
        if not (start_date <= current_date <= end_date):
            continue
        
        # メッセージを抽出(### で始まり、次の ### または --- または ## まで)
        messages = re.findall(
            r"### (\d{2}:\d{2}) - ([^\[\n]+?)(?:\s*\[\[Slack\]\]\(([^)]+)\))?\n(.*?)(?=\n### \d{2}:\d{2}|\n---|\n## \d{4}|$)",
            section,
            re.DOTALL
        )
        
        # 同じ日付内の全メッセージを時系列でリスト化
        all_messages_in_date = []
        for time_str, sender, slack_link, body in messages:
            main_body = body.split("> #### ")[0] if "> #### " in body else body
            all_messages_in_date.append({
                "time": time_str,
                "sender": sender.strip(),
                "body": main_body.strip()
            })
        
        # 時系列でソート
        all_messages_in_date.sort(key=lambda x: x["time"])
        
        for time_str, sender, slack_link, body in messages:
            # ユーザーへのメンションをチェック(本文の最初の部分のみ、スレッド返信は除く)
            main_body = body.split("> #### ")[0] if "> #### " in body else body
            
            for user in users:
                if f"@{user}" in main_body:
                    # スレッド返信を抽出(> #### HH:MM - username 形式)
                    thread_replies = []
                    seen_replies = set()  # 重複排除用
                    reply_pattern = r"> #### (\d{2}:\d{2}) - ([^\[\n]+?)(?:\s*\[\[Slack\]\]\([^)]+\))?\n((?:> [^\n]*\n?)*)"
                    
                    for match in re.finditer(reply_pattern, body):
                        reply_time = match.group(1)
                        reply_sender = match.group(2).strip()
                        reply_body = match.group(3)
                        
                        # 重複チェック
                        reply_key = f"{reply_time}:{reply_sender}"
                        if reply_key in seen_replies:
                            continue
                        seen_replies.add(reply_key)
                        
                        # "> " プレフィックスを除去
                        reply_body = "\n".join(
                            line[2:] if line.startswith("> ") else line
                            for line in reply_body.split("\n")
                        ).strip()
                        
                        thread_replies.append({
                            "time": reply_time,
                            "sender": reply_sender,
                            "body": reply_body
                        })
                    
                    mentions.append({
                        "date": current_date.strftime("%Y-%m-%d"),
                        "time": time_str,
                        "sender": sender.strip(),
                        "slack_link": slack_link or "",
                        "body": main_body.strip(),
                        "thread_replies": thread_replies,
                        "mentioned_user": user,
                        "file": str(file_path),
                        "subsequent_messages": all_messages_in_date  # 後続メッセージチェック用
                    })
    
    return mentions


def determine_status(
    mention: dict,
    target_users: list[str],
    subsequent_messages: list[dict] = None
) -> tuple[str, Optional[str], Optional[str]]:
    """
    メンションのステータスを判定
    
    判定ルール:
    - 対象ユーザーからの完了報告（「完了」「対応しました」等） → 完了
    - 依頼者からの完了確認（「ありがとう」「確認します」等） → 完了
    - 対象ユーザーからの受諾（「承知」「やります」等） → 対応中（期限までは未完了）
    - 返信なし → 未対応
    
    Args:
        mention: メンション情報
        target_users: 対象ユーザーリスト
        subsequent_messages: メンション後の同じチャンネルでのメッセージリスト
    
    Returns:
        (status, response, response_time)
    """
    thread_replies = mention.get("thread_replies", [])
    requester = mention.get("sender", "")
    
    best_status = "pending"
    best_response = None
    best_time = None
    
    # 1. スレッド返信を確認
    for reply in thread_replies:
        reply_sender = reply["sender"]
        reply_body = reply["body"]
        reply_time = reply["time"]
        
        # 対象ユーザーからの返信をチェック
        is_target_user = any(
            user.lower() in reply_sender.lower()
            for user in target_users
        )
        
        # 依頼者からの返信をチェック
        is_requester = requester.lower() in reply_sender.lower() if requester else False
        
        if is_target_user:
            # 完了報告キーワード -> 完了
            if any(kw in reply_body for kw in DONE_KEYWORDS):
                return "completed", reply_body[:50], reply_time
            # 受諾キーワード -> 対応中(完了ではない)
            if any(kw in reply_body for kw in ACCEPTANCE_KEYWORDS):
                if best_status == "pending":
                    best_status = "in_progress"
                    best_response = reply_body[:50]
                    best_time = reply_time
        
        if is_requester or (not is_target_user):
            # 依頼者からの完了確認 -> 完了
            if any(kw in reply_body for kw in REQUESTER_COMPLETION_KEYWORDS):
                return "completed", reply_body[:50], reply_time
    
    # 2. 後続のチャンネルメッセージを確認(スレッドでない返信)
    if subsequent_messages:
        mention_time = mention.get("time", "00:00")
        
        for msg in subsequent_messages:
            msg_time = msg.get("time", "00:00")
            msg_sender = msg.get("sender", "")
            msg_body = msg.get("body", "")
            
            # メンション後のメッセージのみ
            if msg_time <= mention_time:
                continue
            
            # 対象ユーザーからのメッセージをチェック
            is_target_user = any(
                user.lower() in msg_sender.lower()
                for user in target_users
            )
            
            if is_target_user:
                # 完了報告 -> 完了
                if any(kw in msg_body for kw in DONE_KEYWORDS):
                    return "completed", msg_body[:50], msg_time
                # 受諾 -> 対応中
                if any(kw in msg_body for kw in ACCEPTANCE_KEYWORDS):
                    if best_status == "pending":
                        best_status = "in_progress"
                        best_response = msg_body[:50]
                        best_time = msg_time
                # 返信っぽい短いメッセージ -> 対応中
                elif len(msg_body) < 200 and best_status == "pending":
                    best_status = "in_progress"
                    best_response = msg_body[:50]
                    best_time = msg_time
    
    return best_status, best_response, best_time


def extract_deadline(text: str) -> Optional[str]:
    """テキストから期限を抽出"""
    for pattern in DEADLINE_PATTERNS:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return None


def extract_task_summary(body: str, max_length: int = 100) -> str:
    """メッセージ本文からタスク要約を抽出"""
    # @メンションを除去
    text = re.sub(r"@\S+", "", body)
    # URLを除去
    text = re.sub(r"https?://\S+", "[URL]", text)
    # 改行を空白に
    text = re.sub(r"\n+", " ", text)
    # 先頭の空白を除去
    text = text.strip()
    
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text


def main():
    parser = argparse.ArgumentParser(description="Slack TODO抽出ツール")
    parser.add_argument(
        "--users", "-u",
        required=True,
        help="対象ユーザー名（カンマ区切り）"
    )
    parser.add_argument(
        "--period", "-p",
        required=True,
        help="検索期間（例: 2026-01-06:2026-01-08 または 1/6:8）"
    )
    parser.add_argument(
        "--workspace", "-w",
        help="ワークスペース（省略時は全て）"
    )
    parser.add_argument(
        "--data-dir",
        default=None,
        help="slack-sync/dataディレクトリのパス"
    )
    parser.add_argument(
        "--output", "-o",
        choices=["markdown", "json"],
        default="markdown",
        help="出力形式"
    )
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="LLM（Gemini 2.0 Flash）でステータス判定（より正確、要GEMINI_API_KEY）"
    )
    
    args = parser.parse_args()
    
    # パラメータ解析
    users = [u.strip() for u in args.users.split(",")]
    start_date, end_date = parse_date_range(args.period)
    
    # データディレクトリを探す
    if args.data_dir:
        data_dir = Path(args.data_dir)
    else:
        # スクリプトの場所から相対パスで探す
        script_dir = Path(__file__).parent
        candidates = [
            script_dir.parent.parent.parent / "slack-sync" / "data",
            Path.cwd() / "slack-sync" / "data",
            Path.cwd() / "knowledge-base" / "slack-sync" / "data",
        ]
        data_dir = None
        for c in candidates:
            if c.exists():
                data_dir = c
                break
        
        if data_dir is None:
            print("❌ slack-sync/data ディレクトリが見つかりません")
            print("   --data-dir オプションでパスを指定してください")
            return
    
    print(f"🔍 検索条件:")
    print(f"   ユーザー: {', '.join(users)}")
    print(f"   期間: {start_date.strftime('%Y-%m-%d')} 〜 {end_date.strftime('%Y-%m-%d')}")
    print(f"   データ: {data_dir}")
    print()
    
    # ワークスペースを決定
    if args.workspace:
        workspaces = [data_dir / args.workspace]
    else:
        workspaces = [d for d in data_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
    
    # 全メンションを収集
    all_mentions = []
    for ws_dir in workspaces:
        if not ws_dir.exists():
            continue
        
        ws_name = ws_dir.name
        for md_file in ws_dir.glob("*.md"):
            mentions = find_mentions_in_file(md_file, users, start_date, end_date)
            for m in mentions:
                m["workspace"] = ws_name
                m["channel"] = md_file.stem
            all_mentions.extend(mentions)
    
    if not all_mentions:
        print("📭 メンションが見つかりませんでした")
        return
    
    # TODOアイテムに変換
    todos = []
    use_llm = args.use_llm
    
    if use_llm:
        if not GENAI_AVAILABLE:
            print("❌ --use-llm を使用するには google-generativeai をインストールしてください")
            print("   pip install google-generativeai")
            return
        if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
            print("❌ --use-llm を使用するには GEMINI_API_KEY を設定してください")
            return
        print("🤖 LLM（Gemini 2.0 Flash）でステータス判定中...")
        print()
    
    for i, m in enumerate(all_mentions):
        subsequent = m.get("subsequent_messages", [])
        
        if use_llm:
            print(f"  [{i+1}/{len(all_mentions)}] {m.get('channel', '')} - {m.get('sender', '')}...")
            status, deadline, response, llm_reason = determine_status_with_llm(m, users, subsequent)
            response_time = None
        else:
            status, response, response_time = determine_status(m, users, subsequent)
            llm_reason = None
            deadline = extract_deadline(m["body"])
            
            # スレッド返信から期限を探す
            if not deadline:
                for reply in m.get("thread_replies", []):
                    deadline = extract_deadline(reply["body"])
                    if deadline:
                        break
        
        todo = TodoItem(
            task=extract_task_summary(m["body"]),
            requester=m["sender"],
            date=m["date"],
            time=m["time"],
            channel=m["channel"],
            workspace=m["workspace"],
            slack_link=m["slack_link"],
            status=status,
            deadline=deadline,
            response=response,
            response_time=response_time,
            llm_reason=llm_reason
        )
        todos.append(todo)
    
    if use_llm:
        print()
    
    # 出力
    if args.output == "json":
        print(json.dumps([t.__dict__ for t in todos], indent=2, ensure_ascii=False))
    else:
        # Markdown出力
        print(f"## 📋 TODO一覧（{start_date.strftime('%m/%d')}〜{end_date.strftime('%m/%d')}）")
        print()
        
        # ステータス別に分類
        pending = [t for t in todos if t.status == "pending"]
        in_progress = [t for t in todos if t.status == "in_progress"]
        completed = [t for t in todos if t.status == "completed"]
        
        if pending:
            print("### 🔴 未対応")
            print("| タスク | 依頼者 | 日時 | チャンネル |")
            print("|--------|--------|------|-----------|")
            for t in pending:
                print(f"| {t.task} | {t.requester} | {t.date} {t.time} | {t.workspace}/{t.channel} |")
            print()
        
        if in_progress:
            print("### 🟡 対応中")
            if use_llm:
                print("| タスク | 期限 | 判定理由 | 依頼者 | チャンネル |")
                print("|--------|------|----------|--------|-----------|")
                for t in in_progress:
                    deadline = t.deadline or "-"
                    reason = (t.llm_reason or "-")[:40]
                    print(f"| {t.task[:50]}... | {deadline} | {reason} | {t.requester} | {t.workspace}/{t.channel} |")
            else:
                print("| タスク | 期限 | 返信 | 依頼者 | 日時 | チャンネル |")
                print("|--------|------|------|--------|------|-----------|")
                for t in in_progress:
                    deadline = t.deadline or "-"
                    response = (t.response or "-")[:30]
                    print(f"| {t.task} | {deadline} | {response} | {t.requester} | {t.date} {t.time} | {t.workspace}/{t.channel} |")
            print()
        
        if completed:
            print("### ✅ 完了")
            if use_llm:
                print("| タスク | 判定理由 | 依頼者 | チャンネル |")
                print("|--------|----------|--------|-----------|")
                for t in completed:
                    reason = (t.llm_reason or "-")[:40]
                    print(f"| {t.task[:50]}... | {reason} | {t.requester} | {t.workspace}/{t.channel} |")
            else:
                print("| タスク | 完了 | 依頼者 | チャンネル |")
                print("|--------|------|--------|-----------|")
                for t in completed:
                    response = (t.response or "-")[:30]
                    print(f"| {t.task} | {response} | {t.requester} | {t.workspace}/{t.channel} |")
            print()
        
        print(f"---")
        print(f"合計: {len(todos)} 件（未対応: {len(pending)}, 対応中: {len(in_progress)}, 完了: {len(completed)}）")


if __name__ == "__main__":
    main()
