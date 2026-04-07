# Stack Detection and Skill Routing

## Purpose

Use this file to decide which review lanes and companion skills belong in the final system review.

## Detection order

1. Read repository manifests and top-level structure.
2. Determine the main source roots and cover them before diving into a single hotspot.
3. Determine whether the repo is:
   - single-language,
   - polyglot,
   - frontend-heavy,
   - mobile app,
   - backend/service-heavy,
   - or mixed product surface + backend.
4. Determine whether the target has user-facing UI.
5. Determine which platform families and concrete targets the selected scope actually ships on.
6. Build an architecture brief: likely goals, quality attributes, decision evidence, open human questions, and platform-aware UX expectations.
7. Route to the smallest useful set of companion skills.

## Common signals

| Signal | Meaning | Review impact |
|---|---|---|
| `pubspec.yaml` with `sdk: flutter` or a `flutter:` section | Flutter app | Architecture + Flutter-specific + likely UI/UX |
| `pubspec.yaml` without Flutter markers | Dart package / tooling | Architecture only unless user-facing surfaces are proven |
| `package.json` + React/Vue/Astro | Web frontend | Architecture + code review + UI/UX |
| `wails.json` | Wails desktop shell | Architecture + code review + UI/UX (desktop + web-rendered shell expectations) |
| `pyproject.toml` / `requirements.txt` | Python | Architecture + code review |
| `Cargo.toml` | Rust | Architecture + code review |
| `go.mod` | Go | Architecture + code review |
| `pom.xml` / non-Flutter `build.gradle` | JVM | Architecture + code review |
| `docker-compose.yml`, `Dockerfile`, `k8s/`, `helm/` | Runtime / deployment layer present | Add operational and boundary review |
| `docs/`, `adr/`, `ADRs`, `*.md` architecture docs | Intent and decisions may be available | Compare code vs docs / ADRs |
| diagrams (`.drawio`, `.puml`, `.mmd`, `.svg`) | Architecture may be documented visually | Compare intended architecture vs implemented structure |
| SARIF / Sonar / Semgrep / other analysis artifacts | Existing tool facts are available | Treat tool output as stronger evidence than unsupported inference |

## UI/UX inclusion rules

UI/UX review is required when the target contains:
- Flutter widgets, themes, screens, settings, onboarding, dialogs,
- web components, templates, CSS, design tokens,
- visible user flows, copy, empty states, error states,
- or when the user explicitly asks for a full impression of the app/product.

When UI/UX review is required, also derive:
- platform families (`web`, `mobile`, `desktop`),
- concrete shipped targets when the repo proves them,
- accessibility, localization, and design-system evidence,
- and whether the architecture appears to support those platform expectations.

UI/UX review is not required for:
- pure infra repos,
- libraries with no user-facing surfaces,
- backend-only services with no admin UI or client surface in scope.

## Companion skill routing

| Condition | Companion skills |
|---|---|
| Unknown or large codebase | `codebase-map` |
| Change-focused review with a concrete diff / PR / staged change | `code-change-review` |
| Architecture, boundaries, layers, module drift | `clean-architecture-review`, `dependency-boundary-check` |
| Performance-sensitive codepaths or data-heavy flows | `performance-regression-scan` |
| Flutter app code | `flutter-best-practices` |
| User-facing UI present | `premium-ui-ux` |
| User-facing UI with user-journey / copy / onboarding concerns | `persona-ux-review` |
| Flutter app with iOS/macOS targets and Apple shipping concern | `apple-guidelines-review` |

If `persona-ux-review` is unavailable, keep user-journey, copy, trust, and onboarding checks inside `premium-ui-ux` instead of dropping the lane.

## Synthesis rule

Companion skills feed the final review, but they do not replace it.

Architecture findings must be synthesized from:
- repository structure,
- code/config evidence,
- docs/ADRs and diagrams when present,
- tool outputs when present,
- and a dual-model corroboration pass with GPT-5.4 and Claude Sonnet 4.6.

Your final answer must synthesize:
- what the system is,
- where it is strong,
- where it is weak,
- whether UI/UX supports or undermines the architecture,
- what should be fixed first.

Avoid returning one disconnected section per skill. Merge them into one review.
