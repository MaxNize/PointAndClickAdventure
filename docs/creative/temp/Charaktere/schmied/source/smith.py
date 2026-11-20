"""Schmied (fünfte Figur): pummelig, aber kräftig.
Gleiches Rig/IDs wie die anderen Figuren; eigener, schwerer Watschelgang."""
from boy import mir, girl_profile

S_CSS = '''
.sshirt{fill:#d8cdb4}.sshirtdk{fill:#b8ab90}.sapron{fill:#7a4a2c}.sapdk{fill:#5a341e}.sglove{fill:#8a5a34}
.spants{fill:#4a4038}.siron{fill:#5b5d66}.sirondk{fill:#3a3c44}.swood{fill:#7a5232}.sband{fill:#8a2f25}
.sbeard{fill:#6b3e24}.sbeardline{fill:none;stroke:#4a2814;stroke-width:1.3}
.sstitch{fill:none;stroke:#c9a46a;stroke-width:1.4;stroke-dasharray:4 3}
.shot{fill:#ff6a3c}.glowr{fill:url(#glowRed)}.spark{fill:#ffd27a}.ssmoke{fill:#ffffff;opacity:.28}
.slens{fill:#7fb5a8;stroke:#3b2219;stroke-width:1.5}.sblush{fill:#e8826e;opacity:.45}
.sshirt,.sshirtdk,.sapron,.sapdk,.sglove,.spants,.siron,.sirondk,.swood,.sband,.sbeard{stroke:#2a1a12;stroke-width:2.2;stroke-linejoin:round}
'''
S_DARK = '''
.sshirt,.sshirtdk,.sglove,.spants,.siron,.sirondk,.swood,.sband,.sapdk,.sbeard{fill:#140e10;stroke:#140e10;stroke-width:1.2}
.sapron{fill:#261a1d;stroke:#140e10;stroke-width:1.2}
.sstitch,.sbeardline,.sblush{display:none}
.shot{fill:#ff6a3c}.glowr{fill:url(#glowRed)}.spark{fill:#ffd27a}.slens{fill:#ff7a5a;stroke:none}.ssmoke{fill:#e8b8a8;opacity:.16}
'''
S_DEFS = '''<radialGradient id="glowRed"><stop offset="0" stop-color="#ff8a5a" stop-opacity=".9"/><stop offset="1" stop-color="#ff4a2a" stop-opacity="0"/></radialGradient>'''

# Schwer und behäbig: kurze Schritte, deutliches Wiegen/Watscheln, kräftiger Armschwung
WALK_STYLE = {'hip': 14, 'knee': 28, 'arm': 12, 'fore': 6, 'lean': 0, 'swag': 2.8, 'lift': 10, 'bob': 6, 'sway': 4.6, 'armOut': 8, 'speed': 235}
SCALE = 1.28   # größer als die anderen Figuren
ROOT = f'transform="translate(200 773) scale({SCALE}) translate(-200 -773)"'

def tongs(hx, hy, dx=22, dy=82):
    """Zange ab Hand (hx,hy) schräg nach unten, mit glühendem Barren."""
    ex, ey = hx + dx, hy + dy
    s = f'<circle class="glowr" cx="{ex+4}" cy="{ey+6}" r="34"/>'
    s += f'<path class="ssmoke" d="M{ex},{ey-8} Q{ex-10},{ey-30} {ex+2},{ey-48} Q{ex+10},{ey-62} {ex+2},{ey-78} Q{ex+18},{ey-60} {ex+10},{ey-44} Q{ex+2},{ey-28} {ex+10},{ey-10} Z"/>'
    s += f'<path class="sirondk" d="M{hx-3},{hy} L{ex-3},{ey} L{ex+1},{ey+1} L{hx+3},{hy} Z"/>'
    s += f'<path class="siron" d="M{hx+4},{hy} L{ex+5},{ey-2} L{ex+9},{ey-1} L{hx+9},{hy} Z"/>'
    s += f'<rect class="shot" x="{ex-8}" y="{ey}" width="26" height="12" rx="3" transform="rotate(14 {ex+5} {ey+6})"/>'
    for (a, b, r) in ((22, -6, 1.8), (28, 8, 1.4), (-10, 10, 1.5), (16, 20, 1.2)):
        s += f'<circle class="spark" cx="{ex+a}" cy="{ey+b}" r="{r}"/>'
    return s

def hammer_back(x1, y1, x2, y2, head_at_end=True):
    """Vorschlaghammer schräg (Stiel von (x1,y1) nach (x2,y2), Kopf am Ende)."""
    import math
    ang = math.degrees(math.atan2(y2-y1, x2-x1))
    s = f'<path class="swood" d="M{x1},{y1} L{x2},{y2}" stroke-width="0"/>'
    L = math.hypot(x2-x1, y2-y1)
    s = (f'<g transform="translate({x1} {y1}) rotate({ang:.1f})">'
         f'<rect class="swood" x="0" y="-5" width="{L:.0f}" height="10" rx="4"/>'
         f'<rect class="sirondk" x="{L*0.15:.0f}" y="-6.5" width="14" height="13" rx="2"/>'
         f'<rect class="siron" x="{L-6:.0f}" y="-26" width="34" height="52" rx="5"/>'
         f'<rect class="sirondk" x="{L+2:.0f}" y="-26" width="6" height="52"/><rect class="sirondk" x="{L+18:.0f}" y="-26" width="6" height="52"/>'
         f'</g>')
    return s

def eye(cx, side):
    m = 1 if side == "l" else -1
    X = lambda dx: cx + dx*m
    return (f'<g id="s_eye_{side}"><path class="eyewhite" d="M{X(-9)},160 Q{X(0)},155 {X(9)},159 Q{X(8)},164 {X(0)},165 Q{X(-8)},164 {X(-9)},160 Z"/>'
            f'<ellipse class="iris" cx="{X(-0.5)}" cy="160.5" rx="4" ry="4.6"/><ellipse class="pupil" cx="{X(-0.5)}" cy="160.5" rx="1.8" ry="2.4"/>'
            f'<circle class="hl" cx="{X(1.4)}" cy="159" r="1.1"/>'
            f'<path class="lash" d="M{X(-10)},160 Q{X(0)},153.5 {X(10)},158.5"/>'
            f'<path class="lowlash" d="M{X(-7)},165.5 Q{X(0)},168 {X(7)},165"/>'
            f'<path class="sbeard" d="M{X(-14)},149 Q{X(-1)},142 {X(13)},146 L{X(14)},151.5 Q{X(0)},148 {X(-13)},154 Z"/></g>')

# ------------------------------------------------------------------ FRONT (stilisiert: Fass-Bauch, Keulen-Unterarme, Stummelbeine)
def front_leg(side):
    d = 'M136,470 C126,560 130,650 138,722 L192,722 C194,650 195,560 192,470 Z'
    return f'<path class="spants" d="{d if side=="l" else mir(d)}"/>'

def front_boot(side):
    d = 'M124,704 L198,704 L199,752 Q201,774 174,774 L140,774 Q116,774 120,752 Z'
    t = 'M120,744 Q160,730 199,744 L199,760 L120,760 Z'
    b = 'M118,764 L201,764 L200,774 L120,774 Z'
    f = (lambda p: p) if side == "l" else mir
    return f'<path class="boot" d="{f(d)}"/><path class="sirondk" d="{f(t)}"/><path class="bootdark" d="{f(b)}"/>'

BEARD_F = 'M140,128 C130,170 132,220 150,262 L158,250 L162,278 L174,262 L180,292 L190,270 L200,300 L210,270 L220,292 L226,262 L238,278 L242,250 L250,262 C268,220 270,170 260,128 L248,134 C248,160 244,180 230,192 Q216,186 200,188 Q184,186 170,192 C156,180 152,160 152,134 Z'

FRONT_HEAD = f"""
  <g id="head" transform="translate(0 34) translate(200 196) scale(0.84) translate(-200 -196)">
    <path class="sbeard" d="{BEARD_F}"/>
    <path class="sbeardline" d="M170,206 Q176,240 186,270 M200,196 L200,290 M230,206 Q224,240 214,270 M158,180 Q160,216 166,246 M242,180 Q240,216 234,246"/>
    <circle class="skin" cx="142" cy="160" r="8"/><circle class="skin" cx="258" cy="160" r="8"/>
    <path class="skin" d="M152,124 C150,154 158,176 172,190 Q186,184 200,186 Q214,184 228,190 C242,176 250,154 248,124 Q200,112 152,124 Z"/>
    <ellipse class="sblush" cx="170" cy="174" rx="10" ry="6"/><ellipse class="sblush" cx="230" cy="174" rx="10" ry="6"/>
    {eye(178, "l")}{eye(222, "r")}
    <circle class="skin" cx="200" cy="174" r="9"/><ellipse class="sblush" cx="200" cy="175" rx="7" ry="6"/>
    <path class="sbeard" d="M200,184 Q178,180 164,198 Q182,194 200,192 Q218,194 236,198 Q222,180 200,184 Z"/>
    <g id="s_band">
      <path class="sband" d="M252,108 L290,90 L282,108 L298,120 L256,120 Z"/>
      <path class="sband" d="M142,128 C140,88 166,66 200,64 C234,66 260,88 258,128 Q200,114 142,128 Z"/>
      <path class="cel" d="M142,128 C142,118 144,110 148,104 Q200,118 252,104 C256,110 258,118 258,128 Q200,114 142,128 Z"/>
      <path class="sapdk" d="M144,104 Q200,96 256,104 L257,115 Q200,107 143,115 Z"/>
      <circle class="brass" cx="180" cy="94" r="14"/><circle class="slens" cx="180" cy="94" r="10"/>
      <circle class="brass" cx="220" cy="94" r="14"/><circle class="slens" cx="220" cy="94" r="10"/>
      <rect class="brass" x="192" y="91" width="16" height="5" rx="2"/>
      <path class="lensshine" d="M174,90 L180,86 L183,89 L177,93 Z M214,90 L220,86 L223,89 L217,93 Z"/>
    </g>
  </g>"""

BELLY = 'M112,222 Q200,186 288,222 C334,262 342,340 328,416 C316,488 266,536 200,540 C134,536 84,488 72,416 C58,340 66,262 112,222 Z'
APRON_F = 'M146,244 L254,244 C302,296 320,366 312,436 C306,506 290,562 280,606 Q200,624 120,606 C110,562 94,506 88,436 C80,366 98,296 146,244 Z'

def popeye_arm(side, tong=False, spread=12):
    m = 1 if side == "l" else -1
    X = lambda x: x if m == 1 else 400 - x
    s = f'<g transform="translate({-22*m} 0) rotate({spread*m} {X(128)} 222)">'
    s += f'<path class="sshirt" d="M{X(146)},210 C{X(96)},212 {X(74)},256 {X(80)},306 L{X(140)},314 L{X(154)},248 Z"/>'
    s += f'<path class="sshirtdk" d="M{X(72)},298 L{X(144)},308 L{X(142)},328 L{X(70)},318 Z"/>'
    s += f'<path class="skin" d="M{X(72)},316 L{X(142)},326 C{X(156)},380 {X(150)},450 {X(134)},500 L{X(90)},500 C{X(68)},450 {X(62)},380 {X(72)},316 Z"/>'
    if tong:
        s += tongs(X(112), 524, 30*m, 86)
        s += f'<circle class="skin" cx="{X(112)}" cy="516" r="30"/><path class="line" d="M{X(96)},508 L{X(128)},508 M{X(96)},520 L{X(128)},520"/>'
    else:
        s += f'<circle class="sglove" cx="{X(112)}" cy="518" r="33"/><path class="sapdk" d="M{X(82)},492 L{X(142)},492 L{X(142)},506 L{X(82)},506 Z"/>'
    return s + '</g>'

FRONT = f"""
<g id="character" {ROOT}>
  <ellipse class="groundshadow" cx="200" cy="773" rx="120" ry="9"/>
  <g id="s_hammer_front">{hammer_back(104, 400, 284, 112)}</g>
  <g id="front_leg_l">{front_leg("l")}</g><g id="front_leg_r">{front_leg("r")}</g>
  <g id="boot_l">{front_boot("l")}</g><g id="boot_r">{front_boot("r")}</g>
  <g id="s_body">
    <path class="sshirt" d="{BELLY}"/>
    <path class="sapron" d="{APRON_F}"/>
    <path class="sstitch" d="M158,250 L242,250 M108,436 Q200,452 292,436 M134,594 Q200,608 266,594"/>
    <path class="sapron" d="M150,240 L170,206 L184,210 L164,246 Z"/><path class="sapron" d="{mir('M150,240 L170,206 L184,210 L164,246 Z')}"/>
    <path class="sapdk" d="M168,330 L232,330 L229,384 L171,384 Z"/>
    <path class="siron" d="M180,330 L182,304 L188,304 L188,330 Z M194,330 L196,298 L202,298 L202,330 Z"/><path class="swood" d="M214,330 L216,294 L224,294 L222,330 Z"/>
    <path class="sapron" d="M84,424 Q200,458 316,424 L314,442 Q200,476 86,442 Z"/>
    <rect class="brass" x="190" y="442" width="20" height="20" rx="3"/>
    <path class="siron" d="M120,440 L124,480 L132,480 L130,440 Z M124,480 Q116,492 128,496 Q138,492 130,480 Z"/>
  </g>
  <g id="arm_l">{popeye_arm("l")}</g>
  <g id="arm_r">{popeye_arm("r", tong=True)}</g>
  {FRONT_HEAD}
</g>
"""

# ------------------------------------------------------------------ SEITE
def side_leg(gid, far=False):
    thigh = 'M160,352 C152,430 168,500 182,552 L232,554 C242,500 252,430 250,352 Z'
    shin = 'M182,546 C170,600 178,680 182,716 L232,716 C236,690 240,620 232,553 Z'
    boot = 'M174,700 L236,700 L236,726 L270,738 Q284,752 274,770 L182,770 L174,760 Z'
    s = f'<g id="{gid}"><path class="spants" d="{thigh}"/>'
    if far: s += f'<path class="shade" d="{thigh}"/>'
    s += f'<g id="{gid}_shin"><circle class="spants" cx="206" cy="550" r="25"/><path class="spants" d="{shin}"/>'
    s += f'<path class="boot" d="{boot}"/><path class="sirondk" d="M236,726 L270,738 Q284,752 274,770 L246,770 Q248,744 236,734 Z"/>'
    s += '<path class="bootdark" d="M177,762 L276,762 L274,770 L182,770 Z"/>'
    if far: s += f'<circle class="shade" cx="206" cy="550" r="25"/><path class="shade" d="{shin}"/><path class="shade" d="{boot}"/>'
    return s + '</g></g>'

def side_arm(gid, far=False, with_tongs=False):
    upper = 'M168,214 C140,240 144,292 176,312 L236,312 C264,292 264,240 236,214 Z'
    s = f'<g id="{gid}"><g id="{gid}_fore">'
    s += '<path class="sshirtdk" d="M168,298 L240,298 L239,320 L169,320 Z"/>'
    s += '<path class="skin" d="M168,316 L240,316 C254,372 248,444 232,494 L180,494 C162,444 156,372 168,316 Z"/>'
    if with_tongs:
        s += tongs(214, 522, 36, 84)
        s += '<circle class="skin" cx="206" cy="514" r="30"/><path class="line" d="M190,506 L222,506 M190,518 L222,518"/>'
    else:
        s += '<circle class="sglove" cx="206" cy="516" r="33"/><path class="sapdk" d="M176,490 L236,490 L236,504 L176,504 Z"/>'
    if far: s += '<path class="shade" d="M168,298 L240,298 L232,494 L180,494 Z"/><circle class="shade" cx="206" cy="516" r="33"/>'
    s += f'</g><path class="sshirt" d="{upper}"/>'
    if far: s += f'<path class="shade" d="{upper}"/>'
    return s + '</g>'

SIDE_HEAD_HAIR = 'M154,120 L222,120 C216,136 214,152 216,168 C220,180 232,188 246,184 L256,176 C264,182 270,196 268,214 C266,246 256,276 240,300 L230,284 L224,302 L212,282 L204,292 L196,270 C186,250 172,236 160,222 C148,200 146,150 154,120 Z'

SIDE = f"""
<g id="characterSide" style="display:none" {ROOT}>
  <ellipse class="groundshadow" cx="214" cy="773" rx="84" ry="8"/>
  <g id="s_hammer_side">{hammer_back(170, 440, 142, 100)}</g>
  {side_arm("side_arm_far", far=True)}
  {side_leg("side_leg_far", far=True)}
  {side_leg("side_leg_near")}
  <g id="side_torso">
    <path class="sshirt" d="M160,206 C124,240 120,334 136,424 C148,490 186,532 234,536 C298,530 342,466 342,384 C342,298 308,232 256,214 Q230,202 204,200 Z"/>
    <path class="sapron" d="M236,230 C306,258 348,330 342,414 C338,488 310,548 300,606 L232,610 Z"/>
    <path class="sstitch" d="M242,246 C300,274 330,340 324,414 C320,480 298,540 288,598"/>
    <path class="sapdk" d="M262,326 L318,338 L312,392 L262,386 Z"/>
    <path class="sapron" d="M226,234 L208,206 L196,212 L216,242 Z"/>
    <path class="sapron" d="M140,414 L332,426 L330,444 L140,432 Z"/>
    <path class="siron" d="M150,432 L154,470 L162,470 L160,432 Z"/>
  </g>
  {side_arm("side_arm_near", with_tongs=True)}
  <g id="side_head" transform="translate(6 34) translate(206 196) scale(0.84) translate(-206 -196)">
    <path class="skin" d="{girl_profile()}"/>
    <path class="sbeard" d="{SIDE_HEAD_HAIR} M226,190 Q236,196 250,194 L252,186 Q238,190 226,184 Z" fill-rule="evenodd"/>
    <path class="sbeardline" d="M170,140 C164,166 166,194 176,214 M204,204 Q226,226 238,262 M226,196 Q244,214 254,240"/>
    <path class="skin" d="M199.5,170 C195,172.5 189,169.5 186,165 C183,160 182.2,154 182.6,150 C183.2,146 185.5,143.4 188,143.2 C190.6,143 192.6,144.6 193.6,146.8 C195.5,151 197.5,157 199,162 Z"/>
    <path class="line" d="M187.5,148.5 Q185.2,155.5 189.5,162.5"/>
    <ellipse class="sblush" cx="238" cy="168" rx="9" ry="5"/>
    <circle class="skin" cx="258" cy="166" r="8.5"/><ellipse class="sblush" cx="258" cy="167" rx="6.5" ry="5.5"/>
    <g id="s_side_eye">
      <ellipse class="iris" cx="233" cy="155" rx="2.6" ry="4.4"/><circle class="hl" cx="233.6" cy="153.4" r="1.1"/>
      <path class="lash" d="M238,151 Q231,148.4 226,152.4"/>
      <path class="sbeard" d="M223,145 Q233,138 246,140 L246,146 Q234,145 223,150 Z"/>
    </g>
    <path class="sbeard" d="M246,177 Q262,178 268,188 Q256,186 244,188 Z"/>
    <g id="s_side_band">
      <path class="sband" d="M150,108 L116,92 L126,112 L108,128 L150,122 Z"/>
      <path class="sband" d="M148,126 C146,90 172,70 206,70 C238,72 260,92 260,126 Z"/>
      <path class="sapdk" d="M148,106 Q204,98 260,106 L260,117 Q204,109 148,117 Z"/>
      <circle class="brass" cx="240" cy="96" r="14"/><ellipse class="slens" cx="242" cy="96" rx="6.5" ry="10"/>
    </g>
  </g>
</g>
"""

# ------------------------------------------------------------------ RÜCKEN
def back_leg(side):
    return f'<g id="back_leg_{side}">{front_leg(side)}{front_boot(side)}</g>'

def back_arm(side, with_tongs=False):
    m = 1 if side == "l" else -1
    X = lambda x: x if m == 1 else 400 - x
    s = f'<g id="back_arm_{side}"><g>'
    s += popeye_arm(side, tong=with_tongs)
    return s + '</g></g>'

BACK = f"""
<g id="characterBack" style="display:none" {ROOT}>
  <ellipse class="groundshadow" cx="200" cy="773" rx="120" ry="9"/>
  <g id="back_legs">{back_leg("l")}{back_leg("r")}</g>
  <path class="sshirt" d="{BELLY}"/>
  <path class="line" d="M200,232 L200,500 M150,260 Q130,360 150,470 M250,260 Q270,360 250,470"/>
  <path class="sapron" d="M160,210 L176,208 L252,420 L236,424 Z"/><path class="sapron" d="M240,210 L224,208 L148,420 L164,424 Z"/>
  <path class="sapron" d="M84,424 Q200,458 316,424 L314,442 Q200,476 86,442 Z"/>
  <path class="sapron" d="M200,446 L164,420 L156,446 L170,452 L160,486 L184,458 Z"/>
  <path class="sapron" d="M200,446 L236,420 L244,446 L230,452 L240,486 L216,458 Z"/>
  <circle class="sapron" cx="200" cy="448" r="9"/>
  <path class="sapron" d="M100,440 L100,600 Q110,610 122,600 L124,452 Z"/><path class="sapron" d="M300,440 L300,600 Q290,610 278,600 L276,452 Z"/>
  {back_arm("l")}{back_arm("r", with_tongs=True)}
  <g id="s_hammer_back">{hammer_back(100, 420, 286, 112)}</g>
  <g id="back_head" transform="translate(0 34) translate(200 196) scale(0.84) translate(-200 -196)">
    <path class="sbeard" d="M136,124 C130,154 132,182 142,200 L126,214 C144,226 166,226 184,212 L184,200 C200,206 216,206 216,200 L216,212 C234,226 256,226 274,214 L258,200 C268,182 270,154 264,124 Z"/>
    <path class="sbeardline" d="M158,140 C152,162 152,182 158,198 M200,132 L200,198 M242,140 C248,162 248,182 242,198"/>
    <circle class="skin" cx="140" cy="160" r="8"/><circle class="skin" cx="260" cy="160" r="8"/>
    <g id="s_back_band">
      <path class="sband" d="M142,128 C140,88 166,66 200,64 C234,66 260,88 258,128 Q200,114 142,128 Z"/>
      <path class="sapdk" d="M144,104 Q200,96 256,104 L257,115 Q200,107 143,115 Z"/>
      <path class="sband" d="M196,110 L168,148 L186,150 L200,124 L214,150 L232,148 L204,110 Z"/>
      <circle class="sband" cx="200" cy="110" r="8"/>
    </g>
  </g>
</g>
"""

if __name__ == "__main__":
    from gen import ANIME_CSS, ANIME_DEFS
    import anime_dark
    for style, css in (("farbe", ANIME_CSS + S_CSS), ("scherenschnitt", anime_dark.css + S_DARK)):
        for name, body in (("front", FRONT), ("seite", SIDE), ("rueck", BACK)):
            body = body.replace('style="display:none"', '')
            bg = '#e9dcc8' if style == "farbe" else '#a8604e'
            open(f"schmied_{name}_{style}.svg", "w").write(
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-60 -130 520 920" width="520" height="920"><title>Schmied – {name}</title>'
                f'<defs>{ANIME_DEFS}{S_DEFS}</defs><style>{css}</style><rect x="-60" y="-130" width="520" height="920" fill="{bg}"/>{body}</svg>')
    print("schmied ok")
