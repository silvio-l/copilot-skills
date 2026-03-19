---
name: flutter-best-practices
description: "MUST USE for ALL Flutter/Dart code changes. Invoke this skill IMMEDIATELY when writing, reviewing, or refactoring any Flutter widget, screen, provider, repository, or Dart utility. Enforces: reusable widget architecture, consistent UI/UX through shared abstractions, intuitive gesture controls, proper state management, performance patterns, accessibility, and i18n compliance. Also triggers on German: 'Widget erstellen', 'Screen bauen', 'Flutter Code', 'Dart Code'. This skill ensures every Flutter change follows production-grade patterns — never write Flutter code without it."
---

# Flutter Best Practices — Production-Grade Mobile Apps

Du bist der Qualitäts-Gate-Keeper für Flutter/Dart-Code. Jede Änderung an `.dart`-Dateien MUSS diesen Regeln folgen. Keine Ausnahmen.

---

## 🔴 REGEL #1: Wiederverwendbare Widgets über alles

**Das ist die wichtigste Regel.** Eine gute UI/UX lebt von konsistenter Benutzererfahrung durch wiederverwendbare, konsistente Widgets. Inkonsistente Screens und Widgets sind der häufigste Qualitätskiller.

### Pflichten

1. **Bevor du ein neues Widget schreibst**: Suche in `lib/core/widgets/` und im Feature-Ordner, ob ein ähnliches Widget existiert. Erweitere es statt neu zu schreiben.
2. **Gemeinsame UI-Muster zentral halten**: Buttons, Cards, Form-Felder, Bottom-Sheets, Dialoge, Empty-States, Loading-States — alles in `lib/core/widgets/`.
3. **Screen-Grundgerüste teilen**: Wenn mehrere Screens dasselbe Layout haben (Header, Body, FAB), extrahiere ein Scaffold-Widget.
4. **Widget-API-Design**:
   - Nur nötige Parameter exposen (Label, Callback, Style-Overrides)
   - `const`-Konstruktoren wo möglich
   - Doc-Kommentare (`///`) für Klasse und öffentliche Parameter
   - Keine Geschäftslogik im Widget — die gehört in Provider/Repository

### Anti-Patterns (VERBOTEN)

```dart
// ❌ VERBOTEN: Inline-Styling, das sich auf 5 Screens wiederholt
Container(
  padding: EdgeInsets.all(16),
  decoration: BoxDecoration(
    color: Colors.white,           // ← Hardcoded!
    borderRadius: BorderRadius.circular(12),
  ),
  child: ...
)

// ✅ RICHTIG: Wiederverwendbares Widget mit Theme-Anbindung
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

### Konsistenz-Checkliste (bei jedem Screen-Review)

- [ ] Verwendet der Screen dasselbe Scroll-Verhalten wie alle anderen Screens?
- [ ] Sind Header, Spacing, Typografie identisch zu Geschwister-Screens?
- [ ] Verwendet der Screen zentrale Widgets statt Inline-Definitionen?
- [ ] Sind Eingabeformulare über das gemeinsame FormSheet-Widget gebaut?
- [ ] Sind Empty-States über das gemeinsame EmptyState-Widget gebaut?
- [ ] Sind Farben über `Theme.of(context).colorScheme` referenziert?

---

## 🔴 REGEL #2: Intuitive Gestensteuerung

Mobile Apps MÜSSEN sich nativ anfühlen. Gestensteuerung ist kein Nice-to-have — sie ist Pflicht auf Screen-, Widget- und Komponenten-Ebene.

### Pflicht-Gesten

| Kontext | Geste | Flutter-Widget | Details |
|---------|-------|----------------|---------|
| Listen-Items löschen | Swipe-to-Dismiss | `Dismissible` | Roter Hintergrund mit Trash-Icon, Undo-Snackbar |
| Scrollbare Listen | Pull-to-Refresh | `RefreshIndicator` | Nur bei Daten, die aktualisiert werden können |
| Bottom-Sheets/Modals | Swipe-Down-to-Close | `DraggableScrollableSheet` / `showModalBottomSheet(enableDrag: true)` | Drag-Handle oben sichtbar |
| Navigations-Rückkehr | Swipe-Back (Edge) | `WillPopScope` / iOS-native | Nicht blockieren! Nur bei ungespeicherten Änderungen warnen |
| Sortierbare Listen | Long-Press + Drag | `ReorderableListView` | Haptic Feedback bei Drag-Start |
| Formulare / Inputs | Tap-Outside-to-Dismiss-Keyboard | `GestureDetector(onTap: () => FocusScope.of(context).unfocus())` | Auf jedem Screen mit Inputs |

### Haptic Feedback

```dart
import 'package:flutter/services.dart';

// Bei wichtigen Aktionen:
HapticFeedback.lightImpact();   // Tap-Feedback
HapticFeedback.mediumImpact();  // Drag-Start, Toggle
HapticFeedback.heavyImpact();   // Destruktive Aktion bestätigt
HapticFeedback.selectionClick(); // Auswahl in Liste/Picker
```

**Regeln für Haptic Feedback:**
- ✅ Bei destruktiven Aktionen (Löschen), Toggles, Drag-Start/Ende
- ✅ Bei Auswahl-Änderungen (Picker, Toggle-Gruppen)
- ❌ NICHT bei jedem Tap auf einen Button (zu viel Vibration nervt)
- ❌ NICHT bei Scroll-Events

### Touch-Targets

- **Minimum 44×44 logische Pixel** — auch für Icon-Buttons
- Verwende `IconButton` (hat automatisch 48×48) statt `GestureDetector` auf einem nackten `Icon`
- Bei Custom-Widgets: `SizedBox(width: 44, height: 44)` als Minimum-Wrapper

### Gesten-Konflikte vermeiden

```dart
// ❌ PROBLEM: GestureDetector fängt Scroll-Events ab
GestureDetector(
  onHorizontalDragUpdate: ...,
  child: ListView(...),  // Scroll wird blockiert!
)

// ✅ LÖSUNG: Richtungsspezifisch oder mit Threshold
GestureDetector(
  onHorizontalDragEnd: (details) {
    if (details.primaryVelocity!.abs() > 500) { // Threshold
      // Handle swipe
    }
  },
  child: ListView(...),
)
```

### Dual-Input-Regel: Touch + Mouse + Keyboard

**Mobile-first heißt NICHT touch-only.** Sobald ein Custom-Control über Standard-Widgets hinausgeht, muss es beide Bedienkonzepte gemeinsam unterstützen:

- **Touch**: Tap, Swipe, Drag, große Touch-Targets
- **Mouse**: Hover-State, Klick, bei Overflow auch präziser Zugriff per Mausrad/Trackpad, Drag oder Chevron-Affordance
- **Keyboard**: Fokus-Reihenfolge, sichtbarer Fokus, Aktivierung via Enter/Space, Erreichbarkeit versteckter Overflow-Items

#### Pflicht für horizontale Overflow-Controls

Das gilt besonders für Kategorien, Chips, Icon-/Farb-Selectoren, Recurrence-Pills und ähnliche horizontale Optionen:

- **Nie nur `SingleChildScrollView` + `GestureDetector`**
- Verwende **focusable** Interaktions-Widgets (`InkWell`, `IconButton`, `TextButton`, `SegmentedButton`, `ChoiceChip`) oder ein zentrales Wrapper-Widget mit Fokus-/Aktivierungslogik
- Overflow-Inhalte müssen **mit der Maus erreichbar** sein:
  - per Mausrad/Trackpad während Hover **oder**
  - per Mouse-Drag auf der Scrollfläche **oder**
  - per expliziten Scroll-Buttons/Chevrons **oder**
  - per sichtbarer/interaktiver Scrollbar nur wenn sie funktional wirklich nötig ist
- Overflow-Inhalte müssen **mit Keyboard erreichbar** sein:
  - Tab-/Arrow-Navigation zu Items
  - fokussierte Items scrollen sich bei Bedarf in den sichtbaren Bereich
- Persistente horizontale Scrollbar-Thumbnails sind **nicht** der Default für mobile-first Picker-/Chip-Reihen; bevorzuge reduziertes Overflow-Chrome und behalte die Präzisionssteuerung über Wheel/Trackpad, Drag und Chevrons
- Sichtbares Overflow-Chrome, das Breite kostet (z.B. Chevrons oder Scrollbars), darf schmale mobile-first Layouts nicht zusammendruecken; in reduzierten Layouts bleibt die Praezisionsbedienung bevorzugt unsichtbar

#### Verboten

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

## 🟡 REGEL #3: Widget-Architektur & State Management

### Widget-Hierarchie

```
StatelessWidget (bevorzugt)
  └── Composition über Vererbung
  └── const-Konstruktoren wo möglich
  └── build() ist rein — keine Side-Effects

StatefulWidget (nur wenn nötig)
  └── setState() so lokal wie möglich
  └── dispose() für ALLE Controller, Subscriptions, Timer
  └── initState() nur für einmalige Initialisierung

ConsumerWidget / ConsumerStatefulWidget (Riverpod)
  └── ref.watch() für reaktive Daten
  └── ref.read() nur in Callbacks (onPressed, onTap)
  └── NIEMALS ref.watch() in Callbacks!
```

### State Management mit Riverpod

```dart
// ✅ Provider-Pattern:
final settingsProvider = StreamProvider<Settings>((ref) {
  return ref.watch(repositoryProvider).watchSettings();
});

// ✅ Im Widget:
class MyWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final settings = ref.watch(settingsProvider);
    return settings.when(
      data: (data) => Text(data.currency),
      loading: () => const CircularProgressIndicator(),
      error: (e, st) => Text('Fehler: $e'),
    );
  }
}

// ❌ VERBOTEN:
ref.watch(provider);  // in onPressed-Callback
ref.read(provider);   // in build()-Methode für reaktive Daten
```

### Dispose-Pflicht (Memory-Leak-Prävention)

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

**Regel: Jeder Controller/Subscription der in `initState()` oder im Feld erstellt wird, MUSS in `dispose()` aufgeräumt werden. Keine Ausnahmen.**

---

## 🟡 REGEL #4: Theming & Design-Tokens

### Verboten

```dart
// ❌ NIEMALS:
Color(0xFF1A73E8)              // Hardcoded Farbe
Colors.white                    // Material-Farbe direkt
TextStyle(fontSize: 16)         // Inline Text-Style
EdgeInsets.all(16)              // Magic-Number Spacing
BorderRadius.circular(12)       // Magic-Number Radius
```

### Pflicht

```dart
// ✅ IMMER über Theme/Design-Tokens:
Theme.of(context).colorScheme.primary
Theme.of(context).colorScheme.surface
colorScheme.onSurface            // Kontrastfarbe
AppTextStyles.heading            // Zentrale Text-Styles
AppSpacing.md                    // Zentrale Spacing-Werte
AppRadius.borderRadiusMd         // Zentrale Radien
AppShadows.sm                    // Zentrale Schatten
```

### Custom-Farben über Extensions

```dart
// Für produktspezifische Farben (income-grün, expense-rot):
extension AppColorExtension on ColorScheme {
  Color get income => brightness == Brightness.light
      ? const Color(0xFF2E7D32)
      : const Color(0xFF66BB6A);
  Color get expense => brightness == Brightness.light
      ? const Color(0xFFD32F2F)
      : const Color(0xFFEF5350);
}

// Nutzung:
Theme.of(context).colorScheme.income
```

### Dark Mode

- **Pflicht**: Jedes Widget MUSS in Light UND Dark Mode korrekt aussehen.
- **Test**: Bei jedem visuellen Change den anderen Theme-Mode prüfen.
- **Niemals**: `Brightness.light` hart annehmen. Immer `colorScheme.brightness` prüfen, wenn Theme-abhängige Logik nötig ist.

---

## 🟡 REGEL #5: Performance

### const ist ansteckend

```dart
// ✅ const überall wo möglich:
const SizedBox(height: 8)
const EdgeInsets.symmetric(horizontal: 16)
const Text('Hallo')
const Icon(LucideIcons.home)
```

**Regel: Wenn der Linter `prefer_const_constructors` vorschlägt — IMMER umsetzen.**

### Listen-Performance

```dart
// ❌ VERBOTEN bei Listen > 10 Items:
Column(children: items.map((i) => ItemWidget(i)).toList())

// ✅ PFLICHT — lazy building:
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(items[index]),
)
```

### Build-Methode schlank halten

```dart
// ❌ VERBOTEN: Schwere Berechnungen in build()
@override
Widget build(BuildContext context) {
  final sorted = items..sort((a, b) => a.date.compareTo(b.date)); // ← NEIN!
  // ...
}

// ✅ RICHTIG: In State oder Provider vorberechnen
@override
void didUpdateWidget(old) {
  super.didUpdateWidget(old);
  if (old.items != widget.items) {
    _sorted = List.of(widget.items)..sort((a, b) => a.date.compareTo(b.date));
  }
}
```

---

## 🟡 REGEL #6: Internationalisierung (i18n)

### Kein hardcodierter Text

```dart
// ❌ VERBOTEN:
Text('Einnahmen')
Text('Verfügbar')
'€ $amount'

// ✅ PFLICHT:
Text(AppLocalizations.of(context).income)
Text(l10n.available)
CurrencyFormatter.format(amount, currency)
```

**Jeder neue User-facing String → in `app_de.arb` UND `app_en.arb` eintragen.**

### ARB-Konventionen

- Keys: camelCase, beschreibend (`savingsGoalTitle`, nicht `title1`)
- Plurals: ICU-Syntax (`{count, plural, one{1 Eintrag} other{{count} Einträge}}`)
- Placeholders immer mit Typ-Annotation dokumentieren

---

## 🟡 REGEL #7: Navigation & Routing

### GoRouter-Regeln

```dart
// Modale Overlays (Forms, Details):
// → parentNavigatorKey: _rootNavigatorKey
// → Damit sie ÜBER der Shell (inkl. Bottom-Nav + FAB) erscheinen

// Tab-interne Navigation:
// → Kein parentNavigatorKey (bleibt in der Branch)

// Navigation von innerhalb einer Shell-Branch zum Root:
// → appRouter.push() statt context.push()
// → Garantiert Root-Navigator-Kontext
```

### Transitions

```dart
// Modale Bottom-Sheets: SlideTransition von unten, easeOutCubic
// Settings/Detail-Screens: SlideTransition von rechts
// Tab-Wechsel: Kein Übergang (instant)
// Destruktive Aktionen: Bestätigungsdialog vor Navigation
```

---

## 🟢 REGEL #8: Testing

### Pflicht-Tests

| Was | Typ | Priorität |
|-----|-----|-----------|
| Simulationsengine | Unit | 🔴 Höchste |
| CurrencyFormatter | Unit | 🔴 |
| Repositories | Unit | 🟡 |
| Wiederverwendbare Widgets | Widget | 🟡 |
| Screen-Smoke-Tests | Widget | 🟢 |
| User-Flows | Integration | 🟢 |

### Test-Konventionen

```dart
// Datei: lib/core/utils/x.dart → test/core/utils/x_test.dart
// Mocking: mocktail (NICHT mockito)
// Testdaten: test/fixtures/test_data.dart (shared)
// Jeder Test eigenständig lauffähig
```

---

## 🟢 REGEL #9: Accessibility

- **Semantics**: Jedes interaktive Widget braucht ein Semantics-Label
- **Kontrast**: Minimum 4.5:1 (WCAG AA)
- **Touch-Targets**: Minimum 44×44px
- **Focus-States**: Sichtbar, nie entfernen
- **Screen-Reader**: App mit TalkBack/VoiceOver testen
- **Keyboard**: Custom-Controls müssen per Tab/Fokus erreichbar und per Enter/Space aktivierbar sein
- **Mouse**: Hover- und Overflow-Verhalten müssen bei Desktop-/Web-Nutzung mitgedacht werden

```dart
// ✅ Icon-Button mit Semantik:
Semantics(
  label: l10n.deleteEntry,
  child: IconButton(
    icon: const Icon(LucideIcons.trash2),
    onPressed: _delete,
  ),
)
```

---

## 🟢 REGEL #10: Code-Organisation

### Feature-First-Struktur

```
lib/
  core/              — Geteilte Utilities, Theme, l10n, Widgets
    widgets/         — Wiederverwendbare Widgets (WICHTIGSTER Ordner!)
    theme/           — Design-Tokens, Farben, Spacing, Typografie
    l10n/            — Lokalisierung
    utils/           — Formatter, Helpers
  features/
    {feature}/
      models/        — Datenmodelle
      repositories/  — Datenzugriff
      providers/     — Riverpod Provider
      screens/       — Vollständige Screens
      widgets/       — Feature-spezifische Widgets
  router/            — GoRouter-Konfiguration
  database/          — Drift-Datenbankdefinition
```

### Import-Reihenfolge

```dart
// 1. Dart SDK
import 'dart:async';

// 2. Flutter SDK
import 'package:flutter/material.dart';

// 3. Packages (alphabetisch)
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

// 4. Projekt-Imports (alphabetisch)
import 'package:hellerio/core/theme/app_spacing.dart';
import 'package:hellerio/features/planning/models/...';
```

---

## Anwendung dieses Skills

**Bei JEDER Flutter/Dart-Änderung** prüfe:

1. ✅ Wiederverwendet bestehende Widgets? (Regel #1)
2. ✅ Gesten intuitiv? (Regel #2)
3. ✅ State korrekt gemanaged? (Regel #3)
4. ✅ Keine hardcoded Farben/Strings/Spacing? (Regel #4 + #6)
5. ✅ const wo möglich? (Regel #5)
6. ✅ Dark Mode kompatibel? (Regel #4)
7. ✅ Touch-Targets ≥ 44px? (Regel #9)
8. ✅ Custom-Controls auch mit Mouse + Keyboard vollständig bedienbar?

**Wenn eine Regel verletzt wird: Behebe es SOFORT, bevor du den Code präsentierst.**
