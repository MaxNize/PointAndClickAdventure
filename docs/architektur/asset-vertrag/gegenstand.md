# Asset-Vertrag: Gegenstand und Rezept

Teil des [Asset-Vertrags](README.md), **Status: Entwurf**.

## Gegenstand

Ein Ordner je Gegenstand. Begriffe und Anforderungen: [Gegenstände](../../creative/gegenstaende.md) (FA-G-01 bis FA-G-08).

| Datei | Inhalt |
|---|---|
| `item.json` | siehe Tabelle unten |
| `world.svg` | Darstellung im Raum mit genau einem `data-part="anchor"` (Fehler `item.anchor-missing`). Gezeichnet in Raumeinheiten bei Skalierung 1. Entfällt bei Gegenständen, die nie im Raum liegen (z. B. nur herstellbare Alchemiegegenstände). |
| `icon.svg` | Inventar-Icon, viewBox `0 0 128 128` |

**item.json**

| Feld | Typ | Pflicht | Bedeutung |
|---|---|---|---|
| `schemaVersion`, `id`, `name`, `description` | – | ja | `description` ist der Text bei „Ansehen“ |
| `type` | `alchemie` oder `quest` | ja | Alchemiegegenstand (herstellbar, unbegrenzt) oder Questgegenstand (nicht herstellbar, begrenzt) |
| `maxCount` | ganze Zahl ≥ 1 | bei `quest` ja, bei `alchemie` verboten | Höchstmenge im Inventar (FA-G-07) |
| `combine` | Objekt `Gegenstand-ID → Effektliste` | nein | Erlaubte Kombinationen |

**Kombinationen:** Eine Kombination steht nur bei einem der beiden Gegenstände. Die Engine findet sie in beiden Reihenfolgen. Steht dasselbe Paar bei beiden, meldet der Validator `item.combine-duplicate`. Jede nicht definierte Kombination lehnt die Engine ab: Alle Gegenstände bleiben unverändert, es erscheint `defaults.combine` (FA-G-04; Rückmeldung ist eine Annahme bis zur Antwort von Creative).

**Einsatzorte** sind die `useItem`-Einträge an Hotspots und die `give`-Einträge an Figuren. Ein Rätsel setzt dort ein Flag (FA-G-02), eine Information erscheint per `say` (FA-G-08). Ob ein Gegenstand beim Einsetzen verbraucht wird, legt jeder Einsatzort selbst mit `removeItem` fest.

**Menge:** Das Inventar führt je Gegenstand eine Anzahl. `addItem` und `pickUp` erhöhen sie um 1. Bei einem Questgegenstand, der seine Höchstmenge erreicht hat, lehnt die Engine das ab (Ereignis `inventory.quest-limit`), und der Raumgegenstand bleibt liegen. Annahme bis zur Antwort von Creative: Die Höchstmenge gilt für den aktuellen Bestand, nicht für alle je erhaltenen Exemplare.

```json
{
  "schemaVersion": 1,
  "id": "wuerfel",
  "name": "Würfel",
  "description": "Ein roter Würfel.",
  "type": "quest",
  "maxCount": 1,
  "combine": {
    "kugel": [{ "type": "removeItem", "item": "wuerfel" }, { "type": "removeItem", "item": "kugel" }, { "type": "addItem", "item": "kegel" }]
  }
}
```

| Prüfung | Fehlercode |
|---|---|
| `quest` ohne `maxCount` | `item.quest-max-missing` |
| `alchemie` mit `maxCount` | `item.alchemie-max-forbidden` |
| Ein Gegenstand, der in einem Raum platziert ist, hat `world.svg` | `item.world-missing` |

## Rezept

`content/recipes/<id>.json`, eine Datei je Rezept (FA-G-01, FA-G-03, FA-G-05, FA-G-06).

| Feld | Typ | Pflicht | Bedeutung |
|---|---|---|---|
| `schemaVersion`, `id`, `name` | – | ja | `name` erscheint im Rezeptbuch |
| `result` | Gegenstands-ID | ja | Erzeugter Gegenstand, muss `type: "alchemie"` haben |
| `unlockedBy` | Flag | ja | Meilenstein, der das Rezept freischaltet |
| `ingredients` | Liste von Texten | ja | Zutaten zur Anzeige im Rezeptbuch |

Herstellen verbraucht nichts. `craft` legt den Gegenstand ins Inventar, beliebig oft (FA-G-06). Damit freigeschaltete Rezepte verfügbar bleiben (FA-G-03), darf kein Effekt ein Meilenstein-Flag wieder löschen.

**Annahmen bis zur Antwort von Creative** (Issues #71 und #76, [Offene Fragen](../../offene-fragen.md)):

- Ein Meilenstein ist ein Flag, das ein Rätsel oder eine Zwischensequenz setzt.
- Ressourcen sind keine Inventargegenstände. Zutaten stehen nur als Text im Rezept.

```json
{
  "schemaVersion": 1,
  "id": "trank-blau",
  "name": "Blauer Trank",
  "result": "trank-blau",
  "unlockedBy": "kiste-offen",
  "ingredients": ["Wasser", "Blaue Blüte"]
}
```

| Prüfung | Fehlercode |
|---|---|
| `result` ist ein Questgegenstand (FA-G-05, NF-V-01) | `recipe.result-quest` |
| `result` existiert | `content.ref-missing` |
| `unlockedBy` wird irgendwo gesetzt | `content.flag-never-set` |
| Höchstens ein Rezept je Ergebnis | `recipe.result-duplicate` |
| Kein `clearFlag` auf ein `unlockedBy`-Flag | `recipe.unlock-cleared` |

