# Personas

Schritt 2 der Voranalyse. Je eine Persona pro Spieler-Stakeholder aus [Stakeholder und Rollen](01-stakeholder-und-rollen.md), dazu eine für die Systemrolle Entwickler. Weiter mit [Anforderungen](03-anforderungen.md).

**Status: Proto-Personas.** Sie beruhen auf Annahmen des Teams und sind unabhängig vom Spielinhalt. Widerspricht eine Rückmeldung von Spielern einer Annahme, wird die Persona angepasst und in den [Entscheidungen](../entscheidungen.md) vermerkt.

**Rahmen:** Das Spiel läuft im Desktop-Browser. Smartphones und Tablets sind ausgeschlossen.

## P-01 · Lena, die Gelegenheitsspielerin

| | |
|---|---|
| Stakeholder / Rolle | SH-04 / SR-01 Spieler |
| Steckbrief | 24, Auszubildende, spielt in der Mittagspause am Laptop |
| Gerät | Laptop, Chrome oder Firefox, Touchpad |
| Spielverhalten | 10–15 min am Stück, oft unterbrochen, spielt nur ohne Installation |
| Ziel | Dort weiterspielen, wo sie aufgehört hat |
| Frust | Lange Ladezeiten, verlorener Fortschritt, Warten beim Raumwechsel |
| Zitat | „Wenn ich nach der Pause alles nochmal machen muss, bin ich raus.“ |
| Treibt | NF-A-01, NF-A-02, NF-V-03, NF-E-01, NF-E-03 |

## P-02 · Jonas, der Genre-Fan

| | |
|---|---|
| Stakeholder / Rolle | SH-05 / SR-01 Spieler |
| Steckbrief | 38, Softwareentwickler, mit klassischen Adventures aufgewachsen |
| Gerät | Desktop, Maus, großer Bildschirm |
| Spielverhalten | Abends 1–2 h, probiert systematisch jede Kombination |
| Ziel | Rätsel, die mit Logik lösbar sind |
| Frust | Sackgassen ohne Ausweg, Pixelsuche, ruckelnde Animationen, Fehler, die den Fortschritt blockieren |
| Zitat | „Ein Rätsel darf schwer sein. Es darf nur nicht kaputt sein.“ |
| Treibt | NF-V-01, NF-V-02, NF-V-04, NF-E-02; Ausbau: Sackgassen-Suche |

## P-03 · Kim, aus dem Team

| | |
|---|---|
| Stakeholder / Rolle | SH-02 / SR-02 Entwickler |
| Steckbrief | Teammitglied, testet Rätsel und lässt Agenten Fehler beheben |
| Gerät | Desktop, Entwicklungs-Build |
| Arbeitsweise | Prüft eine Stelle im späten Spielverlauf mehrmals am Tag |
| Ziel | In Sekunden an jeder Stelle des Spiels sein |
| Frust | Jedes Mal von vorn spielen, Fehler nicht nachstellen können, veraltete Testspielstände |
| Zitat | „Ich will den Bug-Report öffnen und direkt im Fehler stehen.“ |
| Treibt | FA-DEV-01 bis FA-DEV-06, NF-V-02 |

## Abdeckung

| Anforderung | P-01 | P-02 | P-03 |
|---|---|---|---|
| NF-A-01 Browser | ● | ● | |
| NF-A-02 Fenstergröße | ● | ● | |
| NF-V-01 Inhalt konsistent | | ● | |
| NF-V-02 Lösbarkeit | | ● | ● |
| NF-V-03 Spielstand | ● | | |
| NF-V-04 Fehlerraum | | ● | |
| NF-E-01 Ladezeit | ● | | |
| NF-E-02 Bildrate | | ● | |
| NF-E-03 Raumwechsel | ● | | |
| FA-E Engine | ● | ● | |
| FA-DEV Entwicklungsmodus | | | ● |

NF-W-01 bis NF-W-07 dienen keiner Persona direkt. Sie sichern, dass die übrigen Anforderungen unter Agentenarbeit haltbar bleiben (SH-01, SH-02).
