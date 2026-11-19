# Umsetzungsplan Erstimplementierung

Stand 2026-11-19, Vorschlag der Architektur. Vorgeschlagene Reihenfolge der Stories für die erste Fassung der Engine. Grundlage: [Engine-Konzept](engine-konzept.md), [Asset-Vertrag](asset-vertrag/README.md), [Autoren-Workflow](autoren-workflow.md).

**Verbindlichkeit:** Die Reihenfolge ist ein Vorschlag, zu prüfen, nicht erzwungen. Schritte sind keine Sprints. Sprint, Aufwand, Priorität und Zuweisung legen Planning und PO fest ([Issues aus Anforderungen](../prozess/issues-aus-anforderungen.md)). Erzwungene Abhängigkeiten („Blockiert durch“) stehen nur in den Issues und nur, wo Katalog oder Engine-Konzept sie stützen.

**IDs:** Kursiv gesetzte IDs sind vorläufig. Sie stehen in den [Anforderungsvorschlägen](anforderungs-vorschlaege.md) oder in Issue #78 und werden erst nach Entscheidung des PO zu Issues. Alle anderen IDs stehen im [Katalog](../voranalyse/03-anforderungen.md) und haben schon Issues.

## Prinzip

- **Vertikale Durchstiche:** Jeder Schritt endet mit etwas, das im Referenz-Testraum sichtbar oder per Test prüfbar ist.
- **Creative früh produktiv:** Validator, Gerüst und Raum-Overlay kommen vor der Interaktion, damit Creative parallel Räume und Figuren liefern kann.
- **Referenz-Testraum:** neutraler Inhalt unter `content/`, der jede Vertragsregel abdeckt (Issue #74). Fehlerhafte Varianten für die Validator-Tests liegen getrennt unter `tests/fixtures/`.

## Schritte

| Schritt | Ziel | Stories | Bezug zu bestehenden Issues |
|---|---|---|---|
| S | Spike Claude Design | Prozessaufgabe ohne Story-ID, Ergebnis im [Asset-Vertrag](asset-vertrag/README.md#spike-claude-design) | #69 Schema, #1 Artstyle |
| 0 | Fundament | *EP-16* (Projektgerüst, #78), EP-01, EP-06, EP-14, NF-W-02, NF-W-04, NF-W-05 | #42, #47, #55, #17, #19, #20 |
| 1 | Vertrag ausführbar | NF-V-01 (Zod-Schemas, Validator), *FA-DEV-07*, *FA-DEV-09* | #9, #69, #74 |
| 2 | Raum sichtbar | FA-E-01, *FA-E-03*, *FA-E-04*, *FA-E-02*, NF-W-01, NF-V-04, *FA-DEV-08*, *FA-DEV-10* (Raum) | #23, #16, #12 |
| 3 | Bewegung | FA-E-07, *FA-E-08*, *FA-E-09*, FA-E-10, *FA-E-11*, *FA-E-12*, *FA-DEV-15*, *FA-DEV-10* (Drehpunkte) | #25, #26, #75 Spielfigur |
| 4 | Interaktion | FA-E-05, *FA-E-06*, *FA-E-17*, *FA-E-18*, *FA-G-09*, *FA-G-10*, *FA-E-14*, *FA-E-15*, FA-E-16, FA-DEV-05 | #24, #27, #40 |
| 5 | Gegenstände | FA-G-04, FA-G-07, FA-G-02, FA-G-08, FA-G-01, FA-G-03, FA-G-05, FA-G-06 | #28 bis #35, #71 Meilensteine, #76 Gegenstandsliste |
| 6 | Erzählung | *FA-E-19*, *FA-E-20*, *FA-E-22*, NF-V-02, *FA-DEV-11*, *FA-DEV-12*, *FA-DEV-13*, *FA-DEV-14* | #10, #77 Lösungsweg |
| 7 | Spielstand und Testzustände | *FA-E-21*, NF-V-03, FA-DEV-01 bis FA-DEV-04, FA-DEV-06 | #11, #36 bis #39, #41 |

Gate-Stories aus Schritt 0 sind Gate-Änderungen. Sie gehen als eigene PRs mit Freigabe der Architektur (EP-11).

## Parallele Arbeit nach Bereich

| Bereich | Ab Schritt | Arbeit |
|---|---|---|
| Creative | S | Spike, danach Räume und Figuren nach [Briefing](claude-design-briefing.md) |
| Creative | 1 | Assets gegen den Validator liefern |
| Creative | 2 | Räumliches im Raum-Overlay setzen |
| Creative mit Agent | 4 | Interaktionen aus Prosa-Beschreibungen, Gegenstände und Rezepte aus der Liste (#76) |
| Fullstack | 0 | Engine nach Schritten |
| Architektur | S | Spike auswerten, Gates, Zod-Schemas |

## Issues

- Für Stories mit Katalog-ID gibt es die Issues schon. Ändert der PO FA-E-05 oder FA-E-07, werden #24 und #25 im selben PR nachgezogen.
- Für vorläufige IDs entstehen Issues erst nach Aufnahme in den Katalog und dem Merge. Die Vorschau dafür steht in den [Anforderungsvorschlägen](anforderungs-vorschlaege.md#vorschau-der-issues).
- Der Spike wird als Prozessaufgabe angelegt (Template `prozess.yml`, Bereich Creative), nach Vorschau an den PO.

## Nicht in der Erstimplementierung

Ton und Musik, Zähler-Flags, Sackgassen-Suche und alles unter „Ausbau“ in den [Anforderungen](../voranalyse/03-anforderungen.md#4-nicht-zugesagt).
