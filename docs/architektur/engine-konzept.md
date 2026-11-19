# Engine-Konzept

Vorgabe der Architektur (PR-03), eingegangen 2026-11-17, ausgebaut 2026-11-19. Die Anforderungen daraus stehen mit neuen IDs in [Anforderungen](../voranalyse/03-anforderungen.md). Die Zuordnung steht unten.

Das Format der Inhaltsdateien regelt der [Asset-Vertrag](asset-vertrag/README.md). Wie Creative daraus ein Spiel baut, beschreibt der [Autoren-Workflow](autoren-workflow.md). Die Reihenfolge der Umsetzung steht im [Umsetzungsplan](umsetzungsplan.md).

Anforderungs-IDs, die noch nicht im Katalog stehen (z. B. FA-E-06, FA-E-09, FA-DEV-10), sind vorläufig. Sie stehen in den [Anforderungsvorschlägen](anforderungs-vorschlaege.md) und gelten erst nach Entscheidung des PO.

## Überblick

Das Spiel ist eine Webanwendung mit React, TypeScript und Vite. Jeder Raum wird als einzelnes `<svg>` gerendert (viewBox 1920×1080, 16:9 skalierend). Eine JSON-Raumdefinition beschreibt den Raum vollständig und wird mit Zod validiert. Sie gehört zu genau einer Raum-SVG mit benannten Ebenen-Gruppen und enthält:

- das Polygon der begehbaren Fläche,
- die Tiefenskalierung,
- die Ausgänge,
- die Hotspot-Aktionen,
- die platzierten Figuren und Gegenstände.

| Baustein | Umsetzung |
|---|---|
| Hotspots | SVG-Elemente mit ID-Präfix `hotspot-` in der Gruppe `hotspots` |
| Bewegung | A*-Wegsuche auf dem Sichtbarkeitsgraphen der begehbaren Fläche |
| 2,5D-Effekt | Skalierung nach y-Position, Zeichenreihenfolge nach Basislinie |
| Figuren | Eine SVG je Figur mit drei Ansichten und benannten Teilen (`data-part`), animiert mit GSAP |
| Spiellogik | reines TypeScript in `src/engine/core`, besitzt Zustand und Zeit |
| Darstellung | React stellt nur dar. Eingaben gehen als Befehle an den Kern, Ereignisse kommen über einen typisierten Event-Bus zurück. |
| Erweiterung | Neue Räume, Figuren, Gegenstände, Animationen, Dialoge und Zwischensequenzen kommen ausschließlich über SVG- und JSON-Dateien unter `content/` ins Spiel, ohne Codeänderung. |

## Schichten

| Schicht | Ort | Aufgabe | Darf nicht |
|---|---|---|---|
| Kern | `src/engine/core` | Zustand, Regeln, Befehle, Zeit, Wegsuche, Tiefe, Zeichenreihenfolge, Dialog- und Sequenz-Ablauf, Zod-Schemas, Spielstand (de)serialisieren | `react`, `react-dom`, `gsap`, Browser-Globals importieren oder nutzen (NF-W-02) |
| Ports | Interfaces im Kern | `ContentSource` liefert Inhalte, `SaveStore` speichert Spielstände, `Clock` liefert Zeit | – |
| Browser-Adapter | `src/engine/adapters` | `import.meta.glob` über `content/**` (JSON, SVG als `?raw`), `localStorage`, `requestAnimationFrame` | Spiellogik enthalten |
| Darstellung | `src/engine/render` | SVG einbetten, Hit-Test über das DOM, Kontextmenü, Inventar, Rezeptbuch, Textblasen, Dialogauswahl, GSAP für Teil-Animationen | Zustand ändern, außer über Befehle |
| Entwicklungsmodus | `src/engine/dev` | Testzustände, Overlays, Werkzeuge aus dem [Autoren-Workflow](autoren-workflow.md) | im Produktions-Build enthalten sein (FA-DEV-06) |
| Werkzeuge | `tools/` (Node) | Content-Validator, Gerüst-Generator, Inhaltsgraph, Lösungsweg-Lauf | – |

Der Kern läuft in Node und im Browser gleich. Der Content-Validator und der Lösungsweg-Test (NF-V-02) nutzen dieselben Zod-Schemas und denselben Kern wie das Spiel.

**Inhalte finden:** Der Browser-Adapter sammelt alle Dateien unter `content/` per `import.meta.glob`. Ein neuer Raum braucht deshalb keinen Eintrag im Code (NF-W-01). Der Node-Adapter liest dieselben Dateien vom Dateisystem.

## Befehle und Ereignisse

Die Darstellung übersetzt Klicks in **semantische Befehle**. Der Kern kennt keine Bildschirmkoordinaten außer dem Zielpunkt beim Laufen.

| Befehl | Bedeutung |
|---|---|
| `walkTo(point)` | Spielfigur läuft zum Punkt (viewBox-Einheiten) |
| `interact(target, verb)` | Verb auf ein Interaktionsziel anwenden (Hotspot, platzierte Figur, platzierter Gegenstand) |
| `exit(target)` | Ausgang benutzen: hinlaufen, dann Raumwechsel |
| `useItem(item, target)` | Inventar-Gegenstand auf ein Interaktionsziel anwenden (bei Figuren: geben) |
| `combine(a, b)` | Zwei Inventar-Gegenstände kombinieren |
| `craft(recipe)` | Alchemiegegenstand aus einem freigeschalteten Rezept herstellen (FA-G-01) |
| `choose(option)` | Dialogoption wählen |
| `skip()` | Sprechtext oder Zwischensequenz überspringen |
| `save()` / `load(state)` | Spielstand speichern oder laden |

Der Kern meldet Änderungen als Ereignisse über den Event-Bus, z. B. `roomEntered`, `actorMoved`, `say`, `inventoryChanged`, `dialogOpened`, `cutsceneStarted`, `gameEnded`, `error`. Jedes Ereignis hat einen Typ im Kern.

Der [Lösungsweg](asset-vertrag/ablauf.md#lösungsweg) besteht aus denselben Befehlen. Deshalb kann ihn ein Test ohne Browser abspielen (NF-V-02).

## Zeitmodell

Der Kern besitzt die Zeit. `tick(dtMs)` bewegt Figuren entlang ihres Pfads, zählt Textdauern herunter und schaltet Schritte von Zwischensequenzen weiter. Effekte wie `walkTo` oder `say` sind fertig, wenn der Kern es nach seiner eigenen Zeit entscheidet, nicht wenn die Darstellung es meldet.

- Die Darstellung ruft `tick` pro Frame auf und liest danach die Positionen. Sie setzt Transforms direkt über Refs, ohne React-Re-Render pro Frame (NF-E-02).
- GSAP animiert nur die Teile einer Figur (`idle`, `walk`, `talk`). Die Position der Figur im Raum kommt immer aus dem Kern.
- Tests ticken in großen Schritten. Der Ablauf ist deterministisch.

## Eingabe

| Eingabe | Ziel | Wirkung |
|---|---|---|
| Linksklick | begehbare Fläche | Spielfigur läuft zum Punkt |
| Linksklick | außerhalb der begehbaren Fläche | Spielfigur läuft zum nächstgelegenen Punkt der Fläche |
| Linksklick | Ausgang-Hotspot | `exit`: hinlaufen zum `walkTo`-Punkt, dann Raumwechsel |
| Linksklick | Hotspot ohne Ausgang, Figur, Gegenstand | Spielfigur läuft zum `walkTo`-Punkt des Ziels |
| Rechtsklick | Hotspot, Figur, Gegenstand im Raum | Kontextmenü |
| Rechtsklick | Gegenstand im Inventar | Kontextmenü: Ansehen, Kombinieren mit …, Benutzen mit … |

**Kontextmenü:** „Ansehen“ steht immer im Menü. Dazu kommen die Verben, die das Ziel im JSON definiert. „Gegenstand benutzen …“ (bei Figuren „Geben …“) steht immer im Menü, sobald das Inventar nicht leer ist. So verrät das Menü keine Lösung (P-02). Gibt es für eine Kombination keine Aktion, erscheint der Standardtext aus `game.json`. Vor jeder Aktion läuft die Spielfigur zum `walkTo`-Punkt des Ziels und dreht sich in die angegebene Richtung.

Während eines Dialogs oder einer Zwischensequenz nimmt der Kern nur `choose` und `skip` an. Andere Befehle verwirft er.

## Raum, Koordinaten und Tiefe

**Koordinaten:** Alle Raumkoordinaten sind viewBox-Einheiten des Raums (0–1920 × 0–1080). Auch Toleranzen in Akzeptanzkriterien (z. B. FA-E-07) meinen diese Einheiten. Figur- und Gegenstands-SVGs haben eigene Koordinaten, die die Engine über den Anker umrechnet.

**Tiefe:** Die Skalierung einer Figur folgt linear ihrer y-Position zwischen `depth.far` und `depth.near`. Außerhalb dieses Bereichs wird sie geklemmt. Die Größe bei Skalierung 1 legt `height` in der Figurdefinition fest.

**Wegsuche:** A* auf dem Sichtbarkeitsgraphen aus Start, Ziel und den konkaven Ecken der begehbaren Fläche (Außenrand plus Löcher). Ein Weg verlässt die Fläche nie. Liegt das Ziel außerhalb, wird es vorher auf den nächstgelegenen Randpunkt verschoben.

**Ansicht:** Ist die horizontale Bewegung größer als die vertikale, zeigt die Figur die Seitenansicht, nach links gespiegelt. Sonst zeigt sie die Vorder- oder Rückansicht. Die Blickrichtung (`left`, `right`, `front`, `back`) steht im Zustand.

## Zeichenreihenfolge

DOM-Reihenfolge im Raum-`<svg>`:

1. `layer-background`
2. `hotspots` (unsichtbar, von der Engine mit `pointer-events: all` klickbar gemacht)
3. Akteure, sortiert nach Basislinie, aufsteigend: Figuren (Fußpunkt y), platzierte Gegenstände (Platzierung y) und Mittelebenen `layer-mid-*` (Basislinie aus `room.json`, `pointer-events: none`)
4. `layer-foreground` (`pointer-events: none`)

Figuren und Gegenstände liegen damit über den Hotspots und fangen deren Klicks ab. Mittelebenen und Vordergrund blockieren keine Klicks.

## SVG einbetten und ID-Namensraum

Raum, Figuren und Gegenstände liegen inline im selben DOM.

- Das **Raum-SVG** bleibt unverändert. Es ist immer nur ein Raum im DOM, und die `hotspot-`-IDs bleiben für FA-E-05, FA-DEV-05 und NF-V-01 direkt zählbar.
- **Figuren und Gegenstände** präfixt die Engine beim Einbetten: Jede ID wird zu `<instanz>--<id>`, Verweise in `url(#…)` und `href` werden umgeschrieben.
- Der Vertrag verbietet `<style>`-Elemente, weil CSS-Klassen über Dateien hinweg kollidieren würden.

## Fehlerbehandlung

- Der Content-Validator prüft im Gate-Lauf alle Regeln des [Asset-Vertrags](asset-vertrag/README.md) (NF-V-01).
- Zur Laufzeit prüft der Kern jede geladene Definition erneut mit Zod. Bei einem Verstoß zeigt die Engine den Fehlerraum mit Fehlercode und läuft weiter (NF-V-04).
- Fehlercodes folgen dem Muster `<bereich>.<grund>`. Die Liste steht im [Asset-Vertrag](asset-vertrag/fehlercodes.md).

## Modulschnitt

NF-W-04 (Komplexität ≤ 10) und NF-W-05 (≤ 200 Zeilen) bestimmen den Schnitt:

- Effekte und Bedingungen laufen über eine Registry mit einem Handler je Typ, nicht über ein großes `switch`.
- Zod-Schemas liegen je Asset-Typ in eigenen Dateien.
- Wegsuche, Polygon-Geometrie und Tiefe sind getrennte Module.

## Inhalte einbinden

Die Formate im Detail regelt der [Asset-Vertrag](asset-vertrag/README.md).

| Inhalt | Dateien | Verknüpfung |
|---|---|---|
| Spiel | `content/game.json` (Startraum, Spielfigur, Standardtexte) | – |
| Raum | `room.svg` mit Ebenen-Gruppen und Hotspots, `room.json` (begehbare Fläche, Tiefe, Ausgänge, Hotspot-Aktionen, Basislinien, platzierte Figuren und Gegenstände) | – |
| Figur | `character.svg` mit den Ansichten `view-side`, `view-front`, `view-back`, Teilen per `data-part` und Anker, `character.json` (Name, Größe, Geschwindigkeit, Drehpunkte), `animations.json` | Raumdefinition platziert die Figur per ID |
| Gegenstand | Ordner je Gegenstand: `item.json` (Name, Beschreibung, Typ `alchemie` oder `quest`, Höchstmenge, Kombinationen), `world.svg`, `icon.svg` | Raumdefinition platziert per ID. Beim Aufnehmen setzt die Engine das Flag `item.<raum-id>.<gegenstand-id>.taken` und meldet `inventoryChanged`. Das Inventar führt Mengen und lehnt Questgegenstände über der Höchstmenge ab (FA-G-07). |
| Rezept | `content/recipes/<id>.json` (erzeugter Alchemiegegenstand, freischaltendes Flag, Zutaten) | Rezeptbuch zeigt freigeschaltete Rezepte, `craft` legt den Gegenstand ins Inventar (FA-G-01, FA-G-03) |
| Animation | `animations.json` je Figur, mindestens `idle`, `walk`, `talk`. Keyframes wenden Rotation, Verschiebung, Skalierung und Deckkraft auf benannte Teile an. | GSAP spielt sie ab |
| Dialog | `content/dialogs/<id>.json` | Effekt `startDialog` |
| Zwischensequenz | `content/cutscenes/<id>.json` | Effekt `startCutscene` |
| Lösungsweg | `content/walkthrough.json` | NF-V-02, FA-DEV-02 |

## Zuordnung der Architektur-IDs

| Architektur | Projekt-ID | Anmerkung |
|---|---|---|
| E-01 | FA-E-01 | übernommen |
| E-02 | FA-E-02 | neu 2026-11-19, ID vorläufig |
| E-03 | FA-E-03 | neu 2026-11-19, ID vorläufig |
| E-04 | FA-E-04 | neu 2026-11-19, ID vorläufig |
| E-05 | FA-E-05 | übernommen. Änderung des Kriteriums an das Eingabemodell vorgeschlagen ([Anforderungsvorschläge](anforderungs-vorschlaege.md)) |
| E-06 | FA-E-06 | neu 2026-11-19, ID vorläufig |
| E-07 | FA-E-07 | übernommen. Einheit geklärt (viewBox-Einheiten), Änderung des Kriteriums vorgeschlagen |
| E-08 | FA-E-08 | neu 2026-11-19, ID vorläufig |
| E-09 | FA-E-09 | neu 2026-11-19, ID vorläufig |
| E-10 | FA-E-10 | übernommen |
| E-11 | FA-E-11 | neu 2026-11-19, ID vorläufig |
| E-12 | FA-E-12 | neu 2026-11-19, ID vorläufig |
| E-13 | FA-G-09 | neu 2026-11-19, entspricht „Aufnehmen“ aus Issue #78, das Vorrang hat. Keine eigene FA-E-13. |
| E-14 | FA-E-14 | neu 2026-11-19, ID vorläufig |
| E-15 | FA-E-15 | neu 2026-11-19, ID vorläufig |
| E-16 | FA-E-16 | übernommen |
| E-17 | FA-E-17 | neu 2026-11-19, ID vorläufig |
| E-18 | FA-E-18 | neu 2026-11-19, ID vorläufig |
| E-19 | FA-E-19 | neu 2026-11-19, ID vorläufig |
| E-20 | FA-E-20 | neu 2026-11-19, ID vorläufig |
| E-21 | FA-E-21 | neu 2026-11-19, ID vorläufig |
| E-22 | FA-E-22 | neu 2026-11-19, ID vorläufig |
| N-01 | NF-W-01 | ersetzt die bisherige Fassung. Eingeordnet unter Wartbarkeit statt Akzeptanz, weil es um Erweiterbarkeit geht. |
| N-04 | NF-V-04 | übernommen |
| N-06 | NF-E-02 | übernommen, manuelle Messung |
| N-07 | NF-E-03 | übernommen, Rückfrage zu den Messbedingungen |
| N-11 | NF-W-02 | zusammengeführt. „React- oder DOM-APIs“ verstößt gegen die Regel „keine und/oder-Ketten“, daher „Browser-Abhängigkeiten“ mit Liste im Akzeptanzkriterium. |

Die E-Liste der Architektur ist seit 2026-11-19 vollständig. „ID vorläufig“ heißt: Die Anforderung steht in den [Anforderungsvorschlägen](anforderungs-vorschlaege.md), nicht im Katalog. Über die Aufnahme entscheidet der PO (siehe [Offene Fragen](../offene-fragen.md)). Die N-Liste hat noch Lücken (N-02, N-03, N-05, N-08 bis N-10).

Die Gegenstandsanforderungen FA-G-01 bis FA-G-08 stammen von Creative ([Gegenstände](../creative/gegenstaende.md)) und haben keine E-Nummer. Die Engine setzt sie über das Inventar, `useItem`, `combine` und `craft` um.
