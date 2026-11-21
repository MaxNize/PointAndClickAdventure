# Anforderungsvorschläge der Architektur

Stand 2026-11-19. **Vorschlag, nicht Teil des Katalogs.** Maßgeblich bleibt [`03-anforderungen.md`](../voranalyse/03-anforderungen.md). Die IDs hier sind vorläufig. Der PO entscheidet im Planning am 26.11. zusammen mit Issue #78, was in den Katalog kommt ([Issues aus Anforderungen](../prozess/issues-aus-anforderungen.md), Schritt 1). Erst danach entstehen Issues.

Herkunft: [Engine-Konzept](engine-konzept.md) (E-02 bis E-22 der Architektur-Liste) und [Autoren-Workflow](autoren-workflow.md) (Werkzeuge für Creative). Format und Qualitätskriterien wie im Katalog. Unit-Tests laufen gegen den Kern, E2E-Tests im Referenz-Testraum. *Einheit* = viewBox-Einheit des Raums. *Akteur*, *Interaktionsziel*, *Anker*, *Basislinie*: siehe [Asset-Vertrag](asset-vertrag/README.md#begriffe).

## Abgleich mit Issue #78

| #78 | Hier | Umgang |
|---|---|---|
| FA-G-09 Aufnehmen | E-13 | #78 hat Vorrang. E-13 wird auf FA-G-09 abgebildet, keine eigene FA-E-13. **Hinweis fürs Planning:** Das Kriterium „Klick auf den Gegenstand“ passt nicht zum Eingabemodell. Aufnehmen läuft über Rechtsklick → „Nehmen“ ([Engine-Konzept](engine-konzept.md#eingabe)). |
| FA-G-10 Inventar | – | #78 hat Vorrang. FA-E-14 und FA-E-15 setzen ein Inventar voraus. |
| FA-G-11 Inhaltsformat Gegenstände | – | Das Format steht im [Asset-Vertrag](asset-vertrag/gegenstand.md). FA-G-11 wäre die zugehörige Prüfung. Prüfen, ob NF-V-01 sie schon abdeckt. |
| EP-16 Projektgerüst | – | Voraussetzung für Schritt 0 im [Umsetzungsplan](umsetzungsplan.md). Nicht zu verwechseln mit FA-DEV-09 (Gerüst für Inhaltsdateien). |

## Änderungen an bestehenden Anforderungen

Bei Annahme ändert sich der Wortlaut im Katalog. Die Issue-Texte von #24 und #25 werden im selben PR nachgezogen.

| ID | Issue | Bisher | Vorschlag | Grund |
|---|---|---|---|---|
| FA-E-05 | #24 | Anforderung: „… als anklickbare Hotspots registrieren.“ Kriterium: „E2E-Test: Ein Klick löst die hinterlegte Aktion aus.“ | Anforderung: „Das System muss SVG-Elemente mit ID-Präfix `hotspot-` als Interaktionsziele registrieren.“ Kriterium: „E2E-Test: Ein Rechtsklick auf jedes `hotspot-`-Element des Testraums öffnet das Kontextmenü genau dieses Hotspots.“ | Linksklick = laufen, Rechtsklick = Menü. Die Aktion selbst prüft FA-E-06. |
| FA-E-07 | #25 | Kriterium: „Endposition höchstens 2 px vom Klickpunkt entfernt.“ | Kriterium: „Endposition höchstens 2 Einheiten vom Klickpunkt entfernt.“ | Rückfrage zur Einheit beantwortet: viewBox-Einheiten. |

## Engine

| ID | Bereich | Nutzerrolle | Anforderung | Akzeptanzkriterium |
|---|---|---|---|---|
| FA-E-02 | Zeichenreihenfolge | Spieler | Das System muss alle Elemente zwischen Hinter- und Vordergrundebene nach ihrer Basislinie sortiert zeichnen. | Unit-Test: Zeichenreihenfolge im Testraum aufsteigend nach Basislinie, 0 Abweichungen. E2E-Test: Figur mit Fußpunkt unter der Basislinie einer Mittelebene liegt im DOM nach dieser Ebene. |
| FA-E-03 | Spielstart | Spieler | Das System muss ein neues Spiel im Startraum aus `game.json` beginnen. | E2E-Test: Nach dem Start ist `startRoom` aktiv, die Spielfigur steht höchstens 2 Einheiten vom Spawn `startSpawn` entfernt. |
| FA-E-04 | Platzierung | Spieler | Das System muss jeden sichtbaren Akteur an seiner Position aus der Raumdefinition anzeigen. | E2E-Test: Anker jedes Akteurs im Testraum höchstens 2 Einheiten von der Position entfernt. Akteure mit nicht erfüllter `visibleIf`-Bedingung: 0 angezeigt. |
| FA-E-06 | Kontextmenü | Spieler | Das System muss bei Rechtsklick auf ein Interaktionsziel ein Kontextmenü mit dessen Verben anzeigen. | E2E-Test je Interaktionsziel im Testraum: Einträge = „Ansehen“ + definierte Verben + Gegenstands-Eintrag bei nichtleerem Inventar. Auswahl eines Eintrags führt dessen Effekte aus. |
| FA-E-08 | Wegsuche | Spieler | Das System muss die Spielfigur auf einem Weg innerhalb der begehbaren Fläche führen. | Unit-Test mit Polygonen mit und ohne Löcher: 0 Wegsegmente außerhalb der Fläche. |
| FA-E-09 | Klick außerhalb | Spieler | Das System muss die Spielfigur nach einem Klick außerhalb der begehbaren Fläche zum nächstgelegenen Punkt der Fläche bewegen. | Unit-Test: Endposition höchstens 2 Einheiten vom nächstgelegenen Randpunkt entfernt. |
| FA-E-11 | Ansicht | Spieler | Das System muss die Ansicht einer laufenden Figur aus ihrer Laufrichtung wählen. | Unit-Test mit 8 Richtungen: Ansicht und Spiegelung wie im Engine-Konzept, 0 Abweichungen. |
| FA-E-12 | Figurenanimation | Spieler | Das System muss für jede Figur die Animation ihres aktuellen Zustands abspielen. | E2E-Test: stehen → `idle`, laufen → `walk`, sprechen → `talk`. Die Transforms der animierten Teile ändern sich innerhalb von 500 ms. |
| FA-E-13 | – | – | nicht vergeben, siehe FA-G-09 aus Issue #78 | – |
| FA-E-14 | Gegenstand anwenden | Spieler | Das System muss einen Inventar-Gegenstand auf ein Interaktionsziel anwenden. | Unit-Test: Mit Eintrag in `useItem` bzw. `give` laufen dessen Effekte, ohne Eintrag erscheint der Standardtext aus `game.json`. Deckt den Mechanismus hinter FA-G-02 und FA-G-08. |
| FA-E-15 | Kombinieren | Spieler | Das System muss zwei Inventar-Gegenstände kombinieren. | Unit-Test: Beide Reihenfolgen führen dieselben Effekte aus. Ohne Eintrag erscheint der Standardtext, alle Gegenstände bleiben unverändert (vgl. FA-G-04). |
| FA-E-17 | Bedingungen | Spieler | Das System muss eine bedingte Aktion nur bei erfüllter Bedingung ausführen. | Unit-Test je Bedingungstyp (`flag`, `hasItem`, `not`, `all`, `any`): erfüllt → `then`, nicht erfüllt → `else`, 0 Abweichungen. |
| FA-E-18 | Sprechtext | Spieler | Das System muss Sprechtext über der sprechenden Figur anzeigen. | E2E-Test: Textblase liegt oberhalb der Figur, Anzeigedauer nach Formel aus `game.json` ± 100 ms. |
| FA-E-19 | Dialog | Spieler | Das System muss Dialoge aus einer Dialogdefinition abspielen. | Unit-Test mit Testdialog: angebotene Optionen = Optionen mit erfüllter Bedingung. Die Auswahl folgt `next`, `end` beendet den Dialog. |
| FA-E-20 | Zwischensequenz | Spieler | Das System muss Zwischensequenzen ohne Spielereingabe abspielen. | Unit-Test: Schritte in Reihenfolge, Befehle außer `skip` während der Sequenz verworfen. Nach `skip` ist der Zustand gleich dem nach vollständigem Ablauf. |
| FA-E-21 | Speichern | Spieler | Das System muss den Spielstand im Ruhezustand im Browser speichern. | E2E-Test: Gespeicherter Zustand besteht die Schemaprüfung mit 0 Fehlern. Speichern während eines Dialogs liefert `save.busy`. |
| FA-E-22 | Spielende | Spieler | Das System muss nach dem Effekt `endGame` den Endbildschirm anzeigen. | E2E-Test ab Testzustand vor dem Ende: Endbildschirm sichtbar, Klicks auf den Raum lösen 0 Befehle aus. |

## Werkzeuge für Creative

Herkunft: [Autoren-Workflow](autoren-workflow.md), Persona-Vorschlag P-04. Alle nur im Entwicklungs-Build (FA-DEV-06).

| ID | Bereich | Nutzerrolle | Anforderung | Akzeptanzkriterium |
|---|---|---|---|---|
| FA-DEV-07 | Vertragsfehler anzeigen | Entwickler | Das System muss Verstöße gegen den Asset-Vertrag im laufenden Entwicklungs-Build anzeigen. | E2E-Test: Fehlerhafte Datei unter `content/` speichern → Overlay zeigt Fehlercode und Dateipfad innerhalb von 2 s. |
| FA-DEV-08 | Hot Reload | Entwickler | Das System muss geänderte Inhaltsdateien ohne Verlust des Spielzustands neu laden. | E2E-Test: `room.json` ändern → Änderung innerhalb von 2 s sichtbar, abweichende Zustandsfelder: 0. |
| FA-DEV-09 | Gerüst | Entwickler | Das System muss je Asset-Typ ein vertragskonformes Gerüst erzeugen. | Skript-Test für Raum, Figur, Gegenstand, Rezept: Erzeugtes Gerüst besteht den Validator mit 0 Fehlern. |
| FA-DEV-10 | Koordinaten setzen | Entwickler | Das System muss im Entwicklungsmodus gesetzte Koordinaten in die zugehörige Inhaltsdatei schreiben. | E2E-Test, zwei Fälle: (1) Polygonpunkt im Raum-Overlay verschieben, speichern → `room.json` enthält die neue Koordinate. (2) Drehpunkt in der Figuren-Vorschau verschieben, speichern → `pivots` in `character.json` enthält ihn. Je Fall: Validator 0 Fehler, geänderte Dateien außerhalb von `content/`: 0. |
| FA-DEV-11 | Lösungsweg aufzeichnen | Entwickler | Das System muss gespielte Befehle im Entwicklungsmodus als Lösungsweg aufzeichnen. | Aufzeichnung ohne Browser abspielen: abweichende Zustandsfelder gegenüber dem aufgezeichneten Endzustand: 0. |
| FA-DEV-12 | Inhaltsgraph | Entwickler | Das System muss aus den Inhaltsdateien einen Inhaltsgraphen erzeugen. | Skript-Test mit Testinhalt bekannter Verweise: Der Graph enthält je Flag und je Gegenstand die setzenden und lesenden Stellen sowie je Dialog alle Knoten und Übergänge. Fehlende Kanten: 0. Nie gesetzte Flags werden gemeldet. |
| FA-DEV-13 | Dialog starten | Entwickler | Das System muss einen Dialog über den URL-Parameter `?dialog=<id>&node=<knoten>` starten. | E2E-Test: Angezeigter Knoten = angegebener Knoten. Unbekannte ID: Fehlercode `content.ref-missing` sichtbar. |
| FA-DEV-14 | Sequenz ab Schritt | Entwickler | Das System muss eine Zwischensequenz über `?cutscene=<id>&step=<n>` ab Schritt n abspielen. | Unit-Test: Erster ausgeführter Schritt = n. Zustand entspricht dem nach `skip` der Schritte 0 bis n−1. |
| FA-DEV-15 | Figuren-Vorschau | Entwickler | Das System muss jede Animation einer Figur im Entwicklungsmodus je Ansicht abspielen. | E2E-Test: Anzahl abspielbarer Einträge = Anzahl Animation × Ansicht in `animations.json`. |

## Ohne ID: Raumteile (Artstyle, Issue #1)

Stand 2026-11-20. Die Demo-Szene zum [Artstyle](../creative/artstyle.md) braucht Raumgrafik, die sich mit dem Zustand ändert, und Bewegung im Raum. Das Format steht im [Asset-Vertrag](asset-vertrag/raum.md). Die IDs vergibt der PO bei Aufnahme in den Katalog.

| ID | Bereich | Nutzerrolle | Anforderung | Akzeptanzkriterium |
|---|---|---|---|---|
| offen | Raumteile | Spieler | Das System muss jedes Raumteil mit `visibleIf` nur anzeigen, solange seine Bedingung erfüllt ist. | E2E-Test im Testraum: Nach Setzen des Flags wechselt die Anzeige innerhalb von 100 ms, angezeigte Teile mit nicht erfüllter Bedingung: 0. |
| offen | Raumanimation | Spieler | Das System muss jede Raumanimation in Schleife abspielen, solange ihr Teil sichtbar ist. | E2E-Test: Der Transform jedes animierten Teils ändert sich innerhalb von 500 ms. Ausgeblendete Teile: 0 laufende Animationen. |

## Vorschau der Issues

Nach der Anleitung, Schritt 2: erst nach Aufnahme in den Katalog und Merge, Vorschau vorher an den PO. Typ `Story`, Label `story`, Bereich `Fullstack` für alle Zeilen. Titel = `<ID> <Bereich>`, z. B. `FA-E-06 Kontextmenü`.

„Blockiert durch“ steht nur dort, wo Anforderung oder Engine-Konzept die andere Funktion ausdrücklich voraussetzen. Alles andere ist ein Vorschlag zur Reihenfolge, zu prüfen, nicht erzwungen (wie in #24 und #25).

| ID | Titel | Blockiert durch | Vorschlag Reihenfolge (zu prüfen, nicht erzwungen) |
|---|---|---|---|
| FA-E-02 | FA-E-02 Zeichenreihenfolge | – | zuerst FA-E-01 |
| FA-E-03 | FA-E-03 Spielstart | – | zuerst FA-E-01 |
| FA-E-04 | FA-E-04 Platzierung | – | zuerst FA-E-01 |
| FA-E-06 | FA-E-06 Kontextmenü | FA-E-05 (Menü öffnet sich an registrierten Interaktionszielen) | – |
| FA-E-08 | FA-E-08 Wegsuche | – | zuerst FA-E-07 |
| FA-E-09 | FA-E-09 Klick außerhalb | – | zuerst FA-E-07 |
| FA-E-11 | FA-E-11 Ansicht | – | zuerst FA-E-07 |
| FA-E-12 | FA-E-12 Figurenanimation | – | zuerst FA-E-11 |
| FA-E-14 | FA-E-14 Gegenstand anwenden | FA-E-06 (Menüeintrag „Gegenstand benutzen …“), FA-G-10 (Inventar, #78) | – |
| FA-E-15 | FA-E-15 Kombinieren | FA-G-10 (Inventar, #78) | – |
| FA-E-17 | FA-E-17 Bedingungen | – | – |
| FA-E-18 | FA-E-18 Sprechtext | – | – |
| FA-E-19 | FA-E-19 Dialog | – | zuerst FA-E-18 |
| FA-E-20 | FA-E-20 Zwischensequenz | – | zuerst FA-E-17 |
| FA-E-21 | FA-E-21 Speichern | – | – |
| FA-E-22 | FA-E-22 Spielende | – | – |
| FA-DEV-07 | FA-DEV-07 Vertragsfehler anzeigen | NF-V-01 (zeigt Validator-Ergebnisse) | – |
| FA-DEV-08 | FA-DEV-08 Hot Reload | – | zuerst FA-E-01 |
| FA-DEV-09 | FA-DEV-09 Gerüst | NF-V-01 (Kriterium prüft mit dem Validator) | – |
| FA-DEV-10 | FA-DEV-10 Koordinaten setzen | – | zuerst FA-E-01 |
| FA-DEV-11 | FA-DEV-11 Lösungsweg aufzeichnen | – | zuerst NF-V-02 |
| FA-DEV-12 | FA-DEV-12 Inhaltsgraph | – | zuerst NF-V-01 |
| FA-DEV-13 | FA-DEV-13 Dialog starten | FA-E-19 (startet einen Dialog) | – |
| FA-DEV-14 | FA-DEV-14 Sequenz ab Schritt | FA-E-20 (startet eine Sequenz) | – |
| FA-DEV-15 | FA-DEV-15 Figuren-Vorschau | FA-E-12 (spielt Animationen ab) | – |
