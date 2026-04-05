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

## 13. Emotional hook and first impression

The emotional hook is the single most impactful element of step 1. It must:

- Make users feel they made the right choice (trust + validation)
- Create an emotional connection to the product's promise
- Be warm, personal, and on-brand — not clinical or generic
- Use visual delight (logo animation, brand colors, micro-interactions)

Good emotional hooks:

- "Welcome to [Product] — your voice, your words, anywhere" (outcome-focused)
- Persona question: "What brings you here?" (user feels seen)
- Brief value proposition that speaks to the user's pain, not the product's features

Bad emotional hooks:

- Generic "Welcome to [Product]" with no context
- Feature lists on the first screen
- Technical jargon or configuration upfront

Reference: Canva asks "What will you be using Canva for?" on screen 1, immediately personalizing the experience and making users feel the product is built for them. Wistia asks "What's your main goal with Wistia?" — same principle.

## 14. The aha moment — science and application

### Definition

The aha moment is the pivotal point where a new user first realizes the value of the product. It's emotional, memorable, and the switch that turns an evaluating user into an activated user.

### Psychology (Kahneman)

- **System 1 (fast, emotional, intuitive)**: The aha moment must feel good instantly — a visual result, a successful outcome, a micro-celebration.
- **System 2 (slow, analytical, deliberate)**: After the emotional spark, reinforce with logic — "This saved you X seconds", "Your text is ready to paste".

Effective onboarding engages System 1 FIRST (emotional quick win), then System 2 (logical reinforcement).

### Critical insight: The aha moment must happen INSIDE the onboarding

The most successful onboardings don't just set up the product — they deliver the first real success during the wizard itself.

- **Duolingo**: You complete your first lesson during onboarding, not after.
- **Canva**: You create your first design during onboarding, not after.
- **Basecamp**: You interact with sample projects during onboarding.

For desktop productivity/utility apps: the user should perform the core action (record → see result) as part of onboarding, not just configure settings and hope they come back.

### Finding your aha moment

1. Identify behaviors that correlate with retained users (not churned users)
2. Validate with user feedback ("What got you excited?")
3. Design onboarding to reach that behavior as fast as possible
4. Measure: does reaching this moment predict day-7/day-30 retention?

## 15. Gamification and progress psychology

### Zeigarnik Effect

Incomplete tasks linger in the mind, creating an urge to complete them. Progress indicators ("Step 2 of 4") leverage this — users feel compelled to finish.

### Endowed Progress Effect

Showing even a small head start increases motivation. If step 1 is already "complete" when step 2 loads, users feel closer to the goal.

### Practical applications

- Progress dots/bar with current step highlighted
- Checklist items that check off with micro-animations
- Milestone celebrations (confetti, checkmark animation, success message) when key actions complete
- "You're almost there!" messaging near the final step

### Benchmark data (Chameleon 2024)

- 3-step tours: **72% completion rate**
- 7-step tours: **16% completion rate**
- Sweet spot: **3–5 steps** for products requiring setup

## 16. Three-stage onboarding model

### Primary onboarding (signup → activation)

The initial wizard. Goal: reach the aha moment.

Surfaces: welcome screen, setup wizard, first action, first result.

### Secondary onboarding (activation → feature adoption)

Triggered after the user has experienced first value. Goal: discover advanced features.

Surfaces: contextual tooltips, feature callout banners, in-app tip banners, empty-state guidance, one-time badges in settings.

Examples:

- After first transcription: "Tip: Enable Smart Mode to polish your text automatically"
- On first visit to Settings: Info badges next to unexplored features
- On empty History page: Action cards ("Start your first recording", "Try Smart Mode")

### Tertiary onboarding (adoption → mastery)

For power users. Goal: unlock full potential.

Surfaces: keyboard shortcut hints, advanced setting explanations, "Did you know?" tooltips.

## 17. Persona-based personalization

### When to personalize

Personalize only when the next screen or result becomes better because of it.

### How to implement

1. Ask a lightweight persona question on step 1 ("What brings you here?")
2. Map personas to different defaults, copy, and emphasis:
   - **Content Creator**: Emphasize quality, Smart Mode, hands-free dictation
   - **Office/Admin**: Emphasize reliability, speed, paste-anywhere
   - **Developer**: Emphasize keyboard shortcuts, local privacy, API options
   - **General**: Balanced defaults
3. Do NOT create entirely different flows — same structure, different emphasis and defaults

### Key references

- **Twilio**: Developer vs non-developer split on screen 1 → completely different paths
- **Canva**: "What will you use Canva for?" → tailored templates
- **Duolingo**: Beginner vs experienced → different lesson difficulty

## 18. Evidence distilled from research (2024-2026)

### Benchmark data

- 40-60% of SaaS users sign up once and never return (Intercom)
- 25% of mobile app users abandon after one use (Appcues)
- Effective onboarding increases customer retention by 50% (BusinessDasher)
- 86% of customers are more loyal when provided educational onboarding (OnRamp)
- Multi-button surveys: 40.2% completion rate; NPS surveys: 10% (Chameleon 2024)

### Strongest patterns across all sources

1. **Activation over completion** — completing onboarding ≠ success; reaching aha moment = success
2. **First value in earliest session** — don't defer the core experience
3. **Emotional hook before configuration** — make users feel welcome before asking for settings
4. **Progressive disclosure over front-loaded teaching** — reveal features when needed
5. **Just-in-time permissions** — ask when the user is trying to do the thing
6. **Empty states as activation surfaces** — blank pages = onboarding failure
7. **Micro-celebrations at milestones** — confetti, checkmarks, success messages
8. **Secondary onboarding via contextual hints** — tooltips, banners, badges after primary flow
9. **Experimentation and analytics** — measure every step, A/B test flows
10. **Skip option for power users** — respect autonomy, never trap users

### Sources

- Appcues: user onboarding best practices + aha moment guide (2024)
- Userpilot: 7 best practices + primary/secondary/tertiary model (2025)
- Chameleon: 12 best practices + benchmark report (2024)
- HubSpot: customer onboarding process workflow (2025)
- Chameleon benchmark: tour completion rates by step count (2024)

## 19. Recommended review checklist

When reviewing onboarding, always answer:

1. What is the activation event (aha moment)?
2. Does the user EXPERIENCE first value during onboarding (not just configure it)?
3. Is there an emotional hook on step 1?
4. How quickly can a user get to the aha moment?
5. What steps are unnecessary before that?
6. Is there persona-based personalization?
7. Are there micro-celebrations at key milestones?
8. Where does the user hit a dead end?
9. Are permissions well timed (just-in-time)?
10. Is monetization too early, too late, or ungrounded?
11. Can the team measure each important drop-off?
12. Is there a secondary onboarding system for post-activation feature discovery?
13. Can power users skip?
14. Are progress indicators visible (dots, bar, step count)?

If you cannot answer these, the onboarding recommendation is not ready.
