# Offene Fragen

Erledigte Fragen wandern mit Datum in die [Entscheidungen](entscheidungen.md).

## Rückfragen an den Dozenten
- [ ] Welche Rolle hat die Hochschule im Projekt (Vorgaben, Prüfungsordnung, Abnahme)? (SH-03)
- [ ] Wie müssen wir KI-Nutzung kennzeichnen? Bis zur Antwort: Abschnitt „KI-Beteiligung“ in der PR-Vorlage.

## Modul
- [ ] Abgabetermine (Zwischen- und Endabgabe)
- [ ] Bewertungskriterien und Abgabeform

## Produkt
- [ ] Spielkonzept: Setting, Ton, Länge, erstes Release. Daraus folgen die FA zum Spielinhalt (mind. 15 FA gesamt, 11 stehen: FA-E und FA-DEV).
- [ ] Projektsteckbrief: Projektname, Ziel, Abgrenzung

## Rückfragen an die Architektur (Lars, Benedict)
- [ ] **FA-E-07, Einheit:** „2 px vom Klickpunkt“ in SVG-Einheiten oder Bildschirmpixeln? Und was passiert bei einem Klick außerhalb der begehbaren Fläche?
- [ ] **NF-E-03, Messbedingungen:** Assets schon geladen oder mit gedrosselter Verbindung? Ohne Bedingung ist der Wert nicht reproduzierbar.
- [ ] **NF-E-02, Gate:** Die Bildrate wird manuell gemessen. Zusätzlich ein CI-Näherungswert (Playwright-Trace mit CPU-Drosselung, Frame-Zeit)?
- [ ] **Vollständige Liste:** E-02 bis E-04, E-06, E-08, E-09, E-11 bis E-15 und die übrigen N-IDs fehlen noch.
- [ ] **Ablageort der Inhalte:** `content/` als Wurzel für Räume, Figuren, Gegenstände, Animationen bestätigen.

## Technik
- [ ] Rulesets auf GitHub einrichten (EP-02 bis EP-04, EP-11), sobald das Team Zugriff hat
- [ ] Agenten-Werkzeug: bestimmt die Umsetzung von EP-12 und EP-15
- [ ] Speicherort der Spielstände: Browser oder Server (NF-V-03). Ein Server würde die nicht übernommenen Gates wieder relevant machen.
- [ ] Claim gegen Doppelarbeit: bei 7 Personen plus Agenten wahrscheinlich nötig

## Mit dem Team bestätigen
- [ ] Zusage: 16 NF, 11 FA, 15 EP
- [ ] Akzeptanz-Vorschläge NF-A-01 (Browser) und NF-A-02 (ab 1280 px Fensterbreite) bestätigen
- [ ] Personas P-01 bis P-03 als Arbeitsgrundlage
