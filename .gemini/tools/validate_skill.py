#!/usr/bin/env python3
"""Tool: Validate Agent Skill markdown files (skill.md / SKILL.md).

Checks:
- Frontmatter exists and parses properly.
- Required keys: name, description, triggers.
- Non-empty instructions body.

Usage:
    python .gemini/tools/validate_skill.py [path_to_skill.md ...]
    python .gemini/tools/validate_skill.py --scan
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from mini_coding_agent import Skill  # noqa: E402


def validate_skill_file(path: Path) -> bool:
    print(f"Validating skill at: {path.relative_to(REPO_ROOT)}")
    if not path.is_file():
        print(f"  [FAIL] File does not exist: {path}")
        return False

    raw = path.read_text(encoding="utf-8", errors="replace")
    if not raw.startswith("---"):
        print("  [FAIL] Missing YAML frontmatter ('---')")
        return False

    meta, instructions = Skill.parse_content(raw)
    name = meta.get("name") or path.parent.name
    desc = meta.get("description", "")
    triggers = meta.get("triggers", [])

    errors = []
    if not name:
        errors.append("Skill 'name' is empty or missing")
    if not desc:
        errors.append("Skill 'description' is empty or missing")
    if not triggers:
        errors.append("Skill 'triggers' list is empty or missing")
    if not instructions.strip():
        errors.append("Skill instruction body is empty")

    if errors:
        for err in errors:
            print(f"  [FAIL] {err}")
        return False

    print(f"  [PASS] Name: '{name}' | Triggers: {len(triggers)} | Instructions: {len(instructions.strip())} chars")
    return True


def scan_and_validate():
    all_valid = True
    found_any = False
    for search_dir in ("skill", "skills", ".gemini/skills"):
        dir_path = REPO_ROOT / search_dir
        if not dir_path.is_dir():
            continue
        for item in sorted(dir_path.rglob("*.md")):
            if item.name.lower() in ("skill.md",):
                found_any = True
                if not validate_skill_file(item):
                    all_valid = False

    if not found_any:
        print("No skill files found to validate.")
        return False
    return all_valid


def main():
    if len(sys.argv) > 1 and sys.argv[1] != "--scan":
        paths = [Path(p).resolve() for p in sys.argv[1:]]
        success = all(validate_skill_file(p) for p in paths)
    else:
        success = scan_and_validate()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
