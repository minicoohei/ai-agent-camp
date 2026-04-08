#!/usr/bin/env python3
"""
Typefully API v2 クライアントライブラリ

Typefully API v2 を使用してソーシャルセット・ドラフトの管理を行う。
x-research の XAPIClient パターンに準拠。
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

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
# TypefullyClient
# =============================================================================


class TypefullyClient:
    """Typefully API v2 クライアント"""

    BASE_URL = "https://api.typefully.com/v2"

    def __init__(self, api_key: str = None):
        """
        クライアントを初期化する。

        Args:
            api_key: Typefully API キー。None の場合は環境変数 TYPEFULLY_API_KEY から取得。
        """
        if api_key is None:
            api_key = os.environ.get("TYPEFULLY_API_KEY")
        if not api_key:
            logger.error(
                "エラー: TYPEFULLY_API_KEY が設定されていません。\n"
                "\n"
                "設定方法:\n"
                "  1. Typefully (https://typefully.com) でアカウントを作成\n"
                "  2. Settings > API でAPIキーを発行\n"
                "  3. .env ファイルに追加: TYPEFULLY_API_KEY=your_key_here"
            )
            sys.exit(1)

        self.api_key = api_key.strip().strip('"').strip("'")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "content-optimizer/1.0",
            }
        )

    # -------------------------------------------------------------------------
    # 内部ユーティリティ
    # -------------------------------------------------------------------------

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """
        HTTP リクエストを実行し、エラーハンドリングを行う。

        Args:
            method: HTTP メソッド（GET / POST / PATCH / DELETE）
            path: Base URL からの相対パス（例: "/me"）
            params: クエリパラメータ
            json_body: リクエストボディ（JSON）

        Returns:
            requests.Response オブジェクト
        """
        url = f"{self.BASE_URL}{path}"
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json_body,
            timeout=30,
        )

        # Rate Limit ヘッダーをログ出力
        self._log_rate_limit(response)

        # 429: レート制限 → 待機してリトライ
        if response.status_code == 429:
            self._handle_rate_limit(response)
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_body,
                timeout=30,
            )
            self._log_rate_limit(response)

        # 400: 不正なリクエスト
        if response.status_code == 400:
            body = self._safe_json(response)
            logger.error(
                "エラー: リクエストが不正です (400)。\n  詳細: %s", body
            )
            sys.exit(1)

        # 401: 認証エラー
        if response.status_code == 401:
            logger.error(
                "エラー: 認証に失敗しました (401)。"
                " TYPEFULLY_API_KEY が正しいか確認してください。"
            )
            sys.exit(1)

        # 403: アクセス拒否
        if response.status_code == 403:
            body = self._safe_json(response)
            logger.error(
                "エラー: アクセスが拒否されました (403)。\n  詳細: %s\n"
                "  APIキーの権限・プランを確認してください。",
                body,
            )
            sys.exit(1)

        response.raise_for_status()
        return response

    def _safe_json(self, response: requests.Response) -> Any:
        """JSON パースを試み、失敗した場合はテキストを返す。"""
        try:
            return response.json()
        except Exception:
            return response.text

    def _log_rate_limit(self, response: requests.Response) -> None:
        """Rate Limit ヘッダーをデバッグログに出力する。"""
        limit = response.headers.get("X-RateLimit-User-Limit")
        remaining = response.headers.get("X-RateLimit-User-Remaining")
        reset = response.headers.get("X-RateLimit-User-Reset")
        if limit or remaining or reset:
            logger.debug(
                "Rate Limit - Limit: %s, Remaining: %s, Reset: %s",
                limit,
                remaining,
                reset,
            )

    def _handle_rate_limit(self, response: requests.Response) -> None:
        """429 レスポンスのレート制限処理。リセット時刻まで待機する。"""
        reset_header = response.headers.get("X-RateLimit-User-Reset")
        if reset_header:
            try:
                wait_seconds = int(reset_header) - int(time.time()) + 1
            except ValueError:
                wait_seconds = 60
        else:
            wait_seconds = 60

        wait_seconds = max(1, min(wait_seconds, 900))  # 1秒〜最大15分
        logger.info("  レート制限に到達。%d 秒待機中...", wait_seconds)
        time.sleep(wait_seconds)

    # -------------------------------------------------------------------------
    # /me
    # -------------------------------------------------------------------------

    def get_me(self) -> Dict[str, Any]:
        """
        GET /v2/me - 認証ユーザー情報を取得する。

        Returns:
            ユーザー情報の dict
        """
        response = self._request("GET", "/me")
        return self._safe_json(response)

    # -------------------------------------------------------------------------
    # /social-sets
    # -------------------------------------------------------------------------

    def list_social_sets(self) -> List[Dict[str, Any]]:
        """
        GET /v2/social-sets - ソーシャルセット一覧を取得する。

        Returns:
            ソーシャルセットのリスト
        """
        response = self._request("GET", "/social-sets")
        data = self._safe_json(response)
        # レスポンスがリストの場合はそのまま、dict の場合はデータキーを取得
        if isinstance(data, list):
            return data
        return data.get("data", data)

    def get_social_set(self, social_set_id: str) -> Dict[str, Any]:
        """
        GET /v2/social-sets/{id} - ソーシャルセット詳細を取得する。

        Args:
            social_set_id: ソーシャルセット ID

        Returns:
            ソーシャルセット詳細の dict
        """
        response = self._request("GET", f"/social-sets/{social_set_id}")
        return self._safe_json(response)

    # -------------------------------------------------------------------------
    # /social-sets/{id}/drafts
    # -------------------------------------------------------------------------

    def list_drafts(
        self,
        social_set_id: str,
        status: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """
        GET /v2/social-sets/{id}/drafts - ドラフト一覧を取得する。

        Args:
            social_set_id: ソーシャルセット ID
            status: フィルタするステータス（"draft" / "scheduled" / "published"）
            tag: フィルタするタグ名
            limit: 1回のリクエストで取得する最大件数（最大 50）
            offset: ページネーション用オフセット

        Returns:
            ドラフト一覧を含む dict（"data" キー配下にリスト）
        """
        params: Dict[str, Any] = {
            "limit": min(limit, 50),
            "offset": offset,
        }
        if status is not None:
            params["status"] = status
        if tag is not None:
            params["tag"] = tag

        response = self._request(
            "GET", f"/social-sets/{social_set_id}/drafts", params=params
        )
        return self._safe_json(response)

    def create_draft(
        self,
        social_set_id: str,
        content: str,
        schedule_date: Optional[str] = None,
        thread_tweets: Optional[List[Dict[str, Any]]] = None,
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        POST /v2/social-sets/{id}/drafts - ドラフトを作成する。

        Args:
            social_set_id: ソーシャルセット ID
            content: 投稿テキスト
            schedule_date: スケジュール日時（ISO 8601 形式）。省略するとドラフト保存のみ。
            thread_tweets: スレッド投稿の場合のリスト（例: [{"content": "2ツイート目"}]）
            tags: タグ ID のリスト

        Returns:
            作成されたドラフトの dict
        """
        body: Dict[str, Any] = {"content": content}
        if schedule_date is not None:
            body["schedule_date"] = schedule_date
        if thread_tweets is not None:
            body["thread_tweets"] = thread_tweets
        if tags is not None:
            body["tags"] = tags

        response = self._request(
            "POST", f"/social-sets/{social_set_id}/drafts", json_body=body
        )
        return self._safe_json(response)

    def get_draft(self, social_set_id: str, draft_id: str) -> Dict[str, Any]:
        """
        GET /v2/social-sets/{id}/drafts/{draft_id} - ドラフト詳細を取得する。

        Args:
            social_set_id: ソーシャルセット ID
            draft_id: ドラフト ID

        Returns:
            ドラフト詳細の dict
        """
        response = self._request(
            "GET", f"/social-sets/{social_set_id}/drafts/{draft_id}"
        )
        return self._safe_json(response)

    def update_draft(
        self, social_set_id: str, draft_id: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """
        PATCH /v2/social-sets/{id}/drafts/{draft_id} - ドラフトを更新する。

        Args:
            social_set_id: ソーシャルセット ID
            draft_id: ドラフト ID
            **kwargs: 更新するフィールド（content, schedule_date, tags など）

        Returns:
            更新されたドラフトの dict
        """
        response = self._request(
            "PATCH",
            f"/social-sets/{social_set_id}/drafts/{draft_id}",
            json_body=kwargs,
        )
        return self._safe_json(response)

    def delete_draft(self, social_set_id: str, draft_id: str) -> bool:
        """
        DELETE /v2/social-sets/{id}/drafts/{draft_id} - ドラフトを削除する。

        Args:
            social_set_id: ソーシャルセット ID
            draft_id: ドラフト ID

        Returns:
            削除成功の場合 True
        """
        response = self._request(
            "DELETE", f"/social-sets/{social_set_id}/drafts/{draft_id}"
        )
        # 204 No Content または 200 OK を成功とみなす
        return response.status_code in (200, 204)

    # -------------------------------------------------------------------------
    # ヘルパーメソッド
    # -------------------------------------------------------------------------

    def get_default_social_set_id(self) -> str:
        """
        最初のソーシャルセット ID を返す便利メソッド。

        Returns:
            ソーシャルセット ID の文字列

        Raises:
            SystemExit: ソーシャルセットが存在しない場合
        """
        sets = self.list_social_sets()
        if not sets:
            logger.error(
                "エラー: ソーシャルセットが見つかりません。"
                " Typefully でアカウントを接続してください。"
            )
            sys.exit(1)
        first = sets[0]
        # ID は "id" または "social_set_id" キーに格納される場合がある
        return str(first.get("id") or first.get("social_set_id", ""))

    def create_ab_drafts(
        self,
        social_set_id: str,
        variant_a: str,
        variant_b: str,
        tag_name: str = "ab-test",
    ) -> Dict[str, Any]:
        """
        A/B テスト用に 2 つのドラフトを作成し、同じタグで紐付ける。

        Args:
            social_set_id: ソーシャルセット ID
            variant_a: バリアント A のテキスト
            variant_b: バリアント B のテキスト
            tag_name: 両ドラフトに付与するタグ名（デフォルト: "ab-test"）

        Returns:
            {"variant_a": draft_a, "variant_b": draft_b} の dict
        """
        logger.info("A/B ドラフトを作成中（タグ: %s）...", tag_name)

        draft_a = self.create_draft(
            social_set_id=social_set_id,
            content=variant_a,
            tags=[tag_name],
        )
        logger.info("  バリアント A 作成完了: id=%s", draft_a.get("id"))

        draft_b = self.create_draft(
            social_set_id=social_set_id,
            content=variant_b,
            tags=[tag_name],
        )
        logger.info("  バリアント B 作成完了: id=%s", draft_b.get("id"))

        return {"variant_a": draft_a, "variant_b": draft_b}


# =============================================================================
# CLI エントリポイント
# =============================================================================


def _print_json(data: Any) -> None:
    """dict / list を整形して標準出力に出力する。"""
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Typefully API v2 クライアント CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "使用例:\n"
            "  %(prog)s --test\n"
            "  %(prog)s --list-sets\n"
            "  %(prog)s --list-drafts SET_ID\n"
            "  %(prog)s --list-drafts SET_ID --status draft\n"
            '  %(prog)s --create-draft SET_ID "本日のX投稿です"\n'
        ),
    )

    # 操作サブコマンド（排他グループ）
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--test",
        action="store_true",
        help="接続テスト: GET /v2/me を実行して認証ユーザー情報を表示",
    )
    group.add_argument(
        "--list-sets",
        action="store_true",
        help="ソーシャルセット一覧を表示",
    )
    group.add_argument(
        "--list-drafts",
        metavar="SET_ID",
        help="指定ソーシャルセットのドラフト一覧を表示",
    )
    group.add_argument(
        "--create-draft",
        nargs=2,
        metavar=("SET_ID", "CONTENT"),
        help="ドラフトを作成（SET_ID と投稿テキストを指定）",
    )

    # オプション
    parser.add_argument(
        "--status",
        choices=["draft", "scheduled", "published"],
        default=None,
        help="--list-drafts のフィルタ: ステータス",
    )
    parser.add_argument(
        "--tag",
        default=None,
        help="--list-drafts のフィルタ: タグ名",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="--list-drafts の取得件数（最大 50、デフォルト: 50）",
    )
    parser.add_argument(
        "--schedule",
        default=None,
        metavar="ISO8601",
        help="--create-draft のスケジュール日時（例: 2026-03-01T09:00:00Z）",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="デバッグログ（Rate Limit ヘッダーなど）を表示",
    )

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    client = TypefullyClient()

    # --test
    if args.test:
        logger.info("接続テスト: GET /v2/me ...")
        me = client.get_me()
        logger.info("認証成功。ユーザー情報:")
        _print_json(me)
        return

    # --list-sets
    if args.list_sets:
        logger.info("ソーシャルセット一覧を取得中...")
        sets = client.list_social_sets()
        logger.info("%d 件のソーシャルセットが見つかりました。", len(sets))
        _print_json(sets)
        return

    # --list-drafts SET_ID
    if args.list_drafts:
        set_id = args.list_drafts
        logger.info(
            "ドラフト一覧を取得中 (social_set_id=%s, status=%s)...",
            set_id,
            args.status or "all",
        )
        result = client.list_drafts(
            social_set_id=set_id,
            status=args.status,
            tag=args.tag,
            limit=args.limit,
        )
        drafts = result if isinstance(result, list) else result.get("data", result)
        logger.info("%d 件のドラフトが見つかりました。", len(drafts) if isinstance(drafts, list) else 1)
        _print_json(result)
        return

    # --create-draft SET_ID CONTENT
    if args.create_draft:
        set_id, content = args.create_draft
        logger.info(
            "ドラフトを作成中 (social_set_id=%s, schedule=%s)...",
            set_id,
            args.schedule or "なし（ドラフト保存）",
        )
        draft = client.create_draft(
            social_set_id=set_id,
            content=content,
            schedule_date=args.schedule,
        )
        logger.info("ドラフト作成完了: id=%s", draft.get("id"))
        _print_json(draft)
        return


if __name__ == "__main__":
    main()
