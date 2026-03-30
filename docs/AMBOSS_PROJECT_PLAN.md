# Projekt-Plan

> Automatisch gepflegt von Amboss. Letzte Aktualisierung: 2026-03-30 21:18 UTC

## Projekt-Uebersicht
Dieses Repository enthaelt wiederverwendbare Skills fuer die Copilot-CLI. Jeder Skill kapselt ein klar abgegrenztes Arbeitsgebiet mit triggerstarker Beschreibung, Workflow-Anweisungen und optionalen Referenzen oder Evals.

## Architektur-Entscheidungen
- 2026-03-30: Neuer Onboarding-Skill wird als eigenstaendiger Pflicht-Skill angelegt, aber klar gegen `premium-ui-ux` und `ui-copy-localization` abgegrenzt. - Vermeidet Doppelverantwortung und haelt Trigger sauber.

## Aktuelle Aufgaben & Naechste Schritte
- [ ] Benchmark des neuen `onboarding-best-practices`-Skills gegen eine baseline ohne Skill ausfuehren
- [ ] Triggerbeschreibung nach Eval-Ergebnissen weiter schaerfen
- [ ] Ueberschneidungen mit bestehenden Skills regelmaessig pruefen, falls weitere onboarding-nahe Skills entstehen

## Bekannte Probleme & Technische Schulden
- Dirty-main-Warnungen bleiben in diesem Repo wahrscheinlich haeufig relevant, weil mehrere Skills parallel bearbeitet werden. | Entdeckt: 2026-03-30 | Prioritaet: Mittel

## Gelernte Muster & Konventionen
- Pflicht-Skills in diesem Repo verwenden sehr pushy Beschreibungen mit expliziten Triggerbegriffen und "MUST USE" oder "REPLACES ad-hoc ..." Formulierungen. | Sichtbar in `premium-ui-ux/SKILL.md`, `ui-copy-localization/SKILL.md`, `bug-fix/SKILL.md`
- Umfangreiche Fachgebiete werden besser in `SKILL.md` plus eine Referenzdatei aufgeteilt als in eine einzelne ueberladene Skill-Datei. | Sichtbar in `premium-ui-ux/` und `apple-guidelines-review/`

## Letzte Aenderungen
| Datum | Aufgabe | Groesse | Branch | Zusammenfassung |
|-------|---------|-------|--------|-----------------|
| 2026-03-30 | create-onboarding-skill | M | main | Neuer `onboarding-best-practices`-Skill mit Wissensbasis, Boundary-Regeln und Eval-Suite erstellt |
