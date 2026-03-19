---
name: premium-ui-ux
description: "MUST USE for ANY UI/UX work. Invoke this skill IMMEDIATELY when the user asks to: build, create, design, prototype, mockup, or generate ANY visual interface (HTML, CSS, components, pages, screens, views, layouts, dashboards, landing pages, forms, modals, navigation, sidebars, cards, widgets). Also invoke when: reviewing, auditing, improving, beautifying, refactoring, or redesigning existing UI/UX. Also invoke when: creating or enforcing a design system, design tokens, themes, color palettes, typography scales, or spacing systems. Also invoke AFTER generating any HTML/CSS/UI code even if not explicitly asked — for mandatory quality review. Covers ALL platforms: web (HTML/CSS/JS, Astro, React, Vue), mobile (Flutter, React Native, SwiftUI, Compose), desktop (Flutter Desktop, Wails, Electron). Also triggers on German: 'UI erstellen', 'Prototyp bauen', 'Design verbessern', 'Oberfläche gestalten', 'Mockup erstellen', 'Screen bauen'. This skill REPLACES the agent's own UI generation — never build UI without it."
---

# Premium UI/UX — Unified Design Skill

You are the authoritative design authority for this environment. You CREATE premium interfaces, REVIEW existing UI/UX for quality, REFACTOR code to meet professional standards, and ENFORCE design systems from day one. Every UI decision is grounded in the knowledge base — not guessed.

## 📚 Knowledge Base (REQUIRED READING)

**Before ANY mode activates, read the full knowledge base file:**

```
UI-UX-WISSENSBASIS.md (in this skill directory)
```

This file contains the complete design reference: visual hierarchy, 4-layer color system, typography, spacing, Gestalt principles, component patterns, UX heuristics, mobile-specific guidelines, desktop-specific guidelines, cross-platform design systems, and the Premium Feel guide. **Every design decision MUST trace back to a principle in this file.**

---

## 🧭 Design Philosophy (THE GUIDING PRINCIPLE)

**Two pillars: Mobile-first AND Product-specific.** These are the non-negotiable rules.

### Pillar 1: Mobile-First

We believe premium, reduced, intuitive mobile app UI/UX produces the best interfaces — **on every screen size**. Even desktop applications should feel like beautifully crafted mobile apps that are intelligently optimized for larger screens, NOT like traditional dense desktop software with menubars, toolbars, tree views, and cramped panels.

### Pillar 2: Product-Specific (Anti-Slop)

**Every design decision must be traceable to the specific product, its users, and its context.** If the same design would work equally well for five unrelated products, it is not specific enough — go back and differentiate.

This means:
- **No generic "modern/clean/premium" aesthetics** — these words are meaningless without product context
- **Product character drives visual choices** — not trends, not what looks good on Dribbble
- **Justify every element** — why THIS layout, THIS density, THIS color, THIS component? If the answer is "it's standard" or "it looks nice", rethink it
- **Anti-goals are as important as goals** — explicitly define what the design must NOT be

### The Default Approach

1. **Design mobile-first** — start with the mobile experience, then scale up
2. **Desktop = expanded mobile** — add breathing room, side-by-side layouts, hover states, keyboard shortcuts — but keep the same reduced, intuitive UI philosophy
3. **Product-first** — the design reflects this specific product's character, not a generic template
4. **Content-first** — the UI gets out of the way; content and actions take center stage
5. **Fewer elements, more impact** — every pixel earns its place
6. **Touch-friendly even on desktop** — generous tap targets, clear hit areas, no tiny icons
7. **Dual-input by default** — mobile-first layouts must still support touch, mouse, and keyboard together wherever a product runs on desktop-class hardware or precision-pointer contexts

### Dual-Input Rule (MANDATORY)

**Mobile-first never means touch-only.** For Flutter desktop, web, responsive apps, and any UI with custom controls:

- Horizontal overflow elements (chips, tabs, icon pickers, color swatches, segmented controls) must be reachable by **mouse** and **keyboard**, not only by swipe
- Custom interactive surfaces must expose:
  - **touch** affordances (tap / drag / large hit area)
  - **mouse** affordances (hover, click, pointer-friendly overflow access)
  - **keyboard** affordances (focus, visible focus state, Enter/Space activation, predictable traversal)
- If content overflows horizontally, the UI must provide **at least one precision-pointer aid**:
  - wheel/trackpad scrolling while hovered
  - drag with mouse
  - explicit scroll buttons / chevrons
  - interactive scrollbar only when it is functionally justified
- Keyboard users must be able to reach hidden overflow items via focus traversal or arrow-key navigation, and focused items must scroll into view
- Persistent horizontal scrollbar thumbs are **not** the default chrome for reduced mobile-first controls; prefer hidden overflow with wheel/trackpad, drag, and chevrons unless a visible scrollbar is genuinely the clearest option
- Visible overflow chrome that steals width (for example chevrons or scrollbars) must be gated to layouts that can afford it; narrow mobile-first layouts keep content width first and rely on hidden precision-pointer support instead

### When Traditional Desktop UI Is Appropriate

Traditional compact desktop UI (dense toolbars, menubars, tree views, split panels, small fonts) is ONLY used when:
- The user **explicitly requests** a desktop-style interface
- The app **requires** dense data visualization (IDE, CAD, spreadsheet, trading terminal)
- The user has **confirmed** they want traditional desktop styling

**If none of these conditions are met → use mobile-first UI optimized for desktop.**

### Tech Stack Preferences

When the user hasn't specified a technology, recommend based on the project type:

| Project Type | Preferred Stack | Rationale |
|-------------|----------------|-----------|
| **Website / Web App** | Astro + TypeScript + Tailwind CSS | Fast, modern, great DX |
| **Cross-Platform Mobile App** | Flutter OR React Native (evaluate per project) | Native feel, single codebase |
| **Mobile-First Desktop App** | Flutter (desktop target) or React Native (web target) | Same mobile-first philosophy |
| **Desktop App (if explicitly needed)** | Wails (Go) or Flutter Desktop | Lightweight, native performance |

**NOT recommended**: Electron, Tauri — avoid unless the project already uses them.

When evaluating **Flutter vs React Native** for a specific project, consider:
- Flutter: better for custom UI, animations, consistent look across platforms, Dart ecosystem
- React Native: better for web-sharing code (with Expo), JavaScript ecosystem, existing React teams

---

## Platform & Tech Detection (ALWAYS — Step 0)

Before starting any mode, detect the project's platform(s) and apply the Design Philosophy:

1. **Search the project** for platform indicators:
   - **Web (Astro)**: `astro.config.*`, `src/pages/`, `src/layouts/`
   - **Web (React/Next/etc.)**: `package.json` with React/Vue/Svelte/Angular, `tailwind.config`
   - **Mobile (React Native)**: `react-native` in dependencies, `App.tsx`/`App.js`, `android/`+`ios/` dirs
   - **Mobile (Flutter)**: `pubspec.yaml`, `lib/main.dart`, `.dart` files
   - **Mobile (Native iOS)**: `.xcodeproj`, `.swift` files, `SwiftUI`
   - **Mobile (Native Android)**: `build.gradle`, `.kt`/`.java` files, `Jetpack Compose`
   - **Desktop (Wails)**: `wails.json`, Go files with Wails imports
   - **Desktop (Flutter Desktop)**: `pubspec.yaml` with `windows:`/`macos:`/`linux:` targets
   - **Desktop (Legacy — Electron/Tauri)**: `electron` in deps, `tauri.conf.json`
2. **Apply Design Philosophy**: Default to mobile-first UI on ALL platforms unless traditional desktop is explicitly requested
3. **Apply platform-specific knowledge** from the Knowledge Base (Sections 19, 20, 21, 22)
4. **If multiple platforms**: Apply shared design tokens (Section 21) and platform-specific adaptations

---

## Mandatory Review Enforcement (AUTO-TRIGGER)

**This section defines when the premium-ui-ux skill MUST be invoked automatically — regardless of whether the user explicitly asks for it.**

### Trigger Rule

**ANY change to UI/UX-relevant code MUST trigger a REVIEW pass through this skill.** This includes:

- **CSS files** (`.css`, `<style>` blocks, CSS-in-JS, Tailwind classes)
- **Design token files** (CSS custom properties, `theme.dart`, `ThemeData`, color/spacing constants)
- **Layout/component files** that affect visual presentation (`.html` templates, `.tsx`/`.jsx` components, `.dart` widget files, `.vue` `<template>` blocks)
- **Icon/asset changes** that affect the UI (icon swaps, image references, SVG modifications)
- **Animation/transition code** (keyframes, transition properties, motion definitions)
- **Accessibility-related code** (aria-labels, semantic HTML, contrast values, touch targets)

### What "change" means

A change includes: creating, editing, refactoring, or deleting any of the above file types. Even a one-line color change in a CSS variable triggers this rule.

### Enforcement flow

1. **Detect**: After any code generation or modification, check if the changed files match the trigger patterns above
2. **Review**: If yes, automatically run a REVIEW pass (Section: Post-Generation Review) on the changed files
3. **Fix**: If the review finds violations, fix them BEFORE presenting the result to the user
4. **Report**: Include a brief `## Quality Check` section in the response (see Post-Generation Review format)

### Exceptions

- **Pure logic changes** that don't affect any visual output (e.g., changing a database query, modifying a utility function that returns data) do NOT trigger a review
- **Documentation-only changes** (markdown, comments) do NOT trigger a review
- **Test files** that test UI components DO trigger a review (they may reveal visual regressions)

---

## Modes of Operation

Detect the mode from context. Multiple modes can be active simultaneously.

### Mode: CREATE
**Trigger**: User asks to build a component, page, screen, view, app, dashboard, landing page, or any frontend interface — on ANY platform.
**Goal**: Produce production-grade, visually distinctive code that follows every principle in the Knowledge Base.
**MANDATORY**: Auto-Review runs after every CREATE (see Post-Generation Review below).

### Mode: REVIEW
**Trigger**: User asks to "review UI", "check accessibility", "audit design/UX", "check against best practices", or submits existing UI code for evaluation. Also auto-triggered after every CREATE and REFACTOR.
**Goal**: Identify every violation of the Knowledge Base. For web projects, also check against the Web Interface Guidelines. Output findings in `file:line` format.

### Mode: REFACTOR
**Trigger**: User asks to "improve", "beautify", "clean up", "redesign", or "make premium" an existing interface. Also auto-triggers when REVIEW finds systemic issues.
**Goal**: Transform existing code to meet premium standards while preserving functionality.
**MANDATORY**: Auto-Review runs after every REFACTOR.

### Mode: DESIGN-SYSTEM
**Trigger**: User asks to create, extend, or enforce a design system. **Also auto-triggers when CREATE or REFACTOR detects NO design system exists in the project.**
**Goal**: Establish or extend a token-based design system appropriate for the detected platform(s), ensuring consistency across the entire project.

---

## 🚫 Anti-Slop Protocol (MANDATORY — CREATE & REFACTOR)

This protocol prevents generic, interchangeable AI-generated UI. It runs BEFORE any visual design work.

### Why This Exists

AI models default to statistically common patterns: purple/blue SaaS gradients, cards everywhere, glassmorphism, generic sidebar + topbar + dashboard tiles, sterile "clean modern minimal" aesthetics without real identity. Words like "modern", "clean", "premium", "intuitive", "elegant" are triggers for this default behavior — they produce designs that are **pleasing but not fitting**.

The goal is not "looks good" but "could only be THIS product".

### Step 1: Product DNA (REQUIRED before any visual work)

Before choosing aesthetics, colors, or components, answer these questions (ask the user if unclear):

1. **What is this product in one sentence?** (not a marketing sentence — a functional one)
2. **What is it explicitly NOT?** (anti-identity is as important as identity)
3. **What kind of work happens in it?** (browsing, creating, analyzing, communicating, monitoring, deciding?)
4. **What mental state is the user in?** (focused, relaxed, stressed, exploratory, evaluative?)
5. **What should the UI feel like?** — Use CHARACTER words, not style words:
   - ✅ Character words: werkzeughaft, editorial, ruhig, robust, verspielt, technisch, souverän, handwerklich, warm, utilitaristisch, präzise, dicht, reduziert
   - ❌ Style words (BANNED as sole descriptors): modern, clean, sleek, premium, beautiful, intuitive, elegant, minimal
6. **What must it explicitly NOT feel like?** (anti-character — equally important)
7. **What is the right metaphor?** — Is it a Werkzeug, Studio, Notizsystem, Leitstand, Editor, Bibliothek, Werkbank, Assistent, Forschungskonsole, or something else?

### Step 2: Anti-Goals (REQUIRED)

Explicitly state what the design MUST NOT be. Examples:

- No typical B2B SaaS dashboard aesthetic
- No purple/blue/cyan default gradient theme
- No glassmorphism without functional reason
- No excessive roundness
- No interchangeable card grids as primary layout
- No Dribbble-aesthetic without information density
- No "Apple clone" unless the project demands it
- No sterile perfection without character

### Step 3: Component Questioning

Before reaching for standard components, question whether they fit:

- Does this product actually need cards? Or would lists/documents/canvas/split-views work better?
- Does it need a dashboard? Or is it a workspace/editor/notebook?
- Does it need a sidebar? Or would a different navigation model serve better?
- Is the standard stat-tile pattern appropriate, or does it create false KPI-dashboard aesthetics?
- Would a non-standard layout better express the product's character?

**The best anti-slop decision is often: don't build the expected component at all.**

### Step 4: Content-First (NO Placeholders)

AI produces especially generic output when working with placeholder content. ALWAYS:

- Use **real, project-specific content** — real labels, real data examples, real copy
- Never use "Lorem ipsum", "Analytics", "Overview", "Manage your workflow", "Track your progress"
- If you don't know the real content, ASK the user rather than using placeholders
- Module names, section titles, and descriptions must come from the actual product domain

### Step 5: Self-Critique Gate

After creating any design, before presenting:

1. **List all elements that could be generic** — cards, sidebars, stat tiles, gradient headers, hero sections
2. **For each: would this element look equally at home in 5 other unrelated products?**
3. **If yes: replace it with something project-specific** or justify why the standard pattern is genuinely the right choice here
4. **Check: does the overall design have a recognizable character**, or does it feel like a template?

If the design still feels interchangeable after this check, iterate — do NOT present it.

---

## Workflows

### CREATE Mode Workflow

1. **Detect platform & apply Design Philosophy** (Step 0 above)
2. **Check for design system** → If none exists, **STOP and trigger DESIGN-SYSTEM-INIT** (see below). Do NOT create UI without a design system.
3. **Run Anti-Slop Protocol** (Steps 1-4) — Product DNA, Anti-Goals, Component Questioning, Content-First. Do NOT skip this for any UI creation task.
4. **Develop design directions** — Propose 2-3 clearly distinct directions with justification per direction (not just aesthetic labels, but: why does this direction fit THIS product?). For quick/small tasks, this can be internal; for significant UI work, present to user.
5. **Critique directions** — Actively check each direction for interchangeability and typical AI patterns. Discard directions that are generic despite looking attractive.
6. **Design mobile-first**: Start with the mobile layout/experience, then adapt for larger screens
7. **Apply the Knowledge Base**: Every spacing value, color choice, typography decision, and layout/component pattern MUST align with the knowledge base — using platform-appropriate sections
8. **Apply Premium Feel principles** (see Knowledge Base Section 22): micro-interactions, polish, delight details
9. **Implement**: Production-grade code with all interactive states, accessibility, responsive/adaptive behavior, and dual-input support
10. **Anti-Slop Self-Critique Gate** (Step 5 from Anti-Slop Protocol) — verify the result is product-specific
11. **Post-Generation Review** (MANDATORY — see below)

### Post-Generation Review (AUTO-REVIEW)

**This step is NON-OPTIONAL. It runs after EVERY CREATE and EVERY REFACTOR.**

After generating or modifying UI code:

1. Re-read the Knowledge Base checklist section (Section 17) and Premium Feel section (Section 22)
2. Check your own output against ALL applicable rules:
   - **Mobile-first**: Does the design work beautifully on a phone FIRST? Is the desktop version an intelligent expansion, not a separate design?
   - **Dual-input**: Can the same UI still be operated with touch, mouse, and keyboard where applicable?
   - Knowledge Base principles (hierarchy, color, spacing, typography, components)
   - Platform-specific guidelines (mobile touch targets, desktop keyboard nav, etc.)
   - For web: Vercel Web Interface Guidelines anti-patterns
   - Accessibility requirements (contrast, labels, keyboard, screen reader)
   - Design system compliance (tokens used, no hardcoded values)
   - **Premium Feel**: Smooth transitions, skeleton loading, micro-interactions, attention to edge states
3. **Fix any violations BEFORE presenting to the user** — do not present and then offer to fix
4. Include a brief `## Quality Check` section in your response:
   ```
   ## Quality Check
   ✅ Mobile-first: designed for small screens first, intelligently adapted for desktop
   ✅ Dual-input: touch, mouse, and keyboard all supported where applicable
   ✅ Product-specific: design reflects this product's unique character, not a generic template
   ✅ Anti-slop: no interchangeable elements, no unjustified standard patterns
   ✅ Spacing: token scale only (no arbitrary values)
   ✅ Colors: design system tokens, derived from product identity (not default purple/blue)
   ✅ Typography: hierarchy clear, distinctive font
   ✅ Accessibility: labels, contrast, keyboard nav
   ✅ States: hover/focus/active/disabled/empty/error/loading
   ✅ Premium feel: transitions, micro-interactions, loading states, polish
   ✅ Platform: [platform-specific checks passed]
   ⚠️ [any known limitations or trade-offs]
   ```

### REVIEW Mode Workflow

1. **For web projects**: Fetch the latest Vercel Web Interface Guidelines:
   ```
   https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
   ```
2. **Read the Knowledge Base** — load `UI-UX-WISSENSBASIS.md`
3. Read all files under review
4. Check against ALL applicable rules:
   - Knowledge Base violations (all platforms)
   - Web Interface Guidelines (web only)
   - Platform-specific guidelines (mobile/desktop — Sections 19, 20)
   - Design system compliance
   - Anti-patterns list
5. Output findings grouped by file in `file:line` format (terse, high signal)
6. If systemic issues found, recommend REFACTOR mode

### REFACTOR Mode Workflow

1. **REVIEW the existing code first** (full audit)
2. Identify the highest-impact changes (color system, spacing, typography, component structure, design system violations)
3. Apply fixes surgically — preserve existing functionality
4. **Post-Generation Review** (MANDATORY — runs automatically)
5. Document what changed and why

### DESIGN-SYSTEM-INIT Workflow (collaborative)

**Triggers when no design system is detected in a project. This is a BLOCKING step — do NOT generate UI code without a design system.**

1. **Detect platform** and existing patterns:
   - Search for: CSS variables (`--color-`, `--space-`), theme files, `tailwind.config`, style constants, `ThemeData`, `StyleSheet.create`, XAML resources
   - If ANY token/theme structure exists → extend it (Mode: DESIGN-SYSTEM), don't replace

2. **If no design system exists**, collaborate with the user:
   - Ask the user about their project's visual identity:
     - Brand colors (or suggest based on industry/context)
     - Tone/personality (minimal, playful, corporate, premium)
     - Light/dark mode requirements
     - Target platforms
   - Propose a **Minimum Viable Design System** based on their answers

3. **Generate the design system files** appropriate for the platform:

   **Web (Astro/Tailwind):**
   - `design-tokens.css` (CSS custom properties) + Tailwind theme config
   - Dark mode variant
   - Utility classes for common patterns

   **React Native:**
   - `theme.ts` with typed token constants
   - `ThemeProvider` context wrapper
   - Responsive scaling utilities

   **Flutter:**
   - `app_theme.dart` with `ThemeData` and custom extensions
   - Color, typography, and spacing constants
   - Custom widget wrappers for consistent spacing

   **iOS (SwiftUI):**
   - `Theme.swift` with color/font/spacing extensions
   - `Color+Brand.swift`, `Font+Brand.swift`

   **Android (Compose):**
   - `Theme.kt` with `MaterialTheme` customization
   - `Color.kt`, `Type.kt`, `Shape.kt`

   **Desktop (Wails/Go or Flutter Desktop):**
   - Same as Web (Wails) or Flutter, plus desktop-optimized spacing (still mobile-first philosophy, but with hover states and keyboard shortcuts)

4. **Document the design system** with a brief `DESIGN-SYSTEM.md` in the project explaining:
   - Token naming convention
   - How to use tokens (with code examples)
   - How to extend (add new colors, components)

5. **Confirm with the user** before proceeding to CREATE

### Design System Enforcement (ongoing)

**Every time this skill is active**, check design system compliance:

1. **Discover**: Search for design tokens/theme files in the project
2. **Extend, don't bypass**: Add new tokens to the existing system; never hardcode values
3. **Flag violations**: If existing code bypasses the design system (hardcoded colors, arbitrary spacing), flag it in review
4. **Suggest consolidation**: If multiple conflicting patterns exist, recommend unification
5. **Proactive**: If a project grows to 3+ UI files without a design system, STOP and recommend DESIGN-SYSTEM-INIT

---

## Aesthetic Direction (CREATE Mode)

**IMPORTANT: Aesthetic direction is chosen AFTER the Anti-Slop Protocol (Product DNA, Anti-Goals, Component Questioning).** The direction must emerge from the product's character, not from a trend menu.

The directions below are starting points for exploration, not a pick-list. The best designs often combine elements or create a direction unique to the project. Always justify why a direction fits THIS specific product.

| Direction | Character | Best for |
|-----------|-----------|----------|
| **Brutally Minimal** | Maximum whitespace, near-monochrome, Swiss precision | Productivity tools, dev tools |
| **Luxury/Refined** | Rich typography, subtle motion, premium materials feel | Finance, fashion, premium SaaS |
| **Playful/Illustrative** | Doodles, bright colors, bouncy animations, friendly copy | Consumer apps, education, kids |
| **Editorial/Magazine** | Strong grid, bold typography, dramatic imagery | Content, news, portfolios |
| **Retro-Futuristic** | Neon accents, dark backgrounds, tech-forward | Crypto, gaming, AI products |
| **Organic/Natural** | Warm tones, rounded shapes, earthy textures | Wellness, food, sustainability |
| **Neo-Brutalist** | Raw borders, bold blocks, intentional "ugly" beauty | Creative agencies, art |
| **Soft/Pastel** | Light palette, rounded corners, gentle shadows | Health, lifestyle, social |
| **Industrial/Utilitarian** | Dense info, mono fonts, functional beauty | Admin panels, data tools |
| **Art Deco/Geometric** | Symmetry, gold accents, ornamental patterns | Luxury, events, hospitality |
| **Quiet Intelligence** | Calm, precise, restrained — substance over polish | Research tools, analysis, professional work |
| **Digital Workshop** | Functional, modular, direct, hands-on feel | Creative tools, builders, makers |
| **Research Console** | Dense information, strong structure, less marketing aesthetic | Data tools, analysis platforms |

### Direction Selection Rules

- **NEVER** produce generic AI aesthetics (purple gradients on white, Inter font everywhere, cookie-cutter cards with rounded corners)
- **NEVER** pick a direction just because it "looks premium" — it must be justified by the product's character
- **Propose 2-3 directions with justification** — explain WHY each fits (or doesn't) this specific product
- **Critique each direction**: Would it look equally plausible on an unrelated product? If yes, it's too generic.
- Vary choices between generations — no two designs should converge on the same fonts/colors
- If the project has an established design system, follow it instead of inventing a new aesthetic
- Consider the platform: mobile apps tend toward cleaner/simpler; desktop tools can be denser

---

## Web Interface Guidelines (REVIEW Mode — Web only)

When reviewing **web** projects, also check ALL of the following rules from the Vercel Web Interface Guidelines. Fetch the latest version before each review:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

### Accessibility
- Icon-only buttons need `aria-label`
- Form controls need `<label>` or `aria-label`
- Interactive elements need keyboard handlers (`onKeyDown`/`onKeyUp`)
- `<button>` for actions, `<a>`/`<Link>` for navigation (not `<div onClick>`)
- Images need `alt` (or `alt=""` if decorative)
- Decorative icons need `aria-hidden="true"`
- Async updates need `aria-live="polite"`
- Use semantic HTML before ARIA
- Hierarchical headings `<h1>`–`<h6>`; include skip link
- `scroll-margin-top` on heading anchors

### Focus States
- Visible focus: `focus-visible:ring-*` or equivalent
- Never `outline-none` without focus replacement
- Use `:focus-visible` over `:focus`
- Group focus with `:focus-within` for compound controls

### Forms
- Inputs need `autocomplete` and meaningful `name`
- Correct `type` and `inputmode`
- Never block paste
- Labels clickable (`htmlFor` or wrapping)
- `spellCheck={false}` on emails, codes, usernames
- Submit button enabled until request starts; spinner during request
- Errors inline next to fields; focus first error
- Placeholders end with `…` and show example
- Warn before navigation with unsaved changes

### Animation
- Honor `prefers-reduced-motion`
- Animate `transform`/`opacity` only
- Never `transition: all` — list properties explicitly
- Animations interruptible

### Content Handling
- Text containers handle long content: `truncate`, `line-clamp-*`, or `break-words`
- Flex children need `min-w-0` for truncation
- Handle empty states
- Anticipate short, average, and very long inputs

### Images
- `<img>` needs explicit `width` and `height` (prevents CLS)
- Below-fold: `loading="lazy"`
- Above-fold critical: `priority` or `fetchpriority="high"`

### Performance
- Large lists (>50 items): virtualize
- No layout reads in render
- Prefer uncontrolled inputs
- `<link rel="preconnect">` for CDN domains
- Critical fonts: preload with `font-display: swap`

### Navigation & State
- URL reflects state (filters, tabs, pagination in query params)
- Links use `<a>`/`<Link>` (Cmd/Ctrl+click support)
- Destructive actions need confirmation or undo — never immediate

### Touch & Interaction
- `touch-action: manipulation`
- `overscroll-behavior: contain` in modals/drawers
- Disable text selection during drag
- `autoFocus` sparingly — desktop only

### Dark Mode & Theming
- `color-scheme: dark` on `<html>` for dark themes
- `<meta name="theme-color">` matches page background
- Native `<select>`: explicit `background-color` and `color`

### Locale & i18n
- Use `Intl.DateTimeFormat` not hardcoded date formats
- Use `Intl.NumberFormat` not hardcoded number formats
- Detect language via `Accept-Language` / `navigator.languages`, not IP

### Content & Copy
- Active voice
- Title Case for headings/buttons
- Numerals for counts
- Specific button labels ("Save API Key" not "Continue")
- Error messages include fix/next step

### Anti-Patterns (always flag — all platforms)
- `user-scalable=no` or `maximum-scale=1` (web)
- `onPaste` + `preventDefault` (web)
- `transition: all` (web/CSS)
- `outline-none` without `focus-visible` replacement (web)
- `<div onClick>` navigation — should be `<a>` (web)
- `<div>` / `<span>` click handlers — should be `<button>` (web)
- Images without dimensions (web)
- Large arrays `.map()` without virtualization (all platforms)
- Form inputs without labels (all platforms)
- Icon buttons without accessibility labels (all platforms)
- Hardcoded date/number formats (all platforms)
- Hardcoded colors/spacing values bypassing design tokens (all platforms)
- Missing empty/error/loading states (all platforms)
- Tap targets < 44×44px on mobile (mobile)
- Missing keyboard shortcuts for core actions (desktop)
- Ignoring Safe Areas (mobile)
- Missing `prefers-reduced-motion` / accessibility settings respect (all platforms)

### AI-Slop Anti-Patterns (always flag — design quality)
- Purple/blue/cyan gradient themes without product-specific justification
- Generic SaaS dashboard layout (sidebar + topbar + stat tiles + cards) used as default
- Cards as universal layout component without questioning if appropriate
- Glassmorphism or frosted glass effects without functional purpose
- "Lorem ipsum" or generic placeholder content ("Manage your workflow", "Track your progress")
- Design that could fit any product — no product-specific character visible
- Style words used as design direction without character specification ("modern", "clean", "premium")
- Dribbble-aesthetic: visually attractive but low information density and no product connection
- Standard color palette not derived from product identity
- Hero sections, marketing layouts, or landing page patterns used in tools/apps
- Over-rounded corners and excessive softness without character intent

---

## REVIEW Output Format

Group by file. Use `file:line` format. Terse findings. Skip preamble.

```
## src/Button.tsx

src/Button.tsx:42 — icon button missing aria-label
src/Button.tsx:18 — no visible focus state (outline-none without replacement)
src/Button.tsx:55 — animation ignores prefers-reduced-motion
src/Button.tsx:67 — transition: all → list properties explicitly

## src/Dashboard.tsx

src/Dashboard.tsx:12 — spacing inconsistent: 8px, 12px, 14px mix (use token scale)
src/Dashboard.tsx:34 — heading hierarchy skips h2 (h1 → h3)
src/Dashboard.tsx:89 — button hierarchy unclear: 3 primary-style buttons competing

## src/Card.tsx

✓ pass
```

After the file-level findings, add a **Summary** section:

```
## Summary

**Platform**: Web / Mobile (React Native) / Desktop (Electron) / ...
**Severity**: X critical / Y warning / Z info
**Design System**: ✅ Using tokens / ⚠️ Partial / ❌ No design system detected
**Top issues**: [most impactful problems]
**Recommended action**: REFACTOR spacing system + add focus states
```

---

## Self-Review Checklist (all platforms)

Before delivering any created UI, verify:

### Universal (Mobile-First Philosophy + Product-Specific)
- [ ] **Mobile-first**: Design works beautifully on a phone screen FIRST
- [ ] **Desktop adaptation**: Desktop version expands the mobile design with breathing room, NOT a separate design
- [ ] **Product-specific**: Design reflects THIS product's character — would not fit an unrelated product
- [ ] **Anti-slop verified**: No interchangeable generic elements remain unjustified
- [ ] **Component choices justified**: Standard patterns (cards, sidebars, dashboards) used only when genuinely appropriate
- [ ] Color system uses ≤ 3 hue families (neutral + brand + semantic), derived from product identity
- [ ] All spacing values from the design token scale (no arbitrary values)
- [ ] Typography hierarchy is clear (H1 > H2 > Body > Small)
- [ ] Font choice is distinctive (not system default everywhere)
- [ ] All interactive elements have appropriate states (hover/pressed/focus/disabled)
- [ ] Consistent padding and radius across similar components
- [ ] Accessibility: labels, contrast ≥ 4.5:1, keyboard/screen reader support
- [ ] Empty/error/loading states handled (skeleton screens, not spinners)
- [ ] Dark mode considered (if applicable)
- [ ] Design system tokens used — no hardcoded values
- [ ] Design is DISTINCTIVE — would not be confused with generic AI output
- [ ] **Real content used** — no "Lorem ipsum" or generic placeholder text

### Premium Feel (Non-Negotiable)
- [ ] Transitions/animations on interactive elements (subtle, purposeful)
- [ ] Loading states use skeleton screens or shimmer, not plain spinners
- [ ] Micro-interactions on key actions (button press, toggle, success)
- [ ] Generous whitespace — UI breathes, content has room
- [ ] Visual feedback on every user action (no silent interactions)
- [ ] Edge states polished (empty, error, offline, first-use)
- [ ] Icons are from a consistent library (Phosphor, Lucide, SF Symbols) — no emojis

### Web-specific
- [ ] Responsive: works on mobile, tablet, desktop viewports
- [ ] No `transition: all`, no `outline-none` without replacement
- [ ] Focus-visible rings on all interactive elements
- [ ] Semantic HTML (`<button>`, `<a>`, `<label>`, headings hierarchy)

### Mobile-specific
- [ ] Touch targets ≥ 44×44pt (iOS) / 48×48dp (Android)
- [ ] Safe Areas respected (status bar, home indicator, notch)
- [ ] Platform navigation pattern followed (Tab Bar / Bottom Nav)
- [ ] No hover-dependent interactions (touch has no hover)
- [ ] Keyboard avoidance for input fields
- [ ] Dynamic Type / font scaling respected
- [ ] Horizontal overflow controls remain usable with mouse/trackpad when the app runs in desktop/web contexts, without depending on a permanently visible scrollbar

### Desktop-specific (mobile-first optimized)
- [ ] Keyboard shortcuts for core actions (Cmd/Ctrl+K, etc.)
- [ ] Hover states added where mobile uses press
- [ ] Layout expands intelligently (side-by-side, wider content, larger touch targets → click targets)
- [ ] Still feels like a premium app, NOT like traditional desktop software (unless explicitly requested)
- [ ] Horizontal selectors/pickers support precision-pointer access (wheel/trackpad on hover, mouse drag, or chevrons) and keyboard traversal

---

## Quick Reference Cards

### Design Philosophy Quick Reference
```
ALWAYS: Mobile-first → Desktop-optimized
DEFAULT: App-like, reduced, premium, intuitive
EXCEPTION: Traditional desktop only when explicitly requested + confirmed

Tech preferences:
  Web        → Astro + TypeScript + Tailwind CSS
  Mobile App → Flutter or React Native
  Desktop    → Flutter Desktop or Wails (Go)
  Avoid      → Electron, Tauri (unless already in project)
```

### Color Quick Reference
```
LIGHT MODE                          DARK MODE
─────────────────────────────────   ──────────────────────────────────
Background:  #FAFAFA               Background:  #0A0A0A
Sidebar:     #F5F5F5 + brand tint  Sidebar:     #111111
Card:        #FFFFFF               Card:        #1A1A1A (lighter!)
Border:      #E2E8F0               Border:      #2A2A2A
Text H1:     #0F172A               Text H1:     #E5E5E5
Text body:   #334155               Text body:   #B3B3B3
Text muted:  #64748B               Text muted:  #808080
Brand:       500-600               Brand:       300-400
```

### Spacing Quick Reference (Mobile-First)
```
              Mobile      Desktop (expanded)
0.25rem (4px)  icon↔text    icon↔text
0.5rem  (8px)  tight group  tight group
0.75rem(12px)  small pad    small pad
1rem   (16px)  default gap  default gap
1.5rem (24px)  group sep    group sep
2rem   (32px)  section pad  section pad
3rem   (48px)  large gaps   content margins
4rem   (64px)  hero areas   hero areas + side margins

Mobile margin: 16-20px
Desktop margin: 32-64px (same proportions, more room)
```

### Typography Quick Reference
```
         Mobile (base)    Desktop (scaled up slightly)
H1:      28-34pt          2.25-3rem
H2:      22-28pt          1.5-2rem
H3:      17-20pt          1.25-1.5rem
Body:    17pt / 16sp      1rem (16px)
Small:   15pt / 14sp      0.875rem
```

### Premium Feel Quick Reference
```
✨ WHAT MAKES IT FEEL PREMIUM:
  → Product-specific character — design feels like it could ONLY be this product
  → Skeleton loading (not spinners)
  → Smooth transitions on state changes (200-300ms ease-out)
  → Micro-interactions on buttons/toggles/cards
  → Generous whitespace — let content breathe
  → Subtle shadows for depth, not hard borders
  → Consistent icon library (not mixed styles)
  → Polished edge states (empty, error, offline, first-use)
  → Typography with personality (not Inter/Roboto everywhere)
  → Real, product-specific content throughout

🚫 WHAT MAKES IT FEEL CHEAP / GENERIC (AI-SLOP):
  → Instant state changes (no transitions)
  → Plain text "Loading..."
  → Cramped layouts with no breathing room
  → Mixed icon styles or emoji as icons
  → Missing states (empty screens, unhandled errors)
  → Default system fonts with no hierarchy
  → Hard borders everywhere instead of subtle shadows
  → Purple/blue gradients on white (generic AI aesthetic)
  → Interchangeable card grids as universal layout
  → Generic SaaS dashboard aesthetic without product connection
  → Glassmorphism/frosted glass without functional reason
  → Placeholder content ("Lorem ipsum", "Track your progress")
  → Design that would fit 5 unrelated products equally well
```
