# CS 440 — Vacuum Robot Q-Learning Task

## Assignment basis
Solve the earlier vacuum-robot lab using reinforcement learning. The environment is a 4-by-4 grid. Transition and reward tables (T and R) are not provided; define and document a simple, consistent transition/reward model for this experiment. The original earlier lab said Q-learning would be implemented later; this follow-up asks to solve that lab, so implement tabular Q-learning.

## Grid

| Start | 0 | 0 | 0 |
|---|---|---|---|
| 0 | X | 0 | 0 |
| 0 | 0 | 0 | 0 |
| 0 | -1 | 0 | 10 |

Coordinates are (row, column), zero-indexed. Start at (0,0); obstacle X at (1,1); terminal penalty -1 at (3,1); terminal goal +10 at (3,3). Other cells are traversable. Treat movement into walls or outside the grid as staying in place. Use four actions: up, down, left, right. These are explicit modeling assumptions for the experiment, not details stated in the assignment.

## Hyperparameters
- Living reward: -0.01 per nonterminal step
- Discount factor gamma: 0.90
- Learning rate alpha: 0.10
- Initial epsilon: 1.00
- Epsilon decay: 0.99 per episode; minimum epsilon: 0.05 (additional choice)
- Seed: 42 for reproducibility

## Implementation
1. Create `vacuum_q_learning.py` with the environment, Q-table, epsilon-greedy action selection, and Bellman Q-learning update.
2. Train for a configurable number of episodes with a maximum step limit to prevent endless loops.
3. Report the learned greedy path from the start, whether it reaches the +10 goal, and basic training/evaluation statistics. Evaluate without exploration or Q-table updates.
4. Create `test_vacuum_q_learning.py` using pytest. Cover the obstacle, boundaries, terminal rewards, Q update, and a deterministic seeded run.
5. Create `LAB5_RESULTS.md` recording commands, test outcomes, observed behavior, actual skill/delegation usage, and limitations.

## Done when
The implementation is runnable, tests have been attempted, results are documented honestly, and the original mini coding agent and Gemini configuration remain unchanged. If unable to complete all steps, deliver partial work and clearly explain what failed.
