# Asset-Vertrag

**Status: Entwurf.** Verbindlich wird der Vertrag nach dem [Spike mit einem echten Claude-Design-Export](#spike-claude-design). Verantwortlich: Architektur (PR-03) zusammen mit Creative (PR-04), vertreten durch Benedict ([Rollentrennung](../../voranalyse/01-stakeholder-und-rollen.md#projektrollen)). Dieses Dokument ist der Schema-Entwurf zu Issue #69. Die Abstimmung mit Fabian und Ivan steht aus.

Dieser Vertrag legt fest, wie Inhaltsdateien unter `content/` aussehen müssen, damit die Engine sie ohne Codeänderung lädt (NF-W-01). Er richtet sich an Creative, an Agenten, die Inhalte schreiben, und an die Entwickler von Engine und Validator.

## Teile

| Datei | Inhalt |
|---|---|
| [README.md](README.md) | Grundsätze, Begriffe, Verzeichnis, SVG-Regeln für alle Dateien, `game.json`, Spike |
| [raum.md](raum.md) | `room.svg`, `room.json` |
| [figur.md](figur.md) | `character.svg`, `character.json`, `animations.json` |
| [gegenstand.md](gegenstand.md) | `item.json`, `world.svg`, `icon.svg`, Rezepte |
| [aktionen.md](aktionen.md) | Verben, Bedingungen, Effekte, Dialoge, Zwischensequenzen |
| [ablauf.md](ablauf.md) | Lösungsweg, Zustand und Spielstand |
| [fehlercodes.md](fehlercodes.md) | alle Fehlercodes |

## Grundsätze

- **Eine Regel, eine Prüfung.** Jede Regel hier hat eine Prüfung im Content-Validator mit Fehlercode `<bereich>.<grund>`. Eine Regel ohne Prüfung gehört nicht in diesen Vertrag.
- **Zod ist die Quelle.** Die Zod-Schemas in [`src/engine/core/schema/`](../../../src/engine/core/schema/) sind maßgeblich. Dieses Dokument ist ihre lesbare Fassung und wird in derselben Änderung nachgezogen. Die JSON-Beispiele für Spiel, Raum, Figur, Animationen, Dialog und Zwischensequenz sind Testfälle: Besteht eines sein Schema nicht, ist `make ci` rot (NF-V-01). Gegenstände und Rezepte haben noch kein Schema.
- **SVG ist Grafik, JSON ist Spiel.** SVG-Dateien enthalten nur Grafik und Namen. Alles, was das Spiel tut, und alle Koordinaten, die Werkzeuge setzen, stehen im JSON. So bleiben die SVGs aus Claude Design unverändert.
- **Version:** Jede JSON-Datei beginnt mit `"schemaVersion": 1`. Bricht eine Vertragsänderung bestehende Dateien, steigt die Version.
- **Texte** stehen auf Deutsch direkt im JSON.
- **Koordinaten** in Raumdateien sind viewBox-Einheiten des Raums (0–1920 × 0–1080). Koordinaten in Figuren und Gegenständen beziehen sich auf deren eigene viewBox.
- **Anforderungen** ohne Katalog-ID stehen in den [Anforderungsvorschlägen](../anforderungs-vorschlaege.md).
- **Beispiele** sind Ausschnitte aus einem neutralen Testinhalt ohne Handlung. Verweise auf nicht gezeigte Dateien (z. B. `nebenraum`, `kegel`) sind angenommen.

## Begriffe

| Begriff | Bedeutung |
|---|---|
| ID | Kleinbuchstaben, Ziffern, Bindestrich (`^[a-z0-9]+(-[a-z0-9]+)*$`). Umlaute als `ae`, `oe`, `ue`, `ss`. |
| Flag | Boolescher Schalter im Spielzustand. Name aus IDs mit Punkt getrennt, z. B. `kiste-offen`, `item.testraum.kugel.taken`. |
| Akteur | Figur oder Gegenstand, der in einem Raum platziert ist |
| Interaktionsziel | Hotspot, platzierte Figur oder platzierter Gegenstand |
| Anker | Punkt einer Figur oder eines Gegenstands, der auf der Position im Raum steht (Fußpunkt). Element mit `data-part="anchor"`, maßgeblich ist die Mitte seiner Bounding Box. |
| Basislinie | y-Wert, nach dem Akteure und Mittelebenen sortiert gezeichnet werden. Größeres y liegt weiter vorn. |
| Spawn | Benannter Startpunkt in einem Raum mit Blickrichtung |
| Blickrichtung | `left`, `right`, `front`, `back` |

## Verzeichnis

```
content/
  game.json
  rooms/<raum-id>/room.json
  rooms/<raum-id>/room.svg
  characters/<figur-id>/character.json
  characters/<figur-id>/character.svg
  characters/<figur-id>/animations.json
  items/<gegenstand-id>/item.json
  items/<gegenstand-id>/world.svg
  items/<gegenstand-id>/icon.svg
  recipes/<rezept-id>.json
  dialogs/<dialog-id>.json
  cutscenes/<sequenz-id>.json
  walkthrough.json
  states/<checkpoint-id>.json
  states/manual/<id>.json
```

Der Ordnername ist die ID. Das Feld `id` in der JSON-Datei muss ihm gleichen (`content.id-mismatch`). Dateien außerhalb dieses Schemas meldet der Validator (`content.unknown-file`).

## SVG-Regeln für alle Dateien

| Regel | Fehlercode |
|---|---|
| Wurzelelement `<svg>` mit `viewBox`. Räume: exakt `0 0 1920 1080`. Inventar-Icons: exakt `0 0 128 128`. | `svg.viewbox` |
| Keine Elemente `<image>`, `<text>`, `<script>`, `<foreignObject>`, `<style>` | `svg.forbidden-element` |
| Keine Attribute `on*` (Event-Handler) | `svg.forbidden-attribute` |
| `href` und `xlink:href` nur auf interne Ziele (`#…`) | `svg.external-ref` |
| IDs sind innerhalb der Datei eindeutig | `svg.duplicate-id` |
| IDs folgen dem ID-Format (siehe Begriffe) | `svg.id-format` |
| Kein `<filter>` in Figuren (Bildrate, NF-E-02) | `svg.filter-in-character` |

Farben stehen als Attribute (`fill`, `stroke`) oder im `style`-Attribut des Elements. Verläufe und Masken in `<defs>` sind erlaubt.

## Spiel

`content/game.json`, genau eine Datei.

| Feld | Typ | Pflicht | Bedeutung |
|---|---|---|---|
| `schemaVersion` | `1` | ja | – |
| `title` | Text | ja | Spieltitel |
| `startRoom` | Raum-ID | ja | Raum beim Spielstart (FA-E-03) |
| `startSpawn` | Spawn-Name | ja | Spawn in `startRoom` |
| `player` | Figur-ID | ja | Spielfigur |
| `defaults.look` | Text | ja | Text, wenn „Ansehen“ keine Aktion hat (nur bei Gegenständen ohne Beschreibung relevant) |
| `defaults.useItem` | Text | ja | Text, wenn ein Gegenstand auf ein Ziel ohne passende Aktion angewendet wird |
| `defaults.give` | Text | ja | Text, wenn eine Figur einen Gegenstand nicht annimmt |
| `defaults.combine` | Text | ja | Text, wenn zwei Gegenstände nicht kombinierbar sind |
| `text.minMs` | Zahl | ja | Mindestdauer eines Sprechtexts in ms (Startwert 1500) |
| `text.msPerChar` | Zahl | ja | Dauer je Zeichen in ms (Startwert 70) |

Sprechdauer = max(`text.minMs`, Zeichenzahl × `text.msPerChar`).

```json
{
  "schemaVersion": 1,
  "title": "Testspiel",
  "startRoom": "testraum",
  "startSpawn": "start",
  "player": "figur-a",
  "defaults": {
    "look": "Nichts Besonderes.",
    "useItem": "Das funktioniert so nicht.",
    "give": "Das möchte ich nicht.",
    "combine": "Das passt nicht zusammen."
  },
  "text": { "minMs": 1500, "msPerChar": 70 }
}
```

## Spike Claude Design

Mehrere SVG-Regeln sind Annahmen darüber, was Claude Design ausgibt. Bevor der Vertrag verbindlich wird, erzeugt Creative mit dem [Briefing](../claude-design-briefing.md) einen Raum und eine Figur mit drei Ansichten, exportiert sie und prüft sie von Hand gegen jede Regel.

| Regel | Ergebnis | Workaround |
|---|---|---|
| Export als einzelne SVG-Datei möglich | offen | – |
| viewBox exakt wie gefordert | offen | – |
| keine `<style>`-Elemente, Farben als Attribute | offen | – |
| keine `<text>`- und `<image>`-Elemente | offen | – |
| oberste Gruppen mit geforderten IDs | offen | – |
| `data-part`-Attribute bleiben erhalten | offen | – |
| drei Ansichten deckungsgleich in einer viewBox | offen | – |
| Hotspot-Formen liegen über den gezeichneten Objekten | offen | – |

Hält eine Regel nicht, wird sie angepasst, oder die Entscheidung „kein Import-Skript“ wird neu gestellt ([Entscheidungen](../../entscheidungen.md)).
