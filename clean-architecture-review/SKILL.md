---
name: clean-architecture-review
description: Prüfe eine Änderung, ein Feature oder einen Bestandscode auf Clean-Architecture-Tauglichkeit, Layer-Verletzungen, Kopplung und falsch platzierte Verantwortlichkeiten.
---

# Clean Architecture Review Skill

## Ziel
Prüfe, ob Code, Änderungen oder Architekturentscheidungen saubere Verantwortlichkeiten und stabile Abhängigkeiten wahren.

## Prüffokus
- richtige Schicht für die jeweilige Logik
- Abhängigkeitsrichtung
- Leaking von Infrastruktur- oder Transportdetails
- falsche Shared-Abstraktionen
- zu frühe Generalisierung
- Querkopplung zwischen Features

## Vorgehen
1. Benenne die relevanten Layer / Module.
2. Ordne Verantwortlichkeiten zu.
3. Suche Boundary-Verletzungen.
4. Prüfe Abhängigkeitsrichtung und Kopplung.
5. Prüfe, ob die Lösung lokal genug ist.
6. Gib konkrete Verbesserungsvorschläge mit möglichst kleinem Eingriff.

## Ausgabeformat
1. Beobachtete Struktur
2. Verantwortlichkeiten je Bereich
3. Layer- / Boundary-Verletzungen
4. Kopplungs- und Wartbarkeitsrisiken
5. Konkrete Verbesserungen
6. Minimaler empfohlener Eingriff
