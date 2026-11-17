# Spec: Agent Skills Component
Constraints carried in: stdlib only; do not alter original agent functionality; maintain SDLC stage files (intent.md -> spec.md -> plan.md)

## Requirements <!-- numbered, so tests can cite them -->
- R1. Folder-based skill discovery identifies skills in `skill/<name>/skill.md` or `skills/<name>/SKILL.md` (e.g., `skill/pr-review/skill.md`).
- R2. A similarity check evaluates the prompt against registered skills and triggers the skill when similarity meets or exceeds the threshold.
- R3. The agent can dynamically trigger a skill during execution via a structured tool (`use_skill`) when a specific skill is needed.
- R4. Triggering a skill executes the instructions in `skill.md` by injecting them into the agent's reasoning context.
- R5. The component logs the prompt, the similarity check (scores, threshold, outcome), and the executed skill to both session history and `.mini-coding-agent/skills.log`.
- R6. Original agent functionality remains unaltered when no skill matches or no skills exist.

## Design
- `SkillRegistry` scans `skill/` and `skills/` under the workspace root, parsing metadata (`name`, `description`, `triggers`) and instruction text.
- `SimilarityMatcher` uses stdlib tokenization and term-frequency cosine similarity to score prompts against candidate skills against a default threshold (0.35).
- `MiniAgent.ask()` runs the similarity check before tool steps; if matched, it sets the active skill and logs the evaluation.
- `build_tools()` adds a `use_skill` tool allowing the model to load and execute skill instructions mid-turn.
- Active skill instructions are injected into the dynamic prompt context ahead of the user request.
- `SkillLogger` records the prompt, similarity check details, and executed skill into `session["history"]` and appends to `.mini-coding-agent/skills.log`.

## Areas of concern <!-- each one has an owner -->
1. False-positive or low-confidence skill triggers on short, ambiguous prompts. Owner: ML/Prompt Engineer
2. Exceeding token budget when large `skill.md` instruction files are injected into prompt context. Owner: Agent Runtime Maintainer
3. Maintaining stdlib-only compatibility without heavy external NLP or embedding libraries. Owner: Core Maintainer
4. Handling Windows vs. POSIX path separators in folder paths (e.g., `\skill\pr-review` vs `skill/pr-review`). Owner: Cross-Platform / CI Team
