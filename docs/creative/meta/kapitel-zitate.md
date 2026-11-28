# Kapitelzitate

Meta-Vorgabe für alle Kapitel ([09-kapitel.md](../story/09-kapitel.md)). Angelegt am 2026-11-28 auf Wunsch von Fabian, überarbeitet am selben Tag. Das Konzept ist festgelegt. Die Beispielzitate unten sind nur Entwürfe.

## Vorgabe (festgelegt)

Jedes Kapitel beginnt mit einem poetischen Zitat.

- **Im ersten Durchgang** wirkt das Zitat rätselhaft oder einfach nur schön. Der Spieler denkt: „Was soll das Zitat?“
- **Im erneuten Durchspielen** bekommt es eine andere Bedeutung. Der Spieler kennt jetzt den Twist, liest dasselbe Zitat neu und denkt: „Das stand schon am Anfang da.“
- **Das Spiel zeigt die Zitate am Ende nicht noch einmal** und erklärt sie nie. Die zweite Bedeutung findet nur, wer erneut spielt und selbst wieder hinsieht.

## Warum das zum Spiel passt

Der Twist des Spiels funktioniert genauso: Ersetzte Freunde, das Angebot im Finale und der Meteor sind von Anfang an sichtbar und werden erst mit Wissen lesbar ([08-enden-und-hinweise.md](../story/08-enden-und-hinweise.md)). Die Zitate sind ein weiterer stiller Hinweis, der den zweiten Durchgang belohnt. Wer nur einmal spielt, verpasst nichts, denn das Zitat ist dann einfach Stimmung.

## Regeln für jedes Zitat

1. **Zwei Lesarten.** Die *erste Lesart* klingt harmlos oder schön, passt aber nicht klar zum Kapitel. Die *zweite Lesart* ergibt sich erst mit Wissen über den Twist. Beide werden schriftlich festgehalten (siehe Vorlage).
2. **Der erste Durchgang bleibt ohne Deutung gut.** Das Zitat muss für sich stehen können, ohne zu frustrieren oder wie ein ungelöstes Rätsel zu wirken. Es ist Atmosphäre, kein Rätsel.
3. **Kein Spoiler.** Wer das Zitat im ersten Durchgang liest, darf nichts über den Twist ahnen. Rätselhaft heißt nicht „Warnung“.
4. **Die zweite Lesart ist im Spiel verankert.** Sie muss zu Dingen passen, die der Spieler im Spiel selbst sieht und hört, also zu Figuren, Orten, Dialogen und dem Ende. Wer es zum zweiten Mal spielt, kann sie finden, ohne die Doku gelesen zu haben.
5. **Kurz.** Ein bis vier Zeilen, auf einen Blick lesbar.
6. **Poetisch, nicht erklärend.** Bilder statt Aussagen. Kein Zitat sagt „Vorsicht, X ist ein Homunkulus“.
7. **Erfunden und eingeordnet.** Die Zitate stammen aus der Spielwelt (Pilgerlied, Kinderreim, Akademiespruch, Notiz einer Figur) und nicht von realen Dichtern. Die Quelle selbst darf ein Hinweis sein.
8. **Passend zu den Themen der Story:** Abhängigkeit, Seele als Preis, Fäden und Strippenzieher, Wert und Sinn ([01-kernidee-und-twist.md](../story/01-kernidee-und-twist.md), KI-14).
9. **Jedes Zitat gehört zu seinem Kapitel.** Die zweite Lesart bezieht sich auf das, was in diesem Kapitel geschieht oder verborgen ist, nicht nur auf die Welt im Allgemeinen.

## Vorlage pro Kapitel

| Punkt | Inhalt |
|---|---|
| Kapitel | Name aus [09-kapitel.md](../story/09-kapitel.md) |
| Zitat | der Text, wie er im Spiel steht |
| Quelle | wer es in der Spielwelt gesagt oder geschrieben hat |
| Erste Lesart | was der Spieler im ersten Durchgang versteht |
| Zweite Lesart | was es mit Wissen über den Twist bedeutet |
| Bezug im Kapitel | welche Szene, Figur oder welcher Ort die zweite Lesart trägt |
| Spoiler-Check | verrät das Zitat im ersten Durchgang etwas? (ja/nein, wenn ja: ändern) |

## Entwürfe (Beispiele, nicht festgelegt)

Die Zahl der Kapitel steht noch nicht fest (KA-01). Die Beispiele zeigen nur, wie ein Zitat aussehen kann. Die Arten der Rettung stammen aus dem Vorschlag in KA-02 und sind ebenfalls offen.

### Beispiel A: Kapitel mit unbewusster Rettung

> „Wer die Tür nur anlehnt, hat sie noch nicht geschlossen.“
> *Hausspruch der Akademie*

| Punkt | Inhalt |
|---|---|
| Erste Lesart | Ein Spruch über Gastfreundschaft oder Schlamperei. |
| Zweite Lesart | Eine kleine, unbedachte Tat des Spielers hat in diesem Kapitel eine Tür offen gelassen. Wer weiß, dass hier jemand unbemerkt ersetzt werden sollte, sieht: Die Rettung war nie gewollt, aber möglich, weil nichts abgeschlossen wurde. |
| Bezug im Kapitel | die Tür, die der Spieler im Kapitel nicht schließt |
| Spoiler-Check | nein |

### Beispiel B: Kapitel mit Werwolf (Entlarven)

> „Ich kenne dein Gesicht so gut, dass ich es nie ansehe.“
> *Brief, ohne Absender*

| Punkt | Inhalt |
|---|---|
| Erste Lesart | Ein liebevoller oder verbitterter Brief an einen Vertrauten. |
| Zweite Lesart | Wer einen Menschen zu gut zu kennen glaubt, prüft ihn nicht mehr. Der Homunkulus fällt nur auf, wenn man genau hinsieht (EN-01). |
| Bezug im Kapitel | die Figur, der der Spieler von Anfang an vertraut |
| Spoiler-Check | nein, der Satz passt zu jeder Freundschaft |

### Beispiel C: Kapitel mit direkter Rettung

> „Das Feuer fragt nicht, wer es zuerst gerufen hat.“
> *Pilgerlied, dritte Strophe*

| Punkt | Inhalt |
|---|---|
| Erste Lesart | Ein frommes Lied über die Wärme des Meteors. |
| Zweite Lesart | Das Incendium ist ein Feuer, das jeden verbrennt, der von ihm abhängt, auch den, der es nur gerufen hat (KI-02). |
| Bezug im Kapitel | die Szene, in der der Spieler vor der Wahl steht, einen Splitter zu benutzen |
| Spoiler-Check | nein, es klingt nach Glauben und nicht nach Warnung |

## Umsetzung (Hinweis für die Architektur)

Zitate sind Inhalt und kommen nur als Daten ins Spiel (NF-W-01):

- Zitat und Quelle stehen im Kapitel-JSON als Text, ohne Codeänderung.
- Die Anzeige am Kapitelanfang ist eine Engine-Funktion (Textkarte vor dem ersten Raum). Gibt es sie noch nicht, ist das ein Story-Vorschlag an die Architektur.
- Das Spiel braucht keinen Zustand dafür. Das Zitat steht am Kapitelanfang, und weder Finale noch Epilog greifen es auf.

## Offene Fragen

- [ ] **ME-01 Sollen die Zitate zusammen ein Gedicht ergeben?**
  Warum wichtig: Ein verteiltes Gedicht belohnt den zweiten Durchgang zusätzlich, weil man die Zeilen dann hintereinander liest. Es darf aber im ersten Durchgang nichts verraten und muss auch ohne eine Zeile lesbar bleiben (Projektvorgabe: keine Sackgassen, P-02).
  Optionen: A) ein eigenes, einzeln stehendes Zitat pro Kapitel, B) die Zitate bilden zusammen ein Gedicht, C) einzelne Zitate, die lose zusammenpassen.
  Vorschlag: A. Es ist am einfachsten, und jedes Zitat kann eine eigene zweite Lesart tragen.
  Antwort: offen
