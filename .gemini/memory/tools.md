# Gemini Agent Tools Index

The following custom tools are maintained under `.gemini/tools/`:

## 1. `run_tests.py`
- **Path**: `.gemini/tools/run_tests.py`
- **Purpose**: Runs the test suite using `pytest` inside the `cs440_project2` virtual environment with `PYTHONPATH` set to the repository root. Supports passing custom pytest options (e.g. `-k`, `-v`, `-q`).
- **Usage**:
  ```bash
  python .gemini/tools/run_tests.py [pytest options...]
  ```

## 2. `run_linter.py`
- **Path**: `.gemini/tools/run_linter.py`
- **Purpose**: Wraps `ruff` inside `cs440_project2` for code linting and formatting.
- **Usage**:
  ```bash
  python .gemini/tools/run_linter.py [options]
  python .gemini/tools/run_linter.py --fix
  ```

## 3. `validate_skill.py`
- **Path**: `.gemini/tools/validate_skill.py`
- **Purpose**: Verifies that skill markdown files (`skill.md` or `SKILL.md`) have valid YAML frontmatter, non-empty `name`, `description`, and `triggers`, and valid instruction bodies.
- **Usage**:
  ```bash
  python .gemini/tools/validate_skill.py --scan
  python .gemini/tools/validate_skill.py <path_to_skill.md>
  ```
