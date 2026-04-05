---
name: appstore-screenshots
description: >
  MUST USE for creating app store screenshots for ANY app (iOS, Android, Desktop, Web).
  Invoke this skill whenever the user mentions app store screenshots, store listings,
  screenshot generation, ASO visuals, App Store Optimization screenshots, Play Store
  screenshots, Microsoft Store screenshots, or wants to create promotional images for
  their app. Also trigger when users say "generate store screens", "create app previews",
  "store listing images", "screenshot automation", or any variation of creating visual
  marketing assets for app distribution platforms. Works for Flutter, React Native,
  SwiftUI, native iOS/Android, Electron, web apps, and any other framework.
  Handles Apple App Store, Google Play Store, and Microsoft Store formats.
  Also triggers on German: 'App Store Screenshots erstellen', 'Store Bilder generieren',
  'Screenshots für den App Store', 'Play Store Screenshots'.
---

# App Store Screenshot Generator

Generate high-converting app store screenshots that follow a proven formula for
driving downloads. This skill combines a conversion-optimized headline formula with
an automated panorama-slice rendering pipeline (HTML → Playwright → Sharp).

## Why This Matters

Most indie developers treat screenshots as an afterthought — they list features
instead of selling benefits. This skill applies a formula that has been proven to
increase download conversion:

**The #1 mistake:** "Screen 1: Feature A. Screen 2: Feature B. Screen 3: Feature C."
That's boring. Nobody reads it. Nobody downloads.

**What works:** Tell users WHY they should care. Signal that this is the app that
solves their problem. Do it fast — you have 2 seconds while they scroll.

## Prerequisites

The generation pipeline requires Node.js with two packages:

```bash
npm install playwright sharp
npx playwright install chromium
```

If the project already has a `tools/` directory with these dependencies, use that.
Otherwise, create a temporary working directory.

## The Workflow

Follow these 6 phases in order. Each phase builds on the previous one.

---

### Phase 1: App Analysis

Before touching any design, understand the app deeply. This phase is non-negotiable.

**1a. Scan the codebase:**
- App name and icon/logo
- Primary color palette (from theme, CSS variables, or design tokens)
- Main screens/features (from router config, navigation, screen files)
- Target platforms (iOS, Android, Desktop, Web)
- Supported languages/locales

**1b. Ask the user 3 critical questions:**

Read `references/headline-formula.md` for the full framework, then ask:

1. **Who is your target user?** (Be specific: "busy parents", not "everyone")
2. **What is the #1 reason someone downloads this app?** (One sentence max)
3. **What transformation does your app deliver?**
   - NOT what it does → what it makes the user BECOME
   - Habit tracker → "Makes you better every single day"
   - Recipe app → "Makes cooking at home effortless"
   - Budget app → "Shows you exactly what's left to spend"

**1c. Identify the key screens to showcase:**
- Scan the app's screens/routes
- Recommend 5-7 screens that best represent the core value
- Each screen should map to one benefit headline

**Output:** A brief analysis summary shared with the user for confirmation.

---

### Phase 2: Headline Generation

Read `references/headline-formula.md` for the complete formula with examples.

**The Verb+Benefit Formula:**

Every screenshot headline follows this pattern:
```
[ACTION VERB] + [USER BENEFIT]
```

Examples:
- ❌ "Monthly budget overview" (feature description)
- ✅ "Plan your month at a glance" (verb + benefit)
- ❌ "Savings goal tracking feature"
- ✅ "Reach your savings goals"

**Rules:**
1. Start each headline with a single, strong action verb
2. The verb is big, bold, and impossible to miss
3. Follow with the benefit — what the user GETS, not what the app DOES
4. Headlines must work when scanning across all screenshots quickly
5. Use `<em>` tags around 1-2 key words for accent coloring

**Generate 5-8 headlines** (one per screenshot), then present to user:

```
Here are the headlines I'd recommend for your store screenshots:

1. 🏠 HERO: "Your Money. Your Plan." — establishes the transformation
2. 📊 MONTH: "Plan your month at a glance" — verb: plan, benefit: clarity
3. 📅 YEAR: "Plan your year ahead" — verb: plan, benefit: foresight
4. 💰 SAVINGS: "Reach your savings goals" — verb: reach, benefit: achievement
...

Do these capture your app's value? Want to adjust any?
```

Also generate a **category label** for each screen (short, ALL CAPS):
MONTHLY PLANNING, YEARLY OVERVIEW, SAVINGS GOALS, etc.

---

### Phase 3: Design Configuration

**3a. Color palette:**
- Extract the app's primary brand color
- Derive a complementary palette:
  - `bgDark` — deep dark background (navy/charcoal, never pure black)
  - `bgLight` — soft light background
  - `accent` — the attention-grabbing highlight color
  - `textDark` / `textLight` — text colors per theme
  - `categoryColor` — color for the category label (usually = accent)

**3b. Decide the screen sequence:**

Proven order that converts:
1. **Hero** — Brand + tagline + trust signals (no app screenshot)
2. **Core feature 1** — The #1 reason to download
3. **Core feature 2** — Second strongest benefit
4. **Core feature 3** — Third benefit
5. **Secondary feature** — Nice-to-have
6. **Detail/depth screen** — Shows the app has substance
7. **Trust/closing** — Privacy, security, social proof (no app screenshot)

**3c. Theme per screen:**
Alternate between dark and light backgrounds to create visual rhythm.
Hero and Trust screens are typically dark.

**3d. Generate the config file:**

Create a `config.js` following the structure in `references/template-architecture.md`.
This config drives the entire generation pipeline.

---

### Phase 4: App Screenshot Capture

The pipeline needs actual screenshots of the app. Guide the user:

**Option A: Integration test (recommended for Flutter/mobile):**
```dart
// Use tester.binding.renderViews to capture at exact dimensions
```

**Option B: Manual screenshots:**
- Take screenshots at the highest resolution available
- Crop to the app content area (no OS chrome)
- Save as PNG with transparent or solid background

**Option C: Existing screenshots:**
- If the project already has screenshots, use those
- Check `website/public/screenshots/` or similar paths

For each headline, recommend which app screen best represents it.
Present recommendations to the user:

```
Screenshot mapping:
  "Plan your month at a glance" → Monthly overview screen (dark mode)
  "Plan your year ahead" → Year grid screen (light mode)
  "Reach your savings goals" → Savings goals list (dark mode)
```

---

### Phase 5: Generation

Read `references/template-architecture.md` for the full technical details.

**5a. Generate HTML templates:**

Use the bundled templates in `assets/` as starting points:
- `assets/template-mobile.html` — for iPhone / Google Play
- `assets/template-desktop.html` — for Microsoft Store

Customize them with the config from Phase 3 (colors, fonts, layout).

**5b. Generate the config.js:**

The config must define:
- `STORE_SIZES` — target dimensions per store
- `SCREENS` — array of screen definitions (id, headline, subtitle, screenshot paths, theme)
- `DESIGN` — color tokens, font family, phone mockup styling
- `ASSET_PATHS` — paths to logo, mascot/icon, screenshots

**5c. Run the generator:**

Execute the generation script from `scripts/generate-screenshots.cjs`:

```bash
node <skill-path>/scripts/generate-screenshots.cjs \
  --config <path-to-config.js> \
  --template-mobile <path-to-template.html> \
  --template-desktop <path-to-desktop-template.html> \
  --output <output-directory> \
  --languages de,en
```

Or, if the project already has its own generator (like HellerIO's
`tools/appstore-screens/generate.cjs`), prefer using that instead of the
bundled one. The skill's generator is a fallback for projects without
existing tooling.

**5d. Output structure:**

```
output/
├── panorama/          — Full panorama images (debug/preview)
├── {lang}/
│   ├── iphone_6_9/    — Apple App Store (1320×2868)
│   ├── play_phone/    — Google Play (1080×1920)
│   └── microsoft/     — Microsoft Store (1920×1080)
```

Read `references/store-requirements.md` for exact size requirements.

---

### Phase 6: Quality Assessment

After generation, assess the screenshots as a set:

**6a. Visual checklist:**
- [ ] Headlines readable at thumbnail size (App Store search results)
- [ ] Action verb is the largest text element on each screen
- [ ] Color contrast meets WCAG AA (4.5:1 for body text)
- [ ] Screenshots work as a cohesive set (consistent style)
- [ ] Alternating dark/light creates visual rhythm
- [ ] Phone mockups are realistic (proper bezels, shadows)
- [ ] Hero screen immediately communicates app purpose
- [ ] Trust screen builds confidence (privacy, ratings, compliance)

**6b. Conversion checklist:**
- [ ] Can a user understand the app's value by scanning only the headlines?
- [ ] Does the verb+benefit pattern hold across all screenshots?
- [ ] Is the #1 benefit on screen 2 (first feature screen)?
- [ ] Would YOU download this app based on these screenshots?

**6c. Store compliance:**
Read `references/store-requirements.md` to verify:
- [ ] Dimensions match store requirements exactly
- [ ] No text cut off at edges
- [ ] No misleading UI elements
- [ ] File size under limits

**6d. Present results to user:**
Show each generated screenshot with its headline.
Highlight any issues found.
Offer to regenerate with adjustments.

---

## Bundled References

Read these when you need deeper details:

| File | When to Read |
|------|-------------|
| `references/headline-formula.md` | Phase 2 — headline generation |
| `references/store-requirements.md` | Phase 5-6 — generation & compliance |
| `references/template-architecture.md` | Phase 5 — understanding the pipeline |

## Bundled Assets

| File | Purpose |
|------|---------|
| `assets/template-mobile.html` | Generic mobile panorama template |
| `assets/template-desktop.html` | Generic desktop panorama template |
| `scripts/generate-screenshots.cjs` | Universal screenshot generator |

## Tips for Great Screenshots

1. **Verb first, always.** "Track your habits" not "Habit tracking feature"
2. **Transformation > features.** Sell the after-state, not the tool.
3. **Color matters.** A vibrant accent color that complements your app's palette grabs attention in the store.
4. **Rhythm.** Alternate dark/light backgrounds. Don't use the same background 7 times.
5. **The 2-second test.** If someone scrolling can't understand your app in 2 seconds of looking at the screenshots, rethink the headlines.
6. **Don't crowd.** Each screenshot = ONE message. One verb, one benefit, one supporting visual.
7. **Trust seals work.** Privacy badges, star ratings, "Free to start" — put them on the hero or closing screen.
8. **Localize everything.** Headlines, subtitles, screenshots, badges — all must be in the target language.
