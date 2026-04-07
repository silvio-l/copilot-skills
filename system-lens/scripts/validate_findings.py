from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "claim",
    "why_it_matters",
    "primary_evidence",
    "confidence",
    "recommended_action",
    "needs_human_confirmation",
}
HIGH_CONFIDENCE = {"high", "High"}
REQUIRED_ARCH_MODELS = {"gpt-5.4", "claude-sonnet-4.6"}
ARCH_CORROBORATION_STATUSES = {"shared", "disputed", "degraded"}
VALIDATION_BLOCKER_TYPES = {
    "validation-blocker",
    "validation_blocker",
    "tooling-blocker",
    "tooling_blocker",
    "environment-blocker",
    "environment_blocker",
}
ALLOWED_ATTRIBUTION_SCOPES = {"repo", "environment", "unknown"}


def _load_bundle(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("findings"), list):
        return payload["findings"]
    raise ValueError("Expected a JSON array or an object with a 'findings' list.")


def _validate_finding(index: int, finding: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(field for field in REQUIRED_FIELDS if field not in finding)
    if missing:
        errors.append(f"finding[{index}] missing required fields: {', '.join(missing)}")

    finding_type = str(finding.get("finding_type", "")).lower()
    confidence = str(finding.get("confidence", ""))
    corroborating_evidence = finding.get("corroborating_evidence", [])
    model_corroborated_by = {str(model) for model in finding.get("model_corroborated_by", [])}
    architecture_corroboration_status = str(
        finding.get("architecture_corroboration_status", "")
    ).lower()
    attribution_scope = str(finding.get("attribution_scope", "")).lower()

    if finding_type == "architecture":
        if not corroborating_evidence:
            errors.append(f"finding[{index}] architecture findings need corroborating_evidence.")
        if architecture_corroboration_status not in ARCH_CORROBORATION_STATUSES:
            errors.append(
                f"finding[{index}] architecture findings must declare architecture_corroboration_status as shared, disputed, or degraded."
            )
        if confidence in HIGH_CONFIDENCE and not REQUIRED_ARCH_MODELS.issubset(model_corroborated_by):
            errors.append(
                f"finding[{index}] high-confidence architecture findings must be corroborated by GPT-5.4 and Claude Sonnet 4.6."
            )
        if confidence in HIGH_CONFIDENCE and architecture_corroboration_status != "shared":
            errors.append(
                f"finding[{index}] high-confidence architecture findings must use architecture_corroboration_status='shared'."
            )

    if finding_type in VALIDATION_BLOCKER_TYPES:
        if attribution_scope not in ALLOWED_ATTRIBUTION_SCOPES:
            errors.append(
                f"finding[{index}] validation blockers must declare attribution_scope as repo, environment, or unknown."
            )
        if confidence in HIGH_CONFIDENCE and attribution_scope == "unknown":
            errors.append(
                f"finding[{index}] high-confidence validation blockers cannot use attribution_scope='unknown'."
            )

    if confidence in HIGH_CONFIDENCE and not finding.get("primary_evidence"):
        errors.append(f"finding[{index}] high-confidence findings need primary_evidence.")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_findings.py <findings-json-path>", file=sys.stderr)
        return 2

    bundle_path = Path(sys.argv[1]).resolve()
    if not bundle_path.exists():
        print(f"bundle not found: {bundle_path}", file=sys.stderr)
        return 1

    try:
        findings = _load_bundle(bundle_path)
    except (ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    errors: list[str] = []
    for index, finding in enumerate(findings):
        errors.extend(_validate_finding(index, finding))

    if errors:
        print(json.dumps({"ok": False, "errors": errors}, indent=2))
        return 1

    print(json.dumps({"ok": True, "finding_count": len(findings)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
