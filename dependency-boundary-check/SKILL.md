---
name: dependency-boundary-check
description: Finde unerwünschte Abhängigkeiten, Schichtverletzungen, zyklische Kopplung und ungeeignete Shared-Abstraktionen in einer Codebasis oder Änderung.
---

# Dependency Boundary Check Skill

## Ziel
Abhängigkeitsprobleme sichtbar machen, bevor sie die Architektur erodieren.

## Prüfpunkte
- verbotene Richtungen zwischen Layern
- Zyklen oder implizite Kopplung
- Shared-Code-Missbrauch
- Infrastrukturwissen in Domain / Use Cases
- UI oder Delivery als Träger fachlicher Entscheidungen

## Ausgabeformat
1. beobachtete Abhängigkeiten
2. Boundary-Verletzungen
3. Kopplungsrisiken
4. empfohlene Korrekturen
5. minimale Sofortmaßnahmen
