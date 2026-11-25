# Anforderungsvorschläge der Architektur

Stand 2026-11-21. Die Vorschläge mit vorläufiger ID (FA-E-02 bis FA-E-22, FA-DEV-07 bis FA-DEV-15) und die Änderungen an FA-E-05 und FA-E-07 stehen seit 2026-11-21 im [Katalog](../voranalyse/03-anforderungen.md), zusammen mit FA-G-09 bis FA-G-11 und EP-16 aus Issue #78 ([Entscheidungen](../entscheidungen.md)). Maßgeblich ist der Katalog.

Hier stehen nur noch Vorschläge, die der PO noch nicht entschieden hat. Format und Qualitätskriterien wie im Katalog. Erst nach Aufnahme in den Katalog entstehen Issues ([Issues aus Anforderungen](../prozess/issues-aus-anforderungen.md)).

## Ohne ID: Raumteile (Artstyle, Issue #1)

Stand 2026-11-20. Die Demo-Szene zum [Artstyle](../creative/artstyle.md) braucht Raumgrafik, die sich mit dem Zustand ändert, und Bewegung im Raum. Das Format steht im [Asset-Vertrag](asset-vertrag/raum.md). Die IDs vergibt der PO bei Aufnahme in den Katalog.

| ID | Bereich | Nutzerrolle | Anforderung | Akzeptanzkriterium |
|---|---|---|---|---|
| offen | Raumteile | Spieler | Das System muss jedes Raumteil mit `visibleIf` nur anzeigen, solange seine Bedingung erfüllt ist. | E2E-Test im Testraum: Nach Setzen des Flags wechselt die Anzeige innerhalb von 100 ms, angezeigte Teile mit nicht erfüllter Bedingung: 0. |
| offen | Raumanimation | Spieler | Das System muss jede Raumanimation in Schleife abspielen, solange ihr Teil sichtbar ist. | E2E-Test: Der Transform jedes animierten Teils ändert sich innerhalb von 500 ms. Ausgeblendete Teile: 0 laufende Animationen. |
