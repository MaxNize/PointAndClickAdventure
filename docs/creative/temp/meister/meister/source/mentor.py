"""Meister (dritte Figur): starker Verbündeter in Messingrüstung.
Gleiches Rig/IDs wie Alchemistin und Lehrling -> gleiche Laufanimation."""
import re
from gen import scallop
import math
from boy import mir, girl_profile
def gear(cx, cy, r, n=8):
    pts = []
    for i in range(n*2):
        a = math.pi*i/n
        rr = r if i % 2 == 0 else r*0.72
        for da in (-0.18, 0.18):
            pts.append(f"{cx+rr*math.cos(a+da*(1 if i%2==0 else 1.4)):.1f},{cy+rr*math.sin(a+da*(1 if i%2==0 else 1.4)):.1f}")
    return "M" + " L".join(pts) + " Z"

def spike(x, y, ang, ln=22, w=9):
    a = math.radians(ang); px, py = math.cos(a+math.pi/2)*w/2, math.sin(a+math.pi/2)*w/2
    tx, ty = x+math.cos(a)*ln, y+math.sin(a)*ln
    return f"M{x-px:.1f},{y-py:.1f} L{tx:.1f},{ty:.1f} L{x+px:.1f},{y+py:.1f} Z"

def pauldron(cx, cy, side, scale=1.0):
    m = 1 if side == "l" else -1
    X = lambda dx: cx + dx*m*scale
    Y = lambda dy: cy + dy*scale
    s = f'<path class="armor" d="{spike(X(-6),Y(-16),-90-28*m,26*scale,10*scale)}"/>'
    s += f'<path class="armor" d="{spike(X(-22),Y(-6),-90-58*m,24*scale,10*scale)}"/>'
    s += f'<ellipse class="armor" cx="{cx}" cy="{cy}" rx="{34*scale}" ry="{27*scale}"/>'
    s += f'<path class="armorhl" d="M{X(-26)},{Y(-6)} Q{X(0)},{Y(-30)} {X(26)},{Y(-8)} Q{X(0)},{Y(-18)} {X(-26)},{Y(-6)} Z"/>'
    s += f'<path class="armordk" d="M{X(-34)},{Y(6)} Q{X(0)},{Y(30)} {X(34)},{Y(6)} L{X(32)},{Y(16)} Q{X(0)},{Y(40)} {X(-32)},{Y(16)} Z"/>'
    s += f'<path class="armor" d="M{X(-32)},{Y(18)} Q{X(0)},{Y(42)} {X(32)},{Y(18)} L{X(28)},{Y(28)} Q{X(0)},{Y(50)} {X(-28)},{Y(28)} Z"/>'
    s += f'<circle class="brass" cx="{X(-20)}" cy="{Y(4)}" r="{2.6*scale}"/><circle class="brass" cx="{X(0)}" cy="{Y(10)}" r="{2.6*scale}"/><circle class="brass" cx="{X(20)}" cy="{Y(4)}" r="{2.6*scale}"/>'
    return s


M_CSS = '''
.armor{fill:#b8873e}.armordk{fill:#7a5526}.armorhl{fill:#e3b866}.core{fill:#ffe066;stroke:#7a5526;stroke-width:2}
.tubep{fill:#c38bff}.redb{fill:#8e2a2a}.reddk{fill:#5e1a1c}.mcoat{fill:#2c2734}.mvest{fill:#8d8b93}
.mhair{fill:#cfc7d6}.mhairline{fill:none;stroke:#8e8598;stroke-width:1.3}.mhat{fill:#2b2a33}.mcoatt{fill:#2c2734}.mpants{fill:#25212b}
.lensr{fill:#ff7f9f;stroke:#3b2219;stroke-width:1.5}.glowy{fill:url(#glowYellow)}.glowp{fill:url(#glowPurple)}
.pin{fill:none;stroke:#4a4256;stroke-width:1.2}.trim{fill:none;stroke:#d9a84e;stroke-width:3}.pipe{fill:none;stroke:#c38bff;stroke-width:5;stroke-linecap:round}.pipecase{fill:none;stroke:#2a1a12;stroke-width:8.5;stroke-linecap:round}
.armor,.armordk,.armorhl,.redb,.reddk,.mcoat,.mcoatt,.mvest,.mhair,.mhat,.mpants{stroke:#2a1a12;stroke-width:2.2;stroke-linejoin:round}
'''
M_DARK = '''
.armor,.armordk,.armorhl,.redb,.reddk,.mcoat,.mvest,.mhair,.mhat,.mpants{fill:#140e10;stroke:#140e10;stroke-width:1.2}
.mcoatt{fill:#140e10;stroke:none;opacity:.8}
.armor{fill:#1f1418;stroke:#140e10;stroke-width:1.4}.armorhl{fill:#2a1c21;stroke:none}.armordk{fill:#140e10}
.redb,.reddk{fill:#26121a}.mhat{fill:#140e10}
.mhairline,.pin{display:none}.trim{stroke:#e0ad4a;stroke-width:1.6;opacity:.45}.pipecase{stroke:#140e10}.pipe{stroke:#c38bff}
.core{fill:#ffe066;stroke:none}.tubep{fill:#c38bff}.lensr{fill:#ff8fae;stroke:none}
.glowy{fill:url(#glowYellow)}.glowp{fill:url(#glowPurple)}
'''
# Selbstbewusster Gang: aufrecht (Brust raus), lange ruhige Schritte, weiter Armschwung, Schulterrollen
WALK_STYLE = {'hip': 23, 'knee': 34, 'arm': 24, 'fore': 8, 'lean': -1.5, 'swag': 1.4, 'lift': 11, 'bob': 4, 'sway': 3.4, 'armOut': 6, 'speed': 290}

M_DEFS = '''<radialGradient id="glowYellow"><stop offset="0" stop-color="#ffe680" stop-opacity=".85"/><stop offset="1" stop-color="#ffe680" stop-opacity="0"/></radialGradient>
<radialGradient id="glowPurple"><stop offset="0" stop-color="#d4a8ff" stop-opacity=".85"/><stop offset="1" stop-color="#d4a8ff" stop-opacity="0"/></radialGradient>'''

def tube(x, y, h=74):
    return (f'<circle class="glowp" cx="{x+6.5}" cy="{y+h*0.35}" r="26"/>'
            f'<rect class="vialglass" x="{x}" y="{y}" width="13" height="{h}" rx="6"/>'
            f'<rect class="tubep" x="{x+2.5}" y="{y+8}" width="8" height="{h-14}" rx="4"/>'
            f'<rect class="armordk" x="{x-2}" y="{y+h-6}" width="17" height="10" rx="2"/>')

def eye(cx, side):
    m = 1 if side == "l" else -1
    X = lambda dx: cx + dx * m
    white = f"M{X(-12)},156 Q{X(0)},148 {X(11)},153 Q{X(10)},163 {X(0)},164.5 Q{X(-11)},163.5 {X(-12)},156 Z"
    return f'''<g id="m_eye_{side}">
      <clipPath id="mclip_{side}"><path d="{white}"/></clipPath>
      <path class="eyewhite" d="{white}"/>
      <g clip-path="url(#mclip_{side})">
        <ellipse class="iris" cx="{X(-0.5)}" cy="157" rx="5.8" ry="7"/>
        <ellipse class="pupil" cx="{X(-0.5)}" cy="157" rx="2.4" ry="3.6"/>
        <path class="irisshadow" d="M{cx-15},145 L{cx+15},145 L{cx+15},154 Q{cx},150 {cx-15},154 Z"/>
      </g>
      <circle class="hl" cx="{X(2.5)}" cy="154.5" r="1.8"/>
      <path class="lash" d="M{X(-13)},156 Q{X(-1)},147 {X(12)},152.5"/>
      <path class="brow2" d="M{X(-14)},144 Q{X(-1)},137 {X(12)},139 L{X(12)},142.5 Q{X(-1)},141 {X(-14)},147.5 Z"/>
    </g>'''

# ------------------------------------------------------------------ FRONT
def front_leg(side):
    d = 'M141,350 C135,420 137,500 143,556 C141,620 143,680 147,730 L188,730 C189,680 190,620 188,556 C192,500 193,420 192,350 Z'
    s = f'<path class="mpants" d="{d if side=="l" else mir(d)}"/>'
    sh = 'M182,350 C186,420 185,500 181,556 C183,620 182,680 182,730 L188,730 C189,680 190,620 188,556 C192,500 193,420 192,350 Z'
    s += f'<path class="shade" d="{sh if side=="l" else mir(sh)}"/>'
    kp = 'M143,536 Q166,522 189,536 L188,566 Q166,578 144,566 Z'
    s += f'<path class="armor" d="{kp if side=="l" else mir(kp)}"/>'
    return s

def front_boot(side):
    d = 'M143,714 L191,714 L192,756 Q194,773 175,773 L153,773 Q138,773 141,756 Z'
    s = f'<path class="boot" d="{d if side=="l" else mir(d)}"/>'
    c = 'M141,748 Q167,736 193,748 L193,773 L141,773 Z'
    s += f'<path class="armor" d="{c if side=="l" else mir(c)}"/>'
    b = 'M140,764 L194,764 L193,773 L141,773 Z'
    s += f'<path class="bootdark" d="{b if side=="l" else mir(b)}"/>'
    return s

HAT_FRONT = f'''
    <g id="m_hat" transform="translate(0 -12)">
      <path class="brass" d="M152,92 L122,66" fill="none" stroke-width="4"/>
      <circle class="brass" cx="118" cy="62" r="10"/><circle class="lensr" cx="118" cy="62" r="6"/>
      <path class="mhat" d="M146,114 C142,72 158,38 204,32 C244,36 258,72 254,114 Q200,122 146,114 Z"/>
      <path class="cel" d="M146,114 C145,100 147,90 150,82 Q200,102 252,82 C255,90 256,100 254,114 Q200,122 146,114 Z"/>
      <path class="line" d="M176,44 Q170,74 172,100 M226,42 Q232,74 230,100"/>
      <path class="redb" d="M147,92 Q200,102 253,92 L254,110 Q200,120 146,110 Z"/>
      <path class="brass" d="M147,92 Q200,102 253,92 L253,97 Q200,107 147,97 Z"/>
      <path class="mhat" d="M88,126 Q150,112 200,110 Q258,108 296,86 Q318,92 308,114 Q258,144 200,146 Q116,146 88,126 Z"/>
      <path class="redb" d="M96,132 Q200,150 300,118 Q304,126 290,132 Q250,150 200,152 Q112,150 96,132 Z"/>
      <path class="trim" d="M88,126 Q150,112 200,110 Q258,108 296,86"/>
      <path class="armor" d="{gear(250, 96, 17, 9)}"/><circle class="armordk" cx="250" cy="96" r="6"/><circle class="core" cx="250" cy="96" r="3"/>
      <circle class="brass" cx="178" cy="78" r="13"/><circle class="lensr" cx="178" cy="78" r="9"/>
      <circle class="brass" cx="214" cy="76" r="13"/><circle class="lensr" cx="214" cy="76" r="9"/>
      <rect class="brass" x="189" y="74" width="14" height="5" rx="2"/>
      <path class="lensshine" d="M172,74 L178,70 L181,73 L175,77 Z M208,72 L214,68 L217,71 L211,75 Z"/>
      <circle class="brass" cx="160" cy="104" r="2.4"/><circle class="brass" cx="200" cy="108" r="2.4"/><circle class="brass" cx="232" cy="104" r="2.4"/>
    </g>'''

FRONT_HEAD = f'''
  <g id="head">
    <path class="mhair" d="M149,118 C141,132 141,150 145,163 L151,155 L154,167 L160,150 L162,124 Z"/>
    <path class="mhair" d="{mir('M149,118 C141,132 141,150 145,163 L151,155 L154,167 L160,150 L162,124 Z')}"/>
    <circle class="skin" cx="151" cy="155" r="6.5"/><circle class="skin" cx="249" cy="155" r="6.5"/>
    <path class="skin" d="M152,124 C151,160 163,184 189,196 Q200,200 211,196 C237,184 249,160 248,124 Q200,114 152,124 Z"/>
    <path class="cel" d="M153,140 L160,142 L168,152 L177,139 L186,155 L195,140 L203,160 L211,142 L219,167 L226,146 L234,178 L240,150 L247,174 L248,124 Q200,114 152,124 Z"/>
    {eye(180, "l")}{eye(220, "r")}
    <path class="nose" d="M200.5,171 l-1.8,2.6"/>
    <path class="mouthline" d="M191,180 Q200,188 209,180"/>
    <path class="line" d="M190,179 L192,181 M210,179 L208,181"/>
    <path class="mhair" d="M146,140 Q146,104 200,98 Q256,104 254,142 L251,148 L247,170 L240,146 L234,174 L226,142 L219,163 L211,138 L203,156 L195,136 L186,151 L177,135 L168,148 L158,136 Z"/>
    <path class="mhairline" d="M234,170 Q230,136 214,110 M226,142 Q220,122 206,108 M247,166 Q246,134 236,112 M195,136 Q190,120 182,110"/>
    {HAT_FRONT}
  </g>'''

FRONT = f'''
<g id="character">
  <ellipse class="groundshadow" cx="200" cy="772" rx="88" ry="8"/>
  <g id="m_pack_front">
    {tube(122, 146)}{tube(265, 140)}
    <rect class="armordk" x="126" y="206" width="148" height="150" rx="16"/>
  </g>
  <path class="mcoatt" d="M156,330 L244,330 L262,616 L138,616 Z"/>
  <path class="pin" d="M170,340 L162,612 M186,340 L182,612 M214,340 L218,612 M230,340 L238,612"/>
  <g id="front_leg_l">{front_leg("l")}</g><g id="front_leg_r">{front_leg("r")}</g>
  <g id="boot_l">{front_boot("l")}</g><g id="boot_r">{front_boot("r")}</g>
  <g id="m_coat_front">
    <path class="mcoatt" d="M150,300 L136,330 C132,420 132,520 128,616 L170,608 L180,340 Z"/>
    <path class="mcoatt" d="{mir('M150,300 L136,330 C132,420 132,520 128,616 L170,608 L180,340 Z')}"/>
    <path class="pin" d="M146,340 L140,610 M160,336 L156,608 M254,340 L260,610 M240,336 L244,608"/>
  </g>
  <g id="m_torso">
    <rect class="skin" x="186" y="184" width="28" height="32"/>
    <path class="mvest" d="M146,226 Q200,214 254,226 L256,334 L144,334 Z"/>
    <circle class="glowy" cx="200" cy="268" r="52"/>
    <path class="armor" d="M134,214 Q200,194 266,214 L270,282 Q244,324 200,330 Q156,324 130,282 Z"/>
    <path class="armorhl" d="M148,220 Q200,206 252,220 L252,232 Q200,220 148,232 Z"/>
    <path class="line" d="M200,232 L200,250 M154,240 Q170,272 160,300 M246,240 Q230,272 240,300"/>
    <path class="armordk" d="M130,282 Q156,324 200,330 Q244,324 270,282 L268,298 Q242,338 200,344 Q158,338 132,298 Z"/>
    <path class="armor" d="M144,300 Q170,332 200,336 Q230,332 256,300 L250,316 Q228,346 200,350 Q172,346 150,316 Z"/>
    <circle class="armordk" cx="200" cy="268" r="20"/><circle class="core" cx="200" cy="268" r="14"/>
        <circle class="armordk" cx="180" cy="306" r="8"/><circle class="core" cx="180" cy="306" r="5"/>
    <circle class="armordk" cx="220" cy="306" r="8"/><circle class="core" cx="220" cy="306" r="5"/>
    <circle class="brass" cx="146" cy="236" r="2.6"/><circle class="brass" cx="254" cy="236" r="2.6"/>
    <circle class="brass" cx="142" cy="272" r="2.6"/><circle class="brass" cx="258" cy="272" r="2.6"/>
    <path class="armor" d="M168,188 L232,188 L240,226 Q200,234 160,226 Z"/>
    <path class="armordk" d="M176,198 L224,198 L225,204 L175,204 Z M174,210 L226,210 L227,216 L173,216 Z"/>
  </g>
  <g id="m_belt">
    <path class="redb" d="M140,320 Q200,336 260,320 L260,340 Q200,356 140,340 Z"/>
    <path class="brass" d="M186,330 Q200,322 214,330 L214,348 Q200,354 186,348 Z"/>
    <path class="armorhl" d="M214,334 Q234,322 252,330 Q236,336 216,344 Z"/><path class="armorhl" d="M186,334 Q166,322 148,330 Q164,336 184,344 Z"/>
    <rect class="redb" x="140" y="338" width="22" height="34" rx="3"/><path class="reddk" d="M140,338 L162,338 L162,348 L140,348 Z"/>
    <rect class="redb" x="168" y="346" width="16" height="30" rx="3"/><rect class="redb" x="216" y="346" width="16" height="30" rx="3"/>
    <circle class="brass" cx="151" cy="356" r="2.5"/>
  </g>
  <g id="arm_l">
    <path class="mcoat" d="M144,228 C120,232 110,258 110,288 L108,314 L144,318 L148,288 Z"/>
    <path class="armor" d="M102,298 L148,302 L146,378 L108,376 Z"/>
    <path class="armorhl" d="M106,304 L144,307 L144,316 L106,313 Z"/>
    <path class="armordk" d="M104,342 L147,345 L147,353 L104,350 Z"/>
    <path class="armor" d="M104,372 L150,374 Q156,398 144,412 Q128,420 114,410 Q100,396 104,372 Z"/>
    <path class="armor" d="{spike(110,384,-150,14,7)} {spike(108,398,-165,14,7)}"/>
    <path class="line" d="M116,392 L116,410 M127,394 L127,414 M138,392 L138,410"/>
    <circle class="armordk" cx="125" cy="326" r="8"/><circle class="core" cx="125" cy="326" r="5"/>
    <path class="pipecase" d="M142,216 C120,236 112,276 118,318"/><path class="pipe" d="M142,216 C120,236 112,276 118,318"/>
    {pauldron(136, 232, "l")}
  </g>
  <g id="arm_r">
    <path class="mcoat" d="M256,228 C280,232 290,258 288,286 L286,306 L256,306 L254,264 Z"/>
    <path class="mcoat" d="M258,290 L290,296 L256,344 L234,332 Z"/>
    <path class="armor" d="M238,322 Q226,318 221,330 Q221,344 233,346 Q247,346 252,336 Z"/>
    {pauldron(264, 232, "r")}
  </g>
  {FRONT_HEAD}
</g>
'''

# ------------------------------------------------------------------ SEITE
def side_leg(gid, far=False):
    thigh = 'M170,352 C164,430 176,500 188,552 L225,554 C232,500 242,430 240,352 Z'
    shin = 'M189,546 C178,600 184,680 188,722 L224,722 C228,690 232,620 225,553 Z'
    boot = 'M183,708 L228,708 L228,732 L258,742 Q268,754 260,768 L190,768 L183,760 Z'
    s = f'<g id="{gid}"><path class="mpants" d="{thigh}"/>'
    s += '<path class="shade" d="M170,352 C164,430 176,500 188,552 L196,552 C186,500 178,430 182,352 Z"/>'
    if far: s += f'<path class="shade" d="{thigh}"/>'
    s += f'<g id="{gid}_shin"><circle class="mpants" cx="206" cy="550" r="18"/><path class="mpants" d="{shin}"/>'
    s += '<path class="armor" d="M198,530 Q222,522 234,540 L231,570 Q216,580 200,570 Z"/><path class="armor" d="{spike(233,548,-10,15,8)}"/>'
    s += f'<path class="boot" d="{boot}"/><path class="armor" d="M228,732 L258,742 Q268,754 260,768 L236,768 Q238,748 228,740 Z"/>'
    s += '<path class="bootdark" d="M186,762 L262,762 L260,768 L190,768 Z"/>'
    if far: s += f'<circle class="shade" cx="206" cy="550" r="18"/><path class="shade" d="{shin}"/><path class="shade" d="{boot}"/>'
    return s + '</g></g>'

def side_arm(gid, far=False, gauntlet=False):
    upper = 'M178,226 C160,246 164,282 186,300 L228,300 C246,282 246,244 226,226 Z'
    lower = 'M185,286 L226,286 L222,362 L190,362 Z'
    s = f'<g id="{gid}"><g id="{gid}_fore">'
    if gauntlet:
        s += '<path class="armor" d="M180,284 L231,284 L227,372 L184,372 Z"/>'
        s += '<path class="armordk" d="M185,322 L225,322 L225,331 L185,331 Z"/><circle class="armordk" cx="205" cy="304" r="7"/><circle class="core" cx="205" cy="304" r="4.5"/>'
        s += '<path class="armor" d="M183,368 L228,368 Q235,394 221,409 Q205,418 192,408 Q178,394 183,368 Z"/>'
        s += f'<path class="armor" d="{spike(222,378,-10,14,7)} {spike(223,392,5,14,7)}"/>'
    else:
        s += f'<path class="mcoat" d="{lower}"/>'
        s += '<path class="armor" d="M190,358 L220,358 Q224,380 214,392 Q204,398 196,392 Q187,380 190,358 Z"/>'
    if far: s += f'<path class="shade" d="{lower}"/><path class="shade" d="M186,358 L224,358 L224,406 L186,406 Z"/>'
    s += f'</g><path class="mcoat" d="{upper}"/>'
    if gauntlet:
        s += '<path class="pipecase" d="M170,236 C186,256 196,272 200,292"/><path class="pipe" d="M170,236 C186,256 196,272 200,292"/>'
    s += f'<path class="armor" d="{spike(224,226,-48,26,11)}"/><path class="armor" d="{spike(212,218,-75,24,10)}"/><path class="armor" d="{spike(178,232,-150,22,9)}"/>'
    s += '<ellipse class="armor" cx="203" cy="238" rx="35" ry="28"/><path class="armorhl" d="M179,232 Q203,212 227,230 Q203,221 179,232 Z"/>'
    s += '<path class="armordk" d="M174,246 Q203,268 232,246 L230,257 Q203,278 176,257 Z"/>'
    s += '<path class="armor" d="M176,258 Q203,280 230,258 L226,268 Q203,288 180,268 Z"/>'
    s += '<circle class="brass" cx="190" cy="244" r="2.4"/><circle class="brass" cx="216" cy="244" r="2.4"/>'
    if far: s += f'<path class="shade" d="{upper}"/><ellipse class="shade" cx="203" cy="238" rx="30" ry="25"/>'
    return s + '</g>'

SIDE = f'''
<g id="characterSide" style="display:none">
  <ellipse class="groundshadow" cx="208" cy="772" rx="56" ry="7"/>
  <path class="mcoatt" d="M166,330 L210,330 C208,420 206,520 204,616 L126,606 C140,520 152,420 166,330 Z"/>
  <path class="pin" d="M186,340 L172,608 M198,340 L190,610"/>
  {side_arm("side_arm_far", far=True)}
  {side_leg("side_leg_far", far=True)}
  <path class="mcoatt" d="M212,340 L246,340 C250,420 252,500 254,582 L224,586 C222,500 218,420 212,340 Z"/>
  <path class="shade" d="M212,340 L246,340 C250,420 252,500 254,582 L224,586 C222,500 218,420 212,340 Z"/>
  {side_leg("side_leg_near")}
  <g id="side_torso">
    <rect class="skin" x="192" y="182" width="26" height="42"/>
    <path class="mvest" d="M166,222 C152,246 152,294 160,346 L248,346 C254,300 252,250 242,232 Q222,218 205,216 Z"/>
    <circle class="glowy" cx="258" cy="272" r="46"/>
    <path class="armor" d="M164,210 C148,236 148,280 162,314 Q214,340 262,306 C274,272 268,230 250,212 Q210,198 164,210 Z"/>
    <path class="armorhl" d="M184,216 Q212,206 238,220 L238,230 Q212,220 184,226 Z"/>
    <path class="armordk" d="M162,314 Q214,340 262,306 L260,320 Q214,352 164,328 Z"/>
    <path class="line" d="M190,236 Q184,270 192,300 M226,232 Q232,262 228,296"/>
    <ellipse class="armordk" cx="260" cy="268" rx="9" ry="16"/><ellipse class="core" cx="262" cy="268" rx="5.5" ry="11.5"/>
    <ellipse class="armordk" cx="252" cy="308" rx="5" ry="8"/><ellipse class="core" cx="253" cy="308" rx="3" ry="5.5"/>
    <path class="armor" d="M186,188 L230,188 L240,226 L180,226 Z"/>
    <path class="armordk" d="M192,198 L230,198 L231,204 L191,204 Z M190,210 L234,210 L235,216 L189,216 Z"/>
    <path class="redb" d="M158,318 L254,318 L254,342 L158,342 Z"/><rect class="brass" x="240" y="322" width="13" height="17" rx="2"/>
    <rect class="redb" x="152" y="338" width="22" height="36" rx="3"/>
  </g>
  <g id="side_pack">
    {tube(116, 136)}{tube(142, 124, 86)}
    <path class="armordk" d="M128,208 Q110,208 110,226 L110,350 Q110,368 128,368 L176,368 L178,208 Z"/>
    <path class="armor" d="M110,238 L178,238 L178,252 L110,252 Z"/><path class="armor" d="M110,322 L178,322 L178,336 L110,336 Z"/>
    <circle class="brass" cx="132" cy="288" r="10"/><circle class="lensr" cx="132" cy="288" r="5"/>
  </g>
  {side_arm("side_arm_near", gauntlet=True)}
  <g id="side_head">
    
    <path class="skin" d="{girl_profile()}"/>
    <path class="mhair" d="M157,118 C147,138 146,160 150,178 L157,170 L160,184 L168,172 L174,186 L181,174 L186,182 L190,168 C186,156 188,144 196,134 C202,127 208,123 216,120 Z"/>
    <path class="mhairline" d="M168,130 C162,146 162,162 166,176 M180,128 C175,142 175,158 178,172"/>
    <path class="skin" d="M199.5,181 C195,183.5 189,180.5 186,176 C183,171 182.2,165 182.6,161 C183.2,157 185.5,154.4 188,154.2 C190.6,154 192.6,155.6 193.6,157.8 C195.5,162 197.5,168 199,173 Z"/>
    <path class="line" d="M187.5,159.5 Q185.2,166.5 189.5,173.5"/>
    <g id="m_side_eye">
      <ellipse class="iris" cx="231.2" cy="152.4" rx="3" ry="7"/>
      <ellipse class="pupil" cx="231.1" cy="153.4" rx="1.4" ry="3.2"/>
      <circle class="hl" cx="231.8" cy="148.6" r="1.4"/>
      <ellipse class="lowlash" cx="231.2" cy="152.4" rx="3" ry="7"/>
      <path class="lash" d="M236.4,142.6 Q229,139.4 224.8,143.4 Q221,147.6 219,154"/>
      <path class="brow2" d="M225,140 Q232,133.5 242,133.5 L241.5,137 Q232,137 225,142.5 Z"/>
    </g>
    <path class="mouthline" d="M249,179.6 Q245,182 241,180.4"/>
    <path class="mhair" d="M198,112 C224,106 248,112 257,128 L263,152 L253,141 L252,162 L243,138 L237,153 L229,130 L221,142 L213,124 L204,134 Z"/>
    <path class="mhair" d="M204,134 L207,156 L211,146 L214,160 L216,136 Z"/>
    <g id="m_side_hat">
      <path class="mhat" d="M150,114 C144,72 168,36 214,32 C248,36 262,76 256,114 Z"/>
      <path class="line" d="M190,40 Q182,74 184,104"/>
      <path class="redb" d="M150,94 Q204,102 257,94 L257,112 Q204,120 150,112 Z"/>
      <path class="brass" d="M150,94 Q204,102 257,94 L257,99 Q204,107 150,99 Z"/>
      <path class="mhat" d="M84,96 Q96,88 112,104 Q160,118 210,118 Q270,118 318,114 Q322,124 300,130 Q220,136 150,132 Q100,128 84,96 Z"/>
      <path class="redb" d="M110,126 Q200,136 306,126 Q300,132 220,138 Q150,138 110,126 Z"/>
      <path class="trim" d="M84,96 Q96,88 112,104 Q160,118 210,118 Q270,118 318,114"/>
      <path class="armor" d="{gear(168, 102, 16, 9)}"/><circle class="armordk" cx="168" cy="102" r="5.5"/><circle class="core" cx="168" cy="102" r="2.8"/>
      <circle class="brass" cx="234" cy="80" r="13"/><ellipse class="lensr" cx="236" cy="80" rx="6" ry="9"/>
      <circle class="brass" cx="214" cy="76" r="11"/><ellipse class="lensr" cx="215" cy="76" rx="4.5" ry="7"/>
      <path class="brass" d="M246,86 L274,70" fill="none" stroke-width="4"/>
      <circle class="brass" cx="278" cy="67" r="9"/><ellipse class="lensr" cx="279" cy="67" rx="4" ry="6"/>
    </g>
  </g>
</g>
'''

# ------------------------------------------------------------------ RÜCKEN
def back_leg(side):
    s = front_leg(side) + front_boot(side)
    return f'<g id="back_leg_{side}">{s}</g>'

def back_arm(side):
    m = 1 if side == "l" else -1
    X = lambda x: x if m == 1 else 400 - x
    up = f'M{X(156)},226 C{X(128)},226 {X(116)},252 {X(118)},280 L{X(120)},304 L{X(154)},304 C{X(156)},276 {X(160)},252 {X(166)},236 Z'
    lo = f'M{X(114)},298 L{X(156)},300 L{X(154)},370 L{X(120)},368 Z'
    hand = f'M{X(116)},366 L{X(156)},368 Q{X(160)},390 {X(150)},404 Q{X(136)},412 {X(124)},404 Q{X(112)},390 {X(116)},366 Z'
    return (f'<g id="back_arm_{side}"><g transform="rotate({8*m} {X(168)} 230)">'
            f'<path class="armor" d="{lo}"/><path class="armordk" d="M{X(115)},332 L{X(156)},334 L{X(156)},342 L{X(115)},340 Z"/>'
            f'<path class="armor" d="{hand}"/><path class="mcoat" d="{up}"/>'
            f'{pauldron(X(140), 232, side)}</g></g>')

BACK = f'''
<g id="characterBack" style="display:none">
  <ellipse class="groundshadow" cx="200" cy="772" rx="86" ry="8"/>
  <g id="back_legs">{back_leg("l")}{back_leg("r")}</g>
  <g id="back_coat">
    <path class="mcoatt" d="M146,222 Q200,210 254,222 C264,330 270,470 274,616 L210,610 L200,560 L190,610 L126,616 C130,470 136,330 146,222 Z"/>
    <path class="pin" d="M168,330 L160,610 M184,330 L180,606 M216,330 L220,606 M232,330 L240,610 M200,330 L200,560"/>
    <path class="redb" d="M146,318 L254,318 L254,338 L146,338 Z"/>
    <rect class="redb" x="150" y="336" width="20" height="32" rx="3"/><rect class="redb" x="230" y="336" width="20" height="32" rx="3"/>
  </g>
  {back_arm("l")}{back_arm("r")}
  <path class="armor" d="M168,190 L232,190 L240,226 Q200,234 160,226 Z"/>
  <g id="back_pack" transform="translate(0 18)">
    {tube(134, 128, 86)}{tube(253, 128, 86)}
    <path class="armordk" d="M144,216 Q144,200 160,200 L240,200 Q256,200 256,216 L256,340 Q256,356 240,356 L160,356 Q144,356 144,340 Z"/>
    <path class="armor" d="M144,232 L256,232 L256,246 L144,246 Z"/>
    <path class="armor" d="M144,310 L256,310 L256,324 L144,324 Z"/>
    <circle class="armor" cx="200" cy="278" r="22"/><circle class="brass" cx="200" cy="278" r="13"/><circle class="lensr" cx="200" cy="278" r="7"/>
    <circle class="brass" cx="156" cy="216" r="3"/><circle class="brass" cx="244" cy="216" r="3"/>
  </g>
  <g id="back_head">
    <rect class="skin" x="186" y="180" width="28" height="40"/>
    <circle class="skin" cx="151" cy="154" r="6.5"/><circle class="skin" cx="249" cy="154" r="6.5"/>
    <path class="skin" d="M156,130 C156,104 178,92 200,92 C222,92 244,104 244,130 L244,176 C232,194 168,194 156,176 Z"/>
    <path class="mhair" d="M146,116 C138,134 140,158 148,176 L156,168 L160,182 L168,172 L176,186 L184,174 L192,186 L200,176 L208,186 L216,174 L224,186 L232,172 L240,182 L244,168 L252,176 C260,158 262,134 254,116 Z"/>
    <path class="mhairline" d="M172,126 C168,146 170,162 174,176 M200,124 L200,176 M228,126 C232,146 230,162 226,176"/>
    <g id="m_back_hat">
      <path class="brass" d="M248,92 L278,66" fill="none" stroke-width="4"/>
      <circle class="brass" cx="282" cy="62" r="10"/><circle class="armordk" cx="282" cy="62" r="6"/>
      <path class="mhat" d="M146,114 C142,72 156,38 196,32 C242,36 258,72 254,114 Q200,122 146,114 Z"/>
      <path class="line" d="M224,42 Q230,74 228,104"/>
      <path class="redb" d="M147,92 Q200,102 253,92 L254,110 Q200,120 146,110 Z"/>
      <path class="brass" d="M147,92 Q200,102 253,92 L253,97 Q200,107 147,97 Z"/>
      <path class="mhat" d="M312,126 Q250,112 200,110 Q142,108 104,86 Q82,92 92,114 Q142,144 200,146 Q284,146 312,126 Z"/>
      <path class="trim" d="M312,126 Q250,112 200,110 Q142,108 104,86"/>
      <path class="armor" d="{gear(150, 96, 17, 9)}"/><circle class="armordk" cx="150" cy="96" r="6"/><circle class="core" cx="150" cy="96" r="3"/>
      <rect class="buckle" x="193" y="98" width="14" height="10" rx="2"/>
    </g>
  </g>
</g>
'''

if __name__ == "__main__":
    from gen import ANIME_CSS, ANIME_DEFS
    import anime_dark
    for style, css in (("farbe", ANIME_CSS + M_CSS), ("scherenschnitt", anime_dark.css + M_DARK)):
        for name, body in (("front", FRONT), ("seite", SIDE), ("rueck", BACK)):
            body = body.replace('style="display:none"', '')
            bg = '#e9dcc8' if style == "farbe" else '#a8604e'
            open(f"meister_{name}_{style}.svg", "w").write(
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 800" width="400" height="800"><title>Meister – {name}</title>'
                f'<defs>{ANIME_DEFS}{M_DEFS}</defs><style>{css}</style><rect width="400" height="800" fill="{bg}"/>{body}</svg>')
    print("meister ok")
