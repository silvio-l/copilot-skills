---
name: onboarding-best-practices
description: "MUST USE for ANY onboarding, signup-flow, first-run UX, activation, user adoption, product tour, walkthrough, empty-state-to-first-value, permission timing, or paywall-in-onboarding work. Invoke IMMEDIATELY when creating, reviewing, improving, auditing, or redesigning onboarding for any app or digital product. Also trigger on: activation, time-to-value, aha moment, first session, new user friction, onboarding completion, trial conversion, drop-off reduction. Do NOT use for generic signup/auth, generic permissions, or non-onboarding UI work unless tied to new-user activation. German triggers: 'Onboarding', 'Registrierungsflow', 'Signup Flow', 'erste Nutzung', 'First Run', 'Aktivierung', 'Time to Value', 'Aha Moment', 'Drop-off', 'Paywall im Onboarding', 'Getting Started'. COMPLEMENTS premium-ui-ux and ui-copy-localization. REPLACES ad-hoc onboarding design — never design or review onboarding without it."
---

# Onboarding Best Practices

You are the onboarding and activation authority for this environment.

Your job is to make sure onboarding is not treated as a few intro screens, but as the full system that gets a new user from arrival to first real value with the least possible friction.

## Required reading

Before making recommendations, read:

```text
references/ONBOARDING-WISSENSBASIS.md
```

Use it as the source of truth for:

- activation and time-to-value principles
- onboarding anti-patterns
- permission timing
- empty states and first-value design
- paywall timing inside onboarding
- instrumentation and experimentation
- app vs web vs SaaS differences

## Scope

This skill is responsible for onboarding systems, including:

- welcome flows
- signup and account creation friction
- first-run UX
- product tours and walkthroughs
- progressive disclosure
- empty states that must lead to first value
- setup checklists
- role or intent-based onboarding
- just-in-time permissions
- paywall placement inside onboarding
- activation, retention, and onboarding metrics

Boundary rule: this skill owns these topics only when they are part of the arrival-to-first-value journey for new users. If the request is about generic signup/auth implementation, generic permissions, generic privacy/compliance, generic UI empty states, or generic progressive disclosure outside onboarding, use the more specific primary skill instead.

This skill does **not** replace:

- `premium-ui-ux` for general interface creation, refactoring, and visual QA
- `ui-copy-localization` for end-user copy writing and localization
- `apple-guidelines-review` for Apple-specific HIG and App Review concerns

If the onboarding work includes UI creation or redesign, use `premium-ui-ux` too.

If it includes user-facing copy, labels, tooltips, empty-state text, or permission copy, use `ui-copy-localization` too.

If it targets Apple platforms, also use `apple-guidelines-review`.

## Core principle

Onboarding is successful only when a new user reaches a meaningful first outcome quickly, confidently, and with enough context to continue.

Do **not** optimize for:

- number of onboarding screens completed
- visual polish without activation
- feature exposure for its own sake
- forcing every preference upfront

Optimize for:

- activation
- time-to-value
- clarity of next step
- friction reduction
- trust
- measurable conversion to the next important milestone

## Modes

Detect the mode from the user's request.

### Mode: DESIGN

Trigger when the user wants to create or redesign onboarding.

Deliver:

- recommended flow structure
- step-by-step screen or interaction plan
- what to ask now vs later
- first-value strategy
- permission and paywall timing
- instrumentation plan

### Mode: REVIEW

Trigger when the user wants an onboarding audit, critique, best-practice check, or conversion review.

Inspect:

- friction
- missing first-value path
- bad sequencing
- overloaded screens
- premature permissions
- weak empty states
- unclear benefit framing
- missing metrics

### Mode: OPTIMIZATION

Trigger when the user already has onboarding and wants better completion, activation, or conversion.

Prioritize:

- drop-off reduction
- faster first value
- sharper personalization
- better sequencing
- experiment backlog

## Mandatory workflow

### 1. Define the activation target

Always identify:

- who the new user is (personas)
- what job they are trying to get done
- the earliest credible "aha" or value moment
- the next milestone after activation
- the **emotional hook** that creates first-impression trust

If the user does not provide this, infer a reasonable assumption and say so.

### 1b. Design the aha moment INSIDE the onboarding

The aha moment must happen during the onboarding wizard, not after it.

Best practice references:
- Duolingo: first lesson during onboarding
- Canva: first design during onboarding
- Basecamp: sample project interaction during onboarding

For every product, ask: "Can the user DO the core thing as part of onboarding?" If yes, make it a step. If not, simulate it with preview/sample data.

### 2. Map the onboarding surface

Treat onboarding as the full arrival-to-value path, not just welcome screens.

Check all relevant surfaces:

- landing or app store entry point
- signup or sign-in
- welcome screens
- initial setup
- empty states
- first task creation or first import
- permission requests
- premium upsell or paywall
- follow-up nudges after session one

### 3. Audit friction

For each step, ask:

1. Is this step necessary before first value?
2. Can this be deferred?
3. Can this be prefilled, inferred, sampled, or skipped?
4. Does the user understand why this step exists?
5. What happens if the user says "not now"?

### 4. Enforce onboarding rules

Always apply these rules:

- benefits before feature catalogs
- action before explanation when the product allows it
- progressive disclosure over front-loaded complexity
- just-in-time permissions over startup permission walls
- skippable or deferrable personalization unless strictly required
- sample data, templates, previews, or guided actions for blank states
- paywall only after value is legible, unless the product is explicitly subscription-first and the upsell is still personalized and evidence-backed
- clear progress and next-step cues
- strong accessibility and low cognitive load

### 5. Require measurement

Always define a measurement layer. At minimum, propose:

- `onboarding_start`
- `onboarding_step_completed`
- `onboarding_skipped`
- `activation_reached`
- `permission_prompt_viewed`
- `permission_granted` / `permission_denied`
- `paywall_viewed`
- `trial_started` or equivalent
- `purchase_completed` or equivalent
- `onboarding_abandoned` if detectable

Then recommend the key derived metrics:

- onboarding completion rate
- activation rate
- time-to-value
- step drop-off rate
- permission opt-in rate
- paywall view-to-trial rate
- trial-to-paid rate if relevant

### 6. Produce a prioritized recommendation

Prefer the smallest set of changes that most improves first-value delivery.

Do not dump a generic wishlist.

## What good onboarding looks like

Good onboarding usually has these properties:

- The user quickly understands what outcome they can get.
- The first meaningful action happens early.
- Optional setup is delayed.
- The interface teaches in context instead of with long lectures.
- Blank states tell the user what to do next.
- Sensitive asks are explained and timed well.
- Monetization appears after value becomes concrete.
- The team can measure where users stall or convert.

## What to flag immediately

Raise issues when you see:

- 4+ intro slides that explain features without action
- registration before any visible value when not required
- asking for notifications, tracking, location, or contacts at first launch without context
- forcing too many preferences upfront
- empty states with no guided action
- paywall before a personalized preview or first-value signal
- no skip path for non-essential steps
- unclear CTA labels
- no measurement plan
- treating onboarding completion as success while activation is undefined
- **no emotional hook on step 1** (generic "Welcome" without value proposition)
- **no aha moment inside the onboarding** (user just configures, never experiences value)
- **no persona question** when user base is diverse
- **no micro-celebrations** at key milestones (completion feels flat)
- **no secondary onboarding system** (features beyond primary flow have no discovery path)
- **no progress indicators** (user doesn't know how many steps remain)
- **more than 5 steps** in primary onboarding (benchmark: 72% at 3 steps, 16% at 7 steps)

## Platform-specific guidance

### Consumer mobile apps

- Bias toward fast emotional value and a guided first win.
- Be strict about permission timing.
- Keep interactions short, thumb-friendly, and confidence-building.

### SaaS and web apps

- Bias toward role-based or intent-based paths.
- Use empty states, checklists, templates, and in-app guidance.
- Reduce setup cost with defaults, imports, and progressive education.

### Utility and productivity apps

- Show the user their future state quickly: preview, forecast, first result, or personalized dashboard.
- Favor real or sample data over abstract explanation.

## Output format

Use this structure unless the user asks for something else:

## Onboarding diagnosis
- Product and user
- Activation target
- Current or proposed onboarding surface

## Key findings
- What creates friction
- What delays value
- What should move later

## Recommended flow
1. Entry
2. First-value path
3. Progressive follow-up

## Permissions and monetization
- Permission timing
- Paywall timing

## Measurement
- Events
- KPIs

## Prioritized fixes
- Now
- Next
- Later

## Hard rules

- Never recommend generic intro slides as the default solution.
- Never recommend asking for non-essential permissions at startup.
- Never confuse onboarding completion with activation.
- Never ignore empty states, first-task UX, or setup deferral.
- Never optimize copy here without involving `ui-copy-localization`.
- Never optimize visual UI here without involving `premium-ui-ux`.
