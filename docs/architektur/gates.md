# Gates

## Gate-Lauf (EP-01)

`make ci` führt alle Prüfungen der Reihe nach aus, lokal und in der CI (Job `ci-status`) gleich. Der erste Fehler bricht ab. Die Schrittliste steht in [`tools/ci/run-ci.mjs`](../../tools/ci/run-ci.mjs). Ein neues Gate kommt dort als Eintrag dazu, nicht als eigener Schritt im Workflow.

| Schritt | Prüfung | Regel bei Fehler |
|---|---|---|
| 1 | `git config core.hooksPath` ist `.githooks` (EP-24), sonst `make setup` | `ci.hooks_missing` |
| 2 | jede versionierte `*.test.mjs` einzeln mit `node --test` | `ci.test_failed` |
| 3 | Doku-Gates EP-17 bis EP-23 über `run-all.mjs` | `ci.step_failed` |
| 4 | E2E-Tests im Browser (Playwright, Chromium) über `playwright.config.ts`, Testinhalte aus `e2e/fixtures/content/` | `ci.e2e_failed` |

Ein Fehler steht als `<regel> <datei> <meldung>` auf stderr, darüber die Ausgabe der Prüfung selbst (z. B. `docs.link_broken <datei>:<zeile>` oder der rote Test). Exit-Code ungleich 0.

**Voraussetzungen:** GNU Make (Windows: `scoop install make`), Node ≥ 22.12 (`.nvmrc`), `gh` angemeldet (für EP-21), einmal pro Klon `make setup`. Es setzt die Hooks und installiert die Abhängigkeiten mit `npm ci`. Ohne `node_modules` schlägt der Test des Projektgerüsts fehl (EP-16).

## Doku-Gates

Prüfen Katalog, Doku und Backlog. Reines Node ohne Pakete, die Skripte liegen in [`tools/check/docs/`](../../tools/check/docs/). `make ci` startet sie (Schritt 3).

| ID | Gate | Skript | Regel bei Fund | Netz nötig |
|---|---|---|---|---|
| EP-17 | Links und Anker | `check-links.mjs` | `docs.link_broken` | nein |
| EP-18 | ID doppelt definiert | `check-ids.mjs` | `docs.id_duplicate` | nein |
| EP-19 | ID-Verweis ins Leere | `check-ids.mjs` | `docs.id_undefined`, `docs.id_baseline_stale` | nein |
| EP-20 | Zusage-Zahlen | `check-counts.mjs` | `docs.count_mismatch` | nein |
| EP-21 | Katalog und Issues | `check-backlog.mjs` | `docs.backlog_missing`, `_duplicate`, `_drift`, `_orphan`, `_unavailable` | ja, `gh` |
| EP-22 | Markdown-Größe | `check-doc-size.mjs` | `docs.file_too_long` | nein |
| EP-23 | Repo-Root | `check-root.mjs` | `docs.root_unexpected` | nein |

### Aufruf einzeln

```sh
node tools/check/docs/run-all.mjs            # alle Doku-Gates, Abbruch beim ersten Fund
node tools/check/docs/run-all.mjs --offline  # ohne EP-21
node --test "tools/check/docs/*.test.mjs"    # Tests der Gates
```

Ein Fund steht als `<regel> <datei>:<zeile> <meldung>` auf stderr, Exit-Code 1.

### Konfiguration (Gate-Dateien, Freigabe durch Architekten, EP-11)

| Datei | Inhalt |
|---|---|
| `counts.config.json` | Fundstellen der Zusage-Zahlen. Verschwindet eine Fundstelle, schlägt EP-20 an. |
| `ids.baseline.json` | Vorläufige IDs aus den Vorschlägen der Architektur, die der Katalog noch nicht kennt (EP-19). Darf nur schrumpfen: Eine inzwischen definierte oder nirgends mehr verwiesene ID muss raus. |
| `limits.json` | Zeilengrenze für Markdown (200, wird nur gesenkt) |
| `root-allowlist.json` | Erlaubte Einträge im Root, `*` als Platzhalter |

### Was die Doku-Gates ausnehmen

- Nur versionierte Dateien (`git ls-files`).
- IDs: nur Projekt-IDs nach dem Schema `FA-(E|G|DEV)-nn`, `NF-(A|V|E|W)-nn`, `EP-nn`. Die Original-IDs von Creative und Architektur (`FA-01`, `E-01`) sind fremd.
- Zeilen mit „gestrichen“ zählen in EP-20 nicht.
- EP-21 überspringt Issues mit Label `prozess` und Issues ohne ID im Titel.

### Offen

- markdownlint kommt, sobald das Projektgerüst (npm) steht.
- Ein Skript, das die Zusage-Zahlen automatisch schreibt, ist nicht zugesagt.
