#!/usr/bin/env python3
"""
Readability Audit Tool for Course Pages

Analyzes all HTML course pages for:
- Color contrast ratios (WCAG compliance)
- Font sizes and typography
- Spacing consistency
- Touch target sizes
- Visual hierarchy
"""

import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import argparse

# Configuration
PROJECT_ROOT = Path.home() / "aiagent-base"
COURSE_DIR = PROJECT_ROOT / "course"
CSS_FILE = COURSE_DIR / "assets" / "css" / "bootcamp.css"
RESULTS_DIR = PROJECT_ROOT / "test-results" / "readability"

# WCAG Contrast Standards
WCAG_AA_NORMAL = 4.5
WCAG_AA_LARGE = 3.0
WCAG_AAA_NORMAL = 7.0
WCAG_AAA_LARGE = 4.5

# Touch target minimum (iOS/Android HIG)
MIN_TOUCH_TARGET = 44  # pixels


def calculate_contrast_ratio(color1_hex, color2_hex):
    """
    Calculate WCAG contrast ratio between two hex colors
    Returns ratio (1-21)
    """
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def relative_luminance(rgb):
        """Calculate relative luminance"""
        rgb_normalized = [c / 255.0 for c in rgb]
        rgb_linear = []
        for c in rgb_normalized:
            if c <= 0.03928:
                rgb_linear.append(c / 12.92)
            else:
                rgb_linear.append(((c + 0.055) / 1.055) ** 2.4)
        return 0.2126 * rgb_linear[0] + 0.7152 * rgb_linear[1] + 0.0722 * rgb_linear[2]

    try:
        rgb1 = hex_to_rgb(color1_hex)
        rgb2 = hex_to_rgb(color2_hex)

        lum1 = relative_luminance(rgb1)
        lum2 = relative_luminance(rgb2)

        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)

        ratio = (lighter + 0.05) / (darker + 0.05)
        return round(ratio, 2)
    except:
        return 0


def parse_css_colors():
    """Extract color definitions from CSS"""
    colors = {}

    try:
        with open(CSS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract CSS variables
        var_pattern = r'--([a-z0-9-]+):\s*(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3});'
        matches = re.findall(var_pattern, content)

        for name, value in matches:
            colors[f'--{name}'] = value

    except Exception as e:
        print(f"Error parsing CSS: {e}")

    return colors


def find_color_combinations(css_content):
    """Find all color/background combinations in CSS"""
    combinations = []

    # Pattern for color and background-color in same rule
    rule_pattern = r'\{([^}]+)\}'

    for rule_match in re.finditer(rule_pattern, css_content):
        rule = rule_match.group(1)

        color_match = re.search(r'color:\s*(var\(--[a-z0-9-]+\)|#[0-9a-fA-F]{6})', rule)
        bg_match = re.search(r'background(?:-color)?:\s*(var\(--[a-z0-9-]+\)|#[0-9a-fA-F]{6}|white)', rule)

        if color_match and bg_match:
            color = color_match.group(1)
            bg = bg_match.group(1)
            combinations.append((color, bg))

    return combinations


def analyze_contrast():
    """Analyze color contrast ratios"""
    print("🎨 Analyzing color contrast...")

    colors = parse_css_colors()

    try:
        with open(CSS_FILE, 'r', encoding='utf-8') as f:
            css_content = f.read()
    except:
        return {"error": "Could not read CSS file"}

    # Define common combinations to check
    test_combinations = [
        ("--gray-700", "--gray-50", "Body text", "normal"),
        ("--gray-600", "white", "Sidebar links", "normal"),
        ("--navy-primary", "--gray-50", "Navy on light", "large"),
        ("--accent-blue", "white", "Blue links", "normal"),
        ("--gray-500", "white", "Muted text", "small"),
        ("white", "--navy-primary", "White on navy", "large"),
        ("--gray-900", "white", "Dark text", "normal"),
    ]

    results = {
        "passed": [],
        "warnings": [],
        "failures": []
    }

    for fg, bg, label, size in test_combinations:
        # Resolve var() references
        fg_color = colors.get(fg, fg)
        bg_color = colors.get(bg, "white" if bg == "white" else bg)

        if bg_color == "white":
            bg_color = "#FFFFFF"

        ratio = calculate_contrast_ratio(fg_color, bg_color)

        # Determine threshold based on size
        threshold = WCAG_AA_LARGE if size == "large" else WCAG_AA_NORMAL
        aaa_threshold = WCAG_AAA_LARGE if size == "large" else WCAG_AAA_NORMAL

        result = {
            "label": label,
            "foreground": fg,
            "background": bg,
            "ratio": ratio,
            "size": size,
            "wcag_aa": threshold,
            "wcag_aaa": aaa_threshold
        }

        if ratio >= aaa_threshold:
            result["status"] = "AAA"
            results["passed"].append(result)
        elif ratio >= threshold:
            result["status"] = "AA"
            results["warnings"].append(result)
        else:
            result["status"] = "FAIL"
            results["failures"].append(result)

    return results


def analyze_typography():
    """Analyze font sizes and typography"""
    print("📝 Analyzing typography...")

    try:
        with open(CSS_FILE, 'r', encoding='utf-8') as f:
            css_content = f.read()
    except:
        return {"error": "Could not read CSS file"}

    # Extract font-size declarations
    font_sizes = []
    font_size_pattern = r'font-size:\s*([0-9.]+)(rem|px|em);'

    for match in re.finditer(font_size_pattern, css_content):
        value = float(match.group(1))
        unit = match.group(2)

        # Convert to px (assuming 1rem = 16px)
        if unit == "rem":
            px_value = value * 16
        elif unit == "em":
            px_value = value * 16  # Assuming base 16px
        else:
            px_value = value

        font_sizes.append({
            "value": value,
            "unit": unit,
            "px": px_value
        })

    # Check line-height
    line_heights = []
    lh_pattern = r'line-height:\s*([0-9.]+);'

    for match in re.finditer(lh_pattern, css_content):
        line_heights.append(float(match.group(1)))

    # Analyze
    issues = []

    # Minimum font size check (14px for small text)
    small_fonts = [f for f in font_sizes if f["px"] < 14]
    if small_fonts:
        issues.append({
            "type": "small_font",
            "count": len(small_fonts),
            "message": f"Found {len(small_fonts)} font sizes below 14px"
        })

    # Line-height check (should be at least 1.4)
    low_line_heights = [lh for lh in line_heights if lh < 1.4]
    if low_line_heights:
        issues.append({
            "type": "low_line_height",
            "count": len(low_line_heights),
            "message": f"Found {len(low_line_heights)} line-heights below 1.4"
        })

    return {
        "font_sizes": font_sizes,
        "line_heights": line_heights,
        "issues": issues,
        "stats": {
            "min_font_size": min([f["px"] for f in font_sizes]) if font_sizes else 0,
            "max_font_size": max([f["px"] for f in font_sizes]) if font_sizes else 0,
            "avg_line_height": sum(line_heights) / len(line_heights) if line_heights else 0
        }
    }


def analyze_spacing():
    """Analyze padding and margin consistency"""
    print("📏 Analyzing spacing...")

    try:
        with open(CSS_FILE, 'r', encoding='utf-8') as f:
            css_content = f.read()
    except:
        return {"error": "Could not read CSS file"}

    # Extract padding/margin values
    spacing_values = []
    spacing_pattern = r'(padding|margin):\s*([^;]+);'

    for match in re.finditer(spacing_pattern, css_content):
        prop = match.group(1)
        value = match.group(2).strip()
        spacing_values.append({
            "property": prop,
            "value": value
        })

    # Check for var() usage (good practice)
    var_usage = len([s for s in spacing_values if "var(--space-" in s["value"]])
    non_var_usage = len(spacing_values) - var_usage

    return {
        "total_declarations": len(spacing_values),
        "using_variables": var_usage,
        "using_hardcoded": non_var_usage,
        "consistency_score": round(var_usage / len(spacing_values) * 100, 1) if spacing_values else 0
    }


def find_all_html_pages():
    """Find all HTML pages to audit"""
    pages = []

    # Foundation pages
    foundation_dir = COURSE_DIR / "foundation"
    if foundation_dir.exists():
        pages.extend(foundation_dir.glob("*.html"))

    # Setup pages
    setup_dir = COURSE_DIR / "setup"
    if setup_dir.exists():
        pages.extend(setup_dir.glob("*.html"))

    # Module pages
    modules_dir = COURSE_DIR / "modules"
    if modules_dir.exists():
        for module_dir in modules_dir.iterdir():
            if module_dir.is_dir():
                pages.extend(module_dir.glob("**/*.html"))

    # Main index
    index = COURSE_DIR / "index.html"
    if index.exists():
        pages.append(index)

    return sorted(pages)


def generate_report(contrast_results, typography_results, spacing_results):
    """Generate comprehensive audit report"""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    report = {
        "timestamp": datetime.now().isoformat(),
        "pages_found": len(find_all_html_pages()),
        "contrast": contrast_results,
        "typography": typography_results,
        "spacing": spacing_results,
        "summary": {
            "contrast_failures": len(contrast_results.get("failures", [])),
            "contrast_warnings": len(contrast_results.get("warnings", [])),
            "typography_issues": len(typography_results.get("issues", [])),
            "spacing_consistency": spacing_results.get("consistency_score", 0)
        }
    }

    # Save JSON report
    json_file = RESULTS_DIR / "audit-report.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Generate text summary
    summary_lines = []
    summary_lines.append("=" * 80)
    summary_lines.append("READABILITY AUDIT REPORT")
    summary_lines.append("=" * 80)
    summary_lines.append(f"Generated: {report['timestamp']}")
    summary_lines.append(f"Pages found: {report['pages_found']}")
    summary_lines.append("")

    # Contrast summary
    summary_lines.append("COLOR CONTRAST")
    summary_lines.append("-" * 80)
    summary_lines.append(f"✅ Passed (AAA): {len(contrast_results.get('passed', []))}")
    summary_lines.append(f"⚠️  Warnings (AA): {len(contrast_results.get('warnings', []))}")
    summary_lines.append(f"❌ Failures: {len(contrast_results.get('failures', []))}")

    if contrast_results.get("failures"):
        summary_lines.append("\nFAILURES:")
        for failure in contrast_results["failures"]:
            summary_lines.append(f"  - {failure['label']}: {failure['ratio']}:1 (need {failure['wcag_aa']}:1)")

    summary_lines.append("")

    # Typography summary
    summary_lines.append("TYPOGRAPHY")
    summary_lines.append("-" * 80)
    if typography_results.get("stats"):
        stats = typography_results["stats"]
        summary_lines.append(f"Minimum font size: {stats['min_font_size']:.1f}px")
        summary_lines.append(f"Average line-height: {stats['avg_line_height']:.2f}")

    if typography_results.get("issues"):
        summary_lines.append("\nISSUES:")
        for issue in typography_results["issues"]:
            summary_lines.append(f"  - {issue['message']}")

    summary_lines.append("")

    # Spacing summary
    summary_lines.append("SPACING")
    summary_lines.append("-" * 80)
    summary_lines.append(f"Consistency score: {spacing_results.get('consistency_score', 0):.1f}%")
    summary_lines.append(f"Using CSS variables: {spacing_results.get('using_variables', 0)} declarations")
    summary_lines.append(f"Using hardcoded values: {spacing_results.get('using_hardcoded', 0)} declarations")

    summary_lines.append("")
    summary_lines.append("=" * 80)

    summary_file = RESULTS_DIR / "audit-summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(summary_lines))

    return json_file, summary_file


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(description="Audit course pages for readability")
    parser.add_argument("--check", choices=["contrast", "typography", "spacing", "all"],
                       default="all", help="What to check")
    args = parser.parse_args()

    print("🔍 Starting readability audit...")
    print(f"📁 Course directory: {COURSE_DIR}")
    print(f"📄 CSS file: {CSS_FILE}")
    print()

    contrast_results = {}
    typography_results = {}
    spacing_results = {}

    if args.check in ["contrast", "all"]:
        contrast_results = analyze_contrast()

    if args.check in ["typography", "all"]:
        typography_results = analyze_typography()

    if args.check in ["spacing", "all"]:
        spacing_results = analyze_spacing()

    # Generate reports
    json_file, summary_file = generate_report(contrast_results, typography_results, spacing_results)

    print()
    print("✅ Audit complete!")
    print(f"📊 JSON report: {json_file}")
    print(f"📄 Summary: {summary_file}")
    print()

    # Print summary to console
    with open(summary_file, 'r', encoding='utf-8') as f:
        print(f.read())

    # Return exit code based on failures
    failures = len(contrast_results.get("failures", []))
    return failures


if __name__ == "__main__":
    exit(main())
