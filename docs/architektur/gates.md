# Doku-Gates

Prüfen Katalog, Doku und Backlog. Reines Node ohne Pakete, die Skripte liegen in [`tools/check/docs/`](../../tools/check/docs/). Das Einhängen in `make ci` übernimmt EP-01. Die Tabelle zeigt nur diese Gates. Architektur ergänzt weitere.

| ID | Gate | Skript | Regel bei Fund | Netz nötig |
|---|---|---|---|---|
| EP-17 | Links und Anker | `check-links.mjs` | `docs.link_broken` | nein |
| EP-18 | ID doppelt definiert | `check-ids.mjs` | `docs.id_duplicate` | nein |
| EP-19 | ID-Verweis ins Leere | `check-ids.mjs` | `docs.id_undefined`, `docs.id_baseline_stale` | nein |
| EP-20 | Zusage-Zahlen | `check-counts.mjs` | `docs.count_mismatch` | nein |
| EP-21 | Katalog und Issues | `check-backlog.mjs` | `docs.backlog_missing`, `_duplicate`, `_drift`, `_orphan`, `_unavailable` | ja, `gh` |
| EP-22 | Markdown-Größe | `check-doc-size.mjs` | `docs.file_too_long` | nein |
| EP-23 | Repo-Root | `check-root.mjs` | `docs.root_unexpected` | nein |

## Aufruf

```sh
node tools/check/docs/run-all.mjs            # alle Gates, Abbruch beim ersten Fund
node tools/check/docs/run-all.mjs --offline  # ohne EP-21
node --test "tools/check/docs/*.test.mjs"    # Tests der Gates
```

Ein Fund steht als `<regel> <datei>:<zeile> <meldung>` auf stderr, Exit-Code 1.

## Konfiguration (Gate-Dateien, Freigabe durch Architekten, EP-11)

| Datei | Inhalt |
|---|---|
| `counts.config.json` | Fundstellen der Zusage-Zahlen. Verschwindet eine Fundstelle, schlägt EP-20 an. |
| `ids.baseline.json` | Vorläufige IDs aus den Vorschlägen der Architektur, die der Katalog noch nicht kennt (EP-19). Darf nur schrumpfen: Eine inzwischen definierte oder nirgends mehr verwiesene ID muss raus. |
| `limits.json` | Zeilengrenze für Markdown (200, wird nur gesenkt) |
| `root-allowlist.json` | Erlaubte Einträge im Root, `*` als Platzhalter |

## Was die Gates ausnehmen

- Nur versionierte Dateien (`git ls-files`).
- IDs: nur Projekt-IDs nach dem Schema `FA-(E|G|DEV)-nn`, `NF-(A|V|E|W)-nn`, `EP-nn`. Die Original-IDs von Creative und Architektur (`FA-01`, `E-01`) sind fremd.
- Zeilen mit „gestrichen“ zählen in EP-20 nicht.
- EP-21 überspringt Issues mit Label `prozess` und Issues ohne ID im Titel.

## GitHub-Ruleset

Schützt `main` auf GitHub. Die Datei [`.github/rulesets/main.json`](../../.github/rulesets/main.json) ist die Quelle, im Format der REST-API. Ausnahmen gibt es keine, auch nicht für Admins. Änderungen geben nur Architekten frei (EP-11). EP-02 und EP-11 ergänzen später dasselbe Ruleset.

| ID | Regel im Ruleset | Wirkung |
|---|---|---|
| EP-03 | `pull_request` | Merge nur per PR mit 1 Freigabe einer anderen Person. Neue Commits machen die Freigabe ungültig, den letzten Push gibt jemand anderes frei. |
| EP-04 | `non_fast_forward` | Force-Push auf `main` wird abgewiesen. |

Einspielen kann nur ein Admin des Repos:

```sh
gh api --method POST repos/MaxNize/PointAndClickAdventure/rulesets --input .github/rulesets/main.json   # anlegen
gh api repos/MaxNize/PointAndClickAdventure/rulesets --jq '.[] | select(.name=="main") | .id'          # ID
gh api --method PUT repos/MaxNize/PointAndClickAdventure/rulesets/<id> --input .github/rulesets/main.json  # aktualisieren
gh api repos/MaxNize/PointAndClickAdventure/rules/branches/main                                        # prüfen, mit Schreibrecht
```

Notfall: Ein Admin setzt `enforcement` vorübergehend auf `disabled` und danach wieder auf `active`. `node --test tools/repo/ruleset.test.mjs` prüft nur die Datei.

## Offen

- markdownlint kommt, sobald das Projektgerüst (npm) steht.
- Ein Skript, das die Zusage-Zahlen automatisch schreibt, ist nicht zugesagt.
