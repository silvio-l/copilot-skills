from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "review"


def _scope_slug(include_roots: list[str], include_ecosystems: list[str]) -> str:
    parts: list[str] = []
    for root in include_roots:
        parts.append(f"root-{_slug(root.replace('\\', '-').replace('/', '-'))}")
    for ecosystem in include_ecosystems:
        parts.append(f"ecosystem-{_slug(ecosystem)}")
    return "--".join(parts) if parts else "whole-repo"


def _default_output_root() -> Path:
    return Path.home() / ".copilot" / "review-artifacts" / "system-lens"


def build_artifact_paths(
    target_path: Path,
    include_roots: list[str],
    include_ecosystems: list[str],
    output_root: Path,
    run_stamp: str,
) -> dict[str, str]:
    repo_slug = _slug(target_path.name)
    scope_slug = _scope_slug(include_roots, include_ecosystems)
    artifact_dir = output_root / repo_slug / f"{run_stamp}--{scope_slug}"
    artifact_dir.mkdir(parents=True, exist_ok=True)

    file_stem = f"{repo_slug}--{scope_slug}"
    return {
        "target_path": str(target_path),
        "output_root": str(output_root),
        "artifact_dir": str(artifact_dir),
        "scope_slug": scope_slug,
        "report_markdown_path": str(artifact_dir / f"{file_stem}--report.md"),
        "findings_json_path": str(artifact_dir / f"{file_stem}--findings.json"),
        "context_json_path": str(artifact_dir / f"{file_stem}--context.json"),
        "outline_json_path": str(artifact_dir / f"{file_stem}--outline.json"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare deterministic system-lens artifact paths with absolute output locations."
    )
    parser.add_argument("target_path", help="Repository or scoped target path being reviewed.")
    parser.add_argument("--include-root", action="append", default=[], dest="include_roots")
    parser.add_argument("--include-ecosystem", action="append", default=[], dest="include_ecosystems")
    parser.add_argument(
        "--output-root",
        default=str(_default_output_root()),
        help="Base directory for persistent review artifacts. Defaults to ~/.copilot/review-artifacts/system-lens",
    )
    parser.add_argument(
        "--run-stamp",
        default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        help="Optional deterministic run stamp, mainly for tests.",
    )
    args = parser.parse_args()

    target_path = Path(args.target_path).resolve()
    if not target_path.exists():
        raise SystemExit(f"target path not found: {target_path}")

    output_root = Path(args.output_root).expanduser().resolve()
    payload = build_artifact_paths(
        target_path=target_path,
        include_roots=list(args.include_roots),
        include_ecosystems=list(args.include_ecosystems),
        output_root=output_root,
        run_stamp=args.run_stamp,
    )
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
