# Asset-Vertrag: Aktionen, Dialog, Zwischensequenz

Teil des [Asset-Vertrags](README.md), **Status: Entwurf**.

## Aktionen

Hotspots, Figuren, Gegenstände, Dialoge und Zwischensequenzen nutzen dasselbe Vokabular. Es ist fest und wird nur per Story erweitert. Unbekannte Typen meldet der Validator (`content.schema`).

### Verben

| Schlüssel | Im Menü | Für |
|---|---|---|
| `look` | Ansehen | alle Interaktionsziele, Pflicht |
| `take` | Nehmen | Hotspots, Gegenstände |
| `use` | Benutzen | Hotspots |
| `open` | Öffnen | Hotspots |
| `talk` | Reden | Figuren, Hotspots |
| `useItem` / `give` | Gegenstand benutzen … / Geben … | erscheint bei nichtleerem Inventar immer |

### Bedingungen

Eine Bedingung ist ein Objekt mit genau einem Schlüssel.

| Bedingung | Erfüllt, wenn |
|---|---|
| `{ "flag": "<flag>" }` | Flag gesetzt |
| `{ "hasItem": "<gegenstand-id>" }` | Gegenstand mindestens einmal im Inventar |
| `{ "not": <bedingung> }` | Bedingung nicht erfüllt |
| `{ "all": [<bedingung>, …] }` | alle erfüllt |
| `{ "any": [<bedingung>, …] }` | mindestens eine erfüllt |

`visibleIf` an Platzierungen ist eine Bedingung.

### Effekte

Ein Effekt ist ein Objekt mit `type`. Effektlisten laufen der Reihe nach. Wartende Effekte halten die Liste an, bis sie fertig sind.

| `type` | Felder | Wirkung | Wartet |
|---|---|---|---|
| `say` | `text`, `speaker?` (Figur-ID, Standard: Spielfigur) | Sprechtext über der Figur | ja, Sprechdauer |
| `setFlag` | `flag` | Flag setzen | nein |
| `clearFlag` | `flag` | Flag löschen | nein |
| `addItem` | `item` | Anzahl im Inventar um 1 erhöhen, bei Questgegenständen höchstens bis `maxCount` | nein |
| `removeItem` | `item` | Anzahl im Inventar um 1 senken | nein |
| `pickUp` | `item` | `addItem` und Flag `item.<raum-id>.<gegenstand-id>.taken` für den aktuellen Raum, die Platzierung verschwindet. Bei erreichter Höchstmenge passiert nichts davon. | nein |
| `walkTo` | `x`, `y` oder `hotspot`, `character?` | Figur läuft hin | ja |
| `face` | `facing`, `character?` | Blickrichtung setzen | nein |
| `playAnimation` | `animation`, `character?` | Animation einmal abspielen | ja, eine `duration` |
| `changeRoom` | `room`, `spawn` | Raumwechsel | ja |
| `startDialog` | `dialog` | Dialog starten | ja, bis Dialogende |
| `startCutscene` | `cutscene` | Zwischensequenz starten | ja, bis Sequenzende |
| `if` | `cond`, `then`, `else?` | Verzweigung | wie der gewählte Zweig |
| `wait` | `ms` | Pause | ja |
| `endGame` | – | Spielende, Endbildschirm (FA-E-22) | – |

Ohne `character` wirkt ein Effekt auf die Spielfigur.

| Prüfung | Fehlercode |
|---|---|
| Jede referenzierte Raum-, Figur-, Gegenstands-, Dialog-, Sequenz- und Animations-ID existiert | `content.ref-missing` |
| Jedes gelesene Flag wird irgendwo gesetzt (Ausnahme: `item.<raum-id>.<gegenstand-id>.taken`) | `content.flag-never-set` |

## Dialog

`content/dialogs/<id>.json`

| Feld | Typ | Pflicht | Bedeutung |
|---|---|---|---|
| `schemaVersion`, `id` | – | ja | – |
| `start` | Knoten-ID | ja | Startknoten |
| `nodes` | Objekt `Knoten-ID → Knoten` | ja | – |
| Knoten `lines[]` | `{ speaker, text }` | ja | `speaker`: Figur-ID oder `player` |
| Knoten `effects` | Effektliste | nein | läuft nach den Zeilen |
| Knoten `options[]` | `{ id, text, if?, effects?, next \| end }` | nein | Ohne Optionen endet der Dialog nach dem Knoten. Optionen mit nicht erfüllter Bedingung erscheinen nicht. |

```json
{
  "schemaVersion": 1,
  "id": "test-dialog",
  "start": "hallo",
  "nodes": {
    "hallo": {
      "lines": [{ "speaker": "figur-b", "text": "Hallo." }],
      "options": [
        { "id": "frage", "text": "Was ist in der Kiste?", "next": "kiste" },
        { "id": "tschuess", "text": "Tschüss.", "end": true }
      ]
    },
    "kiste": {
      "lines": [{ "speaker": "figur-b", "text": "Ein Würfel." }],
      "effects": [{ "type": "setFlag", "flag": "von-kiste-gehoert" }],
      "options": [{ "id": "zurueck", "text": "Noch etwas …", "next": "hallo" }]
    }
  }
}
```

| Prüfung | Fehlercode |
|---|---|
| `start` und jedes `next` verweisen auf einen Knoten | `dialog.node-unknown` |
| Jeder Knoten ist vom Start aus erreichbar | `dialog.unreachable` |
| Von jedem Knoten ist ein Ende erreichbar (Rücksprünge erlaubt) | `dialog.no-end` |
| Options-IDs sind je Knoten eindeutig | `dialog.option-duplicate` |

## Zwischensequenz

`content/cutscenes/<id>.json` mit `schemaVersion`, `id` und `steps` (Effektliste). Während der Sequenz nimmt das Spiel keine Eingaben außer `skip` an. `skip` führt alle verbleibenden Zustandsänderungen sofort aus: Figuren stehen am Ziel, Flags und Inventar sind gesetzt, Texte entfallen.

```json
{
  "schemaVersion": 1,
  "id": "test-sequenz",
  "steps": [
    { "type": "walkTo", "character": "figur-b", "x": 1000, "y": 950 },
    { "type": "face", "character": "figur-b", "facing": "front" },
    { "type": "say", "speaker": "figur-b", "text": "Fertig." },
    { "type": "setFlag", "flag": "sequenz-gesehen" }
  ]
}
```

