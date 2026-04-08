#!/usr/bin/env python3
"""
Hypothesis Generator - 市場インテリジェンス → 仮説生成 → A/Bバリアント作成

5ソース（X, Google検索, Google Trends, Reddit/HN, 競合アカウント）から
市場データを並列収集し、LLMで統合分析して仮説とバリアントを自動生成する。

Usage:
    python hypothesis_generator.py --topic "AIエージェント" --channel x_twitter
    python hypothesis_generator.py --topic "SaaS pricing" --competitors "competitor1,competitor2"
    python hypothesis_generator.py --topic "生成AI" --dry-run
    python hypothesis_generator.py --test
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
import yaml
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from tools.credential_manager import inject_to_environ
    inject_to_environ()
except ImportError:
    try:
        from credential_manager import inject_to_environ
        inject_to_environ()
    except ImportError:
        pass
load_dotenv(ROOT_DIR / ".env")


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

DEFAULT_OUTPUT_DIR = ROOT_DIR / "output" / "content-optimizer" / "hypotheses"
GEMINI_MODEL = os.environ.get("GEMINI_HYPOTHESIS_MODEL", "gemini-3-flash-preview")

X_API_BASE = "https://api.x.com/2"
REDDIT_SEARCH_URL = "https://www.reddit.com/search.json"
HN_SEARCH_URL = "https://hn.algolia.com/api/v1/search"

CHANNELS = ["x_twitter", "email", "linkedin"]

# Subreddits to search per topic category
DEFAULT_SUBREDDITS = [
    "technology", "artificial", "MachineLearning",
    "SaaS", "startups", "Entrepreneur",
]


# =============================================================================
# Utility
# =============================================================================


def sanitize_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*\s]+', "_", name)[:80]


def get_gemini_client():
    """Initialize Gemini client."""
    from google import genai  # noqa: delayed import

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        logger.error("Error: GEMINI_API_KEY が環境変数に設定されていません。")
        sys.exit(1)
    return genai.Client(api_key=api_key)


def get_x_bearer_token() -> Optional[str]:
    """Get X API bearer token from environment."""
    token = os.environ.get("X_BEARER_TOKEN")
    if not token:
        logger.warning("X_BEARER_TOKEN が未設定のため、X関連データ収集をスキップします。")
    return token


# =============================================================================
# Source 1: X Buzz Collection
# =============================================================================


def collect_x_buzz(topic: str, lang: str = "ja", days: int = 7,
                   max_results: int = 50) -> Dict[str, Any]:
    """X API v2 でバズ投稿を収集。x-research の XAPIClient パターンを再利用。"""
    token = get_x_bearer_token()
    if not token:
        return {"source": "x_twitter", "status": "skipped", "data": []}

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "User-Agent": "content-optimizer/1.0",
    })

    query_parts = [topic]
    if lang and lang != "all":
        query_parts.append(f"lang:{lang}")
    query_parts.append("-is:retweet")
    query = " ".join(query_parts)

    tweet_fields = "created_at,public_metrics,lang,entities"
    user_fields = "name,username,public_metrics"

    params = {
        "query": query,
        "max_results": min(max(max_results, 10), 100),
        "tweet.fields": tweet_fields,
        "user.fields": user_fields,
        "expansions": "author_id",
        "sort_order": "relevancy",
    }

    logger.info("  [X] '%s' を検索中...", topic)

    try:
        response = session.get(f"{X_API_BASE}/tweets/search/recent",
                               params=params, timeout=30)
        if response.status_code == 429:
            reset_time = response.headers.get("x-rate-limit-reset")
            wait = max(int(reset_time) - int(time.time()) + 1, 1) if reset_time else 15
            wait = min(wait, 60)
            logger.info("  [X] レート制限。%d秒待機...", wait)
            time.sleep(wait)
            response = session.get(f"{X_API_BASE}/tweets/search/recent",
                                   params=params, timeout=30)
        if response.status_code in (400, 401, 403):
            logger.warning("  [X] API エラー (%d): %s", response.status_code,
                           response.text[:200])
            return {"source": "x_twitter", "status": "error", "data": []}

        response.raise_for_status()
        result = response.json()
    except Exception as e:
        logger.warning("  [X] 収集失敗: %s", e)
        return {"source": "x_twitter", "status": "error", "data": []}

    tweets = result.get("data", [])
    users = {u["id"]: u for u in result.get("includes", {}).get("users", [])}

    enriched = []
    for tw in tweets:
        metrics = tw.get("public_metrics", {})
        engagement = (metrics.get("like_count", 0) + metrics.get("retweet_count", 0)
                      + metrics.get("reply_count", 0))
        author = users.get(tw.get("author_id", ""), {})
        enriched.append({
            "text": tw.get("text", ""),
            "author": author.get("username", "unknown"),
            "author_name": author.get("name", ""),
            "likes": metrics.get("like_count", 0),
            "retweets": metrics.get("retweet_count", 0),
            "replies": metrics.get("reply_count", 0),
            "engagement": engagement,
            "created_at": tw.get("created_at", ""),
            "id": tw.get("id", ""),
        })

    enriched.sort(key=lambda x: x["engagement"], reverse=True)
    top_n = enriched[:20]

    logger.info("  [X] %d件取得（上位%d件を使用）", len(enriched), len(top_n))
    return {
        "source": "x_twitter",
        "status": "ok",
        "total": len(enriched),
        "data": top_n,
    }


# =============================================================================
# Source 2: Google Search via Gemini Grounding
# =============================================================================


def collect_web_trends(topic: str, lang: str = "ja") -> Dict[str, Any]:
    """Gemini Google Search grounding でトレンド記事を収集。"""
    logger.info("  [Google] '%s' のトレンド記事を検索中...", topic)

    try:
        from google.genai import types

        client = get_gemini_client()
        search_tool = types.Tool(google_search=types.GoogleSearch())

        lang_label = "日本語" if lang == "ja" else "English"
        prompt = (
            f"「{topic}」について、直近1ヶ月のトレンドや話題を{lang_label}で調べてください。\n"
            f"以下の点を重点的に:\n"
            f"1. 最新のトレンドや注目されている話題\n"
            f"2. 人気のあるコンテンツフォーマットや切り口\n"
            f"3. 業界の最新動向や変化\n"
            f"4. SNSやブログで反響のある話題\n\n"
            f"具体的なデータや事例を含めてまとめてください。"
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[prompt],
            config=types.GenerateContentConfig(
                tools=[search_tool],
                temperature=0.3,
            ),
        )

        text = response.text if response.text else ""
        logger.info("  [Google] トレンド記事取得完了 (%d文字)", len(text))
        return {
            "source": "google_search",
            "status": "ok",
            "data": text,
        }
    except Exception as e:
        logger.warning("  [Google] 収集失敗: %s", e)
        return {"source": "google_search", "status": "error", "data": ""}


# =============================================================================
# Source 3: Google Trends via Gemini Grounding
# =============================================================================


def collect_google_trends(topic: str, lang: str = "ja") -> Dict[str, Any]:
    """Gemini grounding で Google Trends データを取得。"""
    logger.info("  [Trends] '%s' の検索トレンドを調査中...", topic)

    try:
        from google.genai import types

        client = get_gemini_client()
        search_tool = types.Tool(google_search=types.GoogleSearch())

        prompt = (
            f"Google Trends で「{topic}」の検索トレンドを調べてください。\n"
            f"以下の情報を含めてください:\n"
            f"1. 直近の検索ボリュームの推移（上昇中/安定/下降中）\n"
            f"2. 関連する急上昇キーワード（breakout queries）\n"
            f"3. 関連トピックの人気度\n"
            f"4. 地域別の関心度の違い\n"
            f"5. 今後のトレンド予測\n\n"
            f"Google Trends のデータに基づいて具体的に回答してください。"
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[prompt],
            config=types.GenerateContentConfig(
                tools=[search_tool],
                temperature=0.3,
            ),
        )

        text = response.text if response.text else ""
        logger.info("  [Trends] トレンドデータ取得完了 (%d文字)", len(text))
        return {
            "source": "google_trends",
            "status": "ok",
            "data": text,
        }
    except Exception as e:
        logger.warning("  [Trends] 収集失敗: %s", e)
        return {"source": "google_trends", "status": "error", "data": ""}


# =============================================================================
# Source 4: Reddit + HackerNews
# =============================================================================


def collect_reddit(topic: str) -> List[Dict]:
    """Reddit JSON API で関連スレッドを収集。"""
    headers = {"User-Agent": "content-optimizer/1.0"}
    params = {
        "q": topic,
        "sort": "top",
        "t": "week",
        "limit": 15,
        "type": "link",
    }
    try:
        resp = requests.get(REDDIT_SEARCH_URL, params=params,
                            headers=headers, timeout=15)
        if resp.status_code != 200:
            logger.warning("  [Reddit] HTTP %d", resp.status_code)
            return []

        data = resp.json().get("data", {}).get("children", [])
        results = []
        for item in data:
            d = item.get("data", {})
            results.append({
                "title": d.get("title", ""),
                "subreddit": d.get("subreddit", ""),
                "score": d.get("score", 0),
                "num_comments": d.get("num_comments", 0),
                "url": f"https://reddit.com{d.get('permalink', '')}",
                "created_utc": d.get("created_utc", 0),
            })
        return sorted(results, key=lambda x: x["score"], reverse=True)[:10]
    except Exception as e:
        logger.warning("  [Reddit] 収集失敗: %s", e)
        return []


def collect_hackernews(topic: str) -> List[Dict]:
    """HackerNews Algolia API で関連ストーリーを収集。"""
    params = {
        "query": topic,
        "tags": "story",
        "hitsPerPage": 15,
        "numericFilters": "created_at_i>%d" % (int(time.time()) - 7 * 86400),
    }
    try:
        resp = requests.get(HN_SEARCH_URL, params=params, timeout=15)
        if resp.status_code != 200:
            logger.warning("  [HN] HTTP %d", resp.status_code)
            return []

        hits = resp.json().get("hits", [])
        results = []
        for h in hits:
            results.append({
                "title": h.get("title", ""),
                "points": h.get("points", 0),
                "num_comments": h.get("num_comments", 0),
                "url": f"https://news.ycombinator.com/item?id={h.get('objectID', '')}",
                "created_at": h.get("created_at", ""),
            })
        return sorted(results, key=lambda x: x["points"], reverse=True)[:10]
    except Exception as e:
        logger.warning("  [HN] 収集失敗: %s", e)
        return []


def collect_reddit_hn(topic: str) -> Dict[str, Any]:
    """Reddit + HackerNews を収集。"""
    logger.info("  [Reddit/HN] '%s' のコミュニティ議論を収集中...", topic)

    reddit = collect_reddit(topic)
    hn = collect_hackernews(topic)

    logger.info("  [Reddit/HN] Reddit %d件, HN %d件", len(reddit), len(hn))
    return {
        "source": "reddit_hn",
        "status": "ok",
        "data": {
            "reddit": reddit,
            "hackernews": hn,
        },
    }


# =============================================================================
# Source 5: Competitor Analysis
# =============================================================================


def collect_competitor(competitors: List[str], topic: str) -> Dict[str, Any]:
    """競合アカウントの直近投稿を X API v2 で収集。"""
    if not competitors:
        return {"source": "competitor", "status": "skipped", "data": []}

    token = get_x_bearer_token()
    if not token:
        return {"source": "competitor", "status": "skipped", "data": []}

    logger.info("  [競合] %d アカウントの投稿を収集中...", len(competitors))

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "User-Agent": "content-optimizer/1.0",
    })

    all_data = []
    for username in competitors:
        username = username.strip().lstrip("@")
        try:
            # Get user ID
            user_resp = session.get(
                f"{X_API_BASE}/users/by/username/{username}",
                timeout=15,
            )
            if user_resp.status_code != 200:
                logger.warning("  [競合] @%s の取得失敗 (%d)", username, user_resp.status_code)
                continue

            user_id = user_resp.json().get("data", {}).get("id")
            if not user_id:
                continue

            time.sleep(1)

            # Get recent tweets
            tweets_resp = session.get(
                f"{X_API_BASE}/users/{user_id}/tweets",
                params={
                    "max_results": 20,
                    "tweet.fields": "created_at,public_metrics",
                    "exclude": "retweets,replies",
                },
                timeout=15,
            )
            if tweets_resp.status_code != 200:
                logger.warning("  [競合] @%s のツイート取得失敗 (%d)",
                               username, tweets_resp.status_code)
                continue

            tweets = tweets_resp.json().get("data", [])
            for tw in tweets:
                metrics = tw.get("public_metrics", {})
                engagement = (metrics.get("like_count", 0)
                              + metrics.get("retweet_count", 0)
                              + metrics.get("reply_count", 0))
                all_data.append({
                    "author": username,
                    "text": tw.get("text", ""),
                    "likes": metrics.get("like_count", 0),
                    "retweets": metrics.get("retweet_count", 0),
                    "replies": metrics.get("reply_count", 0),
                    "engagement": engagement,
                    "created_at": tw.get("created_at", ""),
                })

            time.sleep(1)

        except Exception as e:
            logger.warning("  [競合] @%s の処理失敗: %s", username, e)

    all_data.sort(key=lambda x: x["engagement"], reverse=True)
    top = all_data[:15]
    logger.info("  [競合] 合計 %d件（上位%d件を使用）", len(all_data), len(top))
    return {
        "source": "competitor",
        "status": "ok",
        "data": top,
    }


# =============================================================================
# Parallel Collection
# =============================================================================


def collect_all_sources(topic: str, channel: str, lang: str,
                        days: int, competitors: List[str]) -> Dict[str, Any]:
    """5ソースを並列収集。"""
    logger.info("\n=== データ収集開始 ===")

    results = {}

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(collect_x_buzz, topic, lang, days): "x_twitter",
            executor.submit(collect_web_trends, topic, lang): "google_search",
            executor.submit(collect_google_trends, topic, lang): "google_trends",
            executor.submit(collect_reddit_hn, topic): "reddit_hn",
            executor.submit(collect_competitor, competitors, topic): "competitor",
        }

        for future in as_completed(futures):
            source_name = futures[future]
            try:
                results[source_name] = future.result()
            except Exception as e:
                logger.error("  [%s] 予期せぬエラー: %s", source_name, e)
                results[source_name] = {
                    "source": source_name,
                    "status": "error",
                    "data": None,
                }

    ok_count = sum(1 for r in results.values() if r.get("status") == "ok")
    logger.info("\n=== 収集完了: %d/5 ソース成功 ===\n", ok_count)
    return results


# =============================================================================
# LLM Analysis & Hypothesis Generation
# =============================================================================


def _build_source_summary(sources: Dict[str, Any]) -> str:
    """収集データを LLM に渡すテキストに変換。"""
    parts = []

    # X buzz
    x_data = sources.get("x_twitter", {})
    if x_data.get("status") == "ok" and x_data.get("data"):
        tweets_text = "\n".join(
            f"- @{t['author']}: \"{t['text'][:150]}\" "
            f"(likes:{t['likes']}, RT:{t['retweets']}, replies:{t['replies']})"
            for t in x_data["data"][:10]
        )
        parts.append(f"## X (Twitter) バズ投稿 Top10\n{tweets_text}")

    # Google Search
    gs_data = sources.get("google_search", {})
    if gs_data.get("status") == "ok" and gs_data.get("data"):
        parts.append(f"## Google 検索トレンド\n{gs_data['data'][:2000]}")

    # Google Trends
    gt_data = sources.get("google_trends", {})
    if gt_data.get("status") == "ok" and gt_data.get("data"):
        parts.append(f"## Google Trends\n{gt_data['data'][:2000]}")

    # Reddit/HN
    rh_data = sources.get("reddit_hn", {})
    if rh_data.get("status") == "ok" and rh_data.get("data"):
        reddit = rh_data["data"].get("reddit", [])
        hn = rh_data["data"].get("hackernews", [])
        reddit_text = "\n".join(
            f"- r/{r['subreddit']}: \"{r['title']}\" (score:{r['score']}, comments:{r['num_comments']})"
            for r in reddit[:7]
        )
        hn_text = "\n".join(
            f"- \"{h['title']}\" (points:{h['points']}, comments:{h['num_comments']})"
            for h in hn[:7]
        )
        parts.append(f"## Reddit\n{reddit_text}\n\n## HackerNews\n{hn_text}")

    # Competitor
    comp_data = sources.get("competitor", {})
    if comp_data.get("status") == "ok" and comp_data.get("data"):
        comp_text = "\n".join(
            f"- @{c['author']}: \"{c['text'][:150]}\" "
            f"(likes:{c['likes']}, RT:{c['retweets']})"
            for c in comp_data["data"][:8]
        )
        parts.append(f"## 競合アカウント\n{comp_text}")

    return "\n\n".join(parts) if parts else "データ収集結果が空です。"


ANALYSIS_PROMPT_TEMPLATE = """\
あなたはコンテンツマーケティングの専門家です。
以下の5ソースから収集した市場データを分析し、コンテンツ改善の仮説を生成してください。

トピック: {topic}
チャネル: {channel}

--- 収集データ ---
{source_summary}
--- ここまで ---

以下のJSON形式で出力してください。JSON以外のテキストは含めないでください。

```json
{{
  "market_summary": "市場の現状サマリー（300字程度）。今バズっている投稿パターン、評価されているフォーマット、注目されている切り口を具体的に説明。",
  "trend_prediction": "トレンド予測（200字程度）。次に来そうなトピック/フォーマットと、その根拠。",
  "hypotheses": [
    {{
      "id": "H1",
      "priority": 9.0,
      "statement": "Because [具体的なデータに基づく観察], we believe [具体的な変更] will cause [期待される効果]",
      "test_variable": "hook | format | tone | cta | timing",
      "reasoning": "この仮説の根拠（どのデータソースから導かれたか）"
    }}
  ]
}}
```

仮説は{num_hypotheses}個生成してください。
priority は 1.0〜10.0 のスケールで、市場データの裏付け強度 × 実行容易性で評価。
各仮説は異なる test_variable をカバーしてください。
"""

VARIANT_PROMPT_TEMPLATE = """\
あなたはSNSコンテンツライターです。
以下の仮説に基づいて、A/Bテスト用の投稿バリアントを生成してください。

トピック: {topic}
チャネル: {channel}
仮説: {hypothesis}
テスト変数: {test_variable}

チャネル制約:
{channel_constraints}

以下のJSON形式で出力してください。JSON以外のテキストは含めないでください。

```json
{{
  "variant_a": {{
    "label": "バリアントAのラベル（例: 質問形フック）",
    "content": "実際の投稿文（そのままコピペで投稿できるクオリティ）"
  }},
  "variant_b": {{
    "label": "バリアントBのラベル（例: ステートメント形フック）",
    "content": "実際の投稿文"
  }},
  "primary_metric": "engagement_rate | likes | retweets | replies | open_rate | click_rate",
  "secondary_metrics": ["metric1", "metric2"],
  "expected_winner": "A or B",
  "expected_lift": "予想されるリフト（例: +20%）"
}}
```
"""

CHANNEL_CONSTRAINTS = {
    "x_twitter": "- 280文字以内（日本語は140文字程度が目安）\n- ハッシュタグは0-2個\n- スレッド形式も可\n- 画像添付を示す場合は[画像: 説明]と記載",
    "email": "- 件名は50文字以内\n- プレヘッダー80文字以内\n- CTA は1つに絞る\n- パーソナライズタグ使用可: {{name}}, {{company}}",
    "linkedin": "- 3000文字以内\n- 改行を多用して読みやすく\n- プロフェッショナルなトーン\n- ハッシュタグ3-5個",
}


def analyze_and_hypothesize(sources: Dict[str, Any], topic: str,
                            channel: str, num_hypotheses: int) -> Dict[str, Any]:
    """LLM で統合分析 → 仮説生成。"""
    logger.info("=== LLM 分析・仮説生成 ===")

    source_summary = _build_source_summary(sources)

    prompt = ANALYSIS_PROMPT_TEMPLATE.format(
        topic=topic,
        channel=channel,
        source_summary=source_summary,
        num_hypotheses=num_hypotheses,
    )

    try:
        from google.genai import types

        client = get_gemini_client()
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[prompt],
            config=types.GenerateContentConfig(temperature=0.4),
        )

        text = response.text or ""
        # Extract JSON from markdown code block
        json_match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if json_match:
            text = json_match.group(1)
        else:
            # Try finding raw JSON
            json_match = re.search(r"\{.*\}", text, re.DOTALL)
            if json_match:
                text = json_match.group(0)

        result = json.loads(text)
        n = len(result.get("hypotheses", []))
        logger.info("  仮説 %d個 生成完了", n)
        return result

    except json.JSONDecodeError as e:
        logger.error("  LLM レスポンスの JSON パース失敗: %s", e)
        logger.debug("  Raw response: %s", text[:500] if text else "empty")
        return {
            "market_summary": "JSON パースエラー。生テキスト: " + (text[:500] if text else ""),
            "trend_prediction": "",
            "hypotheses": [],
        }
    except Exception as e:
        logger.error("  LLM 分析失敗: %s", e)
        return {"market_summary": "", "trend_prediction": "", "hypotheses": []}


def generate_variants(hypothesis: Dict, topic: str, channel: str) -> Dict[str, Any]:
    """仮説に基づいてA/Bバリアントを生成。"""
    prompt = VARIANT_PROMPT_TEMPLATE.format(
        topic=topic,
        channel=channel,
        hypothesis=hypothesis.get("statement", ""),
        test_variable=hypothesis.get("test_variable", "hook"),
        channel_constraints=CHANNEL_CONSTRAINTS.get(channel, "特になし"),
    )

    try:
        from google.genai import types

        client = get_gemini_client()
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[prompt],
            config=types.GenerateContentConfig(temperature=0.6),
        )

        text = response.text or ""
        json_match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if json_match:
            text = json_match.group(1)
        else:
            json_match = re.search(r"\{.*\}", text, re.DOTALL)
            if json_match:
                text = json_match.group(0)

        return json.loads(text)

    except Exception as e:
        logger.warning("  バリアント生成失敗 (H%s): %s",
                       hypothesis.get("id", "?"), e)
        return {
            "variant_a": {"label": "A", "content": "生成失敗"},
            "variant_b": {"label": "B", "content": "生成失敗"},
            "primary_metric": "engagement_rate",
            "secondary_metrics": [],
        }


# =============================================================================
# Typefully Draft Creation
# =============================================================================


def create_typefully_drafts(experiment: Dict, auto_draft: bool) -> Optional[Dict]:
    """Typefully にドラフトを自動作成（--auto-draft 時のみ）。"""
    if not auto_draft:
        return None

    api_key = os.environ.get("TYPEFULLY_API_KEY")
    if not api_key:
        logger.warning("  TYPEFULLY_API_KEY が未設定。ドラフト作成をスキップ。")
        return None

    try:
        # Import from sibling module
        from typefully_client import TypefullyClient

        client = TypefullyClient(api_key=api_key)
        social_set_id = client.get_default_social_set_id()

        variants = experiment.get("variants", {})
        variant_a_content = variants.get("variant_a", {}).get("content", "")
        variant_b_content = variants.get("variant_b", {}).get("content", "")

        if not variant_a_content or not variant_b_content:
            logger.warning("  バリアントが空のためドラフト作成をスキップ。")
            return None

        result = client.create_ab_drafts(
            social_set_id=social_set_id,
            variant_a=variant_a_content,
            variant_b=variant_b_content,
            tag_name=f"ab-test-{experiment.get('hypothesis_id', 'unknown')}",
        )
        logger.info("  Typefully ドラフト作成完了: %s", result)
        return result
    except Exception as e:
        logger.warning("  Typefully ドラフト作成失敗: %s", e)
        return None


# =============================================================================
# Output
# =============================================================================


def save_outputs(output_dir: Path, topic: str, sources: Dict,
                 analysis: Dict, experiments: List[Dict]) -> None:
    """全出力を保存。"""
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_topic = sanitize_filename(topic)

    # 1. Market Report (Markdown)
    md_lines = [
        f"# Market Intelligence Report: {topic}",
        f"\n> Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "",
        "## 市場サマリー",
        "",
        analysis.get("market_summary", "(分析データなし)"),
        "",
        "## トレンド予測",
        "",
        analysis.get("trend_prediction", "(予測データなし)"),
        "",
        "## 仮説一覧",
        "",
    ]

    for h in analysis.get("hypotheses", []):
        md_lines.extend([
            f"### {h.get('id', '?')} (priority: {h.get('priority', '?')})",
            "",
            f"**Statement:** {h.get('statement', '')}",
            "",
            f"**Test variable:** {h.get('test_variable', '')}",
            "",
            f"**Reasoning:** {h.get('reasoning', '')}",
            "",
        ])

    if experiments:
        md_lines.extend(["## A/B バリアント", ""])
        for exp in experiments:
            variants = exp.get("variants", {})
            md_lines.extend([
                f"### 仮説 {exp.get('hypothesis_id', '?')}",
                "",
                f"**Variant A ({variants.get('variant_a', {}).get('label', 'A')}):**",
                "",
                f"> {variants.get('variant_a', {}).get('content', '')}",
                "",
                f"**Variant B ({variants.get('variant_b', {}).get('label', 'B')}):**",
                "",
                f"> {variants.get('variant_b', {}).get('content', '')}",
                "",
                f"Primary metric: {variants.get('primary_metric', '')}",
                "",
            ])

    market_report_path = output_dir / f"{safe_topic}_market_report.md"
    market_report_path.write_text("\n".join(md_lines), encoding="utf-8")

    # 2. Hypotheses (YAML)
    hypotheses_data = {
        "topic": topic,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "market_summary": analysis.get("market_summary", ""),
        "trend_prediction": analysis.get("trend_prediction", ""),
        "hypotheses": [],
    }

    for i, h in enumerate(analysis.get("hypotheses", [])):
        hyp_entry = {
            "id": h.get("id", f"H{i+1}"),
            "priority": h.get("priority", 5.0),
            "statement": h.get("statement", ""),
            "test_variable": h.get("test_variable", ""),
            "reasoning": h.get("reasoning", ""),
        }

        # Attach variants if generated
        matching_exp = next(
            (e for e in experiments if e.get("hypothesis_id") == h.get("id")),
            None,
        )
        if matching_exp:
            hyp_entry["variants"] = matching_exp.get("variants", {})

        hypotheses_data["hypotheses"].append(hyp_entry)

    hypotheses_path = output_dir / f"{safe_topic}_hypotheses.yaml"
    hypotheses_path.write_text(
        yaml.dump(hypotheses_data, allow_unicode=True, default_flow_style=False,
                  sort_keys=False, width=120),
        encoding="utf-8",
    )

    # 3. Experiment Design (YAML) for top hypothesis
    if experiments:
        top_exp = experiments[0]
        design = {
            "id": f"exp-{datetime.now().strftime('%Y-%m-%d')}-001",
            "channel": top_exp.get("channel", "x_twitter"),
            "hypothesis": top_exp.get("hypothesis_statement", ""),
            "test_variable": top_exp.get("test_variable", ""),
            "variants": [
                {
                    "id": "A",
                    "label": top_exp.get("variants", {}).get("variant_a", {}).get("label", "A"),
                    "content": top_exp.get("variants", {}).get("variant_a", {}).get("content", ""),
                },
                {
                    "id": "B",
                    "label": top_exp.get("variants", {}).get("variant_b", {}).get("label", "B"),
                    "content": top_exp.get("variants", {}).get("variant_b", {}).get("content", ""),
                },
            ],
            "primary_metric": top_exp.get("variants", {}).get("primary_metric", "engagement_rate"),
            "secondary_metrics": top_exp.get("variants", {}).get("secondary_metrics", []),
            "status": "planned",
            "results": None,
        }
        design_path = output_dir / f"{safe_topic}_experiment_design.yaml"
        design_path.write_text(
            yaml.dump(design, allow_unicode=True, default_flow_style=False,
                      sort_keys=False, width=120),
            encoding="utf-8",
        )

    # 4. Raw Data (JSON)
    raw_data = {
        "topic": topic,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": {},
    }
    for key, val in sources.items():
        raw_data["sources"][key] = {
            "status": val.get("status", "unknown"),
            "data": val.get("data"),
        }

    raw_path = output_dir / f"{safe_topic}_raw_data.json"
    raw_path.write_text(
        json.dumps(raw_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 5. Draft files
    if experiments:
        drafts_dir = output_dir / "drafts"
        drafts_dir.mkdir(exist_ok=True)
        for exp in experiments:
            h_id = exp.get("hypothesis_id", "unknown").lower()
            variants = exp.get("variants", {})

            va = variants.get("variant_a", {})
            (drafts_dir / f"{h_id}_variant_a.md").write_text(
                f"# {va.get('label', 'Variant A')}\n\n{va.get('content', '')}",
                encoding="utf-8",
            )

            vb = variants.get("variant_b", {})
            (drafts_dir / f"{h_id}_variant_b.md").write_text(
                f"# {vb.get('label', 'Variant B')}\n\n{vb.get('content', '')}",
                encoding="utf-8",
            )

    logger.info("=== 出力完了 ===")
    logger.info("  Market Report: %s", market_report_path)
    logger.info("  Hypotheses:    %s", hypotheses_path)
    logger.info("  Raw Data:      %s", raw_path)
    if experiments:
        logger.info("  Drafts:        %s/", drafts_dir)


# =============================================================================
# Main
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Content Optimizer: 市場調査 → 仮説生成 → A/Bバリアント作成",
    )
    parser.add_argument("--topic", "-t", required=False,
                        help="調査トピック（--test 時は省略可）")
    parser.add_argument("--channel", "-c", default="x_twitter",
                        choices=CHANNELS, help="チャネル (default: x_twitter)")
    parser.add_argument("--competitors", default="",
                        help="競合アカウント（カンマ区切り、例: user1,user2）")
    parser.add_argument("--lang", "-l", default="ja",
                        help="言語: ja, en, all (default: ja)")
    parser.add_argument("--days", "-d", type=int, default=7,
                        help="調査期間（日数、default: 7）")
    parser.add_argument("--num-hypotheses", type=int, default=5,
                        help="生成する仮説数 (default: 5)")
    parser.add_argument("--auto-draft", action="store_true",
                        help="Typefully にドラフトを自動作成")
    parser.add_argument("--output", "-o", default=None,
                        help="出力ディレクトリ")
    parser.add_argument("--dry-run", action="store_true",
                        help="API 呼び出しなしでパラメータ確認")
    parser.add_argument("--test", action="store_true",
                        help="セルフテスト（API 呼び出しなし）")

    args = parser.parse_args()

    # Self-test
    if args.test:
        logger.info("=== Self-test ===")
        logger.info("  ROOT_DIR: %s", ROOT_DIR)
        logger.info("  GEMINI_API_KEY: %s", "SET" if os.environ.get("GEMINI_API_KEY") else "NOT SET")
        logger.info("  X_BEARER_TOKEN: %s", "SET" if os.environ.get("X_BEARER_TOKEN") else "NOT SET")
        logger.info("  TYPEFULLY_API_KEY: %s", "SET" if os.environ.get("TYPEFULLY_API_KEY") else "NOT SET")
        logger.info("  Output dir: %s", DEFAULT_OUTPUT_DIR)
        logger.info("  Channels: %s", CHANNELS)

        # Test imports
        try:
            from google import genai  # noqa
            logger.info("  google-genai: OK")
        except ImportError:
            logger.warning("  google-genai: NOT INSTALLED")

        try:
            import yaml as _yaml  # noqa
            logger.info("  pyyaml: OK")
        except ImportError:
            logger.warning("  pyyaml: NOT INSTALLED")

        logger.info("  Self-test OK")
        return

    # Validate topic
    if not args.topic:
        parser.error("--topic は必須です（--test 時を除く）")

    competitors = [c.strip() for c in args.competitors.split(",") if c.strip()]

    # Dry run
    if args.dry_run:
        logger.info("=== Dry Run ===")
        logger.info("  Topic: %s", args.topic)
        logger.info("  Channel: %s", args.channel)
        logger.info("  Language: %s", args.lang)
        logger.info("  Days: %d", args.days)
        logger.info("  Hypotheses: %d", args.num_hypotheses)
        logger.info("  Competitors: %s", competitors or "(なし)")
        logger.info("  Auto-draft: %s", args.auto_draft)
        logger.info("  Output: %s", args.output or str(DEFAULT_OUTPUT_DIR))
        return

    # === Execute ===
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = sanitize_filename(args.topic)
    session_name = f"{timestamp}_{safe_topic}"

    output_base = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR
    output_dir = output_base / session_name

    logger.info("=" * 60)
    logger.info("Content Performance Optimizer - Hypothesis Generator")
    logger.info("=" * 60)
    logger.info("Topic:       %s", args.topic)
    logger.info("Channel:     %s", args.channel)
    logger.info("Language:    %s", args.lang)
    logger.info("Competitors: %s", competitors or "(なし)")
    logger.info("Output:      %s", output_dir)

    # Step 1: Collect
    sources = collect_all_sources(
        topic=args.topic,
        channel=args.channel,
        lang=args.lang,
        days=args.days,
        competitors=competitors,
    )

    # Step 2: Analyze & Hypothesize
    analysis = analyze_and_hypothesize(
        sources=sources,
        topic=args.topic,
        channel=args.channel,
        num_hypotheses=args.num_hypotheses,
    )

    # Step 3: Generate variants for top hypotheses
    experiments = []
    hypotheses = analysis.get("hypotheses", [])
    hypotheses.sort(key=lambda h: h.get("priority", 0), reverse=True)

    for h in hypotheses[:3]:  # Top 3 hypotheses
        logger.info("  バリアント生成: %s (%s)...",
                     h.get("id", "?"), h.get("test_variable", "?"))
        variants = generate_variants(h, args.topic, args.channel)
        exp = {
            "hypothesis_id": h.get("id", "?"),
            "hypothesis_statement": h.get("statement", ""),
            "test_variable": h.get("test_variable", ""),
            "channel": args.channel,
            "variants": variants,
        }
        experiments.append(exp)

        # Step 4: Auto-draft (optional)
        if args.auto_draft:
            create_typefully_drafts(exp, args.auto_draft)

    # Step 5: Save
    save_outputs(output_dir, args.topic, sources, analysis, experiments)

    logger.info("\n✓ 完了！%d個の仮説と%d個の実験設計を生成しました。",
                len(hypotheses), len(experiments))


if __name__ == "__main__":
    main()
