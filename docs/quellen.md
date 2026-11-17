# Quellen

Woher die technischen Anforderungen stammen. Ausgewertet wurde nur der technische Teil der Referenzprojekte, nicht ihre Fachlichkeit.

## Referenzprojekt PflanzenDex

Öffentliches TypeScript-Monorepo (Web, API, Kernlogik, Datenbank) mit ausgebautem Quality Gating: <https://github.com/PflanzenDex/PflanzenDex>

| Was wir übernehmen | Wo es dort steht |
|---|---|
| Leitsatz: Eine Regel, die nur in einem Dokument steht, ist ein Wunsch. Eine Regel, die ein Skript prüft und den Merge blockiert, ist ein Gate. | `docs/specs/product/18-architecture-and-quality-gates.md` |
| Startwerte für Komplexität, Coverage, Bundle-Budget | `app/config/gates/quality-limits.json`, Gate-Matrix QG-K1, QG-T1 |
| Eine Regeldatei für Menschen und Agenten | `AGENTS.md` |
| Gate-Schutz: Agenten ändern keine Gates, um einen roten Lauf grün zu machen | `AGENTS.md`, Abschnitt „Gates you must not weaken“ |
| Agenten-Hooks: Sperre von `--no-verify`, Erinnerung an den Gate-Lauf vor „fertig“ | `.claude/settings.json` |
| Ein Worktree pro Agentenaufgabe | `AGENTS.md`, `make worktree` |
| Claim gegen Doppelarbeit (bei uns im Ausbau) | `AGENTS.md`, `make claim` |
| Ratchet: neue Regel erst als Report mit Baseline, dann blockierend (bei uns im Ausbau) | Story US-QG-06 |

## Weitere Referenzprojekte

Zwei nicht öffentliche Projekte (React/Flask, Angular/Spring Boot) bestätigen dieselben Muster: Coverage-Schwellen, Lighthouse erst als Report, dann als Gate, Architekturtests für Schichten, Baselines für Duplikate. Ihre Datenbank- und API-Gates übernehmen wir nicht, weil das Spiel kein Backend hat.

## Kernaussagen

1. Übernommen wird eine **Auswahl**: was ein Browser-Spiel ohne Backend braucht und ab Sprint 1 prüfbar ist ([Anforderungen](voranalyse/03-anforderungen.md)).
2. Der wichtigste Teil sind Agentenregeln und Gate-Schutz (EP-11 bis EP-15). Ohne sie ändern Agenten Gates, um Läufe grün zu machen.
3. Neue Regeln starten als Report und werden später blockierend. Die Baseline darf nur schrumpfen.
