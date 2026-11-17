---
name: sdlc-task-runner
description: Standard operating procedure for AI-native SDLC task execution in CS440Lab2
triggers:
  - run sdlc task
  - implement task
  - sdlc workflow
tags:
  - sdlc
  - process
  - engineering
---

# SDLC Task Runner Skill

## Workflow Protocol
1. **Context & Verification**:
   - Read `README.md` and `GEMINI.md`.
   - Read `.gemini/tasks/T-###/intent.md`, `spec.md`, and `plan.md`.
   - Validate that requirements (R1..Rn) have clear definition of done.
2. **Interactive Confirmation**:
   - Suggest planned implementation to the user and obtain confirmation before editing code.
3. **Test-Driven Development**:
   - Write failing Pytest tests first in `tests/test_*.py`.
   - Implement minimal working code to satisfy tests.
4. **Quality Gates**:
   - Run test suite using `.gemini/tools/run_tests.py`.
   - Check coding standards with `.gemini/tools/run_linter.py`.
   - Validate skills with `.gemini/tools/validate_skill.py`.
5. **Memory and Record Keeping**:
   - Update `.gemini/memory/memory.md` with decisions, questions, and completed tasks.
   - Run `.gemini/hooks/sync-memory.sh` to ensure consistency.
