import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from mini_coding_agent import (
    FakeModelClient,
    MiniAgent,
    SessionStore,
    SimilarityMatcher,
    SkillRegistry,
    WorkspaceContext,
)


def create_pr_review_skill(workspace_dir: Path):
    skill_dir = workspace_dir / "skill" / "pr-review"
    skill_dir.mkdir(parents=True, exist_ok=True)
    content = """---
name: pr-review
description: Review pull requests, git diffs, and staged changes against code standards
triggers:
  - review pull request
  - check pr
  - review diff
  - inspect git diff
tags:
  - review
  - git
---

# Pull Request Review Skill

## Instructions
1. Inspect git status and modified files.
2. Provide a structured review of bugs and quality.
"""
    (skill_dir / "skill.md").write_text(content, encoding="utf-8")


def create_code_refactor_skill(workspace_dir: Path):
    skill_dir = workspace_dir / "skills" / "code-refactor"
    skill_dir.mkdir(parents=True, exist_ok=True)
    content = """---
name: code-refactor
description: Refactor Python functions for readability and standards
triggers:
  - refactor code
  - clean up function
tags:
  - refactor
  - python
---

# Code Refactor Skill

## Instructions
1. Inspect code and refactor cleanly.
"""
    (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")


def build_test_agent(tmp_path, outputs, **kwargs):
    (tmp_path / "README.md").write_text("test workspace\n", encoding="utf-8")
    workspace = WorkspaceContext.build(tmp_path)
    store = SessionStore(tmp_path / ".mini-coding-agent" / "sessions")
    approval_policy = kwargs.pop("approval_policy", "auto")
    return MiniAgent(
        model_client=FakeModelClient(outputs),
        workspace=workspace,
        session_store=store,
        approval_policy=approval_policy,
        **kwargs,
    )


class TestAgentSkills(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_r1_skill_discovery(self):
        print("\n" + "=" * 65)
        print("TEST [R1]: Folder-Based Skill Discovery")
        print("  Scanning directories: skill/pr-review/skill.md and skills/code-refactor/SKILL.md")
        create_pr_review_skill(self.root)
        create_code_refactor_skill(self.root)
        registry = SkillRegistry(self.root)
        skills = registry.discover()

        self.assertIn("pr-review", skills)
        skill = skills["pr-review"]
        self.assertEqual(skill.name, "pr-review")
        self.assertIn("Review pull requests", skill.description)
        self.assertIn("review pull request", skill.triggers)
        self.assertIn("Inspect git status", skill.instructions)

        self.assertIn("code-refactor", skills)
        skill2 = skills["code-refactor"]
        self.assertEqual(skill2.name, "code-refactor")
        self.assertIn("Refactor Python functions", skill2.description)
        self.assertIn("refactor code", skill2.triggers)

        print(f"  -> Discovered skills: {[s.name for s in skills.values()]}")
        print("  [PASS] R1: Successfully discovered and parsed both skill/ and skills/ format skills.")

    def test_r2_similarity_matching_trigger_and_fallback(self):
        print("\n" + "=" * 65)
        print("TEST [R2]: Prompt Similarity Matching & Threshold Trigger")
        print("  Configured similarity threshold: 0.35")
        create_pr_review_skill(self.root)
        registry = SkillRegistry(self.root)
        matcher = SimilarityMatcher(threshold=0.35)

        # Test case 1: Matching prompt
        prompt_match = "Please review this pull request and inspect git diff"
        print(f"  Prompt A (relevant):   '{prompt_match}'")
        result_match = matcher.evaluate(prompt_match, registry.skills)
        print(f"     Score: {result_match['top_score']:.2f} (Threshold: 0.35) -> Matched: {result_match['matched']} (Top skill: {result_match['top_skill']})")
        self.assertTrue(result_match["matched"])
        self.assertEqual(result_match["top_skill"], "pr-review")
        self.assertGreaterEqual(result_match["top_score"], 0.35)

        # Test case 2: Unrelated prompt
        prompt_unrelated = "Calculate the fibonacci sequence of 10"
        print(f"  Prompt B (unrelated):  '{prompt_unrelated}'")
        result_unrelated = matcher.evaluate(prompt_unrelated, registry.skills)
        print(f"     Score: {result_unrelated['top_score']:.2f} (Threshold: 0.35) -> Matched: {result_unrelated['matched']} (No trigger)")
        self.assertFalse(result_unrelated["matched"])
        self.assertLess(result_unrelated["top_score"], 0.35)

        print("  [PASS] R2: High-similarity prompt triggered skill; unrelated prompt correctly skipped.")

    def test_r3_and_r4_tool_use_skill_in_execution(self):
        print("\n" + "=" * 65)
        print("TEST [R3 & R4]: Runtime In-Execution Skill Triggering via use_skill tool")
        create_pr_review_skill(self.root)
        agent = build_test_agent(
            self.root,
            [
                '<tool>{"name":"use_skill","args":{"name":"pr-review"}}</tool>',
                "<final>Review completed following skill instructions.</final>",
            ],
        )

        user_msg = "I need a specialized review."
        print(f"  User input: '{user_msg}'")
        print("  Model step 1: emits <tool>{\"name\":\"use_skill\",\"args\":{\"name\":\"pr-review\"}}</tool>")
        answer = agent.ask(user_msg)
        print(f"  Model final answer: '{answer}'")
        print(f"  Active skill on agent: '{agent.active_skill.name if agent.active_skill else None}'")

        self.assertEqual(answer, "Review completed following skill instructions.")
        self.assertIsNotNone(agent.active_skill)
        self.assertEqual(agent.active_skill.name, "pr-review")

        # Verify tool invocation is recorded
        tool_events = [item for item in agent.session["history"] if item.get("role") == "tool"]
        self.assertTrue(any(item.get("name") == "use_skill" for item in tool_events))
        print("  [PASS] R3 & R4: In-turn use_skill call loaded and activated skill instructions.")

    def test_r4_prompt_injection_when_triggered(self):
        print("\n" + "=" * 65)
        print("TEST [R4]: Active Skill Instruction Injection into Agent Prompt Context")
        create_pr_review_skill(self.root)
        agent = build_test_agent(
            self.root,
            ["<final>Done reviewing PR.</final>"],
        )

        trigger_prompt = "Please review this pull request and check git diff"
        print(f"  Prompt: '{trigger_prompt}'")
        answer = agent.ask(trigger_prompt)
        self.assertEqual(answer, "Done reviewing PR.")
        self.assertIsNotNone(agent.active_skill)
        self.assertEqual(agent.active_skill.name, "pr-review")

        # Verify active skill instructions were injected into the generated prompt
        prompt_text = agent.prompt("Followup request")
        print("  Inspecting generated prompt for injected skill context:")
        self.assertIn("Active Skill Instructions [pr-review]", prompt_text)
        self.assertIn("Inspect git status and modified files.", prompt_text)
        print("     Found block: '--- Active Skill Instructions [pr-review] ---'")
        print("     Found instructions: '1. Inspect git status and modified files...'")
        print("  [PASS] R4: Skill instructions correctly injected into agent turn context.")

    def test_r5_mandatory_logging_history_and_file(self):
        print("\n" + "=" * 65)
        print("TEST [R5]: Mandatory Structured Audit Logging (History & File)")
        create_pr_review_skill(self.root)
        agent = build_test_agent(
            self.root,
            ["<final>Done.</final>"],
        )

        user_prompt = "Please review this pull request"
        print(f"  User prompt: '{user_prompt}'")
        agent.ask(user_prompt)

        # 1. Verify session history contains skill_audit event
        audit_events = [item for item in agent.session["history"] if item.get("role") == "skill_audit"]
        self.assertGreaterEqual(len(audit_events), 1)
        audit = audit_events[0]["content"]

        print("  1. Session history audit event:")
        print(f"     Prompt:           '{audit['prompt']}'")
        print(f"     Matched:          {audit['similarity_check']['matched']}")
        print(f"     Top score:        {audit['similarity_check']['top_score']}")
        print(f"     Executed skill:   '{audit['executed_skill']['name']}' (mode: {audit['executed_skill']['trigger_mode']})")

        self.assertEqual(audit["prompt"], user_prompt)
        self.assertIn("similarity_check", audit)
        self.assertTrue(audit["similarity_check"]["matched"])
        self.assertEqual(audit["similarity_check"]["top_skill"], "pr-review")
        self.assertIsNotNone(audit["executed_skill"])
        self.assertEqual(audit["executed_skill"]["name"], "pr-review")

        # 2. Verify skills.log file exists and contains JSONL record
        log_file = self.root / ".mini-coding-agent" / "skills.log"
        self.assertTrue(log_file.exists())
        lines = [json.loads(line) for line in log_file.read_text(encoding="utf-8").strip().splitlines() if line]
        self.assertGreaterEqual(len(lines), 1)
        self.assertEqual(lines[0]["prompt"], user_prompt)
        self.assertEqual(lines[0]["executed_skill"]["name"], "pr-review")

        print("  2. Persistent log file (.mini-coding-agent/skills.log):")
        print(f"     Line count: {len(lines)}")
        print(f"     Sample line: {json.dumps(lines[0])[:80]}...")
        print("  [PASS] R5: Verified prompt, similarity check matrix, and executed skill logged to both targets.")

    def test_r6_zero_regression_when_no_skills_present(self):
        print("\n" + "=" * 65)
        print("TEST [R6]: Zero Regression When No Skills Are Present")
        # Empty workspace without skill/ folder
        agent = build_test_agent(
            self.root,
            [
                '<tool>{"name":"list_files","args":{"path":"."}}</tool>',
                "<final>Finished listing.</final>",
            ],
        )

        user_prompt = "List all workspace files"
        print(f"  Workspace has 0 skills. Prompt: '{user_prompt}'")
        answer = agent.ask(user_prompt)
        print(f"  Agent tool execution succeeded. Final answer: '{answer}'")
        print(f"  Active skill remains: {agent.active_skill}")

        self.assertEqual(answer, "Finished listing.")
        self.assertIsNone(agent.active_skill)

        # Audit should record no executed skill
        audit_events = [item for item in agent.session["history"] if item.get("role") == "skill_audit"]
        self.assertGreaterEqual(len(audit_events), 1)
        self.assertIsNone(audit_events[0]["content"]["executed_skill"])
        print("  Audit entry logged: executed_skill=None (clean fallback)")
        print("  [PASS] R6: Zero-regression confirmed: agent functions identically with no skills.")
        print("=" * 65)


if __name__ == "__main__":
    unittest.main()
