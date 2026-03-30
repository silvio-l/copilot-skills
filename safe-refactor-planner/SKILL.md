---
name: safe-refactor-planner
description: Plan refactorings to stay small, safe, incremental, and well-validatable without unnecessary architecture movement.
---

# Safe Refactor Planner Skill

## Goal
Break a refactor into small, controllable steps.

## Workflow
1. Clearly name the refactor goal
2. Capture existing code and dependencies
3. Mark risks and fragile areas
4. Plan the smallest possible steps
5. For each step define:
   - Purpose
   - Changed files
   - Expected benefit
   - Validation
   - Rollback capability

## Rules
- Do not unintentionally change behavior
- Do not mix refactoring with feature work, unless deliberate and explicit
- Stabilization first, then structural improvement

## Output Format
1. Refactor goal
2. Relevant areas
3. Risks
4. Step plan
5. Validation per step
6. Rollback / safety strategy
