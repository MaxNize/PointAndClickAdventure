"""Professor Odilo Gernegroß (O. G.): mager, arrogant, pingelig – und fachlich schwach.
Gleiches Rig/IDs wie die anderen Figuren; eigener steifer, hochnäsiger Gang.
Silhouette: lang und dürr, langes Gesicht, ungepflegter Seitenscheitel, rechteckige Brille,
Frack mit Schößen, erhobener Zeigefinger, Klemmbrett mit seinem 'eigenen' Zirkel.
Leuchtfarbe: Magenta (Brillengläser, Zirkel-Diagramm)."""
from boy import mir
from profile import profile

NAME = "Professor Odilo Gernegroß"
P_CSS = '''
.pcoat{fill:#3e4838}.pcoatt{fill:#343d30}.pcoatsh{fill:#2c3428}.pvest{fill:#b8974a}.pshirt{fill:#ece4d2}.ptie{fill:#8a2f5a}
.ppants{fill:#5a5660}.pshoe{fill:#2a2226}.phair{fill:#a8996e}.phairline{fill:none;stroke:#7a6c48;stroke-width:1.3}
.pboard{fill:#7a5232}.ppaper{fill:#efe6cf}.pcirc{fill:none;stroke:#8a2f7a;stroke-width:1.6}
.pglass{fill:#e8f4f4;fill-opacity:.35;stroke:#2a2226;stroke-width:2}.pglint{fill:none;stroke:#fff;stroke-width:1.4;opacity:.8}
.pchain{fill:none;stroke:#c99846;stroke-width:1.6}.plid{fill:#f4e2d6}.pbrow{fill:none;stroke:#7a6c48;stroke-width:2.2;stroke-linecap:round}
.glowm{fill:url(#glowMagenta)}
.pcoat,.pcoatt,.pcoatsh,.pvest,.pshirt,.ptie,.ppants,.pshoe,.phair,.pboard,.ppaper{stroke:#2a1a12;stroke-width:2.2;stroke-linejoin:round}
'''
P_DARK = '''
.pcoat,.pcoatt,.pcoatsh,.pvest,.pshirt,.ptie,.ppants,.pshoe,.phair,.pboard,.ppaper,.plid{fill:#140e10;stroke:#140e10;stroke-width:1.2}
.phairline,.pbrow,.pglint{display:none}.pchain{stroke:#e0ad4a;opacity:.35}
.pglass{fill:none;stroke:#ff6ad5;stroke-width:1.6;opacity:.9}
.pcirc{stroke:#ff6ad5;stroke-width:1.8}.glowm{fill:url(#glowMagenta)}
'''
P_DEFS = '''<radialGradient id="glowMagenta"><stop offset="0" stop-color="#ff8ae0" stop-opacity=".8"/><stop offset="1" stop-color="#ff6ad5" stop-opacity="0"/></radialGradient>'''

# Steif, hochnäsig: aufrecht/leicht zurückgelehnt, kaum Kniebeugung, wenig Armschwung, federnd
WALK_STYLE = {'hip': 17, 'knee': 22, 'arm': 6, 'fore': 4, 'lean': -3, 'swag': 0.8, 'lift': 10, 'bob': 7, 'sway': 1.0, 'armOut': 3, 'speed': 280}
SCALE = 1.06
ROOT = f'transform="translate(200 773) scale({SCALE}) translate(-200 -773)"'
LONGFACE = 'transform="translate(200 160) scale(0.9 1.1) translate(-200 -160)"'

LINES = [
    "Ah, ein Erstjähriger. Wie … erfrischend unbedarft.",
    "Der Gernegroß-Zirkel! Meine Erfindung. Siebenfach verbessert, versteht sich.",
    "Ihre Schrift ist zwei Millimeter zu schräg. Punktabzug.",
    "Die Klausur ist selbstverständlich fair. Für mich jedenfalls.",
    "Mein Zirkel kommt mit einem Strich weniger aus. Dafür explodiert er nur gelegentlich.",
    "Wer meine Zirkel nicht versteht, versteht die Alchemie nicht.",
]

def clipboard(x, y, rot=-8):
    """Klemmbrett mit dem 'erfundenen' Zirkel (leicht schiefes Dreieck, überflüssige Linie)."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<circle class="glowm" cx="{x}" cy="{y}" r="30"/>'
            f'<rect class="pboard" x="{x-18}" y="{y-24}" width="36" height="48" rx="3"/>'
            f'<rect class="ppaper" x="{x-14}" y="{y-18}" width="28" height="38" rx="1"/>'
            f'<rect class="brass" x="{x-7}" y="{y-27}" width="14" height="6" rx="2"/>'
            f'<circle class="pcirc" cx="{x}" cy="{y}" r="10"/>'
            f'<path class="pcirc" d="M{x},{y-10} L{x+9},{y+5} L{x-8},{y+6} Z M{x-10},{y-3} L{x+11},{y+8} M{x+4},{y-13} l3,-3"/>'
            f'</g>')

def glasses_front():
    s = ''
    for cx in (181, 219):
        s += f'<rect class="pglass" x="{cx-15}" y="151" width="30" height="13" rx="1.5"/>'
        s += f'<path class="pglint" d="M{cx-9},162 L{cx-3},153 M{cx-3},162 L{cx+1},156"/>'
    s += '<path class="pglass" d="M196,155 Q200,152 204,155" fill="none"/>'
    s += '<path class="pglass" d="M166,155 L152,153 M234,155 L248,153" fill="none"/>'
    return s

def eye(cx, side):
    m = 1 if side == "l" else -1
    X = lambda dx: cx + dx*m
    raised = side == "l"
    brow = (f'M{X(-12)},144 Q{X(0)},136 {X(12)},141' if raised else f'M{X(-12)},146 Q{X(0)},143 {X(12)},145')
    return (f'<path class="eyewhite" d="M{X(-10)},158 Q{X(0)},154 {X(10)},157 Q{X(9)},162 {X(0)},163 Q{X(-9)},162 {X(-10)},158 Z"/>'
            f'<ellipse class="iris" cx="{X(1)}" cy="159.5" rx="3.3" ry="4"/><circle class="pupil" cx="{X(1)}" cy="159.5" r="1.5"/>'
            f'<circle class="hl" cx="{X(2.5)}" cy="160.5" r="0.9"/>'
            f'<path class="plid" d="M{X(-11)},157.5 Q{X(0)},150 {X(11)},155.5 L{X(11)},157.6 Q{X(0)},156.6 {X(-11)},159.6 Z" style="stroke:none"/>'
            f'<path class="lash" d="M{X(-11)},159.4 Q{X(0)},156.2 {X(11)},157.4" style="stroke-width:2"/>'
            f'<path class="pbrow" d="{brow}"/>')

# ------------------------------------------------------------------ FRONT
def front_leg(side):
    d = 'M181,350 C179,450 181,620 183,730 L197,730 C198,620 198,450 199,350 Z'
    return f'<path class="ppants" d="{d if side=="l" else mir(d)}"/><path class="line" d="{"M190,360 L190,720" if side=="l" else "M210,360 L210,720"}"/>'

def front_shoe(side):
    d = 'M180,722 L199,722 L200,760 Q201,773 189,773 L174,773 Q162,772 170,762 Z'
    return f'<path class="pshoe" d="{d if side=="l" else mir(d)}"/>'

HAIR_TOP = 'M152,128 C150,100 176,90 200,90 C224,90 250,100 248,128 Q232,108 200,100 Q186,98 180,100 Q166,110 152,128 Z'
PART_L = 'M180,97 Q164,100 156,114 C150,130 150,150 152,168 L158,158 L160,176 L164,150 C165,134 170,118 180,106 Z'
PART_R = 'M180,97 Q212,92 238,106 Q254,120 251,150 L245,138 L243,164 L236,142 L230,158 L224,134 L215,150 L208,126 L199,140 L194,120 L186,128 L182,110 Z'
BACKHAIR = 'M150,118 C138,150 139,192 146,214 L153,202 L156,218 L162,198 L165,206 L167,132 Z'
STRAYS = ('M198,92 Q192,78 182,74 Q192,80 194,92 Z M204,92 Q212,80 226,82 Q214,84 208,94 Z '
          'M160,104 Q148,96 140,100 Q150,100 158,110 Z M240,104 Q254,94 262,98 Q252,100 242,110 Z')

FRONT_HEAD = f'''
  <g id="head" {LONGFACE}>
    <path class="phair" d="{BACKHAIR}"/><path class="phair" d="{mir(BACKHAIR)}"/>
    <circle class="skin" cx="152" cy="156" r="6"/><circle class="skin" cx="248" cy="156" r="6"/>
    <path class="skin" d="M154,124 C153,160 165,184 190,196 Q200,200 210,196 C235,184 247,160 246,124 Q200,114 154,124 Z"/>
    <path class="cel" d="M154,124 L156,140 Q166,124 180,110 Q210,118 244,168 L246,124 Q200,114 154,124 Z"/>
    {eye(181, "l")}{eye(219, "r")}
    <path class="nose" d="M200,160 L201.5,175 L198,176.5"/>
    <path class="mouthline" d="M192,186 Q201,186 209,182"/>
    {glasses_front()}
    <path class="phair" d="{HAIR_TOP}"/>
    <path class="phair" d="{PART_L}"/><path class="phair" d="{PART_R}"/>
    <path class="phair" d="{STRAYS}"/>
    <path class="phairline" d="M181,91 L180,103 M186,101 Q218,102 242,134 M190,108 Q214,116 230,150 M196,116 Q210,124 214,146 M176,104 Q162,116 156,140"/>
  </g>'''

FRONT = f'''
<g id="character" {ROOT}>
  <ellipse class="groundshadow" cx="200" cy="773" rx="52" ry="6"/>
  <path class="pcoatt" d="M168,318 L232,318 L242,572 L214,562 L200,520 L186,562 L158,572 Z"/>
  <g id="front_leg_l">{front_leg("l")}</g><g id="front_leg_r">{front_leg("r")}</g>
  <g id="boot_l">{front_shoe("l")}</g><g id="boot_r">{front_shoe("r")}</g>
  <g id="p_body">
    <rect class="skin" x="193" y="188" width="14" height="34"/>
    <path class="pshirt" d="M184,214 Q200,208 216,214 L218,300 L182,300 Z"/>
    <path class="pvest" d="M182,232 L200,246 L218,232 L220,336 Q200,342 180,336 Z"/>
    <circle class="brass" cx="200" cy="268" r="2.2"/><circle class="brass" cx="200" cy="286" r="2.2"/><circle class="brass" cx="200" cy="304" r="2.2"/>
    <path class="pchain" d="M200,296 Q210,312 218,304"/><circle class="brass" cx="219" cy="302" r="3"/>
    <path class="pshirt" d="M186,204 L197,214 L189,224 Z"/><path class="pshirt" d="{mir('M186,204 L197,214 L189,224 Z')}"/>
    <path class="ptie" d="M192,212 L208,212 L204,226 L210,244 L200,252 L190,244 L196,226 Z"/>
    <path class="pcoat" d="M178,214 L162,228 C157,270 157,310 162,342 L180,346 L186,300 L190,240 L196,214 Z"/>
    <path class="pcoat" d="{mir('M178,214 L162,228 C157,270 157,310 162,342 L180,346 L186,300 L190,240 L196,214 Z')}"/>
    <path class="pcoatsh" d="M196,214 L182,226 L188,262 Z"/><path class="pcoatsh" d="{mir('M196,214 L182,226 L188,262 Z')}"/>
  </g>
  <g id="arm_l">
    <path class="pcoat" d="M172,220 C156,224 150,248 150,276 L147,342 L167,345 L168,280 C170,262 174,246 179,236 Z"/>
    <path class="pcoatsh" d="M145,336 L169,339 L170,356 L143,353 Z"/>
    {clipboard(150, 370)}
    <ellipse class="skin" cx="158" cy="360" rx="7" ry="9"/>
  </g>
  <g id="arm_r">
    <path class="pcoat" d="M228,220 C244,224 252,248 250,276 L248,300 L234,300 L230,260 Z"/>
    <path class="pcoat" d="M238,292 L252,296 L262,222 L250,218 Z"/>
    <path class="pcoatsh" d="M248,212 L266,216 L262,230 L246,226 Z"/>
    <ellipse class="skin" cx="256" cy="206" rx="7" ry="8.5"/>
    <rect class="skin" x="254" y="180" width="5" height="22" rx="2.5"/>
  </g>
  {FRONT_HEAD}
</g>
'''

# ------------------------------------------------------------------ SEITE
PROF = profile(nose="pointy", L=15, ty=160, lip=250.5, chin=245, cy=196, jaw="soft", jx=210)

def side_leg(gid, far=False):
    thigh = 'M194,352 C191,430 196,500 199,550 L213,553 C216,500 219,430 216,352 Z'
    shin = 'M199,546 C195,600 198,680 200,730 L212,730 C213,690 215,620 213,553 Z'
    shoe = 'M197,722 L213,722 L213,744 L246,756 Q252,764 242,768 L201,768 L197,760 Z'
    s = f'<g id="{gid}"><path class="ppants" d="{thigh}"/>'
    if far: s += f'<path class="shade" d="{thigh}"/>'
    s += f'<g id="{gid}_shin"><circle class="ppants" cx="206" cy="550" r="7.5"/><path class="ppants" d="{shin}"/><path class="pshoe" d="{shoe}"/>'
    if far: s += f'<circle class="shade" cx="206" cy="550" r="7.5"/><path class="shade" d="{shin}"/><path class="shade" d="{shoe}"/>'
    return s + '</g></g>'

def side_arm(gid, far=False, board=False):
    up = 'M196,226 C188,242 189,272 198,290 L214,290 C220,272 220,242 212,226 Z'
    lo = 'M198,284 L213,284 L211,350 L200,350 Z'
    s = f'<g id="{gid}"><g id="{gid}_fore"><path class="pcoat" d="{lo}"/>'
    s += '<path class="pcoatsh" d="M196,346 L215,346 L218,364 L193,364 Z"/>'
    if board:
        s += clipboard(214, 382, 6)
    s += '<ellipse class="skin" cx="206" cy="372" rx="7" ry="9"/>'
    if far: s += f'<path class="shade" d="{lo}"/>'
    s += f'</g><path class="pcoat" d="{up}"/>'
    if far: s += f'<path class="shade" d="{up}"/>'
    return s + '</g>'

SIDE_HAIR = ('M154,118 C150,100 176,90 206,92 C222,94 236,100 244,112 L230,112 L218,118 C214,140 214,160 212,178 '
             'L210,200 L203,210 L197,200 L189,214 L182,200 L174,212 L167,198 L159,204 C150,172 148,140 154,118 Z')
SIDE_FRONT = 'M212,100 C232,100 248,112 251,132 L244,126 L243,146 L236,124 L230,138 L226,116 Z'
SIDE_STRAYS = 'M190,94 Q182,80 170,78 Q182,84 186,96 Z M214,96 Q222,82 236,84 Q224,88 218,98 Z M156,120 Q142,116 136,124 Q146,120 156,128 Z'

SIDE = f'''
<g id="characterSide" style="display:none" {ROOT}>
  <ellipse class="groundshadow" cx="210" cy="773" rx="40" ry="5"/>
  <path class="pcoatt" d="M190,320 L212,320 L198,584 L162,574 Z"/>
  {side_arm("side_arm_far", far=True)}
  {side_leg("side_leg_far", far=True)}
  {side_leg("side_leg_near")}
  <g id="side_torso">
    <rect class="skin" x="198" y="184" width="14" height="40"/>
    <path class="pcoat" d="M190,222 C180,250 180,300 186,344 L222,344 C226,300 226,252 220,230 Q212,220 204,218 Z"/>
    <path class="pvest" d="M214,232 L222,236 C226,270 226,306 224,340 L216,340 Z"/>
    <path class="pshirt" d="M210,206 L222,214 L216,224 Z"/>
    <path class="ptie" d="M214,214 L226,218 L222,230 L228,246 L220,250 L216,230 Z"/>
    <path class="pcoatsh" d="M206,214 L224,232 L216,256 Z"/>
    <path class="pchain" d="M218,296 Q224,306 222,314"/>
  </g>
  {side_arm("side_arm_near", board=True)}
  <g id="side_head" transform="rotate(-5 205 190) translate(205 150) scale(0.95 1.08) translate(-205 -150)">
    <path class="skin" d="{PROF["d"]}"/>
    <path class="phair" d="{SIDE_HAIR}"/>
    <path class="phairline" d="M170,104 C162,140 162,174 168,204 M186,100 C178,140 178,178 184,208 M202,98 C196,130 194,170 198,200"/>
    <path class="skin" d="M199.5,181 C195,183.5 189,180.5 186,176 C183,171 182.2,165 182.6,161 C183.2,157 185.5,154.4 188,154.2 C190.6,154 192.6,155.6 193.6,157.8 C195.5,162 197.5,168 199,173 Z"/>
    <path class="line" d="M187.5,159.5 Q185.2,166.5 189.5,173.5"/>
    <ellipse class="iris" cx="232.5" cy="155" rx="2.5" ry="4"/><circle class="hl" cx="233.2" cy="156.4" r="0.9"/>
    <path class="plid" d="M225,150 Q232,147 240,151 L240,153.6 Q232,151.5 225,154 Z" style="stroke:none"/>
    <path class="lash" d="M225,154 Q232,151.4 240,153.4" style="stroke-width:2"/>
    <path class="pbrow" d="M224,143 Q232,135.5 243,139"/>
    <path class="mouthline" d="{PROF["mouth"]}"/>
    <rect class="pglass" x="226" y="149" width="18" height="11" rx="1.2"/>
    <path class="pglint" d="M230,158 L234,151 M235,158 L238,153"/>
    <path class="pglass" d="M226,153 L196,151" fill="none"/>
    <path class="phair" d="{SIDE_FRONT}"/>
    <path class="phair" d="{SIDE_STRAYS}"/>
  </g>
</g>
'''

# ------------------------------------------------------------------ RÜCKEN
def back_leg(side):
    x = 184 if side == "l" else 204
    return f'<g id="back_leg_{side}">{front_leg(side)}{front_shoe(side)}<rect class="pshoe" x="{x}" y="760" width="12" height="13" rx="2"/></g>'

def back_arm(side, board=False):
    m = 1 if side == "l" else -1
    X = lambda x: x if m == 1 else 400 - x
    up = f'M{X(172)},220 C{X(156)},224 {X(150)},248 {X(150)},276 L{X(147)},342 L{X(167)},345 L{X(168)},280 C{X(170)},262 {X(174)},246 {X(179)},236 Z'
    s = f'<g id="back_arm_{side}"><g transform="rotate({6*m} {X(168)} 230)">'
    s += f'<path class="pcoat" d="{up}"/><path class="pcoatsh" d="M{X(145)},336 L{X(169)},339 L{X(170)},356 L{X(143)},353 Z"/>'
    if board: s += clipboard(X(152), 374, 8*m)
    s += f'<ellipse class="skin" cx="{X(158)}" cy="362" rx="7" ry="9"/>'
    return s + '</g></g>'

BACK_HAIR = ('M148,116 C138,150 140,190 148,212 L156,200 L162,214 L170,202 L178,216 L186,204 L194,216 L200,206 '
             'L206,216 L214,204 L222,216 L230,202 L238,214 L244,200 L252,212 C260,190 262,150 252,116 '
             'C252,94 230,82 200,82 C170,82 148,94 148,116 Z')

BACK = f'''
<g id="characterBack" style="display:none" {ROOT}>
  <ellipse class="groundshadow" cx="200" cy="773" rx="52" ry="6"/>
  <g id="back_legs">{back_leg("l")}{back_leg("r")}</g>
  <path class="pcoat" d="M166,222 Q200,212 234,222 C238,270 238,310 236,330 L240,580 L206,570 L200,520 L194,570 L160,580 L164,330 C162,310 162,270 166,222 Z"/>
  <path class="line" d="M200,232 L200,520 M176,336 L224,336"/>
  <circle class="brass" cx="190" cy="336" r="2.6"/><circle class="brass" cx="210" cy="336" r="2.6"/>
  {back_arm("l")}{back_arm("r", board=True)}
  <g id="back_head" {LONGFACE}>
    <rect class="skin" x="193" y="186" width="14" height="38"/>
    <circle class="skin" cx="152" cy="156" r="6"/><circle class="skin" cx="248" cy="156" r="6"/>
    <path class="phair" d="{BACK_HAIR}"/>
    <path class="phair" d="{STRAYS}"/>
    <path class="phairline" d="M180,86 L182,104 M184,104 C190,140 192,176 192,206 M188,100 C214,130 220,170 218,206 M170,104 C160,140 158,176 162,204 M230,104 C240,140 242,176 238,204"/>
  </g>
</g>
'''

if __name__ == "__main__":
    from gen import ANIME_CSS, ANIME_DEFS
    import anime_dark
    for style, css in (("farbe", ANIME_CSS + P_CSS), ("scherenschnitt", anime_dark.css + P_DARK)):
        for name, body in (("front", FRONT), ("seite", SIDE), ("rueck", BACK)):
            body = body.replace('style="display:none"', '')
            bg = '#e9dcc8' if style == "farbe" else '#a8604e'
            open(f"professor_{name}_{style}.svg", "w").write(
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -50 440 840" width="440" height="840"><title>{NAME} – {name}</title>'
                f'<defs>{ANIME_DEFS}{P_DEFS}</defs><style>{css}</style><rect x="-20" y="-50" width="440" height="840" fill="{bg}"/>{body}</svg>')
    print("professor ok")
