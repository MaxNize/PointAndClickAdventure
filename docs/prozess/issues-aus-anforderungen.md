# Issues aus Anforderungen anlegen

Für Architektur, Creative und ihre Agenten. Der Anforderungskatalog ([`03-anforderungen.md`](../voranalyse/03-anforderungen.md)) ist maßgeblich. Das Issue verweist nur darauf.

## Ablauf

| Schritt | Wer | Ergebnis |
|---|---|---|
| 1 | Autor (Mensch oder Agent) | Anforderung steht im Katalog, nach den [Qualitätskriterien](../vorgaben-modul.md#qualitätskriterien) und mit neuer ID. Eigener PR, Freigabe nach der [Freigaberegel](../entscheidungen.md). |
| 2 | Autor | Erst nach dem Merge: Issue anlegen (siehe unten). Die Vorschau geht vorher an den PO. |
| 3 | PO | Prüft Wortlaut, Typ, Bereich und Abhängigkeiten. Setzt den Status auf **Bereit**. |
| 4 | Team | Schätzt `Aufwand` und ordnet den **Sprint** zu, im Sprint Planning. |

Nur der PO setzt **Bereit**. Ein Issue im Status **Backlog** ist ein Entwurf und kommt in keinen Sprint.

## Vorschau vor dem Anlegen

Ein Agent legt keine Issues im Block an, bevor ein Mensch die Vorschau gesehen hat. Die Vorschau ist eine Tabelle mit ID, Titel, Typ, Bereich und Abhängigkeiten. Sie geht per Chat oder PR-Kommentar an den PO. Ohne Freigabe entstehen keine Issues.

## Das Issue

| Feld | Regel |
|---|---|
| Titel | `<ID> <Bereich der Anforderung>`, z. B. `FA-E-05 Hotspots`. Keine Namen im Titel, außer `@Name` für Personen, die noch keinen Zugang haben. |
| Label | `story` für `FA-*`, `enabler` für `NF-*` und `EP-*`, `prozess` für Aufgaben ohne Story-ID |
| Body | Die Überschriften des Templates [`story.yml`](../../.github/ISSUE_TEMPLATE/story.yml): `### Story-ID`, `### Anforderung`, `### Akzeptanzkriterium`, `### Abhängigkeiten`. Anforderung und Kriterium **unverändert** aus dem Katalog kopieren. Weicht ein Issue ab, gilt der Katalog. |
| Aufgaben ohne Story-ID | Template [`prozess.yml`](../../.github/ISSUE_TEMPLATE/prozess.yml), Label `prozess`, Typ `Prozess` |

## Felder im Projekt

Das Projekt ist [Point-and-Click-Adventure (Nr. 6)](https://github.com/users/MaxNize/projects/6). Feld-IDs ändern sich, hole sie mit `gh project field-list 6 --owner MaxNize --format json`.

| Feld | Wer setzt es |
|---|---|
| `Typ` | Autor: `Story` (FA), `Enabler` (NF, EP), `Bug`, `Prozess` |
| `Bereich` | Autor, nach der Tabelle unten |
| `Status` | Neue Issues stehen automatisch auf `Backlog`. **Bereit** setzt nur der PO. |
| `Aufwand`, `Sprint`, `Priorität` | **Nicht der Autor.** Sprint Planning und PO. |

| Gruppe | Bereich |
|---|---|
| FA-E, FA-G, FA-DEV, NF-A, NF-E, NF-V-03, NF-V-04 | Fullstack |
| NF-W, NF-V-01, NF-V-02, EP | Architektur |
| Creative-Aufgaben, Inhalte | Creative |
| Projekt, Prozess, Doku | PO/SM |

Die Verteilung auf Personen entscheidet das Team im Planning. Ein Autor weist nur zu, wenn er das Issue selbst umsetzt.

Neue Issues kommen ins Projekt mit `gh project item-add 6 --owner MaxNize --url <issue-url>`.

## Abhängigkeiten

- **Erzwungen (native „Blocked by“-Beziehung):** nur, wenn Katalog oder Engine-Konzept sie stützen. Beispiel: FA-E-16 braucht den Ausgang-Hotspot aus FA-E-05. Setzen per GraphQL `addBlockedBy(input: {issueId, blockingIssueId})`. Im Body stehen die Nummern unter `**Blockiert durch:**` und `**Blockiert:**`.
- **Vorschlag zur Reihenfolge:** Technisch plausibel, aber nicht belegt? Nur als Textzeile im Body, mit dem Zusatz „zu prüfen, nicht erzwungen“. Sonst zeigt das Board falsche Sperren.
- Fehlt eine Voraussetzung im Katalog, lege kein Issue mit erfundener ID an. Schlage sie dem PO als Anforderung vor (eigenes Issue mit Typ `Prozess`).

## Änderungen und Streichungen

- Die **ID bleibt**, wenn sich eine Anforderung ändert. Der Issue-Text wird im selben PR nachgezogen wie der Katalog.
- Entfällt eine Anforderung, bleibt die ID mit Vermerk „gestrichen“ im Katalog. Das Issue wird **aus dem Projekt entfernt**, nicht geschlossen. Das Schließen würde es auf **Fertig** setzen und den Burndown verfälschen.

## Was ein Agent nicht tut

- Kein `Aufwand`, kein `Sprint`, keine `Priorität` setzen.
- Nicht auf **Bereit** oder **Fertig** setzen.
- Keine ID vergeben oder ändern, ohne dass der PO zugestimmt hat.
- Keine Gate-Dateien ändern ([`AGENTS.md`](../../AGENTS.md), EP-11).
- Bei Massenanlage ein Skript verwenden, das vorhandene Titel überspringt. So lässt sich ein Abbruch ohne Doppelungen wiederholen.
