# Apple Guidelines Wissensbasis

This file distills the Apple Human Interface Guidelines (HIG), the App Store Review Guidelines, and Apple's App Review prep guidance into an audit model that is safe to use during code review.

## Source hierarchy

Use sources in this order:

1. App Store Review Guidelines  
   `https://developer.apple.com/app-store/review/guidelines/`
2. Human Interface Guidelines  
   `https://developer.apple.com/design/human-interface-guidelines/`
3. App Review prep / submission guidance  
   `https://developer.apple.com/distribute/app-review/`

If the repo suggests a rule and Apple docs do not clearly support it, do not invent a rule.

## Non-guarantee rule

This skill reduces rejection risk. It does not certify approval.

Apple review depends on more than source code:

- App Store Connect metadata
- screenshots and previews
- age ratings
- privacy nutrition labels
- review notes
- demo accounts and backend readiness
- legal paperwork and licenses
- storefront-specific policy exceptions
- runtime behavior during review

Always keep these separate from code-backed findings.

## Evidence classes

### Code-verifiable

Use this only when the repo itself proves the point.

Examples:

- missing `Info.plist` purpose strings for sensitive APIs
- third-party login SDKs present with no Sign in with Apple implementation signals
- account creation flows with no account deletion path in code
- external payment SDKs or checkout flows without StoreKit signals
- background modes declared in `Info.plist`
- private framework references
- ad or tracking SDKs without ATT-related disclosure/config signals

### Partial

Use this when the repo strongly suggests the risk, but business context still matters.

Examples:

- third-party login may not be the app's primary account
- external payment may be for physical goods or person-to-person services
- a WebView-heavy app may still provide enough native value
- ads may be contextual rather than tracked
- tracking SDKs may be configured in limited, compliant ways

### Manual

Use this when code cannot settle the question.

Examples:

- screenshots or previews overstating features
- metadata category or age rating
- review notes completeness
- demo account availability
- privacy policy wording
- licensing documents, healthcare/finance approvals
- storefront-specific entitlement use

## HIG review lenses

## 1. Native feel and system conventions

Ask:

- Does the app use platform-appropriate navigation and controls?
- Does it feel like an Apple app rather than a generic web shell?
- Does it preserve expected system behaviors instead of fighting them?

Signals:

- custom navigation patterns replacing obvious native flows
- heavy WebView usage as the main experience
- login, settings, or paywall flows that feel detached from the platform

## 2. Clarity, deference, depth

Use these as design review principles, not as decorative slogans.

- **Clarity**: text, icons, hierarchy, and actions are understandable
- **Deference**: chrome does not overpower content
- **Depth**: layering and transitions communicate structure

From code, this is usually partial evidence:

- excessive modal stacking
- opaque overlays blocking content
- confusing nested navigation
- gesture or interaction traps

## 3. Accessibility

This is both HIG and review risk.

Check for:

- meaningful accessibility labels / semantics
- support for Dynamic Type or scalable text
- visible focus states where relevant
- reduced-motion awareness when heavy motion exists
- sufficient hit targets for custom controls
- contrast-safe color choices and not color-only status signaling

High-value code clues:

- icon-only buttons with no accessibility label
- custom gesture surfaces with no keyboard or focus affordance
- hardcoded tiny frames on interactive controls
- blanket disabling of motion or focus handling

## 4. Permission timing and trust

Apple cares about both the presence of permission strings and the user experience around them.

Check:

- sensitive resource use is paired with clear `Info.plist` purpose strings
- the app requests access when the feature is invoked, not speculatively on launch
- alternatives exist when the user declines access where practical

Code can prove missing or weak strings. Code usually cannot fully prove prompt timing or copy quality, so keep those partial when needed.

## 5. Authentication experience

When an app uses third-party login for the primary account, App Review guideline `4.8` becomes hot.

Audit:

- Google/Facebook/X/LinkedIn/Amazon/WeChat login presence
- Sign in with Apple implementation presence
- parity in the user-facing login experience

Code can often prove implementation presence or absence. Equal prominence is usually partial unless UI code is explicit.

## 6. Destructive and sensitive actions

Check for:

- account deletion
- destructive content deletion
- recording or screen capture flows
- subscription purchase / cancellation disclosures

Apple expects destructive or privacy-sensitive flows to be understandable and not deceptive.

## App Review rules that map well to code

| Rule | Why it matters | Strong repo signals | Typical fix |
| --- | --- | --- | --- |
| `2.1 App Completeness` | Incomplete apps are rejected quickly | placeholder text, dead URLs, debug/demo-only logic, obvious TODO surfaces | remove placeholders, enable backend, provide demo account and review notes |
| `2.3.1 Hidden Features` | Dormant or undocumented behavior triggers distrust | hidden flags, undocumented routes, debug menus shipping in release paths | document or remove hidden paths, expose review steps in notes |
| `2.5.1 Public APIs` | Private APIs are a hard rejection risk | `PrivateFrameworks`, suspicious private symbols | remove private API usage and use public frameworks |
| `2.5.2 Self-contained app` | Downloading code that changes features is risky | OTA/code-push frameworks, bundle swapping, dynamic loaders | move feature changes into reviewed binaries |
| `2.5.4 Background modes` | Apple rejects unjustified background behavior | `UIBackgroundModes` entries such as audio, location, VOIP | keep only justified modes and document the use case |
| `2.5.6 WebKit` | Browser-like apps must use approved engine paths | custom browser engine signals, web container patterns | confirm WebKit usage or entitlement status |
| `2.5.14 Recording consent` | Recording requires explicit consent and indication | screen capture, audio capture, camera recording flows | add clear consent UX and visible recording signals |
| `2.5.18 Ads` | Ads have placement and targeting limits | ad SDKs, ads in extensions/widgets, targeted tracking | keep ads in the main app, add ATT where needed, provide reporting and skip/close affordances |
| `3.1.1 IAP` | Digital goods must use IAP unless an exception applies | Stripe/PayPal/Braintree checkout for digital unlocks | move digital purchases to StoreKit or document a valid exception |
| `3.1.2 Subscriptions` | Subscriptions need ongoing value and clear disclosure | recurring paywalls, subscription copy, entitlement logic | clarify value, upgrade/downgrade, renewal and cancellation details |
| `4.2 Minimum Functionality` | Thin wrappers and low-value apps are commonly rejected | WebView-first shells, mostly-link directories, no native value | add native utility, deeper workflows, device-appropriate UX |
| `4.4 Extensions` | Extensions have extra constraints | keyboard, Safari, widget, App Clip, notification extensions | verify extension-specific limits and remove ads/IAP where disallowed |
| `4.8 Login Services` | Third-party login often requires Sign in with Apple | Google/Facebook/etc. auth with no Apple auth path | add Sign in with Apple or document a valid exemption |
| `4.9 Apple Pay` | Apple Pay requires correct disclosure and branding | Apple Pay button or APIs | ensure full purchase details and cancellation disclosure for recurring payments |
| `5.1.1 Privacy` | Privacy failures are a major rejection source | missing purpose strings, no deletion path, unnecessary login, overbroad data access | minimize data, add deletion flow, fix permission strings, remove forced login where invalid |
| `5.1.2 Data Use and Sharing` | Tracking and third-party sharing require consent | ATT-related SDKs, ad/tracking SDKs, analytics tied to personal data | add ATT where required, tighten sharing, disclose AI/third-party data flows |

## Highest-value audit paths

### Login services

Hot when repo shows:

- Google Sign-In
- Facebook Login
- social auth via Firebase/Auth providers

Questions:

- Is this the user's primary account?
- Is Sign in with Apple implemented?
- Is the Apple option equivalent in access and not visually hidden?

### Account deletion

Hot when repo shows:

- registration or account creation
- auth-protected user profile
- backend user records

Questions:

- Can the user initiate deletion in-app?
- Is deletion obvious enough to satisfy `5.1.1(v)`?
- Does the flow revoke connected social credentials where relevant?

### Payments

Hot when repo shows:

- paywalls
- subscriptions
- premium feature unlocks
- checkout SDKs or purchase URLs

Questions:

- Are the goods digital?
- Does StoreKit cover the flow?
- If not, is there a documented exception such as physical goods, reader app, person-to-person service, or approved regional entitlement?

### Permissions and privacy

Hot when repo shows:

- camera, microphone, photos, location, contacts, motion, speech, tracking, health

Questions:

- Is there a matching purpose string?
- Is the purpose string specific and not boilerplate?
- Is the access clearly tied to a user action?
- Is there a lower-privilege alternative such as a picker or manual entry?

### Ads and tracking

Hot when repo shows:

- ad SDKs
- AppsFlyer / Adjust / Facebook SDKs
- ATT-related APIs

Questions:

- Is ATT likely required?
- Are ads likely limited to the main app binary?
- Could the app be using sensitive data for targeted ads?
- Is there any kids-app risk?

### Web wrapper risk

Hot when repo shows:

- `WKWebView`
- `react-native-webview`
- `webview_flutter`
- a small native shell around a site

Questions:

- Is the app mostly a website in a wrapper?
- Does it add real native utility, workflows, or device-specific value?
- Would `4.2` minimum functionality become a review question?

## Manual-only checklist

Always call these out as unresolved if they are relevant and not proven by code:

- App Store screenshots, previews, and marketing copy accuracy
- app category and age rating
- privacy nutrition labels
- privacy policy text and in-app placement
- App Review notes and demo account credentials
- backend uptime and review environment readiness
- legal entity correctness for regulated domains
- healthcare, finance, gambling, air travel, or crypto licensing
- regional entitlement use and storefront-specific exceptions
- whether push notifications are used for marketing versus transactional value

## Severity guidance

### High

Likely blocker or serious review risk:

- private API evidence
- missing sensitive-purpose strings
- third-party login with no Apple login signal
- digital-goods checkout with no StoreKit signal
- no account deletion path in an account-based app

### Medium

Real review question, but context matters:

- background modes present
- ad/tracking SDK with unclear ATT posture
- WebView-heavy architecture
- weak purpose strings
- screen recording without obvious consent UX

### Low

Polish or caution:

- HIG consistency concerns
- unclear Apple Pay disclosure readiness
- UX choices that may not block review but feel off-platform

## Final rule

Be skeptical, specific, and useful.

Do not create fake certainty, and do not water down real App Review risk.
