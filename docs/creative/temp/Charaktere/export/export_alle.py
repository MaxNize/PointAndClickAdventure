"""Exportiert alle Figuren in den Asset-Vertrag nach content/characters/<figur-id>/.

Aufruf aus dem Repo-Root:  python docs/creative/temp/Charaktere/export/export_alle.py [zielordner]
Standardziel: content/characters
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from export_contract import export_figure  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CHARS = os.path.dirname(HERE)
NEUTRAL = "#e8dcc8"  # Platzhalter: Figuren ohne Leuchtfarbe im Styleguide, Entscheidung durch Creative offen


def scherenschnitt(folder, prefix):
    return {v: os.path.join(CHARS, folder, f"{prefix}_{d}_scherenschnitt.svg")
            for v, d in (("front", "front"), ("side", "seite"), ("back", "rueck"))}


ALCHEMISTIN = os.path.join("Alchemistin", "akademie-der-alchemie", "akademie-der-alchemie", "assets")

# (figur-id, Name, Textfarbe aus Styleguide 8.2, Dateien)
FIGUREN = [
    ("alchemistin", "Alchemistin", "#ffcf6b",
     {v: os.path.join(CHARS, ALCHEMISTIN, f"alchemistin_{d}.svg") for v, d in (("front", "front"), ("side", "seite"), ("back", "rueck"))}),
    ("lehrling", "Lehrling", "#7fe3ff", scherenschnitt(os.path.join("Lehrling", "lehrling", "lehrling", "svg"), "lehrling")),
    ("meister", "Meister", "#ffe066", scherenschnitt(os.path.join("meister", "meister", "svg"), "meister")),
    ("erzalchemist", "Erzalchemist", "#ffb35a", scherenschnitt(os.path.join("erzalchemist", "erzalchemist", "svg"), "erzalchemist")),
    ("schmied", "Schmied", "#ff6a3c", scherenschnitt(os.path.join("schmied", "svg"), "schmied")),
    ("professor", "Professor Odilo Gernegroß", NEUTRAL, scherenschnitt(os.path.join("professor", "svg"), "professor")),
] + [
    (nid, name, NEUTRAL, scherenschnitt(os.path.join("npcs", "svg"), f"npc_{nid}"))
    for nid, name in [("lena", "Lena"), ("tobi", "Tobi"), ("grombart", "Herr Grombart"), ("seidel", "Frau Seidel"),
                      ("maren", "Maren"), ("fynn", "Fynn"), ("brandt", "Herr Brandt"), ("ilse", "Ilse"),
                      ("kurt", "Kurt"), ("yara", "Yara")]
]

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join("content", "characters")
    for fid, name, color, files in FIGUREN:
        print(fid)
        for line in export_figure(fid, name, color, files, os.path.join(target, fid)):
            print(line)
    print(f"{len(FIGUREN)} Figuren nach {target}")
