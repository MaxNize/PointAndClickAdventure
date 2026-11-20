"""Lehrling (zweite Figur): Front-, Seiten- und Rückansicht.
Gleiches Koordinatensystem und gleiche Gelenk-IDs wie die Alchemistin,
damit die Laufanimation aus der Demo unverändert funktioniert."""
import re
from gen import scallop

def mir(d):
    """Spiegelt alle x-Koordinaten eines Pfads (nur absolute M/L/C/Q/Z) um x=200."""
    return re.sub(r'(-?\d+\.?\d*),(-?\d+\.?\d*)', lambda m: f"{400-float(m.group(1)):g},{m.group(2)}", d)

# ------------------------------------------------------------------ Farben
BOY_CSS = '''
.coat{fill:#efe7d6}.coatsh{fill:#cdbfa4}.vest{fill:#d6bf94}.shirt{fill:#4b3228}.tie{fill:#8a4a2a}
.pants{fill:#3e2c25}.glove{fill:#3a2620}.leather{fill:#7a4a2c}.pack{fill:#8a5a36}.packdark{fill:#5e3a22}
.bhair{fill:#e6b48e}.bhairsh{fill:#c58b66}.bhairline{fill:none;stroke:#9a6446;stroke-width:1.3}
.bcap{fill:#ece4d0}.bcapband{fill:#3a2a22}.bbrim{fill:#2f2521}
.lensb{fill:#8fd0dc;stroke:#3b2219;stroke-width:1.5}.tube{fill:#6fc3ff}.glowb{fill:url(#glowBlue)}
.biris{fill:url(#irisB)}.hlb{fill:#fff}
.coat,.coatsh,.vest,.shirt,.tie,.pants,.glove,.leather,.pack,.packdark,.bhair,.bcap,.bcapband,.bbrim{stroke:#3b2219;stroke-width:2.2;stroke-linejoin:round}
'''
BOY_DARK = '''
.coat,.coatsh,.vest,.shirt,.tie,.pants,.glove,.leather,.pack,.packdark,.bhair,.bhairsh,.bcap,.bcapband,.bbrim{fill:#140e10;stroke:#140e10;stroke-width:1.2}
.biris,.bhairline{display:none}
.lensb{fill:#7fe3ff;stroke:none}.tube{fill:#6fc3ff}.glowb{fill:url(#glowBlue)}.hlb{fill:#9ff0ff}
'''
BOY_DEFS = '''<radialGradient id="glowBlue"><stop offset="0" stop-color="#8fe6ff" stop-opacity=".9"/><stop offset="1" stop-color="#8fe6ff" stop-opacity="0"/></radialGradient>
<linearGradient id="irisB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1f3d55"/><stop offset=".6" stop-color="#3f86b0"/><stop offset="1" stop-color="#9fe0f0"/></linearGradient>'''

# ------------------------------------------------------------------ gemeinsame Teile
def goggles_front():
    s = ''
    for cx in (180, 222):
        s += f'<circle class="brass" cx="{cx}" cy="103" r="15"/><circle class="lensb" cx="{cx}" cy="103" r="10"/>'
    s += '<rect class="brass" x="193" y="100" width="16" height="6" rx="2"/>'
    s += '<path class="lensshine" d="M174,99 L180,95 L183,98 L177,102 Z M216,99 L222,95 L225,98 L219,102 Z"/>'
    s += '<circle class="brass" cx="152" cy="104" r="6"/><circle class="lensb" cx="152" cy="104" r="3"/>'
    return s

def eye(cx, side):
    m = 1 if side == "l" else -1
    X = lambda dx: cx + dx * m
    white = f"M{X(-12)},157 Q{X(0)},149 {X(11)},154 Q{X(10)},163 {X(0)},164.5 Q{X(-11)},163.5 {X(-12)},157 Z"
    return f'''<g id="b_eye_{side}">
      <clipPath id="bclip_{side}"><path d="{white}"/></clipPath>
      <path class="eyewhite" d="{white}"/>
      <g clip-path="url(#bclip_{side})">
        <ellipse class="biris" cx="{X(-0.5)}" cy="157.5" rx="5.8" ry="7"/>
        <ellipse class="pupil" cx="{X(-0.5)}" cy="157.5" rx="2.4" ry="3.6"/>
        <path class="irisshadow" d="M{cx-15},146 L{cx+15},146 L{cx+15},155 Q{cx},151 {cx-15},155 Z"/>
      </g>
      <circle class="hlb" cx="{X(2.5)}" cy="155" r="1.8"/>
      <path class="lash" d="M{X(-13)},157 Q{X(-1)},148 {X(12)},153.5"/>
      <path class="brow2" d="M{X(-13)},143 Q{X(0)},139.5 {X(12)},141.5 L{X(12)},144 Q{X(0)},142.5 {X(-13)},146 Z"/>
    </g>'''

# ------------------------------------------------------------------ FRONT
def front_leg(side):
    d = 'M162,340 C157,420 161,500 165,560 C163,620 165,680 169,736 L195,736 C197,680 199,620 197,560 C200,500 201,420 200,340 Z'
    if side == "r": d = mir(d)
    s = f'<path class="pants" d="{d}"/>'
    sh = 'M192,340 C196,420 196,500 192,560 C194,620 192,680 191,736 L195,736 C197,680 199,620 197,560 C200,500 201,420 200,340 Z'
    s += f'<path class="shade" d="{sh if side=="l" else mir(sh)}"/>'
    if side == "r":
        s += '<path class="leather" d="M203,470 L238,466 L238,476 L203,480 Z"/><rect class="brass" x="214" y="467" width="7" height="11" rx="1"/>'
        s += '<rect class="leather" x="224" y="476" width="16" height="20" rx="3"/><circle class="brass" cx="232" cy="486" r="4"/>'
    return s

def front_boot(side):
    d = 'M166,724 L198,724 L199,758 Q200,773 186,773 L171,773 Q161,773 164,758 Z'
    if side == "r": d = mir(d)
    s = f'<path class="boot" d="{d}"/>'
    b = 'M164,764 L200,764 L199,773 L165,773 Z'
    s += f'<path class="bootdark" d="{b if side=="l" else mir(b)}"/>'
    return s

FRONT_HEAD = f'''
  <g id="head">
    <path class="bhair" d="M150,118 C138,140 139,168 146,186 L154,177 L157,192 L163,172 L163,126 Z"/>
    <path class="bhair" d="{mir('M150,118 C138,140 139,168 146,186 L154,177 L157,192 L163,172 L163,126 Z')}"/>
    <circle class="skin" cx="152" cy="155" r="6.5"/><circle class="skin" cx="248" cy="155" r="6.5"/>
    <path class="skin" d="M153,124 C152,158 164,182 190,195 Q200,199 210,195 C236,182 248,158 247,124 Q200,114 153,124 Z"/>
    <path class="cel" d="M154,140 L164,144 L172,146 L182,128 L190,146 L200,124 L208,146 L218,128 L226,146 L236,142 L246,138 L247,124 Q200,114 153,124 Z"/>
    {eye(180, "l")}{eye(220, "r")}
    <path class="nose" d="M200.5,172 l-1.6,2.2"/>
    <path class="mouthline" d="M195,183 Q200,184.5 205,183"/>
    <path class="bhair" d="M150,142 Q147,106 200,100 Q253,106 250,142 L242,130 L238,148 L228,124 L219,147 L209,121 L200,149 L191,121 L181,147 L172,124 L162,146 L158,130 Z"/>
    <path class="bhair" d="M154,124 L133,128 L148,136 L135,146 L156,145 Z"/>
    <path class="bhair" d="{mir('M154,124 L133,128 L148,136 L135,146 L156,145 Z')}"/>
    <path class="bhairline" d="M191,121 Q195,112 198,106 M209,121 Q210,113 207,106 M228,124 Q226,116 222,110 M172,124 Q176,116 180,110"/>
    <g id="b_cap">
      <path class="bcap" d="M140,116 C128,94 146,68 200,62 C254,68 272,94 260,116 Z"/>
      <path class="cel" d="M140,116 C136,106 138,98 144,92 Q200,110 256,92 C262,98 264,106 260,116 Z"/>
      <path class="line" d="M200,64 L200,92 M168,70 Q176,84 178,94 M232,70 Q224,84 222,94"/>
      <path class="bcapband" d="M143,100 Q200,108 257,100 L258,117 Q200,125 142,117 Z"/>
      <path class="bbrim" d="M146,115 Q200,138 254,115 Q258,128 200,137 Q142,128 146,115 Z"/>
      {goggles_front()}
    </g>
  </g>'''

FRONT = f'''
<g id="character">
  <ellipse class="groundshadow" cx="200" cy="772" rx="66" ry="7"/>
  <g id="b_pack_front">
    <circle class="glowb" cx="256" cy="170" r="30"/>
    <rect class="vialglass" x="250" y="146" width="13" height="86" rx="5"/>
    <rect class="tube" x="252.5" y="166" width="8" height="62" rx="3"/>
    <rect class="cork" x="249" y="138" width="15" height="10" rx="2"/>
    <rect class="pack" x="144" y="214" width="112" height="124" rx="12"/>
  </g>
  <path class="coatsh" d="M160,326 L240,326 L256,612 L144,612 Z"/>
  <g id="front_leg_l">{front_leg("l")}</g><g id="front_leg_r">{front_leg("r")}</g>
  <g id="boot_l">{front_boot("l")}</g><g id="boot_r">{front_boot("r")}</g>
  <g id="b_torso">
    <rect class="skin" x="192" y="186" width="16" height="34"/>
    <path class="shade" d="M192,186 L208,186 L208,200 Q200,205 192,200 Z"/>
    <path class="shirt" d="M176,214 Q200,205 224,214 L228,300 L172,300 Z"/>
    <path class="shirt" d="M190,206 L200,220 L210,206 L214,214 L200,228 L186,214 Z"/>
    <path class="vest" d="M184,228 L200,236 L216,228 L221,332 Q200,340 179,332 Z"/>
    <circle class="brass" cx="200" cy="262" r="2.4"/><circle class="brass" cx="200" cy="284" r="2.4"/><circle class="brass" cx="200" cy="306" r="2.4"/>
    <path class="tie" d="M194,214 L206,214 L203,236 L200,242 L197,236 Z"/>
    <path class="brass" d="M205,270 Q214,282 211,296" fill="none" stroke-width="1.6"/>
  </g>
  <g id="b_coat_front">
    <path class="coat" d="M162,222 L144,240 C140,330 140,470 138,612 L178,604 L186,344 L190,262 L196,214 Z"/>
    <path class="coat" d="{mir('M162,222 L144,240 C140,330 140,470 138,612 L178,604 L186,344 L190,262 L196,214 Z')}"/>
    <path class="shade" d="M144,240 C140,330 140,470 138,612 L150,610 C150,470 151,330 154,250 Z"/>
    <path class="shade" d="{mir('M144,240 C140,330 140,470 138,612 L150,610 C150,470 151,330 154,250 Z')}"/>
    <path class="coatsh" d="M196,214 L174,228 L186,296 Z"/><path class="coatsh" d="{mir('M196,214 L174,228 L186,296 Z')}"/>
    <rect class="brass" x="176" y="300" width="5" height="5"/><rect class="brass" x="219" y="300" width="5" height="5"/>
    <path class="line" d="M160,420 L170,420 M231,420 L240,420"/>
  </g>
  <g id="b_belt">
    <path class="leather" d="M150,318 Q200,328 250,318 L250,331 Q200,341 150,331 Z"/>
    <rect class="brass" x="194" y="322" width="12" height="13" rx="2"/>
    <rect class="leather" x="146" y="328" width="24" height="28" rx="3"/><path class="packdark" d="M146,328 L170,328 L170,337 L146,337 Z"/>
    <rect class="vialglass" x="232" y="326" width="7" height="22" rx="3"/><rect class="tube" x="233.5" y="336" width="4" height="11" rx="2"/>
  </g>
  <g id="arm_l">
    <path class="coat" d="M160,224 C142,228 135,250 135,280 L131,356 L155,360 L160,286 C162,262 166,244 170,236 Z"/>
    <path class="shade" d="M135,280 L131,356 L140,357 L144,282 Z"/>
    <path class="coatsh" d="M130,348 L156,352 L155,368 L129,364 Z"/>
    <path class="glove" d="M131,366 L154,368 Q157,384 150,394 Q142,400 134,394 Q128,384 131,366 Z"/>
    <path class="brass" d="M134,368 L152,370" fill="none" stroke-width="2"/>
  </g>
  <g id="arm_r">
    <path class="coat" d="M240,224 C258,228 266,250 265,276 L264,302 L242,302 L240,262 Z"/>
    <path class="coat" d="M244,290 L267,296 L240,336 L222,326 Z"/>
    <path class="coatsh" d="M226,318 L240,326 L234,336 L220,328 Z"/>
    <path class="glove" d="M220,326 Q212,322 208,330 Q207,340 216,342 Q226,342 230,334 Z"/>
  </g>
  {FRONT_HEAD}
</g>
'''

# ------------------------------------------------------------------ SEITE (Blick nach rechts)
def side_leg(gid, far=False):
    thigh = 'M188,352 C184,430 190,500 195,550 L216,553 C220,500 224,430 222,352 Z'
    shin = 'M196,546 C189,600 194,680 197,730 L215,730 C217,690 219,620 216,553 Z'
    boot = 'M194,722 L217,722 L217,742 L241,750 Q249,758 243,768 L199,768 L195,760 Z'
    s = f'<g id="{gid}"><path class="pants" d="{thigh}"/>'
    s += '<path class="shade" d="M188,352 C184,430 190,500 195,550 L201,550 C197,500 194,430 196,352 Z"/>'
    if far: s += f'<path class="shade" d="{thigh}"/>'
    s += f'<g id="{gid}_shin"><circle class="pants" cx="206" cy="550" r="10.5"/><path class="pants" d="{shin}"/>'
    s += f'<path class="boot" d="{boot}"/><path class="bootdark" d="M196,762 L244,762 L243,768 L199,768 Z"/>'
    if far: s += f'<circle class="shade" cx="206" cy="550" r="10.5"/><path class="shade" d="{shin}"/><path class="shade" d="{boot}"/>'
    s += '</g></g>'
    return s

def side_arm(gid, far=False):
    upper = 'M190,226 C179,240 181,272 194,290 L215,290 C225,272 226,240 214,226 Z'
    lower = 'M194,284 L215,284 L213,362 L197,362 Z'
    s = f'<g id="{gid}"><g id="{gid}_fore">'
    s += f'<path class="coat" d="{lower}"/><path class="shade" d="M194,284 L200,284 L200,362 L197,362 Z"/>'
    s += '<path class="coatsh" d="M195,352 L215,352 L214,368 L196,368 Z"/>'
    s += '<path class="glove" d="M196,366 L214,366 Q217,382 211,392 Q204,398 198,392 Q193,382 196,366 Z"/>'
    if far: s += f'<path class="shade" d="{lower}"/>'
    s += f'</g><path class="coat" d="{upper}"/>'
    if far: s += f'<path class="shade" d="{upper}"/>'
    return s + '</g>'

def girl_profile():
    import side
    m = re.search(r'<path id="side_face" class="skin" d="([^"]*)"', side.SIDE)
    return m.group(1)

SIDE = f'''
<g id="characterSide" style="display:none">
  <ellipse class="groundshadow" cx="210" cy="772" rx="46" ry="6"/>
  <path class="coat" d="M180,330 L208,330 C206,420 204,520 202,614 L146,606 C154,520 166,420 180,330 Z"/>
  <path class="shade" d="M180,330 L192,330 C182,420 170,520 160,608 L146,606 C154,520 166,420 180,330 Z"/>
  {side_arm("side_arm_far", far=True)}
  {side_leg("side_leg_far", far=True)}
  <path class="coat" d="M210,340 L232,340 C236,420 238,500 239,578 L218,582 C217,500 214,420 210,340 Z"/>
  <path class="shade" d="M210,340 L232,340 C236,420 238,500 239,578 L218,582 C217,500 214,420 210,340 Z"/>
  {side_leg("side_leg_near")}
  <g id="side_torso">
    <rect class="skin" x="196" y="184" width="18" height="40"/>
    <path class="coat" d="M184,222 C172,240 171,282 176,346 L235,346 C239,300 237,250 229,232 Q217,220 205,218 Z"/>
    <path class="vest" d="M220,228 L230,233 C235,262 235,302 233,340 L222,340 Z"/>
    <path class="shirt" d="M212,212 L226,222 L222,236 Z"/>
    <path class="coatsh" d="M206,214 L229,229 L220,256 Z"/>
    <path class="shade" d="M184,222 C172,240 171,282 176,346 L188,346 C184,290 186,248 194,226 Z"/>
    <path class="leather" d="M176,318 L235,318 L235,331 L176,331 Z"/>
    <rect class="leather" x="166" y="324" width="16" height="26" rx="3"/>
  </g>
  <g id="side_pack">
    <circle class="glowb" cx="160" cy="184" r="28"/>
    <rect class="vialglass" x="153" y="156" width="13" height="80" rx="5"/>
    <rect class="tube" x="155.5" y="174" width="8" height="58" rx="3"/>
    <rect class="cork" x="152" y="148" width="15" height="10" rx="2"/>
    <path class="pack" d="M150,226 Q144,226 144,236 L144,332 Q144,344 156,344 L186,344 L188,226 Z"/>
    <path class="packdark" d="M144,236 Q144,226 152,226 L188,226 L188,262 L144,262 Z"/>
    <rect class="brass" x="160" y="256" width="9" height="10" rx="1"/>
    <path class="leather" d="M186,226 Q202,220 216,232 L213,242 Q201,233 187,238 Z"/>
  </g>
  {side_arm("side_arm_near")}
  <g id="side_head">
    <path class="bhair" d="M158,118 C147,138 145,168 153,190 L161,180 L165,198 L173,184 L181,196 L186,180 C187,164 191,146 200,130 L214,122 Z"/>
    <path class="skin" d="{girl_profile()}"/>
    <path class="bhair" d="M157,118 C147,140 146,168 152,192 L159,184 L162,204 L170,191 L176,209 L183,195 L189,212 L199,203 L199,186 L193,178 C186,166 186,150 194,136 C200,128 206,123 214,120 Z"/>
    <path class="bhairline" d="M168,130 C162,150 162,172 166,196 M180,128 C174,146 174,170 178,198"/>
    <path class="skin" d="M199.5,181 C195,183.5 189,180.5 186,176 C183,171 182.2,165 182.6,161 C183.2,157 185.5,154.4 188,154.2 C190.6,154 192.6,155.6 193.6,157.8 C195.5,162 197.5,168 199,173 Z"/>
    <path class="line" d="M187.5,159.5 Q185.2,166.5 189.5,173.5"/>
    <ellipse class="blush" cx="237" cy="167" rx="7" ry="3"/>
    <g id="b_side_eye">
      <ellipse class="biris" cx="231.2" cy="152.4" rx="3" ry="7"/>
      <ellipse class="pupil" cx="231.1" cy="153.4" rx="1.4" ry="3.2"/>
      <circle class="hlb" cx="231.8" cy="148.6" r="1.4"/>
      <ellipse class="lowlash" cx="231.2" cy="152.4" rx="3" ry="7"/>
      <path class="lash" d="M236.4,142.6 Q229,139.4 224.8,143.4 Q221,147.6 219,154"/>
      <path class="brow2" d="M226,138 Q233,134.5 241,135.5 L240.5,138 Q233,137 226,140.5 Z"/>
    </g>
    <path class="mouthline" d="M248.6,180.2 L243,180.1"/>
    <path class="bhair" d="M198,112 C222,108 244,114 252,128 L257,146 L249,137 L247,152 L239,133 L233,148 L227,129 L219,142 L213,125 L204,136 Z"/>
    <path class="bhair" d="M204,136 L208,166 L212,150 L216,170 L218,138 Z"/>
    <path class="bhairline" d="M232,116 Q238,126 240,134 M218,118 Q222,126 224,130"/>
    <g id="b_side_cap">
      <path class="bcap" d="M138,114 C132,88 162,68 204,68 C240,70 260,88 256,114 Z"/>
      <path class="cel" d="M138,114 C136,104 138,96 142,90 Q200,108 254,94 C258,100 258,108 256,114 Z"/>
      <path class="line" d="M204,70 Q196,86 194,98"/>
      <path class="bcapband" d="M138,100 Q198,108 258,100 L258,118 Q198,126 138,118 Z"/>
      <path class="bbrim" d="M240,114 Q278,110 294,124 Q268,134 236,127 Z"/>
      <circle class="brass" cx="212" cy="104" r="12"/><ellipse class="lensb" cx="213" cy="104" rx="5" ry="8"/>
      <circle class="brass" cx="236" cy="104" r="14"/><ellipse class="lensb" cx="238" cy="104" rx="6.5" ry="9.5"/>
      <path class="lensshine" d="M234,99 L238,96 L240,98 L236,102 Z"/>
    </g>
  </g>
</g>
'''

# ------------------------------------------------------------------ RÜCKEN
def back_leg(side):
    s = front_leg(side) + front_boot(side)
    x = 175 if side == "l" else 213
    s += f'<rect class="bootdark" x="{x}" y="758" width="12" height="15" rx="2"/>'
    return f'<g id="back_leg_{side}">{s}</g>'

def back_arm(side):
    m = 1 if side == "l" else -1
    X = lambda x: x if m == 1 else 400 - x
    up = f'M{X(172)},222 C{X(150)},220 {X(140)},242 {X(143)},266 L{X(147)},292 L{X(167)},292 C{X(170)},268 {X(173)},246 {X(178)},232 Z'
    lo = f'M{X(146)},286 L{X(166)},286 L{X(164)},350 L{X(150)},350 Z'
    cuff = f'M{X(147)},342 L{X(166)},342 L{X(165)},358 L{X(148)},358 Z'
    glove = f'M{X(148)},356 L{X(165)},356 Q{X(168)},372 {X(162)},382 Q{X(156)},388 {X(150)},382 Q{X(145)},372 {X(148)},356 Z'
    return (f'<g id="back_arm_{side}"><g transform="rotate({8*m} {X(168)} 230)">'
            f'<path class="coat" d="{lo}"/><path class="coatsh" d="{cuff}"/><path class="glove" d="{glove}"/>'
            f'<path class="coat" d="{up}"/><path class="line" d="M{X(156)},236 Q{X(152)},256 {X(156)},280"/></g></g>')

BACK = f'''
<g id="characterBack" style="display:none">
  <ellipse class="groundshadow" cx="200" cy="772" rx="62" ry="7"/>
  <g id="back_legs">{back_leg("l")}{back_leg("r")}</g>
  <g id="back_coat">
    <path class="coat" d="M160,222 Q200,212 240,222 C250,330 258,470 262,612 L208,606 L200,556 L192,606 L138,612 C142,470 150,330 160,222 Z"/>
    <path class="shade" d="M160,222 C150,330 142,470 138,612 L152,611 C154,470 160,330 168,224 Z"/>
    <path class="line" d="M200,340 L200,556 M176,340 L174,600 M224,340 L226,600"/>
    <path class="leather" d="M162,318 L238,318 L238,330 L162,330 Z"/>
    <circle class="brass" cx="172" cy="324" r="3"/><circle class="brass" cx="228" cy="324" r="3"/>
  </g>
  {back_arm("l")}{back_arm("r")}
  <path class="coatsh" d="M174,214 Q200,206 226,214 L228,230 Q200,223 172,230 Z"/>
  <g id="back_pack" transform="translate(0 22)">
    <circle class="glowb" cx="232" cy="176" r="28"/>
    <rect class="vialglass" x="225" y="150" width="13" height="70" rx="5"/>
    <rect class="tube" x="227.5" y="166" width="8" height="50" rx="3"/>
    <rect class="cork" x="224" y="142" width="15" height="10" rx="2"/>
    <path class="pack" d="M156,214 Q156,204 166,204 L234,204 Q244,204 244,214 L244,332 Q244,342 234,342 L166,342 Q156,342 156,332 Z"/>
    <path class="packdark" d="M156,214 Q156,204 166,204 L234,204 Q244,204 244,214 L244,252 Q200,262 156,252 Z"/>
    <rect class="brass" x="174" y="248" width="10" height="12" rx="1"/><rect class="brass" x="216" y="248" width="10" height="12" rx="1"/>
    <rect class="leather" x="168" y="286" width="64" height="40" rx="4"/>
    <path class="line" d="M168,298 L232,298"/>
  </g>
  <g id="back_head">
    <rect class="skin" x="191" y="180" width="18" height="44"/>
    <path class="shade" d="M191,190 L209,190 L209,224 L191,224 Z"/>
    <circle class="skin" cx="152" cy="154" r="6.5"/><circle class="skin" cx="248" cy="154" r="6.5"/>
    <path class="skin" d="M156,130 C156,104 178,92 200,92 C222,92 244,104 244,130 L244,176 C232,194 168,194 156,176 Z"/>
    <path class="bhair" d="M148,116 C138,136 140,168 150,184 L160,176 L164,194 L174,182 L182,198 L192,184 L200,200 L208,184 L218,198 L226,182 L236,194 L240,176 L250,184 C260,168 262,136 252,116 Z"/>
    <path class="bhair" d="M150,124 L132,130 L148,138 L136,148 L154,146 Z"/>
    <path class="bhair" d="{mir('M150,124 L132,130 L148,138 L136,148 L154,146 Z')}"/>
    <path class="bhairline" d="M172,126 C168,150 170,170 174,182 M200,124 L200,196 M228,126 C232,150 230,170 226,182"/>
    <g id="b_back_cap">
      <path class="bcap" d="M140,116 C128,94 146,68 200,62 C254,68 272,94 260,116 Z"/>
      <path class="line" d="M200,64 L200,100 M168,70 Q176,84 178,98 M232,70 Q224,84 222,98"/>
      <path class="bcapband" d="M143,100 Q200,108 257,100 L258,117 Q200,125 142,117 Z"/>
      <path class="leather" d="M143,104 Q200,112 257,104 L257,112 Q200,120 143,112 Z"/>
      <rect class="buckle" x="194" y="105" width="12" height="9" rx="2"/>
    </g>
  </g>
</g>
'''

if __name__ == "__main__":
    from gen import ANIME_CSS, ANIME_DEFS
    import anime_dark
    for style, css in (("farbe", ANIME_CSS + BOY_CSS), ("scherenschnitt", anime_dark.css + BOY_DARK)):
        for name, body in (("front", FRONT), ("seite", SIDE), ("rueck", BACK)):
            body = body.replace('style="display:none"', '')
            bg = '#e9dcc8' if style == "farbe" else '#a8604e'
            open(f"lehrling_{name}_{style}.svg", "w").write(
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 800" width="400" height="800"><title>Lehrling – {name}</title>'
                f'<defs>{ANIME_DEFS}{BOY_DEFS}</defs><style>{css}</style><rect width="400" height="800" fill="{bg}"/>{body}</svg>')
    print("boy ok")
