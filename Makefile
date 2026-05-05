.PHONY: test test-cov test-module test-tools test-skills test-kb test-structure test-html-report test-quality test-skill-invocability test-smoke test-qa-all clean-test cli-mode-check cli-mode-migrate cli-mode-migrate-dry drift-check drift-check-strict

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

# ──────────────────────────────────────────────────────────────────────────
# CLI mode (claude -p / cursor-agent --print) compatibility
# ──────────────────────────────────────────────────────────────────────────

# Static analysis of slash commands for non-interactive mode compatibility.
# Defaults to scanning this repo's commands. Add a sibling aiagent-course
# checkout to also scan its commands (set AIAGENT_COURSE_ROOT).
AIAGENT_COURSE_ROOT ?= ../aiagent-course

cli-mode-check:
	@mkdir -p reports
	@if [ -d "$(AIAGENT_COURSE_ROOT)/.claude/commands" ]; then \
		python3 tools/cli_mode_check/check.py \
			--root .claude/commands \
			--root "$(AIAGENT_COURSE_ROOT)/.claude/commands" \
			--csv reports/cli-mode.csv \
			--md reports/cli-mode.md \
			--locale ja; \
	else \
		python3 tools/cli_mode_check/check.py \
			--root .claude/commands \
			--csv reports/cli-mode.csv \
			--md reports/cli-mode.md \
			--locale ja; \
	fi
	@echo "Reports: reports/cli-mode.csv, reports/cli-mode.md"

# Strict variant for CI: fails (exit 2) if any file scores below 70.
cli-mode-check-strict:
	@$(MAKE) cli-mode-check >/dev/null
	@python3 tools/cli_mode_check/check.py \
		--root .claude/commands \
		--csv reports/cli-mode.csv \
		--md reports/cli-mode.md \
		--locale ja \
		--strict 70

cli-mode-migrate-dry:
	python3 tools/cli_mode_check/migrate.py --root .claude/commands --dry-run

cli-mode-migrate:
	python3 tools/cli_mode_check/migrate.py --root .claude/commands

# ──────────────────────────────────────────────────────────────────────────
# Lesson command ↔ slide drift detection
# ──────────────────────────────────────────────────────────────────────────

drift-check:
	@mkdir -p reports
	@if [ -d "$(AIAGENT_COURSE_ROOT)" ]; then \
		python3 tools/lesson_drift_check/check.py \
			--commands .claude/commands \
			--course "$(AIAGENT_COURSE_ROOT)" \
			--csv reports/lesson-drift.csv \
			--md reports/lesson-drift.md; \
	else \
		echo "ERROR: AIAGENT_COURSE_ROOT=$(AIAGENT_COURSE_ROOT) not found." >&2; \
		echo "       Either clone aiagent-course as a sibling, or set AIAGENT_COURSE_ROOT=/path/to/aiagent-course." >&2; \
		exit 1; \
	fi
	@echo "Reports: reports/lesson-drift.csv, reports/lesson-drift.md"

drift-check-strict:
	@$(MAKE) drift-check >/dev/null
	@python3 tools/lesson_drift_check/check.py \
		--commands .claude/commands \
		--course "$(AIAGENT_COURSE_ROOT)" \
		--csv reports/lesson-drift.csv \
		--md reports/lesson-drift.md \
		--max-drift 5
