# Vorgaben aus dem Modul

Modul: Agile Software Engineering und Softwaretechnik. Diese Vorgaben gelten für alle Anforderungen in [`voranalyse/03-anforderungen.md`](voranalyse/03-anforderungen.md). Menschen und Agenten prüfen jede neue Anforderung dagegen.

## Lieferumfang der Voranalyse

| Liefergegenstand | Vorgabe | Stand |
|---|---|---|
| Funktionale Anforderungen | mind. 15 | 11 (5 Engine, 6 Entwicklungsmodus), Rest folgt aus Spielkonzept und vollständiger Engine-Liste |
| Nicht-funktionale Anforderungen | mind. 5, gegliedert nach Akzeptanz, Verlässlichkeit, Effizienz, Wartbarkeit, messbar | 16 |
| Projektsteckbrief | Name, Ausgangssituation, Ziel (1–3 Sätze), Zielgruppe und Nutzerrollen, Abgrenzung, Tech-Stack (vorläufig), Entscheidungsbegründung | offen |

## Tabellenformat

| ID | Bereich | Nutzerrolle | Anforderung | Akzeptanzkriterium |
|---|---|---|---|---|
| FA-01 | Benutzerverwaltung | Nutzer | Das System muss dem Nutzer ermöglichen, sich mit E-Mail und Passwort zu registrieren. | Nach Registrierung kann sich der Nutzer einloggen; doppelte E-Mail wird abgelehnt. |

(Beispiel aus der Vorgabe.)

## Qualitätskriterien

Darauf prüfen sich die Teams gegenseitig:

1. **Testbar:** Man kann eindeutig sagen, ob die Anforderung erfüllt ist.
2. **Eine Anforderung pro Zeile:** keine „und/oder“-Ketten.
3. **Formulierung:** „Das System muss …“
4. **Keine Wörter ohne Messgröße:** schnell, einfach, benutzerfreundlich, intuitiv, sicher, modern. Stattdessen z. B. „Ladezeit unter 2 Sekunden“.
5. **Realistisch:** mit der Teamgröße im Semester schaffbar. Was zugesagt ist, wird später daran gemessen.
