---
name: dialog-anlegen
description: Einen Dialog für das Adventure aus einer Skizze von Creative anlegen oder ändern (content/dialogs/<id>.json) und an eine Figur oder einen Hotspot anschließen. Verwenden, wenn jemand ein Gespräch, Dialogoptionen, Antworten einer Figur oder „Dialog anlegen“ beschreibt.
---

# Dialog anlegen

Creative skizziert ein Gespräch: wer spricht, welche Optionen der Spieler hat, was eine Option auslöst. Du schreibst daraus einen Dialog nach [Asset-Vertrag: Dialog](../../../docs/architektur/asset-vertrag/aktionen.md#dialog).

## Regeln

- Schreibe nur unter `content/`. Kein Code, keine Doku, keine Gate-Dateien.
- Die Texte kommen von Creative. Fehlen Zeilen, frag nach oder schreib einen klar markierten Vorschlag (`„[Vorschlag] …“`) und nenn ihn im Bericht.
- Nur das Vokabular aus [Aktionen](../../../docs/architektur/asset-vertrag/aktionen.md). Was fehlt, ist eine neue Engine-Funktion. Sag das, statt es nachzubauen.
- IDs: Kleinbuchstaben, Ziffern, Bindestrich, Umlaute als `ae`, `oe`, `ue`, `ss`.
- Du bist fertig, wenn `npm run validate` 0 Fehler meldet.

## Aufbau

```json
{
  "schemaVersion": 1,
  "id": "schmied-begruessung",
  "start": "hallo",
  "nodes": {
    "hallo": {
      "lines": [{ "speaker": "schmied", "text": "Na, auch mal hier?" }],
      "options": [
        { "id": "schwert", "text": "Hast du ein Schwert?", "if": { "not": { "flag": "schwert-gefragt" } }, "next": "schwert" },
        { "id": "tschuess", "text": "Tschüss.", "end": true }
      ]
    },
    "schwert": {
      "lines": [{ "speaker": "schmied", "text": "Nicht für dich." }],
      "effects": [{ "type": "setFlag", "flag": "schwert-gefragt" }],
      "options": [{ "id": "tschuess", "text": "Schade. Tschüss.", "end": true }]
    }
  }
}
```

- Datei `content/dialogs/<dialog-id>.json`, `id` gleich Dateiname. Pflicht sind `schemaVersion: 1`, `id`, `start` und `nodes`. Jede Option braucht eine `id`, eindeutig im Knoten.
- **Namen** (Vorschlag, bis Creative eine Konvention festlegt): Dialog `<figur-id>-<anlass>`, z. B. `schmied-begruessung`. Knoten nach Inhalt (`hallo`, `nach-dem-schwert-fragen`), nicht `n1`, `n2`. Flags nach dem, was passiert ist: `<thema>-gefragt`, `von-<sache>-gehoert`.
- `lines`: `speaker` ist eine Figur-ID oder `player` für die Spielfigur. Mindestens eine Zeile je Knoten, eine Zeile je Sprechblase, kurz halten.
- `options`: Jede Option hat entweder `next` (weiter zu einem Knoten) oder `end: true`. Optionen mit `if` erscheinen nur, wenn die Bedingung erfüllt ist.
- `effects` am Knoten laufen nach den Zeilen, `effects` an der Option nach der Wahl. Typisch: `setFlag` für „davon gehört“, `addItem` für Geschenke.
- **Jeder Knoten muss vom Start erreichbar sein, und von jedem Knoten muss ein Ende erreichbar sein.** Das prüft der Validator, aber **ohne die `if`-Bedingungen**. Deshalb: Die Option zum Gehen hat in jedem Knoten **nie** ein `if`. Dann gibt es bei jedem Spielstand einen Ausgang.
- **Rücksprünge** (`next` auf einen früheren Knoten) sind erlaubt, spielen aber dessen Zeilen erneut ab. Spring also nicht auf die Begrüßung zurück, sondern auf einen Knoten mit kurzer Überleitung (z. B. `noch-etwas` mit „Noch was?“), der dieselben Optionen anbietet.

**Noch offen im Vertrag** (nicht darauf bauen, im Bericht nennen, falls betroffen):
- Ob die `if` der Optionen vor oder nach den `effects` desselben Knotens ausgewertet werden. Lass die Optionen eines Knotens nicht von Flags abhängen, die derselbe Knoten setzt.
- Ob die Spielfigur den Text der gewählten Option selbst ausspricht. Wiederhole ihn nicht zusätzlich als `player`-Zeile.

## Ablauf

1. **Lesen:** [aktionen.md](../../../docs/architektur/asset-vertrag/aktionen.md), die beteiligten Figuren unter `content/characters/` und den Raum, in dem die Figur steht.
2. **Flags abgleichen:** `grep -r '"flag"' content`. Nutze vorhandene Flags, statt neue mit ähnlicher Bedeutung zu erfinden.
3. **Schreiben:** den Dialog nach dem Aufbau oben.
4. **Anschließen:** In `room.json` unter `characters` beim Eintrag der Figur: `verbs.talk: [{ "type": "startDialog", "dialog": "<dialog-id>" }]`. Bei einem Hotspot genauso unter seinen Verben. Gibt es mehrere Dialoge je nach Spielstand, wähle mit `if` und Bedingung.
5. **Prüfen:** `npm run validate`. Typische Fehler: `dialog.unreachable`, `dialog.no-end`, `content.flag-never-set`, `content.ref-missing`. Danach von Hand: Gehe jeden Knoten für jede Kombination der Flags durch, die seine Optionen lesen, und prüfe, dass mindestens eine Option erscheint.
6. **Bericht an Creative:** Datei, Knoten als kurze Liste (Knoten → Optionen → Ziel), neue Flags, Textvorschläge, offene Fragen.

## Was das Spiel schon kann

Der Validator prüft Form, Verweise, Flags und den Knotengraphen, die Bedingungen der Optionen aber nicht. Abspielen im Spiel kommt mit FA-E-19, direkt starten zum Testen mit FA-DEV-13.
