---
name: safe-refactor-planner
description: Plane Refactorings so, dass sie klein, sicher, schrittweise und gut validierbar bleiben, ohne unnötige Architekturbewegung.
---

# Safe Refactor Planner Skill

## Ziel
Einen Refactor in kleine, kontrollierbare Schritte zerlegen.

## Vorgehen
1. Refactor-Ziel klar benennen
2. Bestandscode und Abhängigkeiten erfassen
3. Risiken und fragile Stellen markieren
4. Kleinstmögliche Schritte planen
5. Für jeden Schritt definieren:
   - Zweck
   - geänderte Dateien
   - erwarteter Nutzen
   - Validierung
   - Rollback-Fähigkeit

## Regeln
- Verhalten nicht unbeabsichtigt ändern
- Refactor nicht mit Feature-Arbeit vermischen, außer bewusst und explizit
- zuerst Stabilisierung, dann Strukturverbesserung

## Ausgabeformat
1. Refactor-Ziel
2. relevante Bereiche
3. Risiken
4. Schrittplan
5. Validierung je Schritt
6. Rollback-/Sicherheitsstrategie
