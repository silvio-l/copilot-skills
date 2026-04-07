# Evidence Bundle Template

Use this template whenever the review is important enough that the user will act on it.

## Evidence rules

Every major finding needs:

1. **Finding**
2. **Why it matters**
3. **Evidence**
4. **Confidence**
5. **Recommended action**

If any of these are missing, the finding is not ready.

Additional rule for architecture findings:

- high-confidence architecture findings should be supported by at least two corroborating signals,
- and, when the skill runs its architecture protocol, should survive the mandatory GPT-5.4 + Claude Sonnet 4.6 corroboration step.
- architecture findings should also state `architecture_corroboration_status` as `shared`, `disputed`, or `degraded`.

## Confidence scale

| Confidence | Meaning |
|---|---|
| High | Directly proven by code, config, tool output, or multiple corroborating signals |
| Medium | Strongly suggested by structure or docs, but still partly inferred |
| Low | Plausible but not yet sufficiently evidenced; present as a question or hypothesis |

## Final section template

```markdown
## Evidence bundle

| Finding | Why it matters | Evidence | Confidence | Recommended action |
|---|---|---|---|---|
| ... | ... | `path/to/file.ext`, manifest, helper-script output, or tool result | High / Medium / Low | ... |
```

## Acceptable evidence examples

- `lib/features/editor/editor_page.dart` uses direct repository calls inside widgets
- `pubspec.yaml` + `lib/core/widgets/` show duplicated UI primitives without shared abstraction
- `package.json` scripts expose `test`, but the repo lacks tests in the affected feature
- helper script identifies Flutter + user-facing screens + settings flow, so UI/UX lane is in scope
- a static-analysis or SARIF result proves a cycle, injection risk, or rule violation and therefore outranks unsupported LLM guesswork

## Uncertainty rule

If the repository does not expose enough evidence, say that clearly:

```markdown
Evidence gap: No ADRs or architecture docs were found, so decision intent had to be inferred from structure only.
```

When architecture models disagree:

```markdown
Architecture disagreement: GPT-5.4 and Claude Sonnet 4.6 did not reach the same conclusion about the boundary between `X` and `Y`, so the claim remains medium-confidence pending human clarification.
```

## Validation blocker rule

When a finding is really about blocked validation rather than a proven product defect, mark it explicitly:

```json
{
  "finding_type": "validation-blocker",
  "claim": "Static validation is currently blocked by the available toolchain.",
  "attribution_scope": "environment",
  "primary_evidence": [
    "command output",
    "package config or lockfile evidence"
  ]
}
```

Allowed `attribution_scope` values:
- `repo`
- `environment`
- `unknown`

Do not present environment-blocked or unknown-blocked validation findings as proven repository defects.
