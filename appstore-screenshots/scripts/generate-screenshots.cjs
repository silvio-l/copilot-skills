#!/usr/bin/env node
/**
 * Universal App Store Screenshot Generator
 *
 * Renders HTML panorama templates → slices into individual screens → resizes for all stores.
 *
 * Usage:
 *   node generate-screenshots.cjs --config <config.js> [options]
 *
 * Options:
 *   --config <path>            Path to config.js (required)
 *   --template-mobile <path>   Path to mobile HTML template (default: bundled)
 *   --template-desktop <path>  Path to desktop HTML template (default: bundled)
 *   --output <path>            Output directory (default: ./output)
 *   --languages <langs>        Comma-separated languages (default: from config or "en")
 *   --skip-desktop             Skip desktop screenshot generation
 *   --skip-resize              Skip Google Play resizing
 *   --skip-fastlane            Skip fastlane copy
 *   --fastlane-dir <path>      Fastlane metadata directory
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// ─── Parse CLI Args ─────────────────────────────────────────────
const args = process.argv.slice(2);
function getArg(name, defaultVal) {
  const idx = args.indexOf(`--${name}`);
  if (idx === -1) return defaultVal;
  return args[idx + 1] || defaultVal;
}
function hasFlag(name) {
  return args.includes(`--${name}`);
}

const CONFIG_PATH = getArg('config', null);
if (!CONFIG_PATH) {
  console.error('❌ --config <path> is required');
  process.exit(1);
}

const SKILL_DIR = path.resolve(__dirname, '..');
const DEFAULT_MOBILE_TEMPLATE = path.resolve(SKILL_DIR, 'assets', 'template-mobile.html');
const DEFAULT_DESKTOP_TEMPLATE = path.resolve(SKILL_DIR, 'assets', 'template-desktop.html');

const MOBILE_TEMPLATE = path.resolve(getArg('template-mobile', DEFAULT_MOBILE_TEMPLATE));
const DESKTOP_TEMPLATE = path.resolve(getArg('template-desktop', DEFAULT_DESKTOP_TEMPLATE));
const OUTPUT_BASE = path.resolve(getArg('output', './appstore-screenshots-output'));
const SKIP_DESKTOP = hasFlag('skip-desktop');
const SKIP_RESIZE = hasFlag('skip-resize');
const SKIP_FASTLANE = hasFlag('skip-fastlane');
const FASTLANE_DIR = getArg('fastlane-dir', null);

// ─── Load Config ────────────────────────────────────────────────
const config = require(path.resolve(CONFIG_PATH));
const {
  STORE_SIZES = {
    iphone_6_9: { width: 1320, height: 2868 },
    play_phone: { width: 1080, height: 1920 },
    microsoft: { width: 1920, height: 1080, landscape: true },
  },
  SCREENS = [],
  DESKTOP_SCREENS = [],
  DESIGN = {},
  ASSET_PATHS = {},
  ICONS = {},
} = config;

const LANGUAGES = getArg('languages', config.LANGUAGES?.join(',') || 'en').split(',');
const SCREEN_W = STORE_SIZES.iphone_6_9.width;
const SCREEN_H = STORE_SIZES.iphone_6_9.height;
const NUM_SCREENS = SCREENS.length;

// ─── Utilities ──────────────────────────────────────────────────
function fileUrl(p) {
  return 'file:///' + path.resolve(p).replace(/\\/g, '/');
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function cleanDir(dir) {
  if (fs.existsSync(dir)) {
    for (const file of fs.readdirSync(dir).filter(f => f.endsWith('.png'))) {
      fs.unlinkSync(path.join(dir, file));
    }
  }
}

// ─── Generate Mobile Screenshots ────────────────────────────────
async function generateMobileScreenshots(lang) {
  console.log(`\n🎨 Generating ${lang.toUpperCase()} mobile screenshots...`);

  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: SCREEN_W * NUM_SCREENS, height: SCREEN_H },
    deviceScaleFactor: 1,
  });

  await page.goto(fileUrl(MOBILE_TEMPLATE), { waitUntil: 'networkidle' });

  // Inject CSS custom properties from config
  if (DESIGN.colors || DESIGN.fonts) {
    await page.evaluate((design) => {
      const root = document.documentElement;
      if (design.colors) {
        const colorMap = {
          bgDark: '--bg-dark', bgLight: '--bg-light',
          accent: '--accent', accentGlow: '--accent-glow',
          textDark: '--text-dark', textLight: '--text-light',
          textMuted: '--text-muted', textMutedLight: '--text-muted-light',
          categoryColor: '--category-color',
        };
        for (const [key, prop] of Object.entries(colorMap)) {
          if (design.colors[key]) root.style.setProperty(prop, design.colors[key]);
        }
      }
      if (design.fonts?.family) {
        root.style.setProperty('--font-family', design.fonts.family);
      }
    }, DESIGN);
  }

  // Inject content for each screen
  await page.evaluate(
    (args) => {
      const { screens, lang, assets, icons } = args;

      // Set logo and mascot
      const heroLogo = document.getElementById('hero-logo');
      if (heroLogo && assets.logo) heroLogo.src = assets.logo;
      const heroMascot = document.getElementById('hero-mascot');
      if (heroMascot && assets.mascot) heroMascot.src = assets.mascot;
      const trustMascot = document.getElementById('trust-mascot');
      if (trustMascot && assets.mascot) trustMascot.src = assets.mascot;
      const watermark = document.getElementById('mascot-watermark');
      if (watermark && assets.mascot) watermark.src = assets.mascot;

      screens.forEach((screen, i) => {
        // Category
        const cat = document.getElementById(`cat-${i}`);
        if (cat && screen.category) {
          cat.textContent = typeof screen.category === 'object' ? screen.category[lang] || '' : screen.category;
        }

        // Headline (supports <em> for accent)
        const hl = document.getElementById(`hl-${i}`);
        if (hl && screen.headline) {
          const text = typeof screen.headline === 'object' ? screen.headline[lang] || '' : screen.headline;
          hl.innerHTML = text.replace(/\n/g, '<br>');
        }

        // Subtitle
        const sub = document.getElementById(`sub-${i}`);
        if (sub && screen.subtitle) {
          const text = typeof screen.subtitle === 'object' ? screen.subtitle[lang] || '' : screen.subtitle;
          sub.innerHTML = text.replace(/\n/g, '<br>');
        }

        // Badges
        if (screen.showBadges && screen.badges) {
          const container = document.getElementById(`badges-${i}`);
          if (container) {
            const badgeList = typeof screen.badges === 'object' && !Array.isArray(screen.badges)
              ? screen.badges[lang] || [] : screen.badges;
            container.innerHTML = badgeList
              .map(b => `<span class="badge">${b}</span>`)
              .join('');
          }
        }

        // Trust items
        if (screen.showTrustBadges && screen.trustItems) {
          const list = document.getElementById('trust-list');
          if (list) {
            const items = Array.isArray(screen.trustItems)
              ? screen.trustItems : (screen.trustItems[lang] || []);
            list.innerHTML = items
              .map(item => `<div class="trust-item">
                <div class="trust-icon">${icons[item.icon] || ''}</div>
                <span>${item.text}</span>
              </div>`)
              .join('');
          }
        }
      });

      // Phone screenshots
      for (let i = 1; i <= 5; i++) {
        const screen = screens[i];
        if (!screen || !screen.screenshot) continue;
        const theme = screen.theme || 'dark';
        const ssData = typeof screen.screenshot === 'object' && screen.screenshot[lang]
          ? screen.screenshot[lang] : screen.screenshot;
        const src = typeof ssData === 'object' ? (ssData[theme] || ssData.dark || '') : ssData;
        const el = document.getElementById(`phone-${i}-img`);
        if (el && src) {
          el.src = (assets.screenshotBase || '') + '/' + src;
        }
      }
    },
    {
      screens: SCREENS,
      lang,
      assets: {
        logo: ASSET_PATHS.logo ? fileUrl(ASSET_PATHS.logo) : '',
        mascot: ASSET_PATHS.mascot ? fileUrl(ASSET_PATHS.mascot) : '',
        screenshotBase: ASSET_PATHS.screenshotBase ? fileUrl(ASSET_PATHS.screenshotBase) : '',
      },
      icons: ICONS,
    }
  );

  // Wait for images
  await page.waitForFunction(() => {
    const images = document.querySelectorAll('img[src]:not([src=""])');
    return Array.from(images).every(img => img.complete && img.naturalWidth > 0);
  }, { timeout: 15000 }).catch(() => {
    console.warn('⚠️  Some images may not have loaded');
  });
  await page.waitForTimeout(500);

  // Screenshot panorama
  const panoramaDir = path.join(OUTPUT_BASE, 'panorama');
  ensureDir(panoramaDir);
  const panoramaPath = path.join(panoramaDir, `panorama-${lang}.png`);
  await page.screenshot({ path: panoramaPath, type: 'png' });
  console.log(`  📸 Panorama: panorama-${lang}.png`);

  // Slice into individual screens
  const sharp = require('sharp');
  const iphoneDir = path.join(OUTPUT_BASE, lang, 'iphone_6_9');
  ensureDir(iphoneDir);
  cleanDir(iphoneDir);

  for (let i = 0; i < NUM_SCREENS; i++) {
    const num = String(i + 1).padStart(2, '0');
    const id = SCREENS[i].id;
    const outPath = path.join(iphoneDir, `${num}_${id}.png`);
    await sharp(panoramaPath)
      .extract({ left: i * SCREEN_W, top: 0, width: SCREEN_W, height: SCREEN_H })
      .toFile(outPath);
    console.log(`  📱 iPhone 6.9": ${num}_${id}.png`);
  }

  await browser.close();
  console.log(`✅ ${lang.toUpperCase()} mobile screenshots done!`);
}

// ─── Resize for Google Play ─────────────────────────────────────
async function resizeForStores() {
  if (SKIP_RESIZE) return;
  console.log('\n📐 Resizing for Google Play...');

  const sharp = require('sharp');
  for (const lang of LANGUAGES) {
    const iphoneDir = path.join(OUTPUT_BASE, lang, 'iphone_6_9');
    if (!fs.existsSync(iphoneDir)) continue;

    const files = fs.readdirSync(iphoneDir).filter(f => f.endsWith('.png'));
    const playDir = path.join(OUTPUT_BASE, lang, 'play_phone');
    ensureDir(playDir);
    cleanDir(playDir);

    for (const file of files) {
      await sharp(path.join(iphoneDir, file))
        .resize(STORE_SIZES.play_phone.width, STORE_SIZES.play_phone.height, {
          fit: 'cover',
          position: 'top',
        })
        .png()
        .toFile(path.join(playDir, file));
    }
    console.log(`  📱 Google Play (${lang}): ${files.length} screens`);
  }
}

// ─── Generate Desktop Screenshots ───────────────────────────────
async function generateDesktopScreenshots(lang) {
  if (SKIP_DESKTOP || DESKTOP_SCREENS.length === 0) return;

  console.log(`\n🖥️  Generating ${lang.toUpperCase()} desktop screenshots...`);

  const NUM_DESKTOP = DESKTOP_SCREENS.length;
  const MS_W = STORE_SIZES.microsoft.width;
  const MS_H = STORE_SIZES.microsoft.height;

  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: MS_W * NUM_DESKTOP, height: MS_H },
    deviceScaleFactor: 1,
  });

  await page.goto(fileUrl(DESKTOP_TEMPLATE), { waitUntil: 'networkidle' });

  // Inject CSS custom properties
  if (DESIGN.colors || DESIGN.fonts) {
    await page.evaluate((design) => {
      const root = document.documentElement;
      if (design.colors) {
        const colorMap = {
          bgDark: '--bg-dark', bgLight: '--bg-light',
          accent: '--accent', accentGlow: '--accent-glow',
          textDark: '--text-dark', textLight: '--text-light',
          textMuted: '--text-muted', textMutedLight: '--text-muted-light',
          categoryColor: '--category-color',
        };
        for (const [key, prop] of Object.entries(colorMap)) {
          if (design.colors[key]) root.style.setProperty(prop, design.colors[key]);
        }
      }
      if (design.fonts?.family) {
        root.style.setProperty('--font-family', design.fonts.family);
      }
    }, DESIGN);
  }

  // Inject desktop content
  await page.evaluate(
    (args) => {
      const { desktopScreens, mobileScreens, lang, assets, icons } = args;

      const heroLogo = document.getElementById('hero-logo');
      if (heroLogo && assets.logo) heroLogo.src = assets.logo;
      const heroMascot = document.getElementById('hero-mascot');
      if (heroMascot && assets.mascot) heroMascot.src = assets.mascot;
      const trustMascot = document.getElementById('trust-mascot');
      if (trustMascot && assets.mascot) trustMascot.src = assets.mascot;

      desktopScreens.forEach((ds, i) => {
        const ms = mobileScreens[ds.mobileIndex];
        if (!ms) return;

        const cat = document.getElementById(`cat-${i}`);
        if (cat) cat.textContent = typeof ms.category === 'object' ? ms.category[lang] || '' : ms.category;
        const hl = document.getElementById(`hl-${i}`);
        if (hl) {
          const text = typeof ms.headline === 'object' ? ms.headline[lang] || '' : ms.headline;
          hl.innerHTML = text.replace(/\n/g, '<br>');
        }
        const sub = document.getElementById(`sub-${i}`);
        if (sub) {
          const text = typeof ms.subtitle === 'object' ? ms.subtitle[lang] || '' : ms.subtitle;
          sub.innerHTML = text.replace(/\n/g, '<br>');
        }

        // Desktop screenshot
        if (ds.desktopScreenshot) {
          const theme = ms.theme === 'split' ? 'dark' : (ms.theme || 'dark');
          const img = document.getElementById(`desktop-${i}`);
          if (img) img.src = `${assets.screenshotBase}/screenshots/${lang}/${theme}/${ds.desktopScreenshot}`;
          if (ds.phoneTeaser) {
            const teaser = document.getElementById(`phone-teaser-${i}`);
            if (teaser) teaser.src = `${assets.screenshotBase}/screenshots/${lang}/${theme}/${ds.phoneTeaser}`;
          }
        }

        // Badges
        if (ms.showBadges && ms.badges) {
          const container = document.getElementById(`badges-${i}`);
          if (container) {
            const list = typeof ms.badges === 'object' && !Array.isArray(ms.badges)
              ? ms.badges[lang] || [] : ms.badges;
            container.innerHTML = list.map(b => `<span class="badge">${b}</span>`).join('');
          }
        }

        // Trust items
        if (ms.showTrustBadges && ms.trustItems) {
          const list = document.getElementById('trust-list');
          if (list) {
            const items = Array.isArray(ms.trustItems) ? ms.trustItems : (ms.trustItems[lang] || []);
            list.innerHTML = items
              .map(item => `<div class="trust-item">
                <div class="trust-icon">${icons[item.icon] || ''}</div>
                <span>${item.text}</span>
              </div>`)
              .join('');
          }
        }
      });
    },
    {
      desktopScreens: DESKTOP_SCREENS,
      mobileScreens: SCREENS,
      lang,
      assets: {
        logo: ASSET_PATHS.logo ? fileUrl(ASSET_PATHS.logo) : '',
        mascot: ASSET_PATHS.mascot ? fileUrl(ASSET_PATHS.mascot) : '',
        screenshotBase: ASSET_PATHS.screenshotBase ? fileUrl(ASSET_PATHS.screenshotBase) : '',
      },
      icons: ICONS,
    }
  );

  // Wait for images
  await page.waitForFunction(() => {
    const images = document.querySelectorAll('img[src]:not([src=""])');
    return Array.from(images).every(img => img.complete && img.naturalWidth > 0);
  }, { timeout: 15000 }).catch(() => {
    console.warn('⚠️  Some desktop images may not have loaded');
  });
  await page.waitForTimeout(500);

  // Slice individual desktop screens
  const msDir = path.join(OUTPUT_BASE, lang, 'microsoft');
  ensureDir(msDir);
  cleanDir(msDir);

  for (let i = 0; i < NUM_DESKTOP; i++) {
    const screenEl = await page.$(`#screen-${i}`);
    if (!screenEl) continue;
    const num = String(i + 1).padStart(2, '0');
    const id = DESKTOP_SCREENS[i].id;
    await screenEl.screenshot({ path: path.join(msDir, `${num}_${id}.png`), type: 'png' });
    console.log(`  🖥️  Microsoft: ${num}_${id}.png`);
  }

  await browser.close();
  console.log(`✅ ${lang.toUpperCase()} desktop screenshots done!`);
}

// ─── Copy to Fastlane ───────────────────────────────────────────
async function copyToFastlane() {
  if (SKIP_FASTLANE || !FASTLANE_DIR) return;
  console.log('\n📁 Copying to fastlane metadata...');

  const localeMap = config.LOCALE_MAP || { en: 'en-US', de: 'de-DE' };

  for (const [lang, locale] of Object.entries(localeMap)) {
    if (!LANGUAGES.includes(lang)) continue;

    const stores = [
      { src: 'iphone_6_9', dest: 'iphone_6_9' },
      { src: 'play_phone', dest: 'play_phone' },
      { src: 'microsoft', dest: 'microsoft' },
    ];

    for (const { src, dest } of stores) {
      const srcDir = path.join(OUTPUT_BASE, lang, src);
      if (!fs.existsSync(srcDir)) continue;

      const destDir = path.join(FASTLANE_DIR, locale, 'screenshots', dest);
      ensureDir(destDir);
      const files = fs.readdirSync(srcDir).filter(f => f.endsWith('.png'));
      for (const file of files) {
        fs.copyFileSync(path.join(srcDir, file), path.join(destDir, file));
      }
      console.log(`  📦 ${locale}/screenshots/${dest}: ${files.length} files`);
    }
  }
}

// ─── Main ───────────────────────────────────────────────────────
(async () => {
  console.log('🚀 App Store Screenshot Generator');
  console.log(`   Screens: ${NUM_SCREENS} mobile, ${DESKTOP_SCREENS.length} desktop`);
  console.log(`   Languages: ${LANGUAGES.join(', ')}`);
  console.log(`   Output: ${OUTPUT_BASE}`);
  console.log(`   Config: ${path.resolve(CONFIG_PATH)}`);

  try {
    // Mobile screenshots
    for (const lang of LANGUAGES) {
      await generateMobileScreenshots(lang);
    }

    // Resize for Google Play
    await resizeForStores();

    // Desktop screenshots
    for (const lang of LANGUAGES) {
      await generateDesktopScreenshots(lang);
    }

    // Copy to fastlane
    await copyToFastlane();

    console.log('\n🎉 All screenshots generated successfully!');
    console.log(`\nOutput: ${OUTPUT_BASE}/`);
    for (const lang of LANGUAGES) {
      console.log(`  ${lang}/iphone_6_9/  — Apple App Store (${STORE_SIZES.iphone_6_9.width}×${STORE_SIZES.iphone_6_9.height})`);
      if (!SKIP_RESIZE) {
        console.log(`  ${lang}/play_phone/  — Google Play (${STORE_SIZES.play_phone.width}×${STORE_SIZES.play_phone.height})`);
      }
      if (!SKIP_DESKTOP && DESKTOP_SCREENS.length > 0) {
        console.log(`  ${lang}/microsoft/   — Microsoft Store (${STORE_SIZES.microsoft.width}×${STORE_SIZES.microsoft.height})`);
      }
    }
  } catch (err) {
    console.error('❌ Error:', err.message);
    console.error(err.stack);
    process.exit(1);
  }
})();
