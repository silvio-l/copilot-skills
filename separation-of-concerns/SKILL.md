---
name: separation-of-concerns
description: "MUST USE for ANY medium or large code change across any language or framework. Audits separation of concerns, runs the included script-backed SoC scan, flags files that mix presentation, domain, data, and infrastructure responsibilities, and pushes maintainable refactoring over feature sprawl."
---

# Separation of Concerns — Universal Maintainability Skill

This skill is the cross-language maintainability gate for medium and large changes.

Use it whenever a task spans multiple files, touches existing business logic, or risks blending UI, domain, persistence, orchestration, or infrastructure concerns.

## Core Rule

**One file, one dominant reason to change.**

Perfect purity is not required, but accidental layering violations are not acceptable.

## Required Audit Step

Before presenting a medium or large change, run the included audit script:

```powershell
powershell -ExecutionPolicy Bypass -File scan_soc.ps1 -RepoRoot "<repo-root>" -ChangedOnly
```

If the task is architectural, broad, or already smells mixed, run the full scan:

```powershell
powershell -ExecutionPolicy Bypass -File scan_soc.ps1 -RepoRoot "<repo-root>"
```

The script highlights files that are likely doing too much or living in the wrong layer. Treat it as a refactoring nudge, not a blind lint.

## Responsibility Matrix

### Presentation

Examples: screens, widgets, views, components, pages

- Responsible for composition, rendering, accessibility, input handling, and delegating actions
- May depend on application/state adapters
- Must not own database, network, filesystem, or domain algorithm code
- Must not contain raw persistence queries

### Application / Orchestration

Examples: providers, controllers, view-models, blocs, notifiers

- Responsible for wiring dependencies, state transitions, invalidation, and task orchestration
- May call repositories/services
- Must stay thin enough to reason about quickly
- Should not grow into a second business-logic layer

### Domain / Services

Examples: services, engines, use-cases, calculators

- Responsible for pure business rules and decision logic
- Prefer deterministic inputs and outputs
- Must not depend on UI frameworks or navigation
- Should avoid direct persistence unless the project explicitly uses a domain-service-with-ports pattern

### Data / Infrastructure

Examples: repositories, DAOs, database adapters, API clients

- Responsible for IO, persistence, transport, mapping at boundaries
- Must not import UI frameworks or navigation
- Must not contain visual formatting or widget construction

### Models / DTOs / Entities

- Responsible for data shape and lightweight invariants
- Must not own IO, navigation, or presentation logic

### Cross-Cutting

Examples: logging, monitoring, formatting, configuration

- Keep shared and explicit
- Avoid scattering the same concern across screens and repositories without a central abstraction

## What the Script Flags

- Oversized files that likely carry too many responsibilities
- UI-layer files importing persistence or networking primitives
- Data-layer files importing UI frameworks or navigation
- Service/model files that depend on UI or infrastructure
- Mixed concern clusters such as navigation + persistence + filesystem in one file
- Controllers/providers that are turning into mini-monoliths

## How to Respond to Findings

For each flagged file, ask:

1. Can an existing abstraction be extended instead of adding another helper?
2. Is this file doing two jobs, or just one job with unavoidable context?
3. Would extracting a service, mapper, widget, or repository method make the code easier to test?
4. Would the extraction actually reduce coupling, or only move the same mess elsewhere?

Refactor only when it improves clarity. Do not split files mechanically.

## Presentation Requirement

When this skill is used, briefly report:

- Which files the script flagged
- Which of them you actually refactored
- Which flagged items were intentionally left alone and why

## HellerIO-specific Hint

For this codebase, keep these seams especially clean:

- `screens/` and `widgets/` should stay UI-first
- `providers/` should orchestrate, not simulate
- `services/` should own pure planning math
- `repositories/` should own Drift access
- shared interaction patterns belong in `lib/core/widgets/`
