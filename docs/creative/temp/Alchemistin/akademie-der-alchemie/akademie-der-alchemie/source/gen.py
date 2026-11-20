"""Generiert die Alchemistin in drei Artstyles aus EINER gemeinsamen Geometrie.
Nur der <style>-Block (und ein paar Defs) unterscheiden sich pro Style."""

def scallop(x0, x1, y, n, depth, up=False):
    """Bogenkante von x0 nach x1 (beliebige Richtung) mit n Bögen."""
    step = (x1 - x0) / n
    d = ""
    for i in range(n):
        xa = x0 + step * i
        xm = xa + step / 2
        xb = xa + step
        d += f" Q{xm:.1f},{y + (-depth if up else depth):.1f} {xb:.1f},{y:.1f}"
    return d

def lacing():
    s = ""
    for i in range(7):
        y = 292 + i * 8
        s += f'<path class="lace" d="M193,{y} L207,{y+8} M207,{y} L193,{y+8}"/>'
    return s

def jabot():
    s = ""
    for i in range(4):
        y = 202 + i * 17
        w = 14 + i * 5
        s += (f'<path class="jabot" d="M{200-w},{y} Q200,{y-6} {200+w},{y} '
              f'L{200+w+2},{y+14}{scallop(200+w+2, 200-w-2, y+14, 5, 5)} Z"/>')
    return s

def freckles():
    pts = [(176,163),(181,166),(186,162),(214,162),(219,166),(224,163),(198,160)]
    return "".join(f'<circle class="freckle" cx="{x}" cy="{y}" r="1.2"/>' for x, y in pts)

def boot(side):
    m = 1 if side == "l" else -1
    def X(x):  # spiegelt um x=200
        return x if m == 1 else 400 - x
    p = (f'M{X(167)},598 L{X(199)},598 L{X(198)},742 L{X(203)},762 L{X(160)},762 '
         f'Q{X(158)},748 {X(167)},740 Z')
    s = f'<g id="boot_{side}">'
    s += f'<path class="boot" d="{p}"/>'
    s += f'<path class="bootdark" d="M{X(164)},594 L{X(202)},594 L{X(200)},616 L{X(166)},616 Z"/>'
    for y in (650, 700):
        s += f'<path class="strap" d="M{X(166)},{y} L{X(199)},{y-6} L{X(199)},{y+2} L{X(166)},{y+8} Z"/>'
        s += f'<rect class="buckle" x="{min(X(186),X(194))}" y="{y-5}" width="8" height="9" rx="1"/>'
    for y in (608, 724):
        s += f'<circle class="brass" cx="{X(171)}" cy="{y}" r="2"/><circle class="brass" cx="{X(195)}" cy="{y}" r="2"/>'
    s += '</g>'
    return s

BODY = f'''
<g id="character">
  <!-- Schatten am Boden -->
  <ellipse class="groundshadow" cx="200" cy="764" rx="70" ry="8"/>

  <!-- HINTERER ROCK (high-low, transparent) -->
  <g id="skirt_back">
    <path class="skirtback" d="M166,342 C118,410 92,520 72,650 Q120,615 150,672 Q178,620 200,668 Q222,620 250,672 Q280,615 328,650 C308,520 282,410 234,342 Z"/>
    <path class="shade" d="M200,420 C230,500 250,580 250,672 Q222,620 200,668 Z"/>
  </g>

  <!-- BEINE -->
  <g id="legs">
    <path class="stocking" d="M178,440 L171,640 L195,640 L199,440 Z"/>
    <path class="stocking" d="M201,440 L205,640 L229,640 L222,440 Z"/>
    <path class="tattoo" d="M175,520 Q186,527 197,520 M182,527 L190,527 M207,560 Q217,566 227,560"/>
  </g>
  {boot("l")}
  {boot("r")}

  <!-- ROCK VORNE: Spitzen-Bloomers, zwei Rüschen-Lagen -->
  <g id="skirt_front">
    <path class="bloomers" d="M168,420 L232,420 L236,470{scallop(236,164,470,8,6)} Z"/>
    <path class="skirt2" d="M160,372 L240,372 C262,400 282,425 292,452{scallop(292,108,452,12,9)} C118,425 138,400 160,372 Z"/>
    <path class="shade" d="M240,372 C262,400 282,425 292,452 Q281,461 270,452 C255,420 245,395 232,372 Z"/>
    <path class="skirt1" d="M162,345 Q200,352 238,345 C258,370 270,392 280,416{scallop(280,120,416,10,8)} C130,392 142,370 162,345 Z"/>
    <path class="line" d="M180,355 Q176,385 168,414 M200,356 L200,418 M220,355 Q224,385 232,414"/>
  </g>

  <!-- HAARE HINTEN -->
  <path id="hair_back" class="hair" d="M154,118 C138,162 134,200 144,226 Q154,238 164,228 L236,228 Q246,238 256,226 C266,200 262,162 246,118 Z"/>

  <!-- LINKER ARM (hängend) -->
  <g id="arm_l">
    <path class="blouse" d="M155,222 C112,222 104,280 116,322 C121,343 125,358 128,372 L152,368 C153,338 156,300 166,258 Z"/>
    <path class="shade" d="M116,322 C121,343 125,358 128,372 L138,371 C134,350 128,330 126,300 Z"/>
    <path class="strap" d="M118,298 L158,292 L158,300 L119,307 Z"/>
    <rect class="buckle" x="136" y="292" width="8" height="10"/>
    <path class="jabot" d="M124,368 L156,364 L158,378{scallop(158,124,380,4,5)} Z"/>
    <ellipse class="skin" cx="140" cy="394" rx="10" ry="13"/>
  </g>

  <!-- TORSO -->
  <g id="torso">
    <rect class="skin" x="190" y="186" width="20" height="30"/>
    <path class="shade" d="M190,186 L210,186 L210,200 Q200,206 190,200 Z"/>
    <path class="blouse" d="M150,222 Q200,210 250,222 L242,300 L158,300 Z"/>
    <path class="line" d="M170,240 Q174,265 172,290 M230,240 Q226,265 228,290"/>
    {jabot()}
    <circle class="brass" cx="200" cy="212" r="6"/>
    <circle class="gem" cx="200" cy="212" r="3"/>
    <!-- Träger -->
    <path class="strap" d="M168,222 L178,222 L183,290 L174,290 Z"/>
    <path class="strap" d="M232,222 L222,222 L217,290 L226,290 Z"/>
    <rect class="buckle" x="172" y="246" width="9" height="9"/>
    <rect class="buckle" x="219" y="246" width="9" height="9"/>
    <!-- Korsett -->
    <path class="corset" d="M163,284 Q200,277 237,284 L240,346 Q200,354 160,346 Z"/>
    <path class="shade" d="M163,284 L172,283 L170,348 L160,346 Z"/>
    <path class="corsetpanel" d="M191,284 L209,284 L209,350 L191,350 Z"/>
    {lacing()}
    <circle class="brass" cx="172" cy="292" r="2.2"/><circle class="brass" cx="228" cy="292" r="2.2"/>
    <circle class="brass" cx="171" cy="338" r="2.2"/><circle class="brass" cx="229" cy="338" r="2.2"/>
    <!-- Gürteltasche mit Phiole -->
    <path class="strap" d="M158,340 Q200,350 242,340 L242,348 Q200,358 158,348 Z"/>
    <rect class="vialglass" x="244" y="330" width="7" height="22" rx="3"/>
    <rect class="liquid2" x="245" y="340" width="5" height="11" rx="2"/>
    <rect class="pouch" x="236" y="344" width="22" height="22" rx="3"/>
    <path class="bootdark" d="M236,344 L258,344 L258,352 L236,352 Z"/>
  </g>

  <!-- RECHTER ARM (hebt den Kolben) -->
  <g id="arm_r">
    <path class="blouse" d="M246,222 C292,218 304,268 296,302 L270,308 C268,284 262,262 252,250 Z"/>
    <path class="blouse" d="M270,306 L295,298 L318,252 L296,240 Z"/>
    <path class="shade" d="M270,306 L282,303 L304,246 L296,240 Z"/>
    <path class="jabot" d="M292,236 L322,250 L316,262{scallop(316,288,248,3,5)} Z"/>
    <ellipse class="skin" cx="308" cy="232" rx="11" ry="12"/>
    <g id="flask">
      <circle class="glow" cx="310" cy="196" r="34"/>
      <rect class="vialglass" x="303" y="160" width="14" height="24" rx="2"/>
      <rect class="cork" x="301" y="152" width="18" height="10" rx="2"/>
      <circle class="vialglass" cx="310" cy="202" r="21"/>
      <path class="liquid" d="M290,204 Q300,198 310,204 Q320,210 330,204 A20,20 0 0 1 290,204 Z"/>
      <circle class="bubble" cx="304" cy="212" r="2.5"/><circle class="bubble" cx="315" cy="208" r="1.8"/>
      <circle class="bubble" cx="309" cy="190" r="1.5"/>
      <path class="highlight" d="M297,193 Q300,186 306,184"/>
    </g>
  </g>

  <!-- KOPF -->
  <g id="head">
    <circle class="skin" cx="156" cy="150" r="7"/><circle class="skin" cx="244" cy="150" r="7"/>
    <circle class="brassring" cx="155" cy="162" r="4"/><circle class="brassring" cx="245" cy="162" r="4"/>
    <ellipse class="skin" cx="200" cy="145" rx="44" ry="52"/>
    <path class="shade" d="M157,125 Q200,145 243,125 L243,138 Q200,152 157,138 Z"/>
    <circle class="blush" cx="178" cy="168" r="8"/><circle class="blush" cx="222" cy="168" r="8"/>
    {freckles()}
    <!-- Augen -->
    <path class="lid" d="M173,146 Q183,139 193,146"/><path class="lid" d="M207,146 Q217,139 227,146"/>
    <ellipse class="eye" cx="183" cy="150" rx="5.5" ry="5"/><ellipse class="eye" cx="217" cy="150" rx="5.5" ry="5"/>
    <circle class="glint" cx="185" cy="148" r="1.6"/><circle class="glint" cx="219" cy="148" r="1.6"/>
    <path class="brow" d="M172,135 Q182,130 192,134"/><path class="brow" d="M208,134 Q218,130 228,135"/>
    <path class="nose" d="M199,156 Q197,166 202,167"/>
    <path class="mouth" d="M192,178 Q200,174 208,178 Q200,184 192,178 Z"/>
    <!-- Pony -->
    <path class="hair" d="M156,138 Q160,108 200,104 Q240,108 244,138 Q236,124 222,122 Q214,134 200,128 Q188,138 176,124 Q164,128 156,138 Z"/>
    <!-- Ballonmütze -->
    <g id="cap">
      <ellipse class="cap" cx="198" cy="96" rx="68" ry="32"/>
      <path class="line" d="M198,64 Q176,80 150,104 M198,64 Q222,80 248,104 M198,64 L198,108"/>
      <path class="capdark" d="M146,108 Q200,124 254,108 Q258,122 200,130 Q142,122 146,108 Z"/>
      <circle class="capdark" cx="198" cy="65" r="5"/>
      <!-- Schutzbrille -->
      <path class="strap" d="M132,96 Q198,80 264,96 L264,104 Q198,88 132,104 Z"/>
      <circle class="brass" cx="178" cy="92" r="15"/><circle class="brass" cx="220" cy="92" r="15"/>
      <circle class="lens" cx="178" cy="92" r="10"/><circle class="lens" cx="220" cy="92" r="10"/>
      <path class="highlight" d="M172,88 Q175,84 180,84 M214,88 Q217,84 222,84"/>
      <rect class="brass" x="192" y="89" width="14" height="6" rx="2"/>
      <circle class="bootdark" cx="165" cy="92" r="1.5"/><circle class="bootdark" cx="233" cy="92" r="1.5"/>
    </g>
  </g>
</g>
'''

STYLES = {
"flat": dict(
title="Style A – Flat Vector / Cut-Out",
defs='''<radialGradient id="glowG"><stop offset="0" stop-color="#9ff2b5" stop-opacity=".7"/><stop offset="1" stop-color="#9ff2b5" stop-opacity="0"/></radialGradient>''',
bg='<rect width="400" height="800" fill="#d9cbb6"/><circle cx="200" cy="330" r="190" fill="#cbb89c"/>',
css='''
.skin{fill:#f3d5be}.hair{fill:#7a3524}.cap{fill:#6a4630}.capdark{fill:#4a2f20}
.brass{fill:#c99846}.brassring{fill:none;stroke:#c99846;stroke-width:2}.lens{fill:#86b9ad}
.eye{fill:#2e1c15}.glint{fill:#fff}.lid{fill:none;stroke:#2e1c15;stroke-width:2.2;stroke-linecap:round}
.brow{fill:none;stroke:#5a2619;stroke-width:2.4;stroke-linecap:round}.nose{fill:none;stroke:#c99a83;stroke-width:1.6;stroke-linecap:round}
.mouth{fill:#b4544b}.blush{fill:#e88f86;opacity:.35}.freckle{fill:#b8775c;opacity:.7}
.blouse{fill:#efe3cb}.jabot{fill:#f7eedd;stroke:#d8c7a8;stroke-width:1}.gem{fill:#4d2a3c}
.strap{fill:#5b3a28}.buckle{fill:none;stroke:#c99846;stroke-width:2}
.corset{fill:#4b2d1f}.corsetpanel{fill:#7c563c}.lace{stroke:#e2c39d;stroke-width:1.6;fill:none}
.skirt1{fill:#6e4732}.skirt2{fill:#8f6b56}.skirtback{fill:#8b6f73;opacity:.85}
.bloomers{fill:#f4ecdb}.stocking{fill:#e8c6ae}.tattoo{fill:none;stroke:#b0544b;stroke-width:1.6;opacity:.7}
.boot{fill:#3c241a}.bootdark{fill:#2a1811}.pouch{fill:#6a4630}
.vialglass{fill:#e3f0ec;opacity:.55}.liquid{fill:#4fd27e}.liquid2{fill:#d27e4f}.cork{fill:#a07a52}
.bubble{fill:#d6ffe2}.highlight{fill:none;stroke:#fff;stroke-width:2;stroke-linecap:round;opacity:.8}
.glow{fill:url(#glowG)}.shade{fill:#000;opacity:.13}.line{fill:none;stroke:#000;stroke-opacity:.18;stroke-width:1.5}
.groundshadow{fill:#000;opacity:.15}
'''),
"ink": dict(
title="Style B – Gothic Storybook (Tusche + Sepia)",
defs='''<pattern id="hatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(40)">
<line x1="0" y1="0" x2="0" y2="5" stroke="#2b1d14" stroke-width="1.3"/></pattern>
<radialGradient id="glowG"><stop offset="0" stop-color="#c7e08a" stop-opacity=".55"/><stop offset="1" stop-color="#c7e08a" stop-opacity="0"/></radialGradient>''',
bg='<rect width="400" height="800" fill="#e9dcc0"/><rect x="14" y="14" width="372" height="772" fill="none" stroke="#2b1d14" stroke-width="2"/><rect x="22" y="22" width="356" height="756" fill="none" stroke="#2b1d14" stroke-width=".8"/>',
css='''
*{stroke-linejoin:round;stroke-linecap:round}
.skin,.hair,.cap,.capdark,.blouse,.jabot,.strap,.corset,.corsetpanel,.skirt1,.skirt2,.skirtback,.bloomers,.stocking,.boot,.bootdark,.pouch,.brass,.cork,.vialglass{stroke:#2b1d14;stroke-width:2.4}
.skin{fill:#f0dcc4}.hair{fill:#8a4a33}.cap{fill:#7a5a40}.capdark{fill:#4e3726}
.brass{fill:#b89458}.brassring{fill:none;stroke:#2b1d14;stroke-width:1.8}.lens{fill:#9fb3a0;stroke:#2b1d14;stroke-width:1.5}
.eye{fill:#2b1d14}.glint{fill:#f6efe0}.lid{fill:none;stroke:#2b1d14;stroke-width:2.8}
.brow{fill:none;stroke:#2b1d14;stroke-width:2.2}.nose{fill:none;stroke:#2b1d14;stroke-width:1.6}
.mouth{fill:#9c4a40;stroke:#2b1d14;stroke-width:1.4}.blush{fill:#c97d6a;opacity:.25}.freckle{fill:#2b1d14;opacity:.6}
.blouse{fill:#f1e6cf}.jabot{fill:#f6eedc}.gem{fill:#5a2b38}
.strap{fill:#5a3f2c}.buckle{fill:none;stroke:#2b1d14;stroke-width:2}
.corset{fill:#4e3426}.corsetpanel{fill:#8a6a4e}.lace{stroke:#f1e6cf;stroke-width:1.6;fill:none}
.skirt1{fill:#7a5640}.skirt2{fill:#a07f66}.skirtback{fill:#9a8580}
.bloomers{fill:#f6eedc}.stocking{fill:#ead2b8}.tattoo{fill:none;stroke:#8a2f28;stroke-width:1.6}
.boot{fill:#3e2a1f}.bootdark{fill:#2b1d14}.pouch{fill:#7a5a40}
.vialglass{fill:#f4f2e6;fill-opacity:.4}.liquid{fill:#8fbf5a}.liquid2{fill:#c0703f}.cork{fill:#b08a5e}
.bubble{fill:#f6efe0}.highlight{fill:none;stroke:#fff;stroke-width:2}
.glow{fill:url(#glowG)}.shade{fill:url(#hatch);opacity:.55}.line{fill:none;stroke:#2b1d14;stroke-width:1.4}
.groundshadow{fill:url(#hatch);opacity:.6}
'''),
"silhouette": dict(
title="Style C – Scherenschnitt / Silhouette mit Leuchtakzenten",
defs='''<radialGradient id="bgG" cx=".5" cy=".38" r=".7"><stop offset="0" stop-color="#f2c27a"/><stop offset=".55" stop-color="#b8624a"/><stop offset="1" stop-color="#3a1f2b"/></radialGradient>
<radialGradient id="glowG"><stop offset="0" stop-color="#7dffb0" stop-opacity=".95"/><stop offset=".4" stop-color="#3fe08a" stop-opacity=".45"/><stop offset="1" stop-color="#3fe08a" stop-opacity="0"/></radialGradient>''',
bg='<rect width="400" height="800" fill="url(#bgG)"/><rect y="764" width="400" height="36" fill="#140e10"/>',
css='''
.skin,.hair,.cap,.capdark,.blouse,.jabot,.strap,.corset,.corsetpanel,.skirt1,.skirt2,.bloomers,.stocking,.boot,.bootdark,.pouch,.brass,.cork,.gem{fill:#140e10}
.skirtback{fill:#140e10;opacity:.82}.jabot{stroke:#140e10}
.brassring,.buckle{fill:none;stroke:#140e10;stroke-width:2}
.lens{fill:#ffcf6b}.glint{fill:#ffcf6b}
.eye,.lid,.brow,.nose,.mouth,.blush,.freckle,.line,.tattoo,.shade,.lace{display:none}
.vialglass{fill:#140e10}.liquid{fill:#7dffb0}.liquid2{fill:#ff9a4f}.bubble{fill:#eafff1}
.highlight{fill:none;stroke:#ffe3a3;stroke-width:1.5;stroke-linecap:round}
.glow{fill:url(#glowG)}.groundshadow{display:none}#hair_back{display:none}
'''),
}

for key, s in STYLES.items():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 800" width="400" height="800">
<title>Alchemistin – {s["title"]}</title>
<defs>{s["defs"]}</defs>
<style>{s["css"]}</style>
<g id="background">{s["bg"]}</g>
{BODY}
</svg>'''
    open(f"alchemistin_{key}.svg", "w").write(svg)
print("ok")

# ---------------- ANIME / COMIC ----------------
def eye(cx, side):
    m = 1 if side == "l" else -1
    X = lambda dx: cx + dx * m
    white = (f"M{X(-12)},156 Q{X(-0.5)},145 {X(11.5)},156 Q{X(12)},168 {X(0)},170 Q{X(-12)},168 {X(-12)},156 Z")
    return f'''<g id="eye_{side}">
      <clipPath id="clip_{side}"><path d="{white}"/></clipPath>
      <path class="eyewhite" d="{white}"/>
      <g clip-path="url(#clip_{side})">
        <ellipse class="iris" cx="{X(-0.5)}" cy="160" rx="8.2" ry="9.6"/>
        <ellipse class="irisglow" cx="{X(-0.5)}" cy="165" rx="5.5" ry="3"/>
        <ellipse class="pupil" cx="{X(-0.5)}" cy="159.5" rx="3" ry="3.6"/>
        <path class="irisshadow" d="M{cx-16},140 L{cx+16},140 L{cx+16},154 Q{cx},149 {cx-16},154 Z"/>
      </g>
      <circle class="hl" cx="{X(3)}" cy="156.5" r="2.2"/>
      <circle class="hl" cx="{X(-4)}" cy="164" r="1"/>
      <path class="lash" d="M{X(-13)},156 Q{X(-0.5)},143.5 {X(12.5)},156"/>
      <path class="lash" d="M{X(-13)},156 L{X(-15.5)},154"/>
      <path class="lowlash" d="M{X(-11.5)},164 Q{X(-9)},169.5 {X(-3)},170.5"/>
    </g>'''

HAIR_BACK_ANIME = ('<path id="hair_back" class="hair" d="M150,112 C126,170 124,250 130,304 L145,284 L150,316 '
    'L163,278 L168,236 L232,236 L237,278 L250,316 L255,284 L270,304 C276,250 274,170 250,112 Z"/>'
    '<path class="cel" d="M136,240 C134,270 134,290 136,296 L145,284 L150,316 L158,290 C150,270 146,250 146,236 Z"/>')

HEAD_ANIME = f'''
  <!-- KOPF (Anime) -->
  <g id="head">
    <circle class="skin" cx="151" cy="154" r="6"/><circle class="skin" cx="249" cy="154" r="6"/>
    <circle class="brassring" cx="150" cy="164" r="3.5"/><circle class="brassring" cx="250" cy="164" r="3.5"/>
    <path class="skin" d="M151,124 C149,160 162,184 188,196 Q200,200 212,196 C238,184 251,160 249,124 Q200,114 151,124 Z"/>
    <!-- Cel-Schatten unter Pony und Mütze -->
    <path class="cel" d="M152,146 L164,148 L173,149 L184,130 L196,148 L205,128 L217,147 L226,132 L237,151 L248,144 L249,124 Q200,114 151,124 Z"/>
    <ellipse class="blush" cx="172" cy="176" rx="9" ry="3.5"/><ellipse class="blush" cx="228" cy="176" rx="9" ry="3.5"/>
    {eye(180, "l")}
    {eye(220, "r")}
    <path class="nose" d="M200.5,174 l-1.5,2"/>
    <path class="mouthline" d="M196,186 Q200,188.5 204,186"/>
    <!-- Seitensträhnen -->
    <path class="hair" d="M158,118 Q144,160 148,206 L156,190 L159,212 Q170,170 168,132 Z"/>
    <path class="hair" d="M242,118 Q256,160 252,206 L244,190 L241,212 Q230,170 232,132 Z"/>
    <path class="hairshine" d="M152,160 Q151,172 152,184 L156,176 Z M248,160 Q249,172 248,184 L244,176 Z"/>
    <!-- Pony mit Zacken -->
    <path class="hair" d="M152,146 Q150,106 200,100 Q250,106 248,146 L242,136 L237,143 L226,124 L217,139 L205,120 L196,140 L184,122 L173,141 L164,128 L158,144 Z"/>
    <path class="hairline" d="M184,124 Q190,116 194,110 M205,122 Q206,114 204,108 M226,126 Q224,118 220,112"/>
    <!-- Augenbrauen (über dem Pony) -->
    <g id="brows"><path class="brow2" d="M174.5,142.5 Q177.5,135.5 185,135 Q190,135.5 189,140 Q187.5,143 183,142 Q178.5,141.5 174.5,142.5 Z"/><path class="brow2" d="M225.5,142.5 Q222.5,135.5 215,135 Q210,135.5 211,140 Q212.5,143 217,142 Q221.5,141.5 225.5,142.5 Z"/></g>
    <!-- Mütze, leicht schräg -->
    <g id="cap" transform="rotate(-7 200 100)">
      <ellipse class="cap" cx="198" cy="94" rx="70" ry="32"/>
      <path class="cel" d="M140,104 Q200,126 258,104 Q262,92 255,84 Q200,108 138,90 Z"/>
      <path class="line" d="M198,62 Q176,78 148,102 M198,62 Q222,78 250,102"/>
      <path class="capdark" d="M144,106 Q200,122 256,106 Q260,122 200,130 Q140,122 144,106 Z"/>
      <circle class="capdark" cx="198" cy="63" r="5"/>
      <path class="strap" d="M130,94 Q198,78 266,94 L266,102 Q198,86 130,102 Z"/>
      <circle class="brass" cx="178" cy="90" r="15"/><circle class="brass" cx="220" cy="90" r="15"/>
      <circle class="lens" cx="178" cy="90" r="10"/><circle class="lens" cx="220" cy="90" r="10"/>
      <path class="lensshine" d="M171,86 L177,82 L180,85 L174,89 Z M213,86 L219,82 L222,85 L216,89 Z"/>
      <rect class="brass" x="192" y="87" width="14" height="6" rx="2"/>
    </g>
  </g>
'''

body_anime = BODY.split('  <!-- KOPF -->')[0] + HEAD_ANIME + '</g>\n'
import re
body_anime = re.sub(r'<path id="hair_back"[^>]*/>', HAIR_BACK_ANIME, body_anime)

ANIME_CSS = '''
*{stroke-linejoin:round;stroke-linecap:round}
.skin,.hair,.cap,.capdark,.blouse,.jabot,.strap,.corset,.corsetpanel,.skirt1,.skirt2,.skirtback,.bloomers,.stocking,.boot,.bootdark,.pouch,.brass,.cork,.vialglass,.eyewhite{stroke:#3b2219;stroke-width:2.2}
.skin{fill:#fde4d4}.cel{fill:#c4685a;opacity:.32}
.hair{fill:#b8482c}.hairshine{fill:#f28a5e}.hairline{fill:none;stroke:#6e2416;stroke-width:1.3}
.cap{fill:#7b5038}.capdark{fill:#4f3021}
.brass{fill:#e0ad4a}.brassring{fill:none;stroke:#e0ad4a;stroke-width:2}.lens{fill:#7fd3c8;stroke:#3b2219;stroke-width:1.5}.lensshine{fill:#fff;opacity:.9}
.eyewhite{fill:#fff;stroke-width:0}.iris{fill:url(#irisG);stroke:#5a2a10;stroke-width:.8}.pupil{fill:#2a120a}.irisshadow{fill:#3b2219;opacity:.35}
.hl{fill:#fff}.lash{fill:none;stroke:#2a140c;stroke-width:2.2}.crease{fill:none;stroke:#8a4a3a;stroke-width:1;opacity:.7}.irisglow{fill:#ffe9a8;opacity:.55}.blush{fill:#f59a92;opacity:.4}.mouthline{fill:none;stroke:#8a3a32;stroke-width:1.5}.lowlash{fill:none;stroke:#3b2219;stroke-width:1.2}
.nose{fill:none;stroke:#c98a76;stroke-width:1.5}.mouth{fill:#c0544c;stroke:#3b2219;stroke-width:1.2}
.blushline{fill:none;stroke:#ee7f7a;stroke-width:1.4;opacity:.8}
.blouse{fill:#fbf3e3}.jabot{fill:#fff8ec}.gem{fill:#8a2f5a}
.strap{fill:#64402c}.buckle{fill:none;stroke:#e0ad4a;stroke-width:2}
.corset{fill:#57321f}.corsetpanel{fill:#8c5c3c}.lace{stroke:#f6d9a8;stroke-width:1.6;fill:none}
.skirt1{fill:#7d4c32}.skirt2{fill:#a3745a}.skirtback{fill:#9c7a9a;opacity:.85}
.bloomers{fill:#fff8ec}.stocking{fill:#f6d6c2}.tattoo{fill:none;stroke:#c2463e;stroke-width:1.6}
.boot{fill:#432619}.bootdark{fill:#2c1810}.pouch{fill:#7b5038}
.vialglass{fill:#eafaf6;fill-opacity:.45}.liquid{fill:#3fe08a}.liquid2{fill:#ff8c4a}.cork{fill:#b88a5a}
.bubble{fill:#eafff1}.highlight{fill:none;stroke:#fff;stroke-width:2.2}
.glow{fill:url(#glowG)}.shade{fill:#5b2a4a;opacity:.22}.line{fill:none;stroke:#3b2219;stroke-width:1.2;opacity:.6}
.groundshadow{fill:#5b2a4a;opacity:.25}
.sparkle{fill:#fff6c9}.brow2{fill:#8a2f1c;stroke:#6e2416;stroke-width:.6}
'''
ANIME_DEFS = '''<linearGradient id="irisG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a2410"/><stop offset=".55" stop-color="#b8701e"/><stop offset="1" stop-color="#ffd36a"/></linearGradient>
<radialGradient id="glowG"><stop offset="0" stop-color="#8dffbd" stop-opacity=".85"/><stop offset="1" stop-color="#8dffbd" stop-opacity="0"/></radialGradient>
<linearGradient id="bgA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe9c9"/><stop offset="1" stop-color="#f3b9a4"/></linearGradient>
<pattern id="dots" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="2.2" fill="#e58f7e" opacity=".5"/></pattern>'''
spark = lambda x, y, r: f'<path class="sparkle" d="M{x},{y-r} L{x+r*.25},{y-r*.25} L{x+r},{y} L{x+r*.25},{y+r*.25} L{x},{y+r} L{x-r*.25},{y+r*.25} L{x-r},{y} L{x-r*.25},{y-r*.25} Z"/>'
ANIME_BG = ('<rect width="400" height="800" fill="url(#bgA)"/>'
            '<path d="M400,0 L400,330 L230,0 Z" fill="url(#dots)"/><path d="M0,800 L0,520 L170,800 Z" fill="url(#dots)"/>'
            '<rect x="10" y="10" width="380" height="780" fill="none" stroke="#3b2219" stroke-width="4"/>')
sparks = spark(345, 175, 9) + spark(332, 238, 5) + spark(282, 168, 6)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 800" width="400" height="800">
<title>Alchemistin – Style D – Anime / Comic (Cel-Shading)</title>
<defs>{ANIME_DEFS}</defs>
<style>{ANIME_CSS}</style>
<g id="background">{ANIME_BG}</g>
{body_anime}
<g id="fx">{sparks}</g>
</svg>'''
open("alchemistin_anime.svg", "w").write(svg)
