# Autoren-Workflow

Wie Creative aus Assets ein spielbares Spiel baut. Entschieden am 2026-11-19 ([Entscheidungen](../entscheidungen.md)). Die Werkzeuge stehen als FA-DEV-07 bis FA-DEV-15 im [Katalog](../voranalyse/03-anforderungen.md).

## Grundsatz

Die Engine stellt **schlanke Werkzeuge** bereit. Sie schreiben oder zeigen nur die JSON-Dateien unter `content/`. Diese Dateien bleiben die einzige Wahrheit: Der Validator prüft sie, Git zeigt jede Änderung als Diff, Agenten können sie lesen und schreiben.

| Weg | Bewertung |
|---|---|
| Spiellogik komplett von Hand in den Assets | verworfen. Räumliche Daten (Polygone, Laufpunkte, Drehpunkte) lassen sich ohne Blick aufs Bild nicht verlässlich setzen. Fehler fallen erst spät auf. |
| Eigenes Adventure-Studio mit Timeline- und Knoten-Editor | verworfen. Übersteigt die Kapazität von zwei Fullstack-Entwicklern im Semester und konkurriert mit der Engine. |
| **Schlanke Werkzeuge über dem JSON-Vertrag** | gewählt. Räumliches setzt Creative im Spiel, Erzählerisches schreibt ein Agent aus einer Prosa-Beschreibung. |

## Wer schreibt was

| Daten | Autor | Werkzeug |
|---|---|---|
| Grafik (SVG) | Creative mit Claude Design | [Briefing](claude-design-briefing.md) |
| Räumliches: begehbare Fläche, `walkTo`, Spawns, Tiefe, Basislinien, Platzierungen | Creative | Raum-Overlay (FA-DEV-10) |
| Drehpunkte | Creative | in der Figuren-Vorschau setzen, Schreibweg FA-DEV-10 |
| Animations-Keyframes | Agent aus Beschreibung, Creative prüft | Figuren-Vorschau (FA-DEV-15) |
| Erzählerisches: Hotspot-Aktionen, Bedingungen, Dialoge, Zwischensequenzen | **Agent aus Prosa-Beschreibung**, Creative prüft im Spiel | Agenten-Skills, Dialog direkt starten (FA-DEV-13), Sequenz ab Schritt (FA-DEV-14), Inhaltsgraph (FA-DEV-12) |
| Gegenstände und Rezepte: Typ, Höchstmenge, Zutaten, Meilenstein | Agent aus der Gegenstands- und Rezeptliste von Creative (Issue #76) | Gerüst (FA-DEV-09), Inhaltsgraph (FA-DEV-12) |
| Lösungsweg mit Checkpoints | Creative | Lösungsweg-Rekorder (FA-DEV-11) |

## Ablauf für einen neuen Raum

1. **Gerüst anlegen:** `make new-room ID=<raum-id>` erzeugt Ordner, `room.json` und einen leeren SVG-Rahmen (FA-DEV-09).
2. **Grafik erzeugen:** Raum-SVG mit Claude Design nach [Briefing](claude-design-briefing.md), ablegen als `room.svg`.
3. **Validator grün:** Der Validator im Watch-Modus zeigt Fehlercodes direkt im Spiel (FA-DEV-07).
4. **Räumliches setzen:** Im Entwicklungsmodus das Raum-Overlay öffnen. Begehbare Fläche, Spawns, `walkTo`-Punkte, Tiefe und Basislinien per Klick setzen, Figur zur Probe durch den Raum ziehen. Speichern schreibt `room.json` (FA-DEV-10).
5. **Interaktionen beschreiben:** In Prosa nach der Vorlage unten. Ein Agent schreibt daraus Hotspot-Aktionen, Dialoge und Zwischensequenzen und führt den Validator aus.
6. **Im Spiel prüfen:** Hot Reload lädt jede Änderung am aktuellen Spielzustand (FA-DEV-08). Dialoge und Sequenzen lassen sich direkt starten (FA-DEV-13, FA-DEV-14). Der Inhaltsgraph zeigt, wo Flags und Gegenstände gesetzt und gelesen werden (FA-DEV-12).
7. **Lösungsweg ergänzen:** Den neuen Abschnitt im Entwicklungsmodus durchspielen, der Rekorder schreibt die Schritte in `walkthrough.json`, Checkpoints per Knopf (FA-DEV-11).
8. **PR:** Validator und Lösungsweg-Test laufen im Gate (NF-V-01, NF-V-02). Freigabe nach der Freigaberegel in den [Entscheidungen](../entscheidungen.md), nie durch den Autor (EP-03).

## Vorlage Prosa-Beschreibung

Creative beschreibt einen Raum so, ein Agent übersetzt ihn in JSON nach dem [Asset-Vertrag](asset-vertrag/README.md). Unklare Stellen fragt der Agent nach, statt sie zu erfinden.

```
Raum: <raum-id>
Kurzbeschreibung: <1–2 Sätze>

Hotspots (je einer):
- hotspot-<name> „<Anzeigename>“
  Ansehen: <Text>
  Weitere Verben: <Nehmen/Benutzen/Öffnen/Reden: was passiert>
  Gegenstand anwenden: <Gegenstand> → <was passiert>
  Bedingungen: <z. B. nur wenn X schon passiert ist>
  Ausgang: <Zielraum, Eintrittspunkt, ggf. Bedingung>

Gegenstände im Raum: <Gegenstand, ungefähre Lage, Alchemie oder Quest>
Figuren im Raum: <Figur, ungefähre Lage, worüber man reden kann>
Dialoge: <Skizze: Begrüßung, Optionen, was eine Option auslöst>
Zwischensequenzen: <wann, was passiert>
Beim Betreten: <einmalige oder wiederkehrende Ereignisse>
```

Positionen beschreibt Creative nur grob. Die genauen Koordinaten setzt Creative danach im Raum-Overlay.

## Werkzeuge

| ID | Werkzeug | Art | Ergebnis |
|---|---|---|---|
| FA-DEV-07 | Validator im Watch-Modus | Overlay im Spiel | Fehlercode und Datei sichtbar |
| FA-DEV-08 | Hot Reload von `content/` | Entwicklungs-Build | Änderung sichtbar, Spielzustand bleibt |
| FA-DEV-09 | Gerüst-Generator | `make new-room`, `make new-character`, `make new-item`, `make new-recipe` | vertragskonforme Startdateien |
| FA-DEV-10 | Raum-Overlay | Overlay im Spiel, schreibend | Koordinaten in `room.json`, Drehpunkte in `character.json` |
| FA-DEV-11 | Lösungsweg-Rekorder | Entwicklungsmodus | `walkthrough.json` mit Checkpoints |
| FA-DEV-12 | Inhaltsgraph | Skript, nur lesend | Graph: wo jedes Flag und jeder Gegenstand gesetzt und gelesen wird, Dialogverläufe |
| FA-DEV-13 | Dialog direkt starten | URL-Parameter `?dialog=<id>&node=<knoten>` | Dialog am gewählten Knoten |
| FA-DEV-14 | Zwischensequenz ab Schritt | URL-Parameter `?cutscene=<id>&step=<n>` | Sequenz ab Schritt n |
| FA-DEV-15 | Figuren-Vorschau | Seite im Entwicklungsmodus | alle Animationen je Ansicht abspielbar |

**Agenten-Skills** (Projektdateien, keine FA): „Raum aus Prosa-Beschreibung anlegen“, „Dialog anlegen“, „Zwischensequenz anlegen“, „Animation anlegen“. Jeder Skill liest den Asset-Vertrag, schreibt nur unter `content/` und endet mit dem Validator-Lauf.

**Schreibweg:** Werkzeuge im Browser schreiben über einen Endpunkt des Vite-Dev-Servers (`/__dev/content`). Er nimmt nur JSON-Dateien unter `content/` an und existiert nur im Entwicklungs-Build (FA-DEV-06). SVG-Dateien schreibt kein Werkzeug.

**Bewusst nicht gebaut:** Timeline-Editor für Zwischensequenzen, grafischer Dialog-Editor, eigenes Zeichenwerkzeug.

## Persona-Vorschlag P-04

Für Creative als Autor gibt es noch keine Persona. Vorschlag zur Aufnahme in die [Personas](../voranalyse/02-personas.md), Entscheidung durch den PO.

| | |
|---|---|
| Name | Robin, aus dem Creative-Team |
| Stakeholder / Rolle | SH-02 / SR-02 Entwickler |
| Steckbrief | Teammitglied in Creative, gestaltet Räume und Figuren mit Claude Design, schreibt keinen Code |
| Gerät | Desktop, Entwicklungs-Build, Claude Design im Browser |
| Arbeitsweise | Baut einen Raum vom Bild bis zum spielbaren Abschnitt, beschreibt Rätsel und Dialoge in Prosa, lässt einen Agenten das JSON schreiben |
| Ziel | Einen neuen Raum spielbar machen, ohne auf Entwickler zu warten |
| Frust | Koordinaten raten, Fehler erst im Review sehen, für jede Kleinigkeit neu laden und von vorn spielen |
| Zitat | „Ich will sehen, wo die Figur laufen kann, und es mit der Maus verschieben.“ |
| Treibt | FA-DEV-07 bis FA-DEV-15, NF-W-01, NF-V-01 |
