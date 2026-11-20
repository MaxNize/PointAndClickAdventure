# Akademie der Alchemie – Demo-Szene

## Schnellstart
`index.html` ist komplett eigenständig (alle Grafiken als SVG, CSS und JavaScript in einer Datei).
Im Browser öffnen genügt. In VS Code: Erweiterung **Live Server** installieren, Rechtsklick auf
`index.html` → *Open with Live Server*.

## Ordner
- `index.html` – das spielbare Ergebnis
- `assets/` – die Figur als einzelne SVGs (Front, Seite, Rücken)
- `source/` – die Generator-Skripte, aus denen `index.html` gebaut wird

## Neu bauen (nach Änderungen an den Skripten)
Voraussetzung: Python 3. Im Ordner `source/`:

```
python build_scene.py
```

Das erzeugt `alchemieschule_demo.html` neu (umbenennen bzw. nach `../index.html` kopieren).

| Datei | Inhalt |
|---|---|
| `gen.py` | Grundformen, Frontkopf, Farbpaletten (CSS) |
| `anime2.py` | Körper der Frontansicht |
| `anime_dark.py` | Scherenschnitt-Stil der Figur |
| `side.py` | Seitenansicht (Laufen links/rechts) |
| `back.py` | Rückansicht (Laufen nach hinten) |
| `scene_template.html` | Spiellogik (JavaScript), Oberfläche, Platzhalter |
| `build_scene.py` | Raum (SVG), Raum-Stile, setzt alles zusammen |

## Spieldaten anpassen (in `scene_template.html`, Abschnitt `/* Daten */`)
- `ITEMS` – Gegenstände (Name, Farbe, Beschreibung)
- `RECIPES` – Alchemie-Rezepte `[Zutat A, Zutat B, Ergebnis]`
- `HS` – klickbare Bereiche: `[id, Name, x, y, Breite, Höhe, Laufziel x, Laufziel y]`
- `OBJECTIVES`, `HINTS` – Aufgaben und Tipps der Eule
