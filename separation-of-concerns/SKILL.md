---
name: separation-of-concerns
description: "MUST USE for ANY medium or large code change across any language or framework. Audits separation of concerns, runs the included script-backed SoC scan, flags files that mix presentation, domain, data, and infrastructure responsibilities, and pushes maintainable refactoring over feature sprawl."
---

# Separation of Concerns — Universal Maintainability Gate

This skill is the **mandatory** cross-language architecture gate for medium and large changes. It is not optional, not a suggestion, and not something to "do later."

**Run it BEFORE presenting ANY change** that touches multiple files, modifies existing business logic, or risks blending UI, domain, persistence, orchestration, or infrastructure concerns.

## Core Rule

**One file, one dominant reason to change.**

Perfect purity is not required, but accidental layering violations are not acceptable. Files that grow beyond their layer's size guidance MUST be addressed — either by refactoring or by explicit justification.

## Mandatory Audit Step (Cross-Platform)

The audit script runs on **any platform** with Node.js installed (Windows, macOS, Linux).

### Quick scan — changed files only (default for most tasks):

```sh
node scan_soc.mjs "<repo-root>" --changed-only
```

### Full scan — all files (for architectural or broad tasks):

```sh
node scan_soc.mjs "<repo-root>"
```

### JSON output (for programmatic consumption):

```sh
node scan_soc.mjs "<repo-root>" --json
```

### Options:

| Flag | Short | Description |
|------|-------|-------------|
| `--changed-only` | `-c` | Only scan files with uncommitted git changes |
| `--top N` | `-t N` | Show top N results (default: 25) |
| `--json` | `-j` | Output as JSON |
| `--help` | `-h` | Show usage information |

### Exit Codes:

| Code | Meaning |
|------|---------|
| `0` | No HIGH-severity findings |
| `1` | At least one HIGH-severity finding — **MUST be addressed** |

### Enforcement Rules:

1. **Exit code 1 blocks presentation.** If the scan returns exit code 1, you MUST either fix the violations OR explicitly document why each HIGH finding is an intentional exception.
2. **MEDIUM findings are review nudges.** Address them when practical, document when intentionally left.
3. **LOW findings are informational.** Note them but don't block on them.

## Responsibility Matrix

### Presentation

Examples: screens, widgets, views, components, pages

- Responsible for composition, rendering, accessibility, input handling, and delegating actions
- May depend on application/state adapters
- **Must not** own database, network, filesystem, or domain algorithm code
- **Must not** contain raw persistence queries

### Application / Orchestration

Examples: providers, controllers, view-models, blocs, notifiers

- Responsible for wiring dependencies, state transitions, invalidation, and task orchestration
- May call repositories/services
- **Must** stay thin enough to reason about quickly
- **Must not** grow into a second business-logic layer

### Domain / Services

Examples: services, engines, use-cases, calculators

- Responsible for pure business rules and decision logic
- Prefer deterministic inputs and outputs
- **Must not** depend on UI frameworks or navigation
- Should avoid direct persistence unless the project explicitly uses a domain-service-with-ports pattern

### Data / Infrastructure

Examples: repositories, DAOs, database adapters, API clients

- Responsible for IO, persistence, transport, mapping at boundaries
- **Must not** import UI frameworks or navigation
- **Must not** contain visual formatting or widget construction

### Models / DTOs / Entities

- Responsible for data shape and lightweight invariants
- **Must not** own IO, navigation, or presentation logic

### Cross-Cutting

Examples: logging, monitoring, formatting, configuration

- Keep shared and explicit
- Avoid scattering the same concern across screens and repositories without a central abstraction

## File Size Limits

Every layer has a **target** (preferred maximum) and a **hard review** threshold. Files exceeding the hard review limit are automatically flagged:

| Layer | Target | Hard Review |
|-------|--------|-------------|
| Presentation | 250 lines | 350 lines |
| Application | 220 lines | 320 lines |
| Domain | 200 lines | 280 lines |
| Data | 220 lines | 320 lines |
| Model | 160 lines | 220 lines |
| General | 300 lines | 450 lines |

**Rule:** No file should grow beyond the hard review limit without an explicit justification in the presentation. If a file is already above the limit and you are modifying it, you MUST either reduce it or document why you cannot.

## What the Script Flags

- Oversized files that likely carry too many responsibilities
- UI-layer files importing persistence or networking primitives
- Data-layer files importing UI frameworks or navigation
- Service/model files that depend on UI or infrastructure
- Mixed concern clusters such as navigation + persistence + filesystem in one file
- Controllers/providers that are turning into mini-monoliths
- Files with 5+ top-level type declarations (classes, enums, structs, etc.)

## How to Respond to Findings

For each flagged file, ask:

1. Can an existing abstraction be extended instead of adding another helper?
2. Is this file doing two jobs, or just one job with unavoidable context?
3. Would extracting a service, mapper, widget, or repository method make the code easier to test?
4. Would the extraction actually reduce coupling, or only move the same mess elsewhere?

Refactor only when it improves clarity. Do not split files mechanically.

## Presentation Requirement

When this skill is used, **always** report:

- Which files the script flagged (severity + layer)
- Which of them you actually refactored and how
- Which flagged items were intentionally left alone and **why**
- Whether the scan exited with code 0 or 1

