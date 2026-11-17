#!/usr/bin/env python3
"""Tool: Run pytest test suite for the Mini Coding Agent.

Usage:
    python .gemini/tools/run_tests.py [pytest options...]
"""

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def main():
    pytest_bin = REPO_ROOT / "cs440_project2" / "bin" / "pytest"
    if pytest_bin.exists():
        cmd = [str(pytest_bin)] + sys.argv[1:]
    else:
        # Fallback to python unittest runner if venv pytest is not available
        cmd = [sys.executable, "-m", "unittest", "discover", "tests"] + sys.argv[1:]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT)

    print(f"Running tests with command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=REPO_ROOT, env=env)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
