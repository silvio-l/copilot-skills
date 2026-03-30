---
name: bug-fix
description: "MUST USE for ANY bug, error, defect, crash, regression, or unexpected behavior. Invoke this skill IMMEDIATELY whenever the task involves fixing, debugging, reproducing, triaging, or explaining undesired software behavior, including stack traces, error messages, failing tests, flaky behavior, Sentry issues, logs, wrong output, or requests like 'doesn't work', 'broken', 'why does this crash', and 'debug this'. Also triggers on German: 'Bug fixen', 'Fehler beheben', 'Fehler analysieren', 'funktioniert nicht', 'geht nicht', 'Absturz', 'Fehlverhalten', 'Regression', 'stuerzt ab', 'debuggen'. This skill REPLACES ad-hoc debugging - never analyze or fix defects without it."
---

# Bug Root Cause & Fix Skill

## Goal

Find the **actual root cause** of a bug and implement a small, robust, architecture-respecting fix. Prove every step with evidence. Never patch symptoms.

## Severity Triage (do this FIRST)

Before entering the full workflow, classify the bug:

| Severity | Criteria | Workflow |
|----------|----------|----------|
| **Trivial** | Cause is immediately obvious from the error message (typo, missing import, wrong variable name). Fix is a 1-3 line change with zero ambiguity. | Skip to **Phase 3** (Fix) → **Phase 4** (Verify). No hypotheses needed. |
| **Standard** | Cause is not immediately obvious, or multiple code paths could be responsible. Requires investigation. | Full workflow: Phase 1–5. |
| **Complex** | Multiple interacting systems, race conditions, intermittent failures, data-dependent bugs, or the bug has been "fixed" before and returned. | Full workflow + mandatory git archaeology (Phase 1c) + mandatory regression test (Phase 4c). |

**Rule: When in doubt, classify as Standard. Never classify as Trivial unless you can name the exact line and the exact fix before reading any code beyond the error message.**

---

## Phase 1 — Understand (never skip)

### 1a. Symptom Capture

Document precisely:
- **Expected behavior**: What should happen?
- **Actual behavior**: What happens instead? (exact error messages, screenshots, logs)
- **Reproduction conditions**: When does it happen? Always? Sometimes? Under what conditions?
- **Impact**: Who/what is affected? How severely? Is there a workaround?

If the user's report is vague, use `ask_user` to fill gaps. Do not proceed with assumptions.

### 1b. Reproduction Attempt

Before analyzing code, try to reproduce the bug:
1. If test infrastructure exists: write a failing test that demonstrates the bug
2. If runnable: execute the failing code path and capture the error
3. If neither is possible: document why and proceed with static analysis

**A reproduced bug is 10x easier to fix correctly. Invest time here.**

### 1c. Git Archaeology (Standard + Complex)

Check what changed recently in the affected area:
```
git log --oneline -20 -- {affected_files}
git log --all --oneline --since="2 weeks ago" -- {affected_files}
```

If a recent commit correlates with when the bug appeared:
```
git show {suspect_commit} -- {affected_files}
```

This often reveals the root cause directly. A bug that appeared after commit X was likely introduced by commit X.

### 1d. Impact Assessment

| Dimension | Assessment |
|-----------|-----------|
| **Severity** | Critical / High / Medium / Low |
| **Scope** | Single user / Feature / Module / System-wide |
| **Frequency** | Always / Often / Rare / Once |
| **Data impact** | None / Read-only / Data corruption risk |
| **Urgency** | Immediate / Next release / Backlog |

---

## Phase 2 — Diagnose

### 2a. Narrow Down

Use at least 2 search strategies to find relevant code:
1. Trace from the error message / stack trace backward
2. Search for the function/module mentioned in the bug
3. Check callers and dependencies of the affected code
4. Review recent changes (from 1c)

### 2b. Form Hypotheses

List **at least 2 hypotheses** (for Standard/Complex), ranked by probability:

```
Hypothesis 1 (most likely): {description}
  Evidence for: {what supports this}
  Evidence against: {what contradicts this}
  How to verify: {specific check}

Hypothesis 2: {description}
  Evidence for: ...
  Evidence against: ...
  How to verify: ...
```

### 2c. Verify Root Cause

**Rule: A hypothesis becomes the root cause ONLY when you can show concrete evidence — a code path, a failing condition, a data state. "I think it's X" is not verification.**

Verification methods (use at least one):
- Trace the exact code path that leads to the bug
- Show the specific line(s) where the defect occurs
- Demonstrate with a test or execution that the hypothesized cause produces the observed symptom
- Show via git blame/log that a change introduced the behavior

### 2d. Root Cause Statement

Write one clear sentence:
> **Root Cause**: {what exactly is wrong} in {where exactly} because {why it happens} when {under what conditions}.

---

## Phase 3 — Fix

### 3a. Solution Design

Develop **at least 3 solution options** (for Standard/Complex):

| Option | Description | Pros | Cons | Risk | Effort |
|--------|-------------|------|------|------|--------|
| **A: Minimal** | Smallest possible change that fixes the symptom at its root | Low risk, fast | May not cover edge cases | Low | Small |
| **B: Robust** | Clean fix that handles the root cause and obvious edge cases | Thorough, maintainable | More code to review | Medium | Medium |
| **C: Defensive** | Robust fix + additional hardening (validation, logging, graceful degradation) | Most resilient | May be over-engineering for the bug | Medium | Larger |

**For Trivial bugs**: One solution is sufficient. Skip the matrix.

### 3b. Selection & Justification

State which option you recommend and why. Consider:
- Does the fix match the severity? (Don't over-engineer a typo fix. Don't under-engineer a data corruption bug.)
- Does it follow existing code patterns?
- Will it be obvious to the next developer why this fix exists?

### 3c. Implementation

- Fix only what needs fixing. No drive-by refactoring.
- Follow existing code patterns in the surrounding code.
- Add a comment only if the fix would be non-obvious to a reader (e.g., "This null check is needed because X can return null when Y, see issue #123").
- If test infrastructure exists: write or update a test that would have caught this bug.

---

## Phase 4 — Verify

### 4a. Fix Verification

Prove the fix works:
1. **If a failing test exists from 1b**: run it — it must pass now
2. **If runnable**: execute the previously-failing code path — it must succeed now
3. **If neither**: explain why runtime verification isn't possible and what static evidence confirms the fix

### 4b. Regression Check

Prove the fix doesn't break anything else:
1. Run the project's existing test suite (or relevant subset)
2. Check IDE diagnostics on changed files AND files that import them
3. Run build/type-check if available

### 4c. Regression Test (Complex bugs — mandatory)

For Complex bugs, a regression test is **required**, not optional:
- Write a test that reproduces the exact conditions of the bug
- The test must fail without your fix and pass with it
- Name it descriptively: `test_should_not_crash_when_X_is_null`, not `test_fix_123`

---

## Phase 5 — Document

### Output Format

Present to the user:

```
## 🐛 Bug Analysis

**Severity**: Trivial / Standard / Complex
**Impact**: {severity} | {scope} | {frequency}

### Root Cause
{One clear sentence from 2d}

### Fix Applied
{What you changed and why — concise}

### Files Changed
- `{file}`: {what changed}

### Verification
- [x] Fix verified: {how}
- [x] No regressions: {how}
- [ ] Regression test added (Complex only)

### Residual Risks
{Any remaining concerns, or "None identified."}
```

---

## Rules (non-negotiable)

1. **No symptom patches without root cause.** Adding a null check "because it crashed" is not a fix — find out WHY the value is null. The null check may be the right fix, but only after you understand the cause.
2. **No guesses presented as facts.** If you're not sure, say so. Use "most likely" or "I suspect" — never "the root cause is X" without evidence.
3. **Prove before you fix.** Identify the root cause before writing fix code. Fixing first and explaining later leads to symptom patches.
4. **Minimal blast radius.** Change only what the fix requires. If you see other issues nearby, note them as separate findings — don't fix them in the same change.
5. **No unnecessary refactoring.** The bug fix is not an opportunity to "improve" surrounding code. Keep the diff focused.
6. **Reproduce first when possible.** A bug you can reproduce is a bug you can verify. Invest in reproduction before analysis.
7. **Check the history.** Bugs rarely appear from nowhere. Recent changes are the most common cause. Always check git log for the affected area.
8. **Test what you fix.** If test infrastructure exists, a fix without a test is incomplete. The test proves the fix works and prevents regression.
