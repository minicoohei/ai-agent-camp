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
