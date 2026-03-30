---
name: codebase-map
description: Verstehe eine unbekannte Codebasis strukturiert, finde relevante Einstiegspunkte, Datenflüsse, Modulgrenzen und die wahrscheinlich betroffenen Bereiche für ein Problem oder Vorhaben.
---

# Codebase Map Skill

Nutze diesen Skill, wenn du erst verstehen musst, wie eine Codebasis aufgebaut ist, bevor du analysierst oder änderst.

## Ziel
Erzeuge ein belastbares, knappes Architektur- und Navigationsbild der relevanten Codebasis.

## Vorgehen
1. Kläre das Ziel:
   - Bug?
   - Feature?
   - Refactoring?
   - Architekturverständnis?
2. Finde die relevanten Einstiegspunkte:
   - UI / CLI / API / Events / Scheduler / Background Jobs
3. Verfolge Aufrufketten, Datenflüsse und Zustandsübergänge.
4. Ordne die wichtigsten Dateien und Module:
   - direkt relevant
   - potenziell relevant
   - wahrscheinlich irrelevant
5. Identifiziere Grenzen:
   - Layer
   - Feature-Slices
   - Adapter / Ports
   - Shared Modules
6. Benenne Unsicherheiten explizit.

## Ausgabeformat
1. Ziel / Fragestellung
2. Relevante Einstiegspunkte
3. Wichtige Module / Dateien
4. Datenfluss / Kontrollfluss
5. Architektur- und Boundary-Beobachtungen
6. Offene Fragen / Unsicherheiten
