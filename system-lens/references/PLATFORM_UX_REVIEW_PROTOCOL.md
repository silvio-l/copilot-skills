# Platform-Aware UX Review Protocol

## Purpose

Use this protocol to keep UI/UX review grounded in the platforms the reviewed system actually ships on.

The goal is not "generic UI quality", but:
- detect the real platform families and shipping targets,
- derive the UX conventions users will expect there,
- verify accessibility, localization, and adaptation signals,
- and judge whether the architecture supports those expectations.

## Core rule

Reason from **platform family and shipped target**, not from framework branding alone.

Good:
- "This scope ships on web + mobile, so evaluate browser semantics, touch-first behavior, safe areas, and locale handling."

Bad:
- "This is Flutter, therefore the UX is fine."

## Detection order

1. Determine whether the selected scope has user-facing UI at all.
2. Determine platform families:
   - `web`
   - `mobile`
   - `desktop`
3. Determine concrete shipped targets when the repo proves them:
   - `web`
   - `android`
   - `ios`
   - `windows`
   - `macos`
   - `linux`
4. Collect compact signal samples for:
   - accessibility,
   - localization / i18n,
   - design-system / theming,
   - UI surface files.
5. Use only that compact packet for the UX lane unless a deeper pass is justified.

## Platform-family expectations

### Web

Review for:
- semantic navigation and visible keyboard focus,
- responsive layout and browser-friendly state behavior,
- contrast, labels, reduced motion, and locale-aware formatting,
- user journeys that behave coherently in browser constraints.

### Mobile

Review for:
- touch-first interaction,
- 44x44pt / 48x48dp targets,
- safe areas, keyboard avoidance, and no hover dependence,
- mobile-appropriate navigation / gestures,
- text scaling, offline / loading / permission timing when relevant.

### Desktop

Review for:
- desktop-appropriate interaction, including hover states, keyboard shortcuts, and generous click targets,
- bounded content width and reduced cognitive load for content-light products,
- denser, tool-heavy patterns when the product genuinely behaves like a professional desktop tool,
- and whether the chosen density matches the actual product type instead of a generic default.

## Shared standards

Always keep these in scope when UI is present:
- WCAG-style contrast and accessibility semantics,
- localization / i18n and locale-aware formatting,
- empty / loading / error / reduced-motion states,
- design-system consistency instead of ad-hoc visual rules.

Missing proof is an evidence gap, not proof that the standard is satisfied.

## Architecture coupling questions

The UX lane should explicitly ask:
1. Which platform conventions are expected by users on the detected targets?
2. Which of those expectations are clearly supported in the current UI and architecture?
3. Does the architecture make adaptation possible, or does it force one brittle interaction model across different targets?
4. Are accessibility, localization, and theming first-class capabilities or bolt-ons?

## Load guardrails

To avoid overloading the model:
- do not dump the whole UI knowledge base into the review prompt,
- do not mix every source root into one UX pass,
- do not send the full repo to the UX lane if the UI lives in a subset of roots.

Instead:
1. summarize the relevant roots first,
2. build one compact platform-aware UX brief,
3. review one platform family / UI cluster at a time if the repo is large,
4. merge the findings only after per-cluster passes are done.

## Output expectations

The final system review should make these explicit:
- detected platform families and concrete targets,
- proven platform-specific UX evidence,
- missing accessibility / localization / design-system evidence,
- architecture-to-UX fit,
- and the highest-risk mismatches between shipped platforms and current UX behavior.
