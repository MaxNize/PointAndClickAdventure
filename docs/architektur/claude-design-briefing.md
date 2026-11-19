# Briefing für Claude Design

**Status: Entwurf**, wird im [Spike](asset-vertrag/README.md#spike-claude-design) gegen echte Exporte geprüft.

Vorlagen für Creative, um SVGs in Claude Design so zu erzeugen, dass sie den [Asset-Vertrag](asset-vertrag/README.md) erfüllen. Jede Vorlage hat zwei Teile: die **Gestaltung**, die Creative frei schreibt, und die **technischen Vorgaben**, die wörtlich übernommen werden.

## Ablauf

1. Gestaltung beschreiben, technische Vorgaben unverändert anhängen.
2. In Claude Design erzeugen und überarbeiten, bis das Bild passt.
3. Als SVG exportieren und unter dem Pfad aus dem Vertrag ablegen, z. B. `content/rooms/<raum-id>/room.svg`.
4. Validator ausführen. Meldet er Fehlercodes, die Meldung in Claude Design zurückgeben („Korrigiere: `svg.forbidden-element` – `<style>` in Zeile 3“) und neu exportieren.
5. Erst mit 0 Fehlern weiter im [Autoren-Workflow](autoren-workflow.md).

Die SVG wird nach dem Export nicht von Hand umgebaut. Alles, was ein Werkzeug später setzt (begehbare Fläche, Drehpunkte, Positionen), gehört ins JSON.

## Gemeinsame technische Vorgaben

Diesen Block an jede Vorlage anhängen:

```
Technische Vorgaben (verbindlich):
- Gib genau eine SVG-Datei aus.
- Verwende keine <style>-, <text>-, <image>-, <script>- oder <foreignObject>-Elemente.
- Setze Farben nur als Attribute (fill, stroke) oder im style-Attribut des Elements.
- Schreibe Text als Pfade, nicht als <text>.
- Keine eingebetteten oder verlinkten Bilder, keine Schriftarten.
- IDs nur aus Kleinbuchstaben, Ziffern und Bindestrich, jede ID nur einmal.
- Verläufe und Masken in <defs> sind erlaubt.
```

## Vorlage Raum

```
Gestaltung:
<Beschreibung des Raums: Ort, Stimmung, Perspektive, wichtige Objekte>

Technische Vorgaben Raum (verbindlich):
- viewBox="0 0 1920 1080", Seitenverhältnis 16:9.
- Nur diese obersten Gruppen (die Zeichenreihenfolge im Spiel legt die Engine fest):
  <g id="layer-background"> alles hinter den Figuren
  <g id="layer-mid-<name>"> Objekte, hinter denen Figuren entlanglaufen können (optional, je Objekt eine Gruppe)
  <g id="layer-foreground"> alles, was immer vor den Figuren liegt (optional)
  <g id="hotspots"> anklickbare Bereiche
- Für jedes anklickbare Objekt eine einfache Form (rect, polygon, path) in <g id="hotspots">
  mit id="hotspot-<name>" und fill="transparent", deckungsgleich über dem gezeichneten Objekt.
  Anklickbare Objekte: <Liste, z. B. hotspot-tuer, hotspot-kiste>
- Lass für die Figuren eine freie Bodenfläche im unteren Bilddrittel.
- Zeichne keine Figuren in den Raum.
<gemeinsame technische Vorgaben>
```

## Vorlage Figur

```
Gestaltung:
<Beschreibung der Figur: Gestalt, Kleidung, Farben, Stil passend zu den Räumen>

Technische Vorgaben Figur (verbindlich):
- Eine viewBox, in der die Figur ganz steht, Füße an der Unterkante.
- Drei oberste Gruppen, alle in derselben viewBox an derselben Stelle:
  <g id="view-side"> Seitenansicht, Blick nach rechts
  <g id="view-front"> Vorderansicht
  <g id="view-back"> Rückansicht
- In jeder Ansicht die beweglichen Teile als eigene Gruppen mit data-part:
  data-part="koerper", "kopf", "mund", "arm-links", "arm-rechts", "bein-links", "bein-rechts".
  Kopf und Mund dürfen innerhalb von koerper liegen. Arme und Beine als eigene Formen,
  die an Schulter und Hüfte überlappen, damit beim Drehen keine Lücken entstehen.
- In jeder Ansicht ein kleiner unsichtbarer Kreis
  <circle data-part="anchor" r="1" fill="none"/> genau zwischen den Füßen am Boden.
- Keine <filter>-Elemente.
<gemeinsame technische Vorgaben>
```

Die Drehpunkte der Teile setzt Creative danach in der Figuren-Vorschau. Sie landen über den Schreibweg der Werkzeuge in `character.json` (FA-DEV-10).

## Vorlage Gegenstand

Zwei Dateien, zwei Durchläufe.

```
Gestaltung:
<Beschreibung des Gegenstands>

Technische Vorgaben Gegenstand im Raum (verbindlich):
- viewBox passend zum Gegenstand, gezeichnet in der Größe, die er im Raum
  (1920×1080) vorne im Bild hat.
- Ein unsichtbarer Kreis <circle data-part="anchor" r="1" fill="none"/>
  an der Stelle, mit der der Gegenstand auf dem Boden steht.
<gemeinsame technische Vorgaben>
```

```
Technische Vorgaben Inventar-Icon (verbindlich):
- viewBox="0 0 128 128", Gegenstand mittig, ca. 8 Einheiten Rand.
- Gleiche Gestaltung wie der Gegenstand im Raum, ohne Hintergrund.
<gemeinsame technische Vorgaben>
```

## Checkliste vor dem PR

- [ ] Validator: 0 Fehler
- [ ] Raum: Hotspots liegen sichtbar über den richtigen Objekten (im Spiel mit eingeblendeten Hotspots prüfen, FA-DEV-05)
- [ ] Figur: `view-side` blickt nach rechts, alle drei Ansichten stehen auf demselben Anker
- [ ] Keine Inhalte fremder Herkunft (alle Assets entstehen im Team, siehe [Entscheidungen](../entscheidungen.md))
