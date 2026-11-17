# Intent: Create a new agent skills component (Component 7)
Author: Jack McClellan
Status: draft

## Problem
The mini coding agent lacks the agent skills component (Component 7) to discover, match, and execute domain-specific workflows.

## Proposed Outcome
Our goal is to create this new component. The mini code agent must:
1. Identify folder-based skills located in `skill/<name>/` or `skills/<name>/` containing a `skill.md` (or `SKILL.md`) file (e.g., `skill/pr-review/skill.md`).
2. Automatically trigger a skill by evaluating prompt similarity against skill metadata when an appropriate prompt is entered.
3. Allow the agent to dynamically trigger a skill during execution when it determines a specific skill is needed (via a `use_skill` tool).
4. Execute the skill instructions by injecting them into the agent's turn reasoning context.
5. Provide a reference skill fixture (`skill/pr-review/skill.md`) for verification.

## Constraints & Guardrails
* **In Scope:**
  * The component must log the prompt, the similarity check (candidate scores, threshold, outcome), and the executed skill to both session history and `.mini-coding-agent/skills.log`.
  * Follow an SDLC for code agents by maintaining project stage files (`intent.md`, `spec.md`, `plan.md`).
  * Standard library only (no external NLP or vector database dependencies).
* **Out of Scope**
  * Do not alter any original agent functionality; all existing tools, flags, and default execution behavior must remain intact.
  * If no skill matches or no skills exist, agent behavior proceeds unaltered.
