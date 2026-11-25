# Export der Figuren in die Engine

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
