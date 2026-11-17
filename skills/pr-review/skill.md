---
name: pr-review
description: Review pull requests, git diffs, and staged changes against code standards and best practices
triggers:
  - review pull request
  - check pr
  - review diff
  - inspect git diff
  - review code changes
tags:
  - review
  - git
  - pr
---

# Pull Request Review Skill

## Instructions
1. Inspect git status and recent changes using tools such as `run_shell` or `list_files`.
2. Read the modified files using `read_file`.
3. Provide a structured review covering:
   - Summary of changes
   - Potential bugs, security risks, or regressions
   - Architecture & code quality
   - Recommended tests or improvements
