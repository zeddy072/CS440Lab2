---
name: python-perf-optimization
description: Profile, vectorize, and eliminate bottlenecks in inner simulation loops, state lookups, and numerical computations
triggers:
  - optimize python performance
  - speed up simulation
  - profile python code
  - vectorize loops
  - optimize inner loop
tags:
  - performance
  - profiling
  - optimization
  - numpy
---

# Python Performance Optimization Skill

## Purpose
Guide the Mini Coding Agent in identifying computational bottlenecks and optimizing high-frequency loops in simulations, grid-worlds, and numerical algorithms.

## Optimization Strategy
1. **Locate Hotspots**:
   - Focus on inner per-step loops and state transition calculations executed thousands of times per training run.
   - Use simple timing (`time.perf_counter`) or standard library `cProfile` before attempting optimizations.
2. **State & Lookup Efficiency**:
   - Replace complex nested dictionaries or tuple-string serializations with integer state IDs or flattened coordinates.
   - Cache static environment layout structures (e.g., walls, valid actions per state, reward grids).
3. **Loop & Array Vectorization**:
   - Replace Python `for` loops over states or batches with vectorized NumPy slice operations where applicable.
   - Avoid creating temporary lists or dictionaries inside high-frequency `step()` or `update()` methods.
4. **Validation**:
   - Run unit tests to verify mathematical equivalence and ensure optimizations introduce zero behavioral regressions.
