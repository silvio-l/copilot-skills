# Onboarding Wissensbasis

This file is the reference for onboarding, activation, and first-run UX work.

## 1. First principles

Onboarding is the system that moves a new user from curiosity to first meaningful value.

The real unit of success is **activation**, not exposure.

### Key terms

- **Activation**: the first meaningful outcome that predicts ongoing use.
- **Time-to-value (TTV)**: how long it takes a new user to reach that outcome.
- **Aha moment**: the point where the product's usefulness becomes obvious.
- **Progressive disclosure**: revealing complexity when the user needs it, not all at once.

## 2. What current best practice converges on

Across recent product guidance, onboarding teardowns, and case-study style videos, the strongest recurring patterns are:

1. Reduce friction before adding delight.
2. Get to a credible first win quickly.
3. Ask only for what is needed now.
4. Teach in context, not only with lectures.
5. Use empty states, templates, previews, and seeded examples to prevent dead ends.
6. Time permissions to intent.
7. Place monetization after value is legible.
8. Instrument the funnel so the team can iterate with evidence.

## 3. The arrival-to-value model

Do not scope onboarding too narrowly.

Treat these as one system:

1. Acquisition entry point
2. Signup or sign-in
3. Welcome and positioning
4. Initial setup
5. First action
6. Empty state guidance
7. First result or preview
8. Permission prompt
9. Paywall or upgrade moment
10. Follow-up nudge after session one

If any of these fail, onboarding fails.

## 4. Activation design rules

### 4.1 Define the activation event

Before proposing screens, identify the first event that proves value.

Examples:

- Finance app: user sees a personalized monthly remainder forecast.
- Writing app: user creates and revisits a first note.
- Task app: user creates and completes a first task.
- Collaboration SaaS: user creates a project and invites a teammate or completes one workflow.

If activation is vague, recommendations become generic.

### 4.2 Prefer action to explanation

When possible, let the user do the core thing quickly.

Good:

- show a preview based on one or two inputs
- import existing data
- create from template
- seed sample content

Weak:

- long slide decks
- feature lists
- abstract promises with no concrete result

### 4.3 Defer non-essential setup

Every upfront question must justify its cost.

Ask:

- Is this necessary before first value?
- Can it be skipped?
- Can it be inferred later?
- Can a default stand in for now?

Common deferrals:

- theme choice
- optional profile fields
- detailed preferences
- secondary integrations
- advanced settings

## 5. Progressive disclosure

Use layered education:

- first session: only what is needed to succeed
- early follow-up: next useful capability
- advanced stage: power-user guidance

Use:

- contextual tips
- checklist steps
- inline prompts
- empty-state guidance
- milestone-triggered nudges

Avoid:

- front-loading every feature
- making users memorize the product before using it

## 6. Personalization

Personalization helps when it makes first value faster or more relevant.

Good personalization:

- role selection
- intent or goal selection
- simple preference questions with immediate downstream effect
- lightweight ranges or categories instead of exact sensitive data

Bad personalization:

- too many questions before value
- collecting interesting but currently unused information
- making optional segmentation mandatory

Rule: personalize only when the next screen or result becomes better because of it.

## 7. Empty states and dead-end prevention

A blank state is part of onboarding.

Strong empty states:

- explain why nothing is here yet
- provide the next best action
- show an example, sample, or template when useful
- reinforce the value of completing the next step

Weak empty states:

- blank canvas with no instruction
- decorative illustration with vague copy
- CTA that does not explain what happens next

## 8. Permission timing

Default rule: ask for permissions only when the user is trying to do the thing that needs them.

Examples:

- Notifications: ask when the user enables reminders, follows updates, or would otherwise miss clear value.
- Camera: ask when the user starts scan or photo capture.
- Contacts: ask when they explicitly try to invite or share.
- Tracking: never treat as normal onboarding copy; treat as a trust-critical choice with clear benefit and compliance context.

Good permission flow:

1. user intent becomes clear
2. pre-prompt explains user benefit
3. system prompt appears
4. fallback path exists if denied

Bad permission flow:

- launch-time permission walls
- no explanation of benefit
- blocked progression when permission is not essential

## 9. Paywall timing and monetization

The safest default is: make value concrete before asking for money.

Good paywall moments:

- after a personalized preview
- after the first result
- after the user configures enough to understand the benefit
- after a meaningful first success

Higher-risk paywall moments:

- before any personalized or experiential value
- before the user understands the outcome
- as a surprise interruption during setup

Nuance:

- some products are explicitly subscription-first
- even then, the paywall should be grounded in credible value, outcome framing, and reduced uncertainty
- "pay first, trust later" is usually weak onboarding unless the brand and proposition are already strong

## 10. Metrics and instrumentation

Minimum event layer:

- onboarding_start
- onboarding_step_completed
- onboarding_skipped
- onboarding_completed
- activation_reached
- activation_time_seconds
- permission_prompt_viewed
- permission_granted
- permission_denied
- paywall_viewed
- trial_started
- purchase_completed

Core KPIs:

- onboarding completion rate
- activation rate
- median time-to-value
- per-step drop-off
- permission opt-in rate
- paywall view-to-trial rate
- trial-to-paid rate
- day-1 and day-7 retention of activated vs non-activated cohorts

If a recommendation does not say how to measure success, it is incomplete.

## 11. Common anti-patterns

Flag these immediately:

1. Intro slides with no interaction and no outcome.
2. Explaining every feature before the user can do anything.
3. Registration or login before any visible value when not required.
4. Startup permission prompts without context.
5. Forcing lots of preferences upfront.
6. No skip path for optional steps.
7. Empty states with no guided next action.
8. Paywall before value becomes concrete.
9. CTA labels that hide consequences.
10. No funnel metrics, so the team cannot learn.

## 12. Product-type adjustments

### Mobile consumer apps

- optimize for emotional clarity and speed
- keep first-run interactions compact
- avoid modal overload
- be especially careful with permissions and trial prompts

### SaaS and B2B onboarding

- segment by role, team maturity, or job-to-be-done
- rely more on templates, imports, checklists, and guided setup
- optimize the path to the first team-level or workflow-level success

### Utility and forecast-style products

- a personalized preview is often the activation event
- use inputs to generate a result early
- the user should see "their future state" before being asked for too much

## 13. Evidence distilled from local synthesis and current sources

### Local synthesis highlights

The supplied growth strategy synthesis strongly reinforces:

- onboarding is often the primary revenue lever
- short, preference-only onboarding is usually too weak
- personalization plus a "magic moment" preview is powerful
- paywall timing should follow a meaningful preview or first-value moment
- step analytics and funnel instrumentation are mandatory

### Recent external themes

Recent articles and teardowns repeatedly converge on:

- activation over completion
- first value in the earliest possible session
- progressive disclosure over front-loaded teaching
- just-in-time permissions
- empty states as activation surfaces
- experimentation and analytics over opinion-driven onboarding

### YouTube signals reviewed for this task

- `The app onboarding secrets that convert (proven strategies)` - emphasizes lowering friction and making value legible before monetization.
- `How to get your first 100 PAID app users (my paywall strategy)` - reinforces paywall timing after clearer user value and milestones.
- `Figma Mobile App Onboarding Screen UI Design Tutorial` - useful for flow anatomy, but visual polish must still serve activation, not just aesthetics.

## 14. Recommended review checklist

When reviewing onboarding, always answer:

1. What is the activation event?
2. How quickly can a user get there?
3. What steps are unnecessary before that?
4. Where does the user hit a dead end?
5. Are permissions well timed?
6. Is monetization too early, too late, or ungrounded?
7. Can the team measure each important drop-off?

If you cannot answer these, the onboarding recommendation is not ready.
