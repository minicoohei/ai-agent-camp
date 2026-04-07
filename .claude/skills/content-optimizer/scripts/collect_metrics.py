#!/usr/bin/env python3
"""
Collect Metrics - X API v2 からツイートメトリクスを収集し、バリアント比較レポートを生成。

Usage:
    python collect_metrics.py --tweet-ids "123456,789012"
    python collect_metrics.py --username minicoohei
    python collect_metrics.py --experiment-id exp-2026-02-18-001
    python collect_metrics.py --test
"""

import argparse
import json
import logging
import os
import sys
import time
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

X_API_BASE = "https://api.x.com/2"
DEFAULT_OUTPUT_DIR = ROOT_DIR / "output" / "content-optimizer" / "metrics"

TWEET_FIELDS = "created_at,public_metrics,non_public_metrics,text,author_id"
USER_FIELDS = "name,username,public_metrics"
# Note: non_public_metrics (impressions等) は OAuth 2.0 User Context + 自アカウントツイートのみ取得可能。
# Bearer token (App-Only Auth) では返却されないため、engagement_rate は 0 になる場合がある。


# =============================================================================
# X API Client (lightweight, reuses x-research patterns)
# =============================================================================


class MetricsClient:
    """X API v2 メトリクス取得クライアント。"""

    def __init__(self, bearer_token: str):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {bearer_token}",
            "User-Agent": "content-optimizer-metrics/1.0",
        })

    def get_tweets_by_ids(self, tweet_ids: List[str]) -> List[Dict]:
        """GET /2/tweets?ids=... でツイートメトリクスを取得。"""
        if not tweet_ids:
            return []

        # API allows max 100 IDs per request
        all_tweets = []
        for i in range(0, len(tweet_ids), 100):
            batch = tweet_ids[i:i + 100]
            ids_str = ",".join(batch)

            params = {
                "ids": ids_str,
                "tweet.fields": TWEET_FIELDS,
                "user.fields": USER_FIELDS,
                "expansions": "author_id",
            }

            response = self._request(f"{X_API_BASE}/tweets", params)
            if response:
                tweets = response.get("data", [])
                users = {u["id"]: u for u in response.get("includes", {}).get("users", [])}
                for tw in tweets:
                    tw["_author"] = users.get(tw.get("author_id", ""), {})
                all_tweets.extend(tweets)

            if i + 100 < len(tweet_ids):
                time.sleep(1)

        return all_tweets

    def get_user_tweets(self, username: str, max_results: int = 20) -> List[Dict]:
        """ユーザー名からユーザーIDを取得し、直近ツイートのメトリクスを返す。"""
        # Get user ID
        user_resp = self._request(
            f"{X_API_BASE}/users/by/username/{username}",
            {},
        )
        if not user_resp:
            logger.error("ユーザー @%s が見つかりません。", username)
            return []

        user_id = user_resp.get("data", {}).get("id")
        if not user_id:
            return []

        time.sleep(1)

        # Get tweets
        params = {
            "max_results": min(max(max_results, 5), 100),
            "tweet.fields": TWEET_FIELDS,
            "exclude": "retweets,replies",
        }

        response = self._request(f"{X_API_BASE}/users/{user_id}/tweets", params)
        if not response:
            return []

        return response.get("data", [])

    def _request(self, url: str, params: Dict) -> Optional[Dict]:
        """HTTP GET リクエスト with エラーハンドリング。"""
        try:
            response = self.session.get(url, params=params, timeout=30)

            if response.status_code == 429:
                reset_time = response.headers.get("x-rate-limit-reset")
                wait = max(int(reset_time) - int(time.time()) + 1, 1) if reset_time else 15
                wait = min(wait, 60)
                logger.info("  レート制限。%d秒待機...", wait)
                time.sleep(wait)
                response = self.session.get(url, params=params, timeout=30)

            if response.status_code in (400, 401, 403):
                logger.error("  API エラー (%d): %s",
                             response.status_code, response.text[:300])
                return None

            response.raise_for_status()
            return response.json()

        except (requests.RequestException, ValueError, KeyError) as e:
            logger.exception("  リクエスト失敗: %s", e)
            return None


# =============================================================================
# Metrics Analysis
# =============================================================================


def extract_metrics(tweet: Dict) -> Dict[str, Any]:
    """ツイートから構造化メトリクスを抽出。"""
    pm = tweet.get("public_metrics", {})
    npm = tweet.get("non_public_metrics", {})
    likes = pm.get("like_count", 0)
    retweets = pm.get("retweet_count", 0)
    replies = pm.get("reply_count", 0)
    quotes = pm.get("quote_count", 0)
    impressions = npm.get("impression_count", pm.get("impression_count", 0))

    engagement = likes + retweets + replies + quotes
    engagement_rate = (engagement / impressions * 100) if impressions > 0 else 0.0

    return {
        "tweet_id": tweet.get("id", ""),
        "text": tweet.get("text", "")[:200],
        "created_at": tweet.get("created_at", ""),
        "likes": likes,
        "retweets": retweets,
        "replies": replies,
        "quotes": quotes,
        "impressions": impressions,
        "engagement": engagement,
        "engagement_rate": round(engagement_rate, 2),
    }


def compare_variants(metrics_a: Dict, metrics_b: Dict) -> Dict[str, Any]:
    """2つのバリアントのメトリクスを比較。"""
    comparison = {}

    for key in ["likes", "retweets", "replies", "engagement", "engagement_rate", "impressions"]:
        val_a = metrics_a.get(key, 0)
        val_b = metrics_b.get(key, 0)

        if val_a > 0:
            diff_pct = round((val_b - val_a) / val_a * 100, 1)
        elif val_b > 0:
            diff_pct = 100.0
        else:
            diff_pct = 0.0

        winner = "A" if val_a > val_b else ("B" if val_b > val_a else "tie")

        comparison[key] = {
            "variant_a": val_a,
            "variant_b": val_b,
            "difference": round(val_b - val_a, 2),
            "difference_pct": diff_pct,
            "winner": winner,
        }

    # Overall winner (by engagement)
    eng_a = metrics_a.get("engagement", 0)
    eng_b = metrics_b.get("engagement", 0)
    overall_winner = "A" if eng_a > eng_b else ("B" if eng_b > eng_a else "tie")

    return {
        "metrics": comparison,
        "overall_winner": overall_winner,
        "confidence": "low" if (eng_a + eng_b) < 50 else ("medium" if (eng_a + eng_b) < 200 else "high"),
        "note": "エンゲージメント合計が50未満のため、統計的有意性は低いです。" if (eng_a + eng_b) < 50 else "",
    }


# =============================================================================
# Experiment Loading
# =============================================================================


def load_experiment(experiment_id: str) -> Optional[Dict]:
    """experiment_design.yaml を検索して読み込み。"""
    search_dir = ROOT_DIR / "output" / "content-optimizer"

    # Search in hypotheses/ and metrics/ subdirs
    for subdir in ["hypotheses", "metrics"]:
        base = search_dir / subdir
        if not base.exists():
            continue
        for session_dir in sorted(base.iterdir(), reverse=True):
            if not session_dir.is_dir():
                continue
            for yaml_file in session_dir.glob("*_experiment_design.yaml"):
                try:
                    data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
                    if data and data.get("id") == experiment_id:
                        logger.info("  実験設計を発見: %s", yaml_file)
                        return data
                except Exception:
                    continue

    logger.warning("  実験 '%s' が見つかりません。", experiment_id)
    return None


# =============================================================================
# Report Generation
# =============================================================================


def generate_report(tweet_metrics: List[Dict], comparison: Optional[Dict],
                    experiment: Optional[Dict]) -> str:
    """Markdown レポートを生成。"""
    lines = [
        "# Metrics Collection Report",
        f"\n> Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "",
    ]

    if experiment:
        lines.extend([
            f"## Experiment: {experiment.get('id', 'N/A')}",
            f"**Hypothesis:** {experiment.get('hypothesis', 'N/A')}",
            f"**Test variable:** {experiment.get('test_variable', 'N/A')}",
            "",
        ])

    # Metrics table
    lines.extend([
        "## Tweet Metrics",
        "",
        "| Tweet ID | Text | Likes | RT | Replies | Engagement | Rate |",
        "|----------|------|-------|----|---------|------------|------|",
    ])

    for m in tweet_metrics:
        text_preview = m["text"][:60].replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {m['tweet_id']} | {text_preview} | {m['likes']} | "
            f"{m['retweets']} | {m['replies']} | {m['engagement']} | "
            f"{m['engagement_rate']}% |"
        )

    # Comparison
    if comparison:
        lines.extend([
            "",
            "## Variant Comparison",
            "",
            f"**Overall Winner: Variant {comparison['overall_winner']}** "
            f"(confidence: {comparison['confidence']})",
            "",
        ])

        if comparison.get("note"):
            lines.append(f"> {comparison['note']}")
            lines.append("")

        lines.extend([
            "| Metric | Variant A | Variant B | Diff | Diff % | Winner |",
            "|--------|-----------|-----------|------|--------|--------|",
        ])

        for key, vals in comparison.get("metrics", {}).items():
            lines.append(
                f"| {key} | {vals['variant_a']} | {vals['variant_b']} | "
                f"{vals['difference']:+} | {vals['difference_pct']:+}% | "
                f"{vals['winner']} |"
            )

        lines.extend([
            "",
            "## Learnings",
            "",
            "- TODO: この実験から学んだことを記録してください",
            "- Winner のパターンを `learnings/top_hooks.json` に追加",
            "- Loser のパターンを `learnings/worst_hooks.json` に追加",
        ])

    return "\n".join(lines)


# =============================================================================
# Output
# =============================================================================


def save_results(output_dir: Path, tweet_metrics: List[Dict],
                 comparison: Optional[Dict], report: str,
                 experiment: Optional[Dict]) -> None:
    """結果を保存。"""
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Metrics JSON
    metrics_path = output_dir / f"{timestamp}_metrics.json"
    metrics_data = {
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "experiment_id": experiment.get("id") if experiment else None,
        "tweets": tweet_metrics,
        "comparison": comparison,
    }
    metrics_path.write_text(
        json.dumps(metrics_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Report Markdown
    report_path = output_dir / f"{timestamp}_report.md"
    report_path.write_text(report, encoding="utf-8")

    logger.info("=== 出力完了 ===")
    logger.info("  Metrics: %s", metrics_path)
    logger.info("  Report:  %s", report_path)


# =============================================================================
# Main
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Content Optimizer: ツイートメトリクス収集 & バリアント比較",  # noqa: RUF001
    )
    parser.add_argument("--tweet-ids", default="",
                        help="メトリクス取得対象ツイートID (カンマ区切り)")
    parser.add_argument("--username", "-u", default="",
                        help="ユーザーの直近投稿を取得")
    parser.add_argument("--experiment-id", "-e", default="",
                        help="実験IDで紐付けて比較")
    parser.add_argument("--output", "-o", default=None,
                        help="出力ディレクトリ")
    parser.add_argument("--test", action="store_true",
                        help="セルフテスト")

    args = parser.parse_args()

    # Self-test
    if args.test:
        logger.info("=== Self-test ===")
        logger.info("  ROOT_DIR: %s", ROOT_DIR)
        logger.info("  X_BEARER_TOKEN: %s",
                     "SET" if os.environ.get("X_BEARER_TOKEN") else "NOT SET")
        logger.info("  Output dir: %s", DEFAULT_OUTPUT_DIR)

        try:
            import yaml as _yaml
            _ = _yaml  # ensure import is used
            logger.info("  pyyaml: OK")
        except ImportError:
            logger.warning("  pyyaml: NOT INSTALLED")

        logger.info("  Self-test OK")
        return

    # Validate inputs
    if not args.tweet_ids and not args.username and not args.experiment_id:
        parser.error(
            "--tweet-ids, --username, --experiment-id のいずれかを指定してください。"  # noqa: RUF001
        )

    # Get bearer token
    token = os.environ.get("X_BEARER_TOKEN")
    if not token:
        logger.error("X_BEARER_TOKEN が環境変数に設定されていません。")
        sys.exit(1)

    client = MetricsClient(token)
    output_dir = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR

    experiment = None
    comparison = None
    all_metrics = []

    # Load experiment if specified
    if args.experiment_id:
        experiment = load_experiment(args.experiment_id)
        if experiment:
            # Extract tweet IDs from experiment
            variant_ids = []
            for v in experiment.get("variants", []):
                tid = v.get("tweet_id")
                if tid:
                    variant_ids.append(tid)

            if variant_ids:
                args.tweet_ids = ",".join(variant_ids)
                logger.info("  実験から %d 件のツイートIDを取得", len(variant_ids))
            else:
                logger.warning("  実験にツイートIDが設定されていません。--tweet-ids で指定してください。")

    # Collect metrics
    if args.tweet_ids:
        tweet_ids = [tid.strip() for tid in args.tweet_ids.split(",") if tid.strip()]
        logger.info("=== ツイートメトリクス取得 (%d件) ===", len(tweet_ids))

        tweets = client.get_tweets_by_ids(tweet_ids)
        for tw in tweets:
            all_metrics.append(extract_metrics(tw))

        # Compare if exactly 2 (A/B test)
        if len(all_metrics) == 2:
            logger.info("  2件のバリアントを比較中...")
            comparison = compare_variants(all_metrics[0], all_metrics[1])

    elif args.username:
        logger.info("=== @%s の直近投稿メトリクス取得 ===", args.username)
        tweets = client.get_user_tweets(args.username)
        for tw in tweets:
            all_metrics.append(extract_metrics(tw))

    if not all_metrics:
        logger.warning("メトリクスが取得できませんでした。")
        return

    logger.info("  %d 件のメトリクスを取得", len(all_metrics))

    # Sort by engagement
    all_metrics.sort(key=lambda x: x["engagement"], reverse=True)

    # Generate report
    report = generate_report(all_metrics, comparison, experiment)

    # Save
    save_results(output_dir, all_metrics, comparison, report, experiment)


if __name__ == "__main__":
    main()
