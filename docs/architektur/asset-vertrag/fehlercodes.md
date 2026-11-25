# Asset-Vertrag: Fehlercodes

Teil des [Asset-Vertrags](README.md), **Status: Entwurf**.


| Code | Bedeutung |
|---|---|
| `content.schema` | Datei verletzt das Zod-Schema (Detail nennt Feld und Erwartung) |
| `content.id-mismatch` | `id` weicht vom Ordner- oder Dateinamen ab |
| `content.unknown-file` | Datei passt nicht ins Verzeichnisschema |
| `content.ref-missing` | Verweis auf eine nicht vorhandene ID |
| `content.flag-never-set` | Flag wird gelesen, aber nirgends gesetzt |
| `content.game-missing` | `content/game.json` fehlt |
| `content.json-invalid` | Datei ist kein gültiges JSON |
| `svg.parse` | Datei ist kein gültiges SVG |
| `svg.viewbox` | viewBox fehlt oder falsch |
| `svg.forbidden-element` | verbotenes Element |
| `svg.forbidden-attribute` | Event-Attribut |
| `svg.external-ref` | Verweis auf externe Ressource |
| `svg.duplicate-id` | ID doppelt in der Datei |
| `svg.id-format` | ID verletzt das ID-Format |
| `svg.filter-in-character` | `<filter>` in einer Figur |
| `svg.hotspot-unmapped` | Hotspot im SVG ohne Eintrag in `room.json` |
| `room.svg-missing` | `room.svg` fehlt neben `room.json` |
| `room.layer-missing` | `layer-background` fehlt |
| `room.unknown-layer` | unbekannte oberste Gruppe |
| `room.hotspot-outside-group` | Hotspot außerhalb der Gruppe `hotspots` |
| `room.hotspot-missing-in-svg` | Hotspot in `room.json` ohne Element im SVG |
| `room.layer-unmapped` | Mittelebene ohne Basislinie oder Basislinie ohne Ebene |
| `room.item-placed-twice` | Gegenstand im selben Raum mehrfach platziert |
| `room.point-outside-walkable` | Punkt außerhalb der begehbaren Fläche |
| `room.walkable-invalid` | Polygon ungültig |
| `room.part-duplicate` | Teilname doppelt im Raum oder verletzt das ID-Format |
| `room.part-in-hotspots` | Teil in der Gruppe `hotspots` |
| `room.part-unmapped` | Teil im SVG ohne Eintrag in `parts` oder `animations` |
| `room.part-unknown` | Teilname in `room.json` ohne `data-part` im SVG |
| `room.animation-origin-missing` | Raumanimation mit Drehung oder Skalierung ohne `origin` |
| `character.svg-missing` | `character.svg` fehlt neben `character.json` |
| `character.view-missing` | Ansichtsgruppe fehlt |
| `character.part-duplicate` | Teilname doppelt in einer Ansicht |
| `character.anchor-missing` | Anker fehlt |
| `character.pivot-missing` | Drehpunkt fehlt |
| `animation.required-missing` | Pflicht-Animation fehlt |
| `animation.part-unknown` | Teil existiert nicht in der Ansicht |
| `animation.keyframes-invalid` | Keyframes nicht aufsteigend oder länger als `duration` |
| `item.anchor-missing` | Anker in `world.svg` fehlt |
| `item.combine-duplicate` | Kombination bei beiden Gegenständen definiert |
| `item.quest-max-missing` | Questgegenstand ohne Höchstmenge |
| `item.alchemie-max-forbidden` | Alchemiegegenstand mit Höchstmenge |
| `item.world-missing` | Platzierter Gegenstand ohne `world.svg` |
| `recipe.result-quest` | Rezept erzeugt einen Questgegenstand |
| `recipe.result-duplicate` | Zwei Rezepte für denselben Gegenstand |
| `recipe.unlock-cleared` | Ein Effekt löscht ein Meilenstein-Flag |
| `inventory.quest-limit` | Laufzeit: Erhalt über der Höchstmenge abgelehnt (FA-G-07) |
| `dialog.node-unknown` | Verweis auf fehlenden Knoten |
| `dialog.unreachable` | Knoten nicht erreichbar |
| `dialog.no-end` | Knoten ohne Weg zu einem Ende |
| `dialog.option-duplicate` | Options-ID doppelt im Knoten |
| `walkthrough.step-invalid` | Schritt im aktuellen Zustand nicht ausführbar |
| `walkthrough.unsolvable` | Lösungsweg erreicht das Spielende nicht |
| `walkthrough.checkpoint-duplicate` | Checkpoint-ID doppelt |
| `state.ref-missing` | Zustand verweist auf fehlende ID |
| `state.quest-limit` | Zustand enthält mehr Exemplare als die Höchstmenge |
| `state.player-outside-walkable` | Spielfigur außerhalb der Fläche |
| `state.unknown` | Zustands-ID unbekannt (FA-DEV-04) |
| `save.busy` | Speichern außerhalb des Ruhezustands |

