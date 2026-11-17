---
name: q-learning-agent
description: Implement tabular Q-learning algorithms, epsilon-greedy exploration, Bellman updates, and policy extraction
triggers:
  - implement q-learning
  - tabular q-learning
  - q-table update
  - bellman equation
  - epsilon-greedy policy
  - train q-learning
tags:
  - reinforcement-learning
  - q-learning
  - rl
  - bellman
  - agent
---

# Tabular Q-Learning Agent Skill

## Purpose
Guide the Mini Coding Agent in designing, implementing, and training tabular Q-learning agents for discrete Markov Decision Processes (MDPs).

## Core Algorithm Components
1. **Q-Table Representation**:
   - Represent state-action values $Q(s, a)$ using `collections.defaultdict(lambda: [0.0] * num_actions)` or a 2D NumPy array `(num_states, num_actions)`.
   - Ensure state representations are hashable (tuples or integers).
2. **Exploration Strategy ($\epsilon$-greedy)**:
   - With probability $\epsilon$, choose an action uniformly at random from available actions.
   - With probability $1 - \epsilon$, select the greedy action $\arg\max_a Q(s, a)$ (break ties randomly).
   - Apply decay: $\epsilon \leftarrow \max(\epsilon_{\min}, \epsilon \cdot \text{decay\_rate})$ after each episode.
3. **Bellman Equation TD Update**:
   - For transition $(s, a, r, s', \text{done})$:
     $$\text{TD Target} = r + (0 \text{ if done else } \gamma \cdot \max_{a'} Q(s', a'))$$
     $$\text{TD Error} = \text{TD Target} - Q(s, a)$$
     $$Q(s, a) \leftarrow Q(s, a) + \alpha \cdot \text{TD Error}$$
   - Parameters: learning rate $\alpha \in (0, 1]$, discount factor $\gamma \in [0, 1)$.
4. **Policy Extraction & Evaluation**:
   - Extract deterministic greedy policy: $\pi^*(s) = \arg\max_a Q(s, a)$.
   - Evaluate policy deterministically ($\epsilon = 0$) over test episodes without updating $Q$ values.
