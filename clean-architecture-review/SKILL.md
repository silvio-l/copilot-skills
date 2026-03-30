---
name: clean-architecture-review
description: Review a change, feature, or existing code for clean architecture compliance, layer violations, coupling, and misplaced responsibilities.
---

# Clean Architecture Review Skill

## Goal
Verify that code, changes, or architecture decisions maintain clean responsibilities and stable dependencies.

## Review Focus
- Correct layer for the given logic
- Dependency direction
- Leaking of infrastructure or transport details
- Inappropriate shared abstractions
- Premature generalization
- Cross-coupling between features

## Workflow
1. Name the relevant layers / modules.
2. Assign responsibilities.
3. Search for boundary violations.
4. Check dependency direction and coupling.
5. Check whether the solution is local enough.
6. Provide concrete improvement suggestions with minimal intervention.

## Output Format
1. Observed structure
2. Responsibilities per area
3. Layer / boundary violations
4. Coupling and maintainability risks
5. Concrete improvements
6. Minimal recommended intervention
