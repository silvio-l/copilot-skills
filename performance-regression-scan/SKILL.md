---
name: performance-regression-scan
description: Review changes or code paths for potential performance regressions, unnecessary work, redundant I/O, rendering, sync, or data movement.
---

# Performance Regression Scan Skill

## Goal
Early detection of typical performance risks after changes.

## Check Points
- Unnecessary repetitions / loops / traversals
- Too frequent re-renders / recomputations / rebuilds
- Unnecessary network, filesystem, or DB accesses
- Missing caching or incorrect caching
- Blocking work in critical paths
- Expensive mapping or serialization chains

## Output Format
1. Relevant paths
2. Potential regressions
3. Severity / likelihood
4. Recommended countermeasures
5. Measurement / verification recommendations
