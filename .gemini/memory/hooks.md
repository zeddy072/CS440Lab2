# Gemini Agent Hook Index

The following hooks are maintained under `.gemini/hooks/`:

## 1. `pre-contribution.sh`
- **Path**: `.gemini/hooks/pre-contribution.sh`
- **Purpose**: Pre-contribution verification gate. Automatically executes:
  1. Full Pytest test suite via `run_tests.py`
  2. Skill schema validation across all workspace skills via `validate_skill.py`
  3. Coding standards check via `ruff`
- **Usage**:
  ```bash
  ./.gemini/hooks/pre-contribution.sh
  ```

## 2. `sync-memory.sh`
- **Path**: `.gemini/hooks/sync-memory.sh`
- **Purpose**: Verifies that every task directory in `.gemini/tasks/` has valid `intent.md`, `spec.md`, and `plan.md` files, and is properly referenced in `.gemini/memory/memory.md`.
- **Usage**:
  ```bash
  ./.gemini/hooks/sync-memory.sh
  ```
