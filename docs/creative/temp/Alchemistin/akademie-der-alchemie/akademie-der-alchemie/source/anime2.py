"""Alchemistin – Anime-Körperbau (~7 Kopfhöhen, Beine ≈ 60 % der Figur).
Nutzt Kopf, Haare, CSS und Defs aus gen.py."""
from gen import (HEAD_ANIME, HAIR_BACK_ANIME, ANIME_CSS, ANIME_DEFS, ANIME_BG,
                 spark, scallop)

def M(x):  # Spiegelung um x=200
    return 400 - x

def jabot_small():
    s = ""
    for i, (y, w) in enumerate([(204, 9), (217, 12), (230, 15)]):
        s += (f'<path class="jabot" d="M{200-w},{y} Q200,{y-5} {200+w},{y} '
              f'L{200+w+1},{y+12}{scallop(200+w+1, 200-w-1, y+12, 4, 4)} Z"/>')
    return s

def lacing():
    return "".join(f'<path class="lace" d="M194,{y} L206,{y+7} M206,{y} L194,{y+7}"/>'
                   for y in range(266, 314, 7))

def leg(side):
    X = (lambda x: x) if side == "l" else M
    return (f'<path class="stocking" d="M{X(161)},346 C{X(155)},420 {X(160)},500 {X(165)},545 '
            f'C{X(159)},600 {X(163)},680 {X(167)},745 L{X(180)},745 C{X(183)},690 {X(188)},620 {X(185)},560 '
            f'C{X(189)},505 {X(194)},430 {X(199)},350 Z"/>'
            f'<path class="shade" d="M{X(199)},350 C{X(194)},430 {X(189)},505 {X(185)},560 C{X(188)},620 {X(183)},690 {X(180)},745 '
            f'L{X(176)},745 C{X(179)},680 {X(182)},600 {X(179)},552 C{X(183)},490 {X(187)},430 {X(191)},350 Z"/>')

def boot(side):
    X = (lambda x: x - 11) if side == "l" else (lambda x: M(x - 11))
    lo = lambda a, b: min(X(a), X(b))
    s = f'<g id="boot_{side}">'
    s += (f'<path class="boot" d="M{X(168)},574 L{X(200)},574 L{X(197)},594 C{X(195)},650 {X(193)},700 {X(192)},744 '
          f'L{X(195)},762 Q{X(190)},773 {X(180)},773 Q{X(167)},773 {X(168)},764 L{X(174)},744 '
          f'C{X(173)},700 {X(172)},650 {X(171)},594 Z"/>')
    s += f'<path class="shade" d="M{X(197)},594 C{X(195)},650 {X(193)},700 {X(192)},744 L{X(186)},744 C{X(188)},700 {X(190)},650 {X(191)},594 Z"/>'
    s += f'<path class="bootdark" d="M{X(165)},566 L{X(203)},566 L{X(200)},590 L{X(169)},590 Z"/>'
    for y, a, b in ((640, 171, 196), (700, 172, 194)):
        s += f'<path class="strap" d="M{X(a)},{y+4} L{X(b)},{y-2} L{X(b)},{y+5} L{X(a)},{y+11} Z"/>'
        s += f'<rect class="buckle" x="{lo(184,191)}" y="{y-3}" width="7" height="9" rx="1"/>'
    for y in (578, 584):
        s += f'<circle class="brass" cx="{X(173)}" cy="{y}" r="1.6"/><circle class="brass" cx="{X(196)}" cy="{y}" r="1.6"/>'
    s += '</g>'
    return s

BODY2 = f'''
<g id="character">
  <ellipse class="groundshadow" cx="200" cy="772" rx="72" ry="7"/>

  <g id="skirt_back">
    <path class="skirtback" d="M172,316 C128,380 108,500 90,640 Q128,608 150,662 Q176,614 200,656 Q224,614 250,662 Q272,608 310,640 C292,500 272,380 228,316 Z"/>
    <path class="shade" d="M206,380 C240,460 252,560 250,662 Q224,614 200,656 Z"/>
  </g>

  {HAIR_BACK_ANIME}

  <g id="legs">{leg("l")}{leg("r")}
    <path class="tattoo" d="M159,470 Q174,477 190,470 M168,478 L180,478"/>
  </g>
  {boot("l")}{boot("r")}

  <g id="skirt_front">
    <path class="bloomers" d="M168,366 L232,366 L236,408{scallop(236,164,408,7,5)} Z"/>
    <path class="skirt2" d="M170,330 L230,330 C250,350 262,372 272,396{scallop(272,128,396,10,8)} C138,372 150,350 170,330 Z"/>
    <path class="shade" d="M230,330 C250,350 262,372 272,396 Q263,404 254,396 C244,370 236,350 222,330 Z"/>
    <path class="skirt1" d="M176,312 Q200,318 224,312 C240,332 250,352 258,372{scallop(258,142,372,9,7)} C150,352 160,332 176,312 Z"/>
    <path class="line" d="M186,322 Q182,346 174,368 M200,324 L200,372 M214,322 Q218,346 226,368"/>
  </g>

  <g id="torso">
    <rect class="skin" x="193" y="186" width="14" height="34"/>
    <path class="shade" d="M193,186 L207,186 L207,202 Q200,207 193,202 Z"/>
    <path class="blouse" d="M167,222 Q200,213 233,222 C237,240 235,255 230,268 L170,268 C165,255 163,240 167,222 Z"/>
    <path class="shade" d="M167,222 L176,220 C172,238 172,254 176,268 L170,268 C165,255 163,240 167,222 Z"/>
    {jabot_small()}
    <circle class="brass" cx="200" cy="211" r="5"/><circle class="gem" cx="200" cy="211" r="2.5"/>
    <path class="strap" d="M178,221 L185,220 L189,266 L182,266 Z"/>
    <path class="strap" d="M222,221 L215,220 L211,266 L218,266 Z"/>
    <rect class="buckle" x="180" y="238" width="7" height="8"/><rect class="buckle" x="213" y="238" width="7" height="8"/>
    <path class="corset" d="M171,262 Q200,255 229,262 L231,286 Q222,300 225,318 Q200,325 175,318 Q178,300 169,286 Z"/>
    <path class="shade" d="M171,262 L179,261 Q176,290 182,320 L175,318 Q178,300 169,286 Z"/>
    <path class="corsetpanel" d="M192,260 L208,260 L208,322 L192,322 Z"/>
    {lacing()}
    <circle class="brass" cx="178" cy="268" r="2"/><circle class="brass" cx="222" cy="268" r="2"/>
    <circle class="brass" cx="180" cy="312" r="2"/><circle class="brass" cx="220" cy="312" r="2"/>
    <path class="strap" d="M174,312 Q200,322 226,312 L227,320 Q200,330 173,320 Z"/>
    <rect class="vialglass" x="231" y="304" width="6" height="20" rx="3"/>
    <rect class="liquid2" x="232" y="313" width="4" height="10" rx="2"/>
    <rect class="pouch" x="222" y="316" width="19" height="19" rx="3"/>
    <path class="bootdark" d="M222,316 L241,316 L241,323 L222,323 Z"/>
  </g>

  <!-- LINKER ARM: Hand in der Hüfte -->
  <g id="arm_l">
    <path class="blouse" d="M170,222 C147,217 134,240 139,262 L133,292 Q137,301 148,299 L156,274 C162,258 168,244 173,236 Z"/>
    <path class="shade" d="M139,262 L133,292 Q137,301 148,299 L143,292 Q141,276 146,262 Z"/>
    <path class="blouse" d="M141,287 L171,309 L165,320 L134,298 Z"/>
    <path class="jabot" d="M160,304 L174,312 L170,322{scallop(170,156,316,3,4)} Z"/>
    <path class="skin" d="M168,312 Q178,308 182,316 Q181,326 174,328 Q167,324 168,312 Z"/>
  </g>

  <!-- RECHTER ARM: hebt den Kolben -->
  <g id="arm_r">
    <path class="blouse" d="M230,222 C253,217 266,240 261,262 L267,288 Q263,297 252,295 L246,272 C240,258 234,244 227,236 Z"/>
    <path class="blouse" d="M254,292 L273,218 L287,222 L268,293 Z"/>
    <path class="shade" d="M254,292 L273,218 L279,219 L262,293 Z"/>
    <path class="jabot" d="M270,214 L291,219 L289,231{scallop(289,268,226,3,4)} Z"/>
    <path class="skin" d="M276,214 Q274,200 282,197 Q291,198 290,208 Q288,216 276,214 Z"/>
    <g id="flask">
      <circle class="glow" cx="284" cy="172" r="36"/>
      <rect class="vialglass" x="278" y="134" width="12" height="22" rx="2"/>
      <rect class="cork" x="276" y="126" width="16" height="10" rx="2"/>
      <circle class="vialglass" cx="284" cy="176" r="19"/>
      <path class="liquid" d="M266,178 Q275,172 284,178 Q293,184 302,178 A18,18 0 0 1 266,178 Z"/>
      <circle class="bubble" cx="279" cy="186" r="2.3"/><circle class="bubble" cx="290" cy="182" r="1.6"/>
      <path class="highlight" d="M272,168 Q275,161 280,159"/>
    </g>
  </g>
{HEAD_ANIME}</g>
'''

sparks = spark(330, 140, 9) + spark(318, 214, 5) + spark(250, 140, 5)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 800" width="400" height="800">
<title>Alchemistin – Style D – Anime / Comic (Anime-Proportionen)</title>
<defs>{ANIME_DEFS}</defs>
<style>{ANIME_CSS}</style>
<g id="background">{ANIME_BG}</g>
{BODY2}
<g id="fx">{sparks}</g>
</svg>'''
open("alchemistin_anime.svg", "w").write(svg)
print("ok")
