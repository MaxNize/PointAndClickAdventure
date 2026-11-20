"""Baukasten für neutrale Nebenfiguren (NPCs).
Gleiches Rig/IDs wie die Hauptfiguren. Bewusst neutral: keine Leuchtfarben, gedeckte Töne,
keine Gadgets. Haare in allen Ansichten durchgängig (Styleguide Abschnitt 6)."""
import json
from boy import mir, girl_profile
from profile import preset as _pf

# ------------------------------------------------------------------ Frisuren (Front-hinten, Front-oben, Seite, Rücken)
HAIR = {
 "short": dict(
   fb=["M150,120 C143,134 143,152 147,166 L156,160 L158,128 Z"],
   ft="M150,140 Q148,102 200,98 Q252,102 250,140 L242,128 L236,136 L226,122 L214,132 L200,120 L186,132 L174,122 L164,136 L158,128 Z",
   side="M152,124 C150,100 176,90 208,92 C236,94 254,108 256,130 L246,136 L240,126 L232,134 L224,122 L216,130 C212,146 210,160 206,172 L200,192 L192,186 L184,192 L176,184 L166,188 L160,176 C152,160 150,140 152,124 Z",
   back="M148,118 C140,138 142,166 150,184 L160,180 L168,188 L178,182 L188,190 L200,184 L212,190 L222,182 L232,188 L240,180 L250,184 C258,166 260,138 252,118 C254,96 230,82 200,82 C170,82 146,96 148,118 Z"),
 "long": dict(
   fb=["M148,118 C134,160 134,230 142,268 L156,256 L162,272 L168,200 L166,128 Z"],
   ft="M150,142 Q148,100 200,98 Q252,100 250,142 L240,126 L222,118 Q204,116 186,124 L170,134 L160,148 Z",
   side="M152,124 C150,100 176,90 208,92 C236,94 254,108 256,130 L246,140 L238,124 L222,118 L216,132 C212,150 210,170 210,190 C206,220 200,250 196,272 L186,258 L178,276 L170,256 L160,268 C146,230 146,170 152,124 Z",
   back="M146,116 C134,160 134,230 144,276 L160,262 L170,280 L182,264 L194,282 L206,264 L218,282 L230,264 L240,280 L256,276 C266,230 266,160 254,116 C256,94 230,80 200,80 C170,80 144,94 146,116 Z"),
 "bob": dict(
   fb=["M148,118 C138,150 138,186 144,204 L156,196 L160,206 L166,170 L166,128 Z"],
   ft="M150,146 Q148,100 200,98 Q252,100 250,146 L246,136 Q226,128 200,128 Q174,128 154,136 Z",
   side="M152,124 C150,100 176,90 208,92 C236,94 254,108 256,134 Q240,124 222,124 L216,134 C212,150 210,168 210,186 L206,204 L194,198 L184,206 L174,198 L162,204 C150,176 148,146 152,124 Z",
   back="M146,116 C138,150 140,186 148,206 L162,198 L176,208 L190,200 L200,210 L210,200 L224,208 L238,198 L252,206 C260,186 262,150 254,116 C256,94 230,80 200,80 C170,80 144,94 146,116 Z"),
 "bun": dict(
   fb=["M150,120 C144,134 144,150 148,162 L156,158 L158,128 Z"], extra_fb='<circle class="nhair" cx="200" cy="88" r="20"/>',
   ft="M150,142 Q148,102 200,98 Q252,102 250,142 Q236,120 200,118 Q164,120 150,142 Z",
   side="M152,124 C150,100 176,90 208,92 C236,94 254,108 256,130 Q240,118 220,118 L216,132 C212,148 210,162 206,176 L198,192 C184,194 166,188 158,174 C150,158 150,140 152,124 Z",
   side_extra='<circle class="nhair" cx="164" cy="104" r="19"/>',
   back="M148,118 C140,140 144,170 156,186 Q200,198 244,186 C256,170 260,140 252,118 C254,96 230,82 200,82 C170,82 146,96 148,118 Z",
   back_extra='<circle class="nhair" cx="200" cy="100" r="21"/><path class="hairline" d="M186,96 Q200,88 214,96"/>'),
 "ponytail": dict(
   fb=["M150,120 C144,134 144,150 148,162 L156,158 L158,128 Z"],
   ft="M150,142 Q148,102 200,98 Q252,102 250,142 Q240,124 214,120 L200,126 L186,120 Q160,124 150,142 Z",
   side="M152,124 C150,100 176,90 208,92 C236,94 254,108 256,130 Q240,118 220,118 L216,132 C212,148 210,162 206,176 L198,192 C184,194 166,188 158,174 C150,158 150,140 152,124 Z",
   side_extra='<path class="nhair" d="M166,114 C146,128 140,170 146,238 L154,228 L158,246 L166,226 C164,190 168,150 180,122 Z"/>',
   back="M148,118 C140,140 144,170 156,186 Q200,198 244,186 C256,170 260,140 252,118 C254,96 230,82 200,82 C170,82 146,96 148,118 Z",
   back_extra='<path class="nhair" d="M190,114 C184,160 186,204 192,244 L200,256 L208,244 C214,204 216,160 210,114 Z"/>'),
 "bald": dict(
   fb=["M150,132 C143,146 143,162 147,172 L156,166 L158,138 Z"],
   ft=None,
   side="M156,136 C148,154 150,176 164,190 L200,194 L202,182 C194,178 190,168 191,154 L196,142 Z",
   back="M150,138 C146,160 152,180 166,190 Q200,200 234,190 C248,180 254,160 250,138 Q200,152 150,138 Z"),
}

CAP_FRONT = ('<path class="nhat" d="M146,120 C146,90 170,76 200,76 C230,76 254,90 254,120 Q200,108 146,120 Z"/>'
             '<path class="nhatdk" d="M150,115 Q200,130 250,115 Q252,125 200,131 Q148,125 150,115 Z"/>')
CAP_SIDE = ('<path class="nhat" d="M150,122 C148,92 172,78 206,78 C238,80 256,96 256,120 Z"/>'
            '<path class="nhatdk" d="M238,114 Q268,112 280,121 Q262,127 236,125 Z"/>')
CAP_BACK = '<path class="nhat" d="M146,120 C146,90 170,76 200,76 C230,76 254,90 254,120 Q200,128 146,120 Z"/>'

# ------------------------------------------------------------------ Requisiten
def prop(kind, x, y, view="front"):
    if kind == "book":
        return f'<rect class="nprop" x="{x-12}" y="{y-6}" width="24" height="30" rx="2"/><rect class="npropdk" x="{x-12}" y="{y-6}" width="5" height="30"/>'
    if kind == "scroll":
        return f'<rect class="nprop" x="{x-5}" y="{y-14}" width="10" height="34" rx="4"/><rect class="npropdk" x="{x-7}" y="{y-16}" width="14" height="5" rx="2"/><rect class="npropdk" x="{x-7}" y="{y+17}" width="14" height="5" rx="2"/>'
    if kind == "mug":
        return f'<rect class="nprop" x="{x-8}" y="{y-4}" width="16" height="18" rx="3"/><path class="npropdk" d="M{x+8},{y} Q{x+15},{y+5} {x+8},{y+11}" fill="none" stroke-width="3"/>'
    if kind == "basket":
        return (f'<path class="npropdk" d="M{x-16},{y} Q{x},{y-26} {x+16},{y}" fill="none" stroke-width="3"/>'
                f'<path class="nprop" d="M{x-18},{y} L{x+18},{y} L{x+13},{y+24} L{x-13},{y+24} Z"/>'
                f'<path class="line" d="M{x-15},{y+8} L{x+15},{y+8} M{x-14},{y+16} L{x+14},{y+16}"/>')
    if kind == "broom":
        return (f'<rect class="nprop" x="{x-3}" y="{y-250}" width="6" height="330" rx="2"/>'
                f'<path class="npropdk" d="M{x-4},{y+78} L{x+4},{y+78} L{x+16},{y+130} L{x-16},{y+130} Z"/>')
    return ""

# ------------------------------------------------------------------ Bauteile
def eye(cx, side):
    m = 1 if side == "l" else -1
    X = lambda dx: cx + dx*m
    return (f'<path class="eyewhite" d="M{X(-9)},158 Q{X(0)},153 {X(9)},157 Q{X(8)},162 {X(0)},163 Q{X(-8)},162 {X(-9)},158 Z"/>'
            f'<ellipse class="niris" cx="{X(-0.5)}" cy="158.5" rx="3.6" ry="4.4"/><circle class="pupil" cx="{X(-0.5)}" cy="158.5" r="1.7"/>'
            f'<circle class="hl" cx="{X(1.2)}" cy="157.2" r="1"/>'
            f'<path class="lash" d="M{X(-10)},158 Q{X(0)},151.5 {X(10)},156.5" style="stroke-width:1.8"/>'
            f'<path class="nbrow" d="M{X(-11)},146 Q{X(0)},142.5 {X(10)},144.5"/>')

def build(p):
    """p: dict mit Körper- und Stilparametern -> (FRONT, SIDE, BACK) Markup."""
    sw, ww, lw, belly = p["sw"], p["ww"], p["lw"], p.get("belly", 0)
    outfit, hair, acc = p["outfit"], HAIR[p["hair"]], p.get("prop", "")
    cap, apron, glasses = p.get("cap", False), p.get("apron", False), p.get("glasses", False)
    S = p.get("scale", 1.0)
    PF = _pf(p["id"])
    root = f'transform="translate(200 773) scale({S}) translate(-200 -773)"'
    bl = belly * 14

    # ---------- FRONT
    g = 5
    def fleg(side):
        xl, xr = 200 - g - lw, 200 - g
        d = f"M{xl},350 C{xl-3},450 {xl+1},620 {xl+4},730 L{xr-1},730 C{xr+1},620 {xr+1},450 {xr},350 Z"
        return f'<path class="nlow" d="{d if side=="l" else mir(d)}"/>'
    def fshoe(side):
        c = 200 - g - lw/2
        d = f"M{c-lw/2-1},722 L{c+lw/2+1},722 L{c+lw/2+2},760 Q{c+lw/2+2},773 {c+4},773 L{c-lw/2+2},773 Q{c-lw/2-6},771 {c-lw/2-3},760 Z"
        return f'<path class="nshoe" d="{d if side=="l" else mir(d)}"/>'
    torso = (f"M{200-sw},222 Q200,212 {200+sw},222 C{200+sw+4},270 {200+ww+4+bl},306 {200+ww},342 "
             f"L{200-ww},342 C{200-ww-4-bl},306 {200-sw-4},270 {200-sw},222 Z")
    skirt_len = {"robe": 742, "dress": 668, "tunic": 560, "jacket": 404}.get(outfit)
    flare = {"robe": 44, "dress": 52, "tunic": 22, "jacket": 10}.get(outfit, 0)
    fskirt = (f'<path class="nskirt" d="M{200-ww-2},330 L{200+ww+2},330 C{200+ww+flare*0.5},{(330+skirt_len)/2} {200+ww+flare},{skirt_len-30} {200+ww+flare},{skirt_len} '
              f'Q200,{skirt_len+8} {200-ww-flare},{skirt_len} C{200-ww-flare},{skirt_len-30} {200-ww-flare*0.5},{(330+skirt_len)/2} {200-ww-2},330 Z"/>') if skirt_len else ""
    fapron = (f'<path class="napron" d="M{200-ww+6},250 L{200+ww-6},250 L{200+ww+4},{min(skirt_len or 600, 620)} L{200-ww-4},{min(skirt_len or 600, 620)} Z"/>'
              f'<path class="napron" d="M{200-ww+6},250 L{200-ww+14},222 M{200+ww-6},250 L{200+ww-14},222" fill="none" stroke-width="3"/>') if apron else ""
    def farm(side, with_prop=False):
        x0 = 200 - sw
        d = (f"M{x0+6},224 C{x0-14},228 {x0-20},252 {x0-20},282 L{x0-24},360 L{x0-2},363 L{x0+2},286 C{x0+4},262 {x0+8},244 {x0+12},236 Z")
        s = f'<path class="ntop" d="{d if side=="l" else mir(d)}"/>'
        hx = x0 - 13 if side == "l" else 400 - (x0 - 13)
        s += f'<ellipse class="skin" cx="{hx}" cy="374" rx="9" ry="11"/>'
        if with_prop and acc and acc != "satchel":
            s += prop(acc, hx, 382)
        return s
    satchel_f = (f'<path class="nprop" d="M{200-sw+8},222 L{200+ww+6},330 L{200+ww},336 L{200-sw+2},230 Z"/>'
                 f'<rect class="nprop" x="{200+ww-6}" y="326" width="30" height="26" rx="4"/><path class="npropdk" d="M{200+ww-6},326 L{200+ww+24},326 L{200+ww+24},336 L{200+ww-6},336 Z"/>') if acc == "satchel" else ""
    glasses_f = ('<circle class="nglass" cx="181" cy="158" r="9"/><circle class="nglass" cx="219" cy="158" r="9"/><path class="nglass" d="M190,157 Q200,153 210,157"/>') if glasses else ""
    fhead = (f'<g id="head">'
             + "".join(f'<path class="nhair" d="{d}"/><path class="nhair" d="{mir(d)}"/>' for d in hair["fb"]) + hair.get("extra_fb", "")
             + '<circle class="skin" cx="152" cy="156" r="6.5"/><circle class="skin" cx="248" cy="156" r="6.5"/>'
             + '<path class="skin" d="M153,124 C152,158 164,182 190,195 Q200,199 210,195 C236,182 248,158 247,124 Q200,114 153,124 Z"/>'
             + eye(181, "l") + eye(219, "r") + glasses_f
             + '<path class="nose" d="M200.5,170 l-1.6,2.4"/><path class="mouthline" d="M195,182 Q200,183.5 205,182"/>'
             + (f'<path class="nhair" d="{hair["ft"]}"/>' if hair["ft"] else "")
             + (CAP_FRONT if cap else "") + '</g>')
    FRONT = f'''<g id="character" {root}>
  <ellipse class="groundshadow" cx="200" cy="773" rx="{sw+30}" ry="7"/>
  <g id="front_leg_l">{fleg("l")}</g><g id="front_leg_r">{fleg("r")}</g>
  <g id="boot_l">{fshoe("l")}</g><g id="boot_r">{fshoe("r")}</g>
  <rect class="skin" x="192" y="188" width="16" height="32"/>
  <path class="ntop" d="{torso}"/>
  <path class="ncollar" d="M188,214 L200,230 L212,214 L216,220 L200,238 L184,220 Z"/>
  {fskirt}{fapron}
  <path class="nbelt" d="M{200-ww-2},326 L{200+ww+2},326 L{200+ww+2},336 L{200-ww-2},336 Z"/>
  {satchel_f}
  <g id="arm_l">{farm("l")}</g><g id="arm_r">{farm("r", True)}</g>
  {fhead}
</g>'''

    # ---------- SEITE
    a, b = lw*0.62, lw*0.45
    def sleg(gid, far=False):
        thigh = f"M{205-a},352 C{205-a-3},430 {205-a+4},500 {205-b-2},550 L{205+b+3},553 C{205+a+2},500 {205+a+4},430 {205+a},352 Z"
        shin = f"M{205-b},546 C{205-b-4},600 {205-b},680 {205-b+1},726 L{205+b},726 C{205+b+1},680 {205+b+3},620 {205+b+3},553 Z"
        shoe = f"M{205-b-1},718 L{205+b},718 L{205+b+1},744 L{234},752 Q{241},760 {234},768 L{205-b+4},768 L{205-b-1},760 Z"
        s = f'<g id="{gid}"><path class="nlow" d="{thigh}"/>'
        if far: s += f'<path class="shade" d="{thigh}"/>'
        s += f'<g id="{gid}_shin"><circle class="nlow" cx="206" cy="550" r="{b+2}"/><path class="nlow" d="{shin}"/><path class="nshoe" d="{shoe}"/>'
        if far: s += f'<circle class="shade" cx="206" cy="550" r="{b+2}"/><path class="shade" d="{shin}"/><path class="shade" d="{shoe}"/>'
        return s + '</g></g>'
    def sarm(gid, far=False, with_prop=False):
        up = "M190,226 C179,240 181,272 194,290 L216,290 C226,272 226,240 214,226 Z"
        lo = "M194,284 L215,284 L213,362 L197,362 Z"
        s = f'<g id="{gid}"><g id="{gid}_fore"><path class="ntop" d="{lo}"/><ellipse class="skin" cx="205" cy="374" rx="8.5" ry="11"/>'
        if with_prop and acc and acc != "satchel": s += prop(acc, 207, 382, "side")
        if far: s += f'<path class="shade" d="{lo}"/>'
        s += f'</g><path class="ntop" d="{up}"/>'
        if far: s += f'<path class="shade" d="{up}"/>'
        return s + '</g>'
    d1, d2 = sw*0.62, sw*0.6 + bl
    storso = (f"M{205-d1},224 C{205-d1-8},262 {205-d1-6},302 {205-d1+2},344 L{205+d2},344 "
              f"C{205+d2+6},302 {205+d2+2},252 {205+d2-8},228 Q209,216 201,216 Z")
    sskirt = (f'<path class="nskirt" d="M{205-d1},330 L{205+d2},330 C{205+d2+flare*0.4},{(330+skirt_len)/2} {205+d2+flare*0.7},{skirt_len-30} {205+d2+flare*0.7},{skirt_len} '
              f'L{205-d1-flare*0.7},{skirt_len} C{205-d1-flare*0.7},{skirt_len-30} {205-d1-flare*0.4},{(330+skirt_len)/2} {205-d1},330 Z"/>') if skirt_len else ""
    sapron = f'<path class="napron" d="M{205+d2-8},250 C{205+d2+4},300 {205+d2+6},340 {205+d2+8},{min(skirt_len or 600, 620)} L{205+d2-6},{min(skirt_len or 600, 620)} L{205+d2-16},252 Z"/>' if apron else ""
    satchel_s = (f'<path class="nprop" d="M{205-6},220 L{205+d2},228 L{205+d2-2},236 L{205-8},228 Z"/>'
                 f'<rect class="nprop" x="{205-d1-22}" y="322" width="26" height="28" rx="4"/>') if acc == "satchel" else ""
    glasses_s = '<circle class="nglass" cx="236" cy="156" r="8"/><path class="nglass" d="M228,155 L198,152"/>' if glasses else ""
    SIDE = f'''<g id="characterSide" style="display:none" {root}>
  <ellipse class="groundshadow" cx="210" cy="773" rx="{sw+12}" ry="6"/>
  {sarm("side_arm_far", far=True)}
  {sleg("side_leg_far", far=True)}
  {sleg("side_leg_near")}
  <rect class="skin" x="196" y="184" width="18" height="40"/>
  <path class="ntop" d="{storso}"/>
  {sskirt}{sapron}
  <path class="nbelt" d="M{205-d1+1},326 L{205+d2},326 L{205+d2},336 L{205-d1+1},336 Z"/>
  {satchel_s}
  {sarm("side_arm_near", with_prop=True)}
  <g id="side_head">
    <path class="skin" d="{PF["d"]}"/>
    <path class="nhair" d="{hair["side"]}"/>{hair.get("side_extra", "")}
    <path class="skin" d="M199.5,181 C195,183.5 189,180.5 186,176 C183,171 182.2,165 182.6,161 C183.2,157 185.5,154.4 188,154.2 C190.6,154 192.6,155.6 193.6,157.8 C195.5,162 197.5,168 199,173 Z"/>
    <path class="line" d="M187.5,159.5 Q185.2,166.5 189.5,173.5"/>
    <ellipse class="niris" cx="232" cy="154" rx="2.6" ry="4.6"/><circle class="hl" cx="232.6" cy="152" r="1"/>
    <path class="lash" d="M237,149.5 Q230,147 225,151" style="stroke-width:1.8"/>
    <path class="nbrow" d="M226,141 Q234,137.5 243,139"/>
    {glasses_s}
    <path class="mouthline" d="{PF["mouth"]}"/>
    {CAP_SIDE if cap else ""}
  </g>
</g>'''

    # ---------- RÜCKEN
    def barm(side, with_prop=False):
        m = 1 if side == "l" else -1
        x0 = 200 - sw
        d = (f"M{x0+6},224 C{x0-14},228 {x0-20},252 {x0-20},282 L{x0-24},360 L{x0-2},363 L{x0+2},286 C{x0+4},262 {x0+8},244 {x0+12},236 Z")
        hx = x0 - 13
        s = f'<path class="ntop" d="{d}"/><ellipse class="skin" cx="{hx}" cy="374" rx="9" ry="11"/>'
        if with_prop and acc and acc != "satchel": s += prop(acc, hx, 382)
        s = s if side == "l" else f'<g transform="translate(400 0) scale(-1 1)">{s}</g>'
        return f'<g id="back_arm_{side}"><g transform="rotate({6*m} {168 if side=="l" else 232} 230)">{s}</g></g>'
    satchel_b = f'<rect class="nprop" x="{200-ww-26}" y="326" width="30" height="26" rx="4"/><path class="nprop" d="M{200+sw-8},222 L{200-ww-6},330 L{200-ww},336 L{200+sw-2},230 Z"/>' if acc == "satchel" else ""
    BACK = f'''<g id="characterBack" style="display:none" {root}>
  <ellipse class="groundshadow" cx="200" cy="773" rx="{sw+30}" ry="7"/>
  <g id="back_leg_l">{fleg("l")}{fshoe("l")}</g><g id="back_leg_r">{fleg("r")}{fshoe("r")}</g>
  <path class="ntop" d="{torso}"/>
  {fskirt}
  <path class="nbelt" d="M{200-ww-2},326 L{200+ww+2},326 L{200+ww+2},336 L{200-ww-2},336 Z"/>
  {f'<path class="napron" d="M190,330 L176,346 L184,350 L200,334 L216,350 L224,346 L210,330 Z"/>' if apron else ""}
  {satchel_b}
  {barm("l")}{barm("r", True)}
  <g id="back_head">
    <rect class="skin" x="192" y="182" width="16" height="40"/>
    <circle class="skin" cx="152" cy="156" r="6.5"/><circle class="skin" cx="248" cy="156" r="6.5"/>
    <path class="skin" d="M156,130 C156,104 178,92 200,92 C222,92 244,104 244,130 L244,176 C232,194 168,194 156,176 Z"/>
    <path class="nhair" d="{hair["back"]}"/>{hair.get("back_extra", "")}
    {CAP_BACK if cap else ""}
  </g>
</g>'''
    return FRONT, SIDE, BACK

# ------------------------------------------------------------------ Palette-CSS
BASE_STROKE = "stroke:#3b2219;stroke-width:2.2;stroke-linejoin:round"
def color_css(c):
    k = lambda cls, col: f".{cls}{{fill:{col};{BASE_STROKE}}}"
    return "".join([k("ntop", c["top"]), k("nskirt", c.get("skirt", c["top"])), k("nlow", c["low"]), k("nshoe", c.get("shoe", "#4a3226")),
                    k("nhair", c["hair"]), k("nbelt", c.get("belt", "#5a3e2a")), k("napron", c.get("apron", "#e8e0cc")),
                    k("ncollar", c.get("collar", "#e8e0cc")), k("nprop", c.get("prop", "#8a6a48")), k("npropdk", c.get("propdk", "#5a3e2a")),
                    k("nhat", c.get("hat", "#5a5048")), k("nhatdk", c.get("hatdk", "#3e3630")),
                    f".niris{{fill:{c.get('eye', '#6a5040')}}}.nbrow{{fill:none;stroke:{c.get('brow', '#5a3e2a')};stroke-width:2;stroke-linecap:round}}",
                    ".nglass{fill:none;stroke:#8a7a60;stroke-width:1.6}"])
NPC_DARK = (".ntop,.nskirt,.nlow,.nshoe,.nhair,.nbelt,.napron,.ncollar,.nprop,.npropdk,.nhat,.nhatdk{fill:#140e10;stroke:#140e10;stroke-width:1.2}"
            ".niris,.nbrow,.nglass{display:none}.hl{fill:#cdbfae;opacity:.55}")

# ------------------------------------------------------------------ die 10 NPCs
NPCS = [
 dict(id="lena", name="Lena", role="Mitschülerin", sw=31, ww=25, lw=27, outfit="robe", hair="bun", prop="book",
      colors=dict(top="#5b6475", hair="#7a4e34", low="#3e3a40", eye="#5a6a50"), walk=dict(lean=2, bob=6, sway=1.6, speed=320),
      lines=["Hast du die Hausaufgabe zur Transmutation schon?", "Ich hab die halbe Nacht in der Bibliothek verbracht.", "Pass auf, Magister Uhu sieht alles."]),
 dict(id="tobi", name="Tobi", role="Mitschüler", sw=33, ww=27, lw=29, outfit="trousers", hair="short", prop="satchel",
      colors=dict(top="#7a6a52", collar="#ddd3bc", hair="#4a3424", low="#4a4440", prop="#7a5232"), walk=dict(lean=1, bob=7, sway=1.8, speed=350, arm=18),
      lines=["Mein Trank ist schon wieder explodiert.", "Weißt du, wann es Mittagessen gibt?", "Im zweiten Lehrjahr dürfen wir endlich Schlüssel machen!"]),
 dict(id="grombart", name="Herr Grombart", role="Hausmeister", sw=36, ww=33, lw=30, belly=0.6, outfit="tunic", hair="bald", prop="broom", apron=True,
      colors=dict(top="#6a6050", hair="#8a8478", low="#4a443c", apron="#9a8e74", prop="#7a5a3a"), walk=dict(lean=3, bob=4, sway=2.4, speed=260, arm=10),
      lines=["Nicht auf den frisch gewischten Boden!", "Wer hat schon wieder Schwefel verschüttet?", "Hmpf. Lehrlinge."]),
 dict(id="seidel", name="Frau Seidel", role="Bibliothekarin", sw=30, ww=26, lw=26, outfit="dress", hair="bun", prop="scroll", glasses=True,
      colors=dict(top="#4e5a52", skirt="#4e5a52", hair="#9a948a", low="#3e3a3a", prop="#d8cdb0", eye="#5a5a5a"), walk=dict(lean=1, bob=4, sway=1.2, speed=270),
      lines=["Psst! Hier wird gelesen.", "Band zwei ist für Erstjährige gesperrt.", "Bitte bring die Bücher pünktlich zurück."]),
 dict(id="maren", name="Maren", role="Küchenhilfe", sw=31, ww=27, lw=27, outfit="dress", hair="ponytail", prop="basket", apron=True,
      colors=dict(top="#8a6050", skirt="#6e5a4a", hair="#a0703e", low="#4a3e36", apron="#e2dac6", prop="#a07a4a"), walk=dict(lean=2, bob=7, sway=2, speed=330),
      lines=["Heute gibt's Rübensuppe. Schon wieder.", "Kannst du mir die Kräuter aus dem Garten holen?", "Die Köchin ist heute schlecht gelaunt."]),
 dict(id="fynn", name="Fynn", role="Botenjunge", sw=29, ww=23, lw=25, scale=0.9, outfit="jacket", hair="short", cap=True, prop="satchel",
      colors=dict(top="#5a6a5a", skirt="#5a6a5a", hair="#6a4a30", low="#4a4238", hat="#6a5a48", hatdk="#4a3e32", prop="#8a6a48"), walk=dict(lean=3, bob=8, sway=1.8, speed=380, arm=20),
      lines=["Eilbrief für den Erzalchemisten!", "Ich hab keine Zeit, ich muss weiter!", "Die Treppen hier bringen mich noch um."]),
 dict(id="brandt", name="Herr Brandt", role="Gelehrter", sw=32, ww=29, lw=27, outfit="robe", hair="short", prop="book", glasses=True,
      colors=dict(top="#4a4e3e", hair="#b0aaa0", low="#3a3630", prop="#6a3a2e"), walk=dict(lean=4, bob=3, sway=1.2, speed=240, arm=8),
      lines=["Faszinierend, diese Kristallstrukturen.", "Zu meiner Zeit hatten wir noch keine Athanore.", "Hm? Ach, entschuldige, ich war in Gedanken."]),
 dict(id="ilse", name="Ilse", role="Händlerin", sw=32, ww=29, lw=28, belly=0.3, outfit="tunic", hair="long", prop="basket",
      colors=dict(top="#7a5a48", skirt="#6a4e40", hair="#5a3a2a", low="#4a3e34", prop="#9a7a4a"), walk=dict(lean=1, bob=5, sway=2.2, speed=300),
      lines=["Frische Kräuter! Getrocknete Pilze!", "Für Lehrlinge mach ich einen guten Preis.", "Mondtau ist heute leider ausverkauft."]),
 dict(id="kurt", name="Kurt", role="Pförtner", sw=38, ww=33, lw=31, scale=1.05, belly=0.4, outfit="jacket", hair="short", cap=True, prop="mug",
      colors=dict(top="#4e4a52", skirt="#4e4a52", hair="#3a3230", low="#3a3638", hat="#3e3a40", hatdk="#2a2628", prop="#8a7a6a"), walk=dict(lean=0, bob=4, sway=2.6, speed=270, arm=12),
      lines=["Ausweis? Ach, du bist's.", "Das Tor schließt bei Sonnenuntergang.", "Nichts los heute. Wie immer."]),
 dict(id="yara", name="Yara", role="Studentin", sw=30, ww=24, lw=26, outfit="tunic", hair="bob", prop="scroll",
      colors=dict(top="#6a5a6e", skirt="#5a4e5e", hair="#2e2624", low="#3e3640", prop="#d8cdb0", eye="#4a4a3a"), walk=dict(lean=1, bob=6, sway=1.6, speed=330),
      lines=["Ich übe gerade Transmutationsformeln.", "Erde und Wasser? Das ist doch Nährschlamm.", "Viel Glück bei deiner Prüfung!"]),
]

if __name__ == "__main__":
    from gen import ANIME_CSS, ANIME_DEFS
    import anime_dark
    data = []
    for n in NPCS:
        F, Si, B = build(n)
        n["_markup"] = (F, Si, B)
        for style, css in (("farbe", ANIME_CSS + color_css(n["colors"])), ("scherenschnitt", anime_dark.css + NPC_DARK)):
            for view, body in (("front", F), ("seite", Si), ("rueck", B)):
                body = body.replace('style="display:none"', '')
                bg = '#e9dcc8' if style == "farbe" else '#a8604e'
                open(f"npc_{n['id']}_{view}_{style}.svg", "w").write(
                    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -20 400 820" width="400" height="820"><title>NPC {n["name"]} – {view}</title>'
                    f'<defs>{ANIME_DEFS}</defs><style>{css}</style><rect y="-20" width="400" height="820" fill="{bg}"/>{body}</svg>')
        data.append({k: n[k] for k in ("id", "name", "role", "lines", "walk")})
    json.dump(data, open("npc_dialoge.json", "w"), ensure_ascii=False, indent=2)
    print("npcs ok", len(NPCS))
