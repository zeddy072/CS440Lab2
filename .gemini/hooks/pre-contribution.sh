#!/usr/bin/env bash
# Hook: Pre-Contribution Quality Check
# Enforces that all tests pass with pytest and coding standards are checked with ruff.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

echo "=========================================="
echo "Running Pre-Contribution Quality Checks..."
echo "=========================================="

# 1. Run tests
echo "[1/3] Running tests with pytest..."
"$REPO_ROOT/cs440_project2/bin/python" "$REPO_ROOT/.gemini/tools/run_tests.py" -q

# 2. Run skill validation
echo "[2/3] Validating all skill files..."
"$REPO_ROOT/cs440_project2/bin/python" "$REPO_ROOT/.gemini/tools/validate_skill.py" --scan

# 3. Run ruff lint check
echo "[3/3] Checking coding guidelines with ruff..."
"$REPO_ROOT/cs440_project2/bin/ruff" check "$REPO_ROOT/mini_coding_agent.py" "$REPO_ROOT/tests/" "$REPO_ROOT/.gemini/tools/"

echo "=========================================="
echo "All pre-contribution checks passed!"
echo "=========================================="
