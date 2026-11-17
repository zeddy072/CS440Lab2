---
name: rl-env-diagnostics
description: Diagnose RL training dynamics, track cumulative rewards, detect exploration collapse, and verify policy convergence
triggers:
  - evaluate rl agent
  - diagnose q-learning convergence
  - track reward curves
  - rl evaluation
  - check policy convergence
tags:
  - rl
  - metrics
  - convergence
  - diagnostics
  - evaluation
---

# RL Environment Diagnostics & Evaluation Skill

## Purpose
Guide the Mini Coding Agent in tracking training metrics, validating convergence, and debugging common failure modes in reinforcement learning environments.

## Diagnostics Protocol
1. **Episodic Metrics Tracking**:
   - Record per-episode cumulative return: $G_e = \sum_{t=0}^T r_t$.
   - Record episode lengths (number of steps to termination).
   - Track average Bellman TD error per episode to evaluate value function convergence.
   - Compute moving window averages (e.g. rolling 50-episode or 100-episode mean return).
2. **Common RL Failure Detection**:
   - **Exploration Collapse**: Check if $\epsilon$ decays too rapidly before key states/rewards are discovered.
   - **Cyclic Trajectories / Infinite Loops**: Check if agent steps hit max-step cutoff without reaching terminal state.
   - **Q-Value Oscillation or Divergence**: Monitor $\max_{s,a} |Q(s, a)|$ to ensure bounded values.
   - **Sparse Reward Blindspot**: Verify state-action visit counts $N(s, a) > 0$ for high-value regions.
3. **Verification Summary**:
   - Output structured evaluation statistics (mean return $\pm$ std, success rate over $N$ evaluation episodes).
   - Provide ASCII reward curves or milestone logs when visual plotting is unavailable.
