"""Rückansicht der Alchemistin (Blick von hinten) für das Laufen nach hinten in den Raum.
Gleiches Koordinatensystem wie Front- und Seitenansicht (400x800, Füße bei y≈773),
gleiche CSS-Klassen -> funktioniert im Farb- und im Scherenschnitt-Stil.
Animierbare Gruppen: back_leg_l/back_leg_r (Bein + Stiefel), back_arm_l/back_arm_r (Pivot an der Schulter)."""
from gen import scallop
from anime2 import leg as front_leg, boot as front_boot

def back_leg(side):
    s = front_leg(side) + front_boot(side).replace('id="boot_', 'id="back_boot_')
    # Absatz von hinten sichtbar
    x = 176 if side == "l" else 212
    s += f'<rect class="bootdark" x="{x}" y="756" width="12" height="17" rx="2"/>'
    return f'<g id="back_leg_{side}">{s}</g>'

def back_arm(side, flask=False):
    m = 1 if side == "l" else -1
    X = lambda x: x if m == 1 else 400 - x
    puff = (f'M{X(172)},222 C{X(150)},220 {X(140)},242 {X(143)},266 L{X(147)},292 L{X(167)},292 '
            f'C{X(170)},268 {X(173)},246 {X(178)},232 Z')
    lower = f'M{X(146)},286 L{X(166)},286 L{X(164)},356 L{X(150)},356 Z'
    s = f'<g id="back_arm_{side}"><g transform="rotate({8*m} {X(168)} 230)">'
    s += f'<path class="blouse" d="{lower}"/>'
    s += f'<path class="shade" d="M{X(146)},286 L{X(152)},286 L{X(152)},356 L{X(150)},356 Z"/>'
    a, b = sorted((X(146), X(168)))
    s += f'<path class="jabot" d="M{a},352 L{b},352 L{b+1},364{scallop(b+1, a-1, 364, 3, 4)} Z"/>'
    s += f'<ellipse class="skin" cx="{X(157)}" cy="373" rx="9" ry="11"/>'
    if flask:
        cx = X(158)
        s += (f'<circle class="glow" cx="{cx}" cy="398" r="21"/>'
              f'<rect class="vialglass" x="{cx-4}" y="374" width="8" height="13" rx="1"/>'
              f'<rect class="cork" x="{cx-5}" y="370" width="10" height="6" rx="1"/>'
              f'<circle class="vialglass" cx="{cx}" cy="398" r="11.5"/>'
              f'<path class="liquid" d="M{cx-11.5},399 Q{cx-6},396 {cx},399 Q{cx+6},402 {cx+11.5},399 A11.5,11.5 0 0 1 {cx-11.5},399 Z"/>')
    s += f'<path class="blouse" d="{puff}"/>'
    s += f'<path class="line" d="M{X(156)},236 Q{X(152)},256 {X(156)},280"/>'
    s += '</g></g>'
    return s

def lacing_back():
    s = ""
    for y in range(268, 316, 7):
        s += f'<path class="lace" d="M194,{y} L206,{y+7} M206,{y} L194,{y+7}"/>'
    return s

def bob_tips(y0=208):
    pts = []
    x = 132
    up = True
    while x <= 268:
        pts.append(f"L{x},{y0 + (0 if up else 11)}")
        x += 8
        up = not up
    return " ".join(pts)

BACK = f'''
<g id="characterBack" style="display:none">
  <ellipse class="groundshadow" cx="200" cy="772" rx="62" ry="7"/>


  <g id="back_legs">{back_leg("l")}{back_leg("r")}</g>

  <g id="back_skirt">
    <path class="bloomers" d="M168,366 L232,366 L236,408{scallop(236,164,408,7,5)} Z"/>
    <path class="skirt2" d="M170,330 L230,330 C250,350 262,372 272,396{scallop(272,128,396,10,8)} C138,372 150,350 170,330 Z"/>
    <path class="skirt1" d="M176,312 Q200,318 224,312 C240,332 250,352 258,372{scallop(258,142,372,9,7)} C150,352 160,332 176,312 Z"/>
    <path class="line" d="M186,322 Q182,346 174,368 M200,324 L200,372 M214,322 Q218,346 226,368"/>
  </g>

  <g id="back_torso">
    <rect class="skin" x="193" y="190" width="14" height="34"/>
    <path class="blouse" d="M167,222 Q200,213 233,222 C237,240 235,255 230,268 L170,268 C165,255 163,240 167,222 Z"/>
    <path class="shade" d="M167,222 L176,220 C172,238 172,254 176,268 L170,268 C165,255 163,240 167,222 Z"/>
    <path class="line" d="M200,224 L200,262"/>
    <path class="corset" d="M171,262 Q200,255 229,262 L231,286 Q222,300 225,318 Q200,325 175,318 Q178,300 169,286 Z"/>
    <path class="corsetpanel" d="M192,260 L208,260 L208,322 L192,322 Z"/>
    {lacing_back()}
    <path class="lace" d="M200,316 Q192,322 188,330 M200,316 Q208,322 212,330"/>
    <circle class="brass" cx="200" cy="316" r="2.6"/>
    <path class="strap" d="M178,221 L186,220 L214,262 L206,264 Z"/>
    <path class="strap" d="M222,221 L214,220 L186,262 L194,264 Z"/>
    <circle class="brass" cx="200" cy="242" r="5"/><circle class="corset" cx="200" cy="242" r="2.2"/>
    <path class="strap" d="M174,312 Q200,322 226,312 L227,320 Q200,330 173,320 Z"/>
    <rect class="pouch" x="159" y="316" width="19" height="19" rx="3"/>
    <path class="bootdark" d="M159,316 L178,316 L178,323 L159,323 Z"/>
  </g>

  <!-- Schleppe hängt hinten und liegt von hinten gesehen vorne -->
  <g id="back_train">
    <path class="skirtback" d="M178,318 C136,380 112,500 96,640 Q128,608 150,662 Q176,614 200,656 Q224,614 250,662 Q272,608 304,640 C288,500 264,380 222,318 Z"/>
    <path class="shade" d="M200,330 C206,420 214,540 218,640 Q208,618 200,656 C198,540 198,420 200,330 Z"/>
  </g>

  {back_arm("l")}
  {back_arm("r", flask=True)}

  <g id="back_head">
    <path class="skin" d="M158,130 C158,104 178,92 200,92 C222,92 242,104 242,130 L242,180 C232,196 168,196 158,180 Z"/>
    <g id="back_hair">
      <path class="hair" d="M150,112 C134,140 130,170 132,208 {bob_tips()} C270,170 266,140 250,112 Z"/>
      <path class="hairshine" d="M150,140 Q146,160 147,184 L151,174 Q152,156 155,144 Z"/>
      <path class="hairshine" d="M245,140 Q249,160 248,180 L245,171 Q244,155 241,144 Z"/>
      <path class="hairline" d="M166,124 C162,150 160,176 160,204 M184,120 C182,148 181,176 182,204 M200,118 L200,206 M216,120 C218,148 219,176 218,204 M234,124 C238,150 240,176 240,204"/>
    </g>
    <g id="back_cap" transform="rotate(4 200 100)">
      <ellipse class="cap" cx="200" cy="96" rx="70" ry="32"/>
      <path class="cel" d="M132,100 Q200,128 268,100 Q270,88 262,80 Q200,108 138,80 Q130,88 132,100 Z"/>
      <path class="line" d="M200,64 L200,108 M200,64 Q178,80 150,104 M200,64 Q222,80 250,104"/>
      <path class="capdark" d="M132,104 Q200,124 268,104 Q270,120 200,128 Q130,120 132,104 Z"/>
      <circle class="capdark" cx="200" cy="65" r="5"/>
      <path class="strap" d="M130,94 Q200,110 270,94 L270,102 Q200,118 130,102 Z"/>
      <rect class="buckle" x="194" y="104" width="12" height="9" rx="2"/>
    </g>
  </g>
</g>
'''

if __name__ == "__main__":
    from gen import ANIME_CSS, ANIME_DEFS
    import anime_dark
    for name, css in (("color", ANIME_CSS), ("dark", anime_dark.css)):
        body = BACK.replace('style="display:none"', '')
        bg = '<rect width="400" height="800" fill="#e9dcc8"/>' if name == "color" else '<rect width="400" height="800" fill="#a8604e"/>'
        open(f"back_{name}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 800" width="400" height="800"><defs>{ANIME_DEFS}</defs><style>{css}</style>{bg}{body}</svg>')
    print("back ok")
