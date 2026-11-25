# Offene Fragen

Erledigte Fragen wandern mit Datum in die [Entscheidungen](entscheidungen.md).

## Rückfragen an den Dozenten
- [ ] Welche Rolle hat die Hochschule im Projekt (Vorgaben, Prüfungsordnung, Abnahme)? (SH-03)
- [ ] Wie müssen wir KI-Nutzung kennzeichnen? Bis zur Antwort: Abschnitt „KI-Beteiligung“ in der PR-Vorlage.

## Modul
- [ ] Abgabetermine (Zwischen- und Endabgabe)
- [ ] Bewertungskriterien und Abgabeform

## Produkt
- [ ] Spielkonzept: Setting, Ton, Länge, erstes Release. FA-Vorgabe (mind. 15) ist mit 49 erfüllt.
- [ ] Projektsteckbrief: Projektname, Ziel, Abgrenzung

## Rückfragen an Creative (Fabian, Benedict)
- [ ] **Meilenstein:** Was ist ein Meilenstein? Vorschlag: ein benanntes Flag im Lösungsweg, das die Engine beim Lösen eines Rätsels setzt (FA-G-03). Der [Asset-Vertrag](architektur/asset-vertrag/gegenstand.md#rezept) nimmt das bis zur Antwort an (Issue #71).
- [ ] **Ressourcen:** Wenn sie unbegrenzt sind (FA-G-06), sind sie dann Inventargegenstände, oder reicht ein freigeschaltetes Rezept? Annahme im Asset-Vertrag: keine Inventargegenstände, Zutaten nur als Text im Rezeptbuch (Issue #76).
- [ ] **Verbrauch:** Wird ein Alchemiegegenstand beim Einsetzen verbraucht? Wird ein Questgegenstand beim Einsetzen verbraucht, und kann man ihn danach erneut erhalten (FA-G-07)? Der Asset-Vertrag lässt das je Einsatzort offen (`removeItem`). Annahme: Die Höchstmenge gilt für den Bestand im Inventar.
- [ ] **Ungültige Kombination:** Bekommt der Spieler eine Rückmeldung, z. B. einen Text der Figur (FA-G-04)? Annahme im Asset-Vertrag: der Standardtext `defaults.combine` aus `game.json`.

- [ ] **Artstyle:** Trägt Creative den Vorschlag „Scherenschnitt im Dämmerlicht“ mit ([Artstyle](creative/artstyle.md), Issue #1)?

## Rückfragen an die Architektur (Lars, Benedict)
- [ ] **NF-E-03, Messbedingungen:** Vorschlag steht im Kriterium (Assets geladen, ungedrosselt, Median aus 5 Läufen). Architektur bestätigt?
- [ ] **NF-E-02, Gate:** Die Bildrate wird manuell gemessen. Zusätzlich ein CI-Näherungswert (Playwright-Trace mit CPU-Drosselung, Frame-Zeit)?
- [ ] **Vollständige N-Liste:** N-02, N-03, N-05, N-08 bis N-10 fehlen noch.

Beantwortet 2026-11-19 (siehe [Entscheidungen](entscheidungen.md)):
- Inhaltsformat für Gegenstände: im [Asset-Vertrag](architektur/asset-vertrag/gegenstand.md), Entwurf
- FA-E-07-Einheit (viewBox-Einheiten) und Klick außerhalb der Fläche: im Katalog (FA-E-07, FA-E-09)
- E-Liste: als Architektur-Liste erarbeitet, im Katalog als FA-E-02 bis FA-E-22
- `content/` als Wurzel

## Asset-Vertrag und Werkzeuge
- [ ] **Spike Claude Design:** Erzeugt Claude Design eine einzelne SVG ohne `<style>`, `<text>`, `<image>`? Bleiben IDs und `data-part` erhalten? Ergebnis in den [Asset-Vertrag](architektur/asset-vertrag/README.md#spike-claude-design), danach Status „verbindlich“.
- [ ] **Abstimmung Schema:** Der Asset-Vertrag ist der Schema-Entwurf aus Issue #69. Abstimmung mit Fabian und Ivan steht aus.
- [ ] **Ton und Musik:** Spätere Erweiterung des Vertrags. Würde NF-W-01 über SVG und JSON hinaus erweitern.
- [ ] **Flags:** In v1 nur boolesch. Reicht das für die Rätsel aus dem Spielkonzept, oder braucht es Zähler?

## Technik
- [ ] Rulesets auf GitHub einrichten (EP-02 bis EP-04, EP-11), sobald das Team Zugriff hat
- [ ] Agenten-Werkzeug: bestimmt die Umsetzung von EP-12 und EP-15
- [ ] Speicherort der Spielstände: Browser oder Server (NF-V-03). Ein Server würde die nicht übernommenen Gates wieder relevant machen.
- [ ] Claim gegen Doppelarbeit: bei 7 Personen plus Agenten wahrscheinlich nötig

## Mit dem Team bestätigen
- [ ] Zusage: 16 NF, 49 FA, 24 EP
- [ ] Im Planning am 26.11. prüfen, ob der Umfang von 49 FA im Semester realistisch ist (Qualitätskriterium 5). Die Vorschläge der Architektur und aus Issue #78 stehen seit 2026-11-21 im Katalog.
- [ ] Akzeptanz-Vorschläge NF-A-01 (Browser) und NF-A-02 (ab 1280 px Fensterbreite) bestätigen
- [ ] Personas P-01 bis P-03 als Arbeitsgrundlage, dazu der Vorschlag P-04 Creative ([Autoren-Workflow](architektur/autoren-workflow.md#persona-vorschlag-p-04))
