"""Erzalchemist (vierte Figur): greiser, weiser Alchemist mit Stab.
Gleiches Rig/IDs wie die anderen Figuren -> gleiche Laufanimation, eigener (langsamer, gebeugter) Laufstil."""
import math
from gen import scallop
from boy import mir, girl_profile

E_CSS = '''
.erobe{fill:#2f3b66}.erobet{fill:#2f3b66}.elin{fill:#6a2f3a}.etunic{fill:#d8cba6}.estole{fill:#c0913f}
.ebeard{fill:#eeeae2}.ebeardsh{fill:#d3cbbf}.ehat{fill:#2f3b66}.ewood{fill:#6b4a2e}.epants{fill:#3a3340}
.eorb{fill:#ffb35a}.glowo{fill:url(#glowOrange)}.especs{fill:none;stroke:#c99846;stroke-width:2.2}.eglass{fill:#e8f4f4;opacity:.35}
.esym{fill:none;stroke:#7a4f1c;stroke-width:1.5}.wrinkle{fill:none;stroke:#c08f7a;stroke-width:1.1}.ebeardline{fill:none;stroke:#b8afa2;stroke-width:1.2}
.erobe,.erobet,.elin,.etunic,.estole,.ebeard,.ehat,.ewood,.epants{stroke:#2a1a12;stroke-width:2.2;stroke-linejoin:round}
'''
E_DARK = '''
.erobe,.elin,.etunic,.ehat,.ewood,.epants{fill:#140e10;stroke:#140e10;stroke-width:1.2}
.erobet{fill:#140e10;stroke:none;opacity:.8}
.ebeard{fill:#221a1e;stroke:#140e10;stroke-width:1.2}.ebeardsh{fill:#1a1316}
.estole{fill:#26121a;stroke:#140e10;stroke-width:1.2}
.esym{stroke:#e0ad4a;stroke-width:1.3;opacity:.5}.especs{stroke:#ffb35a;stroke-width:1.8}.eglass{display:none}
.eorb{fill:#ffb35a}.glowo{fill:url(#glowOrange)}
.wrinkle,.ebeardline{display:none}
'''
E_DEFS = '''<radialGradient id="glowOrange"><stop offset="0" stop-color="#ffc070" stop-opacity=".9"/><stop offset="1" stop-color="#ff9a40" stop-opacity="0"/></radialGradient>'''

# Gebrechlich: kurze, vorsichtige Schritte, kaum Armschwung, nach vorn gebeugt, langsam
WALK_STYLE = {'hip': 12, 'knee': 26, 'arm': 5, 'fore': 4, 'lean': 6, 'swag': 0.6, 'lift': 7, 'bob': 2.5, 'sway': 1.2, 'armOut': 2, 'speed': 190}

def staff(x, top, bottom=772):
    """Holzstab mit Messingkäfig und glühendem Kern; x = Mitte."""
    s = f'<circle class="glowo" cx="{x}" cy="{top+20}" r="44"/>'
    s += f'<rect class="ewood" x="{x-4.5}" y="{top+30}" width="9" height="{bottom-top-30}" rx="3"/>'
    for y in (top+40, top+120, bottom-60):
        s += f'<rect class="brass" x="{x-6.5}" y="{y}" width="13" height="6" rx="2"/>'
    s += f'<circle class="eorb" cx="{x}" cy="{top+20}" r="11"/>'
    s += (f'<path class="brass" d="M{x-14},{top+34} Q{x-20},{top+16} {x-6},{top+2} M{x+14},{top+34} Q{x+20},{top+16} {x+6},{top+2} '
          f'M{x},{top+36} L{x},{top+31} M{x-9},{top+36} Q{x-4},{top+24} {x-2},{top+8} M{x+9},{top+36} Q{x+4},{top+24} {x+2},{top+8}" fill="none" stroke-width="3"/>')
    s += f'<rect class="brass" x="{x-10}" y="{top+32}" width="20" height="7" rx="2"/>'
    s += f'<path class="brass" d="M{x-6},{top+2} Q{x},{top-8} {x+6},{top+2}" fill="none" stroke-width="3"/>'
    return s

def symbols(x, y0, n=3):
    s = ''
    for i in range(n):
        y = y0 + i*48
        if i % 3 == 0: s += f'<circle class="esym" cx="{x}" cy="{y}" r="5"/><circle class="esym" cx="{x}" cy="{y}" r="1"/>'
        elif i % 3 == 1: s += f'<path class="esym" d="M{x},{y-6} L{x+6},{y+5} L{x-6},{y+5} Z"/>'
        else: s += f'<path class="esym" d="M{x},{y-6} L{x+6},{y+5} L{x-6},{y+5} Z M{x-6},{y+1} L{x+6},{y+1}"/>'
    return s

def eye(cx, side):
    m = 1 if side == "l" else -1
    X = lambda dx: cx + dx * m
    white = f"M{X(-10)},159 Q{X(0)},154 {X(10)},158 Q{X(9)},163 {X(0)},164 Q{X(-9)},163 {X(-10)},159 Z"
    return f'''<g id="e_eye_{side}">
      <clipPath id="eclip_{side}"><path d="{white}"/></clipPath>
      <path class="eyewhite" d="{white}"/>
      <g clip-path="url(#eclip_{side})"><ellipse class="iris" cx="{X(-0.5)}" cy="160" rx="4.6" ry="5.6"/>
        <ellipse class="pupil" cx="{X(-0.5)}" cy="160" rx="2" ry="2.8"/></g>
      <circle class="hl" cx="{X(1.6)}" cy="158.4" r="1.3"/>
      <path class="lash" d="M{X(-11)},159 Q{X(0)},152.5 {X(11)},157.5"/>
      <path class="wrinkle" d="M{X(-9)},166 Q{X(0)},168.5 {X(9)},165.5 M{X(13)},156 l{3*m},-2 M{X(13)},160 l{4*m},0 M{X(13)},164 l{3*m},2"/>
      <path class="ebeard" d="M{X(-16)},148 Q{X(-3)},139 {X(15)},145 L{X(18)},151 Q{X(1)},145 {X(-14)},153 Z"/>
      <circle class="eglass" cx="{X(0)}" cy="159" r="11"/><circle class="especs" cx="{X(0)}" cy="159" r="11"/>
    </g>'''

# ------------------------------------------------------------------ FRONT
def front_leg(side):
    d = 'M168,360 C165,440 167,540 170,600 C170,650 172,700 174,734 L196,734 C197,700 198,650 197,600 C199,540 200,440 200,360 Z'
    return f'<path class="epants" d="{d if side=="l" else mir(d)}"/>'

def front_boot(side):
    d = 'M168,724 L198,724 L199,760 Q200,773 186,773 L170,773 Q158,771 164,758 Z'
    b = 'M162,766 L200,766 L199,773 L166,773 Z'
    return f'<path class="boot" d="{d if side=="l" else mir(d)}"/><path class="bootdark" d="{b if side=="l" else mir(b)}"/>'

HAT_FRONT = '''
    <g id="e_hat">
      <path class="ehat" d="M146,118 C150,84 174,40 212,14 Q232,2 250,12 Q266,22 266,46 Q256,32 242,32 C236,56 244,90 254,118 Z"/>
      <path class="cel" d="M146,118 C147,108 149,100 152,94 Q200,110 250,92 C252,100 253,108 254,118 Z"/>
      <path class="line" d="M186,40 Q178,74 180,104"/>
      <path class="brass" d="M266,46 L266,58" fill="none" stroke-width="2"/><circle class="brass" cx="266" cy="62" r="5"/>
      <path class="ehat" d="M126,120 Q200,102 274,120 Q278,131 200,137 Q122,131 126,120 Z"/>
      <path class="brass" d="M148,104 Q200,96 252,104 L253,116 Q200,108 147,116 Z"/>
      <circle class="esym" cx="214" cy="60" r="6"/><circle class="esym" cx="214" cy="60" r="1.2"/>
      <path class="esym" d="M182,78 L189,90 L175,90 Z M228,84 L234,94 L222,94 Z M222,90 L234,90"/>
      <circle class="brass" cx="170" cy="104" r="13"/><circle class="eorb" cx="170" cy="104" r="8"/>
      <path class="lensshine" d="M165,100 L170,96 L173,99 L168,103 Z"/>
      <circle class="brass" cx="196" cy="108" r="4"/>
    </g>'''

FRONT_HEAD = f'''
  <g id="head" transform="translate(0 8)">
    <path class="ebeard" d="M150,118 C132,160 134,220 144,262 L158,246 L162,264 L170,206 L168,128 Z"/>
    <path class="ebeard" d="{mir('M150,118 C132,160 134,220 144,262 L158,246 L162,264 L170,206 L168,128 Z')}"/>
    <path class="ebeardline" d="M150,150 C146,190 148,226 154,250 M250,150 C254,190 252,226 246,250"/>
    <circle class="skin" cx="153" cy="157" r="7"/><circle class="skin" cx="247" cy="157" r="7"/>
    <path class="skin" d="M154,124 C153,160 162,186 186,198 Q200,203 214,198 C238,186 247,160 246,124 Q200,114 154,124 Z"/>
    <path class="cel" d="M154,124 L156,134 Q200,146 244,134 L246,124 Q200,114 154,124 Z"/>
    <path class="wrinkle" d="M180,130 Q200,126 220,130 M184,136 Q200,133 216,136"/>
    {eye(178, "l")}{eye(222, "r")}
    <path class="especs" d="M189,158 Q200,153 211,158"/>
    <path class="nose" d="M201,160 Q197,174 203,177 Q200,179 196,177"/>
    <path class="ebeard" d="M162,174 C160,200 168,232 176,262 C182,292 190,318 200,338 C210,318 218,292 224,262 C232,232 240,200 238,174 C226,192 214,198 200,198 C186,198 174,192 162,174 Z"/>
    <path class="ebeardsh" d="M200,338 C210,318 218,292 224,262 C232,232 240,200 238,174 L232,186 C228,222 220,262 210,300 Z"/>
    <path class="ebeardline" d="M184,212 Q188,256 196,300 M200,204 L200,320 M216,212 Q212,256 204,300 M172,196 Q176,224 182,250"/>
    <path class="ebeard" d="M200,180 Q184,176 172,192 Q186,188 200,186 Q214,188 228,192 Q216,176 200,180 Z"/>
    <path class="mouthline" d="M194,190 Q200,193 206,190"/>
    {HAT_FRONT}
  </g>'''

FRONT = f'''
<g id="character">
  <ellipse class="groundshadow" cx="210" cy="772" rx="72" ry="7"/>
  <path class="erobet" d="M162,330 L238,330 L256,700 L144,700 Z"/>
  <g id="front_leg_l">{front_leg("l")}</g><g id="front_leg_r">{front_leg("r")}</g>
  <g id="boot_l">{front_boot("l")}</g><g id="boot_r">{front_boot("r")}</g>
  <g id="e_body">
    <rect class="skin" x="192" y="190" width="16" height="30"/>
    <path class="etunic" d="M174,214 Q200,206 226,214 L232,362 L168,362 Z"/>
    <path class="erobet" d="M162,222 L146,240 C140,340 136,520 130,702 L172,696 L182,362 L188,240 Z"/>
    <path class="erobet" d="{mir('M162,222 L146,240 C140,340 136,520 130,702 L172,696 L182,362 L188,240 Z')}"/>
    <path class="erobe" d="M162,222 L146,240 C142,300 141,340 140,362 L182,362 L188,240 Z"/>
    <path class="erobe" d="{mir('M162,222 L146,240 C142,300 141,340 140,362 L182,362 L188,240 Z')}"/>
    <path class="elin" d="M172,696 L182,362 L176,362 L164,697 Z"/><path class="elin" d="{mir('M172,696 L182,362 L176,362 L164,697 Z')}"/>
    <path class="estole" d="M180,212 L190,215 L186,430 L170,426 Z"/><path class="estole" d="{mir('M180,212 L190,215 L186,430 L170,426 Z')}"/>
    {symbols(179, 300)}{symbols(221, 300)}
    <path class="elin" d="M166,354 Q200,364 234,354 L234,368 Q200,378 166,368 Z"/>
    <rect class="vialglass" x="172" y="368" width="8" height="22" rx="3"/><rect class="liquid" x="173.5" y="378" width="5" height="11" rx="2"/>
    <rect class="vialglass" x="222" y="368" width="8" height="18" rx="3"/><rect class="liquid2" x="223.5" y="376" width="5" height="9" rx="2"/>
    <rect class="elin" x="184" y="368" width="12" height="40" rx="2"/><path class="esym" d="M186,376 L194,376 M186,384 L194,384 M186,392 L192,392"/>
  </g>
  <g id="arm_l">
    <path class="erobe" d="M160,222 C144,228 138,250 138,280 L126,376 L168,380 L164,286 C165,262 167,244 172,236 Z"/>
    <path class="elin" d="M126,370 L168,374 L166,386 L124,382 Z"/>
    <path class="skin" d="M136,384 Q132,402 140,408 Q148,412 154,406 Q158,396 154,384 Z"/>
    <path class="wrinkle" d="M140,394 L150,394 M141,400 L150,400"/>
  </g>
  <g id="arm_r">
    {staff(282, 62)}
    <path class="erobe" d="M240,222 C258,228 264,252 264,280 L270,336 L298,334 L286,276 C283,252 274,234 256,226 Z"/>
    <path class="elin" d="M268,328 L298,326 L299,338 L269,340 Z"/>
    <path class="skin" d="M272,338 Q270,352 278,356 Q290,358 294,350 Q296,340 292,336 Z"/>
    <path class="wrinkle" d="M276,344 L290,344 M276,349 L290,349"/>
  </g>
  {FRONT_HEAD}
</g>
'''

# ------------------------------------------------------------------ SEITE (gebeugt)
def side_leg(gid, far=False):
    thigh = 'M188,352 C184,430 190,500 195,550 L216,553 C220,500 224,430 222,352 Z'
    shin = 'M196,546 C190,600 194,680 197,726 L214,726 C216,690 219,620 216,553 Z'
    boot = 'M193,718 L216,718 L217,744 L246,754 Q252,762 244,768 L199,768 L194,760 Z'
    s = f'<g id="{gid}"><path class="epants" d="{thigh}"/>'
    if far: s += f'<path class="shade" d="{thigh}"/>'
    s += f'<g id="{gid}_shin"><circle class="epants" cx="206" cy="550" r="10"/><path class="epants" d="{shin}"/>'
    s += f'<path class="boot" d="{boot}"/><path class="bootdark" d="M196,762 L248,762 L244,768 L199,768 Z"/>'
    if far: s += f'<circle class="shade" cx="206" cy="550" r="10"/><path class="shade" d="{shin}"/><path class="shade" d="{boot}"/>'
    return s + '</g></g>'

def side_arm(gid, far=False, with_staff=False):
    upper = 'M188,226 C176,242 178,274 192,292 L218,292 C230,274 230,242 216,226 Z'
    s = f'<g id="{gid}"><g id="{gid}_fore">'
    if with_staff:
        # Unterarm nach vorn gestreckt, stützt sich auf den Stab
        s += staff(292, 40)
        s += '<path class="erobe" d="M194,280 L216,284 L282,318 L276,344 L198,306 Z"/>'
        s += '<path class="elin" d="M276,314 L288,320 L282,348 L270,342 Z"/>'
        s += '<path class="skin" d="M282,324 Q296,320 300,330 Q300,344 290,346 Q280,346 280,336 Z"/>'
    else:
        lower = 'M192,284 L218,284 L228,372 L188,372 Z'
        s += f'<path class="erobe" d="{lower}"/><path class="elin" d="M188,366 L228,366 L229,378 L187,378 Z"/>'
        s += '<path class="skin" d="M198,378 Q194,394 202,400 Q210,404 214,396 Q216,386 212,378 Z"/>'
        if far: s += f'<path class="shade" d="{lower}"/>'
    s += f'</g><path class="erobe" d="{upper}"/>'
    if far: s += f'<path class="shade" d="{upper}"/>'
    return s + '</g>'

SIDE = f'''
<g id="characterSide" style="display:none">
  <ellipse class="groundshadow" cx="210" cy="772" rx="50" ry="6"/>
  <path class="erobet" d="M168,330 L210,330 C208,440 206,560 204,704 L128,696 C140,560 154,440 168,330 Z"/>
  {side_arm("side_arm_far", far=True)}
  {side_leg("side_leg_far", far=True)}
  <path class="erobet" d="M212,342 L238,342 C242,440 244,560 246,690 L222,694 C220,560 216,440 212,342 Z"/>
  {side_leg("side_leg_near")}
  <g id="side_torso">
    <rect class="skin" x="200" y="188" width="18" height="40"/>
    <path class="erobe" d="M186,212 C152,214 146,270 164,346 L236,346 C240,300 238,250 230,232 Q218,214 204,210 Z"/><path class="line" d="M176,224 Q160,250 162,290"/>
    <path class="etunic" d="M222,224 L232,230 C236,262 236,302 234,344 L224,344 Z"/>
    <path class="estole" d="M210,214 L226,222 L230,420 L216,420 Z"/>{symbols(223, 300)}
    <path class="elin" d="M164,346 L238,346 L238,360 L164,360 Z"/>
    <rect class="vialglass" x="168" y="358" width="8" height="22" rx="3"/><rect class="liquid" x="169.5" y="368" width="5" height="11" rx="2"/>
    <path class="line" d="M172,240 Q164,280 170,320"/>
  </g>
  {side_arm("side_arm_near", with_staff=True)}
  <g id="side_head" transform="translate(10 12)">
    <path class="ebeard" d="M158,118 C140,150 136,210 144,268 L156,252 L162,272 L172,236 L180,252 C182,212 186,170 200,130 Z"/>
    <path class="ebeardline" d="M156,150 C150,190 150,228 154,256 M170,150 C164,190 166,224 170,246"/>
    <path class="skin" d="{girl_profile()}"/>
    <path class="skin" d="M252,156 Q262,166 262,176 Q258,180 252,178 Z"/>
    <path class="ebeard" d="M154,116 L226,116 C221,132 217,148 216,166 L216,190 C206,194 196,200 190,212 C184,232 181,252 180,274 L172,258 L166,280 L158,262 L150,276 L144,262 C136,212 138,156 154,116 Z"/>
    <path class="ebeardline" d="M210,128 C204,150 202,172 202,196 M196,126 C188,156 186,190 186,220 M180,128 C170,160 166,206 168,250 M166,132 C156,170 152,212 156,252"/>
    <path class="wrinkle" d="M222,166 l-5,3 M222,162 l-6,0 M238,174 Q244,182 248,180"/>
    <g id="e_side_eye">
      <ellipse class="iris" cx="232" cy="156" rx="2.8" ry="5"/>
      <circle class="hl" cx="232.6" cy="154" r="1.2"/>
      <path class="lash" d="M237,151 Q230,148.6 225,152.6"/>
      <path class="ebeard" d="M223,146 Q232,139 244,141 L244,146 Q233,145 223,150 Z"/>
      <circle class="eglass" cx="236" cy="156" r="9"/><circle class="especs" cx="236" cy="156" r="9"/>
      <path class="especs" d="M227,155 L196,152"/>
    </g>
    <path class="ebeard" d="M214,178 C228,180 246,186 254,196 C258,236 252,280 238,326 C228,294 218,262 210,232 C206,212 206,192 214,178 Z"/>
    <path class="ebeardsh" d="M238,326 C252,280 258,236 254,196 L248,198 C250,240 246,282 238,326 Z"/>
    <path class="ebeardline" d="M224,200 Q230,250 236,300 M216,206 Q220,240 228,280"/>
    <path class="ebeard" d="M246,180 Q258,182 262,192 Q252,188 244,190 Z"/>
    <g id="e_side_hat">
      <path class="ehat" d="M150,118 C150,86 158,56 176,36 Q164,30 150,34 Q136,40 130,56 Q142,46 156,46 Q166,44 180,30 Q200,20 218,34 C234,60 248,92 258,118 Z"/>
      <path class="brass" d="M130,56 L130,68" fill="none" stroke-width="2"/><circle class="brass" cx="130" cy="72" r="5"/>
      <path class="ehat" d="M122,120 Q200,108 288,118 Q290,127 200,131 Q120,129 122,120 Z"/>
      <path class="brass" d="M150,104 Q204,98 256,104 L257,116 Q204,110 150,116 Z"/>
      <circle class="esym" cx="206" cy="66" r="6"/><circle class="esym" cx="206" cy="66" r="1.2"/>
      <path class="esym" d="M186,84 L193,96 L179,96 Z"/>
      <circle class="brass" cx="234" cy="108" r="11"/><ellipse class="eorb" cx="236" cy="108" rx="5" ry="7.5"/>
    </g>
  </g>
</g>
'''

# ------------------------------------------------------------------ RÜCKEN
def back_leg(side):
    return f'<g id="back_leg_{side}">{front_leg(side)}{front_boot(side)}</g>'

def back_arm(side, with_staff=False):
    m = 1 if side == "l" else -1
    X = lambda x: x if m == 1 else 400 - x
    up = f'M{X(170)},222 C{X(150)},220 {X(140)},242 {X(143)},266 L{X(132)},372 L{X(170)},376 L{X(166)},268 C{X(168)},252 {X(172)},244 {X(178)},232 Z'
    s = f'<g id="back_arm_{side}">'
    if with_staff:
        s += staff(X(138), 60)
    s += f'<g transform="rotate({6*m} {X(168)} 230)">'
    s += f'<path class="erobe" d="{up}"/><path class="elin" d="M{X(132)},366 L{X(170)},370 L{X(169)},382 L{X(131)},378 Z"/>'
    s += f'<path class="skin" d="M{X(140)},380 Q{X(136)},398 {X(144)},404 Q{X(152)},408 {X(158)},402 Q{X(162)},392 {X(158)},380 Z"/>'
    return s + '</g></g>'

BACK = f'''
<g id="characterBack" style="display:none">
  <ellipse class="groundshadow" cx="200" cy="772" rx="66" ry="7"/>
  <g id="back_legs">{back_leg("l")}{back_leg("r")}</g>
  <path class="erobet" d="M156,222 Q200,212 244,222 C254,340 262,520 268,704 L210,698 L200,640 L190,698 L132,704 C138,520 146,340 156,222 Z"/>
  <path class="erobe" d="M156,222 Q200,212 244,222 C248,270 250,320 252,362 L148,362 C150,320 152,270 156,222 Z"/>
  <path class="elin" d="M148,354 L252,354 L252,368 L148,368 Z"/>
  <path class="line" d="M200,380 L200,640"/>
  {back_arm("l", with_staff=True)}{back_arm("r")}
  <g id="back_head" transform="translate(0 8)">
    <path class="ebeard" d="M148,116 C134,160 134,240 146,300 L162,282 L170,304 L182,284 L192,310 L200,288 L208,310 L218,284 L230,304 L238,282 L254,300 C266,240 266,160 252,116 Z"/>
    <path class="ebeardline" d="M170,140 C166,200 168,250 174,290 M200,130 L200,300 M230,140 C234,200 232,250 226,290"/>
    <circle class="skin" cx="150" cy="156" r="7"/><circle class="skin" cx="250" cy="156" r="7"/>
    <g id="e_back_hat">
      <path class="ehat" d="M146,118 C150,84 168,40 196,16 Q212,4 230,12 Q246,22 248,40 Q236,30 222,32 C222,60 240,92 254,118 Z"/>
      <path class="brass" d="M248,40 L248,52" fill="none" stroke-width="2"/><circle class="brass" cx="248" cy="56" r="5"/>
      <path class="ehat" d="M126,120 Q200,102 274,120 Q278,131 200,137 Q122,131 126,120 Z"/>
      <path class="brass" d="M148,104 Q200,96 252,104 L253,116 Q200,108 147,116 Z"/>
      <circle class="esym" cx="200" cy="66" r="6"/><circle class="esym" cx="200" cy="66" r="1.2"/>
      <path class="esym" d="M180,84 L187,96 L173,96 Z M218,86 L225,98 L211,98 Z"/>
    </g>
  </g>
</g>
'''

if __name__ == "__main__":
    from gen import ANIME_CSS, ANIME_DEFS
    import anime_dark
    for style, css in (("farbe", ANIME_CSS + E_CSS), ("scherenschnitt", anime_dark.css + E_DARK)):
        for name, body in (("front", FRONT), ("seite", SIDE), ("rueck", BACK)):
            body = body.replace('style="display:none"', '')
            bg = '#e9dcc8' if style == "farbe" else '#a8604e'
            open(f"erzalchemist_{name}_{style}.svg", "w").write(
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 800" width="400" height="800"><title>Erzalchemist – {name}</title>'
                f'<defs>{ANIME_DEFS}{E_DEFS}</defs><style>{css}</style><rect width="400" height="800" fill="{bg}"/>{body}</svg>')
    print("erzalchemist ok")
