# Asset-Vertrag: Figur

Teil des [Asset-Vertrags](README.md), **Status: Entwurf**.


## character.svg

Eine Datei je Figur mit allen Ansichten, gezeichnet in derselben viewBox. Die Figur steht in jeder Ansicht an derselben Stelle.

| Regel | Fehlercode |
|---|---|
| Oberste Gruppen `view-side`, `view-front`, `view-back` vorhanden | `character.view-missing` |
| Teile tragen `data-part="<name>"`. Der Name ist je Ansicht eindeutig. | `character.part-duplicate` |
| Jede Ansicht hat genau ein Element `data-part="anchor"` | `character.anchor-missing` |

**Empfohlenes Standard-Rig**, damit Animationen zwischen Figuren übertragbar sind: `koerper`, `kopf`, `mund`, `arm-links`, `arm-rechts`, `bein-links`, `bein-rechts`. Teile dürfen verschachtelt sein (z. B. `kopf` in `koerper`). Ein Teil bewegt sich dann mit seinem Elternteil.

`view-side` zeigt die Figur nach rechts blickend, nach links spiegelt die Engine. Das prüft kein Skript, sondern die Checkliste im [Briefing](../claude-design-briefing.md#checkliste-vor-dem-pr).

Sichtbarkeit (`display`, `visibility`) der Ansichtsgruppen setzt die Engine. Angaben in der Datei werden überschrieben.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 400">
  <g id="view-side">
    <g data-part="bein-links"><rect x="85" y="260" width="20" height="135" fill="#303030"/></g>
    <g data-part="bein-rechts"><rect x="95" y="260" width="20" height="135" fill="#404040"/></g>
    <g data-part="koerper">
      <rect x="70" y="120" width="60" height="150" fill="#3060a0"/>
      <g data-part="kopf">
        <circle cx="100" cy="80" r="40" fill="#f0c090"/>
        <g data-part="mund"><rect x="115" y="95" width="15" height="4" fill="#802020"/></g>
      </g>
    </g>
    <g data-part="arm-links"><rect x="90" y="130" width="20" height="110" fill="#2050a0"/></g>
    <g data-part="arm-rechts"><rect x="95" y="130" width="20" height="110" fill="#2050a0"/></g>
    <circle data-part="anchor" cx="100" cy="399" r="1" fill="none"/>
  </g>
  <g id="view-front"><!-- gleiche data-part-Namen, gleicher Anker --></g>
  <g id="view-back"><!-- gleiche data-part-Namen, gleicher Anker --></g>
</svg>
```

## character.json

| Feld | Typ | Pflicht | Bedeutung |
|---|---|---|---|
| `schemaVersion`, `id`, `name` | – | ja | `name` erscheint im Kontextmenü |
| `height` | Zahl | ja | Höhe der viewBox in Raumeinheiten bei Skalierung 1 |
| `speed` | Zahl | ja | Laufgeschwindigkeit in Raumeinheiten je Sekunde bei Skalierung 1 |
| `textColor` | Farbe `#rrggbb` | ja | Farbe der Sprechtexte |
| `pivots` | Objekt `side\|front\|back → Teil → [x, y]` | ja | Drehpunkt je Teil und Ansicht in Figurkoordinaten |

```json
{
  "schemaVersion": 1,
  "id": "figur-a",
  "name": "Figur A",
  "height": 400,
  "speed": 300,
  "textColor": "#ffffff",
  "pivots": {
    "side":  { "kopf": [100, 115], "arm-links": [100, 135], "arm-rechts": [105, 135], "bein-links": [95, 265], "bein-rechts": [105, 265] },
    "front": { "kopf": [100, 115] },
    "back":  { "kopf": [100, 115] }
  }
}
```

## animations.json

Objekt `Animationsname → Animation`.

| Feld | Typ | Pflicht | Bedeutung |
|---|---|---|---|
| `loop` | ja/nein | ja | Wiederholen |
| `duration` | Sekunden | ja | Länge eines Durchlaufs |
| `views.side`, `views.front`, `views.back` | Objekt mit `tracks` | siehe Pflicht-Animationen | Spuren je Ansicht |
| `tracks[].part` | Teilname | ja | Animiertes Teil |
| `tracks[].keyframes[]` | `{ t, rotate?, x?, y?, scale?, opacity?, ease? }` | ja | `t` in Sekunden ab 0. Werte relativ zur Ruhepose: `rotate` in Grad um den Drehpunkt, `x`/`y` Verschiebung in Figurkoordinaten, `scale` Faktor, `opacity` 0–1. `ease`: `linear`, `in`, `out`, `inOut`. |

**Pflicht-Animationen:** `idle` und `walk` in allen drei Ansichten, `talk` in `side` und `front`. Fehlt `talk` in `back`, spielt die Engine dort `idle`. Das Beispiel zeigt nur `idle`.

```json
{
  "idle": {
    "loop": true, "duration": 2,
    "views": {
      "side":  { "tracks": [{ "part": "kopf", "keyframes": [{ "t": 0, "rotate": 0 }, { "t": 1, "rotate": 2, "ease": "inOut" }, { "t": 2, "rotate": 0 }] }] },
      "front": { "tracks": [] },
      "back":  { "tracks": [] }
    }
  }
}
```

| Prüfung | Fehlercode |
|---|---|
| Pflicht-Animationen vorhanden | `animation.required-missing` |
| Jedes `part` existiert als `data-part` in der Gruppe der Ansicht | `animation.part-unknown` |
| Jedes animierte Teil mit `rotate` oder `scale` hat einen Drehpunkt in `pivots` | `character.pivot-missing` |
| Keyframes aufsteigend nach `t`, letztes `t` ≤ `duration` | `animation.keyframes-invalid` |

