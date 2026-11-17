# Engine-Konzept

Vorgabe der Architektur (PR-03), eingegangen 2026-11-17. Die Anforderungen daraus stehen mit neuen IDs in [Anforderungen](../voranalyse/03-anforderungen.md). Die Zuordnung steht unten.

## Überblick

Das Spiel ist eine Webanwendung mit React, TypeScript und Vite. Jeder Raum wird als einzelnes `<svg>` gerendert (viewBox 1920×1080, 16:9 skalierend). Eine JSON-Raumdefinition beschreibt den Raum vollständig und wird mit Zod validiert. Sie verweist auf die SVG-Ebenen und enthält:

- das Polygon der begehbaren Fläche,
- die Tiefenskalierung,
- die Ausgänge,
- die Hotspot-Aktionen.

| Baustein | Umsetzung |
|---|---|
| Hotspots | SVG-Elemente mit ID-Präfix `hotspot-` |
| Bewegung | A*-Wegsuche im Polygon der begehbaren Fläche |
| 2,5D-Effekt | Skalierung nach y-Position, Zeichenreihenfolge nach Fußpunkt |
| Figuren | SVGs mit benannten Gruppen, animiert mit GSAP |
| Spiellogik | reines TypeScript in `src/engine/core` |
| Darstellung | React stellt nur dar. Ereignisse gehen über einen typisierten Event-Bus an andere Module. |
| Erweiterung | Neue Räume, Figuren, Gegenstände und Animationen kommen ausschließlich über SVG- und JSON-Dateien ins Spiel, ohne Codeänderung. |

## Inhalte einbinden

| Inhalt | Dateien | Verknüpfung |
|---|---|---|
| Raum | SVG-Ebenen plus JSON-Raumdefinition (Ebenen, begehbare Fläche, Tiefenskalierung, Ausgänge, Hotspots, platzierte Figuren und Gegenstände) | – |
| Figur | SVG mit benannten Gruppen (z. B. `#kopf`, `#arm-links`) und Fußpunkt als Anker, plus JSON-Figurdefinition (ID, Name, SVG-Datei, Laufgeschwindigkeit, Animationen) | Raumdefinition setzt die Figur per ID an eine Startposition |
| Gegenstand | SVG für den Raum, SVG-Icon fürs Inventar, Eintrag in `items.json` (ID, Name, Beschreibung) | Raumdefinition platziert per ID. Beim Aufnehmen setzt die Engine ein Flag und meldet ein Event ans Inventar. |
| Animation | JSON je Figur mit benannten Animationen, mindestens `idle`, `walk`, `talk`. Keyframes wenden Rotation und Verschiebung auf benannte SVG-Gruppen an. | GSAP spielt sie ab |

## Zuordnung der Architektur-IDs

| Architektur | Projekt-ID | Anmerkung |
|---|---|---|
| E-01 | FA-E-01 | übernommen |
| E-05 | FA-E-05 | übernommen |
| E-07 | FA-E-07 | übernommen, Rückfrage zur Einheit (siehe [Offene Fragen](../offene-fragen.md)) |
| E-10 | FA-E-10 | übernommen |
| E-16 | FA-E-16 | übernommen |
| N-01 | NF-W-01 | ersetzt die bisherige Fassung. Eingeordnet unter Wartbarkeit statt Akzeptanz, weil es um Erweiterbarkeit geht. |
| N-04 | NF-V-04 | übernommen |
| N-06 | NF-E-02 | übernommen, manuelle Messung |
| N-07 | NF-E-03 | übernommen, Rückfrage zu den Messbedingungen |
| N-11 | NF-W-02 | zusammengeführt. „React- oder DOM-APIs“ verstößt gegen die Regel „keine und/oder-Ketten“, daher „Browser-Abhängigkeiten“ mit Liste im Akzeptanzkriterium. |

Die Architektur-IDs haben Lücken (E-02 bis E-04 usw.). Sobald die vollständige Liste vorliegt, wird sie hier zugeordnet.
