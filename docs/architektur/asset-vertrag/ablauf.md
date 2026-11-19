# Asset-Vertrag: Lösungsweg und Zustand

Teil des [Asset-Vertrags](README.md), **Status: Entwurf**.

## Lösungsweg

`content/walkthrough.json` beschreibt einen vollständigen Weg vom Start bis zum Ende mit semantischen Befehlen. Der Gate-Lauf spielt ihn ohne Browser ab (NF-V-02) und erzeugt daraus die Testzustände (FA-DEV-02).

| `do` | Felder |
|---|---|
| `interact` | `target`, `verb` |
| `exit` | `target` |
| `useItem` | `item`, `target` |
| `combine` | `a`, `b` |
| `craft` | `recipe` |
| `choose` | `option` (Options-ID im aktuellen Dialogknoten) |
| `walkTo` | `x`, `y` |

Jeder Schritt kann `"checkpoint": "<id>"` tragen. Nach diesem Schritt wird `content/states/<id>.json` erzeugt.

```json
{
  "schemaVersion": 1,
  "steps": [
    { "do": "interact", "target": "hotspot-kiste", "verb": "open", "checkpoint": "kiste-offen" },
    { "do": "exit", "target": "hotspot-tuer" }
  ]
}
```

| Prüfung | Fehlercode |
|---|---|
| Jeder Schritt ist im jeweiligen Zustand ausführbar | `walkthrough.step-invalid` |
| Nach dem letzten Schritt ist das Spiel beendet (`endGame`) | `walkthrough.unsolvable` |
| Checkpoint-IDs sind eindeutig | `walkthrough.checkpoint-duplicate` |

## Zustand

Ein Format für Spielstand (NF-V-03, FA-E-21), Testzustände (FA-DEV-01, FA-DEV-02) und Export (FA-DEV-03).

| Feld | Typ |
|---|---|
| `schemaVersion` | `1` |
| `room` | Raum-ID |
| `player` | `{ x, y, facing }` |
| `inventory` | Liste `{ item, count }`, Reihenfolge wie im Inventar |
| `flags` | Liste gesetzter Flags |

Zwei Regeln halten das Format klein:

- Gespeichert wird nur im Ruhezustand, also nicht während eines Dialogs, einer Zwischensequenz oder einer Laufbewegung. Ein Versuch liefert `save.busy`.
- Nebenfiguren stehen nach dem Laden an ihrer Platzierung aus der Raumdefinition. Dauerhafte Änderungen laufen über Flags und `visibleIf`.

Zustand nach dem Checkpoint `kiste-offen` aus dem Lösungsweg oben:

```json
{
  "schemaVersion": 1,
  "room": "testraum",
  "player": { "x": 600, "y": 800, "facing": "back" },
  "inventory": [{ "item": "wuerfel", "count": 1 }],
  "flags": ["kiste-offen"]
}
```

| Prüfung | Fehlercode |
|---|---|
| Alle IDs im Zustand existieren | `state.ref-missing` |
| Keine Anzahl über der Höchstmenge eines Questgegenstands | `state.quest-limit` |
| Spielfigur steht in der begehbaren Fläche | `state.player-outside-walkable` |
| Unbekannte Zustands-ID bei `?state=` | `state.unknown` |

