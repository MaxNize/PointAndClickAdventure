# Stakeholder und Rollen

Schritt 1 der Voranalyse. Ergebnis: wer betroffen ist (SH), welche Rollen das System kennt (SR) und wer im Projekt was verantwortet (PR). Weiter mit [Personas](02-personas.md).

## Stakeholder

Einfluss und Interesse: Einschätzung des Teams, Skala hoch / mittel / gering.

| ID | Stakeholder | Erwartung | Einfluss | Interesse | Umgang |
|---|---|---|---|---|---|
| SH-01 | Dozent / Prüfer | Messbare Zusagen, nachvollziehbarer Prozess | hoch | hoch | eng einbinden |
| SH-02 | Projektteam | Machbarer Umfang, klare Aufteilung. Erstellt auch alle Assets selbst. | hoch | hoch | eng einbinden |
| SH-03 | Hochschule | Rolle wird beim Dozenten erfragt (siehe [Offene Fragen](../offene-fragen.md)) | hoch | gering | zufriedenstellen |
| SH-04 | Gelegenheitsspieler | Ohne Installation am Rechner spielen, Fortschritt bleibt erhalten | gering | mittel | über Persona P-01 |
| SH-05 | Genre-Fans | Faire Rätsel, keine Sackgassen | gering | hoch | über Persona P-02 |
| SH-06 | Anbieter KI-Werkzeug, Git-Hoster | Nutzungsbedingungen, Kontingente | mittel | gering | beobachten |

**Einfluss-Interesse-Matrix**

| | Interesse gering | Interesse mittel / hoch |
|---|---|---|
| **Einfluss hoch** | zufriedenstellen: SH-03 | eng einbinden: SH-01, SH-02 |
| **Einfluss mittel** | beobachten: SH-06 | – |
| **Einfluss gering** | – | über Personas vertreten: SH-04, SH-05 |

**Folgerung:** Die Spieler haben kaum Einfluss, aber das Produkt ist für sie. Sie kommen über Personas ins Backlog.

**KI-Agenten sind keine Stakeholder.** Sie haben kein eigenes Interesse, handeln aber im Projekt. Deshalb haben sie eine Projektrolle (PR-06) mit festen Rechten. Ihre Arbeit verantwortet der Mensch, der sie startet.

## Systemrollen

Rollen, die das Spiel kennt. Sie stehen in der Spalte „Nutzerrolle“ der FA.

| ID | Rolle | Wer | Zugang |
|---|---|---|---|
| SR-01 | Spieler | jede Person im Desktop-Browser | ohne Konto, über die URL |
| SR-02 | Entwickler | Teammitglied oder Agent | Entwicklungsmodus, nur im Entwicklungs-Build (FA-DEV-01 bis FA-DEV-06) |

Keine Admin- oder Kontorolle: Es gibt kein Backend. Kommt eine Online-Speicherung dazu, entsteht die Rolle „Registrierter Spieler“.

## Projektrollen

Vorgehen: Scrum. Sieben Personen, Besetzung vom Team festgelegt.

| ID | Rolle | Person | Verantwortung | Rechte im Repo |
|---|---|---|---|---|
| PR-01 | Product Owner | Max | Backlog, Priorisierung, Abnahme gegen Akzeptanzkriterien, vertritt die Personas | Story auf „fertig“ setzen |
| PR-02 | Scrum Master | Dimi | Prozess, Hindernisse, Definition of Done | Story abnehmen, wenn PR-01 sie selbst umgesetzt hat |
| PR-03 | Architekt | Lars, Benedict | [Engine-Konzept](../architektur/engine-konzept.md), Architekturgrenzen, Gates, Schwellenwerte, `AGENTS.md`, Pipeline | Code-Owner der Gate-Dateien (EP-11) |
| PR-04 | Creative | Fabian, Benedict | Story, Räume, Figuren, Gegenstände, Animationen, Rätsel, Dialoge, Ton, Lösungsweg mit Checkpoints. Vorgabe zu Alchemie und Quests: [Gegenstände](../creative/gegenstaende.md). Alle Assets entstehen im Team. | Code-Owner von `content/` |
| PR-05 | Fullstack-Entwickler | Ivan, Mahmud | Spiellogik, Oberfläche, Entwicklungsmodus, Tests | – |
| PR-06 | Agent | – | Aufgaben einer Story im eigenen Worktree | Rechte und Verbote: EP-11 bis EP-15 |

Alle Menschen (PR-01 bis PR-05) dürfen Agenten starten und PRs anderer freigeben.

**Regeln der Rollentrennung**
1. Wer einen Agenten startet, gilt als Autor von dessen PR. Freigeben muss eine andere Person (EP-03).
2. Gate-Änderungen kommen in einen eigenen PR mit Begründung, nie zusammen mit Spielcode.
3. Benedict sitzt in PR-03 und PR-04. Er verantwortet damit das Schema der Inhaltsdateien, die Schnittstelle zwischen Creative und Code.
