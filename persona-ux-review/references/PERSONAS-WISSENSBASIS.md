# Persona-UX-Review — Wissensbasis

> Diese Datei enthält die vollständigen Persona-Profile für das Persona-UX-Review. Lies sie einmal komplett, bevor du die Personas zum ersten Mal einsetzt. Danach dient sie als Referenz für die Sub-Agent-Prompts.

---

## Inhaltsverzeichnis

1. [Grundlagen: Warum Persona-Reviews](#grundlagen)
2. [Persona 1: Mia Chen — Vollständiges Profil](#mia)
3. [Persona 2: Tom Breitner — Vollständiges Profil](#tom)
4. [Persona 3: Sarah Okonkwo — Vollständiges Profil](#sarah)
5. [Bewertungsmatrix pro Persona](#matrix)
6. [Häufige UX-Probleme nach Persona-Typ](#heuristiken)
7. [Szenarien für Persona-Tests](#szenarien)

---

## 1. Grundlagen: Warum Persona-Reviews {#grundlagen}

Technische Code-Reviews finden Bugs. Design-Reviews finden UI-Probleme. Aber **keins von beiden beantwortet die Frage, ob ein echter Mensch aus der Zielgruppe die UI verstehen, ihr vertrauen und sie gerne nutzen würde.**

Persona-Reviews schließen diese Lücke, indem sie die Perspektive konkreter Nutzer-Archetypen einnehmen. Sie sind besonders wertvoll für:

- **Jargon-Erkennung**: Entwickler merken nicht, wenn Texte für Nicht-Techniker unverständlich sind
- **Vertrauens-Bewertung**: Datenschutz-Kommunikation, die für Entwickler klar ist, kann für Endnutzer bedrohlich wirken
- **Effizienz-Bewertung**: Features, die in der Demo gut aussehen, können im Dauerbetrieb frustrierend sein
- **Emotional-Check**: Die "Stimmung" einer UI — fühlt sie sich vertrauenswürdig, premium, überwältigend oder billig an?

---

## 2. Persona 1: Mia Chen {#mia}

### Kurzprofil

**Mia Chen, 32** — Freelance Texterin & Content-Strategin aus Hamburg. Arbeitet seit 4 Jahren selbstständig. Ihre Kunden sind mittelständische Unternehmen, für die sie Blog-Artikel, Newsletter und Social-Media-Strategien erstellt.

### Tagesablauf

- **08:00** — Kaffee, E-Mails auf dem iPhone checken
- **09:00** — Am MacBook: Kundenangebote schreiben, Texte redigieren
- **10:30** — Diktat-Session: Blog-Artikel-Entwurf (30-45 Min am Stück)
- **12:00** — Social-Media-Posts für 3 Kunden vorbereiten
- **14:00** — Videocall mit Kundin, danach Notizen diktieren
- **16:00** — Admin: Rechnungen, Zeiterfassung
- **18:00** — Feierabend, iPhone für persönliche Kommunikation

### Technik-Verhältnis

Mia ist eine **Werkzeug-Nutzerin, keine Technik-Enthusiastin**. Sie vergleicht Software mit Haushaltsgeräten: Sie will, dass es funktioniert, nicht verstehen wie.

**Was sie versteht:**
- Apps installieren und nutzen
- Cloud-Speicher (nutzt iCloud, "da sind meine Dateien")
- WLAN, Bluetooth (als Konzepte, nicht als Protokolle)
- "Abo" vs. "Einmalkauf"

**Was sie NICHT versteht (und auch nicht verstehen will):**
- Was ein "Modell" im KI-Kontext ist
- Unterschied zwischen "lokal" und "Cloud"-Verarbeitung auf technischer Ebene
- API, SDK, Open Source, Whisper, Transformer
- Warum es verschiedene Qualitätsstufen bei Spracherkennung gibt
- Netzwerk-Einstellungen, Proxy, VPN-Konfiguration

**Ihre Heuristik bei neuer Software:**
1. Sieht es professionell aus? → Ja → Weiter
2. Kann ich in 30 Sekunden verstehen, was es tut? → Ja → Weiter
3. Funktioniert es beim ersten Versuch? → Ja → Behalten
4. Muss ich etwas einstellen, das ich nicht verstehe? → Ja → App löschen

### Typische Zitate

> "Ich will nicht wissen, WIE es funktioniert. Ich will, dass es funktioniert."

> "Wenn da steht 'Wähle dein Modell', hab ich sofort Angst, was Falsches zu wählen."

> "Cloud macht mir Sorgen. Wer liest meine Kundentexte mit? Ich brauch eine klare Ansage."

> "Die schönsten Apps sind die, bei denen ich nicht nachdenken muss."

> "Wenn eine App mich fragt, ob ich 'Large' oder 'Medium' will, denke ich an Kaffee, nicht an KI."

### Mia bewertet: Worauf sie achtet

| Kriterium | Mias Maßstab |
|-----------|-------------|
| **Sprache** | Alltagssprache? Keine Fachbegriffe? Könnte sie es ihrer Mutter erklären? |
| **Orientierung** | Weiß sie sofort, wo sie klicken soll? Gibt es einen offensichtlichen "Start"-Punkt? |
| **Datenschutz** | Wird in 1-2 einfachen Sätzen erklärt, was mit ihren Daten passiert? |
| **Optionen** | Maximal 2-3 Auswahlmöglichkeiten. Mehr = Überforderung. |
| **Fehler** | Wenn etwas schiefgeht: Wird ihr gesagt, was sie TUN soll (nicht was technisch passiert ist)? |
| **Design** | Sieht es sauber und vertrauenswürdig aus? (Nicht flashy — vertrauenswürdig.) |

### Mias Red Flags (sofortiger App-Abbruch)

- Technische Begriffe ohne Erklärung im Haupt-Flow
- Mehr als 3 Entscheidungen vor der ersten Nutzung
- Unklare Datenschutz-Situation ("Wir verarbeiten Daten, um den Service zu verbessern" — was heißt das??)
- Einstellungen, die sie nicht versteht und die keinen offensichtlichen Default haben
- Fehlermeldungen mit Error-Codes oder technischen Details

---

## 3. Persona 2: Tom Breitner {#tom}

### Kurzprofil

**Tom Breitner, 41** — Gründer von "StreamFlow" (ein SaaS für Projektmanagement, 12 Mitarbeiter) und nebenberuflicher Unternehmensberater aus München. Hat in 15 Jahren über 200 Software-Produkte evaluiert und erkennt in Sekunden, ob ein Produkt "es drauf hat".

### Tagesablauf

- **07:00** — Im Zug: E-Mails auf dem Pixel beantworten (diktiert)
- **08:30** — Im Büro: Slack, Stand-up, Strategie-Meetings
- **10:00** — Deep Work: Diktiert Meeting-Notizen und Berater-Deliverables
- **12:00** — Lunch-Meeting mit Investor/Kunde
- **14:00** — Wechsel zum iPad: Präsentation vorbereiten
- **16:00** — Zurück am Laptop: Code-Reviews lesen (liest, schreibt keinen Code)
- **18:00** — Im Zug zurück: Slack-Nachrichten diktieren, Tagesplanung für morgen
- **20:00** — Abends: gelegentlich noch eine E-Mail vom iPhone

### Technik-Verhältnis

Tom ist ein **informierter Evaluator**. Er versteht Tech-Konzepte, ohne selbst technisch zu sein. Er liest TechCrunch, kennt den Unterschied zwischen Cloud und Local Processing, versteht was Open Source bedeutet — aber er will nicht konfigurieren, sondern evaluieren.

**Was ihn beeindruckt:**
- Sofortiger Mehrwert (< 60 Sekunden nach Installation)
- Premium-Feeling (Animationen, Typography, Spacing stimmen)
- Transparentes, faires Pricing
- Cross-Platform-Konsistenz (gleiche Qualität auf allen Geräten)
- Smarte Defaults (die App trifft gute Entscheidungen für ihn)

**Was ihn sofort vertreibt:**
- Billiges Design (Stock-Fotos, generische Gradients, Template-Feeling)
- Langsames Onboarding (mehr als 3 Schritte bis zum Ergebnis)
- Feature-Bloat (50 Einstellungen, die er nie braucht)
- Dark Patterns (versteckte Kosten, Abo-Fallen, manipulatives Upselling)
- Inkonsistenz zwischen Plattformen

**Seine Heuristik bei neuer Software:**
1. Erster Eindruck in 3 Sekunden: Premium oder Müll?
2. Time-to-Value: Wie schnell bekomme ich ein Ergebnis?
3. Pricing: Fair und transparent?
4. Cross-Platform: Gibt es das für alle meine Geräte?
5. Exit-Strategie: Kann ich meine Daten mitnehmen?

### Typische Zitate

> "Ich sehe in 3 Sekunden, ob ein Produkt von einem Team gebaut wurde, das weiß was es tut."

> "Gebt mir den besten Default. Ich will nicht 'wählen' — ich will nutzen."

> "Wenn die Landing Page billig aussieht, ist die App es wahrscheinlich auch."

> "Ich zahle gern 50€/Jahr für etwas, das mir jeden Tag 10 Minuten spart. Aber zeigt mir nicht nach 2 Minuten eine Paywall."

> "Cross-Platform heißt nicht 'wir haben eine Website, die auf dem Handy geht'. Es heißt native Apps, die sich richtig anfühlen."

### Tom bewertet: Worauf er achtet

| Kriterium | Toms Maßstab |
|-----------|-------------|
| **Erster Eindruck** | Premium? Durchdacht? Oder Template-Feeling? |
| **Time-to-Value** | Ergebnis in < 60 Sekunden nach Installation? |
| **Pricing** | Transparent, fair, kein Dark Pattern? |
| **Cross-Platform** | Gleiche Qualität auf Win/Android/iOS/macOS? |
| **Defaults** | Smarte Voreinstellungen, die er nicht ändern muss? |
| **Bloat-Faktor** | Nur Features die er braucht? Kein Featuritis? |

### Toms Red Flags

- Template-Design (generische Hero-Section mit Gradient + Stock-Foto)
- "Wähle dein Plan" vor dem ersten Ergebnis
- Mehr als 2 Permissions-Dialoge beim Start
- Unterschiedliche UX auf verschiedenen Plattformen
- Marketing-Sprache in der App ("KI-revolutioniert dein Diktier-Erlebnis!")

---

## 4. Persona 3: Sarah Okonkwo {#sarah}

### Kurzprofil

**Sarah Okonkwo, 28** — Teamleiterin Customer Support bei "ShopNova" (E-Commerce, 800 Bestellungen/Tag). Verantwortlich für ein 8-köpfiges Support-Team. Die Frau, die jedes neue Tool zuerst testet und dann für oder gegen den Team-Einsatz entscheidet.

### Tagesablauf

- **08:00** — Büro: 2-Monitor-Setup hochfahren, Headset an, Ticket-Queue checken
- **08:15** — Erste Diktat-Session: Antworten auf Nacht-Tickets (60+ Stück)
- **10:00** — Team-Meeting: Eskalationen besprechen, Wissensbasis aktualisieren
- **10:30** — Diktat: Trainingsmaterial für neue Teammitglieder erstellen
- **12:00** — Mittagspause (einzige Pause vom Diktat)
- **13:00** — Nachmittags-Schicht: Live-Chat-Support, diktiert Ticket-Zusammenfassungen
- **15:00** — Qualitätskontrolle: Stichproben der Team-Antworten prüfen
- **16:30** — Reporting: Tagesbericht diktieren, KPIs zusammenfassen
- **17:30** — Feierabend

### Technik-Verhältnis

Sarah ist eine **Power-Userin und Tool-Evaluatorin**. Sie ist nicht Entwicklerin, aber sie ist die Person in der Firma, die Tools findet, testet und ausrollt. Sie erstellt Makros, kennt Tastenkürzel, und hasst es, wenn ein Tool ihre Geschwindigkeit bremst.

**Was sie kann:**
- Tastenkürzel für jede häufige Aktion
- Custom-Wörterbücher und Text-Bausteine erstellen
- Team-Lizenzen verwalten und einrichten
- Einfache Automationen (Zapier, Power Automate)
- Barrierefreiheits-Features bewerten (Teammitglied ist sehbehindert)

**Was sie braucht:**
- Sofortiges Start/Stop per Tastenkürzel (Strg+Shift+D oder ähnlich)
- Diktat-Indikator immer sichtbar (ist es gerade aktiv? Aufnahme läuft?)
- Zuverlässige Erkennung von Fachbegriffen (Produktnamen, Ticketnummern, Firmensprache)
- Custom-Wörterbuch für Support-Fachsprache
- Team-Verwaltung: gemeinsame Einstellungen, Wörterbücher, Lizenzen
- Verlässlichkeit: Es darf nicht abstürzen. Diktierter Text darf nicht verloren gehen.

**Was sie verrückt macht:**
- Mausklick statt Tastenkürzel für häufige Aktionen
- Kein sichtbarer Status (diktiere ich gerade oder nicht?)
- Unzuverlässige Erkennung bei Fachbegriffen
- Kein Team-Management (Einzellizenzen × 8 = Katastrophe)
- Jede Mikro-Verzögerung × 200 Tickets/Tag = Stunden verlorene Produktivität

### Typische Zitate

> "Wenn ich für jedes Diktat 2 Sekunden länger brauche als nötig, sind das am Ende des Tages 6-7 Minuten. Mal 5 Tage, mal 50 Wochen — das sind über 25 Stunden pro Jahr. Pro Person."

> "Ich brauche ein Tastenkürzel, das IMMER funktioniert. Egal ob ich gerade im Browser, in Slack oder im Ticket-System bin."

> "Mein Teammitglied Luis ist sehbehindert und nutzt einen Screenreader. Wenn die App nicht barrierefrei ist, kann ich sie nicht fürs Team einsetzen."

> "Ein Custom-Wörterbuch ist kein Nice-to-have. Unsere Kunden heißen 'Müller Schraubentechnik GmbH' — das muss die App lernen können."

> "Ich evaluiere jedes Tool eine Woche lang. Am ersten Tag teste ich die Basics. Ab Tag 3 teste ich, was bei 200 Tickets passiert. Am Tag 5 weiß ich, ob es hält."

### Sarah bewertet: Worauf sie achtet

| Kriterium | Sarahs Maßstab |
|-----------|---------------|
| **Tastenkürzel** | Gibt es globale Hotkeys? Funktionieren sie in jeder App? |
| **Status-Feedback** | Weiß sie IMMER, ob Diktat aktiv ist? Visuell + akustisch? |
| **Zuverlässigkeit** | Stürzt es ab? Geht Text verloren? Funktioniert es 8h am Stück? |
| **Fachbegriffe** | Erkennt es Produktnamen und Fachsprache? Custom-Wörterbuch möglich? |
| **Team-Features** | Team-Lizenzen? Gemeinsame Einstellungen? Admin-Dashboard? |
| **Barrierefreiheit** | Screenreader-kompatibel? Keyboard-navigierbar? Kontrast ausreichend? |
| **Performance** | Latenz < 500ms? Kein Lag bei Dauerbetrieb? |

### Sarahs Red Flags

- Kein globaler Hotkey (nur In-App-Button)
- Kein sichtbarer Diktat-Status
- Keine Team-/Business-Lizenz
- Keine Möglichkeit für Custom-Wörterbücher
- Accessibility-Probleme (fehlende aria-labels, kein Keyboard-Support)
- Performance-Degradation nach 30+ Minuten Dauerbetrieb

---

## 5. Bewertungsmatrix {#matrix}

### Gewichtung pro Persona und Kriterium

| Kriterium | Mia (Gewicht) | Tom (Gewicht) | Sarah (Gewicht) |
|-----------|--------------|--------------|----------------|
| Verständlichkeit der Texte | **Hoch** | Mittel | Mittel |
| Visuelles Design / Premium-Gefühl | Mittel | **Hoch** | Niedrig |
| Datenschutz-Kommunikation | **Hoch** | Mittel | Niedrig |
| Time-to-Value / Onboarding | **Hoch** | **Hoch** | Mittel |
| Tastenkürzel / Effizienz | Niedrig | Niedrig | **Hoch** |
| Status-Feedback | Niedrig | Niedrig | **Hoch** |
| Cross-Platform-Konsistenz | Niedrig | **Hoch** | Niedrig |
| Barrierefreiheit | Niedrig | Niedrig | **Hoch** |
| Pricing-Transparenz | Mittel | **Hoch** | Mittel |
| Team-Features | Nicht relevant | Nicht relevant | **Hoch** |
| Fachbegriff-Erkennung | Niedrig | Niedrig | **Hoch** |
| Fehler-Kommunikation | **Hoch** | Mittel | Mittel |

### Wie die Matrix zu lesen ist

- **Hoch**: Dieses Kriterium ist für diese Persona geschäftskritisch. Probleme hier → hohes Kipppunkt-Risiko.
- **Mittel**: Dieses Kriterium ist merkbar, aber kein Dealbreaker allein.
- **Niedrig**: Dieses Kriterium ist für diese Persona nicht im Fokus.
- **Nicht relevant**: Dieses Kriterium existiert nicht im Kontext dieser Persona.

---

## 6. Häufige UX-Probleme nach Persona-Typ {#heuristiken}

### Probleme, die Mia (nicht-technisch) findet, aber Entwickler übersehen

1. **Versteckte Fachsprache**: Begriffe wie "Modell", "Engine", "Pipeline", "lokal", "Latenz", "Sync" sind für Entwickler selbstverständlich — für Mia Fremdwörter.
2. **Optionen-Overload**: Jede Einstellung, die Mia nicht versteht, erzeugt Unsicherheit. Unsicherheit → Abbruch.
3. **Implizite Datenschutz-Annahmen**: "Daten werden zur Verbesserung des Service genutzt" ist für Entwickler eine Standardklausel. Für Mia ist es eine Bedrohung: "Wer liest meine Kundentexte?"
4. **Fehlende Orientierung**: Entwickler kennen den Flow. Mia nicht. Jeder Screen ohne klaren nächsten Schritt ist ein Abbruch-Risiko.

### Probleme, die Tom (Entscheider) findet, aber Designer übersehen

1. **Template-Feeling**: Tom hat 200 Apps gesehen. Er erkennt sofort, ob ein Design generisch ist. Generisches Design → kein Vertrauen in das Produkt.
2. **Time-to-Value-Barrieren**: Jeder Schritt zwischen Installation und erstem Ergebnis senkt Toms Interesse. 3 Schritte sind ok. 7 sind zu viel.
3. **Pricing-Intransparenz**: Tom will sofort wissen, was es kostet und was er dafür bekommt. Versteckte Preise → Verdacht auf Dark Patterns.
4. **Plattform-Inkonsistenz**: Wenn die iOS-App poliert ist aber die Windows-App hinterherhinkt, schließt Tom: "Das Team priorisiert eine Plattform. Meine wird vernachlässigt."

### Probleme, die Sarah (Power-User) findet, aber Product Manager übersehen

1. **Fehlende Tastenkürzel**: Ein Button, den man 200x/Tag klickt, MUSS ein Tastenkürzel haben.
2. **Unsichtbarer Status**: Diktat aktiv? Verarbeitung läuft? Gespeichert? Sarah braucht IMMER Feedback.
3. **Performance-Degradation**: Das Tool funktioniert in der 5-Minuten-Demo. Aber nach 2 Stunden Dauerbetrieb? Memory-Leaks? Lag?
4. **Keine Team-Skalierung**: Ein Tool, das für Einzelnutzer designed ist, kann nicht für ein 8-Personen-Team eingesetzt werden. Fehlende Team-Features → Dealbreaker für Sarah (sie entscheidet für 8 Lizenzen).
5. **Barrierefreiheits-Lücken**: Luis im Team nutzt einen Screenreader. Wenn aria-labels fehlen, kann Sarah das Tool nicht einsetzen.

---

## 7. Szenarien für Persona-Tests {#szenarien}

### Szenario 1: Erster App-Start (Onboarding)

**Mia**: Öffnet die App zum ersten Mal. Erwartet, in 30 Sekunden zu verstehen, was sie tun soll, und in 60 Sekunden ihr erstes Diktat zu starten. Jede technische Frage ("Welches Modell?") ist ein Kipppunkt.

**Tom**: Installiert die App zwischen zwei Meetings. Hat genau 90 Sekunden Geduld. Erwartet sofort Premium-Design und ein erstes Ergebnis. Bewertet parallel, ob die App sein Geld wert wäre.

**Sarah**: Evaluiert die App systematisch. Tag 1: Basis-Funktionen testen. Prüft: Tastenkürzel? Status-Anzeige? Team-Pricing? Wenn eins davon fehlt, ist die Evaluation nach Tag 1 vorbei.

### Szenario 2: Einstellungen / Konfiguration

**Mia**: Geht selten in Einstellungen. Wenn, dann weil etwas nicht funktioniert. Erwartet verständliche Labels und hilfreich erklärte Optionen. Jede unverständliche Einstellung erzeugt Angst ("Was passiert, wenn ich das ändere?").

**Tom**: Schaut sich Einstellungen einmal an, um zu bewerten, ob die App durchdacht ist. Erwartet smarte Defaults. Verändert max. 1-2 Dinge. Erwartet, dass die App ohne Konfiguration gut funktioniert.

**Sarah**: Verbringt 20 Minuten in den Einstellungen beim Setup. Konfiguriert Tastenkürzel, richtet Custom-Wörterbuch ein, sucht Team-Features. Erwartet Granularität und Kontrolle — aber logisch strukturiert.

### Szenario 3: Fehlerfall

**Mia**: Diktat funktioniert nicht. Erwartet eine Meldung in Alltagssprache: "Diktat konnte nicht gestartet werden. Prüfe, ob dein Mikrofon angeschlossen ist." NICHT: "Error: Audio capture failed (0x80070005)".

**Tom**: Diktat-Qualität ist schlecht. Erwartet entweder automatische Verbesserung oder eine klare Option: "Verbesserte Genauigkeit aktivieren (benötigt Internetverbindung)". Keine technische Erklärung warum.

**Sarah**: Diktat stürzt nach 45 Minuten ab. Erwartet: (1) Kein Textverlust — der diktierte Text muss erhalten bleiben. (2) Automatischer Neustart. (3) Crash-Report an Support mit Referenznummer. (4) Keine Unterbrechung des Ticket-Workflows.

### Szenario 4: Pricing / Upgrade

**Mia**: Möchte wissen, ob es gratis geht oder was es kostet. Erwartet einfache Preise: "5€/Monat" oder "einmalig 29€". Kein Feature-Matrix-Vergleich mit 15 Zeilen.

**Tom**: Bewertet das Pricing-Modell professionell. Schaut auf: Preis-Leistung, Fairness, ob Premium-Features auch wirklich Premium-Wert liefern. Hasst: "Enterprise — Kontaktiere uns".

**Sarah**: Braucht Team-Pricing. Sucht: Preis pro Nutzer, Mengenrabatt, zentrale Abrechnung, Admin-Dashboard. Wenn es nur Einzellizenzen gibt, muss sie 8 separate Käufe managen → Dealbreaker.
