---
name: performance-regression-scan
description: Prüfe Änderungen oder Codepfade auf potenzielle Performance-Regressionen, unnötige Arbeit, überflüssige I/O-, Render-, Sync- oder Datenbewegungen.
---

# Performance Regression Scan Skill

## Ziel
Frühe Erkennung typischer Performance-Risiken nach Änderungen.

## Prüfpunkte
- unnötige Wiederholungen / Schleifen / Traversals
- zu häufige Re-Renders / Recomputations / Rebuilds
- unnötige Netzwerk-, Dateisystem- oder DB-Zugriffe
- fehlendes Caching oder falsches Caching
- blockierende Arbeit in kritischen Pfaden
- teure Mapping- oder Serialisierungsketten

## Ausgabeformat
1. relevante Pfade
2. potenzielle Regressionen
3. Schweregrad / Wahrscheinlichkeit
4. empfohlene Gegenmaßnahmen
5. Mess- / Prüfempfehlungen
