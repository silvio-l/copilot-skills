# App Store Screenshot Requirements

Exact pixel dimensions, file formats, and submission rules for each major store.
Last verified: 2025-Q4.

## Apple App Store

### Required Device Families

Apple requires screenshots for specific device sizes. At minimum, you need
iPhone 6.9" — this covers ALL iPhone models.

| Device | Dimensions (px) | Aspect Ratio | Covers |
|--------|-----------------|--------------|--------|
| **iPhone 6.9"** | 1320 × 2868 | ~1:2.17 | All iPhones (required) |
| iPhone 6.7" | 1290 × 2796 | ~1:2.17 | Auto-scaled from 6.9" |
| iPhone 6.5" | 1284 × 2778 | ~1:2.16 | Auto-scaled from 6.9" |
| iPhone 5.5" | 1242 × 2208 | ~1:1.78 | Older iPhones (optional) |
| **iPad 13"** | 2064 × 2752 | ~1:1.33 | All iPads (required if iPad app) |
| iPad 12.9" | 2048 × 2732 | ~1:1.33 | Auto-scaled from 13" |

### Rules
- **Min 3, Max 10** screenshots per device family per locale
- **PNG or JPEG** format
- **No alpha channel** (no transparency)
- Must be **flat artwork** (no 3D device frames from Apple)
- Must accurately represent the app experience
- Text must be legible
- No pricing information in screenshots
- No references to other platforms ("Also on Android")

### Recommended Strategy
- Generate at **iPhone 6.9" (1320×2868)** — covers all iPhones
- Generate at **iPad 13" (2064×2752)** if you have an iPad app
- 7 screenshots is the sweet spot (fills the carousel without overwhelming)

---

## Google Play Store

### Required Sizes

| Type | Dimensions (px) | Aspect Ratio | Notes |
|------|-----------------|--------------|-------|
| **Phone** | 1080 × 1920 | 9:16 | Required |
| 7" Tablet | 1200 × 1920 | 5:8 | Optional |
| 10" Tablet | 1800 × 2560 | ~9:12.8 | Optional |

### Rules
- **Min 2, Max 8** screenshots per device type per locale
- **PNG or JPEG** (24-bit, no alpha)
- Each screenshot must be **16:9 or 9:16** aspect ratio
- Min dimension: 320px, Max dimension: 3840px
- **Max file size: 8MB** per image
- Must not contain mature or violent content
- Must represent actual app experience

### Recommended Strategy
- Resize iPhone 6.9" screenshots to **1080×1920** (Google Play phone)
- Use `sharp` with `fit: 'cover', position: 'top'` for aspect ratio conversion
- 7 screenshots matches Apple — same content, resized

---

## Microsoft Store

### Required Sizes

| Type | Dimensions (px) | Aspect Ratio | Notes |
|------|-----------------|--------------|-------|
| **Desktop** | 1920 × 1080 | 16:9 (landscape) | Recommended |
| Desktop alt | 2560 × 1440 | 16:9 (landscape) | Higher res option |
| Desktop alt | 3840 × 2160 | 16:9 (landscape) | 4K option |

### Rules
- **Min 1, Max 10** screenshots
- **PNG** format (recommended; JPEG also accepted)
- Must be **landscape** (16:9)
- Should show the desktop app experience (not phone UI)
- Desktop window mockup recommended for mobile-first apps
- Min dimension: 1366×768, Recommended: 1920×1080

### Recommended Strategy
- Create a **separate desktop template** with:
  - Desktop window mockup (fake titlebar with traffic light dots)
  - Phone teaser beside it (shows cross-platform)
  - Two-column layout: text left, devices right
- 5 desktop screenshots is usually sufficient

---

## Cross-Store Summary

| Store | Primary Size | Orientation | Min | Max | Format |
|-------|-------------|-------------|-----|-----|--------|
| Apple (iPhone) | 1320×2868 | Portrait | 3 | 10 | PNG/JPEG |
| Apple (iPad) | 2064×2752 | Portrait | 3 | 10 | PNG/JPEG |
| Google Play | 1080×1920 | Portrait | 2 | 8 | PNG/JPEG |
| Microsoft | 1920×1080 | Landscape | 1 | 10 | PNG |

## Generation Pipeline

### Recommended approach: Generate once, resize for all stores

1. **Render at iPhone 6.9" (1320×2868)** — highest resolution portrait
2. **Slice** panorama into individual screens
3. **Resize for Google Play** (1080×1920) using sharp cover/top
4. **Render desktop separately** (1920×1080) with desktop-specific template
5. **Copy to fastlane** directories if using fastlane for submission

### File Naming Convention

```
{NN}_{screen-id}.png

01_hero.png
02_month.png
03_year.png
04_savings.png
05_entry-form.png
06_month-detail.png
07_trust.png
```

Numbered prefix ensures correct ordering in stores.

## Localization

Each store supports localized screenshots. Generate a complete set per locale:

| Store | Locale Format | Examples |
|-------|--------------|----------|
| Apple | `{lang}-{REGION}` | `en-US`, `de-DE`, `fr-FR` |
| Google | `{lang}-{REGION}` | `en-US`, `de-DE` |
| Microsoft | `{lang}-{region}` | `en-us`, `de-de` |

### Directory structure
```
output/
├── de/
│   ├── iphone_6_9/    (7 screenshots)
│   ├── play_phone/    (7 screenshots)
│   └── microsoft/     (5 screenshots)
└── en/
    ├── iphone_6_9/
    ├── play_phone/
    └── microsoft/
```

### What to localize
- All headline text
- All subtitle text
- Category labels
- Trust badges / feature pills
- The actual app screenshots (if the app UI changes per locale)
