"""Vorschau: alle 10 NPCs – auswählen, laufen lassen, ansprechen."""
import json, base64, io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import build_scene as B
    import npc
from gen import ANIME_CSS, ANIME_DEFS
import anime_dark

tpl = open("scene_template.html").read()
walk_js = tpl[tpl.index("/* ---------- Laufen ----------"):tpl.index("/* ---------- Interaktion ohne Gegenstand ---------- */")]

css_c = B.scope(ANIME_CSS, "body.color #player")
for n in npc.NPCS:
    css_c += "\n" + B.scope(npc.color_css(n["colors"]), f"body.color #player.npc-{n['id']}")
css_d = B.scope(anime_dark.css + npc.NPC_DARK, "body.dark #player")

data = {}
for n in npc.NPCS:
    F, S, Bk = npc.build(n)
    w = {k: v for k, v in n["walk"].items() if k != "hip"}
    data[n["id"]] = dict(name=n["name"], role=n["role"], lines=n["lines"], walk=w, markup=F + S + Bk)

def thumb(nid, style):
    return "data:image/svg+xml;base64," + base64.b64encode(open(f"npc_{nid}_front_{style}.svg", "rb").read()).decode()
thumbs = "".join(
    f'<button class="th" data-id="{n["id"]}"><img src="{thumb(n["id"],"scherenschnitt")}"><img class="c" src="{thumb(n["id"],"farbe")}">'
    f'<span>{n["name"]}</span><small>{n["role"]}</small></button>' for n in npc.NPCS)

html = f'''<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>NPCs – Nebenfiguren der Akademie</title>
<style>
:root{{--gold:#e0ad4a;--cream:#f6ecd8}}*{{box-sizing:border-box}}
html,body{{margin:0;background:#140e10;color:var(--cream);font-family:Georgia,serif}}
#app{{max-width:1280px;margin:0 auto;padding:10px}}
header{{display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:6px 4px 10px}}
h1{{font-size:18px;margin:0;color:var(--gold)}}.hint{{flex:1;font-size:13px;opacity:.8;min-width:200px}}
button{{font:inherit;font-size:13px;color:var(--cream);background:#3b2620;border:1px solid #6b4836;border-radius:8px;padding:6px 12px;cursor:pointer}}
button:hover{{border-color:var(--gold)}}
#stage{{position:relative;width:100%;aspect-ratio:16/9;border-radius:10px;overflow:hidden;box-shadow:0 6px 30px #000}}
#stage svg{{display:block;width:100%;height:100%;cursor:crosshair}}
#bubble{{position:absolute;max-width:320px;background:#1d1210ee;border:2px solid var(--gold);border-radius:12px;padding:8px 12px;font-size:14px;line-height:1.4;transform:translate(-50%,-100%);display:none;pointer-events:none}}
#bubble b{{color:var(--gold)}}
.sheet{{display:grid;grid-template-columns:repeat(auto-fill,minmax(112px,1fr));gap:8px;margin-top:12px}}
.th{{display:flex;flex-direction:column;align-items:center;padding:6px;background:#2a1a14;border-radius:10px}}
.th.sel{{border-color:var(--gold);box-shadow:0 0 10px #e0ad4a66}}
.th img{{height:150px}}.th img.c{{display:none}}body.color .th img{{display:none}}body.color .th img.c{{display:block}}
.th span{{color:var(--gold);font-size:13px}}.th small{{font-size:11px;opacity:.7}}
#player{{pointer-events:none}}
.bub{{animation:bub 1.6s infinite ease-in}}.b2{{animation-delay:.5s}}.b3{{animation-delay:1s}}
@keyframes bub{{0%{{transform:translateY(0);opacity:0}}20%{{opacity:.9}}100%{{transform:translateY(-34px);opacity:0}}}}
.flicker{{animation:fl .35s infinite alternate;transform-box:fill-box;transform-origin:50% 100%}}
@keyframes fl{{from{{transform:scaleY(1)}}to{{transform:scaleY(1.12) scaleX(.94)}}}}
.blink{{animation:blink 5s infinite;transform-box:fill-box;transform-origin:50% 50%}}
@keyframes blink{{0%,94%,100%{{transform:scaleY(1)}}96%{{transform:scaleY(.1)}}}}
{css_c}
{css_d}
{B.SC_COLOR}
{B.SC_DARK}
</style></head>
<body class="dark nolines"><div id="app">
<header><h1>⚗ Nebenfiguren der Akademie</h1>
<div class="hint">Figur unten auswählen, auf den Boden klicken zum Laufen.</div>
<button id="btnTalk">💬 Ansprechen</button><button id="btnTour">▶ Demo-Runde</button><button id="btnStyle">Farbversion ansehen</button></header>
<div id="stage"><svg id="svg" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
<defs>{B.DEFS}{ANIME_DEFS}</defs>
{B.SCENE}
<g id="player" transform="translate(640,690)"><g id="flip" transform="scale(0.5,0.5)"><g id="bob"><g id="npcRoot" transform="translate(-200,-773)"></g></g></g></g>
</svg><div id="bubble"></div></div>
<div class="sheet">{thumbs}</div>
</div>
<script>
const $ = s => document.querySelector(s);
const svg = $('#svg');
const S = {{x:640, y:690, dir:1, pose:'idle', walking:false}};
window.WALK_STYLE = {{hip:18}};
const NPC = {json.dumps(data, ensure_ascii=False)};
function svgPoint(e){{ const p = svg.createSVGPoint(); p.x=e.clientX; p.y=e.clientY; return p.matrixTransform(svg.getScreenCTM().inverse()); }}
{walk_js}
const BASE = Object.assign({{}}, WALK);
let current = null, lineIdx = 0, bubbleTimer;
function select(id){{
  target = null; running = false;
  current = id; lineIdx = 0;
  $('#npcRoot').innerHTML = NPC[id].markup;
  $('#player').setAttribute('class', 'npc-' + id);
  Object.assign(WALK, BASE, NPC[id].walk);
  document.querySelectorAll('.th').forEach(b => b.classList.toggle('sel', b.dataset.id === id));
  setPose('idle'); hideBubble();
}}
function hideBubble(){{ $('#bubble').style.display='none'; }}
function talk(){{
  const n = NPC[current], line = n.lines[lineIdx++ % n.lines.length];
  const r = $('#player').getBoundingClientRect(), st = $('#stage').getBoundingClientRect();
  const b = $('#bubble'); b.innerHTML = `<b>${{n.name}}</b> <small>(${{n.role}})</small><br>${{line}}`;
  b.style.left = (r.left + r.width/2 - st.left) + 'px'; b.style.top = (r.top - st.top - 6) + 'px'; b.style.display = 'block';
  clearTimeout(bubbleTimer); bubbleTimer = setTimeout(hideBubble, 3800);
}}
svg.addEventListener('click', e => {{ tour = null; hideBubble(); const p = svgPoint(e); walkTo(p.x, null, p.y >= 600 ? p.y : null); }});
document.querySelectorAll('.th').forEach(b => b.onclick = () => select(b.dataset.id));
$('#btnTalk').onclick = talk;
let tour = null;
const ROUTE = [[1000,690],[1000,648],[300,648],[300,702],[640,690]];
function runTour(i=0){{ if(tour===null) return; if(i>=ROUTE.length){{ tour=null; talk(); return; }} walkTo(ROUTE[i][0], ()=>setTimeout(()=>runTour(i+1),300), ROUTE[i][1]); }}
$('#btnTour').onclick = () => {{ hideBubble(); tour = 1; runTour(0); }};
$('#btnStyle').onclick = () => {{
  const c = document.body.classList.toggle('color'); document.body.classList.toggle('dark', !c); document.body.classList.toggle('nolines', !c);
  $('#btnStyle').textContent = c ? 'Scherenschnitt ansehen' : 'Farbversion ansehen';
}};
select('lena');
setTimeout(talk, 500);
</script></body></html>'''
open("npc_vorschau.html", "w").write(html)
print("ok", len(html)//1024, "KB")
