from gen import STYLES, spark
from anime2 import BODY2
sil = STYLES["silhouette"]
css = sil["css"] + '''
.eyewhite,.iris,.pupil,.irisshadow,.irisglow,.crease,.lash,.lowlash,.brow2,.hairshine,.hairline,.cel,.mouthline,.blushline{display:none}
.hl{fill:#ffcf6b}.lensshine{fill:#fff3d0}.sparkle{fill:#fff1c4}
.lens{fill:#ffcf6b}
.skin,.hair,.cap,.capdark,.blouse,.jabot,.strap,.corset,.corsetpanel,.skirt1,.skirt2,.bloomers,.stocking,.boot,.bootdark,.pouch,.brass,.cork,.gem{stroke:#140e10;stroke-width:1.2}
'''
sparks = spark(330, 140, 9) + spark(318, 214, 5) + spark(250, 140, 5)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 800" width="400" height="800">
<title>Alchemistin – Anime-Proportionen im Scherenschnitt-Stil</title>
<defs>{sil["defs"]}</defs>
<style>{css}</style>
<g id="background">{sil["bg"]}</g>
{BODY2}
<g id="fx">{sparks}</g>
</svg>'''
open("alchemistin_anime_dunkel.svg","w").write(svg)
