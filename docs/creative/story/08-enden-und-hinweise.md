# Enden und Hinweise

Woran der Spieler den Austausch merken kann, wann er als „bemerkt“ gilt und was das für Inhalte und Engine bedeutet.

## Was der Scherenschnitt zeigt

Im Spiel sind Figuren dunkle Silhouetten. Sichtbar bleiben nur der Umriss, Glanzpunkte, Gläser, Tränke und die eigene Leuchtfarbe ([Styleguide 8](../temp/STYLEGUIDE_Charaktere.md)). Der Umriss eines Homunkulus ist gleich. Hinweise müssen deshalb über die übrigen Kanäle laufen.

| Kanal | Möglicher Hinweis | Umsetzung |
|---|---|---|
| Leuchtfarbe | wird zur Farbe des Meteors, verblasst oder fehlt | anderes Figuren-SVG oder CSS-Klasse |
| Glanzpunkt im Auge | fehlt | eigene SVG-Variante |
| Gang | gleichförmig, alle Homunkuli haben denselben `WALK_STYLE` | Laufstil in JSON |
| Dialog | Sätze wiederholen sich, Gemeinsames ist vergessen, Gewohnheiten fehlen | Dialog-JSON |
| Verhalten | steht am falschen Ort, isst nicht, ist nachts wach | Raum-JSON |
| Umgebung | Spiegelbild fehlt, Tiere fliehen, Licht flackert in der Nähe | Raum-SVG |
| Gegenstände | ein persönlicher Gegenstand fehlt oder liegt verlassen herum | Gegenstand-JSON |

**Zusätzlicher stiller Hinweis (Fabian, 2026-11-28):** Das Zitat am Anfang jedes Kapitels. Es wirkt im ersten Durchgang wie Stimmung und liest sich beim zweiten Durchgang mit Wissen über den Twist neu. Es wird nie erklärt und am Ende nicht wiederholt. Details: [meta/kapitel-zitate.md](../meta/kapitel-zitate.md).

## Fragen zu den Hinweisen

- [ ] **EN-01 Welche Kanäle nutzen wir?**
  Vorschlag: Dialog und Gang für alle Homunkuli, dazu ein einziger visueller Hinweis (z. B. fehlender Glanzpunkt im Auge). Der Spieler soll eine Regel lernen können, die für alle gilt.
  Antwort: offen

- [ ] **EN-02 Wie subtil?**
  Optionen: A) nur für sehr aufmerksame Spieler, B) beim zweiten Mal Hinsehen erkennbar, C) es wird schrittweise deutlicher, je mehr Personen ersetzt sind.
  Vorschlag: C. Der erste Austausch ist kaum zu merken, der letzte fast offensichtlich. Das ist fair für P-01 und reizvoll für P-02.
  Antwort: offen

- [ ] **EN-03 Gibt es im Spiel einen Moment, der die Regel lehrt?**
  Beispiel: In einer Unterrichtsstunde zeigt Professor Gernegroß einen Versuchs-Homunkulus (eine Ratte, eine Puppe) und dessen fehlendes Licht. Der Spieler kennt das Merkmal dann, ohne zu wissen, dass er es später braucht.
  Vorschlag: Ja. So bleibt der Twist fair.
  Antwort: offen

## Wann gilt es als „bemerkt“?

- [x] **EN-04 Was muss der Spieler tun?**
  Stand (Benedict, 2026-11-20): Die Spielfigur kann das schlechte Ende abwenden, indem sie ihre Freunde rettet. Weitgehend unabhängige Kapitel, in denen man rettet oder nicht rettet.
  Ergänzung (Benedict, 2026-11-20): Es müssen nicht nur Freunde sein, und Kapitel können unterschiedlich funktionieren. Beispiel: ein Kapitel nach Art von *Werwolf* (EN-19).
  Entschieden (Benedict, 2026-11-20): Es gibt keine „normalen“ Kapitel. Jedes hat einen eigenen Aufbau. Teils rettet man jemanden unbewusst durch kleine Taten, der sonst unbemerkt ersetzt würde. Teils kann man direkt eingreifen. Ausarbeitung pro Kapitel: [09-kapitel.md](09-kapitel.md).
  Vorschlag war: Der Spieler bemerkt die Hinweise und löst rechtzeitig ein Rätsel. Verpasst er das, läuft das Kapitel trotzdem weiter, und die Person ist ab dann ein Homunkulus.
  Ursprüngliche Optionen:
  - A) **Passiv:** Er hat genug Hinweise gesehen (Gespräche geführt, Gegenstände untersucht).
  - B) **Aktiv:** Er beschuldigt am Ende die richtige Person oder benennt die Homunkuli.
  - C) **Beides:** Hinweise sammeln öffnet erst die Möglichkeit, aktiv zu handeln. *(Vorschlag)*
  Bei C: Wie viele Hinweise reichen? Alle, die meisten, eine feste Zahl?

- [ ] **EN-05 Was passiert im guten Ende?**
  Stand (2026-11-20): Es muss etwas passieren, „nichts passiert“ ist zu langweilig (Benedict). Ernte als gutes Ende ist ein KI-Vorschlag (EN-14).
  Offen: Details. Vorschlag: Alles transmutierte Gold zerfällt, der Meteor auch, die Zivilisation ist über Nacht arm, aber alle leben. Genommene Seelen kommen frei, auch die Erinnerungen, die die Spielfigur für Splitter hergegeben hat.
  Antwort: offen

- [x] **EN-06 Was passiert im schlechten Ende?**
  Antwort (Benedict, 2026-11-20): Midas. Es wirkt verlockend: Der Strippenzieher verspricht der Spielfigur im Auftrag des Wesens unvorstellbaren Reichtum für ihre Seele. Das ist nicht gelogen, nur eine Halbwahrheit, denn danach wird alles zu Gold. Nicht nur die Stadt, sondern die ganze Zivilisation, die auf dem Meteor aufgebaut wurde.
  Offen: Was genau Midas auslöst, siehe EN-18.

- [ ] **EN-07 Gibt es nur zwei Enden oder Zwischenstufen?**
  Beispiel: Strippenzieher gestellt, aber nicht alle Opfer gerettet.
  Vorschlag: Zwei Enden mit einer Schwelle (eine Mindestzahl Geretteter). Die Zahl der Geretteten ändert nur Details im Epilog, z. B. wer im Schlussbild steht.
  Antwort: offen

- [ ] **EN-08 Erfährt der Spieler im schlechten Ende, dass es ein anderes gibt?**
  Optionen: gar nicht, ein Satz im Abspann, ein Hinweis beim Neustart.
  Antwort: offen

- [ ] **EN-14 Wie verteilen sich Midas und Ernte auf die Enden?**
  Stand (Benedict, 2026-11-20): „Midas und Ernte finde ich eine gute Idee.“ Midas ist ausdrücklich das schlechte Ende (EN-06). Dass Ernte das gute Ende ist (Spiegel, Option A), hat Benedict nicht ausdrücklich bestätigt. Korrigiert am 2026-11-20, vorher fälschlich als entschieden markiert.
  Stand (Benedict, 2026-11-20): Beide gefallen. Sie greifen das Thema auf: Geld hat nur den Wert, den Menschen ihm geben.
  Optionen:
  - A) **Spiegel:** Gutes Ende = Ernte (Geld weg, Menschen bleiben). Schlechtes Ende = Midas (Geld überall, Menschen weg).
  - B) **Drei Stufen:** alle gerettet = Wesen besiegt ohne Preis, einige = Ernte, keiner = Midas.
  - C) Beide im selben Ende: erst Ernte, dann Midas.
  Vorschlag: A.
  Antwort: offen

- [ ] **EN-15 Wie sieht das Finale ohne Kampf aus?**
  Entschieden (Benedict, 2026-11-20): Das Angebot macht immer der Strippenzieher. Er hat seine Seele bei riesigen Experimenten mit Splittern verloren (um seine „schwermütige“ Mutter zu heilen, siehe KI-08) und handelt nur noch im Interesse des Meteors.
  Ergänzung (Benedict, 2026-11-20): Das Wesen spricht nie selbst, nur durch andere (KI-05).
  Offen: Ablauf der Finalszene, und wie das Ablehnen funktioniert (Gegenstand ohne Geldwert? Dialog?). Siehe EN-22.
  Früherer Stand: Point-and-Click, kein Kampf. Das Wesen verspricht Reichtum gegen die Seele der Spielfigur (EN-06, EN-18). Nur wer mindestens einen Splitter benutzt hat, kann mit dem Wesen sprechen, vielleicht per Telepathie.
  Benedicts Frage: Wer keinen Splitter benutzt hat, bekommt kein Angebot und kann auch keinen Gegenstand ohne Geldwert übergeben. Geht das Finale dann überhaupt? Oder sollte der Strippenzieher das Angebot immer machen?
  Optionen:
  - A) Ohne Splitter kein Angebot. Das Ende hängt dann nur an den Geretteten. Ernte entsteht, weil dem Wesen die Körper fehlen. Einen Gegenstand muss man nicht übergeben.
  - B) Das Angebot kommt immer. Hat die Spielfigur keinen Splitter benutzt, spricht das Wesen durch den Strippenzieher, dessen Seele schon fast leer ist. Hat sie Splitter benutzt, spricht es direkt in ihren Kopf.
  - C) Das Angebot macht immer der Strippenzieher selbst. Er glaubt, er biete eigenen Reichtum an.
  Entschieden: eine Variante von C, das Wesen spricht durch ihn.
  Bisheriger Vorschlag: Ein Gespräch mit dem Wesen. Annehmen führt zu Midas. Ablehnen geht nur, wenn die Spielfigur etwas hat, das ihr mehr bedeutet als Gold: gerettete Freunde und Erinnerungen an sie. Als Gegenstandsrätsel: Sie hält dem Wesen etwas ohne Geldwert hin, z. B. das Geschenk eines Freundes. Das Wesen kann diesen Wert nicht messen.
  Antwort: offen

- [ ] **EN-16 Wie zeigen wir die Enden?**
  Optionen: A) als eigene spielbare Szene, B) als Schattentheater aus Standbildern mit Text, C) nur als Text.
  Vorschlag: B. Passt zum Scherenschnitt und kostet wenig. Im Midas-Ende werden die Silhouetten nach und nach golden.
  Antwort: offen

- [x] **EN-17 Kann die Spielfigur Splitter benutzen und dafür Seele verlieren?**
  Korrektur (Benedict, 2026-11-20): Splitter sind **nicht unbegrenzt**, sie sind wertvoll. „Immer benutzbar“ heißt: Wer einen hat, kann ihn überall einsetzen.
  Ergänzung (Benedict, 2026-11-20): Der Preis bleibt verborgen. Spieler kennen solche Helfer als Tippsystem ohne Nachteil und erwarten keine Folgen. Auch die Spielfigur weiß es nicht. Genau das ist der Sinn.
  Antwort (Benedict, 2026-11-20): Ja, immer, auch beim Brauen. Splitter nützen eigentlich wenig, sollen aber jederzeit zur Wahl stehen. Die Verlockung, sie zu benutzen, soll möglichst groß sein. Jeder Gebrauch kostet ein Stück Seele. Dadurch fallen Dialogoptionen weg, weil die Spielfigur Informationen nicht mehr abrufen kann. Irgendwann kann sie Freunde nicht mehr retten.
  Spannung: „wenig nützlich“ und „große Verlockung“ müssen zusammenpassen. Was ein Splitter konkret bringt, klärt EN-20.
  Wie man an Splitter kommt: RS-09. Warnzeichen: EN-21.
  Ursprüngliche Optionen:
  Optionen:
  - A) Splitter als freiwillige Abkürzung an manchen Rätseln. Jeder Gebrauch löscht eine Erinnerung, sichtbar als ausgegraute Dialogoption.
  - B) Nur an wenigen festen Momenten der Verlockung, z. B. einer pro Kapitel.
  - C) Nur erzählt, ohne Spielmechanik.
  Vorschlag war: B, mit zwei Regeln für Fairness: Das Spiel zeigt den Preis vor dem Gebrauch, und jedes Rätsel ist auch ohne Splitter lösbar. Die erste Regel hat Benedict verworfen (Preis bleibt verborgen).
  Hinweis: Kein Rezept darf einen Splitter brauchen, denn Zutaten sind unbegrenzt (FA-G-06). Splitter beim Brauen bleibt eine Zusatzoption.

- [x] **EN-18 Was löst das Midas-Ende aus?**
  Antwort (Benedict, 2026-11-20): Es gibt mehrere Auslöser:
  1. Die Spielfigur hat nicht genug Personen gerettet.
  2. Sie nimmt das Angebot an und bietet für den Reichtum ihre eigene Seele.
  Hinweis (2026-11-24): Laut KI-21 braucht die große Verwandlung ihren Wunsch. Wie Auslöser 1 ohne ihren Wunsch zu Midas führt, ist offen (W-05 in ki-plan). Klären, wenn die Handlung am Ende ist.
  Geändert (Benedict, 2026-11-20): Das Angebot kommt immer, und zwar vom Strippenzieher (EN-15). Die frühere Regel „Angebot nur mit Splitter“ entfällt.
  Ursprüngliche Optionen:
  - A) Nur die Entscheidung im Finale (Angebot annehmen).
  - B) Nur zu wenige gerettete Freunde.
  - C) Die Entscheidung im Finale. Ablehnen kann man aber nur, wenn genug Freunde gerettet und genug Erinnerungen übrig sind.
  Vorschlag war: C. Damit zählen Freunde, Splitter und die letzte Entscheidung zusammen.

- [ ] **EN-19 Wie funktioniert das Werwolf-Kapitel?**
  Priorität (Benedict, 2026-11-20): Die Idee für das Kapitel steht. Die Details sind weniger wichtig als die Grundsatzfragen und kommen später.
  Stand (Benedict, 2026-11-20): Es geht das Gerücht, dass sich ein Homunkulus unter den Leuten versteckt. Die Spielfigur muss ihn entlarven und dafür Rätsel lösen und gut kombinieren. Am Ende wird jemand angeklagt und geopfert. War es nicht der Homunkulus, zählt das als eine gerettete Person weniger.
  Offen:
  - Wer klagt an und opfert: die Akademie (Tribunal), die Pilger, der Strippenzieher?
  - Wird ein Unschuldiger getötet, oder trifft ihn etwas anderes, z. B. Verbannung in den Krater? Das bestimmt, wie dunkel das Spiel wird.
  - Woher kommt das Gerücht? Vorschlag: Der Strippenzieher streut es selbst, um von sich abzulenken.
  - Fairness: Die Hinweise müssen auf genau eine Person zeigen, wenn man alle findet. Eine falsche Anklage darf das Spiel nicht blockieren.
  Antwort: offen

- [x] **EN-20 Was bringt ein Splitter, damit die Verlockung groß ist?**
  Antwort (Benedict, 2026-11-20): Er löst ein Rätsel sofort (A). Die Verlockung entsteht dadurch, dass das einfach geht und schnell hilft. Spieler halten ihn für eine Hilfe ohne Nachteil.
  Warum wichtig: Splitter sollen eigentlich wenig nützen und trotzdem sehr verlocken (EN-17).
  Optionen:
  - A) **Abkürzung:** Ein Rätsel ist sofort gelöst, eine Tür geht auf.
  - B) **Glanz:** Ein Trank wird „vollkommen“. Lehrer loben, Mitschüler staunen. Das ist nutzlos, fühlt sich aber gut an und passt zum Thema (Wert, den andere zuschreiben).
  - C) **Flüstern:** Der Splitter verrät einen Hinweis, wenn man nicht weiterkommt. Ironisch: Die Hilfe kostet genau die Erinnerungen, die man zum Weiterkommen braucht.
  - D) Alles davon, je nach Ort.
  Vorschlag war: B und C.

## Folgen für das Projekt

Diese Punkte gehen an die Architektur, sobald die Antworten oben stehen. Laut [AGENTS.md](../../../AGENTS.md) wird jede fehlende Engine-Funktion als Story vorgeschlagen.

- [ ] **EN-09 Zähler statt boolescher Flags?** Die Zahl der Geretteten (EN-18) und die Zahl benutzter Splitter (EN-17) brauchen Zähler oder Bedingungen über mehrere Flags. Die Engine kennt in v1 nur boolesche Flags ([Offene Fragen](../../offene-fragen.md#asset-vertrag-und-werkzeuge)).
- [ ] **EN-10 Figurvarianten nach Spielstand?** Dieselbe Figur muss je nach Flag ein anderes SVG, eine andere Leuchtfarbe, einen anderen Laufstil und andere Dialoge bekommen.
- [ ] **EN-11 Zeitablauf?** Räume und Figuren müssen je Kapitel (ZL-10) anders belegt sein, ggf. auch je Tag (ZL-07).
- [ ] **EN-12 Zwei Enden ohne Sackgasse?** Beide Enden müssen erreichbar sein, und der Spieler darf nicht steckenbleiben, wenn er Hinweise verpasst hat. Das muss der Lösbarkeitstest abdecken.
- [ ] **EN-13 Spieltest:** Wie prüfen wir, ob die Hinweise zu subtil oder zu deutlich sind? Vorschlag: zwei Personen außerhalb von Creative spielen den ersten Prototyp und sagen danach, wer ihnen seltsam vorkam.

- [x] **EN-21 Woran merkt man, dass Splitter etwas kosten?**
  Antwort (Benedict, 2026-11-20): Ein aufmerksamer Spieler soll es erst merken, wenn es fast zu spät ist. Zum Beispiel: Die ersten Dialogoptionen werden grau, und man weiß nicht, warum. Oder man hat nach dem Benutzen Schwindel.
  Verworfen: frühe, steigende Zeichen (schwächere Leuchtfarbe ab dem ersten Splitter, Kommentare von Figuren).
  Stand (Benedict, 2026-11-20, Idee): Ab einer gewissen Zahl gibt es ganz leichte Hinweise, z. B. Schwindel nach dem Benutzen oder die letzte Handlung vergessen.
  Warum wichtig: Der Preis ist verborgen (EN-17). Damit es sich am Ende nicht wie Willkür anfühlt, sollte ein aufmerksamer Spieler es ahnen können.
  Optionen (kombinierbar):
  - A) Schwindel: Das Bild schwankt kurz.
  - B) Die letzte Handlung ist vergessen, z. B. ein Eintrag im Notizbuch der Spielfigur fehlt.
  - C) Die Leuchtfarbe der Spielfigur wird schwächer (Scherenschnitt-Stil, ohne Text).
  - D) Figuren bemerken es: „Du wirkst abwesend.“ Der Strippenzieher sagt: „Gut so. Du lernst schnell.“
  Vorschlag war: steigern. Ab dem 1. Splitter C, ab dem 3. D, ab dem 5. A und B.

- [ ] **EN-22 Ab wann kann die Spielfigur das Angebot nicht mehr ablehnen?**
  Stand (Benedict, 2026-11-20): Späteres To-do. Hängt davon ab, wie viele Leute man gerettet hat.
  Warum wichtig: Splitter kosten Erinnerungen. Davon hängt ab, ob das Ablehnen im Finale noch möglich ist (EN-15, EN-18).
  Optionen:
  - A) Feste Schwelle: Ab z. B. drei benutzten Splittern fehlt die Dialogoption zum Ablehnen.
  - B) Bestimmte Erinnerungen: Jeder Splitter löscht eine konkrete Erinnerung an eine Person. Ablehnen kann man nur mit mindestens einer Erinnerung an eine gerettete Person.
  - C) Keine Schwelle. Splitter erschweren nur die Rettungen, das Finale bleibt frei wählbar.
  Vorschlag: B. Am Ende hält die Spielfigur das fest, woran sie sich noch erinnert. Das ist das Thema als Mechanik.
  Antwort: offen

- [ ] **EN-23 Wie zeigen wir die Telepathie des Wesens?**
  Priorität (Benedict, 2026-11-20): Frage für sehr viel später.
  Stand (Benedict, 2026-11-20, Idee): Wer einen Splitter benutzt hat, empfängt das Wesen telepathisch, in abstrakten Worten, die für diese Person Sinn ergeben. Darstellung: ein unverständlicher Text, der sich dann übersetzt.
  Optionen:
  - A) Nach jedem Splitter erscheint kurz ein fremder Text. Mit jedem weiteren Splitter wird mehr davon lesbar.
  - B) Der Text erscheint nur in bestimmten Momenten (z. B. nahe am Meteor oder beim Strippenzieher).
  - C) Nur im Finale.
  Vorschlag: A. Der Text wird erst spät lesbar und passt damit zu EN-21: Wer ihn versteht, ist schon fast verloren.
  Antwort: offen
