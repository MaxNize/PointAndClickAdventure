# Export der Figuren und des Lehrsaals in die Engine

Die Generatoren schreiben je Figur sechs SVGs: drei Ansichten mal zwei Stile. Die Engine erwartet je Figur **eine** `character.svg` und eine `character.json` nach dem Asset-Vertrag (`docs/architektur/asset-vertrag/figur.md` auf `main`). Dieser Ordner wandelt die Scherenschnitt-Dateien um. So ist es am 20.11. entschieden: Der Generator liefert vertragskonform, die Engine bekommt kein Import-Skript.

## Aufruf

Aus dem Repo-Root:

```
python docs/creative/temp/Charaktere/export/export_alle.py
```

Ergebnis: `content/characters/<figur-id>/character.svg` und `character.json` für alle 16 Figuren. Ein anderer Zielordner geht als Argument. Nach jeder Änderung an einem Generator: erst den Generator laufen lassen, dann den Export.

Eine neue Figur kommt als Zeile in die Liste `FIGUREN` in `export_alle.py`.

## Was der Export macht

| Generator liefert | Export macht daraus |
|---|---|
| eine Datei je Ansicht | eine Datei mit `view-front`, `view-side`, `view-back` |
| Farben als CSS-Klassen in `<style>` | Farben als Attribute. CSS gewinnt, wie im Browser. |
| ausgeblendete Elemente (`display:none`) | entfernt |
| Hintergrund-Rechteck, `<title>` | entfernt |
| IDs wie `side_leg_near`, `characterSide` | IDs in Kebab-Case, Verweise mitgezogen |
| Rig-IDs | zusätzlich `data-part`, z. B. `bein-links`, `arm-rechts-unten`, `kopf` |
| Fußpunkt (200, 773) per Konvention | `data-part="anchor"` je Ansicht, außerhalb der Hülle `koerper` |

Geprüft am 2026-11-25: Alle 16 Figuren laufen in der Engine (Prototyp, PRs #140 bis #147 auf `main`). Der Validator meldet 0 Fehler, jede Ansicht wird angezeigt, die Seitenansicht nach links gespiegelt.

## Offen, bitte entscheiden

- **Größe:** `height` ist aus der Demo-Szene hochgerechnet (viewBox-Höhe × 0,52 × 1,5). Passt die Größe im Raum?
- **Textfarbe:** Professor und die zehn NPCs haben keine Leuchtfarbe im Styleguide. Bis dahin gilt der Platzhalter `#e8dcc8`.
- **Links und rechts:** `bein-links` ist vorerst das Bein links im Bild. Aus Sicht der Figur wäre es das rechte. Das klärt die Architektur mit dem Vertrag.
- **Animationen:** Der Gang ist JavaScript in `scene_template.html`, `idle` und `talk` gibt es nicht. `animations.json` fehlt deshalb noch. Die Drehpunkte in `character.json` stammen aus dem Styleguide, ihr Bezugssystem ist noch offen.
- **Alchemistin:** Die Vorderansicht in `assets/` hat keine getrennten Beine (`front_leg_l/r`). Die gibt es nur in `build_scene.py`. Für die Anzeige reicht es, für den Gang nicht.

## Gefunden beim Export

- `meister/meister/source/mentor.py`, Zeile 208: Vor dem String mit `{spike(233,548,…)}` fehlt das `f`. Deshalb steht der Platzhalter statt eines Pfads in `meister_seite_*.svg`. Der Export meldet solche Stellen als WARNUNG.

## In der Engine ansehen

Die Engine braucht außerdem `content/game.json` und einen Raum. Den legt der Skill `raum-anlegen` an, die Anleitung dazu steht in `docs/creative/mit-der-engine-arbeiten.md` auf `main`.

## Raum: Lehrsaal der Alchemie

```
python docs/creative/temp/Charaktere/export/export_raum.py
```

Liest die gebaute Demo `Alchemistin/akademie-der-alchemie/akademie-der-alchemie/index.html` (Ausgabe von `build_scene.py`) und die Hotspot-Tabelle `HS` aus `source/scene_template.html`. Ergebnis: `content/rooms/lehrsaal/room.svg` und `room.json`.

| Demo | Export |
|---|---|
| 1280×720 | 1920×1080. Die Koordinaten werden umgerechnet, damit Teile und Animationen in Raumeinheiten stehen. Es gibt keine `scale`-Gruppe. |
| Farben über `body.dark #scene .s-…` und `body.nolines` | Attribute, wie im Spielstil der Demo |
| eine Gruppe `#scene` | `layer-background`, die Vignette in `layer-foreground` |
| Hotspots als JS-Tabelle `HS` | `hotspot-<name>` in `hotspots`, dazu `walkTo` in `room.json` |
| Zustände über `show(id)` | Raumteile mit `data-part` und `visibleIf` |
| CSS-Animationen (Flackern, Blasen, Blinzeln, Kristall) | Raumanimationen in `room.json` |
| Laufbereich `FLOOR_MIN`/`FLOOR_MAX`, `depthScale` | `walkable`, `depth`, Spawn `start` |
| 9 `<text>` (Tafel, Glasetiketten, ATHANOR) | **weggelassen**, Liste im Bericht des Exports |

Namen: Hotspots `eisblock`, `fenster`, `kristall`, `buecher`, `wasserkrug`, `erdtopf`, `eisenspaene`, `pflanze`, `eule`, `tafel`, `kessel`, `athanor`, `tuer`. Teile `eisblock`, `pfuetze`, `schluessel-lose`, `kristall`, `pflanze-vertrocknet`, `ranke`, `feuer`, `tuer-zu`, `tuer-offen`, `tuer-licht`. Die Flags für `visibleIf` sind Vorschläge (`lehrsaal.eis-geschmolzen` usw.).

**Geprüft am 2026-11-25:** SVG ohne Verstöße gegen die SVG-Regeln. In der Engine mit Alchemistin als Spielfigur gerendert, 0 Konsolenfehler.

**Was noch fehlt:**
- **Spiellogik:** Die Verben haben nur Platzhalter („Tafel.“). Die Logik aus `interact()` und `useOn()` im Template übersetzt ein Agent mit dem Skill `raum-anlegen`. Bis dahin meldet der Validator 11× `content.flag-never-set`, weil die Flags der Teile noch niemand setzt. Das ist die offene Arbeit.
- **Zustände in der Engine:** Raumteile und Raumanimationen haben noch keine Anforderungs-ID. Bis sie umgesetzt sind, zeigt die Engine alle Zustände gleichzeitig (Eis und Pfütze, Tür zu und offen) und spielt keine Animation ab.
- **Schrift:** als Pfad mit welcher Schrift und Lizenz, oder ganz ohne? Die Tafel ist Teil des Rätsels („Wasser + Erde = ?“).
- **Kesselfarbe:** In der Demo wechselt sie per CSS-Variable je Ergebnis. Im Export ist sie fest `#9be7ff`, abhängig von der Entscheidung zur Alchemie-Mechanik.
