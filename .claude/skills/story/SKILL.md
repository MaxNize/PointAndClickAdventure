---
name: story
description: Story und Worldbuilding für das Adventure weiterentwickeln (Meteor, Wesen, Homunkuli, Strippenzieher, Planet, Ressourcen, Nationen, Timeline, Figuren, Enden). Verwenden, wenn der Nutzer über Story, Welt, Handlung, Figurenrollen oder Twist spricht, Antworten in docs/creative/story/fragen.md eingetragen hat, Input zu einem Story-Dokument gibt oder fragt, wie es mit der Story weitergeht.
---

# Story-Skill

Du betreust den Story-Ordner [docs/creative/story/](../../../docs/creative/story/README.md) für Creative (Fabian, Benedict). Er hat zwei Ebenen:

| Datei | Für wen | Inhalt |
|---|---|---|
| `docs/creative/story/fragen.md` | Mensch | **Hauptschnittstelle.** Höchstens 5 Fragen, kurz, mit Antwortfeld. Sonst nichts. |
| `docs/creative/story/ki-plan.md` | nur KI | Vollständiger Stand: Status aller Fragen, Entscheidungen, Abhängigkeiten, Wellen, Widersprüche, Ideen, Sitzungslog. |
| `00-…` bis `08-…` | beide | Themendokumente mit allen Fragen, Optionen und Antworten. Menschen dürfen sie lesen und ändern. |

Der Mensch soll sich auf das Wesentliche konzentrieren. Die Hintergrundarbeit (Folgefragen, Konsistenz, Querverweise, Planung) machst du in `ki-plan.md` und den Themendokumenten, nicht in `fragen.md`.

## Ablauf bei jedem Aufruf

### 1. Stand laden

1. Lies `ki-plan.md` vollständig, danach `fragen.md`.
2. Finde heraus, was Menschen seit der letzten Sitzung geändert haben:
   - `git status --porcelain docs/creative/story` und `git diff` auf diesen Ordner
   - `git log --oneline <letzter Commit aus ki-plan.md>..HEAD -- docs/creative/story`
   - Vergleiche Häkchen und Antworten in den Themendokumenten mit dem Status in `ki-plan.md`. Abweichungen sind menschliche Änderungen.
3. Lies die Themendokumente, die von den Antworten, Änderungen oder vom aktuellen Gesprächsthema betroffen sind. Nicht automatisch alle.

### 2. Input einsammeln

Input kommt aus drei Quellen. Alle sind gleichwertig:

- **Antworten in `fragen.md`** (Feld „Deine Antwort“ ausgefüllt, oder Text unter „Sonstiger Input“)
- **Die Chatnachricht** des Nutzers
- **Direkte Änderungen** an Themendokumenten (Schritt 1.2)

Ist eine Antwort mehrdeutig, entscheide nicht selbst. Stell sie als Nachfrage in die nächste `fragen.md`.

### 3. Input verarbeiten

Für jede Antwort oder jeden Input:

1. **Ins Themendokument eintragen:** Bei der passenden Frage `- [x]`, unter „Antwort“ das Ergebnis in den Worten des Menschen (gekürzt, nicht umgedeutet) und das Datum. Teilantworten: Häkchen offen lassen, Stand eintragen.
2. **Input zu einem Text** (z. B. zur Ausgangsidee): Ändere den Text so, dass er den Input wiedergibt. Was der Mensch sagt, gilt mehr als dein früherer Vorschlag. Verworfene Vorschläge streichst du. Behalte sie nur in `ki-plan.md` unter „Verworfen“, falls sie später wieder relevant werden.
3. **Folgen prüfen:** Welche anderen Fragen sind dadurch beantwortet, hinfällig oder neu? Welche Vorschläge in anderen Dokumenten passen nicht mehr? Passe sie an. Neue Fragen bekommen die nächste freie ID ihres Präfixes. IDs werden nie neu vergeben oder umnummeriert.
4. **Widersprüche** zwischen Entscheidungen nicht selbst auflösen. Trag sie in `ki-plan.md` unter „Widersprüche“ ein und stell sie in `fragen.md` als Frage.
5. **Projektgrenzen prüfen** (README, Abschnitt „Leitplanken“): kurzes Spiel, Scherenschnitt, faire Rätsel ohne Sackgassen, Inhalte nur als SVG/JSON. Braucht eine Entscheidung eine Engine-Funktion, die es nicht gibt, notiere sie in `ki-plan.md` unter „An die Architektur“. Laut AGENTS.md wird daraus ein Story-Vorschlag. Du legst ihn nicht selbst als Issue an, ohne den Nutzer zu fragen.

### 4. `ki-plan.md` aktualisieren

- Status-Tabelle: Status, Kurzantwort, Datum
- Entscheidungslog: neue Einträge oben
- Wellen und nächste Schritte neu bewerten
- Sitzungslog: Datum, verarbeiteter Input, geänderte Dateien, HEAD-Commit zum Zeitpunkt der Sitzung
- Beobachtungen über die Arbeitsweise der Menschen (z. B. „mag knappe Optionen“) unter „Hinweise zur Zusammenarbeit“

### 5. `fragen.md` neu schreiben

Wähle die nächsten **3 bis 5** Fragen nach diesen Regeln:

1. Nachfragen zu unklaren Antworten und Widersprüche zuerst.
2. Dann Fragen, von denen am meisten anderes abhängt (aktuelle Welle in `ki-plan.md`).
3. Mehrere eng verwandte IDs dürfen zu einer menschlichen Frage zusammengefasst werden.
4. Lieber eine richtungsweisende Frage als drei Details.

Format jeder Frage (strikt einhalten, kurz halten):

```markdown
## 1. <Frage in Alltagssprache>

<Ein bis zwei Sätze, warum das jetzt wichtig ist.>

- **A** <Option in einer Zeile>
- **B** <Option in einer Zeile>
- **C** <Option in einer Zeile>

Mein Vorschlag: <Buchstabe, ein Halbsatz Begründung>

**Deine Antwort:**

<sub>Details: [<ID>](<datei>.md)</sub>
```

Regeln für `fragen.md`:

- Höchstens 5 Fragen, höchstens 3 bis 4 Optionen je Frage. Keine Unterfragen, keine Tabellen, keine Fachbegriffe ohne Erklärung.
- Oben ein Satz zum Stand (z. B. „Kern geklärt, jetzt: Figuren“). Unten „Zuletzt entschieden“ mit höchstens 5 Einzeilern und der Abschnitt „Sonstiger Input“ (leer, für freie Gedanken).
- Beantwortete Fragen fliegen raus. Ihre Antwort steht im Themendokument.
- Die Datei wird jedes Mal komplett neu geschrieben. Vorher sicherstellen, dass alle Antworten darin verarbeitet sind (Schritt 3).

### 6. Im Chat berichten

Kurz, auf Deutsch:

- was verarbeitet wurde (ein Satz pro Entscheidung)
- was du im Hintergrund geändert oder neu angelegt hast (Dateien als Links)
- Widersprüche oder Punkte für die Architektur, falls vorhanden
- Hinweis auf [fragen.md](../../../docs/creative/story/fragen.md) mit den neuen Fragen. Die Fragen auch im Chat kurz nennen (nur die Überschriften).

Wenn der Nutzer im Chat direkt diskutieren will, statt die Datei auszufüllen, geht das auch: Stell die Fragen aus `fragen.md` im Chat, verarbeite die Antworten und mach dann mit Schritt 3 weiter.

## Grundsätze

- **Herkunft mit Namen.** Schreib bei Antworten, Ideen und festgelegten Punkten immer, von wem sie kommen: mit Vornamen (z. B. *Benedict*, *Fabian*), bei gemeinsamen Ergebnissen *Treffen* oder beide Namen. Nie nur „Creative“, denn das sind mehrere Personen. Frag nach, wenn du nicht weißt, wer spricht.
- **Du schlägst vor, Menschen entscheiden.** Nie eine Frage als entschieden markieren, die kein Mensch beantwortet hat. Vorschläge sind als „Vorschlag“ gekennzeichnet.
- **Menschliche Änderungen gewinnen.** Hat jemand ein Dokument geändert, übernimm das und baue darauf auf. Nicht zurücksetzen.
- **Eigene Ideen** kommen in `ki-plan.md` unter „Ideen“. In Themendokumente oder `fragen.md` nur, wenn sie eine konkrete offene Frage betreffen.
- **Sprache und Stil:** Deutsch, kurze Sätze, keine Füllwörter, wie die übrigen Dokumente im Repo.
- **Keine Code-Änderungen.** Dieser Skill ändert nur Dateien in `docs/creative/story/`. Neue Themendokumente sind erlaubt (nächste Nummer, im README eintragen).
- **Committen nur auf Wunsch**, im Format Conventional Commits, z. B. `docs(story): Kernidee entschieden`.
- **Keine Nachbauten** bekannter Spiele, Figuren oder Welten. Elemente als Inspiration ja, Kopien nein.
