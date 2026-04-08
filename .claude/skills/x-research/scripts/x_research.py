#!/usr/bin/env python3
"""
X Research - X (Twitter) API v2 リアルタイム検索・分析ツール

X API v2 Recent Search エンドポイントを使用してツイートを検索し、
構造化レポート（Markdown + JSON + TXT）として出力する。
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
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


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)
logger = logging.getLogger(__name__)

# =============================================================================
# 定数
# =============================================================================

BASE_URL = "https://api.x.com/2/tweets/search/recent"

DEFAULT_OUTPUT_DIR = ROOT_DIR / "output" / "x-research"
DEFAULT_MAX_RESULTS = 50
DEFAULT_MAX_PAGES = 3
DEFAULT_DAYS = 7

TWEET_FIELDS = [
    "created_at",
    "public_metrics",
    "lang",
    "source",
    "conversation_id",
    "in_reply_to_user_id",
    "referenced_tweets",
    "entities",
]

USER_FIELDS = [
    "name",
    "username",
    "description",
    "public_metrics",
    "profile_image_url",
]

EXPANSIONS = ["author_id"]


# =============================================================================
# QueryBuilder
# =============================================================================


class QueryBuilder:
    """X API v2 検索クエリビルダー"""

    def __init__(self, keyword: str):
        self.keyword = keyword
        self.filters: List[str] = []

    def lang(self, lang_code: str) -> "QueryBuilder":
        if lang_code and lang_code != "all":
            self.filters.append(f"lang:{lang_code}")
        return self

    def exclude_retweets(self) -> "QueryBuilder":
        self.filters.append("-is:retweet")
        return self

    def exclude_replies(self) -> "QueryBuilder":
        self.filters.append("-is:reply")
        return self

    def has_media(self) -> "QueryBuilder":
        self.filters.append("has:media")
        return self

    def from_user(self, username: str) -> "QueryBuilder":
        self.filters.append(f"from:{username}")
        return self

    def build(self) -> str:
        parts = [self.keyword] + self.filters
        return " ".join(parts)


# =============================================================================
# XAPIClient
# =============================================================================


class XAPIClient:
    """X API v2 クライアント"""

    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {bearer_token}",
                "User-Agent": "ai-agent-camp-x-research/1.0",
            }
        )

    def search_recent(
        self,
        query: str,
        max_results: int = DEFAULT_MAX_RESULTS,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        next_token: Optional[str] = None,
        sort_order: str = "relevancy",
    ) -> Dict[str, Any]:
        """Recent Search エンドポイントを呼び出す"""
        params: Dict[str, Any] = {
            "query": query,
            "max_results": min(max(max_results, 10), 100),
            "tweet.fields": ",".join(TWEET_FIELDS),
            "user.fields": ",".join(USER_FIELDS),
            "expansions": ",".join(EXPANSIONS),
            "sort_order": sort_order,
        }
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        if next_token:
            params["next_token"] = next_token

        response = self.session.get(BASE_URL, params=params, timeout=30)

        if response.status_code == 429:
            self._handle_rate_limit(response)
            response = self.session.get(BASE_URL, params=params, timeout=30)

        if response.status_code == 400:
            try:
                body = response.json()
            except Exception:
                body = response.text
            logger.error("エラー: リクエストが不正です (400)。\n  詳細: %s", body)
            sys.exit(1)

        if response.status_code == 401:
            logger.error(
                "エラー: 認証に失敗しました。X_BEARER_TOKEN が正しいか確認してください。"
            )
            sys.exit(1)

        if response.status_code == 403:
            try:
                body = response.json()
            except Exception:
                body = response.text
            logger.error(
                "エラー: アクセスが拒否されました (403)。\n  詳細: %s\n"
                "  APIプランが Recent Search をサポートしているか確認してください。",
                body,
            )
            sys.exit(1)

        response.raise_for_status()
        return response.json()

    def search_all_pages(
        self,
        query: str,
        max_results_per_page: int = DEFAULT_MAX_RESULTS,
        max_pages: int = DEFAULT_MAX_PAGES,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        sort_order: str = "relevancy",
    ) -> Tuple[List[Dict], List[Dict], Dict]:
        """ページネーションを使って全ページ取得"""
        all_tweets: List[Dict] = []
        all_users: List[Dict] = []
        meta: Dict = {}
        next_token: Optional[str] = None

        for page in range(max_pages):
            logger.info("  ページ %d/%d を取得中...", page + 1, max_pages)
            result = self.search_recent(
                query=query,
                max_results=max_results_per_page,
                start_time=start_time,
                end_time=end_time,
                next_token=next_token,
                sort_order=sort_order,
            )

            tweets = result.get("data", [])
            users = result.get("includes", {}).get("users", [])
            meta = result.get("meta", {})

            all_tweets.extend(tweets)
            all_users.extend(users)

            next_token = meta.get("next_token")
            if not next_token:
                break

            time.sleep(1)

        # ユーザーの重複排除
        seen_ids: set = set()
        unique_users: List[Dict] = []
        for u in all_users:
            if u["id"] not in seen_ids:
                seen_ids.add(u["id"])
                unique_users.append(u)

        return all_tweets, unique_users, meta

    def _handle_rate_limit(self, response: requests.Response) -> None:
        """429 レスポンスのレート制限処理"""
        reset_time = response.headers.get("x-rate-limit-reset")
        if reset_time:
            wait_seconds = int(reset_time) - int(time.time()) + 1
            wait_seconds = max(wait_seconds, 1)
        else:
            wait_seconds = 15

        wait_seconds = min(wait_seconds, 900)  # 最大15分
        logger.info("  レート制限に到達。%d秒待機中...", wait_seconds)
        time.sleep(wait_seconds)


# =============================================================================
# ReportGenerator
# =============================================================================


class ReportGenerator:
    """検索結果からレポートを生成"""

    def __init__(
        self,
        tweets: List[Dict],
        users: List[Dict],
        meta: Dict,
        query: str,
        params: Dict,
    ):
        self.tweets = tweets
        self.users_map = {u["id"]: u for u in users}
        self.meta = meta
        self.query = query
        self.params = params

    def generate_markdown(self, top_n: int = 10) -> str:
        """Markdown レポートを生成"""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        topic = self.params.get("topic", "unknown")
        stats = self._calculate_stats()
        top_tweets = self._rank_tweets("like_count", top_n)
        hashtags = self._extract_hashtags()
        timeline = self._analyze_timeline()
        urls = self._extract_urls()

        lines = [
            f"# X Research Report: {topic}",
            "",
            f"> Generated: {now} | Query: `{self.query}` | Tweets: {len(self.tweets)}",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Total tweets | {stats['total_tweets']} |",
            f"| Unique authors | {stats['unique_authors']} |",
            f"| Total likes | {stats['total_likes']:,} |",
            f"| Total retweets | {stats['total_retweets']:,} |",
            f"| Total replies | {stats['total_replies']:,} |",
            f"| Avg likes/tweet | {stats['avg_likes']:.1f} |",
            f"| Date range | {stats['date_range']} |",
            "",
        ]

        # トップツイート
        if top_tweets:
            lines.append(f"## Top {len(top_tweets)} Tweets (by engagement)")
            lines.append("")
            for i, t in enumerate(top_tweets, 1):
                author = self.users_map.get(t.get("author_id", ""), {})
                username = author.get("username", "unknown")
                name = author.get("name", "")
                metrics = t.get("public_metrics", {})
                text = t.get("text", "").replace("\n", "\n> ")
                created = t.get("created_at", "")[:10]
                tweet_id = t.get("id", "")
                url = f"https://x.com/{username}/status/{tweet_id}"

                lines.append(f"### {i}. @{username} ({name})")
                lines.append("")
                lines.append(f"> {text}")
                lines.append(">")
                lines.append(f"> -- [{created}]({url})")
                lines.append(
                    f"> Likes: {metrics.get('like_count', 0):,} | "
                    f"Retweets: {metrics.get('retweet_count', 0):,} | "
                    f"Replies: {metrics.get('reply_count', 0):,}"
                )
                lines.append("")

        # ハッシュタグ分析
        if hashtags:
            lines.append("## Hashtag Analysis")
            lines.append("")
            lines.append("| Hashtag | Count |")
            lines.append("|---------|-------|")
            for tag, count in hashtags.most_common(20):
                lines.append(f"| #{tag} | {count} |")
            lines.append("")

        # 時系列分布
        if timeline:
            lines.append("## Timeline Distribution")
            lines.append("")
            lines.append("| Date | Tweet Count |")
            lines.append("|------|-------------|")
            for date_str in sorted(timeline.keys(), reverse=True):
                lines.append(f"| {date_str} | {timeline[date_str]} |")
            lines.append("")

        # URL一覧
        if urls:
            lines.append("## Shared URLs")
            lines.append("")
            lines.append("| URL | Count |")
            lines.append("|-----|-------|")
            for url_entry in urls[:20]:
                lines.append(
                    f"| {url_entry['display_url']} | {url_entry['count']} |"
                )
            lines.append("")

        # パラメータ
        lines.append("## Parameters")
        lines.append("")
        for key, val in self.params.items():
            lines.append(f"- **{key}**: {val}")
        lines.append("")

        return "\n".join(lines)

    def generate_json(self) -> Dict:
        """構造化 JSON を生成"""
        stats = self._calculate_stats()
        enriched_tweets = []
        for t in self.tweets:
            author = self.users_map.get(t.get("author_id", ""), {})
            enriched_tweets.append(
                {
                    "id": t.get("id"),
                    "text": t.get("text"),
                    "created_at": t.get("created_at"),
                    "lang": t.get("lang"),
                    "url": f"https://x.com/{author.get('username', 'i')}/status/{t.get('id', '')}",
                    "metrics": t.get("public_metrics", {}),
                    "author": {
                        "id": author.get("id"),
                        "username": author.get("username"),
                        "name": author.get("name"),
                        "followers": author.get("public_metrics", {}).get(
                            "followers_count", 0
                        ),
                        "verified": author.get("verified", False),
                    },
                }
            )

        return {
            "metadata": {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "query": self.query,
                "parameters": self.params,
                "api_meta": self.meta,
            },
            "stats": stats,
            "hashtags": dict(self._extract_hashtags().most_common(50)),
            "timeline": self._analyze_timeline(),
            "urls": self._extract_urls(),
            "tweets": enriched_tweets,
        }

    def generate_text(self) -> str:
        """プレーンテキスト要約を生成"""
        lines = []
        lines.append(f"X Research: {self.params.get('topic', '')}")
        lines.append(f"Query: {self.query}")
        lines.append(f"Total tweets: {len(self.tweets)}")
        lines.append("")
        lines.append("=" * 60)
        lines.append("")

        for t in self.tweets:
            author = self.users_map.get(t.get("author_id", ""), {})
            username = author.get("username", "unknown")
            metrics = t.get("public_metrics", {})
            text = t.get("text", "")
            created = t.get("created_at", "")[:16]
            likes = metrics.get("like_count", 0)

            lines.append(f"@{username} [{created}] (Likes: {likes})")
            lines.append(text)
            lines.append("-" * 40)
            lines.append("")

        return "\n".join(lines)

    def _calculate_stats(self) -> Dict:
        """統計情報を計算"""
        total_likes = sum(
            t.get("public_metrics", {}).get("like_count", 0) for t in self.tweets
        )
        total_retweets = sum(
            t.get("public_metrics", {}).get("retweet_count", 0) for t in self.tweets
        )
        total_replies = sum(
            t.get("public_metrics", {}).get("reply_count", 0) for t in self.tweets
        )
        unique_authors = len(set(t.get("author_id", "") for t in self.tweets))

        dates = [t.get("created_at", "")[:10] for t in self.tweets if t.get("created_at")]
        date_range = f"{min(dates)} ~ {max(dates)}" if dates else "N/A"

        n = len(self.tweets) or 1
        return {
            "total_tweets": len(self.tweets),
            "unique_authors": unique_authors,
            "total_likes": total_likes,
            "total_retweets": total_retweets,
            "total_replies": total_replies,
            "avg_likes": total_likes / n,
            "date_range": date_range,
        }

    def _rank_tweets(self, metric: str = "like_count", top_n: int = 10) -> List[Dict]:
        """ツイートをメトリクスでランキング"""
        return sorted(
            self.tweets,
            key=lambda t: t.get("public_metrics", {}).get(metric, 0),
            reverse=True,
        )[:top_n]

    def _extract_hashtags(self) -> Counter:
        """ハッシュタグの出現頻度を集計"""
        counter: Counter = Counter()
        for t in self.tweets:
            entities = t.get("entities", {})
            if entities and "hashtags" in entities:
                for ht in entities["hashtags"]:
                    counter[ht.get("tag", "")] += 1
        return counter

    def _extract_urls(self) -> List[Dict]:
        """URLを抽出し、頻度順で返す"""
        counter: Counter = Counter()
        url_map: Dict[str, str] = {}
        for t in self.tweets:
            entities = t.get("entities", {})
            if entities and "urls" in entities:
                for u in entities["urls"]:
                    expanded = u.get("expanded_url", "")
                    display = u.get("display_url", expanded)
                    if expanded and "twitter.com" not in expanded and "x.com" not in expanded:
                        counter[expanded] += 1
                        url_map[expanded] = display

        return [
            {"url": url, "display_url": url_map.get(url, url), "count": count}
            for url, count in counter.most_common(30)
        ]

    def _analyze_timeline(self) -> Dict[str, int]:
        """時系列分布を分析"""
        counter: Counter = Counter()
        for t in self.tweets:
            date_str = t.get("created_at", "")[:10]
            if date_str:
                counter[date_str] += 1
        return dict(counter)


# =============================================================================
# ヘルパー関数
# =============================================================================


def sanitize_filename(name: str) -> str:
    """ファイル名に使えない文字を除去"""
    name = re.sub(r'[<>:"/\\|?*\s]+', "_", name)
    name = name.strip("_.")
    return name[:80] if name else "unnamed"


def get_bearer_token() -> str:
    """Bearer Token を取得"""
    token = os.environ.get("X_BEARER_TOKEN")
    if not token:
        logger.error(
            "エラー: X_BEARER_TOKEN が設定されていません。\n"
            "\n"
            "設定方法:\n"
            "  1. X Developer Portal (https://developer.x.com/en/portal/dashboard) でアプリを作成\n"
            "  2. Bearer Token を取得\n"
            "  3. .env ファイルに追加: X_BEARER_TOKEN=your_token_here"
        )
        sys.exit(1)
    return token.strip().strip('"').strip("'")


# =============================================================================
# main
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="X (Twitter) API v2 リアルタイム検索・分析ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "使用例:\n"
            '  %(prog)s --topic "生成AI"\n'
            '  %(prog)s --topic "Claude AI" --lang en --no-retweets\n'
            '  %(prog)s --topic "OpenAI" --days 3 --sort recency\n'
            '  %(prog)s --query \'"Claude Code" OR "Cursor AI" lang:en\' --topic "AI IDE"\n'
        ),
    )

    # 必須パラメータ
    parser.add_argument("--topic", "-t", required=True, help="検索トピック・キーワード")

    # 検索オプション
    parser.add_argument(
        "--query", "-q", default=None, help="カスタムクエリ（topicの代わりに直接指定）"
    )
    parser.add_argument(
        "--lang", "-l", default="ja", choices=["ja", "en", "all"], help="言語フィルタ"
    )
    parser.add_argument(
        "--days", "-d", type=int, default=DEFAULT_DAYS, help="検索期間（日数、最大7）"
    )
    parser.add_argument(
        "--sort",
        "-s",
        default="relevancy",
        choices=["relevancy", "recency"],
        help="ソート順",
    )

    # フィルタオプション
    parser.add_argument("--no-retweets", action="store_true", help="リツイートを除外")
    parser.add_argument("--no-replies", action="store_true", help="リプライを除外")
    parser.add_argument(
        "--media-only", action="store_true", help="メディア付きツイートのみ"
    )
    parser.add_argument("--from-user", default=None, help="特定ユーザーのツイートのみ")
    parser.add_argument(
        "--min-likes", type=int, default=0, help="最小いいね数（取得後フィルタ）"
    )

    # 出力オプション
    parser.add_argument(
        "--max-results",
        "-m",
        type=int,
        default=DEFAULT_MAX_RESULTS,
        help="1ページあたりの最大取得数（10-100）",
    )
    parser.add_argument(
        "--max-pages", type=int, default=DEFAULT_MAX_PAGES, help="最大ページ数"
    )
    parser.add_argument("--top-n", type=int, default=10, help="トップツイート表示数")
    parser.add_argument("--output", "-o", default=None, help="出力ディレクトリ")
    parser.add_argument("--session", default=None, help="セッション名（出力フォルダ名）")

    # デバッグ
    parser.add_argument(
        "--dry-run", action="store_true", help="クエリを表示するだけで実行しない"
    )
    parser.add_argument(
        "--raw-json", action="store_true", help="生APIレスポンスをstderrに出力"
    )
    parser.add_argument(
        "--test", action="store_true", help="セルフテスト（API呼び出しなし）"
    )

    args = parser.parse_args()

    # --- セルフテスト ---
    if args.test:
        logger.info("self-test OK")
        return

    # --- クエリ構築 ---
    if args.query:
        query = args.query
    else:
        qb = QueryBuilder(args.topic)
        qb.lang(args.lang)
        if args.no_retweets:
            qb.exclude_retweets()
        if args.no_replies:
            qb.exclude_replies()
        if args.media_only:
            qb.has_media()
        if args.from_user:
            qb.from_user(args.from_user)
        query = qb.build()

    # --- 期間計算 ---
    # 7日間（最大）の場合は時間パラメータ省略（APIデフォルト=直近7日）
    # 7日未満の場合のみ start_time を指定
    days = min(max(args.days, 1), 7)
    start_iso = None
    end_iso = None
    if days < 7:
        end_time = datetime.now(timezone.utc) - timedelta(seconds=30)
        start_time = end_time - timedelta(days=days)
        start_iso = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_iso = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    # --- パラメータ記録 ---
    params = {
        "topic": args.topic,
        "query": query,
        "lang": args.lang,
        "days": days,
        "sort": args.sort,
        "no_retweets": args.no_retweets,
        "no_replies": args.no_replies,
        "media_only": args.media_only,
        "from_user": args.from_user,
        "min_likes": args.min_likes,
        "max_results": args.max_results,
        "max_pages": args.max_pages,
    }

    # --- dry-run ---
    if args.dry_run:
        logger.info("=== Dry Run ===")
        logger.info("Query:      %s", query)
        logger.info("Start:      %s", start_iso)
        logger.info("End:        %s", end_iso)
        logger.info("Sort:       %s", args.sort)
        logger.info("Max/page:   %s", args.max_results)
        logger.info("Max pages:  %s", args.max_pages)
        logger.info("Parameters: %s", json.dumps(params, ensure_ascii=False, indent=2))
        return

    # --- 認証 ---
    bearer_token = get_bearer_token()
    client = XAPIClient(bearer_token)

    # --- 検索実行 ---
    logger.info("X Research: 「%s」を検索中...", args.topic)
    logger.info("  クエリ: %s", query)
    logger.info("  期間: %s ~ %s", start_iso, end_iso)
    logger.info("")

    tweets, users, meta = client.search_all_pages(
        query=query,
        max_results_per_page=args.max_results,
        max_pages=args.max_pages,
        start_time=start_iso,
        end_time=end_iso,
        sort_order=args.sort,
    )

    if args.raw_json:
        print(
            json.dumps(
                {"tweets": tweets, "users": users, "meta": meta},
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )

    # --- min-likes フィルタ ---
    if args.min_likes > 0:
        before = len(tweets)
        tweets = [
            t
            for t in tweets
            if t.get("public_metrics", {}).get("like_count", 0) >= args.min_likes
        ]
        logger.info("  min-likes フィルタ: %d → %d tweets", before, len(tweets))

    # --- 結果チェック ---
    if not tweets:
        logger.info("検索結果: 0件。クエリやフィルタ条件を見直してください。")
        return

    logger.info("  取得完了: %d tweets, %d unique authors", len(tweets), len(users))
    logger.info('')

    # --- レポート生成 ---
    report = ReportGenerator(tweets, users, meta, query, params)

    md_content = report.generate_markdown(top_n=args.top_n)
    json_content = report.generate_json()
    txt_content = report.generate_text()

    # --- 出力 ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = sanitize_filename(args.topic)
    session_name = args.session or f"{timestamp}_{safe_topic}"

    output_base = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR
    output_dir = output_base / session_name
    output_dir.mkdir(parents=True, exist_ok=True)

    md_path = output_dir / f"{safe_topic}_report.md"
    json_path = output_dir / f"{safe_topic}_data.json"
    txt_path = output_dir / f"{safe_topic}_raw.txt"

    md_path.write_text(md_content, encoding="utf-8")
    json_path.write_text(
        json.dumps(json_content, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    txt_path.write_text(txt_content, encoding="utf-8")

    logger.info("=== 出力完了 ===")
    logger.info("  Markdown: %s", md_path)
    logger.info("  JSON:     %s", json_path)
    logger.info("  Text:     %s", txt_path)
    logger.info('')

    # --- サマリー表示 ---
    stats = report._calculate_stats()
    logger.info("--- サマリー ---")
    logger.info("  ツイート数:     %s", stats['total_tweets'])
    logger.info("  ユニーク著者:   %s", stats['unique_authors'])
    logger.info("  いいね合計:     %s", f"{stats['total_likes']:,}")
    logger.info("  リツイート合計: %s", f"{stats['total_retweets']:,}")
    logger.info("  リプライ合計:   %s", f"{stats['total_replies']:,}")
    logger.info("  期間:           %s", stats['date_range'])


if __name__ == "__main__":
    main()
