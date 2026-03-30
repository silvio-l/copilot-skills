---
name: code-change-review
description: Prüfe Änderungen auf Korrektheit, Regressionen, Kopplung, Boundary-Verletzungen, Wartbarkeit und ungewollte Seiteneffekte.
---

# Code Change Review Skill

## Ziel
Eine Änderung wie ein erfahrener Reviewer prüfen.

## Prüffokus
- erfüllt die Änderung wirklich das Ziel?
- wurde die Root Cause getroffen?
- entstehen Regressionen?
- bleibt die Architektur sauber?
- ist die Änderung kleiner als nötig oder größer als nötig?
- fehlen Tests oder Guards?

## Ausgabeformat
1. Kurzbewertung
2. funktionale Risiken
3. Architektur- / Boundary-Risiken
4. Wartbarkeitsrisiken
5. fehlende Validierung
6. konkrete Verbesserungsvorschläge
