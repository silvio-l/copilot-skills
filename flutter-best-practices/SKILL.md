---
name: flutter-best-practices
description: "MUST USE for ALL Flutter/Dart code changes. Invoke this skill IMMEDIATELY when writing, reviewing, or refactoring any Flutter widget, screen, provider, repository, or Dart utility. Enforces: reusable widget architecture, consistent UI/UX through shared abstractions, intuitive gesture controls, proper state management, performance patterns, accessibility, and i18n compliance. Also triggers on German: 'Widget erstellen', 'Screen bauen', 'Flutter Code', 'Dart Code'. This skill ensures every Flutter change follows production-grade patterns — never write Flutter code without it."
---

# Flutter Best Practices — Production-Grade Mobile Apps

You are the quality gate-keeper for Flutter/Dart code. Every change to `.dart` files MUST follow these rules. No exceptions.

---

## 🔴 RULE #1: Reusable Widgets Above All

**This is the most important rule.** Good UI/UX depends on a consistent user experience through reusable, consistent widgets. Inconsistent screens and widgets are the most common quality killer.

### Requirements

1. **Before writing a new widget**: Search `lib/core/widgets/` and the feature folder for a similar existing widget. Extend it instead of writing a new one.
2. **Keep shared UI patterns centralized**: Buttons, Cards, Form fields, Bottom-Sheets, Dialogs, Empty-States, Loading-States — all belong in `lib/core/widgets/`.
3. **Share screen scaffolds**: If multiple screens share the same layout (Header, Body, FAB), extract a Scaffold widget.
4. **Widget API design**:
   - Only expose necessary parameters (Label, Callback, Style-Overrides)
   - `const` constructors where possible
   - Doc comments (`///`) for classes and public parameters
   - No business logic in widgets — that belongs in Provider/Repository

### Anti-Patterns (FORBIDDEN)

```dart
// ❌ FORBIDDEN: Inline styling repeated across 5 screens
Container(
  padding: EdgeInsets.all(16),
  decoration: BoxDecoration(
    color: Colors.white,           // ← Hardcoded!
    borderRadius: BorderRadius.circular(12),
  ),
  child: ...
)

// ✅ CORRECT: Reusable widget with theme binding
class AppCard extends StatelessWidget {
  final Widget child;
  final EdgeInsets? padding;
  const AppCard({super.key, required this.child, this.padding});
  
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: padding ?? const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surface,
        borderRadius: AppRadius.borderRadiusMd,
      ),
      child: child,
    );
  }
}
```

### Consistency Checklist (for every screen review)

- [ ] Does the screen use the same scroll behavior as all other screens?
- [ ] Are header, spacing, and typography identical to sibling screens?
- [ ] Does the screen use centralized widgets instead of inline definitions?
- [ ] Are input forms built using the shared FormSheet widget?
- [ ] Are empty states built using the shared EmptyState widget?
- [ ] Are colors referenced via `Theme.of(context).colorScheme`?

---

## 🔴 RULE #2: Intuitive Gesture Controls

Mobile apps MUST feel native. Gesture controls are not a nice-to-have — they are mandatory at the screen, widget, and component level.

### Required Gestures

| Context | Gesture | Flutter Widget | Details |
|---------|---------|----------------|---------|
| Deleting list items | Swipe-to-Dismiss | `Dismissible` | Red background with trash icon, undo snackbar |
| Scrollable lists | Pull-to-Refresh | `RefreshIndicator` | Only for data that can be refreshed |
| Bottom-Sheets/Modals | Swipe-Down-to-Close | `DraggableScrollableSheet` / `showModalBottomSheet(enableDrag: true)` | Drag handle visible at top |
| Navigation back | Swipe-Back (Edge) | `WillPopScope` / iOS-native | Do not block! Only warn on unsaved changes |
| Sortable lists | Long-Press + Drag | `ReorderableListView` | Haptic feedback on drag start |
| Forms / Inputs | Tap-Outside-to-Dismiss-Keyboard | `GestureDetector(onTap: () => FocusScope.of(context).unfocus())` | On every screen with inputs |

### Haptic Feedback

```dart
import 'package:flutter/services.dart';

// For important actions:
HapticFeedback.lightImpact();   // Tap feedback
HapticFeedback.mediumImpact();  // Drag start, toggle
HapticFeedback.heavyImpact();   // Destructive action confirmed
HapticFeedback.selectionClick(); // Selection in list/picker
```

**Rules for Haptic Feedback:**
- ✅ For destructive actions (delete), toggles, drag start/end
- ✅ For selection changes (picker, toggle groups)
- ❌ NOT on every button tap (too much vibration is annoying)
- ❌ NOT on scroll events

### Touch Targets

- **Minimum 44×44 logical pixels** — including for icon buttons
- Use `IconButton` (automatically 48×48) instead of `GestureDetector` on a bare `Icon`
- For custom widgets: `SizedBox(width: 44, height: 44)` as minimum wrapper

### Avoiding Gesture Conflicts

```dart
// ❌ PROBLEM: GestureDetector intercepts scroll events
GestureDetector(
  onHorizontalDragUpdate: ...,
  child: ListView(...),  // Scroll is blocked!
)

// ✅ SOLUTION: Direction-specific or with threshold
GestureDetector(
  onHorizontalDragEnd: (details) {
    if (details.primaryVelocity!.abs() > 500) { // Threshold
      // Handle swipe
    }
  },
  child: ListView(...),
)
```

### Dual-Input Rule: Touch + Mouse + Keyboard

**Mobile-first does NOT mean touch-only.** As soon as a custom control goes beyond standard widgets, it must support both input paradigms together:

- **Touch**: Tap, Swipe, Drag, large touch targets
- **Mouse**: Hover state, click, for overflow also precise access via scroll wheel/trackpad, drag, or chevron affordance
- **Keyboard**: Focus order, visible focus, activation via Enter/Space, reachability of hidden overflow items

#### Requirements for Horizontal Overflow Controls

This applies especially to categories, chips, icon/color selectors, recurrence pills, and similar horizontal options:

- **Never just `SingleChildScrollView` + `GestureDetector`**
- Use **focusable** interaction widgets (`InkWell`, `IconButton`, `TextButton`, `SegmentedButton`, `ChoiceChip`) or a centralized wrapper widget with focus/activation logic
- Overflow content must be **reachable with a mouse**:
  - via scroll wheel/trackpad while hovering **or**
  - via mouse drag on the scroll area **or**
  - via explicit scroll buttons/chevrons **or**
  - via visible/interactive scrollbar only when functionally necessary
- Overflow content must be **reachable with keyboard**:
  - Tab/arrow navigation to items
  - Focused items scroll into the visible area as needed
- Persistent horizontal scrollbar thumbnails are **not** the default for mobile-first picker/chip rows; prefer reduced overflow chrome and keep precision control via wheel/trackpad, drag, and chevrons
- Visible overflow chrome that takes up width (e.g. chevrons or scrollbars) must not compress narrow mobile-first layouts; in reduced layouts, precision controls should preferably remain invisible

#### Forbidden

```dart
// ❌ Touch-only Custom-Control
GestureDetector(
  onTap: onTap,
  child: AnimatedContainer(...),
)

// ❌ Horizontal overflow without mouse/keyboard affordance
SingleChildScrollView(
  scrollDirection: Axis.horizontal,
  child: Row(children: chips),
)
```

```dart
// ✅ Dual-input friendly pattern
Listener(
  onPointerSignal: _handlePointerSignal,
  child: ListView.separated(
    controller: controller,
    scrollDirection: Axis.horizontal,
    itemBuilder: ... // focusable items with InkWell/Button semantics
  ),
)
```

---

## 🟡 RULE #3: Widget Architecture & State Management

### Widget Hierarchy

```
StatelessWidget (preferred)
  └── Composition over inheritance
  └── const constructors where possible
  └── build() is pure — no side effects

StatefulWidget (only when necessary)
  └── setState() as local as possible
  └── dispose() for ALL controllers, subscriptions, timers
  └── initState() only for one-time initialization

ConsumerWidget / ConsumerStatefulWidget (Riverpod)
  └── ref.watch() for reactive data
  └── ref.read() only in callbacks (onPressed, onTap)
  └── NEVER ref.watch() in callbacks!
```

### State Management with Riverpod

```dart
// ✅ Provider pattern:
final settingsProvider = StreamProvider<Settings>((ref) {
  return ref.watch(repositoryProvider).watchSettings();
});

// ✅ In the widget:
class MyWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final settings = ref.watch(settingsProvider);
    return settings.when(
      data: (data) => Text(data.currency),
      loading: () => const CircularProgressIndicator(),
      error: (e, st) => Text('Error: $e'),
    );
  }
}

// ❌ FORBIDDEN:
ref.watch(provider);  // in onPressed callback
ref.read(provider);   // in build() method for reactive data
```

### Dispose Requirement (Memory Leak Prevention)

```dart
@override
void dispose() {
  _nameController.dispose();
  _scrollController.dispose();
  _animationController.dispose();
  _subscription?.cancel();
  _timer?.cancel();
  _focusNode.dispose();
  super.dispose();
}
```

**Rule: Every controller/subscription created in `initState()` or as a field MUST be cleaned up in `dispose()`. No exceptions.**

---

## 🟡 RULE #4: Theming & Design Tokens

### Forbidden

```dart
// ❌ NEVER:
Color(0xFF1A73E8)              // Hardcoded color
Colors.white                    // Direct Material color
TextStyle(fontSize: 16)         // Inline text style
EdgeInsets.all(16)              // Magic number spacing
BorderRadius.circular(12)       // Magic number radius
```

### Required

```dart
// ✅ ALWAYS via Theme/Design Tokens:
Theme.of(context).colorScheme.primary
Theme.of(context).colorScheme.surface
colorScheme.onSurface            // Contrast color
AppTextStyles.heading            // Centralized text styles
AppSpacing.md                    // Centralized spacing values
AppRadius.borderRadiusMd         // Centralized radii
AppShadows.sm                    // Centralized shadows
```

### Custom Colors via Extensions

```dart
// For product-specific colors (income green, expense red):
extension AppColorExtension on ColorScheme {
  Color get income => brightness == Brightness.light
      ? const Color(0xFF2E7D32)
      : const Color(0xFF66BB6A);
  Color get expense => brightness == Brightness.light
      ? const Color(0xFFD32F2F)
      : const Color(0xFFEF5350);
}

// Usage:
Theme.of(context).colorScheme.income
```

### Dark Mode

- **Required**: Every widget MUST look correct in both Light AND Dark Mode.
- **Test**: Check the other theme mode with every visual change.
- **Never**: Hard-assume `Brightness.light`. Always check `colorScheme.brightness` when theme-dependent logic is needed.

---

## 🟡 RULE #5: Performance

### const is Contagious

```dart
// ✅ const everywhere possible:
const SizedBox(height: 8)
const EdgeInsets.symmetric(horizontal: 16)
const Text('Hello')
const Icon(LucideIcons.home)
```

**Rule: When the linter suggests `prefer_const_constructors` — ALWAYS apply it.**

### List Performance

```dart
// ❌ FORBIDDEN for lists > 10 items:
Column(children: items.map((i) => ItemWidget(i)).toList())

// ✅ REQUIRED — lazy building:
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(items[index]),
)
```

### Keep the Build Method Lean

```dart
// ❌ FORBIDDEN: Heavy computations in build()
@override
Widget build(BuildContext context) {
  final sorted = items..sort((a, b) => a.date.compareTo(b.date)); // ← NO!
  // ...
}

// ✅ CORRECT: Pre-compute in State or Provider
@override
void didUpdateWidget(old) {
  super.didUpdateWidget(old);
  if (old.items != widget.items) {
    _sorted = List.of(widget.items)..sort((a, b) => a.date.compareTo(b.date));
  }
}
```

---

## 🟡 RULE #6: Internationalization (i18n)

### No Hardcoded Text

```dart
// ❌ FORBIDDEN:
Text('Einnahmen')
Text('Verfügbar')
'€ $amount'

// ✅ REQUIRED:
Text(AppLocalizations.of(context).income)
Text(l10n.available)
CurrencyFormatter.format(amount, currency)
```

**Every new user-facing string → add to both `app_de.arb` AND `app_en.arb`.**

### ARB Conventions

- Keys: camelCase, descriptive (`savingsGoalTitle`, not `title1`)
- Plurals: ICU syntax (`{count, plural, one{1 entry} other{{count} entries}}`)
- Always document placeholders with type annotations

---

## 🟡 RULE #7: Navigation & Routing

### GoRouter Rules

```dart
// Modal overlays (forms, details):
// → parentNavigatorKey: _rootNavigatorKey
// → So they appear ABOVE the shell (incl. Bottom-Nav + FAB)

// Tab-internal navigation:
// → No parentNavigatorKey (stays in the branch)

// Navigation from within a shell branch to root:
// → appRouter.push() instead of context.push()
// → Guarantees root navigator context
```

### Transitions

```dart
// Modal bottom sheets: SlideTransition from bottom, easeOutCubic
// Settings/detail screens: SlideTransition from right
// Tab switches: No transition (instant)
// Destructive actions: Confirmation dialog before navigation
```

---

## 🟢 RULE #8: Testing

### Required Tests

| What | Type | Priority |
|------|------|----------|
| Simulation engine | Unit | 🔴 Highest |
| CurrencyFormatter | Unit | 🔴 |
| Repositories | Unit | 🟡 |
| Reusable widgets | Widget | 🟡 |
| Screen smoke tests | Widget | 🟢 |
| User flows | Integration | 🟢 |

### Test Conventions

```dart
// File: lib/core/utils/x.dart → test/core/utils/x_test.dart
// Mocking: mocktail (NOT mockito)
// Test data: test/fixtures/test_data.dart (shared)
// Every test must be independently runnable
```

---

## 🟢 RULE #9: Accessibility

- **Semantics**: Every interactive widget needs a Semantics label
- **Contrast**: Minimum 4.5:1 (WCAG AA)
- **Touch Targets**: Minimum 44×44px
- **Focus States**: Visible, never remove
- **Screen Reader**: Test app with TalkBack/VoiceOver
- **Keyboard**: Custom controls must be reachable via Tab/focus and activatable via Enter/Space
- **Mouse**: Hover and overflow behavior must be considered for desktop/web usage

```dart
// ✅ Icon button with semantics:
Semantics(
  label: l10n.deleteEntry,
  child: IconButton(
    icon: const Icon(LucideIcons.trash2),
    onPressed: _delete,
  ),
)
```

---

## 🟢 RULE #10: Code Organization

### Feature-First Structure

```
lib/
  core/              — Shared utilities, theme, l10n, widgets
    widgets/         — Reusable widgets (MOST IMPORTANT folder!)
    theme/           — Design tokens, colors, spacing, typography
    l10n/            — Localization
    utils/           — Formatters, helpers
  features/
    {feature}/
      models/        — Data models
      repositories/  — Data access
      providers/     — Riverpod Provider
      screens/       — Complete screens
      widgets/       — Feature-specific widgets
  router/            — GoRouter configuration
  database/          — Drift database definition
```

### Import Order

```dart
// 1. Dart SDK
import 'dart:async';

// 2. Flutter SDK
import 'package:flutter/material.dart';

// 3. Packages (alphabetical)
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

// 4. Project imports (alphabetical)
import 'package:hellerio/core/theme/app_spacing.dart';
import 'package:hellerio/features/planning/models/...';
```

---

## Applying This Skill

**For EVERY Flutter/Dart change**, check:

1. ✅ Reuses existing widgets? (Rule #1)
2. ✅ Gestures intuitive? (Rule #2)
3. ✅ State correctly managed? (Rule #3)
4. ✅ No hardcoded colors/strings/spacing? (Rule #4 + #6)
5. ✅ const where possible? (Rule #5)
6. ✅ Dark Mode compatible? (Rule #4)
7. ✅ Touch targets ≥ 44px? (Rule #9)
8. ✅ Custom controls also fully operable with mouse + keyboard?

**If a rule is violated: Fix it IMMEDIATELY before presenting the code.**
