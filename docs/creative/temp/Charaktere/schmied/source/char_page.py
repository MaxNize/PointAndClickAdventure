"""Vorschau-Seite: Lehrling läuft im Lehrsaal (gleiche Laufanimation wie in der Demo)."""
import re, base64, subprocess, sys, io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import build_scene as B
from gen import ANIME_CSS, ANIME_DEFS
import anime_dark, importlib
MOD, PREFIX, TITLE = sys.argv[1], sys.argv[2], sys.argv[3]
boy = importlib.import_module(MOD)
CSS_C = getattr(boy, "BOY_CSS", None) or getattr(boy, "M_CSS", None) or getattr(boy, "E_CSS", None) or boy.S_CSS
CSS_D = getattr(boy, "BOY_DARK", None) or getattr(boy, "M_DARK", None) or getattr(boy, "E_DARK", None) or boy.S_DARK
DEFS_X = getattr(boy, "BOY_DEFS", None) or getattr(boy, "M_DEFS", None) or getattr(boy, "E_DEFS", None) or boy.S_DEFS
import json
WALK_JSON = json.dumps(getattr(boy, "WALK_STYLE", {}))

tpl = open("scene_template.html").read()
walk_js = tpl[tpl.index("/* ---------- Laufen ----------"):tpl.index("/* ---------- Interaktion ohne Gegenstand ---------- */")]

CHAR_C = B.scope(ANIME_CSS + CSS_C, "body.color #player")
CHAR_D = B.scope(anime_dark.css + CSS_D, "body.dark #player")

def thumb(view, style):
    data = open(f"{PREFIX}_{view}_{style}.svg","rb").read()
    return "data:image/svg+xml;base64," + base64.b64encode(data).decode()

thumbs = "".join(
    f'<figure><img src="{thumb(v,"scherenschnitt")}" alt="{n}"><img class="c" src="{thumb(v,"farbe")}" alt="{n} farbig"><figcaption>{n}</figcaption></figure>'
    for v, n in (("front","Vorne"),("seite","Seite"),("rueck","Hinten")))

html = f'''<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE} – Charakter &amp; Laufanimation</title>
<style>
:root{{--gold:#e0ad4a;--cream:#f6ecd8}}
*{{box-sizing:border-box}} html,body{{margin:0;background:#140e10;color:var(--cream);font-family:Georgia,serif}}
#app{{max-width:1280px;margin:0 auto;padding:10px}}
header{{display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:6px 4px 10px}}
h1{{font-size:18px;margin:0;color:var(--gold)}} .hint{{flex:1;font-size:13px;opacity:.8;min-width:200px}}
button{{font:inherit;font-size:13px;color:var(--cream);background:#3b2620;border:1px solid #6b4836;border-radius:8px;padding:6px 12px;cursor:pointer}}
button:hover{{border-color:var(--gold)}}
#stage{{position:relative;width:100%;aspect-ratio:16/9;border-radius:10px;overflow:hidden;box-shadow:0 6px 30px #000}}
#stage svg{{display:block;width:100%;height:100%;cursor:crosshair}}
.sheet{{display:flex;gap:12px;justify-content:center;margin-top:12px;flex-wrap:wrap}}
figure{{margin:0;background:#2a1a14;border:1px solid #5a3a2c;border-radius:10px;padding:8px;text-align:center}}
figure img{{height:260px;display:block}} figure img.c{{display:none}} body.color figure img{{display:none}} body.color figure img.c{{display:block}}
figcaption{{font-size:13px;color:var(--gold);margin-top:4px}}
#player{{pointer-events:none}}
.bub{{animation:bub 1.6s infinite ease-in}}.b2{{animation-delay:.5s}}.b3{{animation-delay:1s}}
@keyframes bub{{0%{{transform:translateY(0);opacity:0}}20%{{opacity:.9}}100%{{transform:translateY(-34px);opacity:0}}}}
.flicker{{animation:fl .35s infinite alternate;transform-box:fill-box;transform-origin:50% 100%}}
@keyframes fl{{from{{transform:scaleY(1)}}to{{transform:scaleY(1.12) scaleX(.94)}}}}
.blink{{animation:blink 5s infinite;transform-box:fill-box;transform-origin:50% 50%}}
@keyframes blink{{0%,94%,100%{{transform:scaleY(1)}}96%{{transform:scaleY(.1)}}}}
{CHAR_C}
{CHAR_D}
{B.SC_COLOR}
{B.SC_DARK}
</style></head>
<body class="dark nolines"><div id="app">
<header><h1>⚗ {TITLE} – Charakter &amp; Laufanimation</h1>
<div class="hint">Klick auf den Boden, um ihn laufen zu lassen (auch nach vorn und hinten).</div>
<button id="btnTour">▶ Demo-Runde</button><button id="btnStyle">Farbversion ansehen</button></header>
<div id="stage"><svg id="svg" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
<defs>{B.DEFS}{ANIME_DEFS}{DEFS_X}</defs>
{B.SCENE}
<g id="player" transform="translate(640,690)"><g id="flip" transform="scale(0.5,0.5)"><g id="bob"><g transform="translate(-200,-773)">
{boy.FRONT}{boy.SIDE}{boy.BACK}
</g></g></g></g>
</svg></div>
<div class="sheet">{thumbs}</div>
</div>
<script>
const $ = s => document.querySelector(s);
const svg = $('#svg');
const S = {{x:640, y:690, dir:1, pose:'idle', walking:false}};
window.WALK_STYLE = {WALK_JSON};
function svgPoint(e){{ const p = svg.createSVGPoint(); p.x=e.clientX; p.y=e.clientY; return p.matrixTransform(svg.getScreenCTM().inverse()); }}
{walk_js}
svg.addEventListener('click', e => {{ tour = null; const p = svgPoint(e); walkTo(p.x, null, p.y >= 600 ? p.y : null); }});
let tour = null;
const ROUTE = [[1000,690],[1000,648],[300,648],[300,702],[640,690]];
function runTour(i=0){{ if(tour===null) return; if(i>=ROUTE.length){{ tour=null; return; }} walkTo(ROUTE[i][0], ()=>setTimeout(()=>runTour(i+1),350), ROUTE[i][1]); }}
$('#btnTour').onclick = () => {{ tour = 1; runTour(0); }};
$('#btnStyle').onclick = () => {{
  const c = document.body.classList.toggle('color'); document.body.classList.toggle('dark', !c); document.body.classList.toggle('nolines', !c);
  $('#btnStyle').textContent = c ? 'Scherenschnitt ansehen' : 'Farbversion ansehen';
}};
setPose('idle');
setTimeout(()=>{{ tour = 1; runTour(0); }}, 600);
</script></body></html>'''
open(f"{PREFIX}_vorschau.html","w").write(html)
print("ok", len(html)//1024, "KB")
