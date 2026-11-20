# Charaktere und Animationen ansehen

In diesem Ordner liegen die Figuren für das Spiel: SVGs, Laufanimationen und Dialoge. Für jede Figur gibt es eine HTML-Vorschau. Sie zeigt alle Ansichten und Animationen auf einer Seite.

Die Regeln für Zeichenstil, Farben und Profile stehen im [Styleguide](STYLEGUIDE_Charaktere.md).

## Vorschau in VS Code öffnen

1. Öffne im Explorer links die Vorschau-Datei der Figur (Liste unten).
2. Klick mit der rechten Maustaste auf die Datei.
3. Wähle **Open With…** (bzw. **Öffnen mit…**).
4. Wähle **Integrated Browser**.

Die Seite öffnet sich als Tab in VS Code. Die Animationen laufen sofort.

Alle Grafiken sind in die HTML-Dateien eingebettet. Du brauchst keinen Server und keine Erweiterung.

**Tipp:** Zieh den Tab neben den Code, dann siehst du Quelle und Ergebnis gleichzeitig. Nach einer Änderung lädst du den Tab neu, damit du das neue Ergebnis siehst.

## Vorschauen

| Figur | Vorschau |
|---|---|
| Alchemistin (Demo-Szene) | [Akademie der Alchemie – Demo-Szene(1).html](Alchemistin/Akademie%20der%20Alchemie%20–%20Demo-Szene(1).html) |
| Alchemistin (Akademie) | [index.html](Alchemistin/akademie-der-alchemie/akademie-der-alchemie/index.html) |
| Lehrling | [lehrling_vorschau.html](Lehrling/lehrling/lehrling/lehrling_vorschau.html) |
| Lehrling (Laufanimation) | [Lehrling – Charakter & Laufanimation.html](Lehrling/Lehrling%20–%20Charakter%20&%20Laufanimation.html) |
| Meister | [meister_vorschau.html](meister/meister/meister_vorschau.html) |
| Erzalchemist | [erzalchemist_vorschau.html](erzalchemist/erzalchemist/erzalchemist_vorschau.html) |
| Schmied | [schmied_vorschau.html](schmied/schmied/schmied_vorschau.html) |
| Professor | [professor_vorschau.html](professor/professor_vorschau.html) |
| NPCs (alle zehn) | [npc_vorschau.html](npcs/npc_vorschau.html) |

Die Dateien `scene_template.html` in den `source/`-Ordnern sind Vorlagen für die Generator-Skripte und keine Vorschauen.

## Falls „Integrated Browser“ fehlt

Ältere VS-Code-Versionen haben den Eintrag noch nicht. Dann hast du zwei Möglichkeiten:

- VS Code aktualisieren (**Hilfe → Nach Updates suchen**).
- Die Datei im normalen Browser öffnen: Rechtsklick → **Reveal in File Explorer** und dort doppelklicken.
