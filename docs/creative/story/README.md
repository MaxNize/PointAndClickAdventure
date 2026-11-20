# Story und Worldbuilding

Arbeitsordner von Creative (Fabian, Benedict). Hier klären wir Welt und Handlung Frage für Frage. Stand: 2026-11-20. Der Rahmen steht, die Handlung entsteht Stück für Stück.

## So arbeiten wir damit

**Fang bei [fragen.md](fragen.md) an.** Dort stehen immer nur die drei bis fünf Fragen, die gerade wichtig sind. Trag deine Antworten ein und sag dann im Chat „Story weiter“, oder sprich einfach über die Story. Der Skill `story` ([.claude/skills/story/SKILL.md](../../../.claude/skills/story/SKILL.md)) arbeitet die Antworten ein, passt die Themendokumente an und schreibt die nächsten Fragen.

Im Hintergrund führt die KI [ki-plan.md](ki-plan.md) mit dem vollständigen Stand. Diese Datei musst du nicht lesen.

Du kannst jedes Themendokument auch direkt lesen und ändern, oder im Chat Input dazu geben. Deine Änderungen gelten mehr als die Vorschläge der KI.

1. Jede Frage hat eine ID, z. B. `KI-03`. In Commits und Gesprächen nennen wir die ID.
2. Bei vielen Fragen steht ein **Vorschlag**. Er ist nur ein Startpunkt, den wir annehmen, ändern oder verwerfen.
3. Ist eine Frage entschieden, stehen unter **Antwort** das Ergebnis und das Datum, und sie ist abgehakt: `- [x]`.
4. Stehen Kern, Twist und Spielrahmen, fassen wir alles in einer „Bibel“ zusammen (`welt.md`, später). Die Fragedokumente bleiben als Begründung.

## Reihenfolge

| # | Dokument | Inhalt | Präfix |
|---|---|---|---|
| 0 | [00-ausgangsidee.md](00-ausgangsidee.md) | Die Idee aus dem Treffen, Einschätzung, Vorschlag für den roten Faden | – |
| 1 | [01-kernidee-und-twist.md](01-kernidee-und-twist.md) | Meteor, Wesen, Strippenzieher, Homunkuli, Ausbruch | `KI` |
| 2 | [02-alchemie.md](02-alchemie.md) | Regeln der Transmutation und der Homunkuli | `AL` |
| 3 | [03-planet.md](03-planet.md) | Planet, Himmel, Geografie, Einschlagsort | `PL` |
| 4 | [04-ressourcen.md](04-ressourcen.md) | Meteorgestein, Energie, Wirtschaft, Spielressourcen | `RS` |
| 5 | [05-nationen.md](05-nationen.md) | Nationen, Glaube, Akademie, Konflikte | `NA` |
| 6 | [06-timeline.md](06-timeline.md) | Zeitleiste vom Einschlag bis zum Spielende | `ZL` |
| 7 | [07-figuren.md](07-figuren.md) | Rollen der vorhandenen Figuren: Täter, Opfer, Verbündete | `FG` |
| 8 | [08-enden-und-hinweise.md](08-enden-und-hinweise.md) | Woran man den Twist merkt, zwei Enden, Folgen für die Engine | `EN` |
| 9 | [09-kapitel.md](09-kapitel.md) | Aufbau der einzelnen Kapitel, Arten der Rettung | `KA` |
| 10 | [10-handlung.md](10-handlung.md) | Die Story Stück für Stück, von vorn nach hinten | `ST` |

`KI` zuerst, weil alles andere daran hängt. `PL`, `RS`, `NA` und `ZL` lassen sich danach in beliebiger Reihenfolge klären.

## Leitplanken aus dem Projekt

Diese Punkte stehen schon fest und begrenzen die Story:

- **Kurzes Spiel.** Ein Semesterprojekt, im Browser von Anfang bis Ende lösbar ([Projektsteckbrief](../../projektsteckbrief.md)). Die Welt darf groß sein, das Spiel zeigt aber nur wenige Räume. Faustregel: Was der Spieler nie sieht oder hört, braucht nur einen Satz.
- **Scherenschnitt ist der Spielstil.** Figuren sind dunkle Silhouetten mit eigener Leuchtfarbe ([Styleguide](../temp/STYLEGUIDE_Charaktere.md)).
- **Faire Rätsel ohne Sackgassen.** Persona P-02 erwartet das ([Personas](../../voranalyse/02-personas.md)). Der Twist darf nicht vom Zufall abhängen.
- **Inhalte nur als SVG und JSON** (NF-W-01). Braucht die Story etwas, das die Engine nicht kann (z. B. Zähler statt boolescher Flags), wird daraus ein Story-Vorschlag an die Architektur ([Offene Fragen](../../offene-fragen.md#asset-vertrag-und-werkzeuge)).
- **Schauplatz bisher:** eine Akademie der Alchemie mit Lehrsaal, Bibliothek, Küche, Tor. Figuren: Alchemistin, Lehrling, Meister, Erzalchemist, Schmied, Professor Gernegroß und zehn NPCs.
