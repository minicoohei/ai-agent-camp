.PHONY: test test-cov test-module test-tools test-skills test-kb test-structure test-html-report test-quality test-skill-invocability test-smoke test-qa-all clean-test

# Use uv run pytest (ensures .venv dependencies are available)
PYTEST := uv run pytest

# Run all tests
test:
	$(PYTEST) tests/ -v

# Run tests with coverage report (terminal)
test-cov:
	$(PYTEST) tests/ -v --cov=tools --cov-report=term-missing

# Run tests for a specific module (e.g., make test-module MOD=tools)
test-module:
	$(PYTEST) tests/$(MOD)/ -v --cov --cov-report=term-missing

# Shortcut: tools tests only
test-tools:
	$(PYTEST) tests/tools/ -v --cov=tools --cov-report=term-missing

# Shortcut: skills tests only
test-skills:
	$(PYTEST) tests/skills/ -v --cov-report=term-missing

# Shortcut: knowledge-base tests only
test-kb:
	$(PYTEST) tests/knowledge_base/ -v --cov-report=term-missing

# Shortcut: structure tests only
test-structure:
	$(PYTEST) tests/test_structure.py tests/test_sample_data.py -v

# Generate HTML coverage report
test-html-report:
	$(PYTEST) tests/ -v --cov=tools --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

# Generate XML coverage report (for CI)
test-xml-report:
	$(PYTEST) tests/ -v --cov=tools --cov-report=xml

# Lesson content quality tests
test-quality:
	$(PYTEST) tests/e2e/test_lesson_quality_e2e.py -v

# Skill invocability tests
test-skill-invocability:
	$(PYTEST) tests/skills/test_skill_invocability.py -v

# Smoke invocation tests (slow, requires claude CLI + API key)
test-smoke:
	$(PYTEST) tests/e2e/test_smoke_invocation.py -v -m "slow" --timeout=600

# All QA tests (quality + skill invocability, excluding smoke)
test-qa-all:
	$(PYTEST) tests/skills/test_skill_invocability.py tests/e2e/test_lesson_quality_e2e.py -v

# Clean test artifacts
clean-test:
	rm -rf .pytest_cache htmlcov .coverage coverage.xml
	find . -type d -name __pycache__ -not -path './.venv/*' -exec rm -rf {} + 2>/dev/null || true

# === i18n targets ===
.PHONY: i18n-check i18n-check-html i18n-check-md i18n-check-cli i18n-extract i18n-build i18n-test

# Target languages (override: make i18n-check LANGS="en es")
LANGS ?= en

# Unified QA (all domains)
i18n-check:
	uv run python tools/i18n_qa.py --lang $(LANGS)

# Domain-specific checks
i18n-check-html:
	uv run python tools/i18n_check.py --lang $(LANGS)
	uv run python tools/check_i18n_coverage.py

i18n-check-md:
	uv run python tools/i18n_check_md.py --lang $(LANGS)

i18n-check-cli:
	uv run python tools/i18n_extract_cli.py --check
	uv run python tools/i18n_extract_cli.py --scan

# Extract all (HTML + MD + CLI)
i18n-extract:
	uv run python tools/i18n_extract.py
	uv run python tools/i18n_extract_md.py
	uv run python tools/i18n_extract_cli.py

# Build all translated output
i18n-build:
	uv run python tools/i18n_build.py --lang $(LANGS)
	uv run python tools/i18n_build_md.py --lang $(LANGS)

# Run i18n-specific pytest suite
i18n-test:
	$(PYTEST) tests/tools/test_i18n_*.py -v
