# Mit der Engine arbeiten

Für Creative: vom eigenen Asset zur sichtbaren Szene. Stand 2026-11-25. Das Zielbild steht im [Autoren-Workflow](../architektur/autoren-workflow.md), das Dateiformat im [Asset-Vertrag](../architektur/asset-vertrag/README.md).

## Was schon geht

| Du willst … | Stand |
|---|---|
| einen Raum mit Ebenen sehen | geht |
| Figuren und Gegenstände im Raum sehen, nach Tiefe skaliert und richtig verdeckt | geht |
| Fehler in deinen Dateien finden | geht: im Browser und mit `npm run validate` |
| Hotspot-Aktionen, Dialoge und Zwischensequenzen schreiben | geht: der Validator prüft Form, Verweise, Flags und Dialogknoten, aber nicht, was bei welchem Spielstand passiert |
| Dialoge und Aktionen im Spiel ausprobieren | noch nicht: Klicken, Kontextmenü, Dialoge abspielen folgen (FA-E-05, FA-E-06, FA-E-19) |
| die Figur laufen lassen | noch nicht (FA-E-07, FA-E-12) |
| Koordinaten mit der Maus setzen | noch nicht (FA-DEV-10). Bis dahin Zahlen im JSON ändern und im Browser ansehen. |

## Einmal einrichten

1. [Node 22](https://nodejs.org/) und Git installieren. Unter Windows für `make` zusätzlich `scoop install make`.
2. Das Repo klonen und im Ordner `make setup` ausführen. Ohne `make` geht auch `npm ci`.
3. `npm run dev` starten und die angezeigte Adresse im Browser öffnen, meist `http://localhost:5173`.

Solange `content/` leer ist, zeigt das Spiel den Fehler `content.game-missing`. Das ist richtig so.

## Wo deine Dateien liegen

```
content/
  game.json                            Titel, Startraum, Spielfigur
  rooms/<raum-id>/room.svg             Grafik mit Ebenen und Hotspots
  rooms/<raum-id>/room.json            Fläche, Tiefe, Spawns, Hotspots, Platzierungen
  characters/<figur-id>/character.svg  drei Ansichten, Teile, Anker
  characters/<figur-id>/character.json Name, Größe, Textfarbe, Drehpunkte
  items/<gegenstand-id>/world.svg      Gegenstand im Raum, mit Anker
  dialogs/<dialog-id>.json
  cutscenes/<sequenz-id>.json
```

IDs bestehen aus Kleinbuchstaben, Ziffern und Bindestrichen, Umlaute als `ae`, `oe`, `ue`, `ss`. Der Ordnername ist die ID.

## Einen Raum sichtbar machen

1. **Grafik:** `room.svg` mit viewBox `0 0 1920 1080`, oberste Gruppen `layer-background`, optional `layer-mid-<name>` und `layer-foreground`, Klickflächen als `hotspot-<name>` in der Gruppe `hotspots`. Keine `<style>`- und `<text>`-Elemente, Farben als Attribute. Details: [Raum](../architektur/asset-vertrag/raum.md).
2. **Beschreibung:** In Prosa nach der [Vorlage](../architektur/autoren-workflow.md#vorlage-prosa-beschreibung) aufschreiben, was der Raum kann.
3. **JSON schreiben lassen:** Claude Code im Repo starten und die Beschreibung mit „Raum anlegen“ geben. Der Skill `raum-anlegen` schreibt `room.json` und, falls nötig, `game.json`. Er fragt nach, statt zu raten.
4. **Ansehen:** `npm run dev`. Fehler erscheinen unten in einer roten Liste mit Code und Datei.
5. **Feinschliff:** Positionen (`walkTo`, Spawns, Fläche, Basislinien) im JSON anpassen, speichern, im Browser ansehen.

## Figuren und Gegenstände

- Eine Figur ist **eine** `character.svg` mit drei Gruppen `view-side` (blickt nach rechts), `view-front`, `view-back`. In jeder Ansicht liegt genau ein Element `data-part="anchor"` am Fußpunkt. Bewegliche Teile tragen `data-part`, z. B. `kopf`, `arm-links`. Details: [Figur](../architektur/asset-vertrag/figur.md).
- `height` in `character.json` ist die Höhe der viewBox in Raumeinheiten bei Skalierung 1. Wie groß die Figur im Raum erscheint, bestimmt zusätzlich die Tiefe des Raums.
- **Die vorhandenen Figuren aus den Generatoren** (`creative/temp`) passen noch nicht: eine Datei je Ansicht, CSS-Klassen, kein `data-part`, kein Anker. Ein Export-Schritt in den Generatoren soll sie umwandeln. Bis er steht, sind sie im Spiel nicht nutzbar.

## Dialoge und Zwischensequenzen

Gespräch oder kleine Szene skizzieren und Claude Code mit „Dialog anlegen“ bzw. „Zwischensequenz anlegen“ geben. Die Skills `dialog-anlegen` und `zwischensequenz-anlegen` schreiben die Dateien, schließen sie an Figur oder Hotspot an und prüfen sie. Abspielen im Spiel kommt später, der Validator meldet aber schon jetzt:

- Knoten, die man nie erreicht, oder Gespräche ohne Ausgang,
- Flags, die gelesen, aber nie gesetzt werden,
- Verweise auf Figuren, Gegenstände, Räume oder Dialoge, die es nicht gibt.

## Fehler lesen

Jeder Fehler hat die Form `<code> <datei> <ort>: <meldung>`, z. B.

```
content.ref-missing content/rooms/labor/room.json hotspots.hotspot-tuer.exit: Raum „keller“ gibt es nicht
```

Alle Codes stehen in den [Fehlercodes](../architektur/asset-vertrag/fehlercodes.md). `npm run validate` prüft alles außer den SVG-Regeln. Die zeigt nur das Spiel im Browser.

## Abgeben

Wie bei allen Änderungen: eigener Branch, Pull Request, Freigabe durch eine andere Person ([Entwicklungsprozess](../prozess/entwicklungsprozess.md)). Vor dem PR muss `npm run validate` 0 Fehler melden.
