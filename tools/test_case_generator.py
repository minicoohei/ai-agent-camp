#!/usr/bin/env python3
"""Generate markdown test cases from a use case document."""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path


USECASE_HEADER_RE = re.compile(r"^#{1,4} ユースケース: (.+)$", re.MULTILINE)
UC_ID_ROW_RE = re.compile(r"^\|\s*UC ID\s*\|\s*(UC-\d+)\s*\|$", re.MULTILINE)
TITLE_ROW_RE = re.compile(r"^\|\s*名称\s*\|\s*(.+?)\s*\|$", re.MULTILINE)
PRECONDITION_ROW_RE = re.compile(r"^\|\s*前提条件\s*\|\s*(.+?)\s*\|$", re.MULTILINE)
MAIN_FLOW_SPLIT_RE = re.compile(r"^#{2,5} 主フロー$", re.MULTILINE)
ALT_FLOW_SPLIT_RE = re.compile(r"^#{2,5} 代替フロー$", re.MULTILINE)
EXCEPTION_FLOW_SPLIT_RE = re.compile(r"^#{2,5} 例外フロー$", re.MULTILINE)
FLOW_ITEM_RE = re.compile(r"^\d+\.\s+(.+)$", re.MULTILINE)


@dataclass
class UseCaseDetail:
    uc_id: str
    name: str
    precondition: str
    main_flow: list[str] = field(default_factory=list)
    alternative_flows: list[str] = field(default_factory=list)
    exception_flows: list[str] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to usecases markdown file")
    parser.add_argument("--output", required=True, help="Path to output markdown file")
    parser.add_argument(
        "--coverage",
        default="normal_abnormal",
        choices=[
            "normal_only",
            "normal_abnormal",
            "normal_abnormal_boundary",
            "comprehensive",
        ],
        help="Coverage profile to generate",
    )
    parser.add_argument(
        "--prioritize",
        default="risk_based",
        choices=["risk_based", "coverage_based", "ai_suggested", "priority_all"],
        help="Priority assignment mode",
    )
    return parser.parse_args()


def split_section(block: str, header_re: re.Pattern[str], next_header_res: list[re.Pattern[str]]) -> str:
    match = header_re.search(block)
    if not match:
        return ""
    start = match.end()
    end = len(block)
    for pattern in next_header_res:
        next_match = pattern.search(block, start)
        if next_match:
            end = min(end, next_match.start())
    return block[start:end].strip()


def parse_usecase_details(markdown: str) -> list[UseCaseDetail]:
    blocks = re.split(r"(?=^#{1,4} ユースケース: )", markdown, flags=re.MULTILINE)
    details: list[UseCaseDetail] = []
    for block in blocks:
        if not re.match(r"^#{1,4} ユースケース: ", block):
            continue
        uc_id_match = UC_ID_ROW_RE.search(block)
        title_match = TITLE_ROW_RE.search(block)
        precondition_match = PRECONDITION_ROW_RE.search(block)
        if not (uc_id_match and title_match and precondition_match):
            continue

        main_flow_text = split_section(block, MAIN_FLOW_SPLIT_RE, [ALT_FLOW_SPLIT_RE, EXCEPTION_FLOW_SPLIT_RE])
        alt_flow_text = split_section(block, ALT_FLOW_SPLIT_RE, [EXCEPTION_FLOW_SPLIT_RE])
        exception_flow_text = split_section(block, EXCEPTION_FLOW_SPLIT_RE, [])

        details.append(
            UseCaseDetail(
                uc_id=uc_id_match.group(1),
                name=title_match.group(1),
                precondition=precondition_match.group(1),
                main_flow=FLOW_ITEM_RE.findall(main_flow_text),
                alternative_flows=FLOW_ITEM_RE.findall(alt_flow_text),
                exception_flows=FLOW_ITEM_RE.findall(exception_flow_text),
            )
        )
    return details


def requirement_hint(uc: UseCaseDetail) -> str:
    name = uc.name
    if "ログイン" in name or "認証" in name:
        return "認証情報"
    if "ワークスペース" in name:
        return "ワークスペース情報"
    if "ダッシュボード" in name:
        return "集計表示"
    if "タスク管理" in name:
        return "タスク入力"
    if "通知" in name:
        return "通知イベント"
    if "メンバー招待" in name or "権限" in name:
        return "メンバー権限"
    return "入力値"


def risk_priority(uc: UseCaseDetail, case_type: str) -> str:
    high_risk_keywords = ("ログイン", "認証", "タスク管理", "通知", "権限")
    if any(keyword in uc.name for keyword in high_risk_keywords):
        return "High"
    if case_type in {"セキュリティ", "異常系"}:
        return "High"
    if "ダッシュボード" in uc.name:
        return "Medium"
    return "Medium"


def coverage_priority(case_type: str) -> str:
    if case_type == "正常系":
        return "High"
    if case_type == "境界値":
        return "Medium"
    if case_type == "セキュリティ":
        return "High"
    return "Medium"


def ai_priority(uc: UseCaseDetail, case_type: str) -> str:
    if case_type == "セキュリティ":
        return "High"
    if "ログイン" in uc.name or "権限" in uc.name:
        return "High"
    if case_type == "正常系":
        return "High"
    return "Medium"


def build_priority_lines(uc: UseCaseDetail, case_type: str, mode: str) -> list[str]:
    mappings = {
        "risk_based": [("リスクベース", risk_priority(uc, case_type))],
        "coverage_based": [("カバレッジベース", coverage_priority(case_type))],
        "ai_suggested": [("AI推奨", ai_priority(uc, case_type))],
        "priority_all": [
            ("リスクベース", risk_priority(uc, case_type)),
            ("カバレッジベース", coverage_priority(case_type)),
            ("AI推奨", ai_priority(uc, case_type)),
        ],
    }
    return [f"**優先度**: {value} ({label})" for label, value in mappings[mode]]


def summarise_steps(source_steps: list[str], limit: int = 4) -> list[str]:
    if not source_steps:
        return ["手順はユースケース定義を参照する。"]
    return source_steps[:limit]


def make_normal_case(uc: UseCaseDetail) -> dict[str, object]:
    description = f"{uc.name} の主フローが成立することを確認する"
    steps = summarise_steps(uc.main_flow)
    expectations = [
        "主要な操作がエラーなく完了する",
        "画面または API 応答が次の状態へ遷移する",
        "必要なログまたはイベントが記録される",
    ]
    return {"view": "正常系", "description": description, "steps": steps, "expectations": expectations}


def make_abnormal_case(uc: UseCaseDetail) -> dict[str, object]:
    abnormal_steps = summarise_steps(uc.exception_flows or uc.alternative_flows)
    description = f"{uc.name} で代表的な異常系を処理できることを確認する"
    expectations = [
        "不正または失敗条件で処理が中断される",
        "利用者に分かるエラーまたは警告が表示される",
        "監査ログまたは障害ログに結果が記録される",
    ]
    return {"view": "異常系", "description": description, "steps": abnormal_steps, "expectations": expectations}


def make_boundary_case(uc: UseCaseDetail) -> dict[str, object]:
    hint = requirement_hint(uc)
    steps = [
        f"{hint} の最小値・最大値・閾値直前後のデータを準備する",
        f"{uc.name} の入力または更新操作を実行する",
        "結果表示、保存状態、エラー制御を確認する",
    ]
    expectations = [
        "許容範囲内の値は正常に受け付けられる",
        "範囲外の値は仕様どおり拒否または警告される",
    ]
    return {"view": "境界値", "description": f"{uc.name} の閾値付近を確認する", "steps": steps, "expectations": expectations}


def make_security_case(uc: UseCaseDetail) -> dict[str, object]:
    steps = [
        "権限不足または不正な入力を伴うリクエスト条件を準備する",
        f"{uc.name} を対象に操作または API 呼び出しを実行する",
        "権限制御、入力検証、ログ記録の結果を確認する",
    ]
    expectations = [
        "不正なアクセスまたは入力が拒否される",
        "機微データが漏えいしない",
        "監査可能なログが記録される",
    ]
    return {"view": "セキュリティ", "description": f"{uc.name} の認可・入力検証を確認する", "steps": steps, "expectations": expectations}


def build_case_set(uc: UseCaseDetail, coverage: str) -> list[dict[str, object]]:
    cases = [make_normal_case(uc)]
    if coverage in {"normal_abnormal", "normal_abnormal_boundary", "comprehensive"}:
        cases.append(make_abnormal_case(uc))
    if coverage in {"normal_abnormal_boundary", "comprehensive"}:
        cases.append(make_boundary_case(uc))
    if coverage == "comprehensive":
        cases.append(make_security_case(uc))
    return cases


def build_markdown(usecases: list[UseCaseDetail], coverage: str, prioritize: str) -> str:
    lines: list[str] = [
        "# テストケース一覧",
        "",
        f"- 生成条件: coverage=`{coverage}`, prioritize=`{prioritize}`",
        "",
    ]
    case_number = 1
    for uc in usecases:
        lines.append(f"## ユースケース {uc.uc_id}: {uc.name}")
        lines.append("")
        for case in build_case_set(uc, coverage):
            tc_id = f"TC-{case_number:03d}"
            lines.append(f"### テストケース ID: {tc_id}")
            lines.append(f"**ユースケース**: {uc.uc_id} - {uc.name}")
            lines.append(f"**観点**: {case['view']}")
            lines.append(f"**説明**: {case['description']}")
            lines.append("")
            lines.append("**前提条件**:")
            lines.append(f"- {uc.precondition}")
            lines.append("- システムがテスト可能な状態である")
            lines.append("")
            lines.append("**テスト手順**:")
            for index, step in enumerate(case["steps"], start=1):
                lines.append(f"{index}. {step}")
            lines.append("")
            lines.append("**期待値**:")
            for expectation in case["expectations"]:
                lines.append(f"- {expectation}")
            lines.extend(build_priority_lines(uc, str(case["view"]), prioritize))
            lines.append("**結果**: ⬜ 未実施")
            lines.append("")
            case_number += 1
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    markdown = input_path.read_text(encoding="utf-8")
    usecases = parse_usecase_details(markdown)
    if not usecases:
        raise SystemExit(f"ユースケース詳細を解析できませんでした: {input_path}")

    output = build_markdown(usecases, args.coverage, args.prioritize)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")
    generated_cases = sum(len(build_case_set(uc, args.coverage)) for uc in usecases)
    print(f"Wrote test cases to {output_path}")
    print(f"Use cases: {len(usecases)}")
    print(f"Generated cases: {generated_cases}")
    print(f"Coverage: {args.coverage}")
    print(f"Prioritization: {args.prioritize}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
