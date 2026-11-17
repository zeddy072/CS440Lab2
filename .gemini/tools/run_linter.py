#!/usr/bin/env python3
"""Tool: Run ruff linter and formatter for the Mini Coding Agent.

Usage:
    python .gemini/tools/run_linter.py [options]
    python .gemini/tools/run_linter.py --fix
    python .gemini/tools/run_linter.py format
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def main():
    ruff_bin = REPO_ROOT / "cs440_project2" / "bin" / "ruff"
    if not ruff_bin.exists():
        print(f"Error: ruff binary not found at {ruff_bin}", file=sys.stderr)
        print("Please ensure cs440_project2 venv is set up.", file=sys.stderr)
        sys.exit(1)

    args = sys.argv[1:]
    if not args:
        cmd = [str(ruff_bin), "check", "."]
    elif args[0] in ("format", "check"):
        cmd = [str(ruff_bin)] + args
    else:
        cmd = [str(ruff_bin), "check", "."] + args

    print(f"Running ruff with command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=REPO_ROOT)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
