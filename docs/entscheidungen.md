# Entscheidungen

Jede Entscheidung mit Datum, Begründung und verworfenen Alternativen. Einträge werden nie gelöscht. Wird eine Entscheidung revidiert, bekommt sie den Vermerk „verworfen am …“ und eine neue Zeile.

| Datum | Entscheidung | Begründung | Verworfene Alternativen |
|---|---|---|---|
| 2026-11-17 | Projekt: Point-and-Click-Adventure | Arbeit lässt sich gut aufteilen und parallelisieren, der Umfang lässt sich bewusst begrenzen | – |
| 2026-11-17 | Plattform: Web App, agentic first, Quality Gating als Kern | Teamvorgabe; Gates und Agentenregeln aus Referenzprojekten übertragbar ([Quellen](quellen.md)) | Desktop-Engine (Godot, Unity) |
| 2026-11-17 | Rollen: Max PO, Dimi SM, Lars Architekt, Fabian Creative, Benedict Creative und Architektur, Ivan und Mahmud Fullstack | Teamentscheidung; Architekten sind Code-Owner der Gates, Creative von `content/` | – |
| 2026-11-17 | Zusage: 11 NF, 6 FA Entwicklungsmodus, 15 Prozess-Gates, alle maschinell geprüft | Zusagen werden später gemessen, daher nur, was ein Gate ab Sprint 1 prüfen kann; Rest unter „Ausbau“ | Vollständiges Gate-Set eines Referenzprojekts |
| 2026-11-17 | Entwicklungsmodus mit Testzuständen, erzeugt aus Checkpoints des Lösungswegs | Beim Testen direkt an eine Stelle springen; Erzeugung aus dem Lösungsweg verhindert veraltete Zustände | nur von Hand gepflegte Spielstände |
| 2026-11-17 | Personas P-01 bis P-03 als Proto-Personas, unabhängig vom Spielinhalt | Spielkonzept steht noch nicht; Anpassung bei Rückmeldungen von Spielern | Personas erst nach Spielkonzept |
| 2026-11-17 | Dokumentation lebt in diesem Repo unter `docs/` | Ein Ort für Team und Agenten; Agenten lesen dieselben Anforderungen, gegen die die Gates prüfen | Doku in privaten Notizen |
| 2026-11-17 | Stack und Engine-Konzept der Architektur: React, TypeScript, Vite, SVG-Räume mit Zod-validierter JSON-Definition, A*-Wegsuche, GSAP, Spiellogik in `src/engine/core` | Vorgabe der Architektur ([Engine-Konzept](architektur/engine-konzept.md)); Inhalte ohne Codeänderung passen zu agentic first | Canvas-Engine (Phaser) |
| 2026-11-17 | Funktionale IDs: `FA-E` = Engine (Architektur-Nummern), Entwicklungsmodus umbenannt in `FA-DEV` | Architektur-IDs bleiben wiedererkennbar; Entwicklungsmodus war noch nicht committet | Architektur-IDs umnummerieren |
| 2026-11-17 | Nur Desktop-Browser: kein Smartphone, keine Responsiveness, Barrierefreiheit kein Ziel | Teamentscheidung, Umfang begrenzen | Mobile Bedienung, WCAG 2.2 AA |
| 2026-11-17 | Alle Assets erstellt das Team selbst | Teamentscheidung; keine Fremdlizenzen | Lizenzierte Quellen |
| 2026-11-17 | Stakeholder Peer-Team, Kommilitonen als Testspieler, Spieler mit Einschränkungen, Asset-Urheber gestrichen; Persona Meike gestrichen | Folgen aus den Entscheidungen oben; Peer-Prüfung bleibt als Qualitätskriterium in den Modulvorgaben | – |
| 2026-11-17 | Asset-Budget je Raum gestrichen; Dateigröße, Duplikate, ungenutzte Abhängigkeiten zugesagt (NF-W-05 bis NF-W-07) | Teamentscheidung | – |
| 2026-11-17 | IDs neu durchnummeriert statt „gestrichen“ | Noch nichts committet, keine externen Verweise | – |
| 2026-11-17 | Creative-Anforderungen Alchemie und Questgegenstände übernommen als FA-G-01 bis FA-G-08 | Vorgabe Creative; Wortlaut nur bei Verstößen gegen die Qualitätskriterien angepasst, FA-02 geteilt ([Gegenstände](creative/gegenstaende.md)) | – |
| 2026-11-19 | Eine Freigabe pro PR, nach Zuständigkeit: Anforderungen, Doku und Prozess gibt der PO frei, Code, Pipeline und Konfiguration Lars, Gate-Dateien die Architekten (EP-11), Kleinigkeiten wie Tippfehler jede Person außer dem Autor | Eine Freigabe hält den Fluss bei sieben Personen. Fachliche und technische Verantwortung bleiben getrennt. Selbstfreigabe ist ausgeschlossen (EP-03). Umsetzung als `CODEOWNERS` und Ruleset durch die Architekten | zwei Freigaben je PR; nur PO und Scrum Master als Approver |
