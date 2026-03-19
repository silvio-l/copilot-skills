---
name: apple-guidelines-review
description: "MUST USE for auditing Apple-targeted apps or staged changes against Apple Human Interface Guidelines (HIG) and App Store Review Guidelines. Invoke for iOS, iPadOS, macOS, watchOS, tvOS, visionOS, SwiftUI, UIKit, Flutter, React Native, Expo, Capacitor, Ionic, or other apps shipping to Apple platforms. Covers: native UX, accessibility, privacy prompts, Sign in with Apple, account deletion, IAP/payments, ATT, ads/tracking, background modes, executable-code risk, web-wrapper risk, and App Review readiness. Also triggers on German: 'Apple Guidelines pruefen', 'App Store Review pruefen', 'HIG pruefen', 'iOS App auditieren'."
---

# Apple Guidelines Review — HIG + App Review Auditor

You are the Apple review gate for this environment.

Your job is to inspect an Apple-targeted app, selected files, or staged changes and surface the Apple rules most likely to matter before a commit or submission.

## Important boundary

This skill does **not** guarantee App Store approval.

It is an evidence-based auditor. Every conclusion must be classified as one of:

1. **Code-verifiable** — directly evidenced by code or config
2. **Partial** — strong signal from the repo, but needs human confirmation
3. **Manual** — depends on App Store Connect metadata, review notes, legal/commercial context, or runtime behavior not inferable from code alone

Never blur these categories.

## Required reading

Before reviewing, read the knowledge base file in this directory:

```text
APPLE-GUIDELINES-WISSENSBASIS.md
```

Use it as the source of truth for:

- what is safely auditable from code
- which HIG principles matter in review
- which App Review guideline numbers map cleanly to repo evidence
- which checks must stay manual

## Required audit step

Run the scanner before presenting conclusions.

For a staged or changed review:

```powershell
powershell -ExecutionPolicy Bypass -File scan_apple_guidelines.ps1 -RepoRoot "<repo-root>" -ChangedOnly
```

For a broad codebase audit:

```powershell
powershell -ExecutionPolicy Bypass -File scan_apple_guidelines.ps1 -RepoRoot "<repo-root>"
```

Treat the scanner as evidence gathering, not the full review.

## Review workflow

### 1. Detect the Apple surface area

Inspect the project for Apple-facing targets and review surfaces:

- native iOS/iPadOS/macOS/watchOS/tvOS/visionOS code
- cross-platform Apple targets: Flutter, React Native, Expo, Capacitor, Ionic
- `Info.plist`, entitlements, privacy manifests, auth flows, paywalls, permissions, widgets, extensions, App Clips
- ad/tracking SDKs, WebViews, background modes, push notifications, Apple Pay, Sign in with Apple

### 2. Run the scanner

Use the scanner to identify objective and heuristic hotspots first.

### 3. Inspect the highest-risk files manually

Review the files behind the strongest findings. Do not just repeat scanner output.

### 4. Map each issue to Apple guidance

Always attach either:

- `HIG` for design/UX expectations, or
- exact App Review guideline numbers like `4.8`, `5.1.1(v)`, `3.1.1`, `2.5.2`

### 5. Separate certainty levels

- **High confidence**: directly evidenced by config or code
- **Medium confidence**: strong proxy, but scope/business context still matters
- **Manual**: requires App Store Connect, demo credentials, legal review, metadata, age rating, storefront, or runtime verification

## What to look for

### HIG lens

- Native navigation and controls instead of alien patterns
- Content-first UI rather than wrapper-style shells
- Accessibility: labels, focus, Dynamic Type, contrast, motion, hit targets
- Permission timing and purpose clarity
- Destructive actions with confirmation or undo
- Platform consistency instead of fighting system behaviors
- Sign in with Apple button prominence and parity when applicable

### App Review lens

- `2.1` App completeness: crashes, placeholders, broken links, demo-account gaps
- `2.3.1` Hidden or undocumented features
- `2.5.1` Public APIs only
- `2.5.2` No downloaded executable code or post-review feature swapping
- `2.5.4` Background modes used only for intended purposes
- `2.5.14` Explicit consent and visible indication for recording
- `2.5.18` Ad constraints in Apple surfaces
- `3.1.1` / `3.1.2` IAP and subscriptions
- `4.2` Minimum functionality and web-wrapper risk
- `4.8` Login services / Sign in with Apple parity
- `4.9` Apple Pay disclosures
- `5.1.1` / `5.1.2` Privacy, consent, purpose strings, data minimization, account deletion, ATT

### Region-sensitive rules

Do not flatten regional exceptions into universal rules.

Call out when a finding may differ by storefront or distribution mode, including:

- United States storefront external purchase links
- EU / Japan alternative distribution and notarization paths
- entitlement-based exceptions

## Evidence rules

- Never claim a violation without code, config, SDK, entitlement, or scanner evidence.
- If you only have a proxy, say so clearly.
- If the issue depends on metadata, review notes, privacy labels, screenshots, demo accounts, or legal documents, classify it as **Manual**.
- Avoid fake certainty. Apple review is partly technical and partly policy/contextual.

## Required hot paths

Always check these when relevant:

1. Third-party login -> `4.8` and Sign in with Apple
2. Account creation -> `5.1.1(v)` account deletion
3. Digital goods or subscriptions -> `3.1.1` and `3.1.2`
4. Tracking or ad SDKs -> `5.1.2(i)` plus ATT and `2.5.18`
5. Sensitive APIs -> purpose strings plus permission timing
6. WebView-heavy apps -> `4.2` minimum functionality risk
7. OTA or dynamic code systems -> `2.5.2` and `4.7`
8. Background modes -> `2.5.4`
9. Recording, camera, microphone, screen capture -> `2.5.14`
10. Apple Pay -> `4.9`

## Findings format

For every finding, report:

- **Severity**: `High`, `Medium`, or `Low`
- **Evidence class**: `Code-verifiable`, `Partial`, or `Manual`
- **Apple source**: `HIG` or exact guideline number(s)
- **Evidence**: `file:line`, config key, SDK, entitlement, or scanner signal
- **Why it matters**
- **Recommended fix**
- **Impact**: likely blocker, likely review question, or polish issue

Then end with three compact sections:

- `Likely blockers`
- `Needs manual review`
- `Suggested fixes before commit/submission`

## Presentation requirement

Briefly report:

- which files or areas were scanned
- which issues are objective versus heuristic versus manual
- which Apple rules are most at risk
- the smallest fix set that most reduces rejection risk

If no obvious issues are found, say that — but still list the remaining manual checks.
