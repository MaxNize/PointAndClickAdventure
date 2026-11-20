"""Baut die spielbare Demo-Szene 'Lehrsaal der Alchemie' als eine HTML-Datei.
Charakter-Geometrie kommt aus anime2.BODY2, Styles aus gen / anime_dark."""
import re
from gen import ANIME_CSS, ANIME_DEFS
from anime2 import BODY2
from side import SIDE
from back import BACK
from anime2 import leg as _front_leg
import anime_dark

def scope(css, prefix):
    out = []
    for sel, body in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
        sels = ", ".join(f"{prefix} {s.strip()}" for s in sel.split(",") if s.strip())
        out.append(f"{sels}{{{body}}}")
    return "\n".join(out)

# ---------------------------------------------------------------- Szene
def jar(x, yb, content, label):
    return (f'<rect class="s-glass" x="{x}" y="{yb-46}" width="36" height="46" rx="7"/>'
            f'<rect class="{content}" x="{x+3}" y="{yb-30}" width="30" height="27" rx="5"/>'
            f'<rect class="s-lid" x="{x+2}" y="{yb-52}" width="32" height="8" rx="2"/>'
            f'<rect class="s-paper" x="{x+6}" y="{yb-27}" width="24" height="13" rx="1"/>'
            f'<text class="s-label" x="{x+18}" y="{yb-17}" text-anchor="middle">{label}</text>')

def key(x, y):
    return (f'<g class="s-key"><circle cx="{x-11}" cy="{y}" r="6.5" fill="none" stroke-width="3.5"/>'
            f'<rect x="{x-5}" y="{y-1.8}" width="22" height="3.6"/><rect x="{x+10}" y="{y+1}" width="3" height="6"/>'
            f'<rect x="{x+15}" y="{y+1}" width="3" height="8"/></g>')

books = ""
bx = 398
for w, h, c in [(16, 104, 1), (13, 92, 2), (18, 116, 3), (14, 98, 1), (17, 110, 2)]:
    books += f'<rect class="s-book{c}" x="{bx}" y="{300-h}" width="{w}" height="{h}" rx="2"/>'
    books += f'<rect class="s-bookband" x="{bx}" y="{300-h+14}" width="{w}" height="4"/>'
    bx += w + 2
books += '<path class="s-book3" d="M496,300 L516,206 L532,210 L512,300 Z"/>'

SCENE = f'''
<g id="scene">
  <!-- Wand & Boden -->
  <rect class="s-wall" x="0" y="0" width="1280" height="600"/>
  <rect class="s-bricks" x="0" y="0" width="1280" height="600" fill="url(#bricks)"/>
  <rect class="s-woodd" x="0" y="584" width="1280" height="16"/>
  <rect class="s-floor" x="0" y="600" width="1280" height="120"/>
  <path class="s-plank" d="M0,632 L1280,632 M0,668 L1280,668 M0,704 L1280,704 M210,600 L200,632 M520,632 L512,668 M860,600 L866,632 M1100,668 L1110,704 M330,668 L322,704 M720,668 L724,704"/>
  <rect class="s-floorshade" x="0" y="600" width="1280" height="120"/>
  <path class="s-lightpool" d="M150,604 L370,604 L470,720 L120,720 Z"/>
  <ellipse class="s-floorcircle" cx="780" cy="672" rx="130" ry="24"/>
  <ellipse class="s-floorcircle" cx="780" cy="672" rx="104" ry="18"/>
  <path class="s-floorcircle" d="M676,672 L884,672 M780,648 L780,696 M707,659 L853,685 M707,685 L853,659"/>

  <!-- Fenster -->
  <path class="s-stone" d="M168,404 L168,176 A92,92 0 0 1 352,176 L352,404 Z"/>
  <path class="s-sky" d="M184,396 L184,178 A76,76 0 0 1 336,178 L336,396 Z"/>
  <g class="s-stars"><circle cx="214" cy="200" r="1.8"/><circle cx="236" cy="150" r="1.4"/><circle cx="312" cy="250" r="1.6"/><circle cx="222" cy="300" r="1.2"/><circle cx="300" cy="330" r="1.5"/><circle cx="210" cy="360" r="1.3"/></g>
  <circle class="s-moon" cx="296" cy="176" r="22"/>
  <circle class="s-sky" cx="306" cy="170" r="18"/>
  <rect class="s-stone" x="256" y="100" width="8" height="298"/>
  <rect class="s-stone" x="184" y="272" width="152" height="7"/>
  <rect class="s-stone" x="156" y="396" width="208" height="16" rx="3"/>
  <path class="s-candle" d="M196,396 L196,372 L204,372 L204,396 Z"/><path class="s-flame2 flicker" d="M200,370 Q194,362 200,352 Q206,362 200,370 Z"/>

  <!-- Pult mit Eisblock -->
  <rect class="s-wood" x="82" y="470" width="16" height="130"/>
  <rect class="s-woodd" x="58" y="592" width="64" height="12" rx="3"/>
  <path class="s-woodd" d="M42,472 L138,458 L138,472 L42,486 Z"/>
  <ellipse id="puddle" class="s-water" cx="92" cy="646" rx="48" ry="7" style="display:none"/>
  <g id="iceBlock">
    <rect class="s-ice" x="54" y="388" width="72" height="74" rx="9"/>
    <g opacity=".75">{key(92, 424)}</g>
    <path class="s-icehl" d="M64,400 L74,398 M62,410 L62,440 M114,446 L116,454"/>
  </g>
  <g id="keyLoose" style="display:none">{key(92, 456)}</g>

  <!-- Regal -->
  <rect class="s-wood" x="378" y="60" width="184" height="540" rx="3"/>
  <rect class="s-shelfback" x="390" y="72" width="160" height="516"/>
  <g id="crystal">
    <circle class="s-crystalglow" cx="470" cy="128" r="48"/>
    <path class="s-crystal" d="M470,96 L488,128 L470,158 L452,128 Z"/>
    <path class="s-crystalhl" d="M470,100 L476,128 L470,154"/>
  </g>
  {books}
  {jar(404, 420, "s-water", "Aqua")}
  {jar(458, 420, "s-earth", "Terra")}
  <rect class="s-glass" x="512" y="384" width="26" height="36" rx="6"/><rect class="s-potion1" x="515" y="398" width="20" height="19" rx="4"/>
  {jar(404, 520, "s-iron", "Ferrum")}
  <rect class="s-glass" x="458" y="486" width="22" height="34" rx="5"/><rect class="s-potion2" x="461" y="500" width="16" height="17" rx="4"/>
  <rect class="s-glass" x="490" y="474" width="26" height="46" rx="6"/><rect class="s-potion1" x="493" y="494" width="20" height="23" rx="4"/>
  <rect class="s-book2" x="396" y="560" width="120" height="14" rx="2"/><rect class="s-book1" x="404" y="546" width="104" height="14" rx="2"/>
  <g class="s-wood"><rect x="378" y="156" width="184" height="10"/><rect x="378" y="298" width="184" height="10"/>
    <rect x="378" y="418" width="184" height="10"/><rect x="378" y="518" width="184" height="10"/></g>

  <!-- Pflanze -->
  <g id="plantDead">
    <path class="s-dead" d="M600,592 Q588,560 566,566 M600,592 Q606,552 628,560 M600,592 Q598,556 601,538 Q605,528 595,522"/>
    <ellipse class="s-deadleaf" cx="566" cy="568" rx="7" ry="3" transform="rotate(30 566 568)"/>
    <ellipse class="s-deadleaf" cx="628" cy="562" rx="7" ry="3" transform="rotate(-20 628 562)"/>
  </g>
  <g id="vine" style="display:none">
    <path class="s-vine" d="M600,592 C585,520 602,470 576,420 C556,380 590,330 570,280 C556,240 586,190 568,140 C560,112 576,92 566,70"/>
    <g class="s-leaf">
      <ellipse cx="588" cy="540" rx="13" ry="6" transform="rotate(-30 588 540)"/><ellipse cx="612" cy="560" rx="13" ry="6" transform="rotate(25 612 560)"/>
      <ellipse cx="596" cy="470" rx="12" ry="6" transform="rotate(20 596 470)"/><ellipse cx="566" cy="420" rx="12" ry="6" transform="rotate(-25 566 420)"/>
      <ellipse cx="590" cy="350" rx="12" ry="6" transform="rotate(25 590 350)"/><ellipse cx="562" cy="300" rx="12" ry="6" transform="rotate(-30 562 300)"/>
      <ellipse cx="586" cy="220" rx="12" ry="6" transform="rotate(20 586 220)"/><ellipse cx="560" cy="160" rx="12" ry="6" transform="rotate(-25 560 160)"/>
      <ellipse cx="578" cy="100" rx="11" ry="5" transform="rotate(20 578 100)"/>
    </g>
    <g class="s-flower"><circle cx="602" cy="440" r="5"/><circle cx="575" cy="250" r="5"/><circle cx="570" cy="80" r="5"/></g>
  </g>
  <path class="s-pot" d="M576,640 L570,600 L630,600 L624,640 Z"/>
  <rect class="s-pot" x="565" y="590" width="70" height="13" rx="3"/>

  <!-- Tafel -->
  <rect class="s-wood" x="652" y="102" width="276" height="206" rx="4"/>
  <rect class="s-board" x="664" y="114" width="252" height="182"/>
  <g class="s-chalk">
    <text x="680" y="146" font-size="18" textLength="196" lengthAdjust="spacingAndGlyphs">Lektion 1: Transmutation</text>
    <text x="680" y="182" font-size="16">Wasser + Erde = ?</text>
    <text x="680" y="208" font-size="16">Wasser + Feuer = ?</text>
    <text x="680" y="234" font-size="13" textLength="160" lengthAdjust="spacingAndGlyphs">(Feuer gibt's im Athanor)</text>
    <text x="680" y="276" font-size="14" textLength="196" lengthAdjust="spacingAndGlyphs">Schlüssel ⇒ erst im 2. Lehrjahr!</text>
  </g>
  <g class="s-chalkline">
    <path d="M680,152 L876,152"/><circle cx="878" cy="204" r="26"/><path d="M878,180 L900,216 L856,216 Z"/>
    <rect x="890" y="264" width="14" height="12" rx="2"/><path d="M893,264 Q893,254 897,254 Q901,254 901,264"/>
  </g>
  <rect class="s-chalkpiece" x="700" y="296" width="14" height="5" rx="2"/>

  <!-- Eule -->
  <g id="owl">
    <path class="s-owl" d="M880,78 L884,62 L892,72 L898,72 L906,62 L910,78 Z"/>
    <ellipse class="s-owl" cx="895" cy="88" rx="19" ry="23"/>
    <ellipse class="s-owlbelly" cx="895" cy="96" rx="11" ry="13"/>
    <circle class="s-owleye" cx="888" cy="81" r="6.5"/><circle class="s-owleye" cx="902" cy="81" r="6.5"/>
    <g class="blink"><circle class="s-owlpupil" cx="888" cy="81" r="3"/><circle class="s-owlpupil" cx="902" cy="81" r="3"/></g>
    <path class="s-beak" d="M892,86 L898,86 L895,92 Z"/>
    <path class="s-owlfeet" d="M889,110 L889,104 M901,110 L901,104"/>
  </g>

  <!-- Werkbank & Kessel -->
  <rect class="s-wood" x="680" y="512" width="14" height="128"/><rect class="s-wood" x="866" y="512" width="14" height="128"/>
  <rect class="s-woodd" x="674" y="514" width="212" height="22"/>
  <rect class="s-wood" x="664" y="502" width="232" height="14" rx="3"/>
  <circle id="brewGlow" class="s-brewglow" cx="780" cy="448" r="80"/>
  <path class="s-metal" d="M736,462 Q734,506 780,506 Q826,506 824,462 Z"/>
  <path class="s-metald" d="M750,504 L744,512 M810,504 L816,512"/>
  <ellipse class="s-metald" cx="780" cy="462" rx="47" ry="10"/>
  <ellipse id="brew" class="s-brew" cx="780" cy="463" rx="39" ry="6.5"/>
  <g class="s-bubble"><circle class="bub b1" cx="766" cy="458" r="3"/><circle class="bub b2" cx="790" cy="458" r="2.3"/><circle class="bub b3" cx="780" cy="458" r="2"/></g>
  <path class="s-metal" d="M684,502 L690,484 L712,484 L718,502 Z"/><path class="s-woodd" d="M706,486 L722,466"/>
  <rect class="s-book1" x="836" y="490" width="44" height="12" rx="2"/><rect class="s-paper" x="840" y="482" width="36" height="8" rx="1"/>

  <!-- Athanor -->
  <rect class="s-stone2" x="996" y="236" width="40" height="90"/>
  <path class="s-stone2" d="M958,600 L958,362 Q958,318 1016,314 Q1074,318 1074,362 L1074,600 Z"/>
  <path class="s-mortar" d="M958,400 L1074,400 M958,450 L1074,450 M958,500 L1074,500 M958,550 L1074,550 M1000,362 L1000,400 M1040,400 L1040,450 M990,450 L990,500 M1050,500 L1050,550 M1012,318 L1012,362"/>
  <path class="s-hole" d="M980,586 L980,520 A36,36 0 0 1 1052,520 L1052,586 Z"/>
  <g id="fire" style="display:none">
    <circle class="s-fireglow" cx="1016" cy="548" r="90"/>
    <path class="s-flame1 flicker" d="M986,584 Q990,540 1006,524 Q1004,552 1016,560 Q1022,528 1040,512 Q1048,556 1044,584 Z"/>
    <path class="s-flame2 flicker2" d="M998,584 Q1002,556 1012,546 Q1012,566 1020,568 Q1026,548 1034,540 Q1040,566 1034,584 Z"/>
  </g>
  <rect class="s-coal" x="984" y="580" width="64" height="8" rx="3"/>
  <rect class="s-metal" x="992" y="340" width="48" height="14" rx="2"/>
  <text class="s-plate" x="1016" y="351" text-anchor="middle">ATHANOR</text>

  <!-- Tür -->
  <path class="s-stone2" d="M1108,600 L1108,282 A77,77 0 0 1 1262,282 L1262,600 Z"/>
  <path id="doorway" class="s-hole" d="M1124,600 L1124,286 A61,61 0 0 1 1246,286 L1246,600 Z"/>
  <g id="doorPanel">
    <path class="s-wood" d="M1124,600 L1124,286 A61,61 0 0 1 1246,286 L1246,600 Z"/>
    <path class="s-woodline" d="M1155,600 L1155,244 M1185,600 L1185,226 M1215,600 L1215,244"/>
    <rect class="s-metal" x="1124" y="330" width="122" height="10"/><rect class="s-metal" x="1124" y="526" width="122" height="10"/>
    <rect class="s-metal" x="1220" y="418" width="18" height="34" rx="2"/>
    <circle class="s-keyhole" cx="1229" cy="430" r="3.5"/><rect class="s-keyhole" x="1227.5" y="430" width="3" height="10"/>
  </g>

  <path id="doorLeaf" class="s-wood" style="display:none" d="M1124,600 L1124,286 Q1126,246 1142,232 L1152,238 L1152,612 Z"/>
  <rect class="s-vignette" x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>
</g>
'''

DEFS = '''
<pattern id="bricks" width="80" height="40" patternUnits="userSpaceOnUse">
  <path d="M0,0.5 L80,0.5 M0,20.5 L80,20.5 M0.5,0 L0.5,20 M40.5,20 L40.5,40" stroke="#5f4d46" stroke-width="1.5" fill="none" opacity=".55"/>
</pattern>
<linearGradient id="skyG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d2650"/><stop offset="1" stop-color="#4a4f86"/></linearGradient>
<linearGradient id="duskSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe2a6"/><stop offset="1" stop-color="#f29a5e"/></linearGradient>
<radialGradient id="duskWall" cx=".3" cy=".45" r=".85"><stop offset="0" stop-color="#e8a16a"/><stop offset=".45" stop-color="#9a4e44"/><stop offset="1" stop-color="#42243a"/></radialGradient>
<linearGradient id="floorG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5e353a"/><stop offset="1" stop-color="#321d24"/></linearGradient>
<linearGradient id="poolG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff9a5a" stop-opacity=".2"/><stop offset="1" stop-color="#ffcf8a" stop-opacity="0"/></linearGradient>
<radialGradient id="vignette" cx=".5" cy=".5" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/></radialGradient>
<radialGradient id="crystalG"><stop offset="0" stop-color="#fff08a" stop-opacity=".8"/><stop offset="1" stop-color="#fff08a" stop-opacity="0"/></radialGradient>
<radialGradient id="fireG"><stop offset="0" stop-color="#ffb347" stop-opacity=".75"/><stop offset="1" stop-color="#ff7a2a" stop-opacity="0"/></radialGradient>
<radialGradient id="brewG"><stop offset="0" style="stop-color:var(--brew,#9be7ff);stop-opacity:.55"/><stop offset="1" style="stop-color:var(--brew,#9be7ff);stop-opacity:0"/></radialGradient>
<radialGradient id="doorLight" cx=".5" cy=".6" r=".7"><stop offset="0" stop-color="#fff4cf"/><stop offset="1" stop-color="#f2b866"/></radialGradient>
'''

OUT = "stroke:#3b2219;stroke-width:2;stroke-linejoin:round"
SCENE_COLOR = f'''
.s-wall{{fill:#8b766b}} .s-floor{{fill:#6e4a32}} .s-plank{{stroke:#4d3121;stroke-width:2;fill:none}}
.s-floorcircle{{fill:none;stroke:#f3e6c8;stroke-width:2;opacity:.35}}
.s-wood,.s-lid{{fill:#7b5038;{OUT}}} .s-woodd{{fill:#553521;{OUT}}} .s-woodline{{stroke:#4a2d1c;stroke-width:2;fill:none}}
.s-shelfback{{fill:#4a2f20}} .s-stone{{fill:#a8978b;{OUT}}} .s-stone2{{fill:#9a877a;{OUT}}} .s-mortar{{stroke:#6f5d52;stroke-width:2;fill:none}}
.s-sky{{fill:url(#skyG)}} .s-moon{{fill:#fff3c4}} .s-stars{{fill:#fff}}
.s-candle{{fill:#f3ead2;{OUT}}} .s-flame2{{fill:#ffd84a}} .s-flame1{{fill:#ff8a2a}}
.s-glass{{fill:#dff4f0;fill-opacity:.45;{OUT}}} .s-water{{fill:#4aa8e0}} .s-earth{{fill:#7a4f2e}} .s-iron{{fill:#8d939b}}
.s-potion1{{fill:#b35bd1}} .s-potion2{{fill:#e2504a}} .s-paper{{fill:#efe3c4}} .s-label{{font:bold 8px Georgia,serif;fill:#3b2219}}
.s-book1{{fill:#8a2f3a;{OUT}}} .s-book2{{fill:#2f5a8a;{OUT}}} .s-book3{{fill:#a0742a;{OUT}}} .s-bookband{{fill:#e0ad4a}}
.s-crystal{{fill:#ffd84a;{OUT}}} .s-crystalhl{{stroke:#fff;stroke-width:2;fill:none}} .s-crystalglow{{fill:url(#crystalG)}}
.s-dead{{stroke:#7a5a3a;stroke-width:3;fill:none;stroke-linecap:round}} .s-deadleaf{{fill:#9a7a4a}}
.s-vine{{stroke:#3f7f32;stroke-width:7;fill:none;stroke-linecap:round}} .s-leaf{{fill:#6dbb4a;stroke:#2f5a24;stroke-width:1.5}} .s-flower{{fill:#f2a7c4;stroke:#3b2219;stroke-width:1}}
.s-pot{{fill:#c0693f;{OUT}}}
.s-board{{fill:#2f3d34;{OUT}}} .s-chalk{{fill:#f3efe2;font-family:"Segoe Print","Comic Sans MS","Chalkboard SE",cursive}} .s-chalkline{{stroke:#f3efe2;stroke-width:2;fill:none;opacity:.85}} .s-chalkpiece{{fill:#fff}}
.s-owl{{fill:#8a6a4e;{OUT}}} .s-owlbelly{{fill:#dcc6a2}} .s-owleye{{fill:#ffcf6b;stroke:#3b2219;stroke-width:1.5}} .s-owlpupil{{fill:#2a140c}} .s-beak{{fill:#e0ad4a}} .s-owlfeet{{stroke:#e0ad4a;stroke-width:3}}
.s-metal{{fill:#4a4a55;{OUT}}} .s-metald{{fill:#2e2e36;{OUT}}} .s-brew{{fill:var(--brew,#9be7ff)}} .s-brewglow{{fill:url(#brewG)}} .s-bubble{{fill:#fff;opacity:.8}}
.s-hole{{fill:#1a120e}} .s-coal{{fill:#2a1a14}} .s-fireglow{{fill:url(#fireG)}} .s-plate{{font:bold 9px Georgia,serif;fill:#e0ad4a}}
.s-keyhole{{fill:#120a08}} .s-lightpool,.s-floorshade{{display:none}} .s-doorlight{{fill:url(#doorLight)}}
.s-ice{{fill:#bfe9f5;fill-opacity:.75;stroke:#5a9ab0;stroke-width:2}} .s-icehl{{stroke:#fff;stroke-width:2.5;fill:none;stroke-linecap:round}}
.s-key{{fill:#e0ad4a;stroke:#e0ad4a}}
'''
RIM = "stroke:#d98a62;stroke-width:1.6;stroke-linejoin:round"
RIM2 = "stroke:#b5665a;stroke-width:1.3;stroke-linejoin:round"
FAR, MID, NEAR = "#4a2c33", "#3a242b", "#2e1c22"
DETAIL = "#6a3e42"
SCENE_DARK = f'''
.s-wall{{fill:url(#duskWall)}} .s-bricks{{opacity:.35}}
.s-floor{{fill:url(#floorG)}} .s-floorshade{{display:none}} .s-plank{{stroke:#5a3236;stroke-width:1.5;fill:none;opacity:.8}}
.s-lightpool{{fill:url(#poolG)}}
.s-floorcircle{{fill:none;stroke:#ffcf6b;stroke-width:2;opacity:.3}}
/* Mittelgrund: Möbel */
.s-wood,.s-stone,.s-stone2,.s-metal,.s-candle{{fill:{MID};{RIM}}}
.s-woodd,.s-metald{{fill:#33202a;{RIM2}}}
.s-shelfback,.s-hole{{fill:#2a181d}} .s-board{{fill:{FAR};{RIM2}}}
.s-woodline,.s-mortar{{stroke:{DETAIL};stroke-width:1.8;fill:none}}
.s-book1{{fill:#5a3238;{RIM2}}} .s-book2{{fill:#46293a;{RIM2}}} .s-book3{{fill:#66403e;{RIM2}}} .s-bookband{{fill:#8a5a3a}}
.s-paper{{fill:#d9b98e}} .s-label{{font:bold 8px Georgia,serif;fill:#2e1c22}} .s-plate{{font:bold 9px Georgia,serif;fill:#c9824a}}
.s-chalkpiece{{fill:#ffcf6b;opacity:.5}}
/* Vordergrund */
.s-pot,.s-coal{{fill:{NEAR};{RIM}}}
.s-glass{{fill:#6a454b;{RIM2}}} .s-lid{{fill:#8a5e58;{RIM2}}}
.s-sky{{fill:url(#duskSky)}} .s-moon{{fill:#fff8e0}} .s-stars{{display:none}}
.s-flame2{{fill:#ffd84a}} .s-flame1{{fill:#ff8a2a}}
.s-water{{fill:#5ac8ff}} .s-earth{{fill:#c98a4e}} .s-iron{{fill:#b8c0cc}} .s-potion1{{fill:#c77bff}} .s-potion2{{fill:#ff6a5a}}
.s-crystal{{fill:#ffe46b}} .s-crystalhl{{stroke:#fff;stroke-width:2;fill:none}} .s-crystalglow{{fill:url(#crystalG)}}
.s-dead{{stroke:{NEAR};stroke-width:3;fill:none}} .s-deadleaf{{fill:{NEAR}}}
.s-vine{{stroke:{NEAR};stroke-width:7;fill:none;stroke-linecap:round}} .s-leaf{{fill:#2f3a28;stroke:#d98a62;stroke-width:1}} .s-flower{{fill:#ffb3d1}}
.s-chalk{{fill:#ffcf6b;opacity:.6;font-family:"Segoe Print","Comic Sans MS","Chalkboard SE",cursive}} .s-chalkline{{stroke:#ffcf6b;stroke-width:2;fill:none;opacity:.45}}
.s-owl{{fill:{NEAR};{RIM}}} .s-owlbelly{{fill:#55343a}} .s-owleye{{fill:#ffcf6b}} .s-owlpupil{{fill:{NEAR}}} .s-beak{{fill:#c9824a}} .s-owlfeet{{stroke:#c9824a;stroke-width:3}}
.s-brew{{fill:var(--brew,#9be7ff)}} .s-brewglow{{fill:url(#brewG)}} .s-bubble{{fill:#fff;opacity:.8}}
.s-fireglow{{fill:url(#fireG)}} .s-keyhole{{fill:#ffcf6b}} .s-doorlight{{fill:url(#doorLight)}}
.s-ice{{fill:#bfe9f5;fill-opacity:.55;stroke:#d8f6ff;stroke-width:1.5}} .s-icehl{{stroke:#fff;stroke-width:2.5;fill:none}}
.s-key{{fill:#ffcf6b;stroke:#ffcf6b}} .s-vignette{{opacity:.25}}
'''
CHAR_COLOR = scope(ANIME_CSS + "#side_face_sil{display:none} #side_hair_back{display:none} #side_hair_back_cel{display:none} #side_skullhair{display:none}", "body.color #player")
CHAR_DARK = scope(anime_dark.css + "#side_hair_back{display:none} #side_bangs{display:none} #side_face{display:none} #side_skullhair{display:none}", "body.dark #player")
SC_COLOR = scope(SCENE_COLOR, "body.color #scene")
SC_DARK = scope(SCENE_DARK, "body.dark #scene")
OUTLINED = ["s-wood","s-woodd","s-stone","s-stone2","s-metal","s-metald","s-candle","s-board","s-book1","s-book2",
            "s-book3","s-pot","s-lid","s-coal","s-glass","s-owl","s-crystal","s-leaf","s-owleye","s-ice","s-flower"]
SC_DARK += "\n" + ", ".join(f"body.nolines #scene .{c}" for c in OUTLINED) + "{stroke:none}"

# Frontansicht: Beine einzeln gruppieren (nur Struktur, Aussehen unverändert) für die Lauf-Animation nach vorn
FRONT = BODY2
for _s in ("l", "r"):
    _p = _front_leg(_s)
    assert _p in FRONT
    FRONT = FRONT.replace(_p, f'<g id="front_leg_{_s}">{_p}</g>', 1)
HTML = open("scene_template.html").read()
HTML = (HTML.replace("/*CHAR_COLOR*/", CHAR_COLOR).replace("/*CHAR_DARK*/", CHAR_DARK)
            .replace("/*SC_COLOR*/", SC_COLOR).replace("/*SC_DARK*/", SC_DARK)
            .replace("<!--DEFS-->", DEFS + ANIME_DEFS).replace("<!--SCENE-->", SCENE)
            .replace("<!--PLAYER-->", FRONT + SIDE + BACK))
open("alchemieschule_demo.html", "w").write(HTML)
print("ok", len(HTML) // 1024, "KB")
