import base64, asyncio
from playwright.async_api import async_playwright
logo=base64.b64encode(open("/home/claude/fonibr-midia/marca/logo_transparente.png","rb").read()).decode()
html=f"""<html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;background:#000;color:#fff;font-family:'Inter',sans-serif;position:relative}}
.c{{position:absolute;left:96px;right:96px;top:420px}}
.badge{{display:inline-block;border:2px solid #22C55E;color:#22C55E;font-weight:700;font-size:28px;letter-spacing:6px;padding:14px 28px;border-radius:999px}}
h1{{font-weight:800;font-size:104px;line-height:1.06;letter-spacing:-2px;margin-top:70px}}
.g{{color:#22C55E}}
p{{font-weight:300;font-size:42px;color:#cfcfcf;margin-top:60px;line-height:1.35}}
.cta{{font-weight:700;color:#fff;font-size:40px;margin-top:90px;letter-spacing:1px}}
.foot{{position:absolute;left:96px;right:96px;bottom:420px;display:flex;justify-content:space-between;align-items:flex-end}}
.foot img{{height:76px}} .s{{font-weight:600;font-size:26px;letter-spacing:5px}}
</style></head><body><div class="c"><span class="badge">NOVO POST</span>
<h1>Antes de comprar um iPhone seminovo, confira <span class="g">5 pontos.</span></h1>
<p>O checklist completo está no feed.</p><div class="cta">TOQUE NO PERFIL PARA VER &rarr;</div></div>
<div class="foot"><img src="data:image/png;base64,{logo}"><div class="s">APPLE AO SEU ALCANCE.</div></div></body></html>"""
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        pg=await b.new_page(viewport={"width":1080,"height":1920})
        await pg.set_content(html); await pg.screenshot(path="out/foni_story_checklist.jpg",type="jpeg",quality=95); await b.close()
asyncio.run(m())
