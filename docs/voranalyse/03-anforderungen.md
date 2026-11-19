# Anforderungen

Schritt 3 der Voranalyse. Herkunft jeder Anforderung: [Personas](02-personas.md) (Abdeckung), [Engine-Konzept](../architektur/engine-konzept.md) (Architektur), [Gegenstände](../creative/gegenstaende.md) (Creative) und [Quellen](../quellen.md) (Referenzprojekte).

## Grundsätze

- **Web App für den Desktop-Browser, agentic first:** Kein Smartphone, keine Responsiveness, Barrierefreiheit ist kein Ziel. Agenten schreiben Code und Inhalte. Menschen setzen Ziele, prüfen, geben frei.
- **Jede Anforderung ist ein Gate:** Ein Skript prüft das Akzeptanzkriterium. Rot blockiert den Merge.
- **Startwerte** (markiert) stammen aus Referenz-Repos oder Google-Schwellen. Sie werden nach der ersten Messung fest und danach nur verschärft.
- **Stack** laut [Engine-Konzept](../architektur/engine-konzept.md): React, TypeScript, Vite, SVG-Räume, Zod, GSAP. Prüfwerkzeuge: Vitest, Playwright, Lighthouse, ESLint, jscpd, knip.

**Begriffe:** *Spiellogik* = `src/engine/core`, reines TypeScript mit Zustand und Regeln. *Spielinhalt* = Räume, Figuren, Gegenstände, Animationen, Dialoge, Lösungsweg als SVG- und JSON-Dateien unter `content/`. *Gate-Lauf* = `make ci`, lokal und in der CI gleich. *Nutzerrolle*: Systemrollen Spieler und Entwickler, Projektrollen Team, Architekt und Agent (siehe [Stakeholder und Rollen](01-stakeholder-und-rollen.md)). In Teil 3 meint „System“ das Repository mit seiner Pipeline.

**Umfang der Zusage:** 16 NF, 19 FA (5 Engine, 8 Gegenstände, 6 Entwicklungsmodus), 22 Prozess-Gates. Die Vorgabe von mindestens 15 FA ist erfüllt.

## 1. Nicht-funktionale Anforderungen

### Akzeptanz

| ID | Bereich | Nutzerrolle | Anforderung | Akzeptanzkriterium |
|---|---|---|---|---|
| NF-A-01 | Browser | Spieler | Das System muss in jeder Browser-Engine der Playwright-Testmatrix lauffähig sein. | E2E-Suite grün in Chromium, Firefox, WebKit (Desktop-Profile). |
| NF-A-02 | Fenstergröße | Spieler | Das System muss jeden Raum ab einer Fensterbreite von 1280 px vollständig ohne Scrollen darstellen. | Playwright bei 1280 × 720 px: Raum-SVG liegt vollständig im Viewport, 0 Scrollbalken. |

### Verlässlichkeit

| ID | Bereich | Nutzerrolle | Anforderung | Akzeptanzkriterium |
|---|---|---|---|---|
| NF-V-01 | Inhalt konsistent | Spieler | Das System muss nur Spielinhalte ausliefern, deren ID-Verweise vollständig auflösbar sind. | Content-Validator: Zod-Schemas plus Verweisprüfung (Zielräume der Ausgänge, Figur-, Gegenstands- und Animations-IDs, `hotspot-`-IDs zwischen SVG und JSON, Rezepte erzeugen keine Questgegenstände): 0 Fehler. Der Validator hat eigene Tests mit fehlerhaften Dateien. |
| NF-V-02 | Lösbarkeit | Spieler | Das System muss das Spiel über den hinterlegten Lösungsweg vom Start bis zum Ende spielbar halten. | Headless-Test spielt den Lösungsweg gegen die Spiellogik ab: Endzustand erreicht. |
| NF-V-03 | Spielstand | Spieler | Das System muss einen gespeicherten Spielstand nach dem Neuladen der Seite unverändert wiederherstellen. | E2E-Test: speichern, neu laden, laden. Abweichende Zustandsfelder: 0. |
| NF-V-04 | Fehlerraum | Spieler | Das System muss bei einer ungültigen Raumdefinition weiterlaufen. | E2E-Test mit ungültiger Test-Raumdefinition: Fehlerraum wird angezeigt, 0 unbehandelte Fehler in der Konsole (Architektur N-04). |

### Effizienz

| ID | Bereich | Nutzerrolle | Anforderung | Akzeptanzkriterium |
|---|---|---|---|---|
| NF-E-01 | Ladezeit | Spieler | Das System muss den Startraum mit einem Largest Contentful Paint von höchstens 2,5 s anzeigen. | Lighthouse, Desktop-Profil, Median aus 3 Läufen: ≤ 2,5 s (Startwert). |
| NF-E-02 | Bildrate | Spieler | Das System muss im Referenzraum mindestens 60 Bilder pro Sekunde darstellen. | Median über 30 s in den Chrome DevTools auf einem Lenovo Yoga 7 2-in-1 14AKP10 bei 1920×1080 (Architektur N-06). Manuelle Messung vor jedem Release, kein CI-Gate. |
| NF-E-03 | Raumwechsel | Spieler | Das System muss einen Raumwechsel in unter 1 Sekunde abschließen. | Playwright, Chromium Desktop-Profil, Assets des Zielraums bereits geladen, keine Drosselung: Zeit vom Klick auf den Ausgang bis zur Darstellung des Zielraums, Median aus 5 Läufen < 1 s (Architektur N-07, Messbedingungen Startwert). |

### Wartbarkeit

| ID | Bereich | Nutzerrolle | Anforderung | Akzeptanzkriterium |
|---|---|---|---|---|
| NF-W-01 | Erweiterbarkeit | Team | Das System muss neue Räume ohne Änderung am TypeScript-Quellcode aufnehmen. | CI bindet einen Testraum nur aus SVG- und JSON-Dateien ein und lädt ihn: 0 geänderte `.ts`/`.tsx`-Dateien (Architektur N-01). |
| NF-W-02 | Architektur | Team | Das System muss die Spiellogik in `src/engine/core` ohne Browser-Abhängigkeiten ausführbar halten. | ESLint-Regeln für `src/engine/core` verbieten Importe von `react`, `react-dom`, `gsap` und die Globals `window`, `document`, `localStorage`, `fetch`: 0 Verstöße (Architektur N-11). |
| NF-W-03 | Testabdeckung | Team | Das System muss in der Spiellogik eine Zeilenabdeckung von mindestens 90 % erreichen. | Coverage-Lauf: ≥ 90 % (Startwert, PflanzenDex QG-T1). Schwelle wird nur angehoben. |
| NF-W-04 | Komplexität | Team | Das System muss die zyklomatische Komplexität jeder Funktion auf höchstens 10 begrenzen. | ESLint `complexity`: 0 Funktionen über 10 (Startwert, PflanzenDex). |
| NF-W-05 | Dateigröße | Team | Das System muss jede Quelldatei auf höchstens 200 Zeilen begrenzen. | ESLint `max-lines` (Tests ausgenommen): 0 Verstöße (Startwert, PflanzenDex QG-C2). |
| NF-W-06 | Duplikate | Team | Das System muss den Anteil duplizierter Quellzeilen auf höchstens 1 % begrenzen. | jscpd über `src/`: ≤ 1 % (Startwert, PflanzenDex QG-K5). Der Wert sinkt nur. |
| NF-W-07 | Abhängigkeiten | Team | Das System muss ohne ungenutzte Abhängigkeiten auskommen. | knip: 0 ungenutzte Pakete in `package.json` (PflanzenDex QG-C7). |

**Zusammenhang:** Inhalte kommen nur als SVG und JSON ins Spiel (NF-W-01). Agenten und Creative können sie ändern, ohne Code anzufassen. NF-V-01 und NF-V-02 beweisen danach in jedem Lauf, dass das Spiel konsistent und lösbar bleibt. NF-V-04 fängt zur Laufzeit ab, was trotzdem durchrutscht. Das alles läuft im Gate ohne Browserstart, weil die Spiellogik ohne Browser läuft (NF-W-02).

## 2. Funktionale Anforderungen

### 2.1 Engine

Aus dem [Engine-Konzept](../architektur/engine-konzept.md) der Architektur. Die Nummern folgen der Architektur-Liste, Lücken sind dort noch nicht geliefert.

| ID | Bereich | Nutzerrolle | Anforderung | Akzeptanzkriterium |
|---|---|---|---|---|
| FA-E-01 | Raum laden | Spieler | Das System muss Räume aus einer JSON-Raumdefinition laden. | E2E-Test: Alle Ebenen des Testraums werden angezeigt. |
| FA-E-05 | Hotspots | Spieler | Das System muss SVG-Elemente mit ID-Präfix `hotspot-` als anklickbare Hotspots registrieren. | E2E-Test: Ein Klick löst die hinterlegte Aktion aus. |
| FA-E-07 | Laufen | Spieler | Das System muss die Spielfigur nach einem Klick auf die begehbare Fläche zum Zielpunkt bewegen. | Endposition höchstens 2 px vom Klickpunkt entfernt. |
| FA-E-10 | Tiefenskalierung | Spieler | Das System muss die Spielfigur abhängig von ihrer y-Position skalieren. | Unit-Test: Abweichung vom Sollwert an oberem und unterem Rand der begehbaren Fläche höchstens 1 %. |
| FA-E-16 | Raumwechsel | Spieler | Das System muss beim Anklicken eines Ausgang-Hotspots den verknüpften Zielraum laden. | E2E-Test: Die Figur erscheint am definierten Eintrittspunkt. |

### 2.2 Gegenstände

Von Creative, Begriffe und Änderungen am Wortlaut: [Gegenstände](../creative/gegenstaende.md).

| ID | Bereich | Nutzerrolle | Anforderung | Akzeptanzkriterium |
|---|---|---|---|---|
| FA-G-01 | Herstellen | Spieler | Das System muss dem Spieler ermöglichen, mithilfe des Rezeptbuchs Alchemiegegenstände herzustellen. | Wählt der Spieler ein freigeschaltetes Rezept, erscheint der zugehörige Alchemiegegenstand im Inventar. |
| FA-G-02 | Einsetzen: Rätsel | Spieler | Das System muss dem Spieler ermöglichen, einen hergestellten Alchemiegegenstand zum Lösen eines Rätsels zu verwenden. | Wird der vorgesehene Alchemiegegenstand am vorgesehenen Hotspot eingesetzt, gilt das Rätsel als gelöst (Flag gesetzt). |
| FA-G-03 | Rezeptbuch | Spieler | Das System muss das Rezeptbuch mit jedem erreichten Meilenstein um die dafür vorgesehenen Rezepte erweitern. | Beim Erreichen eines Meilensteins erscheinen dessen Rezepte im Rezeptbuch. Rezepte früherer Meilensteine bleiben verfügbar. |
| FA-G-04 | Questgegenstände | Spieler | Das System muss jede nicht vorgesehene Kombination mit einem Questgegenstand ablehnen. | Eine ungültige Kombination wird nicht ausgeführt. Alle beteiligten Gegenstände bleiben unverändert im Inventar. |
| FA-G-05 | Questgegenstände | Spieler | Das System muss Questgegenstände aus dem Rezeptbuch ausschließen. | E2E-Test mit allen Rezepten freigeschaltet: Das Rezeptbuch zeigt 0 Questgegenstände. |
| FA-G-06 | Ressourcen | Spieler | Das System muss Ressourcen für die Herstellung von Alchemiegegenständen unbegrenzt bereitstellen. | Unit-Test: 100 Herstellungen desselben Gegenstands hintereinander gelingen. Der Ressourcenbestand ist danach unverändert. |
| FA-G-07 | Questgegenstände | Spieler | Das System muss die Anzahl jedes Questgegenstands auf die für die Quest festgelegte Menge begrenzen. | Bei erreichter Menge wird jeder weitere Erhalt abgelehnt. Inventarbestand = festgelegte Menge. |
| FA-G-08 | Einsetzen: Information | Spieler | Das System muss dem Spieler ermöglichen, einen hergestellten Alchemiegegenstand zum Freischalten einer Information zu verwenden. | Wird der vorgesehene Alchemiegegenstand am vorgesehenen Hotspot eingesetzt, wird die hinterlegte Information angezeigt. |

### 2.3 Entwicklungsmodus

Beim Testen direkt an eine Stelle des Spiels springen (Persona P-03). Testzustände entstehen aus den Checkpoints des Lösungswegs, den Creative pflegt. Ändert sich ein Raum, fällt ein veralteter Zustand im Gate auf.

| ID | Bereich | Nutzerrolle | Anforderung | Akzeptanzkriterium |
|---|---|---|---|---|
| FA-DEV-01 | Zustand laden | Entwickler | Das System muss das Spiel über den URL-Parameter `?state=<id>` in einen benannten Testzustand versetzen. | E2E-Test je Zustand: Raum, Inventar, Flags stimmen mit `content/states/<id>.json` überein. Abweichungen: 0. |
| FA-DEV-02 | Checkpoints | Entwickler | Das System muss Testzustände automatisch aus den markierten Checkpoints des Lösungswegs erzeugen. | Skript spielt den Lösungsweg ab, schreibt je Checkpoint eine Datei. Vergleich mit den eingecheckten Dateien: 0 Abweichungen. |
| FA-DEV-03 | Zustand exportieren | Entwickler | Das System muss den aktuellen Spielzustand im Entwicklungsmodus als Zustandsdatei exportieren. | Export, danach Laden über `?state=`: 0 abweichende Felder. |
| FA-DEV-04 | Unbekannte ID | Entwickler | Das System muss eine unbekannte Zustands-ID mit dem Fehlercode `state.unknown` ablehnen. | E2E-Test mit nicht vorhandener ID: Fehlercode sichtbar, Spiel bleibt im Startraum. |
| FA-DEV-05 | Hotspots anzeigen | Entwickler | Das System muss im Entwicklungsmodus die Trefferflächen aller Hotspots des Raums einblenden. | E2E-Test: Anzahl eingeblendeter Flächen = Anzahl `hotspot-`-Elemente im Raum-SVG. |
| FA-DEV-06 | Auslieferung | Spieler | Das System muss den Entwicklungsmodus in der ausgelieferten Version deaktivieren. | E2E-Test gegen den Produktions-Build: `?state=<id>` startet im Startraum. |

Exportierte Zustände (FA-DEV-03) liegen unter `content/states/manual/`. Der Content-Validator prüft sie mit. Bricht eine Inhaltsänderung einen davon, wird er gelöscht oder neu exportiert.

## 3. Entwicklungsprozess und Gates

Diese Anforderungen betreffen Repository und Pipeline, nicht das Spiel. Sie zählen weder zu FA noch zu NF. Ohne sie könnte ein Agent ein Gate abschwächen, um einen roten Lauf grün zu machen.

| ID | Bereich | Nutzerrolle | Anforderung | Akzeptanzkriterium |
|---|---|---|---|---|
| EP-01 | Gate-Lauf | Team | Das System muss alle Prüfungen über den einzigen Befehl `make ci` ausführen. | Fehlerfrei: Exit-Code 0. Erster Fehler bricht ab, nennt Regel-ID und Datei. |
| EP-02 | Merge-Schutz | Team | Das System muss Merges in `main` nur bei grünem Pflicht-Check `ci-status` zulassen. | Test-PR mit rotem Check lässt sich nicht mergen. |
| EP-03 | Review | Team | Das System muss vor jedem Merge die Freigabe einer Person verlangen, die den PR nicht verantwortet. | Ruleset verlangt 1 Approval einer anderen Person. |
| EP-04 | Force-Push | Team | Das System muss Force-Pushes auf `main` ablehnen. | Force-Push auf `main` wird vom Ruleset abgewiesen. |
| EP-05 | Lokale Prüfung | Team | Das System muss Lint-Fehler vor dem Push abfangen. | `pre-push`-Hook bricht bei Lint-Fehler ab. Laufzeit ≤ 60 s. |
| EP-06 | Commit-Format | Team | Das System muss Commit-Nachrichten nach Conventional Commits erzwingen. | `commit-msg`-Hook lehnt ungültige Nachricht ab, nennt die Regel. |
| EP-07 | Rückverfolgbarkeit | Team | Das System muss für jede fertige Story mindestens einen Test mit ihrer Story-ID im Namen nachweisen. | Prüfskript: 0 fertige Storys ohne Test. |
| EP-08 | Story-Pflicht | Team | Das System muss PRs ohne gültige Story-ID ablehnen. | CI-Job prüft die ID im PR-Titel gegen das Backlog. |
| EP-09 | Secrets | Team | Das System muss Secrets in der gesamten Git-History erkennen. | Gitleaks über die History: 0 Funde. |
| EP-10 | Schwachstellen | Team | Das System muss Abhängigkeiten auf bekannte Schwachstellen prüfen. | `npm audit`: 0 Funde „high“ oder „critical“. |
| EP-11 | Gate-Schutz | Architekt | Das System muss jede Änderung an Gate-Dateien an die Freigabe eines Architekten binden. | `CODEOWNERS` deckt CI, Hooks, Lint-Konfiguration, Schwellenwerte ab. Ohne Architekten-Approval kein Merge. |
| EP-12 | Hook-Umgehung | Agent | Das System muss Agenten das Überspringen von Git-Hooks verwehren. | Agenten-Konfiguration lehnt `--no-verify` ab. Die CI wiederholt alle Hook-Prüfungen. |
| EP-13 | Agentenregeln | Agent | Das System muss die Arbeitsregeln für Agenten in der Datei `AGENTS.md` bereitstellen. | Prüfskript bestätigt die Pflichtabschnitte: Story-Referenz, Gate-Lauf, Worktree, verbotene Befehle. |
| EP-14 | Isolation | Agent | Das System muss jede Agentenaufgabe in einem eigenen Git-Worktree starten. | `make worktree STORY=<id>` legt Worktree und Branch an. Start im Hauptverzeichnis: Exit-Code 1. |
| EP-15 | Fertig-Meldung | Agent | Das System muss eine Fertig-Meldung ohne Gate-Lauf nach der letzten Codeänderung zurückweisen. | Stop-Hook vergleicht letzte Änderung mit letztem `make ci`. Liegt die Änderung später, meldet er den fehlenden Lauf. |
| EP-17 | Doku-Links | Team | Das System muss alle relativen Links und Anker in Markdown-Dateien auflösbar halten. | `node tools/check/docs/check-links.mjs` über alle versionierten `.md`-Dateien: 0 nicht auflösbare Links oder Anker. Fehler nennt `docs.link_broken`, Datei und Zeile. |
| EP-18 | Katalog-IDs | Team | Das System muss jede ID des Anforderungskatalogs genau einmal definieren. | `node tools/check/docs/check-ids.mjs`: 0 doppelt definierte IDs in `03-anforderungen.md`. Fehler nennt `docs.id_duplicate`, Datei und Zeile. |
| EP-19 | ID-Verweise | Team | Das System muss jeden Verweis auf eine Projekt-ID auf eine im Katalog definierte ID zeigen lassen. | `node tools/check/docs/check-ids.mjs`: 0 Verweise auf nicht definierte IDs in allen versionierten `.md`-Dateien. Fehler nennt `docs.id_undefined`, Datei und Zeile. |
| EP-20 | Zusage-Zahlen | Team | Das System muss die in der Doku genannten Anzahlen von NF, FA und EP mit den Zeilen des Anforderungskatalogs in Einklang halten. | `node tools/check/docs/check-counts.mjs`: 0 Zahlen, die von der Zeilenzahl abweichen, und 0 nicht mehr gefundene Fundstellen. Fehler nennt `docs.count_mismatch`, Datei und Zeile. |
| EP-21 | Backlog-Abgleich | Team | Das System muss jede Anforderung des Katalogs durch genau ein Issue mit unverändertem Wortlaut abbilden. | `node tools/check/docs/check-backlog.mjs` gegen die GitHub-Issues: 0 Anforderungen ohne oder mit mehreren Issues, 0 Issues mit abweichender Anforderung oder abweichendem Akzeptanzkriterium. Issues mit Label `prozess` sind ausgenommen. Fehler nennt `docs.backlog_missing`, `docs.backlog_duplicate`, `docs.backlog_drift` oder `docs.backlog_orphan` und die ID. |
| EP-22 | Doku-Größe | Team | Das System muss jede Markdown-Datei auf höchstens 200 Zeilen begrenzen. | `node tools/check/docs/check-doc-size.mjs`: 0 versionierte `.md`-Dateien über 200 Zeilen (Startwert, Schwelle in `tools/check/docs/limits.json`, wird nur gesenkt). Fehler nennt `docs.file_too_long`, Datei und Zeilenzahl. |
| EP-23 | Repo-Root | Team | Das System muss das Repo-Root auf eine feste Liste von Einträgen begrenzen. | `node tools/check/docs/check-root.mjs`: 0 versionierte Einträge im Root außerhalb von `tools/check/docs/root-allowlist.json`. Fehler nennt `docs.root_unexpected` und den Eintrag. |

EP-02 bis EP-04 und EP-11 wirken über den Git-Hoster, also für jedes Agenten-Werkzeug. EP-12 und EP-15 brauchen Hooks im Agenten-Werkzeug. Fehlen sie, fängt die CI denselben Fehler später.

## 4. Nicht zugesagt

**Ausbau**, wenn die Zusage steht:

| Punkt | Inhalt | Quelle |
|---|---|---|
| Sackgassen-Suche | Zustandsraum durchsuchen, jeden Zustand ohne Weg zum Ende melden | P-02 |
| JS-Budget | Initiales JavaScript ≤ 125 kB gzip | PflanzenDex |
| Fehlercodes | Jeder Fehler mit Code `<bereich>.<grund>` im Textkatalog | PflanzenDex |
| Visuelle Regression | Screenshot-Vergleich je Raum | – |
| Claim | `make claim` lehnt bereits vergebene Story ab | PflanzenDex |
| Ratchet | Neue Regel erst als Report mit Baseline, dann blockierend | PflanzenDex |
| Automatisches Release | Versionstag nur aus grünen Commits | PflanzenDex |

**Bewusst nicht übernommen**, weil es kein Backend gibt: Mandantentrennung, Abfragen pro Request, Indizes (PflanzenDex), Migrationsprüfungen (weitere Referenzprojekte), generierter API-Client. Kommt ein Backend, werden sie neu geprüft.
