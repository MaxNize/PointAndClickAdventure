# Dokumentation

## Lesereihenfolge

| Schritt | Dokument | Ergebnis |
|---|---|---|
| 0 | [Vorgaben aus dem Modul](vorgaben-modul.md) | Lieferumfang, Tabellenformat, Qualitätskriterien |
| 1 | [Stakeholder und Rollen](voranalyse/01-stakeholder-und-rollen.md) | 6 Stakeholder, 2 Systemrollen, 6 Projektrollen mit Besetzung |
| 2 | [Personas](voranalyse/02-personas.md) | 3 Proto-Personas mit Abdeckungsmatrix |
| 3 | [Anforderungen](voranalyse/03-anforderungen.md) | 16 NF, 11 FA (Engine, Entwicklungsmodus), 15 Prozess-Gates |
| – | [Engine-Konzept](architektur/engine-konzept.md) | Architektur-Vorgabe mit ID-Zuordnung |

Begleitend: [Entscheidungen](entscheidungen.md) · [Offene Fragen](offene-fragen.md) · [Quellen](quellen.md)

## ID-Schema

Jede Stufe verweist über IDs auf die nächste. So lässt sich jede Anforderung auf eine Persona oder eine Quelle zurückführen.

| Präfix | Bedeutung | Definiert in |
|---|---|---|
| `SH-nn` | Stakeholder | Stakeholder und Rollen |
| `SR-nn` | Systemrolle (Spieler, Entwickler) | Stakeholder und Rollen |
| `PR-nn` | Projektrolle (PO, SM, Architekt, …) | Stakeholder und Rollen |
| `P-nn` | Persona | Personas |
| `NF-<A\|V\|E\|W>-nn` | Nicht-funktionale Anforderung nach Akzeptanz, Verlässlichkeit, Effizienz, Wartbarkeit | Anforderungen |
| `FA-<bereich>-nn` | Funktionale Anforderung: `FA-E` = Engine (Nummern aus der Architektur-Liste), `FA-DEV` = Entwicklungsmodus | Anforderungen |
| `EP-nn` | Entwicklungsprozess und Gates | Anforderungen |

IDs werden nie neu vergeben. Fällt eine Anforderung weg, bleibt die ID mit Vermerk „gestrichen“ stehen.

## Pflege

- Neue Anforderungen erfüllen die [Qualitätskriterien](vorgaben-modul.md#qualitätskriterien).
- Jede Entscheidung bekommt eine Zeile in [Entscheidungen](entscheidungen.md), jede offene Frage eine in [Offene Fragen](offene-fragen.md).
- Ändert sich eine Anforderung, werden Personas-Abdeckung und Verweise in derselben Änderung nachgezogen.
