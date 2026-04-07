from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


SKIP_DIRS = {
    ".agents",
    ".copilot",
    ".git",
    ".idea",
    ".vscode",
    ".build",
    ".dart_tool",
    ".turbo",
    ".next",
    ".nuxt",
    ".venv",
    "venv",
    "node_modules",
    "build",
    "dist",
    "coverage",
    "target",
    "vendor",
    "third_party",
    "__pycache__",
}

DIAGRAM_SUFFIXES = {".drawio", ".puml", ".plantuml", ".mmd", ".mermaid", ".uml", ".svg"}
DOCUMENTATION_SUFFIXES = {".md", ".txt", ".adoc", ".rst"}
TOOLING_ARTIFACT_NAMES = {
    "sonar-project.properties",
    "analysis_options.yaml",
    "detekt.yml",
    "detekt.yaml",
    "codeql-config.yml",
    "codeql-config.yaml",
}
TEST_ROOTS = {"test", "tests", "integration_test", "__tests__"}
ENTRYPOINT_FILENAMES = {
    "main.dart",
    "app.dart",
    "main.go",
    "main.py",
    "main.ts",
    "main.tsx",
    "main.js",
    "main.jsx",
    "server.ts",
    "server.js",
    "index.ts",
    "index.tsx",
    "index.js",
    "index.jsx",
}

LANGUAGE_BY_SUFFIX = {
    ".dart": "dart",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".js": "javascript",
    ".jsx": "jsx",
    ".py": "python",
    ".rs": "rust",
    ".go": "go",
    ".java": "java",
    ".kt": "kotlin",
    ".swift": "swift",
    ".cs": "csharp",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".c": "c",
    ".h": "c-header",
    ".hpp": "cpp-header",
    ".vue": "vue",
    ".astro": "astro",
    ".html": "html",
    ".css": "css",
    ".scss": "scss",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".md": "markdown",
}

SOURCE_LANGUAGES = {
    "dart",
    "typescript",
    "tsx",
    "javascript",
    "jsx",
    "python",
    "rust",
    "go",
    "java",
    "kotlin",
    "swift",
    "csharp",
    "cpp",
    "c",
    "vue",
    "astro",
    "html",
    "css",
    "scss",
}

WEB_ECOSYSTEMS = {"react", "next", "vue", "astro", "svelte"}
FRONTEND_ECOSYSTEMS = {"flutter"} | WEB_ECOSYSTEMS
PACKAGE_UI_ECOSYSTEMS = WEB_ECOSYSTEMS | {"react-native", "electron", "tauri"}
UI_SURFACE_ECOSYSTEMS = PACKAGE_UI_ECOSYSTEMS | {"wails"}
PLATFORM_TARGET_ORDER = ("web", "android", "ios", "windows", "macos", "linux")
PLATFORM_FAMILY_ORDER = ("web", "mobile", "desktop")
UI_HINTS = {
    "ui",
    "widget",
    "widgets",
    "screen",
    "screens",
    "page",
    "pages",
    "view",
    "views",
    "dialog",
    "dialogs",
    "theme",
    "themes",
    "component",
    "components",
    "onboarding",
    "settings",
    "landing",
    "empty_state",
    "empty",
    "sidebar",
}
PERFORMANCE_HINTS = {"perf", "performance", "benchmark", "latency", "trace", "tracing", "metrics", "throughput"}
DOC_PATTERN = re.compile(r"(adr|architecture|decision|design)", re.IGNORECASE)
SECURITY_HINTS = {"auth", "token", "secret", "oauth", "login", "password", "jwt", "supabase", "firebase", "sql", "query", "database"}
ACCESSIBILITY_HINTS = {"accessibility", "a11y", "semantics"}
LOCALIZATION_HINTS = {"l10n", "i18n", "locale", "localization", "localisation", "translations", "translation", "intl"}
DESIGN_SYSTEM_HINTS = {"theme", "themes", "tailwind", "typography", "spacing"}
SHARED_PLATFORM_UX_STANDARDS = [
    "Accessibility basics stay in scope: WCAG AA contrast, labels/semantics, keyboard or assistive-technology support where applicable.",
    "Localization stays in scope: locale-aware copy, date/number formatting, and no hardcoded single-locale assumptions.",
    "Empty, error, loading, reduced-motion, and adaptation states matter as first-class UX evidence.",
]
PLATFORM_FAMILY_EXPECTATIONS = {
    "web": [
        "Prefer semantic navigation, visible keyboard focus, responsive layout, and URL/state behavior that matches user expectations.",
        "Check browser-facing standards such as reduced motion, labels, contrast, and locale-aware formatting.",
    ],
    "mobile": [
        "Expect touch-first interaction, 44x44pt/48x48dp targets, safe areas, keyboard avoidance, and no hover-dependent UX.",
        "Check gesture/navigation fit, text scaling, permission timing, and offline/loading states when the app suggests them.",
    ],
    "desktop": [
        "Expect desktop-appropriate interaction: hover states, keyboard shortcuts, generous click targets, and clear window/context behavior.",
        "Judge whether the product is content-light or tool-heavy before penalizing denser desktop interaction patterns.",
    ],
}


def _safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def _walk_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(root).parts
        if any(part in SKIP_DIRS for part in relative_parts):
            continue
        files.append(path)
    return files


def _detect_manifests(root: Path, files: list[Path]) -> dict[str, list[str]]:
    manifests = {
        "package_json": [],
        "pubspec_yaml": [],
        "pyproject_toml": [],
        "requirements_txt": [],
        "cargo_toml": [],
        "go_mod": [],
        "pom_xml": [],
        "gradle": [],
        "wails_json": [],
        "docker": [],
        "kubernetes": [],
        "helm": [],
    }
    for file_path in files:
        name = file_path.name
        relative = str(file_path.relative_to(root))
        if name == "package.json":
            manifests["package_json"].append(relative)
        elif name == "pubspec.yaml":
            manifests["pubspec_yaml"].append(relative)
        elif name == "pyproject.toml":
            manifests["pyproject_toml"].append(relative)
        elif name == "requirements.txt":
            manifests["requirements_txt"].append(relative)
        elif name == "Cargo.toml":
            manifests["cargo_toml"].append(relative)
        elif name == "go.mod":
            manifests["go_mod"].append(relative)
        elif name == "pom.xml":
            manifests["pom_xml"].append(relative)
        elif name.endswith(".gradle") or name.endswith(".gradle.kts"):
            manifests["gradle"].append(relative)
        elif name == "wails.json":
            manifests["wails_json"].append(relative)
        elif name == "Dockerfile" or name in {"docker-compose.yml", "docker-compose.yaml"}:
            manifests["docker"].append(relative)
        elif "k8s" in file_path.parts or "kubernetes" in file_path.parts:
            manifests["kubernetes"].append(relative)
        elif "helm" in file_path.parts:
            manifests["helm"].append(relative)
    return manifests


def _parse_package_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(_safe_read_text(path))
    except json.JSONDecodeError:
        return {}


def _package_json_ecosystems(path: Path) -> set[str]:
    package_json = _parse_package_json(path)
    deps = {
        **package_json.get("dependencies", {}),
        **package_json.get("devDependencies", {}),
    }
    ecosystems: set[str] = set()
    if "react" in deps:
        ecosystems.add("react")
    if "next" in deps or "next.js" in deps:
        ecosystems.add("next")
    if "vue" in deps:
        ecosystems.add("vue")
    if "astro" in deps:
        ecosystems.add("astro")
    if "svelte" in deps:
        ecosystems.add("svelte")
    if "react-native" in deps or "expo" in deps:
        ecosystems.add("react-native")
    if "electron" in deps or "electron-builder" in deps or "electron-vite" in deps:
        ecosystems.add("electron")
    if any(dep.startswith("@tauri-apps/") for dep in deps) or any(
        (path.parent / "src-tauri" / candidate).exists()
        for candidate in ("tauri.conf.json", "tauri.conf.json5", "Cargo.toml")
    ):
        ecosystems.add("tauri")
    return ecosystems


def _pubspec_contains_flutter(path: Path) -> bool:
    text = _safe_read_text(path)
    return "sdk: flutter" in text or re.search(r"^flutter:\s*$", text, flags=re.MULTILINE) is not None


def _pubspec_roots(manifests: dict[str, list[str]]) -> set[Path]:
    roots = set()
    for rel in manifests["pubspec_yaml"]:
        roots.add(Path(rel).parent)
    return roots


def _is_under(relative_path: Path, parent: Path) -> bool:
    if parent == Path("."):
        return True
    return relative_path == parent or parent in relative_path.parents


def _is_flutter_platform_scaffold(relative_path: Path, flutter_roots: set[Path]) -> bool:
    for flutter_root in flutter_roots:
        for platform_dir in ("android", "ios", "macos", "linux", "windows"):
            candidate = flutter_root / platform_dir
            if _is_under(relative_path, candidate):
                return True
    return False


def _non_flutter_gradle_files(manifests: dict[str, list[str]], flutter_roots: set[Path]) -> list[str]:
    result: list[str] = []
    for rel in manifests["gradle"]:
        relative_path = Path(rel)
        if not _is_flutter_platform_scaffold(relative_path, flutter_roots):
            result.append(rel)
    return result


def _is_flutter_lib_file(relative_path: Path, flutter_roots: set[Path]) -> bool:
    for flutter_root in flutter_roots:
        candidate = flutter_root / "lib"
        if _is_under(relative_path, candidate):
            return True
    return False


def _is_documentation_path(relative_path: Path) -> bool:
    parts = {part.lower() for part in relative_path.parts}
    return bool(parts.intersection({"docs", "doc", "adr", "adrs", "references", "reference"}))


def _path_tokens(relative_path: Path) -> set[str]:
    return {
        token
        for token in re.split(r"[\\/._-]+", str(relative_path).replace("\\", "/").lower())
        if token
    }


def _is_global_context_file(relative_path: Path) -> bool:
    name_lower = relative_path.name.lower()
    suffix = relative_path.suffix.lower()
    if len(relative_path.parts) == 1:
        return name_lower.startswith("readme") or suffix in DOCUMENTATION_SUFFIXES or suffix in DIAGRAM_SUFFIXES
    if _is_documentation_path(relative_path):
        return suffix in DOCUMENTATION_SUFFIXES or suffix in DIAGRAM_SUFFIXES
    return False


def _is_probable_web_ui_file(relative_path: Path) -> bool:
    path_lower = str(relative_path).replace("\\", "/").lower()
    if "test/" in path_lower or _is_documentation_path(relative_path):
        return False

    suffix = relative_path.suffix.lower()
    if suffix not in {".tsx", ".jsx", ".vue", ".astro", ".html", ".css", ".scss", ".svelte"}:
        return False

    if any(hint in path_lower for hint in ("src/", "app/", "pages/", "components/", "styles/", "website/", "frontend/", "ui_")):
        return True

    return any(hint in path_lower for hint in UI_HINTS)


def _detect_ecosystems(root: Path, manifests: dict[str, list[str]]) -> list[str]:
    ecosystems: list[str] = []
    flutter_roots = _pubspec_roots(manifests)

    flutter_detected = any(_pubspec_contains_flutter(root / rel) for rel in manifests["pubspec_yaml"])
    if flutter_detected:
        ecosystems.append("flutter")
    elif manifests["pubspec_yaml"]:
        ecosystems.append("dart")

    for rel in manifests["package_json"]:
        ecosystems.extend(sorted(_package_json_ecosystems(root / rel)))

    if manifests["pyproject_toml"] or manifests["requirements_txt"]:
        ecosystems.append("python")
    if manifests["cargo_toml"]:
        ecosystems.append("rust")
    if manifests["go_mod"]:
        ecosystems.append("go")
    if manifests["pom_xml"] or _non_flutter_gradle_files(manifests, flutter_roots):
        ecosystems.append("jvm")
    if manifests["wails_json"]:
        ecosystems.append("wails")
    if manifests["docker"] or manifests["kubernetes"] or manifests["helm"]:
        ecosystems.append("container")

    return sorted(set(ecosystems))


def _language_counts(files: list[Path]) -> list[dict[str, Any]]:
    counts = Counter()
    for file_path in files:
        suffix = file_path.suffix.lower()
        language = LANGUAGE_BY_SUFFIX.get(suffix)
        if language:
            counts[language] += 1
    return [{"language": language, "count": count} for language, count in counts.most_common(12)]


def _source_file_count(files: list[Path]) -> int:
    count = 0
    for file_path in files:
        language = LANGUAGE_BY_SUFFIX.get(file_path.suffix.lower())
        if language in SOURCE_LANGUAGES:
            count += 1
    return count


def _source_root_details(root: Path, files: list[Path]) -> list[dict[str, Any]]:
    counts = Counter()
    languages_by_root: dict[str, set[str]] = {}

    for file_path in files:
        relative = file_path.relative_to(root)
        top = relative.parts[0] if len(relative.parts) > 1 else "."
        if top.startswith(".") or top in SKIP_DIRS or top in TEST_ROOTS:
            continue
        language = LANGUAGE_BY_SUFFIX.get(file_path.suffix.lower())
        if language not in SOURCE_LANGUAGES:
            continue
        counts[top] += 1
        languages_by_root.setdefault(top, set()).add(language)

    return [
        {
            "root": root_name,
            "source_file_count": count,
            "languages": sorted(languages_by_root.get(root_name, set()))[:6],
        }
        for root_name, count in counts.most_common()
    ]


def _find_source_roots(root: Path, files: list[Path]) -> list[str]:
    explicit_roots = []
    for child in root.iterdir():
        if child.is_dir() and child.name in {
            "src",
            "lib",
            "app",
            "apps",
            "packages",
            "services",
            "modules",
            "frontend",
            "backend",
            "internal",
            "website",
            "ui_main",
        }:
            explicit_roots.append(child.name)

    counts = Counter()
    for file_path in files:
        relative = file_path.relative_to(root)
        if not relative.parts:
            continue
        top = relative.parts[0]
        if top.startswith(".") or top in SKIP_DIRS or top in TEST_ROOTS:
            continue
        language = LANGUAGE_BY_SUFFIX.get(file_path.suffix.lower())
        if language in SOURCE_LANGUAGES:
            counts[top] += 1

    inferred_roots = [name for name, count in counts.most_common() if count >= 3 and name not in explicit_roots]
    return explicit_roots + inferred_roots


def _normalize_scope_path(value: str) -> Path:
    normalized = value.replace("\\", "/").strip().strip("/")
    if normalized in {"", "."}:
        return Path(".")
    return Path(normalized)


def _relative_str(path: Path) -> str:
    value = str(path).replace("\\", "/")
    return "." if value in {"", "."} else value


def _normalize_scope_paths(values: list[str] | None) -> tuple[Path, ...]:
    ordered: list[Path] = []
    for value in values or []:
        candidate = _normalize_scope_path(value)
        if candidate not in ordered:
            ordered.append(candidate)
    return tuple(ordered)


def _matching_scope_root(relative_path: Path, scope_roots: tuple[Path, ...]) -> Path | None:
    matches = [scope_root for scope_root in scope_roots if _is_under(relative_path, scope_root)]
    if not matches:
        return None
    return max(matches, key=lambda item: len(item.parts))


def _paths_overlap(left: Path, right: Path) -> bool:
    return _is_under(left, right) or _is_under(right, left)


def _scope_root_details(root: Path, files: list[Path], scope_roots: tuple[Path, ...]) -> list[dict[str, Any]]:
    if not scope_roots:
        return _source_root_details(root, files)

    counts = Counter()
    languages_by_root: dict[str, set[str]] = {}

    for file_path in files:
        relative = file_path.relative_to(root)
        matched_root = _matching_scope_root(relative, scope_roots)
        if matched_root is None:
            continue
        language = LANGUAGE_BY_SUFFIX.get(file_path.suffix.lower())
        if language not in SOURCE_LANGUAGES:
            continue
        root_name = _relative_str(matched_root)
        counts[root_name] += 1
        languages_by_root.setdefault(root_name, set()).add(language)

    return [
        {
            "root": root_name,
            "source_file_count": count,
            "languages": sorted(languages_by_root.get(root_name, set()))[:6],
        }
        for root_name, count in counts.most_common()
    ]


def _find_scoped_source_roots(root: Path, files: list[Path], scope_roots: tuple[Path, ...]) -> list[str]:
    if not scope_roots:
        return _find_source_roots(root, files)
    return [entry["root"] for entry in _scope_root_details(root, files, scope_roots)]


def _scope_roots_from_ecosystems(root: Path, manifests: dict[str, list[str]], requested_ecosystems: set[str]) -> set[Path]:
    scope_roots: set[Path] = set()
    flutter_roots = _pubspec_roots(manifests)

    if "flutter" in requested_ecosystems:
        for flutter_root in flutter_roots:
            for child_name in ("lib", "android", "ios", "macos", "linux", "windows", "web", "test", "integration_test"):
                candidate = flutter_root / child_name if flutter_root != Path(".") else Path(child_name)
                if (root / candidate).exists():
                    scope_roots.add(candidate)

    requested_package_ecosystems = requested_ecosystems.intersection(PACKAGE_UI_ECOSYSTEMS)
    if requested_package_ecosystems:
        for rel in manifests["package_json"]:
            if _package_json_ecosystems(root / rel).intersection(requested_package_ecosystems):
                package_dir = Path(rel).parent
                if package_dir != Path("."):
                    scope_roots.add(package_dir)

    if "go" in requested_ecosystems:
        scope_roots.update(Path(rel).parent for rel in manifests["go_mod"] if Path(rel).parent != Path("."))
    if "python" in requested_ecosystems:
        roots = manifests["pyproject_toml"] + manifests["requirements_txt"]
        scope_roots.update(Path(rel).parent for rel in roots if Path(rel).parent != Path("."))
    if "rust" in requested_ecosystems:
        scope_roots.update(Path(rel).parent for rel in manifests["cargo_toml"] if Path(rel).parent != Path("."))
    if "jvm" in requested_ecosystems:
        roots = manifests["pom_xml"] + _non_flutter_gradle_files(manifests, flutter_roots)
        scope_roots.update(Path(rel).parent for rel in roots if Path(rel).parent != Path("."))
    if "wails" in requested_ecosystems:
        scope_roots.update(Path(rel).parent for rel in manifests["wails_json"] if Path(rel).parent != Path("."))

    return scope_roots


def _file_matches_scope(relative_path: Path, scope_roots: tuple[Path, ...]) -> bool:
    if not scope_roots:
        return True
    return _matching_scope_root(relative_path, scope_roots) is not None


def _file_matches_scope_or_global_docs(relative_path: Path, scope_roots: tuple[Path, ...]) -> bool:
    if not scope_roots:
        return True
    if _file_matches_scope(relative_path, scope_roots):
        return True
    return _is_global_context_file(relative_path)


def _manifest_matches_scope(
    root: Path,
    manifest_kind: str,
    relative_manifest_path: str,
    scope_roots: tuple[Path, ...],
    requested_ecosystems: set[str],
    flutter_roots: set[Path],
) -> bool:
    relative_path = Path(relative_manifest_path)
    if not scope_roots and not requested_ecosystems:
        return True
    if _matching_scope_root(relative_path, scope_roots) is not None:
        return True

    manifest_path = root / relative_manifest_path
    if manifest_kind == "pubspec_yaml":
        if "flutter" in requested_ecosystems and _pubspec_contains_flutter(manifest_path):
            return True
        if "dart" in requested_ecosystems and not _pubspec_contains_flutter(manifest_path):
            return True
    if manifest_kind == "package_json":
        return bool(_package_json_ecosystems(manifest_path).intersection(requested_ecosystems))
    if manifest_kind == "go_mod":
        return "go" in requested_ecosystems
    if manifest_kind in {"pyproject_toml", "requirements_txt"}:
        return "python" in requested_ecosystems
    if manifest_kind == "cargo_toml":
        return "rust" in requested_ecosystems
    if manifest_kind == "pom_xml":
        return "jvm" in requested_ecosystems
    if manifest_kind == "gradle":
        return "jvm" in requested_ecosystems and not _is_flutter_platform_scaffold(relative_path, flutter_roots)
    if manifest_kind == "wails_json":
        return "wails" in requested_ecosystems
    return False


def _filter_manifests(
    root: Path,
    manifests: dict[str, list[str]],
    scope_roots: tuple[Path, ...],
    requested_ecosystems: set[str],
) -> dict[str, list[str]]:
    filtered = {key: [] for key in manifests}
    flutter_roots = _pubspec_roots(manifests)
    for manifest_kind, values in manifests.items():
        for value in values:
            if _manifest_matches_scope(root, manifest_kind, value, scope_roots, requested_ecosystems, flutter_roots):
                filtered[manifest_kind].append(value)
    return filtered


def _command_matches_scope(
    entry: dict[str, str],
    scope_roots: tuple[Path, ...],
    requested_ecosystems: set[str],
) -> bool:
    if not scope_roots and not requested_ecosystems:
        return True
    if not scope_roots:
        return False

    cwd_path = _normalize_scope_path(entry.get("cwd", "."))
    return any(_paths_overlap(cwd_path, scope_root) for scope_root in scope_roots)


def _is_probable_ui_file(relative: Path, is_flutter_app: bool, flutter_roots: set[Path]) -> bool:
    suffix = relative.suffix.lower()
    path_lower = str(relative).replace("\\", "/").lower()

    if suffix in {".tsx", ".jsx", ".vue", ".astro", ".html", ".css", ".scss", ".svelte"}:
        return _is_probable_web_ui_file(relative)

    if suffix != ".dart" or not is_flutter_app:
        return False

    if "test/" in path_lower:
        return False
    if not _is_flutter_lib_file(relative, flutter_roots):
        return False
    if relative.name in {"app.dart", "main.dart"}:
        return True
    return any(hint in path_lower for hint in UI_HINTS)


def _ui_samples(
    files: list[Path],
    root: Path,
    is_flutter_app: bool,
    ecosystems: set[str],
    flutter_roots: set[Path],
) -> list[str]:
    strong_matches: list[str] = []
    fallback_matches: list[str] = []

    for file_path in files:
        relative = file_path.relative_to(root)
        relative_str = str(relative)
        suffix = relative.suffix.lower()

        if _is_probable_ui_file(relative, is_flutter_app, flutter_roots):
            strong_matches.append(relative_str)
        elif _is_probable_web_ui_file(relative):
            fallback_matches.append(relative_str)
        elif is_flutter_app and suffix == ".dart" and _is_flutter_lib_file(relative, flutter_roots):
            fallback_matches.append(relative_str)

    ordered = strong_matches + [item for item in fallback_matches if item not in strong_matches]
    if ordered:
        return ordered[:20]

    return []


def _doc_samples(files: list[Path], root: Path) -> list[str]:
    matches: list[str] = []
    for file_path in files:
        if file_path.suffix.lower() not in {".md", ".txt", ".adoc", ".rst"}:
            continue
        if DOC_PATTERN.search(str(file_path)):
            matches.append(str(file_path.relative_to(root)))
        if len(matches) >= 20:
            break
    return matches


def _readme_samples(files: list[Path], root: Path) -> list[str]:
    matches: list[str] = []
    for file_path in files:
        relative = file_path.relative_to(root)
        name_lower = file_path.name.lower()
        if name_lower.startswith("readme") or relative.parts[0].lower() in {"docs", "doc"}:
            if file_path.suffix.lower() in {".md", ".txt", ".adoc", ".rst"}:
                matches.append(str(relative))
        if len(matches) >= 10:
            break
    return matches


def _diagram_samples(files: list[Path], root: Path) -> list[str]:
    matches: list[str] = []
    for file_path in files:
        relative = file_path.relative_to(root)
        path_lower = str(relative).replace("\\", "/").lower()
        if file_path.suffix.lower() not in DIAGRAM_SUFFIXES:
            continue
        if any(token in path_lower for token in ("arch", "diagram", "uml", "design", "flow", "sequence", "component")):
            matches.append(str(relative))
        if len(matches) >= 20:
            break
    return matches


def _tooling_artifact_samples(files: list[Path], root: Path) -> list[str]:
    matches: list[str] = []
    for file_path in files:
        relative = file_path.relative_to(root)
        name_lower = file_path.name.lower()
        path_lower = str(relative).replace("\\", "/").lower()
        if (
            name_lower in TOOLING_ARTIFACT_NAMES
            or name_lower.endswith(".sarif")
            or ".semgrep" in path_lower
            or "semgrep" in name_lower
            or "eslint" in name_lower
            or "dependency-check" in name_lower
        ):
            matches.append(str(relative))
        if len(matches) >= 20:
            break
    return matches


def _security_signal_samples(files: list[Path], root: Path) -> list[str]:
    matches: list[str] = []
    for file_path in files:
        relative = file_path.relative_to(root)
        path_lower = str(relative).replace("\\", "/").lower()
        if "test/" in path_lower or _is_documentation_path(relative):
            continue
        tokens = _path_tokens(relative)
        if tokens.intersection(SECURITY_HINTS):
            matches.append(str(relative))
        if len(matches) >= 20:
            break
    return matches


def _named_signal_samples(
    files: list[Path],
    root: Path,
    hints: set[str],
    *,
    extra_names: set[str] | None = None,
    extra_suffixes: set[str] | None = None,
) -> list[str]:
    matches: list[str] = []
    extra_names = {name.lower() for name in (extra_names or set())}
    extra_suffixes = {suffix.lower() for suffix in (extra_suffixes or set())}

    for file_path in files:
        relative = file_path.relative_to(root)
        if _is_documentation_path(relative):
            continue
        tokens = _path_tokens(relative)
        name_lower = file_path.name.lower()
        if (
            tokens.intersection(hints)
            or name_lower in extra_names
            or file_path.suffix.lower() in extra_suffixes
        ):
            matches.append(str(relative))
        if len(matches) >= 20:
            break
    return matches


def _accessibility_signal_samples(files: list[Path], root: Path) -> list[str]:
    return _named_signal_samples(files, root, ACCESSIBILITY_HINTS)


def _localization_signal_samples(files: list[Path], root: Path) -> list[str]:
    return _named_signal_samples(
        files,
        root,
        LOCALIZATION_HINTS,
        extra_names={"l10n.yaml", "strings.xml"},
        extra_suffixes={".arb", ".strings"},
    )


def _design_system_signal_samples(files: list[Path], root: Path) -> list[str]:
    return _named_signal_samples(
        files,
        root,
        DESIGN_SYSTEM_HINTS,
        extra_names={
            "tailwind.config.js",
            "tailwind.config.cjs",
            "tailwind.config.mjs",
            "tailwind.config.ts",
        },
    )


def _platform_profile(
    root: Path,
    files: list[Path],
    ecosystems: set[str],
    manifests: dict[str, list[str]],
    flutter_roots: set[Path],
    accessibility_samples: list[str],
    localization_samples: list[str],
    design_system_samples: list[str],
) -> dict[str, Any]:
    relatives = [file_path.relative_to(root) for file_path in files]
    targets: set[str] = set()
    families: set[str] = set()
    evidence: list[str] = []
    evidence_seen: set[str] = set()

    def add_evidence(message: str) -> None:
        if message not in evidence_seen:
            evidence.append(message)
            evidence_seen.add(message)

    def has_under(path: Path) -> bool:
        return any(_is_under(relative, path) for relative in relatives)

    web_ecosystems = ecosystems.intersection(WEB_ECOSYSTEMS)
    if web_ecosystems or any(
        _is_probable_web_ui_file(relative)
        for relative in relatives
    ):
        targets.add("web")
        families.add("web")
        if web_ecosystems:
            add_evidence(f"Web surface signals detected via ecosystems: {', '.join(sorted(web_ecosystems))}.")
        else:
            add_evidence("Web UI files are present in the scoped source roots.")

    for target in ("android", "ios", "macos", "linux", "windows", "web"):
        if has_under(Path(target)):
            targets.add(target)
            if target == "web":
                families.add("web")
            elif target in {"android", "ios"}:
                families.add("mobile")
            else:
                families.add("desktop")

    flutter_targets: list[str] = []
    if "flutter" in ecosystems:
        for flutter_root in flutter_roots or {Path(".")}:
            for target in PLATFORM_TARGET_ORDER:
                candidate = flutter_root / target if flutter_root != Path(".") else Path(target)
                if candidate != Path(".") and has_under(candidate):
                    flutter_targets.append(target)
        if flutter_targets:
            for target in sorted(set(flutter_targets)):
                targets.add(target)
                if target == "web":
                    families.add("web")
                elif target in {"android", "ios"}:
                    families.add("mobile")
                else:
                    families.add("desktop")
            add_evidence(f"Flutter target directories are present in scope: {', '.join(sorted(set(flutter_targets)))}.")
        else:
            add_evidence("Flutter UI code is present, but concrete shipping targets were not proven from scoped files.")

    if "react-native" in ecosystems:
        families.add("mobile")
        rn_targets: set[str] = set()
        for rel in manifests["package_json"]:
            package_json_path = root / rel
            if "react-native" not in _package_json_ecosystems(package_json_path):
                continue
            package_dir = package_json_path.parent
            for target in ("android", "ios"):
                if (package_dir / target).exists():
                    rn_targets.add(target)
                    targets.add(target)
        rn_targets_list = sorted(rn_targets)
        if rn_targets:
            add_evidence(f"React Native mobile targets are present in scope: {', '.join(rn_targets_list)}.")
        else:
            add_evidence("React Native dependencies are present; concrete iOS/Android target folders were not proven in scope.")

    if "electron" in ecosystems:
        families.add("desktop")
        families.add("web")
        add_evidence("Electron desktop shell with web-rendered UI detected via package.json dependencies.")
    if "tauri" in ecosystems:
        families.add("desktop")
        families.add("web")
        add_evidence("Tauri desktop shell with web-rendered UI detected via @tauri-apps signals or src-tauri configuration.")
    if "wails" in ecosystems or manifests["wails_json"]:
        families.add("desktop")
        families.add("web")
        add_evidence("Wails desktop shell with web-rendered UI detected via wails.json.")

    family_expectations = [
        {
            "family": family,
            "checks": PLATFORM_FAMILY_EXPECTATIONS[family],
        }
        for family in PLATFORM_FAMILY_ORDER
        if family in families
    ]

    evidence_gaps: list[str] = []
    if families and not accessibility_samples:
        evidence_gaps.append("No explicit accessibility-focused files or configs were detected in the selected scope.")
    if families and not localization_samples:
        evidence_gaps.append("No explicit localization/i18n assets were detected in the selected scope.")
    if families and not design_system_samples:
        evidence_gaps.append("No explicit design-system or theming artifacts were detected in the selected scope.")

    return {
        "families": [family for family in PLATFORM_FAMILY_ORDER if family in families],
        "targets": [target for target in PLATFORM_TARGET_ORDER if target in targets],
        "evidence": evidence[:8],
        "shared_standards": SHARED_PLATFORM_UX_STANDARDS,
        "family_expectations": family_expectations,
        "evidence_gaps": evidence_gaps,
    }


def _entrypoint_samples(files: list[Path], root: Path) -> list[str]:
    matches: list[str] = []
    for file_path in files:
        relative = file_path.relative_to(root)
        path_lower = str(relative).replace("\\", "/").lower()
        if file_path.name.lower() in ENTRYPOINT_FILENAMES:
            matches.append(str(relative))
        elif any(token in path_lower for token in ("routes/", "router", "bootstrap", "startup", "program.cs")):
            matches.append(str(relative))
        if len(matches) >= 20:
            break
    return matches


def _find_gradle_wrapper(root: Path, start_dir: Path) -> tuple[str, str] | None:
    current = start_dir
    while True:
        gradlew_bat = current / "gradlew.bat"
        gradlew = current / "gradlew"
        if gradlew_bat.exists():
            return (str(current.relative_to(root)), "gradlew.bat test")
        if gradlew.exists():
            return (str(current.relative_to(root)), "./gradlew test")
        if current == root:
            return None
        current = current.parent


def _detect_package_manager(root: Path, package_dir: Path) -> str:
    for directory in (package_dir, root):
        if (directory / "pnpm-lock.yaml").exists() or (directory / "pnpm-workspace.yaml").exists():
            return "pnpm"
        if (directory / "yarn.lock").exists():
            return "yarn"
        if (directory / "bun.lockb").exists() or (directory / "bun.lock").exists():
            return "bun"
        if (directory / "package-lock.json").exists():
            return "npm"
    return "npm"


def _package_script_command(package_manager: str, script_name: str) -> str:
    if package_manager == "pnpm":
        return script_name if script_name.startswith("pnpm ") else f"pnpm {script_name}"
    if package_manager == "yarn":
        return script_name if script_name.startswith("yarn ") else f"yarn {script_name}"
    if package_manager == "bun":
        return script_name if script_name.startswith("bun ") else f"bun run {script_name}"
    return script_name if script_name.startswith("npm ") else f"npm run {script_name}"


def _candidate_commands(
    root: Path,
    manifests: dict[str, list[str]],
    ecosystems: list[str],
    scope_roots: tuple[Path, ...] = (),
    requested_ecosystems: set[str] | None = None,
) -> list[dict[str, str]]:
    commands: list[dict[str, str]] = []
    flutter_roots = _pubspec_roots(manifests)
    requested_ecosystems = requested_ecosystems or set()

    def add_command(cwd: str, command: str, reason: str) -> None:
        entry = {"cwd": cwd or ".", "command": command, "reason": reason}
        if entry not in commands:
            commands.append(entry)

    for rel in manifests["pubspec_yaml"]:
        pubspec_path = root / rel
        if _pubspec_contains_flutter(pubspec_path):
            cwd = str(Path(rel).parent)
            add_command(cwd, "flutter analyze", "Flutter app/package validation")
            add_command(cwd, "flutter test", "Flutter app/package test suite")

    for rel in manifests["package_json"]:
        package_json = _parse_package_json(root / rel)
        scripts = package_json.get("scripts", {})
        package_dir = (root / rel).parent
        cwd = str(Path(rel).parent)
        package_manager = _detect_package_manager(root, package_dir)
        for key in ("lint", "typecheck", "build", "test", "analyze"):
            if key in scripts:
                add_command(cwd, _package_script_command(package_manager, key), f"{package_manager} script: {key}")

    if "python" in ecosystems:
        for rel in manifests["pyproject_toml"] + manifests["requirements_txt"]:
            add_command(str(Path(rel).parent), "pytest", "Python test command candidate")

    for rel in manifests["cargo_toml"]:
        cwd = str(Path(rel).parent)
        add_command(cwd, "cargo test", "Rust test suite")
        add_command(cwd, "cargo build", "Rust build")

    for rel in manifests["go_mod"]:
        add_command(str(Path(rel).parent), "go test ./...", "Go test suite")

    for rel in manifests["pom_xml"]:
        add_command(str(Path(rel).parent), "mvn test", "Maven test suite")

    for rel in _non_flutter_gradle_files(manifests, flutter_roots):
        gradle_info = _find_gradle_wrapper(root, (root / rel).parent)
        if gradle_info:
            cwd, command = gradle_info
            add_command(cwd, command, "Gradle test suite")

    return [
        entry
        for entry in commands
        if _command_matches_scope(entry, scope_roots, requested_ecosystems)
    ]


def _performance_signals(files: list[Path], root: Path) -> list[str]:
    signals: list[str] = []
    for file_path in files:
        path_lower = str(file_path.relative_to(root)).replace("\\", "/").lower()
        tokens = {token for token in re.split(r"[\\/._-]+", path_lower) if token}
        if tokens.intersection(PERFORMANCE_HINTS):
            signals.append(str(file_path.relative_to(root)))
        if len(signals) >= 20:
            break
    return signals


def _apple_targets_present(files: list[Path], root: Path) -> bool:
    for file_path in files:
        relative = file_path.relative_to(root)
        if "ios" in relative.parts or "macos" in relative.parts:
            return True
    return False


def analyze_repository(
    root: Path,
    include_roots: list[str] | None = None,
    include_ecosystems: list[str] | None = None,
) -> dict[str, Any]:
    files = _walk_files(root)
    manifests = _detect_manifests(root, files)
    requested_scope_roots = _normalize_scope_paths(include_roots)
    requested_scope_ecosystems = {value.lower() for value in include_ecosystems or [] if value.strip()}
    resolved_scope_roots = tuple(
        list(requested_scope_roots)
        + [
            candidate
            for candidate in sorted(
                _scope_roots_from_ecosystems(root, manifests, requested_scope_ecosystems),
                key=lambda item: _relative_str(item),
            )
            if candidate not in requested_scope_roots
        ]
    )
    scope_mode = "scoped" if resolved_scope_roots or requested_scope_ecosystems else "whole-repo"

    if scope_mode == "scoped" and not resolved_scope_roots:
        scoped_files = []
        context_files = [
            file_path
            for file_path in files
            if _is_global_context_file(file_path.relative_to(root))
        ]
    else:
        scoped_files = [
            file_path
            for file_path in files
            if _file_matches_scope(file_path.relative_to(root), resolved_scope_roots)
        ]
        context_files = [
            file_path
            for file_path in files
            if _file_matches_scope_or_global_docs(file_path.relative_to(root), resolved_scope_roots)
        ]
    scoped_manifests = _filter_manifests(root, manifests, resolved_scope_roots, requested_scope_ecosystems)
    ecosystems = _detect_ecosystems(root, scoped_manifests)
    is_flutter_app = "flutter" in ecosystems
    flutter_roots = _pubspec_roots(scoped_manifests)
    ui_samples = _ui_samples(scoped_files, root, is_flutter_app, set(ecosystems), flutter_roots)
    accessibility_samples = _accessibility_signal_samples(scoped_files, root)
    localization_samples = _localization_signal_samples(scoped_files, root)
    design_system_samples = _design_system_signal_samples(context_files, root)
    all_source_root_details = _source_root_details(root, files)
    scoped_source_root_details = _scope_root_details(root, scoped_files, resolved_scope_roots)
    if scope_mode == "scoped":
        existing_scoped_roots = {entry["root"] for entry in scoped_source_root_details}
        requested_empty_scope_roots: list[str] = []
        for requested_root in requested_scope_roots:
            requested_root_str = _relative_str(requested_root)
            if requested_root_str in existing_scoped_roots:
                continue
            if (root / requested_root).exists():
                requested_empty_scope_roots.append(requested_root_str)
    else:
        requested_empty_scope_roots = []
    included_scope_roots = [entry["root"] for entry in scoped_source_root_details]
    excluded_scope_roots = []
    scope_resolved = scope_mode != "scoped" or bool(included_scope_roots)
    manifest_flutter_roots = _pubspec_roots(manifests)
    root_level_requested_matches: list[str] = []
    if scope_mode == "scoped" and requested_scope_ecosystems and not scope_resolved:
        for manifest_kind, values in manifests.items():
            for value in values:
                if Path(value).parent == Path(".") and _manifest_matches_scope(
                    root,
                    manifest_kind,
                    value,
                    (),
                    requested_scope_ecosystems,
                    manifest_flutter_roots,
                ):
                    root_level_requested_matches.append(value)
    if scope_resolved:
        platform_profile = _platform_profile(
            root,
            scoped_files,
            set(ecosystems),
            scoped_manifests,
            flutter_roots,
            accessibility_samples,
            localization_samples,
            design_system_samples,
        )
    else:
        platform_profile = {
            "families": [],
            "targets": [],
            "evidence": [],
            "shared_standards": [],
            "family_expectations": [],
            "evidence_gaps": [],
        }
    if scope_mode == "scoped" and included_scope_roots:
        for entry in all_source_root_details:
            entry_root = _normalize_scope_path(entry["root"])
            if not any(_paths_overlap(entry_root, scope_root) for scope_root in resolved_scope_roots):
                excluded_scope_roots.append(entry["root"])
    scope_notes: list[str] = []
    if scope_mode == "scoped":
        if requested_scope_roots:
            scope_notes.append(
                f"Explicit scope roots requested: {', '.join(_relative_str(path) for path in requested_scope_roots)}."
            )
        if requested_scope_ecosystems:
            scope_notes.append(
                f"Scoped ecosystems requested: {', '.join(sorted(requested_scope_ecosystems))}."
            )
        scope_notes.append(
            "Code and validation commands are limited to the included scope. Repository-level README/docs may still inform the architecture brief."
        )
        if excluded_scope_roots:
            scope_notes.append(
                f"Excluded source roots remain outside the review scope: {', '.join(excluded_scope_roots)}."
            )
        if requested_empty_scope_roots:
            scope_notes.append(
                f"Requested roots exist but contain no detected source files in scope: {', '.join(requested_empty_scope_roots)}."
            )
        if root_level_requested_matches:
            scope_notes.append(
                "The requested ecosystem is only evidenced at repository root. This remains unresolved on purpose so the scoped review does not silently widen to whole-repo mode."
            )
        if not included_scope_roots:
            scope_notes.append("The requested scope did not resolve to any detected source roots. Treat the scope as unresolved and confirm it before reviewing.")

    return {
        "root": str(root.resolve()),
        "scope_mode": scope_mode,
        "scope_resolved": scope_resolved,
        "requested_scope_roots": [_relative_str(path) for path in requested_scope_roots],
        "requested_scope_ecosystems": sorted(requested_scope_ecosystems),
        "included_scope_roots": included_scope_roots,
        "excluded_scope_roots": excluded_scope_roots,
        "scope_notes": scope_notes,
        "file_count": len(scoped_files) if scope_mode == "scoped" else len(files),
        "source_file_count": _source_file_count(scoped_files),
        "manifests": scoped_manifests,
        "ecosystems": ecosystems,
        "platform_profile": platform_profile,
        "languages": _language_counts(scoped_files),
        "source_root_details": scoped_source_root_details if scope_mode == "scoped" else all_source_root_details,
        "source_roots": [] if scope_mode == "scoped" and not scope_resolved else _find_scoped_source_roots(root, scoped_files, resolved_scope_roots),
        "ui_present": bool(ui_samples) and scope_resolved,
        "ui_samples": ui_samples,
        "accessibility_signal_samples": accessibility_samples,
        "localization_signal_samples": localization_samples,
        "design_system_signal_samples": design_system_samples,
        "readme_samples": _readme_samples(context_files, root),
        "architecture_doc_samples": _doc_samples(context_files, root),
        "diagram_samples": _diagram_samples(context_files, root),
        "tooling_artifact_samples": _tooling_artifact_samples(context_files, root),
        "entrypoint_samples": _entrypoint_samples(scoped_files, root),
        "candidate_commands": _candidate_commands(root, scoped_manifests, ecosystems, resolved_scope_roots, requested_scope_ecosystems),
        "performance_signals": _performance_signals(scoped_files, root),
        "security_signals": _security_signal_samples(scoped_files, root),
        "apple_targets_present": _apple_targets_present(scoped_files, root),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_path")
    parser.add_argument(
        "--include-root",
        action="append",
        dest="include_roots",
        default=[],
        help="Relative path prefix to keep in scope. Repeatable.",
    )
    parser.add_argument(
        "--include-ecosystem",
        action="append",
        dest="include_ecosystems",
        default=[],
        help="Detected ecosystem to keep in scope, such as flutter, astro, or go. Repeatable.",
    )
    args = parser.parse_args()

    root = Path(args.repo_path).resolve()
    if not root.exists() or not root.is_dir():
        print(f"repository path not found: {root}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            analyze_repository(
                root,
                include_roots=args.include_roots,
                include_ecosystems=args.include_ecosystems,
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
