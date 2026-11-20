# Styleguide: Charaktere für „Akademie der Alchemie“

Mit diesem Dokument lässt sich der Stil der bisherigen Figuren (Alchemistin, Lehrling, Meister, Erzalchemist, Schmied) auf beliebige neue Charaktere übertragen, von Hand oder mit Claude. Es beschreibt Format, Rig, Proportionen, Farben, Silhouette, Animation und die Fehler, die bei den bisherigen Figuren korrigiert werden mussten.

> **Kurzfassung:** Jede Figur besteht aus **SVG-Vektorformen** mit **CSS-Klassen statt fester Farben**. Sie hat **drei Ansichten** (Front, Seite, Rücken) mit **identischen Gruppen-IDs und Gelenkpunkten**. Im Spiel erscheint sie als **Scherenschnitt**: fast schwarz, ohne Außenlinien, mit **eigener Leuchtfarbe**. Erkennbar muss sie **am Umriss** sein.

---

## 1. Grundprinzipien

1. **Scherenschnitt ist der Spielstil.** Die farbige Version ist die Entwurfs- und Referenzfassung. Im Spiel sind alle Figuren dunkle Silhouetten (Stil „Außenlinien: Aus“).
2. **Die Figur ist immer das Dunkelste im Bild.** Kein Hintergrund und kein Objekt darf so dunkel sein wie die Figur.
3. **Die Silhouette muss sprechen.** Jede Figur muss allein am Umriss erkennbar sein, zum Beispiel an Hut, Haaren, Werkzeug, Körperform oder Stab. Innere Farbstufen sind Bonus, nicht Basis.
4. **Jede Figur hat eine eigene Leuchtfarbe.** Augen, Gläser, Tränke und Kerne leuchten in dieser Farbe und unterscheiden die Figuren auch im Dunkeln.
5. **Eine Geometrie, zwei Stile.** Farbe und Scherenschnitt teilen exakt dieselben Pfade. Nur der `<style>`-Block ist ein anderer.
6. **Gleiches Rig für alle.** Gruppen-IDs und Drehpunkte sind bei allen Figuren gleich. Dadurch läuft jede neue Figur sofort mit der bestehenden Laufanimation.
7. **Stilisiert, nicht realistisch.** Proportionen dürfen und sollen übertrieben sein, wenn das die Figur stärker macht, zum Beispiel beim Hünen-Schmied oder beim gebeugten Greis.

---

## 2. Technisches Format

| Eigenschaft | Wert |
|---|---|
| Format | SVG, eine Datei pro Ansicht und Stil |
| Koordinatensystem | `viewBox="0 0 400 800"` |
| Mittelachse | x = 200 |
| Bodenlinie (Fußsohle) | y = 773 |
| Filter | **keine** (`feGaussianBlur` usw. sind zu teuer). Leuchten **nur** über `radialGradient` |
| Farben | **nur über CSS-Klassen**, nie als `fill="#…"` direkt am Pfad (Ausnahme: Hilfslinien) |
| Dateinamen | `<figur>_<front|seite|rueck>_<farbe|scherenschnitt>.svg` |

Größere Figuren (z. B. der Schmied) werden **nicht neu gezeichnet**. Die Wurzelgruppe wird um den Fußpunkt skaliert:

```svg
<g id="character" transform="translate(200 773) scale(1.28) translate(-200 -773)">
```

Dann muss die `viewBox` der Einzeldateien vergrößert werden, z. B. `-60 -130 520 920`.

---

## 3. Rig: Pflicht-IDs und Drehpunkte

Die Laufanimation sucht genau diese IDs. **Namen und Drehpunkte nicht ändern**, sonst bricht die Animation.

### 3.1 Wurzelgruppen

| ID | Ansicht | Sichtbarkeit |
|---|---|---|
| `character` | Front (Stand **und** Laufen nach vorn) | Standard |
| `characterSide` | Seite, Blick nach **rechts** (links wird gespiegelt) | `style="display:none"` |
| `characterBack` | Rücken (Laufen nach hinten) | `style="display:none"` |

### 3.2 Front

| ID | Inhalt | Animation |
|---|---|---|
| `front_leg_l`, `front_leg_r` | Hosenbein / Bein **ohne** Stiefel | wird angehoben (translate y) |
| `boot_l`, `boot_r` | Stiefel, **getrennte** Gruppe | wird mit angehoben |
| `head`, `arm_l`, `arm_r` | frei gestaltbar | statisch |

> Stiefel und Bein werden **beide** angehoben. Steckt der Stiefel **in** der Beingruppe, bewegt er sich doppelt so weit (siehe Fehlerliste).

### 3.3 Seite (Blick nach rechts)

| ID | Drehpunkt | Inhalt |
|---|---|---|
| `side_leg_near`, `side_leg_far` | Hüfte **(205, 352)** | Oberschenkel |
| `side_leg_near_shin`, `side_leg_far_shin` (in der Beingruppe) | Knie **(206, 550)** | Knie-Kreis, Schienbein, Stiefel |
| `side_arm_near`, `side_arm_far` | Schulter **(205, 232)** | Oberarm |
| `side_arm_near_fore`, `side_arm_far_fore` (in der Armgruppe) | Ellbogen **(204, 288)** | Unterarm, Hand, getragene Objekte |

**Zeichenreihenfolge** (hinten nach vorn):
1. Mantel- oder Rockschoß hinten
2. `side_arm_far`
3. `side_leg_far`
4. vorderer Rockteil / Schürze
5. `side_leg_near`
6. Torso
7. Rucksack
8. `side_arm_near`
9. Kopf

Die fernen Glieder bekommen zusätzlich eine `class="shade"`-Überlagerung, damit sie in der Farbversion dunkler wirken.

### 3.4 Rücken

| ID | Drehpunkt | Inhalt |
|---|---|---|
| `back_leg_l`, `back_leg_r` | – | Bein **inklusive** Stiefel und Absatz (eine Gruppe!) |
| `back_arm_l`, `back_arm_r` | (168, 230) bzw. (232, 230) | Arm, leicht **nach außen** gedreht (`rotate(±6–8°)`) |

> Von hinten dürfen die Arme **nie über den Körper** schwingen. Sie hängen mit Abstand zum Torso und pendeln nur nach außen bzw. vor und zurück (Verkürzung).

### 3.5 Weitere Konventionen

- Getragene Objekte (Zange, Stab, Kolben) gehören **in die Unterarm-Gruppe**, damit sie mitschwingen.
- Eigene IDs mit Figuren-Präfix vergeben (z. B. `m_hat`, `e_side_eye`), damit es beim Einbau mehrerer Figuren keine Kollisionen gibt.
- `clipPath`-IDs ebenfalls mit Präfix versehen (`bclip_l`, `mclip_l` …).

---

## 4. Proportionen und Körperbau

### 4.1 Grundraster (Standardfigur)

| Bereich | y-Wert |
|---|---|
| Hut-/Mützenoberkante | ca. 30–70 |
| Kopf (Stirn bis Kinn) | ca. 100–200 |
| Schulterlinie | 222–232 |
| Taille / Gürtel | 310–340 |
| Hüftgelenk | **352** |
| Knie | **550** |
| Stiefelschaft | ca. 700–730 |
| Fußsohle | **773** |

- Etwa 7 Kopfhöhen, Beine etwa 60 % der Figur: Anime-Proportionen.
- Die Figur wirkt durch **Körperform und Größe** unterschiedlich, nicht durch ein anderes Rig.

### 4.2 Körpertypen (Beispiele aus dem Projekt)

| Typ | Umsetzung |
|---|---|
| Zierlich (Alchemistin) | schmale Schultern, enge Taille, lange schlanke Beine mit Lücke zwischen den Oberschenkeln |
| Jugendlich (Lehrling) | schmal, gerade, langer Mantel verlängert die Silhouette |
| Kräftig (Meister) | breite Schulterplatten mit Stacheln, dicke Beine, **gerader, breiter Stand** |
| Gebrechlich (Erzalchemist) | schmale Schultern, dünne Beine, Buckel, Kopf nach vorn versetzt, stützt sich auf Stab |
| Hüne (Schmied) | Skalierung 1,28, Fassbauch, Keulen-Unterarme, Fäuste auf Kniehöhe, **kleiner Kopf** (scale 0,84), Kopf ohne Hals tief zwischen den Schultern |

### 4.3 Regeln

- **Seiten- und Frontansicht müssen gleich massiv sein.** Beine und Arme im Profil sind mindestens so dick wie von vorn. Häufigster Fehler: Profil zu dünn.
- **Beine nicht nach innen laufen lassen.** Von vorn und hinten stehen die Beine gerade, mit sichtbarer Lücke, die auch in der Silhouette erhalten bleibt.
- **Arme vom Körper lösen**, wo der Umriss sonst verschmilzt, z. B. Fäuste leicht abgespreizt (`rotate(12–16°)` an der Schulter).
- **Kleiner Kopf = mächtiger Körper, großer Kopf = jünger/niedlicher.** Kopfgröße bewusst einsetzen.

---

## 5. Gesicht

### 5.1 Frontansicht

- Breites, weiches Gesicht mit rundem Kinn.
- **Augen:** rund bis leicht mandelförmig, mittelgroß (nicht Chibi). Iris füllt fast das ganze Auge, kleine runde Pupille, ein Glanzpunkt oben, optional ein zweiter kleiner unten. Feine, gleichmäßig gebogene Wimpernlinie ohne schräge „böse“ Kante.
- **Augenbrauen:** kurz und kräftig, über dem Pony gezeichnet, damit sie sichtbar bleiben.
- Nase als winziger Strich, Mund als kurzer Strich, Rouge als weiche Fläche.
- Alter oder Charakter über Details: Falten (`wrinkle`), Brille, Pausbacken, buschige Brauen, Bart.

### 5.2 Profil

Das abgestimmte Profil (Pfad `side_face` in `side.py`) wird von allen Figuren wiederverwendet:

- Stirn fast senkrecht, kleine Delle an der Nasenwurzel.
- Nasenspitze knapp unter Augenhöhe, Nase steht klar vor.
- Von der Nase schräg zurück über die Lippen. Das Kinn liegt hinter der Nasenspitze.
- Kurzer gerader Kiefer, der in einem Bogen zum Ohr hochläuft.
- **Auge im Profil:** schmales, hohes Oval **ohne sichtbares Augenweiß**, mit Glanzlicht oben, Wimpernbogen um das Auge und Unterlid nach hinten.
- **Hauptfiguren** (Alchemistin, Lehrling, Meister, Erzalchemist, Schmied) behalten ihre abgestimmten Profile.
- **NPCs und neue Nebenfiguren** bekommen ein eigenes Profil aus dem Generator `profile.py` (`profile(...)` bzw. `preset(name)`). Stirn, Hinterkopf und Halsanschluss sind bei allen gleich, deshalb passen Haare und Hüte weiter. Variiert werden:
  - `nose`: `pointy` (Anime-Standard), `straight`, `upturned` (Stupsnase), `button` (Knollennase), `hook` (Hakennase)
  - `L` Nasenlänge, `ty` Höhe der Nasenspitze, `lip` Lippenposition
  - `chin`, `cy` Kinnvorsprung und -höhe, `jaw` (`soft`, `round`, `square`), `jx` Kieferlänge, `double` Doppelkinn
- Faustregel: Junge Figuren haben kurze Stupsnasen und kleine runde Kinne. Kräftige Figuren haben gerade Nasen und kantige, tiefe Kinne. Alte oder gelehrte Figuren haben Hakennasen und fliehende Kinne. Die Silhouette soll das Profil allein am Umriss unterscheidbar machen.
- Den Mundstrich liefert der Generator passend mit (`["mouth"]`).

---

## 6. Haare: wichtigste Regel

> **Haare müssen in jeder Ansicht durchgängig sein.**

Dieser Fehler kam bei mehreren Figuren vor. Darauf achten:

1. **Seitenansicht:** Die Haare bedecken die **gesamte Kopfseite**: von der Kopfbedeckung über Schläfe und Hinterkopf bis zum Nacken bzw. zur Haarlänge. Es dürfen nicht nur Strähnen hinten heraushängen, während die Kopfseite nackte Haut bleibt.
2. **Keine Lücke zwischen Haaren und Hals.** Das Nackenhaar läuft bis an den Hals heran oder liegt über ihm.
3. **Bartträger:** Haar → Koteletten → Bart ist eine geschlossene Fläche ohne Hautstreifen dazwischen.
4. Das Ohr liegt **über** dem Haar (bei kurzen Haaren) oder wird ganz verdeckt (bei langen Haaren).
5. **Rückansicht:** Bei kurzen Haaren muss der Nacken sichtbar bleiben (Hals einzeichnen). Er darf nicht vom Rucksack verdeckt werden.
6. **Frisuren unterscheiden:** Jede Figur braucht eine eigene Haarform: Länge, Scheitel, Pony über einem Auge, abstehende Strähnen. „Immer gleiche Haare“ war ein Kritikpunkt.
7. **Pony unter Hutkrempen** muss sichtbar bleiben. Notfalls den Hut anheben (`translate(0 -12)`).
8. Bei Scherenschnitt-Problemen (gezackter Pony ergibt eine unruhige Stirnkante) können im Dunkelstil einzelne Gruppen ausgeblendet werden (`#side_bangs{display:none}`). Die farbige Version behält sie.

**Haarelemente:** Basisfläche (`hair`), helle Glanzsträhne (`hairshine`), dunkle Strähnenlinien (`hairline`), Cel-Schatten unter dem Pony (`cel`), Zacken an den Spitzen.

---

## 7. Farbsystem (Farbversion)

### 7.1 Gemeinsame Klassen

| Klasse | Zweck | Beispielwert |
|---|---|---|
| `skin` | Haut | `#fde4d4` |
| `cel` | harter Cel-Schatten | `#c4685a`, Deckkraft 0,32 |
| `shade` | Schatten-Overlay | Violett-Ton, Deckkraft 0,22 |
| `line` | Falten, Nähte | dunkle Kontur, Deckkraft 0,6 |
| `brass`, `buckle` | Messing, Schnallen | `#e0ad4a` |
| `boot`, `bootdark` | Stiefel | `#432619`, `#2c1810` |
| `vialglass`, `liquid` | Glas, Trank | halbtransparent, Trankfarbe |
| `eyewhite`, `iris`, `pupil`, `hl`, `lash`, `brow2` | Augen | – |

**Konturen:** Alle Hauptflächen haben `stroke:#3b2219; stroke-width:2.2; stroke-linejoin:round`.

### 7.2 Eigene Klassen pro Figur

Jede Figur bekommt ein **Präfix** und eigene Klassen, z. B. Meister `armor`, `mcoat`, `mhat`; Erzalchemist `erobe`, `estole`; Schmied `sapron`, `sbeard`. Das hält die Paletten getrennt.

### 7.3 Steampunk-Palette

Warme Brauntöne (Leder, Holz), Messing und Gold, gedecktes Rot, Nachtblau, Creme. Alles leicht entsättigt, nie neonfarben. Neon gibt es nur bei Leuchtelementen.

---

## 8. Scherenschnitt (Spielstil)

### 8.1 Grundwerte

| Element | Wert |
|---|---|
| Figur (Basis) | `#140e10` |
| Nähte gegen Kantenglättung | gleiche Farbe als Kontur: `stroke:#140e10; stroke-width:1.2` |
| Ausgeblendet | Augenweiß, Iris, Wimpern, Brauen, Mund, Cel, Linien, Schatten |
| Sichtbar | nur Glanzpunkte (`hl`), Gläser, Tränke, Leuchtkerne |

### 8.2 Leuchtfarben (jede Figur eine eigene)

| Figur | Leuchtfarbe(n) | Träger |
|---|---|---|
| Alchemistin | Bernstein `#ffcf6b`, Grün `#7dffb0` | Schutzbrille, Augen, Trank |
| Lehrling | Cyan `#7fe3ff` | Brillengläser, Glasröhre im Rucksack |
| Meister | Gelb `#ffe066`, Violett `#c38bff`, Rosa | Brust-Reaktorkern, Röhren und Rohr zum Handschuh, Brille |
| Erzalchemist | Ember-Orange `#ffb35a` | Stabkern, Brillenränder, Monokel |
| Schmied | Rot `#ff6a3c`, Funken `#ffd27a` | glühender Barren in der Zange, Funken, Brille |

**Neue Figur:** Wähle eine noch freie Farbe, z. B. Eisblau-Weiß, Magenta oder Smaragd. Die Farbe sollte zur Rolle passen.

Jedes Leuchtelement besteht aus drei Teilen:
1. einer Fläche in der Leuchtfarbe
2. einem `radialGradient`-Halo dahinter (Deckkraft 0,85 nach 0)
3. optional einem kleinen weißen Glanzpunkt

> **Der Gradient-Halo muss auch im Scherenschnitt-CSS definiert sein** (`.glowx{fill:url(#glowX)}`). Sonst wird der Halo als **schwarzer Kreis** gerendert.

### 8.3 Ebenen und Details: maßvoll einsetzen

Es gibt zwei Strategien. Wähle pro Figur bewusst eine:

**A) Sprechende Silhouette (Standard, z. B. Schmied):**
- Alles einfarbig `#140e10`, nur die Lichter leuchten.
- Die Figur wird über den Umriss erkannt: abstehende Fäuste, Hammer über der Schulter, Kopftuchzipfel, Bartspitzen.
- Höchstens **eine** helle Fläche als Kontrast für ein wichtiges Merkmal, z. B. Schürze `#261a1d`, damit der schwarze Bart darauf lesbar ist.

**B) Geschichtete Silhouette (sparsam, z. B. Meister, Erzalchemist, Alchemistin):**
- **Transparente Stoffe:** lange Mäntel, Roben und Schleppen mit `opacity:0.8`, so dass Beine und Stiefel durchscheinen.
- **Tonstufen:** z. B. Rüstung `#1f1418`, Glanzplatte `#2a1c21`, Fugen `#140e10`, Bart `#221a1e`.
- **Dezente Ornamente:** Goldkanten oder Symbole mit Deckkraft 0,4–0,5.

> Nicht jede Figur braucht viele Farbunterschiede. **Zu viele Tonstufen verwässern den Scherenschnitt.** Im Zweifel Strategie A und die Form verbessern.

### 8.4 Kontrastregel zur Szene

Alle Tonstufen der Figur müssen **dunkler** sein als die dunkelste Stelle der Szene:

| Szenenebene | Ton |
|---|---|
| Hintergrund | `#4a2c33` |
| Mittelgrund | `#3a242b` |
| Vordergrund / Innenräume | `#2e1c22` |

Die hellste Figuren-Stufe sollte deshalb ≤ `#26191d` sein.

---

## 9. Leuchten, Glas, Effekte

- **Glas:** `vialglass` halbtransparent, Flüssigkeit als eigene Fläche, Korken oben.
- **Rauch und Dampf:** weiße bzw. rosa Fläche mit Deckkraft 0,16–0,28. Das gibt eine zusätzliche Transparenzebene im Scherenschnitt.
- **Funken:** kleine Kreise (r = 1,2–1,8) in Funkenfarbe.
- **Funkeln:** vierzackiger Stern (`sparkle`).

---

## 10. Laufanimation und Laufstil

Die Animation ist im Spiel-Template (`scene_template.html`) implementiert und für alle Figuren gleich:

- **Seitlich:** Hüfte schwingt sinusförmig. Das Schwungbein beugt früh das Knie, das Standbein bleibt fast gestreckt. Die Körperhöhe wird **aus der Beinstellung berechnet**, so dass immer ein Fuß den Boden berührt. Die Schrittfrequenz ist an die Laufstrecke gekoppelt, damit die Füße nicht rutschen.
- **Nach vorn und hinten:** Beine heben sich abwechselnd mit Easing. Der Körper ist am höchsten, wenn ein Bein durchschwingt, und pendelt leicht.
- **Tiefe:** Figur wird kleiner, je weiter hinten sie steht. Am Ziel steht sie immer frontal.

### 10.1 Eigener Laufstil (`WALK_STYLE`)

Jede Figur kann ein Objekt mit Parametern mitbringen. Was fehlt, wird mit dem Standard gefüllt (Gang der Alchemistin):

| Parameter | Standard | Bedeutung |
|---|---|---|
| `hip` | 20 | Hüftausschlag in ° (Schrittlänge) |
| `knee` | 44 | maximale Kniebeugung in ° |
| `arm` | 16 | Armschwung in ° |
| `fore` | 16 | Ellbogenbeugung beim Vorschwingen |
| `lean` | 3 | Körperneigung in ° (positiv = nach vorn) |
| `swag` | 0 | rhythmisches Wiegen (Schulterrollen) im Seitengang |
| `lift` | 13 | Beinhub beim Laufen nach vorn/hinten |
| `bob` | 6 | Auf und Ab nach vorn/hinten |
| `sway` | 1,6 | seitliches Pendeln nach vorn/hinten |
| `armOut` | 4 | Armpendeln in der Rückansicht (nur nach außen) |
| `speed` | 330 | Laufgeschwindigkeit |

**Beispiele aus dem Projekt:**

```python
# selbstbewusst (Meister): aufrecht, lange Schritte, Schulterrollen
{'hip': 23, 'knee': 34, 'arm': 24, 'fore': 8, 'lean': -1.5, 'swag': 1.4, 'lift': 11, 'bob': 4, 'sway': 3.4, 'armOut': 6, 'speed': 290}
# gebrechlich (Erzalchemist): kurze Schritte, gebeugt, langsam
{'hip': 12, 'knee': 26, 'arm': 5, 'fore': 4, 'lean': 6, 'swag': 0.6, 'lift': 7, 'bob': 2.5, 'sway': 1.2, 'armOut': 2, 'speed': 190}
# schwer und watschelnd (Schmied)
{'hip': 14, 'knee': 28, 'arm': 12, 'fore': 6, 'lean': 0, 'swag': 2.8, 'lift': 10, 'bob': 6, 'sway': 4.6, 'armOut': 8, 'speed': 235}
```

---

## 11. Arbeitsablauf für einen neuen Charakter

1. **Konzept in drei Sätzen:** Rolle, Persönlichkeit, Körperbau. Bei Vorlagen nur Elemente übernehmen (Hut, Werkzeug, Statur), nie ein fremdes Design kopieren.
2. **Silhouetten-Idee festlegen:** Welche 2–3 Umrissmerkmale machen die Figur unverwechselbar? (Hut, Werkzeug, Körperform, Haare)
3. **Leuchtfarbe wählen**, die noch nicht vergeben ist, und festlegen, was leuchtet.
4. **Modul anlegen** (`<figur>.py`) nach dem Muster von `boy.py`, `mentor.py`, `elder.py` oder `smith.py`:
   - `X_CSS` (Farbe), `X_DARK` (Scherenschnitt), `X_DEFS` (Gradienten)
   - `FRONT`, `SIDE`, `BACK` mit den Pflicht-IDs
   - optional `WALK_STYLE`, `SCALE`/`ROOT`
5. **Rendern und prüfen:** alle drei Ansichten farbig und als Scherenschnitt nebeneinander (Kontrollblatt).
6. **Vorschau bauen:** `python char_page.py <modul> <präfix> "<Name>"` erzeugt `<präfix>_vorschau.html` mit Raum, Laufen und Demo-Runde.
7. **Laufzyklus prüfen:** acht Phasen pro Richtung als Bildstreifen oder GIF.
8. **Checkliste durchgehen** (Abschnitt 12).

---

## 12. Checkliste vor der Abgabe

**Rig und Technik**
- [ ] Alle Pflicht-IDs vorhanden, Drehpunkte unverändert
- [ ] Front: Stiefel in eigener Gruppe, **nicht** im Bein
- [ ] Rücken: Stiefel und Absatz **in** der Beingruppe
- [ ] Getragene Objekte in der Unterarm-Gruppe
- [ ] Alle Glow-Gradienten auch im Scherenschnitt-CSS definiert
- [ ] Keine SVG-Filter, Farben nur über Klassen

**Form und Proportion**
- [ ] Seitenansicht genauso massiv wie die Front (Beine, Arme, Torso)
- [ ] Beine von vorn/hinten gerade, mit Lücke
- [ ] Arme von hinten außerhalb des Körpers
- [ ] Kopfgröße passt zum Charakter

**Haare**
- [ ] Seitenansicht: ganze Kopfseite bedeckt
- [ ] Keine Lücke zwischen Haaren und Hals
- [ ] Bart (falls vorhanden) geht ohne Lücke in die Haare über
- [ ] Rückansicht: Nacken sichtbar (bei kurzen Haaren)
- [ ] Frisur unterscheidet sich von den anderen Figuren

**Scherenschnitt**
- [ ] Figur am Umriss erkennbar (Test: ohne Leuchtfarben anschauen)
- [ ] Figur dunkler als jede Stelle der Szene
- [ ] Eigene Leuchtfarbe, Halos rendern farbig (nicht schwarz)
- [ ] Keine hellen Nahtlinien zwischen Flächen (Kontur in Figurfarbe)
- [ ] Höchstens so viele Tonstufen wie nötig

**Animation**
- [ ] Kein Teil löst sich beim Laufen (Absätze, Gürteltaschen, Stäbe)
- [ ] Standbein berührt immer den Boden, Füße rutschen nicht
- [ ] Laufstil passt zur Persönlichkeit

---

## 13. Bekannte Fehler aus dem Projekt (und Lösung)

| Problem | Ursache | Lösung |
|---|---|---|
| Absatz trennt sich beim Rückwärtslaufen vom Stiefel | Stiefel in der Beingruppe **und** separat angehoben → doppelter Hub | in der Rückansicht nur die ganze Beingruppe anheben |
| Gang wirkt wie Humpeln | Wippen unabhängig von den Beinen; Füße rutschen | Körperhöhe aus der Beinstellung berechnen; Schrittfrequenz an die Strecke koppeln |
| „Stelzen“-Gang | Beine nur aus der Hüfte geschwenkt | Kniegelenk (`*_shin`) und Ellbogen (`*_fore`) einführen |
| Glühen im Scherenschnitt als schwarzer Kreis | Gradient-Klasse fehlt im Dunkel-CSS | `.glowx{fill:url(#glowX)}` in `X_DARK` aufnehmen |
| Helle Haarlinien zwischen schwarzen Flächen | Kantenglättung | Kontur in Figurfarbe: `stroke:#140e10; stroke-width:1.2` |
| Haare nur hinten, Kopfseite nackt | Haarfläche nur hinter dem Kopf gezeichnet | zusätzliche Haarfläche **über** der Haut, die Schläfe und Seite bedeckt |
| Lücke zwischen Nackenhaar und Hals | Haar endet über dem Ohrläppchen | Haarform bis an den Hals verlängern |
| Hals von hinten unsichtbar | Rucksack sitzt zu hoch | Rucksack absenken, Kragen ergänzen |
| Pony unsichtbar unter der Hutkrempe | Hut zu tief | Hut anheben, Ponyspitzen verlängern |
| Profil zu dünn gegenüber der Front | andere Maße im Profil | Bein-/Armbreiten aus der Front übernehmen |
| Arme verschmelzen im Scherenschnitt mit dem Bauch | Arme liegen am Körper an | Arme an der Schulter abspreizen |
| Profil passt nicht zur Referenz | nur die vordere Linie angeglichen; Haarsträhne für Gesichtskante gehalten | Referenz **ausmessen und überlagern** (Abschnitt 14) |
| Gegenstände in der Szene im Dunkeln unsichtbar | zu wenig Kontrast | hellere Gefäße, Etiketten, Randlicht |

---

## 14. Arbeiten mit Referenzbildern

- Bei Korrekturen ist **Einzeichnen** am genauesten: eine rote Linie auf einen Screenshot, die dann Pixel für Pixel übernommen wird.
- Vorgehen bei Vorlagen:
  1. Bild auf die eigene Darstellung registrieren (Skalierung und Versatz über ein gemeinsames Merkmal, z. B. Mütze oder Auge)
  2. Kontur bzw. rote Linie zeilenweise auslesen
  3. in SVG-Koordinaten umrechnen
  4. halbtransparent überlagern und vergleichen
  5. Pixel-Differenzbild erzeugen (rot = fehlt, blau = zu viel)
- **Fremde Figuren und Designs nicht nachbauen.** Bekannte Charaktere oder signierte Artworks dienen nur als Referenz für **Elemente** (Statur, Hut, Werkzeug, Stimmung). Daraus entsteht eine eigene Figur.

---

## 15. Prompt-Vorlage für Claude

```
Erstelle einen neuen Charakter für „Akademie der Alchemie“ nach dem Styleguide
(STYLEGUIDE_Charaktere.md).

Charakter: <Name / Rolle>
Persönlichkeit: <z. B. misstrauisch, hilfsbereit>
Körperbau: <z. B. groß und hager, klein und rund>
Markante Silhouetten-Merkmale: <2–3 Merkmale>
Leuchtfarbe: <noch freie Farbe> – leuchtet an: <z. B. Laterne, Augen>
Silhouetten-Strategie: <A sprechend | B geschichtet>
Laufstil: <z. B. hektisch, schleichend> → WALK_STYLE ableiten
Referenzen (nur als Inspiration): <Bilder/Beschreibung>

Liefere: Modul <figur>.py mit FRONT/SIDE/BACK, X_CSS/X_DARK/X_DEFS, WALK_STYLE;
die 6 SVGs; Vorschauseite über char_page.py; Kontrollblatt und Lauf-GIFs.
Prüfe die Checkliste aus Abschnitt 12, insbesondere durchgängige Haare in der Seitenansicht.
```

---

## 16. Dateiübersicht (Quellcode)

| Datei | Inhalt |
|---|---|
| `gen.py` | Grundformen, Frontkopf der Alchemistin, Farbpaletten (`ANIME_CSS`, `ANIME_DEFS`) |
| `anime2.py` | Körper der Alchemistin (Front) |
| `anime_dark.py` | Scherenschnitt-Basis (`css`) |
| `side.py`, `back.py` | Seiten- und Rückansicht der Alchemistin, abgestimmtes Profil `side_face` |
| `profile.py` | Profil-Generator und Presets für die NPCs |
| `boy.py` | Lehrling, Hilfsfunktion `mir()` (Spiegeln) und `girl_profile()` |
| `mentor.py` | Meister, Hilfsfunktionen `gear()`, `spike()`, `pauldron()` |
| `elder.py` | Erzalchemist, `staff()`, `symbols()` |
| `smith.py` | Schmied, `tongs()`, `hammer_back()`, Skalierung über `ROOT` |
| `scene_template.html` | Spiellogik, Laufanimation, `WALK_STYLE`-Unterstützung |
| `build_scene.py` | Lehrsaal-Szene, setzt die Spieldemo zusammen |
| `char_page.py` | Vorschauseite für eine beliebige Figur |
