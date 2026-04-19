#!/usr/bin/env python3
"""
Command Verification System

Validates all lesson command files for structural integrity,
format consistency, and completeness.
"""

import re
import json
from pathlib import Path
from datetime import datetime
# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
COMMANDS_DIRS = [
    PROJECT_ROOT / ".cursor" / "commands" / "lesson",
    PROJECT_ROOT / ".claude" / "commands" / "lesson",
]
RESULTS_DIR = PROJECT_ROOT / "test-results" / "automated"

# Expected structure (flexible patterns to match real lesson files)
REQUIRED_SECTIONS = [
    r'##\s*(📍\s*(今あなたがやっていること|このセッションでやること)|🎯\s*準備チェック|このセッションでやること|セットアップ)',
    r'##\s*(🚀\s*Step\s*\d+|Step\s*\d+|\d+\.\s|実行|セットアップ方法)',
    r'##\s*(✅|チェック)',
    r'##\s*(➡️|🎉|次|Next)',
]

# Recommended but not required sections (generate warnings, not errors)
OPTIONAL_SECTIONS = [
    r'##\s*(⚠️|トラブル|よくある)',
]


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

    # Check required sections
    for section in REQUIRED_SECTIONS:
        if not re.search(section, content):
            errors.append(f"Missing section: {section}")

    # Check optional sections (warnings only)
    for section in OPTIONAL_SECTIONS:
        if not re.search(section, content):
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

    # Find skill references
    skill_refs = re.findall(r'(\w+-\w+(?:-\w+)?)(?:スキル|skill)', content)
    for skill in skill_refs:
        skill_path = PROJECT_ROOT / ".claude" / "skills" / skill
        if not skill_path.exists():
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

    return results['failed']


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
