# Alchemie- und Questgegenstände

Vorgabe von Creative (PR-04), eingegangen 2026-11-17. Die Anforderungen stehen mit Projekt-IDs `FA-G-nn` in [Anforderungen](../voranalyse/03-anforderungen.md), Abschnitt 2.3. Die Zuordnung und alle Änderungen am Wortlaut stehen unten.

## Begriffe

| Begriff | Bedeutung | Quelle |
|---|---|---|
| Alchemiegegenstand | Gegenstand, den der Spieler über ein Rezept herstellt. Beliebig oft herstellbar. | FA-01, FA-06 |
| Questgegenstand | Gegenstand für ein bestimmtes Rätsel. Nicht herstellbar, nur in festgelegter Menge erhältlich, nur in vorgesehenen Kombinationen nutzbar. | FA-04, FA-05, FA-07 |
| Rezept | Eintrag im Rezeptbuch, der einen Alchemiegegenstand erzeugt. Wird über Meilensteine freigeschaltet. | FA-01, FA-03 |
| Rezeptbuch | Übersicht aller freigeschalteten Rezepte | FA-01, FA-03 |
| Meilenstein | noch nicht definiert (siehe [Offene Fragen](../offene-fragen.md)) | FA-03 |
| Ressource | Zutat für die Herstellung. Unbegrenzt verfügbar. | FA-06 |

## Zuordnung und Änderungen

Inhalt und Absicht sind unverändert. Geändert wurde nur, wo die [Qualitätskriterien](../vorgaben-modul.md#qualitätskriterien) verletzt waren.

| Creative | Projekt-ID | Änderung | Grund |
|---|---|---|---|
| FA-01 | FA-G-01 | Akzeptanzkriterium gekürzt | – |
| FA-02 | FA-G-02, FA-G-08 | in zwei Anforderungen geteilt: Rätsel lösen, Information freischalten | „zum Lösen von Rätseln oder zum Erhalt von Informationen“ ist eine Oder-Kette. Das Akzeptanzkriterium hatte drei mögliche Ergebnisse und war damit nicht eindeutig prüfbar. |
| FA-03 | FA-G-03 | „mit erreichten Meilenstein“ → „mit jedem erreichten Meilenstein“ | Grammatik |
| FA-04 | FA-G-04 | „miteinander oder mit anderen Gegenständen“ → „jede nicht vorgesehene Kombination mit einem Questgegenstand“ | Oder-Kette, gleiche Bedeutung |
| FA-05 | FA-G-05 | auf den Ausschluss aus dem Rezeptbuch gekürzt | Die Verwendung bei Rätseln deckt FA-G-02 bereits ab. Eine Anforderung pro Zeile. |
| FA-06 | FA-G-06 | „beliebig oft“ → 100-mal hintereinander | „beliebig oft“ ist nicht als Test ausführbar |
| FA-07 | FA-G-07 | „aufnehmen oder erhalten“ entfällt, Kriterium über den Inventarbestand | Oder-Kette |

## Originalfassung

| ID | Bereich | Nutzerrolle | Anforderung | Akzeptanzkriterium |
|---|---|---|---|---|
| FA-01 | Alchemiesystem | Spieler | Das System muss dem Spieler ermöglichen, mithilfe des Rezeptbuchs Alchemiegegenstände herzustellen. | Wählt der Spieler ein freigeschaltetes Rezept aus, wird der zugehörige Alchemiegegenstand erstellt und anschließend im Inventar angezeigt. |
| FA-02 | Alchemiesystem | Spieler | Das System muss dem Spieler ermöglichen, hergestellte Alchemiegegenstände zum Lösen von Rätseln oder zum Erhalt von Informationen zu verwenden. | Wird ein passender Alchemiegegenstand an der vorgesehenen Stelle eingesetzt, wird das zugehörige Rätsel gelöst, ein neuer Hinweis angezeigt oder eine Information freigeschaltet. |
| FA-03 | Rezeptbuch | Spieler | Das System muss das Rezeptbuch mit erreichten Meilenstein um neue Rezepte erweitern. | Beim Erreichen eines neuen Meilensteins werden die dafür vorgesehenen Rezepte automatisch freigeschaltet und im Rezeptbuch angezeigt. Rezepte aus vorherigen Meilensteilen bleiben verfügbar. |
| FA-04 | Questgegenstände | Spieler | Das System muss verhindern, dass Questgegenstände in einer nicht vorgesehenen Kombination miteinander oder mit anderen Gegenständen kombiniert werden. | Eine ungültige Kombination wird nicht ausgeführt. Die verwendeten Gegenstände bleiben unverändert erhalten und weiterhin im Inventar verfügbar. |
| FA-05 | Questgegenstände | Spieler | Das System muss Questgegenstände zur Verwendung bei Rätseln bereitstellen, ohne sie als herstellbare Gegenstände im Rezeptbuch aufzuführen. | Questgegenstände können an den vorgesehenen Rätseln verwendet werden, erscheinen jedoch nicht als Rezepte oder herstellbare Gegenstände im Rezeptbuch. |
| FA-06 | Ressourcenverwaltung | Spieler | Das System muss dem Spieler unbegrenzt viele Ressourcen für die Herstellung von Alchemiegegenständen zur Verfügung stellen. | Ein Alchemiegegenstand kann beliebig oft hergestellt werden, ohne dass die dafür benötigten Ressourcen dauerhaft aufgebraucht werden oder die Herstellung wegen fehlender Ressourcen blockiert wird. |
| FA-07 | Questgegenstände | Spieler | Das System muss die Verfügbarkeit von Questgegenständen auf die jeweils für die Quest vorgesehene Menge begrenzen. | Ein Questgegenstand kann nur in der festgelegten Anzahl erhalten werden. Nach Erreichen dieser Anzahl kann der Spieler keine weiteren Exemplare desselben Questgegenstands aufnehmen oder erhalten. |

## Folgen für das Engine-Konzept

Laut [Engine-Konzept](../architektur/engine-konzept.md) kommen alle Inhalte als JSON ins Spiel (NF-W-01). Die bisherige `items.json` kennt nur ID, Name und Beschreibung. Für FA-G braucht das Inhaltsformat zusätzlich:

- **Gegenstandstyp:** `alchemie` oder `quest` (FA-G-04, FA-G-05)
- **Höchstmenge** je Questgegenstand (FA-G-07)
- **Rezepte:** erzeugter Gegenstand, Zutaten, Meilenstein der Freischaltung (FA-G-01, FA-G-03)
- **Erlaubte Kombinationen** (FA-G-04)
- **Einsatzorte:** welcher Gegenstand an welchem Hotspot welches Rätsel löst oder welche Information freischaltet (FA-G-02, FA-G-08)

Der Content-Validator (NF-V-01) prüft damit auch, dass kein Rezept einen Questgegenstand erzeugt.
