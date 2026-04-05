# Template Architecture: Panorama-Slice Pipeline

## Overview

The screenshot generation uses a **panorama-slice** architecture:

1. Render one wide HTML canvas containing ALL screenshots side-by-side
2. Take a single Playwright screenshot of the entire panorama
3. Use Sharp to slice the panorama into individual screenshots
4. Resize for different stores

This approach ensures pixel-perfect consistency across all screenshots because
they're rendered in a single DOM context with shared CSS.

## Why Panorama-Slice?

**Alternative 1: Individual page renders.**
Render each screenshot as a separate HTML page. Problem: inconsistencies
between renders (font loading timing, CSS variable inheritance, gradient
alignment at edges).

**Alternative 2: Panorama-slice (what we use).**
One render, one screenshot, then slice. Benefits:
- 100% consistent typography, colors, and spacing
- Gradient backgrounds can flow across screen boundaries
- Phone mockups can span two screens (bridge phones)
- Single Playwright launch = faster generation
- Debug by opening the panorama in a browser

## The Config File

The config drives everything. Structure:

```javascript
module.exports = {
  // Store dimensions
  STORE_SIZES: {
    iphone_6_9: { width: 1320, height: 2868 },
    play_phone: { width: 1080, height: 1920 },
    microsoft: { width: 1920, height: 1080, landscape: true },
  },

  // Screen definitions
  SCREENS: [
    {
      id: 'hero',                    // URL-safe identifier
      category: { de: 'WILLKOMMEN', en: 'WELCOME' },
      headline: {
        de: 'Dein <em>Geld</em>.\nDein <em>Plan</em>.',
        en: 'Your <em>Money</em>.\nYour <em>Plan</em>.',
      },
      subtitle: {
        de: 'Plane Einnahmen, Ausgaben & Sparziele.',
        en: 'Plan income, expenses & savings goals.',
      },
      screenshot: null,              // null = no phone mockup (hero/trust)
      theme: 'dark',                 // 'dark' or 'light' background
      showMascot: true,              // optional: show mascot/icon
      showBadges: true,              // optional: show pill badges
      badges: {
        de: ['Kostenlos starten', 'DSGVO-konform'],
        en: ['Free to start', 'Privacy-first'],
      },
    },
    {
      id: 'feature-1',
      category: { de: 'HAUPTFEATURE', en: 'KEY FEATURE' },
      headline: { de: 'Headline hier', en: 'Headline here' },
      subtitle: { de: 'Untertitel', en: 'Subtitle' },
      screenshot: {
        de: { dark: 'path/to/dark.png', light: 'path/to/light.png' },
        en: { dark: 'path/to/dark.png', light: 'path/to/light.png' },
      },
      theme: 'dark',
    },
    // ... more screens
  ],

  // Desktop-specific screens (for Microsoft Store)
  DESKTOP_SCREENS: [
    { id: 'hero', mobileIndex: 0 },
    { id: 'feature-1', mobileIndex: 1, desktopScreenshot: 'desktop-feature1.png' },
    // ...
  ],

  // Design tokens
  DESIGN: {
    colors: {
      bgDark: '#0F1A24',
      bgLight: '#F0F9F5',
      accent: '#5EEAD4',
      accentGlow: 'rgba(94, 234, 212, 0.12)',
      textDark: '#E2E8F0',
      textLight: '#142B3D',
      textMuted: 'rgba(226, 232, 240, 0.5)',
      categoryColor: '#5EEAD4',
    },
    fonts: {
      family: "'Inter', system-ui, sans-serif",
      importUrl: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap',
    },
    phone: {
      cornerRadius: 58,
      bezelColor: '#1a2b3c',
      shadowBlur: 60,
      shadowColor: 'rgba(0, 0, 0, 0.35)',
    },
  },

  // Asset paths
  ASSET_PATHS: {
    logo: '/path/to/logo.png',
    mascot: '/path/to/mascot.png',
    screenshotBase: '/path/to/screenshots/',
  },
};
```

## The HTML Template

### Mobile Template Structure

The mobile template is a flex container where each "screen" is exactly
`SCREEN_WIDTH × SCREEN_HEIGHT`:

```
┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│  HERO   │ SCREEN1 │ SCREEN2 │ SCREEN3 │ SCREEN4 │ SCREEN5 │  TRUST  │
│ 1320px  │ 1320px  │ 1320px  │ 1320px  │ 1320px  │ 1320px  │ 1320px  │
│         │         │         │         │         │         │         │
│  2868px │         │         │         │         │         │         │
└─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
          Total: 9240px × 2868px
```

### Key CSS Patterns

**Screen container:**
```css
.screen {
  width: var(--screen-w);
  height: var(--screen-h);
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}
```

**Background themes:**
```css
.bg-dark {
  background: linear-gradient(180deg,
    var(--bg-dark) 0%,
    color-mix(in srgb, var(--bg-dark), var(--accent) 4%) 100%);
}
.bg-light {
  background: linear-gradient(180deg,
    var(--bg-light) 0%,
    color-mix(in srgb, var(--bg-light), var(--accent) 8%) 100%);
}
```

**Phone mockup:**
```css
.phone {
  position: absolute;
  border-radius: var(--phone-radius);
  background: var(--bezel-color);
  box-shadow: 0 var(--shadow-blur) calc(var(--shadow-blur) * 2) var(--shadow-color);
  overflow: hidden;
  padding: 12px;
}
.phone img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: calc(var(--phone-radius) - 12px);
}
```

**Typography:**
```css
.category {
  font-size: 28px;
  font-weight: 800;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--accent);
}
.headline {
  font-size: 82px;
  font-weight: 900;
  line-height: 1.05;
  letter-spacing: -0.02em;
}
.headline em {
  font-style: normal;
  color: var(--accent);
}
.subtitle {
  font-size: 36px;
  font-weight: 400;
  line-height: 1.4;
  opacity: 0.7;
}
```

### Phone Positioning

Phones are positioned absolutely within the panorama (not inside individual
screens). This allows them to span screen boundaries for visual continuity.

Each phone typically:
- Width: ~920px (70% of screen width)
- Height: ~2000px
- Slight rotation: rotate(3-6deg) for visual interest
- Centered vertically with top offset ~640-680px
- Spaced at screen-width intervals

### Desktop Template Structure

For Microsoft Store (landscape format):

```
┌──────────────────┬──────────────────┬──────────────────┐
│      HERO        │     SCREEN1      │     SCREEN2      │  ...
│    1920×1080     │    1920×1080     │    1920×1080     │
└──────────────────┴──────────────────┴──────────────────┘
```

Each desktop screen uses a two-column layout:
- Left (42%): Category + Headline + Subtitle
- Right (58%): Desktop window mockup + iPhone teaser

The desktop window mockup includes:
- Fake titlebar (36px) with red/yellow/green dots
- Content area showing the desktop app screenshot
- Realistic drop shadow
- Optional iPhone teaser floating beside it (rotated 3deg)

## The Generation Script

### Core Flow

```javascript
async function main() {
  // 1. Load config
  const config = require(configPath);

  // 2. Generate mobile screenshots
  for (const lang of languages) {
    // Launch Playwright with panorama-sized viewport
    const browser = await chromium.launch();
    const page = await browser.newPage({
      viewport: {
        width: SCREEN_W * NUM_SCREENS,
        height: SCREEN_H
      },
      deviceScaleFactor: 1,
    });

    // Navigate to template
    await page.goto(templateUrl);

    // Inject localized content via page.evaluate()
    await page.evaluate(injectContent, { config, lang });

    // Wait for all images to load
    await page.waitForFunction(allImagesLoaded);

    // Screenshot the panorama
    await page.screenshot({ path: panoramaPath });

    // Slice into individual screens with Sharp
    for (let i = 0; i < numScreens; i++) {
      await sharp(panoramaPath)
        .extract({
          left: i * SCREEN_W,
          top: 0,
          width: SCREEN_W,
          height: SCREEN_H,
        })
        .toFile(outputPath);
    }

    await browser.close();
  }

  // 3. Resize for stores
  // Google Play: 1320×2868 → 1080×1920 (sharp cover/top)
  for (const file of iphoneFiles) {
    await sharp(file)
      .resize(1080, 1920, { fit: 'cover', position: 'top' })
      .toFile(playStorePath);
  }

  // 4. Generate desktop screenshots (similar flow, desktop template)
  // 5. Copy to fastlane directories (if applicable)
}
```

### Critical Details

- `deviceScaleFactor: 1` — must be 1 for exact pixel match with store requirements
- Use `file:///` URLs for local assets (with proper Windows path conversion)
- Wait for `networkidle` AND explicit image load check before screenshotting
- Add 500ms extra wait after images load (font rendering settle time)
- Use `sharp` for slicing (not Playwright's element screenshot — more reliable)
- Google Play resize uses `position: 'top'` to keep headlines visible after crop

## Customization Points

When adapting the template for a new app:

1. **Colors:** Change CSS custom properties (6-8 color values)
2. **Font:** Change the Google Fonts import URL and family
3. **Phone style:** Adjust corner radius, bezel color, shadow
4. **Layout:** Adjust text position, phone position, badge placement
5. **Content:** Update headlines, subtitles, category labels, badges
6. **Screenshots:** Replace phone screenshots with new app's screens
7. **Logo/Mascot:** Replace brand assets

Everything else (the panorama structure, slicing logic, store resizing)
stays the same across all apps.
