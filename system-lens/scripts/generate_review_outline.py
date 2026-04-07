from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


def _load_analyzer() -> Any:
    try:
        from collect_review_context import analyze_repository  # type: ignore
    except ModuleNotFoundError:
        script_dir = Path(__file__).resolve().parent
        module_path = script_dir / "collect_review_context.py"
        spec = importlib.util.spec_from_file_location("collect_review_context", module_path)
        if spec is None or spec.loader is None:
            raise
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        analyze_repository = module.analyze_repository
    return analyze_repository


ANALYZE_REPOSITORY = _load_analyzer()
NON_SOURCE_LANGUAGES = {"markdown", "json", "yaml", "toml"}


def _load_context(arg: str) -> dict[str, Any]:
    path = Path(arg).resolve()
    if path.is_file() and path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    if path.is_dir():
        return ANALYZE_REPOSITORY(path)
    raise FileNotFoundError(arg)


def _source_language_count(context: dict[str, Any]) -> int:
    return sum(
        1
        for entry in context.get("languages", [])
        if entry["language"] not in NON_SOURCE_LANGUAGES
    )


def _has_persona_signals(context: dict[str, Any]) -> bool:
    haystack = " ".join(context.get("ui_samples", []) + context.get("architecture_doc_samples", [])).lower()
    return any(
        token in haystack
        for token in (
            "onboarding",
            "welcome",
            "paywall",
            "pricing",
            "signup",
            "trial",
        )
    )


def _coverage_targets(context: dict[str, Any]) -> list[dict[str, Any]]:
    coverage = []
    for entry in context.get("source_root_details", []):
        coverage.append(
            {
                "root": entry["root"],
                "source_file_count": entry["source_file_count"],
                "languages": entry.get("languages", []),
                "reason": "Detected source root that must be summarized before hotspot deep-dives.",
            }
        )
    if coverage:
        return coverage

    return [
        {
            "root": root_name,
            "source_file_count": None,
            "languages": [],
            "reason": "Fallback source root inferred from repository scan.",
        }
        for root_name in context.get("source_roots", [])
    ]


def _human_follow_up_questions(context: dict[str, Any]) -> list[str]:
    questions: list[str] = []
    platform_profile = context.get("platform_profile", {})
    platform_families = platform_profile.get("families", [])

    if not context.get("readme_samples"):
        questions.append("What is the product or system primarily trying to achieve for users or operators?")
    if not context.get("architecture_doc_samples"):
        questions.append("Which architecture decisions were intentional, and which trade-offs or rejected alternatives are not visible in the code?")
    if context.get("source_file_count", 0) > 400 and not context.get("diagram_samples"):
        questions.append("Are there architecture diagrams, ADRs, or system maps outside the repository that would explain the major module boundaries?")
    if context.get("security_signals"):
        questions.append("Which trust boundaries, sensitive data paths, or abuse cases matter most for this system?")
    if context.get("ui_present"):
        questions.append("Which user journeys matter most, and what does success or failure look like for those flows?")
    if platform_families:
        questions.append(
            f"Which platform families actually ship from this scope ({', '.join(platform_families)}), and which platform-specific conventions are intentionally overridden?"
        )
    if context.get("ui_present") and not context.get("localization_signal_samples"):
        questions.append("Which locales, regions, or accessibility commitments does the product need to support beyond the default language?")
    if context.get("scope_mode") == "scoped" and context.get("excluded_scope_roots"):
        questions.append("Which dependencies from the included scope into excluded roots matter enough that the team wants them called out explicitly?")

    return questions


def _platform_ux_review_brief(context: dict[str, Any]) -> dict[str, Any]:
    profile = context.get("platform_profile", {})
    if not profile.get("families") and not profile.get("targets"):
        return {}

    return {
        "families": profile.get("families", []),
        "targets": profile.get("targets", []),
        "evidence": profile.get("evidence", []),
        "shared_standards": profile.get("shared_standards", []),
        "family_expectations": profile.get("family_expectations", []),
        "evidence_gaps": profile.get("evidence_gaps", []),
        "signal_samples": {
            "accessibility": context.get("accessibility_signal_samples", []),
            "localization": context.get("localization_signal_samples", []),
            "design_system": context.get("design_system_signal_samples", []),
        },
    }


def _divide_and_conquer_strategy(context: dict[str, Any], scoped_review: bool) -> list[str]:
    strategy = [
        "Start with root-level summaries; do not ask one model to reason over the entire repository in raw form.",
        "Review one included root or one tightly-coupled root cluster per deep-dive, then merge the summaries.",
        "Feed the architecture corroboration pass a condensed evidence packet built from root summaries, docs, diagrams, and tool outputs instead of raw full-repo dumps.",
    ]

    strategy.append("If the task is change-focused, start with delta/impact analysis and re-read unaffected roots only when dependency evidence makes them relevant.")

    if context.get("ui_present"):
        strategy.append(
            "Run the UX lane only on user-facing roots and give it the compact platform_ux_review_brief rather than the full repo context."
        )
    if context.get("scope_mode") == "scoped":
        strategy.append("Keep excluded roots visible, but do not expand the review scope unless cross-scope evidence proves the dependency matters.")
    if context.get("source_file_count", 0) > 400 or len(context.get("source_root_details", [])) > 4:
        strategy.append("Prefer summary-first multi-prompting with follow-up hotspot passes over one giant prompt for large repositories.")

    strategy.append("Use critic/adversarial passes to challenge missing coverage, shaky inferences, and unsupported findings before synthesis.")
    return strategy


def _risk_ranked_lane_order(context: dict[str, Any], review_lanes: list[str]) -> list[str]:
    order = []
    preferred = [
        "system-understanding",
        "whole-repo-coverage",
        "scoped-coverage",
        "architecture",
        "architecture-driver-alignment",
        "clean-architecture",
        "dependency-boundaries",
        "flutter-specific",
        "security-hygiene",
        "performance-risk-scan",
        "ui-ux",
        "platform-ux-fit",
        "persona-ux",
        "implementation-quality",
        "tool-and-diagram-corroboration",
        "evidence",
    ]
    for lane in preferred + review_lanes:
        if lane in review_lanes and lane not in order:
            order.append(lane)
    return order


def build_outline(context: dict[str, Any]) -> dict[str, Any]:
    ecosystems = set(context.get("ecosystems", []))
    ui_present = bool(context.get("ui_present"))
    platform_profile = context.get("platform_profile", {})
    platform_families = platform_profile.get("families", [])
    source_language_count = _source_language_count(context)
    source_file_count = int(context.get("source_file_count", 0))
    scope_mode = context.get("scope_mode", "whole-repo")
    scoped_review = scope_mode == "scoped"
    platform_ux_review_brief = _platform_ux_review_brief(context)

    review_lanes = [
        "system-understanding",
        "scoped-coverage" if scoped_review else "whole-repo-coverage",
        "architecture",
        "architecture-driver-alignment",
        "implementation-quality",
        "evidence",
    ]
    recommended_skills: list[str] = []
    questions = [
        "What is the intended architecture or product shape of this repository?",
        "Which modules or flows are the most critical for maintainers or end users?",
        "Does the current architecture appear to support the system's likely goals and quality attributes?",
    ]
    evidence_targets = [
        "manifests",
        "source roots",
        "README and product docs",
        "docs or ADRs",
        "diagram samples",
        "tooling artifacts or static-analysis outputs",
        "candidate validation commands",
    ]
    fallback_notes = []
    human_follow_up_questions = _human_follow_up_questions(context)

    if scoped_review and not context.get("scope_resolved", True):
        fallback_notes.append(
            "The requested scope did not resolve to concrete source roots. Keep the review fail-closed until the team confirms the intended subtree."
        )

    if len(context.get("source_root_details", [])) > 1 or source_language_count > 2 or source_file_count > 250:
        review_lanes.append("codebase-mapping")
        recommended_skills.append("codebase-map")

    review_lanes.extend(["clean-architecture", "dependency-boundaries"])
    recommended_skills.extend(["clean-architecture-review", "dependency-boundary-check"])

    if "flutter" in ecosystems:
        review_lanes.append("flutter-specific")
        recommended_skills.append("flutter-best-practices")
        questions.append("How are widgets, state management, theming, and shared UI primitives organized?")

    if ui_present:
        review_lanes.append("ui-ux")
        recommended_skills.append("premium-ui-ux")
        questions.append("Do the visible flows feel coherent, accessible, and product-specific?")
        if platform_families:
            review_lanes.append("platform-ux-fit")
            questions.append(
                f"Do the architecture and UX choices support the expectations of the shipped platforms ({', '.join(platform_families)}) without forcing one generic interaction model everywhere?"
            )
            questions.append(
                "Are accessibility, contrast, and localization treated as first-class product requirements across the detected user-facing platforms?"
            )
            evidence_targets.append("platform profile and compact UX-standard signals")
            fallback_notes.append(
                "Keep platform-aware UX review focused on detected platform families and signal samples instead of dumping the entire UI knowledge base into one prompt."
            )

    if ui_present and _has_persona_signals(context):
        review_lanes.append("persona-ux")
        recommended_skills.append("persona-ux-review")
        fallback_notes.append(
            "If persona-ux-review is unavailable, keep user-journey, copy, and trust checks inside premium-ui-ux."
        )

    if context.get("performance_signals") or source_file_count > 1500:
        review_lanes.append("performance-risk-scan")
        recommended_skills.append("performance-regression-scan")

    if context.get("security_signals"):
        review_lanes.append("security-hygiene")
        fallback_notes.append(
            "Security-sensitive paths were detected; if no dedicated security skill is available, cover secrets, auth, injection, and trust-boundary risks manually."
        )

    if context.get("tooling_artifact_samples") or context.get("diagram_samples"):
        review_lanes.append("tool-and-diagram-corroboration")

    if "flutter" in ecosystems and context.get("apple_targets_present"):
        fallback_notes.append(
            "If the user later asks about Apple shipping or App Store readiness, add apple-guidelines-review."
        )

    fallback_notes.append(
        "Architecture conclusions should be synthesized from two parallel model passes: GPT-5.4 and Claude Sonnet 4.6."
    )
    fallback_notes.append(
        "If one of the two required architecture model passes is unavailable, keep the review running but state degraded architecture confidence explicitly."
    )

    deduped_skills: list[str] = []
    seen = set()
    for skill_name in recommended_skills:
        if skill_name not in seen:
            deduped_skills.append(skill_name)
            seen.add(skill_name)

    deduped_lanes: list[str] = []
    seen_lanes = set()
    for lane in review_lanes:
        if lane not in seen_lanes:
            deduped_lanes.append(lane)
            seen_lanes.add(lane)

    return {
        "root": context["root"],
        "review_scope": {
            "mode": scope_mode,
            "requested_roots": context.get("requested_scope_roots", []),
            "requested_ecosystems": context.get("requested_scope_ecosystems", []),
            "included_roots": context.get("included_scope_roots", context.get("source_roots", [])),
            "excluded_roots": context.get("excluded_scope_roots", []),
            "notes": context.get("scope_notes", []),
        },
        "review_lanes": deduped_lanes,
        "review_order": _risk_ranked_lane_order(context, deduped_lanes),
        "recommended_skill_invocations": deduped_skills,
        "divide_and_conquer_strategy": _divide_and_conquer_strategy(context, scoped_review),
        "whole_repo_strategy": [
            (
                "Map the included scope roots before deep reading and keep excluded roots visible."
                if scoped_review
                else "Map the repository at source-root level before deep reading."
            ),
            (
                "Summarize every included coverage target briefly before diving into hotspots."
                if scoped_review
                else "Summarize every coverage target briefly before diving into hotspots."
            ),
            "Cross-check code with README/docs/ADRs, diagrams, and existing tool outputs when present.",
            (
                "If scoped, keep cross-scope dependencies visible but do not silently expand the review beyond the agreed scope."
                if scoped_review
                else "Use targeted deep-dives for hotspots, boundary violations, and user-facing flows."
            ),
            "Synthesize architecture, implementation, security, and UI/UX into one verdict rather than separate mini-reviews.",
        ],
        "coverage_targets": _coverage_targets(context),
        "explicit_assumptions_to_confirm": [
            "The likely product goals inferred from README or UI copy are actually the goals the team cares about.",
            "The detected source roots represent the meaningful subsystem boundaries.",
            "If docs and code disagree, the codebase is treated as the primary ground truth unless the user corrects that assumption.",
            (
                "The requested scoped review is intentionally limited to the included roots, and excluded roots should only be mentioned when they materially affect the scoped area."
                if scoped_review
                else "The default review mode is whole-repo unless the user explicitly narrows the target."
            ),
        ],
        "architecture_review_protocol": {
            "required_parallel_models": ["gpt-5.4", "claude-sonnet-4.6"],
            "required_sections_per_model": [
                "architecture style and boundaries",
                "business goals / quality-attribute alignment",
                "decision-rationale hypotheses and missing evidence",
                "top risks and contradictions",
                "open questions for humans",
            ],
            "synthesis_rule": "Keep only shared architecture conclusions as high-confidence. Surface disagreements and unresolved claims explicitly.",
            "degrade_behavior": "If one required model pass is missing, architecture confidence is degraded and must be labeled as such.",
        },
        "questions_to_answer": questions,
        "human_follow_up_questions": human_follow_up_questions,
        "evidence_targets": evidence_targets,
        "candidate_commands": context.get("candidate_commands", []),
        "platform_ux_review_brief": platform_ux_review_brief,
        "ui_samples": context.get("ui_samples", []),
        "readme_samples": context.get("readme_samples", []),
        "architecture_doc_samples": context.get("architecture_doc_samples", []),
        "diagram_samples": context.get("diagram_samples", []),
        "tooling_artifact_samples": context.get("tooling_artifact_samples", []),
        "entrypoint_samples": context.get("entrypoint_samples", []),
        "security_signals": context.get("security_signals", []),
        "fallback_notes": fallback_notes,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print(
            "usage: generate_review_outline.py <repo-path-or-context-json> [--include-root <path>] [--include-ecosystem <ecosystem>]",
            file=sys.stderr,
        )
        return 2
    try:
        if len(sys.argv) == 2:
            context = _load_context(sys.argv[1])
        else:
            parser = argparse.ArgumentParser(add_help=False)
            parser.add_argument("repo_path_or_context")
            parser.add_argument("--include-root", action="append", dest="include_roots", default=[])
            parser.add_argument("--include-ecosystem", action="append", dest="include_ecosystems", default=[])
            args = parser.parse_args()
            path = Path(args.repo_path_or_context).resolve()
            if path.is_dir():
                context = ANALYZE_REPOSITORY(
                    path,
                    include_roots=args.include_roots,
                    include_ecosystems=args.include_ecosystems,
                )
            else:
                if args.include_roots or args.include_ecosystems:
                    print(
                        "scope flags require a repository path; regenerate the context from the repo path instead of passing them with a JSON file",
                        file=sys.stderr,
                    )
                    return 2
                context = _load_context(args.repo_path_or_context)
    except FileNotFoundError:
        print(f"path not found: {sys.argv[1]}", file=sys.stderr)
        return 1

    print(json.dumps(build_outline(context), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
