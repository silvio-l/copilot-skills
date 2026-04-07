---
name: deep-research
description: Conduct multi-phase, evidence-backed deep research for complex, high-stakes, multi-source questions such as technology choices, vendor or tool comparisons, market scans, policy investigations, and decision memos where a quick answer would be too shallow. Use this skill whenever the user asks for deep research, a thorough investigation, a serious comparison, "research this deeply", or wants a ChatGPT-style deep research result with broad source gathering, source-by-source evaluation, official documentation grounding, and a long-form final report. Do not use it for simple fact lookups or narrow single-source questions.
compatibility: Works best with internet access. Prefer web_search and web_fetch; use Context7 and any first-party documentation tools available in the session when the topic involves specific libraries, frameworks, APIs, products, or vendors.
---

# Deep Research

Use this skill when the user wants a real investigation, not a fast answer. The job is to build an evidence base, pressure-test it, and then write a comprehensive synthesis that is clear about what is known, what is inferred, and what remains uncertain.

## Core stance

- Be exhaustive **within scope**, not unbounded.
- Use the full toolset **when it adds signal**, not to check boxes.
- Prefer primary and current sources over recycled summaries.
- Separate facts, interpretation, and speculation.
- Keep one owning line of reasoning. Even if you collect evidence in multiple passes, the final synthesis should feel like one coherent investigation.

## When not to use this skill

Skip this skill for:

- simple fact lookups
- narrow questions answerable from one authoritative source
- straightforward documentation lookups with no real tradeoff analysis
- quick summaries where the user clearly does not want a long research process

## Research workflow

### 1. Frame the research question

Start by turning the user's request into a precise research brief:

- What decision, question, or risk is the user really trying to resolve?
- What constraints matter: time horizon, geography, budget, stack, company size, regulation, audience, or deadline?
- What would count as a useful answer: recommendation, comparison, risk memo, implementation brief, market landscape, or factual dossier?
- What is out of scope?

If a missing variable would materially change the answer and cannot be responsibly inferred, ask one focused clarifying question. If asking is not possible or would stall the work, proceed with explicit assumptions, mark the uncertainty clearly, and keep going.

### 2. Build a research plan before diving in

Break the topic into research tracks. Good tracks often include:

- background and definitions
- current state of the market or ecosystem
- first-party or official guidance
- implementation or operational realities
- criticisms, failure modes, and contrary evidence
- pricing, adoption, maturity, and maintenance signals
- security, compliance, or legal implications when relevant

Write a short internal search plan with:

- the tracks you will investigate
- the kinds of sources you expect to use
- the gaps you need to close before concluding
- stop criteria

### 3. Gather sources in layers

Use layered evidence collection instead of trusting the first few results.

#### Layer A: Broad discovery

Use `web_search` to map the landscape, discover terminology, find current sources, and identify the strongest first-party references.

#### Layer B: Read the actual sources

Use `web_fetch` to inspect promising pages directly rather than relying on search snippets.

#### Layer C: Pull in official docs when the topic is technical

When the topic involves a specific library, framework, API, SDK, product, or cloud service:

- Use Context7 to resolve the library ID and query current documentation before making implementation claims.
- Use any vendor-specific documentation tools available in the session for first-party grounding.
- Use code or repository search tools when ecosystem maturity, maintenance, API surface, or real-world examples matter.

#### Layer D: Incorporate user-provided evidence

If the user supplied files, URLs, code, logs, screenshots, or documents, inspect them and integrate them into the evidence base instead of treating internet research as the only input.

### 4. Score each source explicitly

Do not just list links. Evaluate each source individually.

For every source you rely on, capture:

- **ID**: `S1`, `S2`, ...
- **Source**: title and URL
- **Type**: official docs, vendor page, research paper, regulator, repo, benchmark, news, blog, forum, issue thread, analyst report, etc.
- **Freshness**: publication date or last meaningful update
- **What it supports**: the specific claim or question it informs
- **Quality score**: `1-5`
- **Why that score**: one sentence
- **Bias or incentive**: what might make it slant the story
- **Caveats**: what the source cannot prove on its own

Use this scoring rubric:

- **5** - primary, current, and directly relevant evidence
- **4** - strong secondary source or expert analysis with clear grounding
- **3** - useful but incomplete, somewhat biased, narrow, or aging
- **2** - weak, anecdotal, thinly sourced, or materially stale
- **1** - only useful as a lead; do not lean on it for conclusions

### 5. Look for disconfirming evidence

Deep research is not a pile of supporting citations. Try to break your own emerging thesis.

- Search for opposing views, failures, criticisms, edge cases, and postmortems.
- If one option looks clearly better, actively search for reasons it might not be.
- If sources conflict, surface the conflict instead of flattening it.
- If a claim matters and you only have one weak source, keep digging.

### 6. Keep going until the evidence is mature

Do not stop just because you have enough material to say something.

Stop when most of these are true:

- each major research track has at least one strong primary source or two independent corroborating sources
- the main alternatives or counterarguments have been checked
- important claims are not resting on low-quality sources alone
- new searches are mostly producing repetition rather than materially new angles
- you can explain not just what is true, but why the confidence level is what it is

If strong sources do not exist for part of the topic after targeted searching, treat that as a finding rather than a failure. State that the evidence ceiling is low, explain why, and continue with a constrained conclusion instead of pretending the gap is closed.

### 7. Synthesize into a real answer

Build the final response from claims upward.

- Lead with the direct answer, not the chronology of your search.
- Group findings into themes instead of dumping notes.
- Cite source IDs inline for major claims.
- Make it obvious what is a fact, what is an interpretation, and what is a recommendation.
- If the user needs a decision, actually make or narrow the decision unless the evidence is too weak.
- If the evidence is mixed, explain what would change the conclusion.

## Tooling rules

Use tools intentionally:

- `web_search` for discovery and current information
- `web_fetch` for reading and comparing source content
- Context7 for current library or framework documentation
- first-party documentation search/fetch tools when the topic maps to a known vendor or ecosystem
- repository or code search tools when adoption, maintenance, or API reality matters
- local file inspection tools for user-provided evidence

Do **not** avoid a useful specialized tool just because the web already has summaries. Official docs usually deserve more weight than commentary.

## Output requirements

The final answer should be comprehensive. "Summary" here means synthesis, not aggressive compression.

Use this structure unless the user asks for a different format:

# Research objective

State the exact question you answered.

## Scope and assumptions

- what was included
- what was excluded
- assumptions made to keep the work moving

## Bottom line

Give the direct answer first.

## Findings by theme

Use subsections for each major research track. For each theme:

- the conclusion
- the strongest supporting evidence
- relevant disagreements or caveats
- why the conclusion is strong, medium, or weak

## Option or competitor comparison

When the task involves alternatives, include a side-by-side comparison table with:

- option
- strengths
- weaknesses
- best fit
- risks
- evidence basis

## Source ledger

Include a table for the most decision-relevant sources used in the main answer:

| ID | Source | Type | Freshness | Score | What it supports | Caveats |
|----|--------|------|-----------|-------|------------------|---------|

If the source set is large, keep the main ledger focused on the highest-leverage sources and put the full per-source ledger in an appendix. Still evaluate each relied-on source individually during the research process.

## Conflicts, unknowns, and gaps

State where the evidence is mixed, missing, or too weak for certainty.

## Recommendation or decision guidance

Translate the research into action for the user's context.

## Optional appendix: search paths and discarded leads

Include this when the topic is contentious, high-stakes, or unusually broad. The appendix is also the right place for the full source ledger when the main answer would otherwise become unwieldy.

## Behaviors to avoid

- Do not answer from memory alone when the user explicitly asked for research.
- Do not trust one source when the decision matters.
- Do not over-index on SEO listicles or affiliate content if primary sources exist.
- Do not hide uncertainty behind confident prose.
- Do not use every available tool mechanically; use the best tools for the current question.
- Do not stop at consensus if the downside of being wrong is high.

## Example trigger cases

**Example 1**
User: "I need a deep research comparison of managed PostgreSQL options for a small SaaS that might outgrow Supabase in 18 months. Include pricing traps, operational tradeoffs, and migration pain."

**Example 2**
User: "Research this deeply: should our React Native app use RevenueCat or build subscriptions directly for iOS and Android? I want the boring operational truth, not just marketing."

**Example 3**
User: "Can you do a serious research brief on whether local-first sync libraries are mature enough for an Electron note-taking app in 2026? Compare the real contenders and tell me what would worry you."
