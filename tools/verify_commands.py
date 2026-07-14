#!/usr/bin/env python3
"""
Command Verification System

Validates all lesson command files for structural integrity,
format consistency, and completeness.
"""

import re
import json
from datetime import datetime
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
COMMANDS_DIRS = [
    PROJECT_ROOT / ".cursor" / "commands" / "lesson",
    PROJECT_ROOT / ".claude" / "commands" / "lesson",
]
RESULTS_DIR = PROJECT_ROOT / "test-results" / "automated"

# Expected structures are selected by both layout and filename locale suffix.
REQUIRED_SECTIONS = {
    "full": {
        "ja": [
            r"^#{2,3}\s*(?:📍|🚀|⚠️)?\s*(?:今あなた|このセッション|Step\s*\d+|ステップ\s*\d+|実施内容|実行手順|演習課題|実行コマンド)",
            r"^#{2,3}\s*(?:✅|🎯|✓|📊)?\s*(?:(?:\d+\.\s*)?成功|チェック|完了|成果物チェック|確認|ファイル確認|ゴール|演習課題)",
            r"^#{2,3}\s*(?:➡️|🎉|✅)?\s*(?:次|Next\b|完成と次|Module\s*\d+\s*完了|モジュール\s*\d+\s*完了|おめでとう)",
        ],
        "en": [
            r"^#{2,3}\s*(?:📍|🚀|⚠️)?\s*(?:Step\s*\d+|Content\b|Execution\b|Commands?\b)",
            r"^#{2,3}\s*(?:✅|🎯|✓|📊)?\s*(?:Check|Completion\b|(?:\d+\.\s*)?Success\b|Deliverables?|(?:File\s+)?Verification\b|Exercises\b)",
            r"^#{2,3}\s*(?:➡️|🎉|✅)?\s*(?:Next\b|Completion(?: Criteria| and Next Steps)?|Module\s*\d+\s*Complete|Congratulations)",
        ],
        "es": [
            r"^#{2,3}\s*(?:📍|🚀|⚠️)?\s*(?:Step\s*\d+|Paso\s*\d+|Contenido\b|Ejecuci[oó]n\b|Comandos?\b)",
            r"^#{2,3}\s*(?:✅|🎯|✓|📊)?\s*(?:Punto\b|(?:Lista de )?Verificaci[oó]n\b|Comprobaci[oó]n\b|(?:\d+\.\s*)?Criterios\b|Entregables?|Ejercicios\b|Comandos de verificaci[oó]n)",
            r"^#{2,3}\s*(?:➡️|🎉|✅)?\s*(?:Siguientes?\b|Pr[oó]ximo|Next\b|Completion Criteria|Finalizaci[oó]n y siguientes pasos|Module\s*\d+\s*Completado|Felicitaciones)",
        ],
    },
    "compact": {
        "ja": [r"^##\s*このセッションでやること", r"^##\s*前提条件", r"^##\s*ゴール", r"^##\s*次のステップ"],
        "en": [r"^##\s*What You'll Do", r"^##\s*Prerequisites", r"^##\s*Goals", r"^##\s*Next Steps"],
        "es": [r"^##\s*Lo que har[aá] en esta sesi[oó]n", r"^##\s*Requisitos previos", r"^##\s*Objetivos", r"^##\s*Siguientes pasos"],
    },
    "reference": {
        "ja": [r"^##\s*(?:このレッスンでやること|What this command does)", r"^##\s*(?:進め方|Steps)", r"^##\s*(?:参考リンク|Reference)"],
        "en": [r"^##\s*What this (?:lesson covers|command does)", r"^##\s*(?:How to proceed|Steps)", r"^##\s*Reference"],
        "es": [r"^##\s*(?:Qu[eé] cubre esta lecci[oó]n|What this command does)", r"^##\s*(?:C[oó]mo avanzar|Steps)", r"^##\s*(?:Enlaces de referencia|Reference)"],
    },
}

# Layouts are identified by headings that are structurally distinctive for
# that document type. This deliberately avoids lesson-id allowlists: newly
# added lessons using an established structure are validated without a code
# change. The full profile is the safe default, while reference detection uses
# its unique introductory heading so a missing later section is still reported
# against the reference contract.
LAYOUT_SIGNATURES = {
    "reference": {
        "ja": [r"^##\s*(?:このレッスンでやること|What this command does)"],
        "en": [r"^##\s*What this (?:lesson covers|command does)"],
        "es": [r"^##\s*(?:Qu[eé] cubre esta lecci[oó]n|What this command does)"],
    },
    "compact": {
        "ja": [r"^##\s*前提条件", r"^##\s*ゴール"],
        "en": [r"^##\s*Prerequisites", r"^##\s*Goals"],
        "es": [r"^##\s*Requisitos previos", r"^##\s*Objetivos"],
    },
}

# Recommended but not required sections (generate warnings, not errors).
OPTIONAL_SECTIONS = {
    "ja": [r"^#{2,3}\s*(?:⚠️\s*)?(?:トラブル|よくある)"],
    "en": [r"^#{2,3}\s*(?:⚠️\s*|🔧\s*)?(?:Common Issues|Troubleshooting)"],
    "es": [r"^#{2,3}\s*(?:⚠️\s*|🔧\s*)?(?:Problemas comunes|Soluci[oó]n de problemas)"],
}


def locale_for_path(filepath: Path) -> str:
    """Infer command locale from its filename suffix."""
    if filepath.name.endswith(".en.md"):
        return "en"
    if filepath.name.endswith(".es.md"):
        return "es"
    return "ja"


def layout_for_content(content: str, locale: str) -> str:
    """Infer the layout profile from locale-specific heading signatures."""
    flags = re.MULTILINE | re.IGNORECASE
    for layout in ("reference", "compact"):
        signatures = LAYOUT_SIGNATURES[layout][locale]
        if all(re.search(signature, content, flags) for signature in signatures):
            return layout
    return "full"


def validate_file_structure(filepath):
    """Validate file structure and sections"""
    errors = []
    warnings = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {'errors': [f"Failed to read file: {e}"], 'warnings': []}

    # Check YAML frontmatter (--- block with description field somewhere inside)
    if not re.search(r'^---\s*\n(?:.*\n)*?description:\s*"[^"]+"\s*\n(?:.*\n)*?---', content, re.MULTILINE):
        errors.append("Missing or invalid YAML frontmatter")

    locale = locale_for_path(Path(filepath))
    layout = layout_for_content(content, locale)

    # Check required sections
    for section in REQUIRED_SECTIONS[layout][locale]:
        if not re.search(section, content, re.MULTILINE | re.IGNORECASE):
            errors.append(f"Missing section: {section}")

    # Check optional sections (warnings only)
    for section in OPTIONAL_SECTIONS[locale]:
        if not re.search(section, content, re.MULTILINE | re.IGNORECASE):
            warnings.append(f"Missing optional section: {section}")

    # Check step prompts are in code blocks
    steps = re.findall(r'##\s*(?:🚀\s*)?Step\s*\d+(.+?)(?=##|\Z)', content, re.DOTALL)
    if steps:
        for i, step in enumerate(steps, 1):
            if '```' not in step:
                warnings.append(f"Step {i} missing code block for prompt")

    # Check troubleshooting format
    trouble_section = re.search(r'##\s*(?:⚠️|トラブル|よくある).*?\n(.+?)(?=##|\Z)', content, re.DOTALL)
    if trouble_section:
        troubles = re.findall(r'###\s*トラブル\d+:', trouble_section.group(1))
        if len(troubles) < 3:
            warnings.append(f"Only {len(troubles)} troubleshooting items (recommended: 3+)")

    # Check next step reference
    next_match = re.search(r'`/start-\d+-\d+`', content)
    if not next_match:
        warnings.append("Next step reference not found")

    return {'errors': errors, 'warnings': warnings}


def validate_link_references(filepath):
    """Validate internal tool/skill references"""
    errors = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return {'errors': ['Failed to read file']}

    # Find tool references (e.g., uv run python tools/something.py)
    tool_refs = re.findall(r'python\s+tools/(\S+\.py)', content)
    for tool in tool_refs:
        tool_path = PROJECT_ROOT / "tools" / tool
        if not tool_path.exists():
            errors.append(f"Referenced tool does not exist: tools/{tool}")

    # Find explicit skill path references. Natural-language hyphenated phrases
    # are not reliable identifiers (for example, "meeting-notes skill").
    skill_refs = re.findall(
        r"(?:\.claude/)?skills/([a-z][a-z0-9-]*)(?=/)",
        content,
        re.IGNORECASE,
    )
    for skill in skill_refs:
        skill_paths = [
            PROJECT_ROOT / "skills" / skill,
            PROJECT_ROOT / ".claude" / "skills" / skill,
        ]
        if not any(path.exists() for path in skill_paths):
            errors.append(f"Referenced skill does not exist: {skill}")

    return {'errors': errors}


def validate_all_commands():
    """Run validation on all command files"""
    command_files = []
    for cmd_dir in COMMANDS_DIRS:
        if cmd_dir.exists():
            command_files.extend(sorted(cmd_dir.glob("start-*.md")))

    results = {
        'timestamp': datetime.now().isoformat(),
        'total_files': len(command_files),
        'passed': 0,
        'failed': 0,
        'files': {}
    }

    # Process all lesson command files that exist in the repo.
    for filepath in command_files:
        try:
            file_key = str(filepath.relative_to(PROJECT_ROOT))
        except ValueError:
            file_key = None
            for cmd_dir in COMMANDS_DIRS:
                try:
                    file_key = f"{cmd_dir.name}/{filepath.relative_to(cmd_dir)}"
                    break
                except ValueError:
                    continue
            if file_key is None:
                file_key = str(filepath)

        # Run validations
        structure_result = validate_file_structure(filepath)
        link_result = validate_link_references(filepath)

        all_errors = structure_result['errors'] + link_result['errors']
        all_warnings = structure_result.get('warnings', [])

        if all_errors:
            results['failed'] += 1
            status = 'FAILED'
        else:
            results['passed'] += 1
            status = 'PASSED'

        results['files'][file_key] = {
            'status': status,
            'errors': all_errors,
            'warnings': all_warnings
        }

    return results


def generate_report(results):
    """Generate validation report"""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # JSON report
    json_file = RESULTS_DIR / "structure-validation.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Text summary
    summary = []
    summary.append("=" * 80)
    summary.append("COMMAND VALIDATION REPORT")
    summary.append("=" * 80)
    summary.append(f"Generated: {results['timestamp']}")
    summary.append("")
    summary.append(f"Total files checked: {results['total_files']}")
    summary.append(f"✅ Passed: {results['passed']}")
    summary.append(f"❌ Failed: {results['failed']}")
    summary.append("")

    if results['failed'] > 0:
        summary.append("FAILURES:")
        summary.append("-" * 80)
        for file_key, data in results['files'].items():
            if data['status'] == 'FAILED':
                summary.append(f"\n{file_key}:")
                for error in data['errors']:
                    summary.append(f"  ❌ {error}")
                for warning in data['warnings']:
                    summary.append(f"  ⚠️  {warning}")

    summary_file = RESULTS_DIR / "validation-summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(summary))

    return json_file, summary_file


def main():
    """Main execution"""
    print("🔍 Starting command validation...")
    for cmd_dir in COMMANDS_DIRS:
        print(f"📁 Commands directory: {cmd_dir}")
    print()

    results = validate_all_commands()

    json_file, summary_file = generate_report(results)

    print(f"\n✅ Validation complete!")
    print(f"📊 Results:")
    print(f"   - Files checked: {results['total_files']}")
    print(f"   - Passed: {results['passed']}")
    print(f"   - Failed: {results['failed']}")
    print(f"\n📄 Reports generated:")
    print(f"   - JSON: {json_file}")
    print(f"   - Summary: {summary_file}")

    return 1 if results['failed'] else 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
