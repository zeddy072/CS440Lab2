# Plan: Agent Skills Component

## Files that change
mini_coding_agent.py <!-- SkillRegistry, SimilarityMatcher, SkillLogger, tool_use_skill(), ask() -->
skill/pr-review/skill.md <!-- new: reference skill fixture -->
tests/test_skills.py <!-- new -->

## Order of work <!-- each step cites requirements -->
1. Create reference skill `skill/pr-review/skill.md` and failing test cases in `tests/test_skills.py` (R1–R6)
2. Implement `SkillRegistry` to discover and parse `skill/<name>/skill.md` and `skills/<name>/SKILL.md` (R1)
3. Implement `SimilarityMatcher` using stdlib term-frequency cosine similarity and threshold check (R2)
4. Add `use_skill` tool to `build_tools()` for in-execution skill triggering (R3)
5. Inject active skill instructions into turn prompt context during reasoning (R4)
6. Implement `SkillLogger` to record prompt, similarity check matrix, and executed skill to `session["history"]` and `.mini-coding-agent/skills.log` (R5)
7. Ensure zero-regression fallback: standard execution proceeds untouched when no skill matches or exists (R6)

## Risks
False-positive matches on brief prompts, token inflation from large skill instructions, and keeping similarity math stdlib-only

## Proof <!-- the tests that prove it is done -->
tests/test_skills.py:
- tests discovery of `skill/pr-review/skill.md` (R1)
- tests prompt triggering when similarity $\ge$ 0.35 (R2, R4)
- tests runtime `use_skill` tool execution (R3, R4)
- tests audit logs contain prompt, similarity scores, and executed skill (R5)
- tests existing agent behavior and test suite run without regressions (R6)
