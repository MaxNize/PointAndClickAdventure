# Entwicklungsprozess

Scrum im Projekt, für Menschen und Agenten. Das Board ist das [GitHub-Projekt Nr. 6](https://github.com/users/MaxNize/projects/6). Rollen stehen in [Stakeholder und Rollen](../voranalyse/01-stakeholder-und-rollen.md).

## Sprints

Jeder Sprint endet am Tag eines Reviews. Die Reviews sind die Vorlesungstermine. Sprint 3 und 4 teilen die Weihnachtspause, dazwischen gibt es kein Review.

| Sprint | Zeitraum | Review | Ziel |
|---|---|---|---|
| 1 | 19.11. bis 26.11. | 26.11. | Projekt steht |
| 2 | 26.11. bis 03.12. | 03.12. | `main` ist geschützt |
| 3 | 03.12. bis 17.12. | – | Ein Raum läuft |
| 4 | 17.12. bis 14.01. | 14.01. | Zwei Räume, Figur läuft |
| 5 | 14.01. bis 28.01. | 28.01. | Alchemie |
| 6 | 28.01. bis 18.02. | 18.02. | Lösbar und testbar |
| 7 | 18.02. bis 25.02. | 25.02. | Feature-complete |
| 8 | 25.02. bis 09.03. | 09.03. | Feature-Freeze: nur Tests, Fehlerkorrekturen und Doku |

Das letzte Review ist die Endpräsentation: 10 Minuten Vorgehen, 10 Minuten Produktvorstellung (Screenshots, Video, Erklärung), danach die Produktdemo.

## Statusweg eines Tickets

| Status | Bedeutung | Gesetzt von |
|---|---|---|
| Backlog | Entwurf, noch nicht geprüft | automatisch, sobald das Issue im Projekt ist |
| Bereit | Wortlaut geprüft, Abhängigkeiten geklärt | nur der PO |
| In Arbeit | Jemand hat angefangen | wer die Arbeit beginnt, von Hand |
| In Review | PR ist offen | automatisch, sobald der PR mit `Closes #n` verlinkt ist |
| Fertig | Definition of Done erfüllt | automatisch beim Merge des PRs oder Schließen des Issues |

Ohne `Closes #n` im PR bleibt das Ticket stehen. Wer einen PR nach Review-Kommentaren überarbeitet, setzt das Ticket zurück auf „In Arbeit“. `Aufwand` schätzt das Team im Sprint Planning, `Sprint` setzt das Planning. Beides setzt kein Agent.

## Welche Story darf angefangen werden

- Sie liegt im **aktuellen Sprint** (`sprint:@current`).
- Ihr Status ist **Bereit**.
- Sie hat keine offene „Blocked by“-Beziehung.
- Niemand anderes hat sie schon begonnen.

Ein Agent arbeitet an der Story des Menschen, der ihn startet (PR-06). Fehlt eine Voraussetzung im Katalog, legt er keine ID an, sondern schlägt sie dem PO vor.

## Definition of Done

Ein Ticket ist fertig, wenn alles gilt:

1. Das Akzeptanzkriterium ist durch einen Test belegt, der die Story-ID im Namen trägt (EP-07).
2. `make ci` endet nach der letzten Änderung mit Exit-Code 0 (EP-01). Bis das Gerüst steht, gelten die vorhandenen Prüfungen und ihr Ergebnis steht im PR.
3. Der PR nutzt die Vorlage, trägt die Story-ID im Titel (EP-08), enthält `Closes #n` und den Abschnitt „KI-Beteiligung“.
4. Der PR ist freigegeben (siehe unten).
5. Der PO hat die Story gegen das Akzeptanzkriterium abgenommen, **vor dem Merge**.
6. Doku und Verweise sind im selben PR nachgezogen.

## Freigabe und Abnahme

| Thema | Freigabe durch |
|---|---|
| Anforderungen, Doku, Prozess | der PO |
| Code, Pipeline, Konfiguration | Lars |
| Gate-Dateien, `AGENTS.md` | die Architekten (EP-11) |
| Kleinigkeiten, z. B. Tippfehler | jede Person außer dem Autor |

Der Autor gibt seinen PR nie selbst frei (EP-03). Wer einen Agenten startet, gilt als Autor. Die **Abnahme** ist davon getrennt: Der PO prüft die Story gegen das Akzeptanzkriterium und ist dafür Reviewer im PR. Hat der PO die Story selbst umgesetzt, nimmt der Scrum Master ab (PR-02).

Die Regel ist beschlossen ([Entscheidungen](../entscheidungen.md)). Technisch erzwungen wird sie erst, wenn die Architekten `CODEOWNERS` und das Ruleset umgesetzt haben (EP-02, EP-03, EP-11). Bis dahin gilt sie als Absprache.

## Aufgaben ohne Story-ID

Doku- und Prozessaufgaben laufen über Issues mit dem Label `prozess` und der Vorlage „Prozessaufgabe“. Sie enthalten **keinen Code**. Für Code gilt immer: Story-ID, sonst kein Code.

## Branches und Worktrees

Bis `make worktree` existiert (EP-14): Worktree unter `../worktrees/<kurzname>`, Branch `<typ>/<kurzname>` mit dem Typ des Conventional Commit (`docs`, `feat`, `fix`). Keine Arbeit im Hauptverzeichnis.

## Rhythmus im Sprint

- **Planning:** Das Team schätzt `Aufwand` mit 1, 2, 3, 5, 8 und ordnet Stories dem Sprint zu. Alles über 8 wird geteilt. Alle Anforderungen im Katalog sind Zusagen.
- **Burndown:** Der Scrum Master legt ihn aus dem Projekt an (Insights) und legt am Sprint-Ende einen Screenshot ab.
- **Review und Retro:** Am Review-Tag zeigt das Team die Ergebnisse. Die Retro-Notizen stehen mit dem Burndown in `docs/prozess/sprint-<n>.md`.

## Belege für die Präsentation

- **Empfohlen:** Bei Stories mit sichtbarer Wirkung ein Screenshot im PR, abgelegt unter `docs/praesentation/screenshots/<Story-ID>.png`.
- **Pflicht für den Scrum Master:** Burndown und Retro pro Sprint (siehe oben).

Aus diesen Dateien entsteht Teil 1 der Präsentation (Vorgehen), aus den Screenshots und dem Video Teil 2.
