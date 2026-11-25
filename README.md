# Point-and-Click-Adventure

Ein Point-and-Click-Adventure als Web App. Teamprojekt im Modul Agile Software Engineering und Softwaretechnik.

- **Agentic first:** KI-Agenten schreiben Code und Spielinhalte. Menschen setzen Ziele, prüfen und geben frei.
- **Quality Gating:** Jede Anforderung hat ein Akzeptanzkriterium, das ein Skript prüft. Ein roter Lauf blockiert den Merge.

**Stand:** Projektgerüst steht (EP-16). Die Engine entsteht nach dem [Umsetzungsplan](docs/architektur/umsetzungsplan.md).

**Stack:** React, TypeScript, Vite. Räume als SVG mit Zod-validierter JSON-Definition, Animation mit GSAP. Details: [Engine-Konzept](docs/architektur/engine-konzept.md).

## Lokal starten

Voraussetzungen: Node 22 (siehe `.nvmrc`), GNU Make (Windows: `scoop install make`).

```sh
make setup      # einmal pro Klon: Git-Hooks und Abhängigkeiten (npm ci)
npm run dev     # Spiel im Browser unter der angezeigten Adresse
npm run build   # Produktions-Build nach dist/
make ci         # alle Prüfungen, wie in der CI
```

## Dokumentation

Start: [docs/README.md](docs/README.md). Kurz:

1. [Vorgaben aus dem Modul](docs/vorgaben-modul.md)
2. [Stakeholder und Rollen](docs/voranalyse/01-stakeholder-und-rollen.md)
3. [Personas](docs/voranalyse/02-personas.md)
4. [Anforderungen](docs/voranalyse/03-anforderungen.md)
5. [Engine-Konzept](docs/architektur/engine-konzept.md)
6. [Gegenstände](docs/creative/gegenstaende.md)
7. [Asset-Vertrag](docs/architektur/asset-vertrag/README.md) und [Autoren-Workflow](docs/architektur/autoren-workflow.md): für alle, die Inhalte erstellen

## Team

| Rolle | Person |
|---|---|
| Product Owner | Max |
| Scrum Master | Dimi |
| Architektur | Lars, Benedict |
| Creative | Fabian, Benedict |
| Fullstack | Ivan, Mahmud |

## Mitarbeiten

Für Menschen und Agenten gelten dieselben Regeln: [AGENTS.md](AGENTS.md).
