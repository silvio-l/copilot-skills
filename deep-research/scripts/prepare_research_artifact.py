from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "research"


def _default_output_root() -> Path:
    return Path.home() / ".copilot" / "review-artifacts" / "deep-research"


def build_artifact_paths(
    research_topic: str,
    output_root: Path,
    run_stamp: str,
) -> dict[str, str]:
    topic_slug = _slug(research_topic)
    artifact_dir = output_root / topic_slug / f"{run_stamp}--{topic_slug}"
    artifact_dir.mkdir(parents=True, exist_ok=True)

    return {
        "research_topic": research_topic,
        "topic_slug": topic_slug,
        "output_root": str(output_root),
        "artifact_dir": str(artifact_dir),
        "report_markdown_path": str(artifact_dir / f"{topic_slug}--report.md"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare deterministic deep-research artifact paths with absolute output locations."
    )
    parser.add_argument(
        "research_topic",
        help="Topic, decision, or question being investigated.",
    )
    parser.add_argument(
        "--output-root",
        default=str(_default_output_root()),
        help="Base directory for persistent deep-research artifacts. Defaults to ~/.copilot/review-artifacts/deep-research",
    )
    parser.add_argument(
        "--run-stamp",
        default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        help="Optional deterministic run stamp, mainly for tests or backfilling prior reports.",
    )
    args = parser.parse_args()

    output_root = Path(args.output_root).expanduser().resolve()
    payload = build_artifact_paths(
        research_topic=args.research_topic,
        output_root=output_root,
        run_stamp=args.run_stamp,
    )
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
