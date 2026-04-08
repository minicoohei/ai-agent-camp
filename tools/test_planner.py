#!/usr/bin/env python3
"""Generate a markdown test plan from a use case document."""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


USECASE_ROW_RE = re.compile(
    r"^\|\s*(UC-\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$"
)


@dataclass
class UseCase:
    uc_id: str
    name: str
    primary_actor: str
    requirements: str
    priority: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to usecases markdown file")
    parser.add_argument("--output", required=True, help="Path to output markdown file")
    parser.add_argument(
        "--experience-level",
        default="intermediate",
        choices=["beginner", "intermediate", "advanced"],
        help="Detail level for the generated plan",
    )
    parser.add_argument(
        "--test-scope",
        default="normal_abnormal",
        choices=[
            "normal_only",
            "normal_abnormal",
            "normal_abnormal_boundary",
            "comprehensive",
        ],
        help="Requested testing scope",
    )
    return parser.parse_args()


def parse_usecases(markdown: str) -> list[UseCase]:
    usecases: list[UseCase] = []
    for line in markdown.splitlines():
        match = USECASE_ROW_RE.match(line.strip())
        if not match:
            continue
        uc_id = match.group(1)
        if uc_id == "UC ID":
            continue
        usecases.append(
            UseCase(
                uc_id=uc_id,
                name=match.group(2),
                primary_actor=match.group(3),
                requirements=match.group(4),
                priority=match.group(5),
            )
        )
    return usecases


def infer_system_name(markdown: str) -> str:
    first_heading = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
    if first_heading and "TaskFlow" in first_heading.group(1):
        return "TaskFlow"
    if "TaskFlow" in markdown:
        return "TaskFlow"
    return "対象システム"


def scope_label(scope: str) -> str:
    return {
        "normal_only": "正常系中心",
        "normal_abnormal": "正常系・異常系",
        "normal_abnormal_boundary": "正常系・異常系・境界値",
        "comprehensive": "正常系・異常系・境界値・セキュリティ",
    }[scope]


def strategy_points(scope: str) -> list[str]:
    points = [
        "正常系シナリオで主要ユースケースの成立を確認する。",
    ]
    if scope in {"normal_abnormal", "normal_abnormal_boundary", "comprehensive"}:
        points.append("異常系シナリオで入力不備、権限不足、外部連携失敗時の制御を確認する。")
    if scope in {"normal_abnormal_boundary", "comprehensive"}:
        points.append("境界値シナリオで件数、文字数、状態遷移、期限などの閾値付近を確認する。")
    if scope == "comprehensive":
        points.append("認証、認可、入力検証、監査ログなどのセキュリティ観点を確認する。")
    return points


def schedule_for(level: str, scope: str) -> list[str]:
    final_phase = "異常系・再確認" if scope != "normal_only" else "結果整理・再確認"
    if level == "beginner":
        return [
            "フェーズ 1: テスト設計レビュー (1 営業日)",
            "フェーズ 2: 正常系テスト実行 (2 営業日)",
            f"フェーズ 3: {final_phase} (2 営業日)",
        ]
    if level == "advanced":
        return [
            "フェーズ 1: リスク分析とテスト設計 (2 営業日)",
            "フェーズ 2: API / 連携テスト (2 営業日)",
            f"フェーズ 3: {'E2E / 回帰テスト' if scope != 'normal_only' else 'E2E / 正常系回帰'} (2 営業日)",
            "フェーズ 4: 欠陥分析と exit criteria 判定 (1 営業日)",
        ]
    return [
        "フェーズ 1: テスト設計とレビュー (1 営業日)",
        "フェーズ 2: 機能テスト実行 (2 営業日)",
        "フェーズ 3: 回帰確認と報告 (1 営業日)",
    ]


def success_criteria(scope: str, level: str) -> list[str]:
    criteria = [
        "テストケース実行率: 100%",
        "重大バグ (Critical / High): 0 件",
        "主要ユースケースの正常系成功率: 100%",
    ]
    if scope != "normal_only":
        criteria.append("異常系テストで期待したエラーハンドリングが確認できること")
    if scope in {"normal_abnormal_boundary", "comprehensive"}:
        criteria.append("境界値テストで仕様外の不整合が検出されないこと")
    if scope == "comprehensive":
        criteria.append("認証・認可・入力検証に重大なセキュリティ欠陥がないこと")
    if level == "advanced":
        criteria.append("高優先度テストケースの完了率: 100%")
    return criteria


def build_plan(system_name: str, usecases: list[UseCase], level: str, scope: str) -> str:
    feature_names = [f"{uc.uc_id}: {uc.name}" for uc in usecases]
    external_dependencies: list[str] = []

    lines: list[str] = [
        f"# テスト計画書: {system_name}",
        "",
        "## 1. テスト概要",
        "### 1.1 テスト目的",
        f"- {system_name} の主要ユースケースを、{scope_label(scope)}の観点で検証する。",
        f"- テスト詳細度は `{level}` とし、レッスン既定値に合わせて生成する。",
        "",
        "### 1.2 テスト対象範囲",
    ]
    lines.extend(f"- {name}" for name in feature_names)
    lines.extend(
        [
            "",
            "### 1.3 除外範囲",
            "- 本レッスンでは性能試験、負荷試験、実環境移行試験は対象外とする。",
            "",
            "## 2. テスト方針",
            "### 2.1 テストレベル",
            "| レベル | 対象 | 手法 | 成果物 |",
            "|--------|------|------|--------|",
            "| 単体テスト | バリデーション、権限制御、集計ロジック | pytest など | 単体テスト結果 |",
            "| 結合テスト | API と外部サービス連携 | API / モック連携検証 | 結合テスト結果 |",
            "| E2E テスト | 主要ユーザーフロー | UI 操作ベース検証 | テストケース実施記録 |",
            "",
            "### 2.2 テスト観点",
        ]
    )
    lines.extend(f"- {point}" for point in strategy_points(scope))
    lines.extend(
        [
            "",
            "### 2.3 リスク前提",
            "- 認証、タスク更新、通知配信、権限管理は業務影響が高いため重点確認対象とする。",
            "- 外部システム連携のタイムアウトや送信失敗は異常系の代表リスクとして扱う。",
            "",
            "## 3. テスト環境",
            "- アプリケーション: ローカルまたは検証環境の TaskFlow",
            "- データ: テスト用ワークスペース、テストユーザー、通知用ダミー連携先",
            "- ログ: アプリケーションログ、監査ログ、外部通知結果ログ",
        ]
    )
    if external_dependencies:
        lines.append(f"- 依存先: {', '.join(external_dependencies)}")
    lines.extend(
        [
            "",
            "## 4. スケジュール",
        ]
    )
    lines.extend(f"- {item}" for item in schedule_for(level, scope))
    lines.extend(
        [
            "",
            "## 5. リソース",
            "- 人員: PM / QA 1 名、必要に応じて開発者レビュー",
            "- ツール: Markdown、pytest、Playwright、ログ確認ツール",
            "- 入力資料: `output/pm/usecases.md`, `output/pm/requirements-spec.md`",
            "",
            "## 6. 成功基準",
        ]
    )
    lines.extend(f"- {item}" for item in success_criteria(scope, level))
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    markdown = input_path.read_text(encoding="utf-8")
    usecases = parse_usecases(markdown)
    if not usecases:
        raise SystemExit(f"ユースケース一覧を解析できませんでした: {input_path}")

    content = build_plan(
        system_name=infer_system_name(markdown),
        usecases=usecases,
        level=args.experience_level,
        scope=args.test_scope,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"Wrote test plan to {output_path}")
    print(f"Use cases: {len(usecases)}")
    print(f"Experience level: {args.experience_level}")
    print(f"Test scope: {args.test_scope}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
