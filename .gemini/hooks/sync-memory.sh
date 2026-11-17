#!/usr/bin/env bash
# Hook: Sync Memory and Task Stages
# Verifies that tasks in .gemini/tasks have intent.md, spec.md, and plan.md, and are indexed in memory.md.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TASKS_DIR="$REPO_ROOT/.gemini/tasks"
MEMORY_FILE="$REPO_ROOT/.gemini/memory/memory.md"

echo "Checking task stage files and memory sync..."

if [ ! -d "$TASKS_DIR" ]; then
    echo "Warning: No tasks directory found at $TASKS_DIR"
    exit 0
fi

for task_dir in "$TASKS_DIR"/T-*; do
    if [ -d "$task_dir" ]; then
        task_id="$(basename "$task_dir")"
        echo "Validating stage files for $task_id:"
        for stage in intent.md spec.md plan.md; do
            if [ -f "$task_dir/$stage" ]; then
                echo "  [OK] $stage exists"
            else
                echo "  [MISSING] $task_dir/$stage does not exist!"
            fi
        done

        if grep -q "$task_id" "$MEMORY_FILE"; then
            echo "  [OK] Indexed in memory.md"
        else
            echo "  [WARNING] $task_id not mentioned in memory.md"
        fi
    fi
done

echo "Memory check complete."
