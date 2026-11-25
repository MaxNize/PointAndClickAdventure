"""Export der Generator-Figuren in den Asset-Vertrag (docs/architektur/asset-vertrag/figur.md).

Liest die drei Scherenschnitt-SVGs einer Figur (front, seite, rueck) und schreibt
character.svg (eine Datei mit view-front, view-side, view-back) und character.json.

- CSS aus <style> wird zu Attributen. CSS gewinnt über vorhandene Attribute, wie im Browser.
- Elemente mit display:none, <title> und das Hintergrund-Rechteck fallen weg.
- IDs werden zu Kebab-Case, Verweise (url(#…), href) ziehen mit. Gleiche Defs werden zusammengelegt.
- Rig-IDs bekommen data-part, jede Ansicht eine Hülle data-part="koerper" und außerhalb davon den Anker.
"""
import json
import os
import re
import xml.etree.ElementTree as ET

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def Q(tag):
    return f"{{{SVG}}}{tag}"


FOOT = (200, 773)  # Fußpunkt aller Figuren (Styleguide, Gelenkpunkte)
DEMO_SCALE = 0.52 * 1.5  # Größe vorn in der Demo-Szene (1280x720), umgerechnet auf 1920x1080

# Rig-ID der Generatoren -> data-part. „links/rechts“ vorerst wie im Bild, aus wessen Sicht ist offen.
PARTS = {
    "front": {"front_leg_l": "bein-links", "front_leg_r": "bein-rechts", "boot_l": "stiefel-links",
              "boot_r": "stiefel-rechts", "arm_l": "arm-links", "arm_r": "arm-rechts", "head": "kopf"},
    "side": {"side_leg_near": "bein-links", "side_leg_far": "bein-rechts", "side_leg_near_shin": "bein-links-unten",
             "side_leg_far_shin": "bein-rechts-unten", "side_arm_near": "arm-links", "side_arm_far": "arm-rechts",
             "side_arm_near_fore": "arm-links-unten", "side_arm_far_fore": "arm-rechts-unten", "side_head": "kopf"},
    "back": {"back_leg_l": "bein-links", "back_leg_r": "bein-rechts", "back_arm_l": "arm-links",
             "back_arm_r": "arm-rechts", "back_head": "kopf"},
}
# Drehpunkte aus dem Styleguide und scene_template.html. Bezugssystem noch offen (Wurzel-Skalierung).
PIVOTS = {
    "side": {"bein-links": [205, 352], "bein-rechts": [205, 352], "bein-links-unten": [206, 550],
             "bein-rechts-unten": [206, 550], "arm-links": [205, 232], "arm-rechts": [205, 232],
             "arm-links-unten": [204, 288], "arm-rechts-unten": [204, 288]},
    "front": {},
    "back": {"arm-links": [168, 230], "arm-rechts": [232, 230]},
}


def kebab(s):
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", s).replace("_", "-").lower()
    return re.sub(r"-+", "-", s).strip("-")


def parse_css(text):
    """Regeln mit .klasse, #id oder *. Andere Selektoren landen in `skipped` und im Bericht."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    rules, skipped = [], []
    for order, (sels, body) in enumerate(re.findall(r"([^{}]+)\{([^{}]*)\}", text)):
        decls = dict((k.strip(), v.strip()) for k, v in (d.split(":", 1) for d in body.split(";") if ":" in d))
        for sel in (s.strip() for s in sels.split(",")):
            if re.fullmatch(r"#[\w-]+", sel):
                rules.append(((1, 0), order, sel, decls))
            elif re.fullmatch(r"\.[\w-]+", sel):
                rules.append(((0, 1), order, sel, decls))
            elif sel == "*":
                rules.append(((0, 0), order, sel, decls))
            else:
                skipped.append(sel)
    return rules, skipped


def matches(sel, el):
    if sel == "*":
        return True
    if sel.startswith("#"):
        return el.get("id") == sel[1:]
    return sel[1:] in (el.get("class") or "").split()


def inline_css(root, rules):
    parent = {c: p for p in root.iter() for c in p}
    hidden = []
    for el in root.iter():
        props = {}
        for _, _, _, decls in sorted((r for r in rules if matches(r[2], el)), key=lambda r: (r[0], r[1])):
            props.update(decls)
        if props.pop("display", None) == "none":
            hidden.append(el)
        for k, v in props.items():
            el.set(k, v)
        el.attrib.pop("class", None)
    for el in hidden:
        if el in parent:
            parent[el].remove(el)
    return len(hidden)


def load_view(path):
    root = ET.parse(path).getroot()
    vb = root.get("viewBox")
    rules, skipped = parse_css("".join(s.text or "" for s in root.findall(Q("style"))))
    for tag in ("style", "title"):
        for e in root.findall(Q(tag)):
            root.remove(e)
    box = [float(n) for n in vb.split()]
    for r in root.findall(Q("rect")):  # Hintergrund über die ganze viewBox
        if [float(r.get(a, "0")) for a in ("x", "y", "width", "height")] == box:
            root.remove(r)
    for g in root.findall(Q("g")):
        if g.get("id") == "background":
            root.remove(g)
    return root, vb, skipped, inline_css(root, rules)


def _rename(view, root, defs_out, seen_defs, used_ids):
    """Vergibt neue IDs, übernimmt Defs (dedupliziert) und setzt data-part."""
    mapping = {}
    for d in root.findall(Q("defs")):
        for el in list(d):
            old, new, body = el.get("id"), kebab(el.get("id")), ET.tostring(el)
            if new in seen_defs and seen_defs[new] != body:
                new = f"{new}-{view}"
            mapping[old] = new
            if new not in seen_defs:
                seen_defs[new] = body
                el.set("id", new)
                defs_out.append(el)
        root.remove(d)
    for el in root.iter():
        old = el.get("id")
        if old and old not in mapping:
            new = kebab(old)
            new = f"{new}-{view}" if new in used_ids or new in seen_defs else new
            mapping[old] = new
            used_ids.add(new)
    for el in root.iter():
        if el.get("id") in PARTS[view]:
            el.set("data-part", PARTS[view][el.get("id")])
        for k, v in list(el.attrib.items()):
            if k == "id":
                el.set(k, mapping.get(v, v))
            elif "url(#" in v:
                el.set(k, re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{mapping.get(m.group(1), m.group(1))})", v))
            elif k.endswith("href") and v.startswith("#"):
                el.set(k, "#" + mapping.get(v[1:], v[1:]))


def export_figure(fid, name, text_color, files, out_dir):
    """files: {"front": pfad, "side": pfad, "back": pfad}. Gibt Berichtszeilen zurück."""
    views, vbs, report = {}, set(), []
    for view, path in files.items():
        root, vb, skipped, removed = load_view(path)
        views[view] = root
        vbs.add(vb)
        note = f", nicht übernommen: {sorted(set(skipped))}" if skipped else ""
        report.append(f"  {view}: {removed} versteckte Elemente entfernt{note}")
        # Unaufgelöste Platzhalter aus dem Generator, z. B. ein vergessenes f vor einem String mit {…}
        for el in root.iter():
            for k, v in el.attrib.items():
                if "{" in v:
                    report.append(f"  WARNUNG {view}: <{el.tag.split('}')[1]} {k}=\"{v[:40]}…\"> enthält einen Platzhalter, Quelle prüfen")
    if len(vbs) != 1:
        raise ValueError(f"{fid}: Ansichten haben verschiedene viewBoxen {vbs}")
    vb = vbs.pop()

    out_root = ET.Element(Q("svg"), {"viewBox": vb})
    defs_out = ET.SubElement(out_root, Q("defs"))
    seen_defs, used_ids = {}, set()
    for view, root in views.items():
        _rename(view, root, defs_out, seen_defs, used_ids)
        g_view = ET.SubElement(out_root, Q("g"), {"id": f"view-{view}"})
        koerper = ET.SubElement(g_view, Q("g"), {"data-part": "koerper"})
        for child in list(root):
            koerper.append(child)
        ET.SubElement(g_view, Q("circle"), {"data-part": "anchor", "cx": str(FOOT[0]), "cy": str(FOOT[1]),
                                            "r": "1", "fill": "none"})
    text = ET.tostring(out_root, encoding="unicode")
    for d in list(defs_out):  # ungenutzte Defs, z. B. Verläufe der ausgeblendeten Augen
        if f"#{d.get('id')}" not in text:
            defs_out.remove(d)

    os.makedirs(out_dir, exist_ok=True)
    ET.ElementTree(out_root).write(os.path.join(out_dir, "character.svg"), encoding="unicode")
    char = {"schemaVersion": 1, "id": fid, "name": name, "height": round(float(vb.split()[3]) * DEMO_SCALE),
            "speed": 300, "textColor": text_color, "pivots": PIVOTS}
    with open(os.path.join(out_dir, "character.json"), "w", encoding="utf-8") as f:
        json.dump(char, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return report
