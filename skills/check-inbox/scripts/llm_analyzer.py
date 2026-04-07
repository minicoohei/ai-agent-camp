#!/usr/bin/env python3
"""
LLM分析モジュール

Gemini 3.0 Flash を使用して、メールとSlackメッセージを分析し、
返信の必要性、優先度、返信ドラフトを生成
"""

import os
import json
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
# プロジェクトルートをパスに追加（credential_manager 解決用）
_ROOT_DIR = Path(__file__).resolve().parents[3]
if str(_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(_ROOT_DIR))

from common import load_dotenv, get_gemini_api_key, TaskItem
from email_parser import Email
from slack_parser import SlackMessage, DEFAULT_TARGET_USERS

# .envを読み込み
try:
    from tools.credential_manager import inject_to_environ
    inject_to_environ()
except ImportError:
    try:
        from credential_manager import inject_to_environ
        inject_to_environ()
    except ImportError:
        pass
load_dotenv()



# Gemini APIの設定
GEMINI_MODEL = "gemini-3-flash-preview"
MAX_JSON_SIZE = 10 * 1024 * 1024  # 10MB

# モジュールレベルでクライアントをキャッシュ
_gemini_client = None


# メール分析用プロンプト
EMAIL_ANALYSIS_PROMPT = """あなたはメール分析アシスタントです。

以下のメールを分析し、返信が必要かどうかを判定してください。

## 判定基準

### 返信が必要（requires_reply: true）
- 質問や依頼が含まれている
- 確認や承認が求められている
- 個人的なやり取り（知人・同僚からのメール）
- ミーティングの調整
- 緊急の連絡

### 返信が不要（requires_reply: false）
- マーケティングメール、ニュースレター
- 自動通知（システム通知、アラート）
- 一方的な情報提供
- スパム

### 優先度判定
- high: 緊急、期限付き、重要な依頼
- medium: 通常の返信が必要なもの
- low: 返信は必要だが急ぎではない

## メール情報
- 件名: {subject}
- 送信者: {sender} <{sender_email}>
- 日付: {date}

## 本文
{body}

## 出力形式（JSON）
{{
  "requires_reply": true/false,
  "priority": "high" | "medium" | "low",
  "reason": "判定理由を1文で（日本語）",
  "draft_reply": "返信ドラフト（日本語、返信不要の場合は空文字）"
}}
"""

# Slack分析用プロンプト
SLACK_ANALYSIS_PROMPT = """あなたはSlackメッセージ分析アシスタントです。

以下のメンションを分析し、返信が必要かどうかを判定してください。

## 判定基準

### 返信が必要（requires_reply: true）
- 質問が含まれている（?マーク、「教えて」「確認」等）
- タスクや依頼が含まれている
- 確認や承認が求められている
- 報告への反応が期待されている

### 返信が不要（requires_reply: false）
- 情報共有のみ（FYI）
- 自分が既に返信している
- 他の人が対応済み

### 優先度判定
- high: 緊急、期限付き、重要な依頼、ブロッカー
- medium: 通常の質問や依頼
- low: 急ぎではない確認事項

## メッセージ情報
- チャンネル: {channel}
- 送信者: {sender}
- 日時: {date} {time}

## 本文
{body}

## スレッド返信
{thread_replies}

## 出力形式（JSON）
{{
  "requires_reply": true/false,
  "priority": "high" | "medium" | "low",
  "reason": "判定理由を1文で（日本語）",
  "draft_reply": "返信ドラフト（日本語、返信不要の場合は空文字）"
}}
"""


@dataclass
class AnalysisResult:
    """分析結果"""
    requires_reply: bool
    priority: str
    reason: str
    draft_reply: str


def get_gemini_client():
    """Geminiクライアントを取得（キャッシュ）"""
    global _gemini_client

    if _gemini_client is not None:
        return _gemini_client

    try:
        from google import genai
    except ImportError:
        raise RuntimeError(
            "google-genai がインストールされていません。\n"
            "pip install google-genai でインストールしてください。"
        ) from None

    api_key = get_gemini_api_key()
    _gemini_client = genai.Client(api_key=api_key)
    return _gemini_client


def analyze_email(email: Email) -> AnalysisResult:
    """
    メールを分析

    Args:
        email: Emailオブジェクト

    Returns:
        AnalysisResult
    """
    from google.genai import types

    client = get_gemini_client()

    # 本文を制限（トークン節約）
    body = email.body[:3000] if len(email.body) > 3000 else email.body

    prompt = EMAIL_ANALYSIS_PROMPT.format(
        subject=email.subject,
        sender=email.sender,
        sender_email=email.sender_email,
        date=email.date.strftime("%Y-%m-%d %H:%M") if email.date else "不明",
        body=body
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1
            )
        )

        response_text = response.text.strip()
        if len(response_text) > MAX_JSON_SIZE:
            raise ValueError(f"Response too large: {len(response_text)} bytes")
        result = json.loads(response_text)
        return AnalysisResult(
            requires_reply=result.get("requires_reply", False),
            priority=result.get("priority", "low"),
            reason=result.get("reason", ""),
            draft_reply=result.get("draft_reply", "")
        )
    except json.JSONDecodeError as e:
        print(f"  ⚠️ JSON解析エラー: {e}")
        return AnalysisResult(
            requires_reply=False,
            priority="low",
            reason="分析エラー",
            draft_reply=""
        )
    except Exception as e:
        print(f"  ⚠️ 分析エラー: {e}")
        return AnalysisResult(
            requires_reply=False,
            priority="low",
            reason=f"エラー: {e}",
            draft_reply=""
        )


def analyze_slack_message(message: SlackMessage) -> AnalysisResult:
    """
    Slackメッセージを分析

    Args:
        message: SlackMessageオブジェクト

    Returns:
        AnalysisResult
    """
    from google.genai import types

    client = get_gemini_client()

    # スレッド返信をフォーマット
    thread_text = ""
    if message.thread_replies:
        for reply in message.thread_replies:
            thread_text += f"- {reply.time} {reply.sender}: {reply.body[:100]}\n"
    else:
        thread_text = "（返信なし）"

    prompt = SLACK_ANALYSIS_PROMPT.format(
        channel=message.channel,
        sender=message.sender,
        date=message.date,
        time=message.time,
        body=message.body[:2000],
        thread_replies=thread_text
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1
            )
        )

        response_text = response.text.strip()
        if len(response_text) > MAX_JSON_SIZE:
            raise ValueError(f"Response too large: {len(response_text)} bytes")
        result = json.loads(response_text)
        return AnalysisResult(
            requires_reply=result.get("requires_reply", False),
            priority=result.get("priority", "low"),
            reason=result.get("reason", ""),
            draft_reply=result.get("draft_reply", "")
        )
    except json.JSONDecodeError as e:
        print(f"  ⚠️ JSON解析エラー: {e}")
        return AnalysisResult(
            requires_reply=True,  # Slackメンションはデフォルトで返信必要
            priority="medium",
            reason="分析エラー",
            draft_reply=""
        )
    except Exception as e:
        print(f"  ⚠️ 分析エラー: {e}")
        return AnalysisResult(
            requires_reply=True,
            priority="medium",
            reason=f"エラー: {e}",
            draft_reply=""
        )


def email_to_task(email: Email, analysis: AnalysisResult) -> TaskItem:
    """
    メールと分析結果からTaskItemを生成

    Args:
        email: Emailオブジェクト
        analysis: AnalysisResult

    Returns:
        TaskItem
    """
    return TaskItem(
        source="email",
        title=email.subject,
        content=email.body[:200],
        sender=email.sender,
        date=email.date.strftime("%Y-%m-%d") if email.date else "",
        time=email.date.strftime("%H:%M") if email.date else "",
        priority=analysis.priority,
        reason=analysis.reason,
        draft_reply=analysis.draft_reply,
        email_id=email.id,
        link=""
    )


def slack_to_task(message: SlackMessage, analysis: AnalysisResult) -> TaskItem:
    """
    Slackメッセージと分析結果からTaskItemを生成

    Args:
        message: SlackMessageオブジェクト
        analysis: AnalysisResult

    Returns:
        TaskItem
    """
    return TaskItem(
        source="slack",
        title=f"@{message.mentioned_user} in #{message.channel}",
        content=message.body,
        sender=message.sender,
        date=message.date,
        time=message.time,
        priority=analysis.priority,
        reason=analysis.reason,
        draft_reply=analysis.draft_reply,
        channel=message.channel,
        workspace=message.workspace,
        link=message.slack_link
    )


def batch_analyze_emails(
    emails: list[Email],
    progress_callback=None
) -> list[TaskItem]:
    """
    メールをバッチ分析

    Args:
        emails: Emailオブジェクトのリスト
        progress_callback: 進捗コールバック関数

    Returns:
        返信が必要なTaskItemのリスト
    """
    tasks = []

    for i, email in enumerate(emails):
        if progress_callback:
            progress_callback(i + 1, len(emails), email.subject[:30])

        analysis = analyze_email(email)

        if analysis.requires_reply:
            tasks.append(email_to_task(email, analysis))

    return tasks


def _is_self_message(sender: str, self_users: list[str] | None = None) -> bool:
    """
    送信者が自分自身かどうかを判定(大文字小文字を区別しない)

    Args:
        sender: メッセージの送信者名
        self_users: 自分自身の名前パターンリスト(デフォルト: DEFAULT_TARGET_USERS)

    Returns:
        自分自身のメッセージならTrue
    """
    if not sender:
        return False
    patterns = DEFAULT_TARGET_USERS if self_users is None else self_users
    sender_lower = sender.lower()
    return any(pattern.lower() in sender_lower for pattern in patterns)


def batch_analyze_slack(
    messages: list[SlackMessage],
    progress_callback=None
) -> list[TaskItem]:
    """
    Slackメッセージをバッチ分析

    Args:
        messages: SlackMessageオブジェクトのリスト
        progress_callback: 進捗コールバック関数

    Returns:
        返信が必要なTaskItemのリスト
    """
    tasks = []

    for i, message in enumerate(messages):
        if progress_callback:
            progress_callback(i + 1, len(messages), f"{message.channel}")

        # 自分自身が送信したメッセージはスキップ(#859)
        if _is_self_message(message.sender):
            print(f"  ⏭️ 自己メッセージをスキップ: {message.sender} in #{message.channel}")
            continue

        analysis = analyze_slack_message(message)

        if analysis.requires_reply:
            tasks.append(slack_to_task(message, analysis))

    return tasks


if __name__ == "__main__":
    # テスト用
    print("LLM Analyzer module loaded successfully.")
    print(f"Using model: {GEMINI_MODEL}")

    try:
        client = get_gemini_client()
        print("✅ Gemini API connection successful")
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
