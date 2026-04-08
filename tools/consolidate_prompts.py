#!/usr/bin/env python3
"""
Consolidate AI Tutor Prompts from all 43 lesson files

This script reads all lesson command files and extracts prompts
into a single comprehensive AITUTOR_PROMPTS.txt file.
"""

import os
import re
from pathlib import Path
from datetime import datetime

# Configuration
PROJECT_ROOT = Path.home() / "aiagent-base"
COMMANDS_DIR = PROJECT_ROOT / ".cursor" / "commands" / "lesson"
OUTPUT_FILE = PROJECT_ROOT / "docs" / "AITUTOR_PROMPTS_COMPLETE.txt"

# Module definitions
MODULES = {
    0: ("セットアップ", [1, 2, 3, 4, 5]),
    1: ("バナー・画像生成", [1, 2, 3]),
    2: ("図表・フロー作成", [1, 2, 3]),
    3: ("スクリーンショット分析", [1, 2, 3, 4, 5, 6]),
    4: ("データ分析・BigQuery", [1, 2, 3, 4]),
    5: ("PowerPoint操作", [1, 2]),
    6: ("Slack連携", [1, 2]),
    7: ("動画生成・解析", [1, 2, 3, 4, 5, 6]),
    8: ("Google Apps Script", [1, 2, 3]),
    9: ("GitHub Actions", [1, 2]),
    10: ("Notion連携", [1, 2]),
    11: ("AIエージェント開発", [1, 2, 3, 4, 5]),
}


def extract_prompts_from_file(filepath):
    """Extract prompts from a lesson markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract YAML frontmatter
    description = ""
    yaml_match = re.search(r'^---\s*\ndescription:\s*"([^"]+)"\s*\n---', content, re.MULTILINE)
    if yaml_match:
        description = yaml_match.group(1)

    # Extract context section (📍)
    context = ""
    context_match = re.search(r'##\s*📍\s*今あなたがやっていること\s*\n(.+?)(?=##|\Z)', content, re.DOTALL)
    if context_match:
        context = context_match.group(1).strip()

    # Extract step prompts (🚀)
    steps = []
    step_pattern = r'##\s*🚀\s*Step\s*\d+[:\s]*(.+?)\n\n以下のプロンプト.*?：\s*\n\n```\s*\n(.+?)\n```'
    for match in re.finditer(step_pattern, content, re.DOTALL):
        step_title = match.group(1).strip()
        prompt = match.group(2).strip()
        steps.append((step_title, prompt))

    # Extract troubleshooting (⚠️)
    troubles = []
    trouble_section = re.search(r'##\s*⚠️\s*よくあるトラブルと解決方法\s*\n(.+?)(?=##|\Z)', content, re.DOTALL)
    if trouble_section:
        trouble_text = trouble_section.group(1)
        trouble_pattern = r'###\s*トラブル\d+:\s*「(.+?)」\s*\n\*\*原因\*\*:\s*(.+?)\n\*\*解決プロンプト\*\*:\s*\n```\s*\n(.+?)\n```'
        for match in re.finditer(trouble_pattern, trouble_text, re.DOTALL):
            title = match.group(1).strip()
            cause = match.group(2).strip()
            solution = match.group(3).strip()
            troubles.append((title, cause, solution))

    # Extract next step (➡️)
    next_step = ""
    next_match = re.search(r'##\s*➡️\s*次のステップ\s*\n(.+?)(?=##|\Z)', content, re.DOTALL)
    if next_match:
        next_step = next_match.group(1).strip()

    return {
        'description': description,
        'context': context,
        'steps': steps,
        'troubles': troubles,
        'next_step': next_step
    }


def format_lesson_prompts(module_num, lesson_num, data):
    """Format extracted data into AItutor prompt format"""
    output = []

    # Header
    output.append("-" * 80)
    output.append(f"LESSON: start-{module_num}-{lesson_num}")
    output.append(f"THEME: {data['description']}")
    output.append("-" * 80)
    output.append("")

    # Theme description
    output.append("【テーマ説明】")
    output.append(data['context'])
    output.append("")

    # Execution prompts
    for i, (title, prompt) in enumerate(data['steps'], 1):
        output.append(f"【実行プロンプト - Step {i}: {title}】")
        output.append("---")
        output.append(prompt)
        output.append("---")
        output.append("")

    # Troubleshooting
    if data['troubles']:
        output.append("【よくあるトラブル】")
        output.append("")
        for title, cause, solution in data['troubles']:
            output.append(f"■ {title}")
            output.append(f"原因: {cause}")
            output.append("解決プロンプト:")
            output.append("---")
            output.append(solution)
            output.append("---")
            output.append("")

    # Next step
    if data['next_step']:
        output.append("【次のステップ】")
        output.append(data['next_step'])
        output.append("")

    return "\n".join(output)


def main():
    """Main consolidation process"""
    print("🚀 Starting AI Tutor Prompts Consolidation...")
    print(f"📁 Commands directory: {COMMANDS_DIR}")
    print(f"📄 Output file: {OUTPUT_FILE}")
    print()

    # Create output content
    output_lines = []

    # Header
    output_lines.append("=" * 80)
    output_lines.append("AI TUTOR PROMPTS COLLECTION")
    output_lines.append("aiagent-base プロジェクト - 全43レッスン完全版")
    output_lines.append("")
    output_lines.append(f"作成日: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output_lines.append("対象: 非エンジニア向けAIエージェント研修")
    output_lines.append("形式: 対話型チューター用プロンプト集")
    output_lines.append("=" * 80)
    output_lines.append("")
    output_lines.append("")

    total_lessons = 0
    total_prompts = 0

    # Process each module
    for module_num in sorted(MODULES.keys()):
        module_name, lessons = MODULES[module_num]

        print(f"📦 Processing Module {module_num}: {module_name}")

        # Module header
        output_lines.append("=" * 80)
        output_lines.append(f"MODULE {module_num}: {module_name}")
        output_lines.append("=" * 80)
        output_lines.append("")

        # Process each lesson
        for lesson_num in lessons:
            filepath = COMMANDS_DIR / f"start-{module_num}-{lesson_num}.md"

            if not filepath.exists():
                print(f"  ⚠️  File not found: {filepath}")
                continue

            print(f"  ✅ Lesson {module_num}-{lesson_num}")

            try:
                data = extract_prompts_from_file(filepath)
                formatted = format_lesson_prompts(module_num, lesson_num, data)
                output_lines.append(formatted)
                output_lines.append("")

                total_lessons += 1
                total_prompts += len(data['steps']) + len(data['troubles'])
            except Exception as e:
                print(f"  ❌ Error processing {filepath}: {e}")

        output_lines.append("")

    # Footer
    output_lines.append("=" * 80)
    output_lines.append("END OF AITUTOR PROMPTS COLLECTION")
    output_lines.append("=" * 80)
    output_lines.append("")
    output_lines.append(f"Total lessons processed: {total_lessons}")
    output_lines.append(f"Total prompts extracted: {total_prompts}")
    output_lines.append("")

    # Write output file
    output_content = "\n".join(output_lines)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output_content)

    print()
    print(f"✅ Consolidation complete!")
    print(f"📊 Stats:")
    print(f"   - Lessons processed: {total_lessons}/43")
    print(f"   - Total prompts: {total_prompts}")
    print(f"   - Output file: {OUTPUT_FILE}")
    print(f"   - File size: {OUTPUT_FILE.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
