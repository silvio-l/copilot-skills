#!/usr/bin/env node

// scan_soc.mjs — Separation of Concerns Scanner (Cross-Platform)
//
// Scans a codebase for files that mix architectural concerns and flags
// oversized files per layer. Works on Windows, macOS, and Linux.
//
// Usage:
//   node scan_soc.mjs [repo-root] [options]
//
// Options:
//   --changed-only, -c   Only scan files with uncommitted git changes
//   --top N, -t N        Show top N results (default: 25)
//   --json, -j           Output as JSON
//   --help, -h           Show this help
//
// Exit codes:
//   0  No HIGH-severity findings (or no findings at all)
//   1  At least one HIGH-severity finding detected

import { readFileSync, readdirSync, existsSync, statSync } from 'fs';
import { join, resolve, extname, relative, sep } from 'path';
import { execSync } from 'child_process';

// ── CLI argument parsing ────────────────────────────────────────────

const argv = process.argv.slice(2);
let repoRoot = process.cwd();
let changedOnly = false;
let top = 25;
let jsonOutput = false;

for (let i = 0; i < argv.length; i++) {
  switch (argv[i]) {
    case '--help': case '-h':
      console.log(
        'Usage: node scan_soc.mjs [repo-root] [--changed-only] [--top N] [--json]\n\n' +
        'Options:\n' +
        '  --changed-only, -c   Only scan files with uncommitted git changes\n' +
        '  --top N, -t N        Show top N results (default: 25)\n' +
        '  --json, -j           Output as JSON\n' +
        '  --help, -h           Show this help\n\n' +
        'Exit codes:\n' +
        '  0  No HIGH-severity findings\n' +
        '  1  At least one HIGH-severity finding detected'
      );
      process.exit(0);
      break;
    case '--changed-only': case '-c':
      changedOnly = true;
      break;
    case '--top': case '-t':
      top = parseInt(argv[++i], 10) || 25;
      break;
    case '--json': case '-j':
      jsonOutput = true;
      break;
    default:
      if (!argv[i].startsWith('-')) repoRoot = argv[i];
      break;
  }
}

repoRoot = resolve(repoRoot);

// Validate repo root exists and is a directory
if (!existsSync(repoRoot)) {
  process.stderr.write(`Error: path does not exist: ${repoRoot}\n`);
  process.exit(2);
}
if (!statSync(repoRoot).isDirectory()) {
  process.stderr.write(`Error: path is not a directory: ${repoRoot}\n`);
  process.exit(2);
}

// ── Configuration ───────────────────────────────────────────────────

const CODE_EXTENSIONS = new Set([
  '.dart', '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs',
  '.py', '.go', '.java', '.kt', '.swift', '.rs', '.cs',
  '.cpp', '.c', '.h', '.hpp', '.php', '.rb',
  '.vue', '.svelte', '.astro',
]);

const EXCLUDED_DIRS = new Set([
  '.git', '.dart_tool', '.next', '.nuxt', '.svelte-kit',
  '__pycache__', '.venv', 'venv', '.gradle',
  'build', 'dist', 'out', 'output',
  'coverage', 'node_modules', 'Pods', 'DerivedData',
  'target', 'vendor', '.turbo', '.cache',
]);

const GENERATED_PATTERNS = [
  /\.g\.dart$/,
  /\.freezed\.dart$/,
  /app_localizations.*\.dart$/,
  /^generated_/,
  /generated_plugin_registrant/,
  /generated_plugins\.cmake/,
  /\.generated\./,
  /\.min\.js$/,
  /\.bundle\.js$/,
  /\.d\.ts$/,
];

// ── Token sets for concern detection ────────────────────────────────
// All tokens are matched case-insensitively against file content.

const UI_TOKENS = [
  // Flutter / Dart
  'package:flutter/material.dart',
  'package:flutter/widgets.dart',
  'go_router',
  'navigator.',
  'context.push',
  'context.go',
  // Apple
  'swiftui',
  'uiviewcontroller',
  'uiview',
  // Android
  'jetpack compose',
  '@composable',
  // Web — React
  'from \'react\'',
  'from "react"',
  'from \'react-dom\'',
  'from "react-dom"',
  'usestate(',
  'useeffect(',
  'createelement(',
  // Web — Vue
  '<template>',
  'v-model',
  'v-if=',
  'definecomponent',
  // Web — Svelte / Astro
  '<script>',
  // Web — Angular
  '@component(',
  'templateurl:',
  // General
  'rendertostring',
  'innerhtml',
  'document.getelementby',
  'document.queryselector',
];

const DATA_TOKENS = [
  // Dart / Flutter
  'drift', 'sqflite',
  // General SQL
  'sqlite', 'nativedatabase',
  // ORM / DB patterns
  'prisma', 'sequelize', 'typeorm', 'mongoose',
  'coredata', 'realm', 'room',
  'knex', 'drizzle',
  // Pattern tokens (broad — scored lower in general layer)
  'database', 'repository', 'dao',
  'query(', 'select(', 'insert(', 'update(', 'delete(',
  'createquerybuild', 'getrepository',
  // Python
  'sqlalchemy', 'django.db',
  // Go
  'database/sql', 'gorm.',
];

const NETWORK_TOKENS = [
  'dio', 'package:http',
  'axios', 'fetch(',
  'retrofit', 'urlsession',
  'xmlhttprequest',
  'got(', 'superagent', 'ky(',
  'alamofire', 'okhttp',
  'net/http', 'requests.get', 'requests.post',
  'httpclien', 'webclient',
];

const FILESYSTEM_TOKENS = [
  // Dart
  'file(', 'directory(',
  // Node.js
  'readfilesync', 'writefilesync',
  'readfile(', 'writefile(',
  'createreadstream', 'createwritestream',
  'fs.read', 'fs.write', 'fs.mkdir',
  // Python
  'os.path', 'pathlib',
  // General
  'process(', 'platform.',
  'stdin', 'stdout',
  'filemanager',
];

const STATE_TOKENS = [
  // Flutter
  'provider', 'consumerwidget', 'statefulwidget',
  'statenotifier', 'changenotifier',
  'bloc', 'cubit', 'setstate(',
  'riverpod',
  // React
  'usestate', 'usereducer', 'usecontext',
  'createstore', 'configurestore',
  'redux', 'zustand', 'recoil', 'jotai',
  // Vue
  'vuex', 'pinia', 'definestore',
  // Angular
  'ngrx', '@injectable',
  // General
  'mobx', 'observable',
];

// ── Layer detection ─────────────────────────────────────────────────
// Patterns require the folder name to be a complete path segment.

const LAYER_PATTERNS = [
  { layer: 'presentation', re: /(^|[/\\])(screens?|widgets?|components?|pages?|views?|ui)([/\\]|$)/i },
  { layer: 'application',  re: /(^|[/\\])(providers?|controllers?|viewmodels?|view_models?|blocs?|cubits?|notifiers?)([/\\]|$)/i },
  { layer: 'domain',       re: /(^|[/\\])(services?|usecases?|use_cases?|domain|engines?|calculators?)([/\\]|$)/i },
  { layer: 'data',         re: /(^|[/\\])(repositor(y|ies)|daos?|database|datasources?|data_sources?|stores?|persistence)([/\\]|$)/i },
  { layer: 'model',        re: /(^|[/\\])(models?|entities|dtos?|contracts|types)([/\\]|$)/i },
];

function getLayer(relativePath) {
  const normalized = relativePath.replace(/\\/g, '/');
  for (const { layer, re } of LAYER_PATTERNS) {
    if (re.test(normalized)) return layer;
  }
  return 'general';
}

// ── Size guidance per layer ─────────────────────────────────────────

const SIZE_GUIDANCE = {
  presentation: { target: 250, review: 350 },
  application:  { target: 220, review: 320 },
  domain:       { target: 200, review: 280 },
  data:         { target: 220, review: 320 },
  model:        { target: 160, review: 220 },
  general:      { target: 300, review: 450 },
};

function getFileSizeSignal(lineCount, layer) {
  const g = SIZE_GUIDANCE[layer] || SIZE_GUIDANCE.general;
  if (lineCount > g.review) {
    return {
      reason: `File exceeds size guidance for ${layer} (${lineCount} lines; target ≤ ${g.target}, hard review > ${g.review}).`,
      score: 2, target: g.target, review: g.review,
    };
  }
  if (lineCount > g.target) {
    return {
      reason: `File above preferred size for ${layer} (${lineCount} lines; target ≤ ${g.target}, hard review > ${g.review}).`,
      score: 1, target: g.target, review: g.review,
    };
  }
  return { reason: null, score: 0, target: g.target, review: g.review };
}

// ── Concern detection ───────────────────────────────────────────────

function matchesAny(contentLower, tokens) {
  return tokens.some(t => contentLower.includes(t));
}

// ── File walking ────────────────────────────────────────────────────

function walkDir(dir) {
  const results = [];
  let entries;
  try {
    entries = readdirSync(dir, { withFileTypes: true });
  } catch {
    return results;
  }
  for (const entry of entries) {
    if (EXCLUDED_DIRS.has(entry.name)) continue;
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...walkDir(full));
    } else if (entry.isFile() && CODE_EXTENSIONS.has(extname(entry.name).toLowerCase())) {
      results.push(full);
    }
  }
  return results;
}

function getChangedFiles() {
  try {
    const raw = execSync('git status --porcelain', {
      cwd: repoRoot,
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe'],
    });
    if (!raw.trim()) return [];

    const seen = new Set();
    const files = [];

    for (const line of raw.split('\n')) {
      const trimmed = line.trimEnd();
      if (trimmed.length < 4) continue;

      // git status --porcelain: XY <space> filename
      let filePath = trimmed.substring(3).trim();

      // Handle renames: "old -> new" — take the new name
      const arrow = filePath.indexOf(' -> ');
      if (arrow !== -1) filePath = filePath.substring(arrow + 4);

      if (!filePath || seen.has(filePath)) continue;
      seen.add(filePath);

      const absolute = join(repoRoot, filePath);
      if (!existsSync(absolute)) continue;
      try {
        if (statSync(absolute).isDirectory()) continue;
      } catch { continue; }
      if (!CODE_EXTENSIONS.has(extname(filePath).toLowerCase())) continue;

      files.push(absolute);
    }

    return files;
  } catch {
    process.stderr.write(
      'Warning: git not available or not a git repository. Falling back to full scan.\n'
    );
    return walkDir(repoRoot);
  }
}

// ── Analysis ────────────────────────────────────────────────────────

function isExcludedPath(relPath) {
  const segments = relPath.replace(/\\/g, '/').split('/');
  return segments.some(seg => EXCLUDED_DIRS.has(seg));
}

function isGenerated(relPath) {
  const name = relPath.split(/[/\\]/).pop();
  return GENERATED_PATTERNS.some(p => p.test(name) || p.test(relPath));
}

const SUGGESTIONS = {
  presentation: 'Push IO/business rules into providers, services, or repositories.',
  application:  'Extract orchestration helpers or move pure rules into services.',
  domain:       'Keep services pure and move UI/IO outward.',
  data:         'Keep repositories infrastructure-only and move UI outward.',
  model:        'Strip models back to data shape and lightweight invariants.',
  general:      'Split by reason-to-change and move side effects to the edge.',
};

function analyzeFile(fullPath) {
  const relPath = relative(repoRoot, fullPath);
  if (isExcludedPath(relPath)) return null;
  if (isGenerated(relPath)) return null;

  let content;
  try {
    content = readFileSync(fullPath, 'utf-8');
  } catch {
    return null;
  }
  if (!content.trim()) return null;

  // Strip trailing newline to avoid off-by-one in line count
  const normalized = content.endsWith('\n') ? content.slice(0, -1) : content;
  const lineCount = normalized.split('\n').length;
  const lower = content.toLowerCase();
  const layer = getLayer(relPath);
  const size = getFileSizeSignal(lineCount, layer);

  const reasons = [];
  let score = 0;

  const hasUi   = matchesAny(lower, UI_TOKENS);
  const hasData  = matchesAny(lower, DATA_TOKENS);
  const hasNet   = matchesAny(lower, NETWORK_TOKENS);
  const hasFs    = matchesAny(lower, FILESYSTEM_TOKENS);
  const hasState = matchesAny(lower, STATE_TOKENS);

  // Layer-specific violation scoring
  switch (layer) {
    case 'presentation':
      if (hasData) { reasons.push('Presentation file touches persistence/repository concerns.'); score += 3; }
      if (hasNet)  { reasons.push('Presentation file touches networking directly.');              score += 2; }
      if (hasFs)   { reasons.push('Presentation file touches filesystem/process concerns.');      score += 2; }
      break;
    case 'application':
      if (hasFs || hasNet) { reasons.push('Application/orchestration file mixes infrastructure concerns.'); score += 2; }
      break;
    case 'domain':
      if (hasUi)   { reasons.push('Domain/service file imports UI or navigation concerns.');  score += 3; }
      if (hasData) { reasons.push('Domain/service file depends on persistence details.');     score += 2; }
      break;
    case 'data':
      if (hasUi) { reasons.push('Data/repository file imports UI or navigation concerns.'); score += 3; }
      break;
    case 'model':
      if (hasUi || hasData || hasNet || hasFs) {
        reasons.push('Model/entity file owns runtime concerns beyond data shape.');
        score += 3;
      }
      break;
  }

  // Size scoring
  if (size.score > 0) {
    reasons.push(size.reason);
    score += size.score;
  }

  // Multi-concern penalty
  const concernCount = [hasUi, hasData, hasNet, hasFs, hasState].filter(Boolean).length;
  if (concernCount >= 3) {
    reasons.push(`File mixes multiple concern clusters (${concernCount} detected).`);
    score += 2;
  }

  // Too many top-level type declarations
  const classMatches = content.match(
    /^\s*(class|interface|enum|struct|typedef|extension|trait|protocol)\s+\w+/gm
  );
  const classCount = classMatches ? classMatches.length : 0;
  if (classCount >= 5) {
    reasons.push(`File declares many top-level types (${classCount}).`);
    score += 1;
  }

  if (score <= 0) return null;

  return {
    severity:   score >= 5 ? 'HIGH' : score >= 3 ? 'MEDIUM' : 'LOW',
    layer,
    file:       relPath.split(sep).join('/'), // normalize to forward slashes
    lines:      lineCount,
    sizeTarget: size.target,
    sizeReview: size.review,
    reasons:    reasons.join(' '),
    suggestion: SUGGESTIONS[layer] || SUGGESTIONS.general,
    score,
  };
}

// ── Main ────────────────────────────────────────────────────────────

const files = changedOnly ? getChangedFiles() : walkDir(repoRoot);
const results = files.map(analyzeFile).filter(Boolean);

results.sort((a, b) => b.score - a.score || b.lines - a.lines);
const topResults = results.slice(0, top);

const hasHigh = topResults.some(r => r.severity === 'HIGH');

if (jsonOutput) {
  console.log(JSON.stringify(topResults, null, 2));
  process.exitCode = hasHigh ? 1 : 0;
} else if (topResults.length === 0) {
  console.log('SoC scan found no obvious hotspots in the selected files.');
  process.exitCode = 0;
} else {
  console.log(`SoC scan hotspots (${topResults.length} of ${results.length} findings):\n`);
  for (const r of topResults) {
    console.log(`[${r.severity}] ${r.file} (${r.layer}, ${r.lines} lines; target ≤ ${r.sizeTarget}, hard review > ${r.sizeReview})`);
    console.log(`  Reasons: ${r.reasons}`);
    console.log(`  Suggestion: ${r.suggestion}`);
    console.log();
  }
  if (hasHigh) {
    console.log('⛔ HIGH-severity findings detected. These MUST be addressed before presenting.');
  }
  process.exitCode = hasHigh ? 1 : 0;
}
