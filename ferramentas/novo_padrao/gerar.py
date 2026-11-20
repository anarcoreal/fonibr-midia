import os, base64, asyncio
from playwright.async_api import async_playwright

OUT = "posts/novo_padrao_saida"
LOGO = "/home/claude/repo/marca/logo_transparente.png"
os.makedirs(OUT, exist_ok=True)
LOGO_URI = "data:image/png;base64," + base64.b64encode(open(LOGO, "rb").read()).decode()

G = "#5CFF9A"   # brilho
G2 = "#22C55E"  # verde da marca

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;background:#000;color:#fff;font-family:'Inter',sans-serif;overflow:hidden;position:relative}}
.top{{position:absolute;top:92px;left:0;right:0;display:flex;justify-content:center}}
.top img{{width:330px}}
.botlogo{{position:absolute;bottom:80px;left:0;right:0;display:flex;justify-content:center}}
.botlogo img{{width:220px;opacity:.9}}
.center{{position:absolute;left:80px;right:80px;text-align:center;display:flex;flex-direction:column;align-items:center}}
h1{{font-weight:600;letter-spacing:-0.045em;line-height:1.03}}
.sub{{font-weight:400;font-size:38px;color:#A8A8A8;line-height:1.35}}
.dim{{color:#8E8E93}}
.swipe{{position:absolute;bottom:76px;left:0;right:0;text-align:center;font-size:24px;letter-spacing:.24em;color:#6E6E6E;font-weight:500}}
.glow{{position:absolute;left:0;right:0;pointer-events:none}}
.count{{position:absolute;top:104px;right:96px;font-size:26px;letter-spacing:.12em;color:#5A5A5A}}
.item{{position:absolute;left:96px;right:96px;top:300px}}
.num{{font-weight:200;font-size:200px;line-height:1;color:{G2};letter-spacing:-0.04em}}
.item h1{{font-size:84px;margin-top:40px}}
.item .body{{font-weight:400;font-size:44px;line-height:1.38;margin-top:44px;color:#EDEDED}}
.item .body b{{font-weight:600;color:#fff}}
.item .note{{font-weight:400;font-size:32px;line-height:1.45;margin-top:36px;color:#8A8A8A}}
.list{{margin-top:44px;width:100%;text-align:center}}
.list div{{font-size:38px;line-height:1.35;padding:20px 0;border-bottom:1px solid #1E1E1E;color:#E6E6E6}}
.list div b{{font-weight:600;color:#fff;display:block}}
.list div span{{display:block;color:#9A9A9A;font-size:32px;margin-top:6px}}
.steps{{margin-top:40px}}
.steps div{{display:flex;justify-content:space-between;align-items:baseline;padding:22px 0;border-bottom:1px solid #1E1E1E;font-size:36px}}
.steps div b{{font-weight:600}}
.steps div span{{color:#9A9A9A;font-size:32px}}
.slogan{{position:absolute;bottom:80px;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:26px}}
.slogan img{{width:300px}}
.slogan span{{font-size:24px;letter-spacing:.32em;font-weight:500;color:#BDBDBD}}
"""

def streak(bottom, height=360, opacity=1.0, d="M-60 300 Q560 70 1140 230"):
    return f'''<svg class="glow" style="bottom:{bottom}px;opacity:{opacity}" width="1080" height="{height}" viewBox="0 0 1080 360">
<defs><linearGradient id="sg" x1="0" x2="1"><stop offset="0" stop-color="{G}" stop-opacity="0"/><stop offset=".55" stop-color="{G}"/><stop offset="1" stop-color="{G}" stop-opacity="0"/></linearGradient>
<filter id="sb" x="-10%" y="-200%" width="120%" height="500%"><feGaussianBlur stdDeviation="14"/></filter></defs>
<path d="{d}" stroke="url(#sg)" stroke-width="22" fill="none" filter="url(#sb)" opacity=".75"/>
<path d="{d}" stroke="url(#sg)" stroke-width="3" fill="none"/></svg>'''

WATCH = f'''<svg width="420" height="560" viewBox="0 0 420 560" aria-hidden="true">
<defs>
<linearGradient id="band" x1="0" x2="1"><stop offset="0" stop-color="#151517"/><stop offset=".5" stop-color="#2A2A2D"/><stop offset="1" stop-color="#151517"/></linearGradient>
<linearGradient id="case" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2D2D7"/><stop offset=".45" stop-color="#5E5E63"/><stop offset="1" stop-color="#A9A9AF"/></linearGradient>
<filter id="ecgb"><feGaussianBlur stdDeviation="6"/></filter>
<radialGradient id="halo" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{G}" stop-opacity=".22"/><stop offset="1" stop-color="{G}" stop-opacity="0"/></radialGradient>
</defs>
<ellipse cx="210" cy="280" rx="210" ry="260" fill="url(#halo)"/>
<rect x="120" y="0" width="180" height="140" rx="26" fill="url(#band)"/>
<rect x="120" y="420" width="180" height="140" rx="26" fill="url(#band)"/>
<rect x="72" y="110" width="276" height="340" rx="76" fill="url(#case)"/>
<rect x="84" y="122" width="252" height="316" rx="66" fill="#000"/>
<rect x="346" y="210" width="16" height="64" rx="7" fill="#9A9A9F"/>
<rect x="348" y="300" width="10" height="56" rx="5" fill="#6A6A6F"/>
<text x="210" y="208" text-anchor="middle" font-family="Inter" font-weight="600" font-size="34" fill="#fff">SOS</text>
<path d="M110 300 H170 L185 270 L200 335 L218 245 L234 318 L246 300 H310" stroke="{G}" stroke-width="10" fill="none" filter="url(#ecgb)" opacity=".7"/>
<path d="M110 300 H170 L185 270 L200 335 L218 245 L234 318 L246 300 H310" stroke="{G}" stroke-width="5" fill="none" stroke-linejoin="round" stroke-linecap="round"/>
<text x="210" y="390" text-anchor="middle" font-family="Inter" font-weight="400" font-size="22" fill="#8E8E93">Detecção de Queda</text>
</svg>'''

def page(inner):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{inner}</body></html>"

TOP = f'<div class="top"><img src="{LOGO_URI}"></div>'
BOT = f'<div class="botlogo"><img src="{LOGO_URI}"></div>'
SLOGAN = f'<div class="slogan"><img src="{LOGO_URI}"><span>APPLE AO SEU ALCANCE.</span></div>'

def item(n, total, num, title, body, note):
    return page(f'''<div class="count">{n:02d}/{total:02d}</div>
<div class="item"><div class="num">{num}</div><h1>{title}</h1><div class="body">{body}</div><div class="note">{note}</div></div>
{streak(150, opacity=.35, d="M-60 320 Q560 200 1140 300")}{BOT}''')

slides = {
"foni_12h_apple_watch_01": page(f'''{TOP}
<div class="center" style="top:250px">{WATCH}</div>
<div class="center" style="top:860px"><h1 style="font-size:100px">Ele pede ajuda<br><span class="dim">por você</span></h1>
<div class="sub" style="margin-top:30px">Três recursos do Apple Watch para ativar hoje.</div></div>
<div class="swipe">DESLIZE</div>'''),
"foni_12h_apple_watch_02": item(2, 5, "01", "Detecção de Queda", "Depois de uma queda forte, o relógio <b>pergunta se você está bem.</b>", "Sem resposta, ele liga para a emergência e avisa seus contatos."),
"foni_12h_apple_watch_03": item(3, 5, "02", "SOS de Emergência", "Segure o <b>botão lateral</b> para ligar para a emergência.", "Seus contatos de emergência recebem a sua localização."),
"foni_12h_apple_watch_04": item(4, 5, "03", "Alertas do coração", "Avisos de frequência <b>alta, baixa e de ritmo irregular.</b>", "Os recursos de saúde variam conforme o modelo."),
"foni_12h_apple_watch_05": page(f'''<div class="count">05/05</div>
<div class="item" style="top:330px"><h1 style="margin-top:0">Configure pelo iPhone</h1>
<div class="body">No app <b>Apple Watch</b>, em poucos toques:</div>
<div class="steps">
<div><b>Detecção de Queda</b><span>SOS de Emergência</span></div>
<div><b>Contatos</b><span>Saúde &gt; Ficha Médica</span></div>
<div><b>Coração</b><span>Apple Watch &gt; Coração</span></div></div></div>
{streak(150, opacity=.35, d="M-60 320 Q560 200 1140 300")}{SLOGAN}'''),
"foni_18h_1ano_historia": page(f'''{TOP}
<div class="center" style="top:330px"><h1 style="font-size:330px;letter-spacing:-0.06em;line-height:.9">1 ano</h1>
<div style="margin-top:56px;font-size:58px;font-weight:500;letter-spacing:-0.02em;color:#E8E8E8;line-height:1.2">27/11/2025, o dia em que<br>a Foni BR nasceu</div></div>
{streak(230)}
<div class="center" style="bottom:90px"><div class="sub" style="font-size:32px;color:#9A9A9A">Obrigado a cada cliente que confiou na gente.<br>Dia 27 tem mais.</div></div>'''),
}

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for name, html in slides.items():
            await pg.set_content(html)
            await pg.wait_for_timeout(150)
            await pg.screenshot(path=f"{OUT}/{name}.jpg", type="jpeg", quality=95)
        await b.close()

asyncio.run(main())
