"""Export des Demo-Raums „Lehrsaal der Alchemie“ in den Asset-Vertrag (docs/architektur/asset-vertrag/raum.md).

Liest die gebaute Demo (index.html, Ausgabe von build_scene.py) und schreibt room.svg und room.json.

- Spielstil wie in der Demo (body.dark und body.nolines): CSS wird zu Attributen.
- 1280x720 wird auf 1920x1080 umgerechnet. Die Koordinaten werden umgerechnet, es gibt keine scale-Gruppe,
  damit Teile, Ursprünge und Keyframes in Raumeinheiten stehen.
- <text> fällt weg (verboten im Vertrag). Die Texte stehen im Bericht.
- Zustände aus show() werden Raumteile mit data-part, CSS-Animationen werden Raumanimationen.
- Hotspots aus der Tabelle HS im Template, Laufbereich und Tiefe aus FLOOR_MIN/FLOOR_MAX und depthScale.

Aufruf aus dem Repo-Root:  python docs/creative/temp/Charaktere/export/export_raum.py [zielordner]
Standardziel: content/rooms/lehrsaal
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(__file__))
from export_contract import Q, SVG, inline_css, kebab, parse_css  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DEMO = os.path.join(os.path.dirname(HERE), "Alchemistin", "akademie-der-alchemie", "akademie-der-alchemie")
F = 1.5  # 1280 -> 1920
ROOM_ID = "lehrsaal"

# Zustände (show/hide in scene_template.html) -> Raumteil. Flags vergibt die Spiellogik, hier nur Vorschläge.
PARTS = {
    "puddle": ("pfuetze", {"flag": "lehrsaal.eis-geschmolzen"}),
    "iceBlock": ("eisblock", {"not": {"flag": "lehrsaal.eis-geschmolzen"}}),
    "keyLoose": ("schluessel-lose", {"all": [{"flag": "lehrsaal.eis-geschmolzen"}, {"not": {"flag": "lehrsaal.schluessel-genommen"}}]}),
    "crystal": ("kristall", {"not": {"flag": "lehrsaal.kristall-genommen"}}),
    "plantDead": ("pflanze-vertrocknet", {"not": {"flag": "lehrsaal.ranke-gewachsen"}}),
    "vine": ("ranke", {"flag": "lehrsaal.ranke-gewachsen"}),
    "fire": ("feuer", {"flag": "lehrsaal.athanor-an"}),
    "doorPanel": ("tuer-zu", {"not": {"flag": "lehrsaal.tuer-offen"}}),
    "doorLeaf": ("tuer-offen", {"flag": "lehrsaal.tuer-offen"}),
}
# HS-ID im Template -> Hotspot-Name im Raum
HOTSPOTS = {"ice": "eisblock", "window": "fenster", "crystal": "kristall", "books": "buecher", "water": "wasserkrug",
            "earth": "erdtopf", "iron": "eisenspaene", "plant": "pflanze", "owl": "eule", "board": "tafel",
            "cauldron": "kessel", "furnace": "athanor", "door": "tuer"}
GEOMETRY = {"x", "y", "width", "height", "cx", "cy", "r", "rx", "ry", "x1", "y1", "x2", "y2", "stroke-width"}


def num(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def scale_path(d):
    """Skaliert alle Koordinaten eines Pfads. Bei A bleiben Drehwinkel und Flags unverändert."""
    out, cmd, i = [], None, 0
    for tok in re.findall(r"[A-Za-z]|-?\d*\.?\d+(?:e-?\d+)?", d):
        if tok.isalpha():
            cmd, i = tok, 0
            out.append(tok)
            continue
        keep = cmd in "Aa" and i % 7 in (2, 3, 4)
        out.append(tok if keep else num(float(tok) * F))
        i += 1
    return " ".join(out)


def scale_transform(t):
    def rot(m):
        a, *c = m.group(1).replace(",", " ").split()
        return "rotate(" + " ".join([a] + [num(float(n) * F) for n in c]) + ")"
    t = re.sub(r"rotate\(([^)]*)\)", rot, t)
    return re.sub(r"translate\(([^)]*)\)", lambda m: "translate(" + " ".join(num(float(n) * F) for n in m.group(1).replace(",", " ").split()) + ")", t)


def scale_tree(el, in_gradient=False):
    in_gradient = in_gradient or el.tag in (Q("linearGradient"), Q("radialGradient"))
    if not in_gradient:
        for k, v in list(el.attrib.items()):
            if k in GEOMETRY and re.fullmatch(r"-?\d*\.?\d+", v):
                el.set(k, num(float(v) * F))
            elif k == "d":
                el.set(k, scale_path(v))
            elif k == "transform":
                el.set(k, scale_transform(v))
    for c in el:
        scale_tree(c, in_gradient)


def read_demo():
    html = open(os.path.join(DEMO, "index.html"), encoding="utf-8").read()
    start = html.index('<svg id="svg"')
    end = html.index("</svg>", html.index('<g id="hits">')) + len("</svg>")
    root = ET.fromstring(html[start:end].replace("var(--brew,#9be7ff)", "#9be7ff"))
    css = []
    for sels, body in re.findall(r"([^{}]+)\{([^{}]*)\}", "".join(re.findall(r"<style>(.*?)</style>", html, re.S))):
        keep = [s.strip()[len(p):] for s in sels.split(",") for p in ("body.dark #scene ", "body.nolines #scene ") if s.strip().startswith(p)]
        if keep:
            css.append(",".join(keep) + "{" + body.replace("var(--brew,#9be7ff)", "#9be7ff") + "}")
    template = open(os.path.join(DEMO, "source", "scene_template.html"), encoding="utf-8").read()
    hs = re.findall(r"\['(\w+)','([^']+)',(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)\]", template)
    return root, "\n".join(css), hs


def collect_texts(scene):
    parent = {c: p for p in scene.iter() for c in p}
    texts = [t for t in scene.iter(Q("text"))]
    for t in texts:
        parent[t].remove(t)
    return ["".join(t.itertext()) for t in texts]


def mark_parts(scene):
    parent = {c: p for p in scene.iter() for c in p}
    for el in scene.iter():
        old = el.get("id")
        if old in PARTS:
            el.set("data-part", PARTS[old][0])
            style = re.sub(r"display\s*:\s*none;?", "", el.get("style", "")).strip()
            el.attrib.pop("style", None) if not style else el.set("style", style)
        if old == "doorway":  # Tür offen: Licht statt dunkler Öffnung
            light = ET.Element(Q("path"), {"d": el.get("d"), "fill": "url(#doorLight)", "data-part": "tuer-licht"})
            siblings = list(parent[el])
            parent[el].insert(siblings.index(el) + 1, light)


def bbox(el):
    nums = [float(n) for n in re.findall(r"-?\d*\.?\d+", el.get("d", ""))]
    if nums:
        xs, ys = nums[0::2], nums[1::2]
        return min(xs), min(ys), max(xs), max(ys)
    pts = [(float(c.get("cx")), float(c.get("cy")), float(c.get("r"))) for c in el.iter(Q("circle"))]
    return min(x - r for x, _, r in pts), min(y - r for _, y, r in pts), max(x + r for x, _, r in pts), max(y + r for _, y, r in pts)


def animations(scene):
    """CSS-Animationen der Demo (scene_template.html) als Raumanimationen, Werte bereits in 1920er-Einheiten."""
    anims, n = [], {"flamme": 0, "blase": 0}
    for el in scene.iter():
        cls = (el.get("class") or "").split()
        if "flicker" in cls or "flicker2" in cls:
            n["flamme"] += 1
            part = f"flamme-{n['flamme']}"
            x0, _, x1, y1 = bbox(el)
            hi, lo = {"scaleY": 1.12, "scaleX": 0.94, "ease": "inOut"}, {"scaleY": 1, "scaleX": 1, "ease": "inOut"}
            half = 0.35 if "flicker" in cls else 0.27
            a, b = (lo, hi) if "flicker" in cls else (hi, lo)
            anims.append({"part": part, "duration": half * 2, "origin": [num((x0 + x1) / 2 * F), num(y1 * F)],
                          "keyframes": [{"t": 0, **a}, {"t": half, **b}, {"t": half * 2, **a}]})
        elif "blink" in cls:
            part = "eule-pupillen"
            x0, y0, x1, y1 = bbox(el)
            anims.append({"part": part, "duration": 5, "origin": [num((x0 + x1) / 2 * F), num((y0 + y1) / 2 * F)],
                          "keyframes": [{"t": 0, "scaleY": 1}, {"t": 4.7, "scaleY": 1}, {"t": 4.8, "scaleY": 0.1}, {"t": 5, "scaleY": 1}]})
        elif "bub" in cls:
            n["blase"] += 1
            part = f"blase-{n['blase']}"
            delay = {"b2": 0.5, "b3": 1.0}.get(next((c for c in cls if c in ("b2", "b3")), ""), 0)
            anim = {"part": part, "duration": 1.6, "keyframes": [
                {"t": 0, "y": 0, "opacity": 0}, {"t": 0.32, "y": -10.2, "opacity": 0.9, "ease": "in"}, {"t": 1.6, "y": -51, "opacity": 0, "ease": "in"}]}
            anims.append({**anim, "delay": delay} if delay else anim)
        elif el.get("id") == "crystal":
            part = PARTS["crystal"][0]
            anims.append({"part": part, "duration": 4, "keyframes": [{"t": 0, "opacity": 0.85}, {"t": 2, "opacity": 1, "ease": "inOut"}, {"t": 4, "opacity": 0.85, "ease": "inOut"}]})
            continue
        else:
            continue
        el.set("data-part", part)
    return anims


def build(out_dir):
    root, css, hs = read_demo()
    defs = root.find(Q("defs"))
    scene = next(g for g in root.iter(Q("g")) if g.get("id") == "scene")
    rules, skipped = parse_css(css)
    report = [f"nicht übernommene CSS-Selektoren: {sorted(set(skipped)) or '-'}"]
    report.append(f"entfernte Texte: {collect_texts(scene)}")
    mark_parts(scene)
    anims = animations(scene)
    hidden = inline_css(scene, rules)
    report.append(f"{hidden} ausgeblendete Elemente entfernt")

    vignette = [el for el in scene if el.get("data-part") is None and "url(#vignette)" in (el.get("fill") or "")]
    out = ET.Element(Q("svg"), {"viewBox": "0 0 1920 1080"})
    out.append(defs)
    bg = ET.SubElement(out, Q("g"), {"id": "layer-background"})
    for el in list(scene):
        if el not in vignette:
            bg.append(el)
    fg = ET.SubElement(out, Q("g"), {"id": "layer-foreground"})
    fg.extend(vignette)
    hot = ET.SubElement(out, Q("g"), {"id": "hotspots"})
    for hid, _, x, y, w, h, _, _ in hs:
        ET.SubElement(hot, Q("rect"), {"id": f"hotspot-{HOTSPOTS[hid]}", "x": x, "y": y, "width": w, "height": h, "fill": "transparent"})
    scale_tree(out)

    # IDs in Kebab-Case, Verweise mitziehen, ungenutzte Defs (z. B. der Figur) entfernen
    mapping = {el.get("id"): kebab(el.get("id")) for el in out.iter() if el.get("id")}
    for el in out.iter():
        for k, v in list(el.attrib.items()):
            if k == "id":
                el.set(k, mapping[v])
            elif "url(#" in v:
                el.set(k, re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{mapping.get(m.group(1), m.group(1))})", v))
    text = ET.tostring(out, encoding="unicode")
    for d in list(defs):
        if f"#{d.get('id')}" not in text:
            defs.remove(d)

    look = lambda name: [{"type": "say", "text": f"{name}."}]  # noqa: E731  Platzhalter bis zur Spiellogik
    room = {
        "schemaVersion": 1, "id": ROOM_ID, "name": "Lehrsaal der Alchemie",
        "walkable": {"outer": [[90, 967.5], [1830, 967.5], [1830, 1057.5], [90, 1057.5]]},
        "depth": {"far": {"y": 967.5, "scale": round(0.44 / 0.52, 3)}, "near": {"y": 1057.5, "scale": 1}},
        "spawns": {"start": {"x": 450, "y": 1035, "facing": "front"}},
        "hotspots": {f"hotspot-{HOTSPOTS[hid]}": {"name": name, "walkTo": {"x": float(num(int(wx) * F)), "y": float(num(int(wy) * F))},
                                                  "verbs": {"look": look(name)}} for hid, name, _, _, _, _, wx, wy in hs},
        "parts": {name: {"visibleIf": cond} for name, cond in PARTS.values()},
        "animations": [{**a, "origin": [float(v) for v in a["origin"]]} if "origin" in a else a for a in anims],
    }
    room["parts"]["tuer-licht"] = {"visibleIf": {"flag": "lehrsaal.tuer-offen"}}
    os.makedirs(out_dir, exist_ok=True)
    ET.ElementTree(out).write(os.path.join(out_dir, "room.svg"), encoding="unicode")
    with open(os.path.join(out_dir, "room.json"), "w", encoding="utf-8") as f:
        json.dump(room, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return report


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join("content", "rooms", ROOM_ID)
    for line in build(target):
        print(line)
    print(f"Raum nach {target}")
