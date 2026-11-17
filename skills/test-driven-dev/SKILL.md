---
name: test-driven-dev
description: Write robust Pytest unit tests, design test fixtures, inspect edge cases, and run test verification
triggers:
  - write unit tests
  - create pytest tests
  - test coverage
  - tdd workflow
  - write test suite
tags:
  - testing
  - pytest
  - tdd
  - quality
---

# Test-Driven Development (TDD) Skill

## Purpose
Guide the Mini Coding Agent through writing comprehensive unit tests using Pytest, inspecting existing implementations before authoring test cases, and verifying all tests pass.

## Instructions
1. **Inspect Implementation**:
   - Use `read_file` to read the target source code.
   - Note function signatures, expected input types, return values, and exceptions raised.
2. **Draft Test Cases**:
   - Use `write_file` or `patch_file` to create/update tests under `tests/test_<module>.py`.
   - Use descriptive test function names prefixed with `test_` (e.g., `test_q_table_update_positive_reward`).
   - Group related scenarios using `@pytest.mark.parametrize` for multiple input/output pairs.
   - Include edge cases: empty data structures, zero values, boundary conditions, and invalid inputs.
3. **Execute & Verify**:
   - Run the test suite using `run_shell` with `pytest` (e.g., `uv run pytest tests/` or python test runner).
   - If tests fail, inspect the failure output, correct either the implementation or test expectations, and re-run.
   - Never mark a task complete without running and passing the applicable test suite.
