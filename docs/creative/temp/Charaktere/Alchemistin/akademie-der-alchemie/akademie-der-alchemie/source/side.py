"""Seitenansicht (Profil, Blick nach rechts) der Alchemistin für den Laufzyklus.
Gleiches Koordinatensystem wie die Frontansicht (400x800, Füße bei y≈770),
gleiche CSS-Klassen -> funktioniert mit Farb- und Scherenschnitt-Stil.
Gelenke: Beine drehen um die Hüfte (205,352), Arme um die Schulter (205,232)."""
from gen import scallop

KNEE = (206, 550)
ELBOW = (204, 288)

def leg(gid, far=False):
    thigh = 'M188,352 C184,430 190,500 195,550 L216,553 C220,500 224,430 222,352 Z'
    shin = 'M196,546 C189,600 194,680 199,745 L213,745 C216,690 219,620 216,553 Z'
    boot = ('M189,572 L222,572 L220,594 C218,650 217,700 216,738 L240,750 Q248,758 242,768 '
            'L198,768 L194,760 L192,742 C191,700 190,650 191,594 Z')
    s = f'<g id="{gid}">'
    s += f'<path class="stocking" d="{thigh}"/>'
    s += '<path class="shade" d="M188,352 C184,430 190,500 195,550 L201,550 C197,500 194,430 196,352 Z"/>'
    if far: s += f'<path class="shade" d="{thigh}"/>'
    s += f'<g id="{gid}_shin">'
    s += f'<circle class="stocking" cx="{KNEE[0]}" cy="{KNEE[1]}" r="10.5"/>'
    s += f'<path class="stocking" d="{shin}"/>'
    s += '<path class="shade" d="M196,546 C189,600 194,680 199,745 L204,745 C201,680 197,600 202,546 Z"/>'
    s += f'<path class="boot" d="{boot}"/>'
    s += '<path class="bootdark" d="M186,564 L225,564 L222,590 L189,590 Z"/>'
    s += '<path class="strap" d="M190,644 L219,638 L219,645 L190,651 Z"/><rect class="buckle" x="202" y="637" width="7" height="9" rx="1"/>'
    s += '<path class="strap" d="M191,704 L218,698 L218,705 L191,711 Z"/><rect class="buckle" x="202" y="697" width="7" height="9" rx="1"/>'
    s += '<rect class="bootdark" x="194" y="756" width="13" height="12"/>'
    if far: s += f'<circle class="shade" cx="{KNEE[0]}" cy="{KNEE[1]}" r="10.5"/><path class="shade" d="{shin}"/><path class="shade" d="{boot}"/>'
    s += '</g></g>'
    return s

def arm(gid, far=False, flask=False):
    puff = 'M188,226 C176,240 178,272 192,290 L216,290 C228,272 228,240 214,226 Z'
    lower = 'M194,284 L214,284 L212,372 L198,372 Z'
    s = f'<g id="{gid}">'
    s += f'<g id="{gid}_fore">'
    s += f'<path class="blouse" d="{lower}"/>'
    s += '<path class="shade" d="M194,284 L200,284 L200,372 L198,372 Z"/>'
    s += f'<path class="jabot" d="M194,368 L216,368 L217,380{scallop(217,193,380,3,4)} Z"/>'
    s += '<ellipse class="skin" cx="205" cy="389" rx="9" ry="11"/>'
    if flask:
        s += ('<circle class="glow" cx="206" cy="414" r="21"/>'
              '<rect class="vialglass" x="202" y="390" width="8" height="13" rx="1"/>'
              '<rect class="cork" x="201" y="386" width="10" height="6" rx="1"/>'
              '<circle class="vialglass" cx="206" cy="414" r="11.5"/>'
              '<path class="liquid" d="M194.5,415 Q200,412 206,415 Q212,418 217.5,415 A11.5,11.5 0 0 1 194.5,415 Z"/>')
    if far: s += f'<path class="shade" d="{lower}"/>'
    s += '</g>'
    s += f'<path class="blouse" d="{puff}"/>'
    if far: s += f'<path class="shade" d="{puff}"/>'
    s += '</g>'
    return s

def jabot_side():
    s = ""
    for y in (200, 213, 226):
        s += (f'<path class="jabot" d="M221,{y} Q229,{y-4} 233,{y} L235,{y+10}'
              f'{scallop(235, 221, y+10, 2, 3)} Z"/>')
    return s

def lacing_side():
    return "".join(f'<path class="lace" d="M223,{y} L229,{y+6}"/>' for y in range(266, 318, 7))

EYE_WHITE = "M226,150 Q234,144 242,150 Q241,160 233,161 Q227,159 226,150 Z"

SIDE = f'''
<g id="characterSide" style="display:none">
  <ellipse class="groundshadow" cx="210" cy="772" rx="46" ry="6"/>

  <path class="skirtback" d="M186,322 C150,384 110,486 68,624 Q100,602 120,646 Q140,604 162,634 C178,522 198,420 216,330 Z"/>
  <path class="shade" d="M186,322 C150,384 110,486 68,624 Q100,602 120,646 L130,560 C150,470 170,400 196,330 Z"/>

  {arm("side_arm_far", far=True)}
  {leg("side_leg_far", far=True)}

  <path id="side_hair_back" class="hair" d="M206,98 C164,98 142,124 142,170 C140,232 130,282 114,318 L132,302 L134,328 L150,298 L160,314 C170,272 178,222 188,182 C194,162 210,142 216,122 Z"/>
  <path id="side_hair_back_cel" class="cel" d="M142,190 C140,240 132,284 118,314 L132,302 L134,328 L146,292 C150,260 152,226 152,196 Z"/>

  {leg("side_leg_near")}

  <g id="side_torso">
    <rect class="skin" x="196.3" y="184" width="18.3" height="40"/>
    <path class="shade" d="M196,184 L213,184 L213,200 Q205,206 196,200 Z"/>
    <path class="blouse" d="M188,222 C178,240 176,264 182,290 L226,290 C232,272 234,250 228,232 Q218,220 205,218 Z"/>
    <path class="shade" d="M188,222 C178,240 176,264 182,290 L192,290 C188,266 188,242 196,222 Z"/>
    {jabot_side()}
    <path class="strap" d="M205,221 L212,221 L215,264 L208,264 Z"/>
    <path class="corset" d="M180,262 Q206,256 229,262 L230,290 Q225,305 227,322 Q204,328 183,322 Q185,305 180,290 Z"/>
    <path class="corsetpanel" d="M221,262 L229,262 L230,290 Q225,305 227,322 L221,323 Z"/>
    {lacing_side()}
    <path class="shade" d="M180,262 L190,261 Q188,292 192,324 L183,322 Q185,305 180,290 Z"/>
    <path class="strap" d="M182,314 Q205,322 228,314 L229,322 Q205,330 181,322 Z"/>
    <rect class="pouch" x="172" y="316" width="18" height="20" rx="3"/>
    <path class="bootdark" d="M172,316 L190,316 L190,323 L172,323 Z"/>
  </g>

  <g id="side_skirt">
    <path class="bloomers" d="M178,366 L234,366 L238,406{scallop(238,174,406,6,5)} Z"/>
    <path class="skirt2" d="M180,330 L232,330 C248,352 256,374 262,396{scallop(262,150,396,9,8)} C156,372 166,352 180,330 Z"/>
    <path class="shade" d="M180,330 L192,330 C180,352 172,374 166,396 Q158,404 150,396 C156,372 166,352 180,330 Z"/>
    <path class="skirt1" d="M182,314 Q206,320 229,314 C241,334 249,354 255,372{scallop(255,158,372,8,7)} C164,352 172,332 182,314 Z"/>
    <path class="line" d="M196,322 Q190,346 182,370 M214,322 Q220,346 228,370"/>
  </g>

  {arm("side_arm_near", flask=True)}

  <g id="side_head">
    <path id="side_face" class="skin" d="M162,140 C162,102 186,96 200,96.5 C215,96.8 230,104 239,114 C243,119 245,124 245.4,130 L245.7,142 C245.4,146 244,148 243.9,150 C244.5,152 246,153.5 248,154.6 C251,156 254.5,157.4 256.5,158.8 L256.8,162 C256.6,164 256,166 254.8,168 C254.2,170 254.1,172 254.1,176 C254,178 252.8,179.5 251.5,180.4 C250.6,181.2 250,182 250,184 C249.6,185.6 248.9,186.6 248.8,188 L248.6,194 C248.4,196.5 248,198 246.5,199.4 C245.3,200.1 243,200.2 240,200.2 L230,199.4 C222,198.5 214,197.2 210,195.6 C206,194 203.5,191.5 201.5,188 C200,185 199,183 197.5,182 C190,184 176,178 168,166 C162,158 162,150 162,140 Z"/><path id="side_face_sil" class="skin" d="M162,140 C162,102 186,96 200,96.5 C215,96.8 230,104 239,114 C243,118 246.5,122 247,128 L247,139 L245.6,140.5 L245.6,147.5 C246.5,149.5 248.5,150.6 251,151.4 L256.5,152.6 C257.8,153.1 258.4,154 258.4,155 L258.4,158.5 C258.2,159.4 257.2,159.8 256.9,160.5 L256.9,163 C256.6,163.7 255.6,164 255.5,165 L255.5,171 C255.3,172 254.3,172.3 254.1,173.2 L254,174.4 C253.4,175.2 252.8,175.6 252.4,176.3 C251.8,177 251.4,177.6 251.3,178.6 C251,179.4 250.1,179.6 249.9,180.6 L249.9,188.4 C249.6,189.2 248.6,189.6 248.4,190.6 C248.2,191.8 247.5,192.6 246.2,193.1 C244,193.6 240,193.6 236,193.4 L231,193.1 C227,192.6 223,191.6 220.3,190.9 L214.6,190.3 L196.3,190.3 L196.3,185 C190,184 176,178 168,166 C162,158 162,150 162,140 Z"/><g id="side_bob"><path class="hair" d="M149.2,215.1 L147.3,213.5 L144.6,208.9 L143.2,207.5 L140.1,210.8 L138.2,209.2 L138.5,190.7 L140.0,172.3 L141.0,146.8 L142.0,138.7 L143.8,131.4 L146.8,123.1 L150.9,114.5 L152.5,112.9 L153.3,112.9 L158.3,115.4 L161.1,116.1 L163.1,118.2 L164.4,117.2 L171.4,118.9 L175.7,119.4 L179.2,122.2 L181.0,120.4 L191.9,121.4 L195.9,121.4 L197.9,121.7 L201.4,124.7 L204.2,121.9 L204.7,121.9 L206.2,123.2 L208.2,121.2 L208.8,121.4 L210.0,120.4 L212.0,120.2 L213.5,119.4 L215.3,119.7 L220.9,117.7 L221.9,117.9 L224.6,116.9 L226.2,117.2 L227.2,116.1 L231.2,115.1 L233.5,114.1 L236.0,113.9 L237.0,114.9 L238.0,113.9 L242.8,113.6 L246.8,113.1 L248.1,112.6 L249.1,113.4 L250.1,112.4 L253.4,112.1 L254.7,111.6 L256.2,113.1 L257.7,111.6 L259.5,111.6 L261.7,112.4 L263.7,113.6 L267.2,117.0 L267.2,124.9 L265.5,126.5 L264.0,126.0 L260.7,125.7 L259.0,126.0 L257.3,127.4 L257.6,132.9 L262.4,136.7 L265.6,141.0 L265.9,142.3 L264.3,143.9 L261.5,142.1 L258.2,141.1 L255.2,143.7 L252.8,140.8 L253.5,139.7 L252.4,138.6 L250.5,140.0 L248.5,146.8 L246.6,148.7 L245.0,147.1 L242.2,138.0 L241.2,137.0 L242.4,134.9 L242.2,133.7 L239.8,131.3 L238.8,132.0 L236.8,132.0 L233.2,133.1 L232.7,133.6 L232.2,133.6 L231.2,132.6 L229.8,133.9 L229.6,134.7 L231.0,136.6 L231.8,136.7 L229.7,136.6 L225.7,141.1 L223.8,139.2 L222.8,137.0 L221.6,135.8 L220.9,135.3 L219.5,136.7 L218.2,142.3 L217.7,149.6 L217.2,150.1 L217.5,151.4 L217.0,151.9 L218.0,156.9 L218.7,166.8 L218.2,179.1 L217.2,186.2 L215.9,191.7 L213.7,194.0 L215.1,195.4 L215.3,195.2 L216.6,196.7 L217.3,196.7 L217.5,197.0 L217.0,198.3 L215.4,199.6 L215.4,201.1 L213.8,202.7 L213.0,202.2 L208.2,208.3 L206.4,204.9 L204.2,202.5 L197.0,210.4 L196.9,211.6 L195.5,210.2 L195.5,206.1 L195.0,204.6 L193.4,203.0 L189.0,207.4 L186.6,210.6 L185.4,209.4 L184.7,207.7 L183.0,206.3 L181.6,207.9 L181.1,210.4 L179.0,212.3 L173.7,207.5 L172.2,207.0 L164.9,214.8 L157.8,207.8 L156.5,207.5 L149.2,215.1 Z"/><path class="hairshine" d="M150.5,146 Q147,162 146.5,180 L150.5,171 Q151.5,158 153.5,149 Z"/><path class="hairline" d="M162,138 C158,162 156,184 155,205 M177,134 C174,158 172,182 171,204 M192,134 C190,156 189,178 188,200 M206,132 C205,152 205,172 204,192"/></g>
    
    <ellipse class="blush" cx="237" cy="167" rx="7.5" ry="3.3"/>
    <g id="side_eye">
      <ellipse class="iris" cx="231.2" cy="152.2" rx="3" ry="7.8"/>
      <ellipse class="irisglow" cx="231.2" cy="157" rx="2" ry="2.2"/>
      <ellipse class="pupil" cx="231.1" cy="153.4" rx="1.4" ry="3.4"/>
      <ellipse class="hl" cx="231.2" cy="149.3" rx="1.5" ry="3"/><circle class="hl" cx="226.6" cy="157.8" r="1.15"/>
      <ellipse class="lowlash" cx="231.2" cy="152.2" rx="3" ry="7.8"/>
      <path class="lash" d="M236.4,141.6 Q229,138.4 224.8,142.4 Q221,146.6 219,153.6"/>
      <path class="lowlash" d="M222,157.6 Q225.5,160.3 228.6,161.2"/>
    </g>
    <path class="mouthline" d="M248.6,180.2 L243,180.1 Q241,180.4 240.2,181.7"/>
    <!-- Haare -->
    <g id="side_bangs">
      <path class="cel" d="M245.6,128 L245.6,149 L242.5,151 L238.5,140 L232.5,147.5 L227.5,136 L220.5,144 L215,131 Z"/>
      <path class="hair" d="M252,121 C259,117.5 265.5,120.5 268.5,127.5 C262.5,124.5 258.5,125 254.5,128 Z"/>
      <path class="hair" d="M256.5,133.5 C262.5,135 266,140 266.5,146.5 C263,142 259.6,140.8 256.2,141 Z"/>
      <path class="hair" d="M162,142 C158,102 196,86 222,92 C240,96 252,106 255.5,118 C257.6,127 257.6,136 256.6,142 L258.6,150.5 L251,137.5 L246.6,151.5 L241,134 L236.6,146.5 L231,131 L225.6,142.5 L219,129 C208,128 198,130 188,140 L178,128 L170,146 Z"/>
      <path class="hairshine" d="M234,116 Q245,113 252.5,121 L249.5,123.5 Q243,118.5 236,120 Z"/>
      <path class="hairshine" d="M243,128 Q249,130 251.5,137.5 L248.6,136 Q246,131.6 243,130.6 Z"/>
      <path class="hairline" d="M244,108 Q251,124 252.6,140 M232,112 Q238,124 240,133 M221,114 Q226,123 227,129"/>
    </g>
    
    
    <g id="side_brow"><path class="brow2" d="M229,136.4 Q233,132.4 239,132.2 Q242.5,132.7 241.8,135.5 Q240.6,137.1 237.6,136.7 Q233,136.3 229,136.4 Z"/></g>
    <!-- Mütze im Profil -->
    <g id="side_cap" transform="rotate(-6 206 100)">
      <ellipse class="cap" cx="204" cy="98" rx="60" ry="30"/>
      <path class="cel" d="M146,104 Q204,126 262,104 Q266,92 258,84 Q204,108 144,90 Z"/>
      <path class="line" d="M204,68 Q184,82 160,104 M204,68 Q224,82 246,104"/>
      <path class="capdark" d="M222,110 Q266,104 280,118 Q256,128 222,124 Z"/>
      <path class="capdark" d="M146,106 Q204,124 262,108 Q264,120 204,130 Q146,122 146,106 Z"/>
      <circle class="capdark" cx="204" cy="69" r="5"/>
      <path class="strap" d="M144,96 Q204,82 264,96 L264,104 Q204,90 144,104 Z"/>
      <circle class="brass" cx="244" cy="94" r="13"/>
      <ellipse class="lens" cx="245" cy="94" rx="6" ry="9"/>
      <path class="lensshine" d="M241,89 L245,86 L247,88 L243,92 Z"/>
    </g>
  </g>
</g>
'''

if __name__ == "__main__":
    from gen import ANIME_CSS, ANIME_DEFS
    import anime_dark
    for name, css in (("color", ANIME_CSS+"#side_face_sil,#side_hair_back,#side_hair_back_cel{display:none}"), ("dark", anime_dark.css+"#side_hair_back,#side_bangs,#side_face,#side_skullhair{display:none}")):
        body = SIDE.replace('style="display:none"', '')
        # Beispiel-Schrittstellung
        body = body.replace('<g id="side_leg_far">', '<g id="side_leg_far" transform="rotate(-12 205 352)">')
        body = body.replace('<g id="side_leg_near">', '<g id="side_leg_near" transform="rotate(12 205 352)">')
        body = body.replace('<g id="side_leg_far_shin">', '<g id="side_leg_far_shin" transform="rotate(4 206 550)">')
        body = body.replace('<g id="side_leg_near_shin">', '<g id="side_leg_near_shin" transform="rotate(22 206 550)">')
        body = body.replace('<g id="side_arm_near_fore">', '<g id="side_arm_near_fore" transform="rotate(-18 204 288)">')
        body = body.replace('<g id="side_arm_far_fore">', '<g id="side_arm_far_fore" transform="rotate(-10 204 288)">')
        body = body.replace('<g id="side_arm_far">', '<g id="side_arm_far" transform="rotate(16 205 232)">')
        body = body.replace('<g id="side_arm_near">', '<g id="side_arm_near" transform="rotate(-16 205 232)">')
        bg = '<rect width="400" height="800" fill="#e9dcc8"/>' if name == "color" else '<rect width="400" height="800" fill="#a8604e"/>'
        open(f"side_{name}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 800" width="400" height="800"><defs>{ANIME_DEFS}</defs><style>{css}</style>{bg}{body}</svg>')
    print("side ok")
