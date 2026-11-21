# Asset-Vertrag: Raum

Teil des [Asset-Vertrags](README.md), **Status: Entwurf**.


## room.svg

| Regel | Fehlercode |
|---|---|
| Oberste Gruppe `layer-background` vorhanden | `room.layer-missing` |
| Hotspots liegen als Elemente mit ID `hotspot-<name>` in der obersten Gruppe `hotspots` | `room.hotspot-outside-group` |
| Weitere oberste Gruppen nur `layer-mid-<name>` und `layer-foreground` | `room.unknown-layer` |
| Jeder `hotspot-…` im SVG hat einen Eintrag in `room.json` | `svg.hotspot-unmapped` |

Hotspots dürfen unsichtbar sein (`fill="transparent"` oder `opacity="0"`). Die Engine macht sie trotzdem klickbar. Was der Spieler sieht, gehört in die Ebenen, nicht in `hotspots`.

**Teile:** Raumgrafik, die sich mit dem Spielzustand ändert (Tür zu und offen, Feuer an) oder sich bewegt (Flamme, Blasen), steht als Gruppe mit `data-part="<name>"` in ihrer Ebene. Mehrere Zustände eines Objekts werden übereinander gezeichnet, je Zustand ein Teil. Was sie tun, steht in `room.json` unter `parts` und `animations`.

| Regel | Fehlercode |
|---|---|
| Teilname folgt dem ID-Format und ist im Raum eindeutig | `room.part-duplicate` |
| Kein Teil in der Gruppe `hotspots` | `room.part-in-hotspots` |
| Jedes Teil im SVG wird in `parts` oder `animations` verwendet | `room.part-unmapped` |

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080">
  <g id="layer-background">
    <rect x="0" y="0" width="1920" height="1080" fill="#d0d0d0"/>
    <g data-part="kiste-zu"><rect x="550" y="600" width="120" height="100" fill="#808080"/></g>
    <g data-part="kiste-auf"><rect x="550" y="620" width="120" height="80" fill="#707070"/></g>
    <rect x="1700" y="500" width="120" height="300" fill="#606060"/>
    <rect x="300" y="560" width="16" height="60" fill="#f0f0f0"/>
    <g data-part="flamme"><path d="M308,556 Q300,544 308,530 Q316,544 308,556 Z" fill="#ffd84a"/></g>
  </g>
  <g id="layer-mid-block">
    <rect x="800" y="760" width="200" height="140" fill="#505050"/>
  </g>
  <g id="layer-foreground">
    <rect x="0" y="1000" width="200" height="80" fill="#404040"/>
  </g>
  <g id="hotspots">
    <rect id="hotspot-kiste" x="550" y="600" width="120" height="100" fill="transparent"/>
    <rect id="hotspot-tuer" x="1700" y="500" width="120" height="300" fill="transparent"/>
  </g>
</svg>
```

## room.json

| Feld | Typ | Pflicht | Bedeutung |
|---|---|---|---|
| `schemaVersion`, `id`, `name` | – | ja | `name` erscheint im Spiel nicht, dient der Übersicht |
| `walkable.outer` | Liste `[x, y]` | ja | Außenrand der begehbaren Fläche, mind. 3 Punkte, nicht selbstschneidend |
| `walkable.holes` | Liste von Polygonen | nein | Hindernisse innerhalb der Fläche |
| `depth.far` | `{ y, scale }` | ja | Skalierung am hinteren Rand |
| `depth.near` | `{ y, scale }` | ja | Skalierung am vorderen Rand, `near.y > far.y` |
| `spawns` | Objekt `name → { x, y, facing }` | ja | mind. ein Spawn, jeder innerhalb der begehbaren Fläche |
| `layers` | Objekt `layer-mid-<name> → { baseline }` | wenn Mittelebenen existieren | Basislinie je Mittelebene |
| `hotspots` | Objekt `hotspot-<name> → Hotspot` | wenn Hotspots existieren | siehe unten |
| `parts` | Objekt `Teilname → { visibleIf }` | nein | Teil nur sichtbar, solange die Bedingung erfüllt ist. Teile ohne Eintrag sind immer sichtbar. |
| `animations` | Liste `Raumanimation` | nein | siehe unten |
| `items` | Liste `Platzierung Gegenstand` | nein | siehe unten |
| `characters` | Liste `Platzierung Figur` | nein | siehe unten |
| `onEnter` | Effektliste | nein | läuft bei jedem Betreten |

**Hotspot**

| Feld | Typ | Pflicht | Bedeutung |
|---|---|---|---|
| `name` | Text | ja | Anzeigename, z. B. im Kontextmenü |
| `visibleIf` | Bedingung | nein | Hotspot nur klickbar, solange die Bedingung erfüllt ist |
| `walkTo` | `{ x, y }` | ja | Hier steht die Spielfigur bei jeder Aktion. Innerhalb der begehbaren Fläche. |
| `facing` | Blickrichtung | nein | Blickrichtung bei der Aktion |
| `exit` | `{ room, spawn, if?, else? }` | nein | Macht den Hotspot zum Ausgang. `if` ist eine Bedingung, `else` eine Effektliste, wenn sie nicht erfüllt ist. |
| `verbs.look` | Effektliste | ja | Ansehen |
| `verbs.take`, `verbs.use`, `verbs.open`, `verbs.talk` | Effektliste | nein | Weitere Verben im Kontextmenü |
| `useItem` | Objekt `Gegenstand-ID → Effektliste` | nein | Gegenstand auf diesen Hotspot anwenden |

**Platzierung Gegenstand:** `{ item, x, y, walkTo, visibleIf?, verbs? }`. `x`, `y` dürfen außerhalb der begehbaren Fläche liegen (z. B. auf einem Tisch), `walkTo` nicht. Ohne eigene `verbs` gilt: Ansehen sagt `description` des Gegenstands, Nehmen führt `pickUp` aus. Nach dem Aufnehmen setzt die Engine das Flag `item.<raum-id>.<gegenstand-id>.taken`. Danach ist diese Platzierung unsichtbar, Platzierungen desselben Gegenstands in anderen Räumen bleiben sichtbar. Je Raum darf ein Gegenstand höchstens einmal platziert sein (`room.item-placed-twice`). Die Basislinie ist `y`.

**Platzierung Figur:** `{ character, x, y, facing, walkTo, visibleIf?, verbs, give? }`. Wie bei Gegenständen muss nur `walkTo` in der begehbaren Fläche liegen. `verbs.look` ist Pflicht, `verbs.talk` meist ein `startDialog`. `give` ist ein Objekt `Gegenstand-ID → Effektliste`. Die Spielfigur wird nicht platziert, sie kommt über Spawns.

**Raumanimation:** `{ part, duration, delay?, origin?, keyframes }`. Läuft in Schleife, solange das Teil sichtbar ist. `keyframes` wie in [`animations.json`](figur.md#animationsjson), Koordinaten in Raumeinheiten. `delay` verschiebt den Start in Sekunden (z. B. versetzte Blasen). `origin` ist der Drehpunkt `[x, y]` für `rotate`, `scale`, `scaleX` und `scaleY`. Erlaubt sind nur Transformationen und Deckkraft (Bildrate, NF-E-02).

```json
{
  "schemaVersion": 1,
  "id": "testraum",
  "name": "Testraum",
  "walkable": {
    "outer": [[100, 700], [1820, 700], [1820, 1060], [100, 1060]],
    "holes": [[[800, 820], [1000, 820], [1000, 900], [800, 900]]]
  },
  "depth": { "far": { "y": 700, "scale": 0.6 }, "near": { "y": 1060, "scale": 1.0 } },
  "spawns": {
    "start": { "x": 300, "y": 950, "facing": "right" },
    "von-nebenraum": { "x": 1700, "y": 900, "facing": "left" }
  },
  "layers": { "layer-mid-block": { "baseline": 900 } },
  "parts": {
    "kiste-zu":  { "visibleIf": { "not": { "flag": "kiste-offen" } } },
    "kiste-auf": { "visibleIf": { "flag": "kiste-offen" } }
  },
  "animations": [
    { "part": "flamme", "duration": 0.6, "origin": [308, 556],
      "keyframes": [{ "t": 0, "scaleY": 1 }, { "t": 0.3, "scaleY": 1.12, "scaleX": 0.94, "ease": "inOut" }, { "t": 0.6, "scaleY": 1 }] }
  ],
  "hotspots": {
    "hotspot-kiste": {
      "name": "Kiste",
      "walkTo": { "x": 600, "y": 800 },
      "facing": "back",
      "verbs": {
        "look": [{ "type": "say", "text": "Eine graue Kiste." }],
        "open": [
          { "type": "if", "cond": { "flag": "kiste-offen" },
            "then": [{ "type": "say", "text": "Schon offen." }],
            "else": [{ "type": "setFlag", "flag": "kiste-offen" }, { "type": "addItem", "item": "wuerfel" }] }
        ]
      }
    },
    "hotspot-tuer": {
      "name": "Tür",
      "walkTo": { "x": 1750, "y": 880 },
      "exit": {
        "room": "nebenraum", "spawn": "von-testraum",
        "if": { "hasItem": "wuerfel" },
        "else": [{ "type": "say", "text": "Erst die Kiste." }]
      },
      "verbs": { "look": [{ "type": "say", "text": "Eine Tür." }] }
    }
  },
  "items": [{ "item": "kugel", "x": 1200, "y": 950, "walkTo": { "x": 1150, "y": 960 } }],
  "characters": [
    { "character": "figur-b", "x": 1400, "y": 780, "facing": "left", "walkTo": { "x": 1300, "y": 800 },
      "verbs": { "look": [{ "type": "say", "text": "Figur B." }], "talk": [{ "type": "startDialog", "dialog": "test-dialog" }] } }
  ]
}
```

| Prüfung über Dateien hinweg | Fehlercode |
|---|---|
| Jeder Eintrag in `hotspots` hat ein Element im SVG | `room.hotspot-missing-in-svg` |
| Jeder Eintrag in `layers` hat eine Gruppe im SVG, jede `layer-mid-*`-Gruppe einen Eintrag | `room.layer-unmapped` |
| Alle `walkTo`-Punkte und Spawns liegen in der begehbaren Fläche (Platzierungen dürfen außerhalb liegen) | `room.point-outside-walkable` |
| Polygon gültig: mind. 3 Punkte, nicht selbstschneidend, Löcher innerhalb | `room.walkable-invalid` |
| `exit.room` und `exit.spawn` existieren | `content.ref-missing` |
| Jeder Teilname in `parts` und `animations` hat ein `data-part` im SVG | `room.part-unknown` |
| Jede Raumanimation mit `rotate`, `scale`, `scaleX` oder `scaleY` hat `origin` | `room.animation-origin-missing` |
| Keyframes aufsteigend nach `t`, letztes `t` ≤ `duration` | `animation.keyframes-invalid` |

