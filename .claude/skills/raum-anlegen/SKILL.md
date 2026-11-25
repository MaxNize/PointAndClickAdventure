---
name: raum-anlegen
description: Einen Raum für das Adventure aus einer Prosa-Beschreibung von Creative anlegen oder erweitern (room.json, bei Bedarf Platzhalter-room.svg und game.json). Verwenden, wenn jemand einen Raum, Hotspots, Ausgänge, platzierte Figuren oder Gegenstände beschreibt oder „Raum anlegen“ sagt.
---

# Raum aus Prosa-Beschreibung anlegen

Creative beschreibt einen Raum in Prosa nach der [Vorlage](../../../docs/architektur/autoren-workflow.md#vorlage-prosa-beschreibung). Du schreibst daraus die Dateien nach dem [Asset-Vertrag](../../../docs/architektur/asset-vertrag/README.md). Creative prüft das Ergebnis im Spiel.

## Regeln

- Schreibe nur unter `content/`. Kein Code, keine Doku, keine Gate-Dateien.
- Erfinde nichts, was die Handlung betrifft: Texte, Rätsellösungen, Bedingungen, Zielräume. Fehlt etwas, frag nach. Sammle die Fragen und stell sie auf einmal.
- Nur das Vokabular aus [Aktionen](../../../docs/architektur/asset-vertrag/aktionen.md). Was dort fehlt, ist eine neue Engine-Funktion. Sag das, statt es nachzubauen.
- IDs: Kleinbuchstaben, Ziffern, Bindestrich, Umlaute als `ae`, `oe`, `ue`, `ss`.
- Ein SVG von Creative änderst du nicht. Fehlt etwas darin (Hotspot, Ebene, Teil), sag es Creative.
- Du bist fertig, wenn `npm run validate` 0 Fehler meldet.

## Ablauf

1. **Lesen:** [raum.md](../../../docs/architektur/asset-vertrag/raum.md) und [aktionen.md](../../../docs/architektur/asset-vertrag/aktionen.md). Dann den Bestand: `content/game.json`, vorhandene Räume, Figuren und Gegenstände. Suche die Flags, die schon gesetzt werden (`grep -r '"setFlag"' content`).
2. **SVG klären:**
   - Liegt `content/rooms/<raum-id>/room.svg` schon vor, lies die obersten Gruppen, die `hotspot-…`-IDs und die `data-part`-Namen. Sie bestimmen, was in `room.json` steht.
   - Fehlt das SVG, leg einen **Platzhalter** an: viewBox `0 0 1920 1080`, eine Gruppe `layer-background` mit einem neutralen Rechteck und einem Kommentar `<!-- Platzhalter, Grafik folgt von Creative -->`, dazu `hotspots` mit je einem transparenten Rechteck an der grob beschriebenen Stelle. Sag Creative, dass die Grafik fehlt.
3. **room.json schreiben:**
   - Begehbare Fläche, Tiefe und Spawns aus der Beschreibung. Ist nichts beschrieben, nimm den Boden im unteren Drittel (`y` 700 bis 1060) und schreib das als Annahme in deinen Bericht.
   - Je Hotspot: `name`, `walkTo` in der begehbaren Fläche, `verbs.look` (Pflicht), weitere Verben, `useItem`, `exit`.
   - Platzierte Figuren und Gegenstände mit `verbs.look`. Bei Figuren wird `talk` meist zu `startDialog`. Den Dialog legt der Skill `dialog-anlegen` an.
   - Flags: Benenne sie nach dem, was passiert ist, z. B. `kiste-offen` oder `<raum-id>.kerze-an`. Jedes gelesene Flag muss irgendwo gesetzt werden.
4. **game.json:** Fehlt sie, leg sie an. Frag nach Titel und Spielfigur. Der erste Raum wird `startRoom`, sein erster Spawn `startSpawn`. Standardtexte schlägst du vor und markierst sie als Vorschlag.
5. **Prüfen:** `npm run validate`. Behebe jeden Fehler. Der Code steht in [Fehlercodes](../../../docs/architektur/asset-vertrag/fehlercodes.md).
6. **Bericht an Creative:** geänderte Dateien, neue Flags, Annahmen (Fläche, Positionen), offene Fragen. Dazu der Hinweis: `npm run dev` zeigt den Raum, Fehler in der SVG stehen in der roten Liste unten.

## Was das Spiel schon kann

Die Szene ist sichtbar: Raum, Figuren, Gegenstände, Tiefe und Verdeckung. Verben, Ausgänge und Dialoge prüft der Validator, das Spiel führt sie aber noch nicht aus (Klick und Kontextmenü: FA-E-05, FA-E-06). Koordinaten setzt Creative vorerst von Hand im JSON und prüft sie im Browser. Das Raum-Overlay (FA-DEV-10) folgt.
