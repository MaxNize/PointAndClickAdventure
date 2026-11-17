# AGENTS.md

Regeln für KI-Agenten (Claude Code, Codex, Copilot, …) in diesem Repo. Menschen folgen denselben Regeln.

**Stand:** Voranalyse, noch kein Code. Die Befehle unten (`make ci`, `make worktree`) entstehen mit dem ersten Code. Bis dahin gelten die Regeln sinngemäß.

## Bevor du anfängst

1. Lies [docs/README.md](docs/README.md). Die Anforderungen stehen in [docs/voranalyse/03-anforderungen.md](docs/voranalyse/03-anforderungen.md).
2. Jede Aufgabe gehört zu einer Story mit ID. Ohne Story kein Code: Schlag zuerst die Story vor (EP-08).
3. Arbeite in einem eigenen Git-Worktree mit eigenem Branch, nie im Hauptverzeichnis (EP-14).

## Während der Arbeit

- **Architektur:** Lies [docs/architektur/engine-konzept.md](docs/architektur/engine-konzept.md) vor jeder Engine-Änderung.
- **Inhalte nur als SVG und JSON:** Räume, Figuren, Gegenstände und Animationen kommen ohne Codeänderung ins Spiel (NF-W-01). Musst du für neuen Inhalt `.ts`/`.tsx` ändern, fehlt eine Engine-Funktion: Schlag sie als Story vor.
- **Spiellogik ohne Browser:** `src/engine/core` importiert weder React noch GSAP und nutzt keine Browser-Globals (NF-W-02). React stellt nur dar und meldet Ereignisse über den Event-Bus.
- **Tests aus Akzeptanzkriterien:** Jeder Test trägt die Story-ID im Namen (EP-07).
- **Fehler mit Code:** Fehler tragen einen stabilen Code `<bereich>.<grund>`, z. B. `state.unknown`.
- **Neue Anforderungen** erfüllen die [Qualitätskriterien](docs/vorgaben-modul.md#qualitätskriterien): „Das System muss …“, eine Anforderung pro Zeile, messbar.
- **Sprache:** Doku, UI-Texte und Commits auf Deutsch. Bezeichner im Code auf Englisch.

## Gates, die du nicht abschwächst

Gate-Dateien legen fest, was „fertig“ heißt: CI-Workflows, Git-Hooks, Lint- und Test-Konfiguration, Schwellenwerte, `CODEOWNERS`, `AGENTS.md`. Änderungen daran gibt nur ein Architekt frei (EP-11).

- Ändere nie ein Gate, um einen roten Lauf grün zu machen. Ist eine Regel falsch, sag es und ändere sie in einem eigenen PR mit Begründung.
- Verboten: `--no-verify` (EP-12), Force-Push (EP-04), direkter Push oder Merge auf `main` (EP-02).

## Bevor du „fertig“ sagst

1. Führe `make ci` nach deiner letzten Änderung aus. Berichte das Ergebnis ehrlich: Befehl, Exit-Code, bei Fehlern die Ausgabe. Nie „sollte funktionieren“ (EP-15).
2. Committe nur, wenn du darum gebeten wirst. Format: Conventional Commits (EP-06).
3. Öffne den PR mit der Vorlage, inklusive Abschnitt „KI-Beteiligung“. Wer dich gestartet hat, gilt als Autor. Freigeben muss eine andere Person (EP-03).
