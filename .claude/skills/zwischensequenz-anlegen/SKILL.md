---
name: zwischensequenz-anlegen
description: Eine Zwischensequenz für das Adventure aus einer Beschreibung von Creative anlegen (content/cutscenes/<id>.json) und auslösen lassen. Verwenden, wenn jemand eine kleine Szene ohne Spielereingabe beschreibt, z. B. Figur läuft herein, sagt etwas, etwas verändert sich, oder „Zwischensequenz anlegen“ sagt.
---

# Zwischensequenz anlegen

Eine Zwischensequenz ist eine Effektliste, die ohne Eingabe abläuft. Format: [Asset-Vertrag: Zwischensequenz](../../../docs/architektur/asset-vertrag/aktionen.md#zwischensequenz).

## Regeln

- Schreibe nur unter `content/`. Kein Code, keine Doku, keine Gate-Dateien.
- Texte und Ablauf kommen von Creative. Fehlt etwas, frag nach.
- Nur das Vokabular aus [Aktionen](../../../docs/architektur/asset-vertrag/aktionen.md). Kameras, Überblendungen oder Musik gibt es nicht. Sag das, statt es nachzubauen.
- IDs: Kleinbuchstaben, Ziffern, Bindestrich, Umlaute als `ae`, `oe`, `ue`, `ss`.
- Du bist fertig, wenn `npm run validate` 0 Fehler meldet.

## Aufbau

- Datei `content/cutscenes/<sequenz-id>.json`, `steps` ist eine Effektliste.
- Typische Schritte: `walkTo` mit `character`, `face`, `say` mit `speaker`, `wait`, `playAnimation`, `setFlag`, `changeRoom`.
- Ohne `character` bzw. `speaker` wirkt ein Schritt auf die Spielfigur.
- **Überspringen:** Der Spieler kann jede Sequenz überspringen. Dann gelten alle Zustandsänderungen sofort (Flags, Inventar, Positionen), Texte entfallen. Nichts Wichtiges darf nur in einem Text stehen, das der Spieler danach noch wissen muss. Setz dafür ein Flag, das später eine Rückfrage oder einen Hinweis ermöglicht.
- Am Ende ein `setFlag` wie `<sequenz-id>-gesehen`, wenn die Sequenz nur einmal laufen soll.

## Ablauf

1. **Lesen:** [aktionen.md](../../../docs/architektur/asset-vertrag/aktionen.md), den Raum, die beteiligten Figuren (stehen sie im Raum?), vorhandene Flags (`grep -r '"flag"' content`).
2. **Schreiben:** die Sequenz.
3. **Auslösen:** mit `{ "type": "startCutscene", "cutscene": "<sequenz-id>" }` an der Stelle, die Creative beschreibt: `onEnter` des Raums, ein Verb, ein Dialog. Einmalig mit `if` und dem Gesehen-Flag.
4. **Prüfen:** `npm run validate`.
5. **Bericht an Creative:** Datei, Schritte als kurze Liste, Auslöser, neue Flags, offene Fragen.

## Was das Spiel schon kann

Der Validator prüft Form und Verweise. Abspielen kommt mit FA-E-20, ab einem Schritt starten mit FA-DEV-14.
