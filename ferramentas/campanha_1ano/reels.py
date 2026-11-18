"""Reels animados da campanha FONI BR 1 ANO (texto animado, sem gravação).
Uso: python3 reels.py
"""
import os, base64, asyncio, subprocess, shutil, sys
from playwright.async_api import async_playwright
from dados import VITRINE, brl

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
LOGO = base64.b64encode(open(os.path.join(ROOT, "marca", "logo_transparente.png"), "rb").read()).decode()
FPS = 30

BASE_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;background:#000;color:#fff;font-family:'Inter',sans-serif;overflow:hidden;position:relative}
.s{position:absolute;left:96px;right:120px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;opacity:0}
.badge{align-self:flex-start;border:2px solid #22C55E;color:#22C55E;font-weight:700;font-size:30px;letter-spacing:7px;padding:14px 30px;border-radius:999px;margin-bottom:60px}
.big{font-weight:900;font-size:300px;line-height:.9;letter-spacing:-10px}
.mid{font-weight:900;font-size:200px;line-height:.92;letter-spacing:-7px}
.h{font-weight:800;font-size:112px;line-height:1.02;letter-spacing:-3px}
.sub{font-weight:300;font-size:52px;color:#cfcfcf;margin-top:44px;line-height:1.3}
.g{color:#22C55E}
.line{height:5px;margin-top:60px;background:linear-gradient(90deg,rgba(29,179,60,0),#1DB33C 15%,#1DB33C 33%,#F2E205 33%,#F2E205 66%,#1F7BEA 66%,#1F7BEA 85%,rgba(31,123,234,0));transform-origin:left;width:100%}
.logo{height:96px;margin-top:90px;align-self:flex-start}
.cta{font-weight:700;font-size:50px;margin-top:56px;line-height:1.3}
.model{font-weight:800;font-size:104px;letter-spacing:-3px;line-height:1.02}
.spec{font-weight:600;font-size:44px;margin-top:28px}
.de{font-weight:300;font-size:46px;color:#8a8a8a;margin-top:80px}
.por{font-weight:900;font-size:180px;color:#22C55E;letter-spacing:-6px;line-height:1;margin-top:6px}
.off{align-self:flex-start;background:#22C55E;color:#000;font-weight:800;font-size:34px;letter-spacing:4px;padding:12px 26px;border-radius:999px;margin-top:40px}
"""

ANIM_JS = """
const ease=x=>1-Math.pow(1-Math.min(Math.max(x,0),1),3);
window.render=t=>{for(const [id,a,b,last] of S){const e=document.getElementById(id);
 const i=ease((t-a)/0.4), o=last?1:1-ease((t-(b-0.3))/0.3);
 const v=(t>=a&&(t<b||last))?Math.min(i,o):0;
 e.style.opacity=v; e.style.transform=`translateY(${(1-i)*50}px)`;
 const c=e.querySelector('[data-count]'); if(c){const n=+c.dataset.count;
   c.textContent=(c.dataset.pre||'')+Math.round(n*ease((t-a)/1.2));}
 const l=e.querySelector('.line'); if(l) l.style.transform=`scaleX(${ease((t-a-0.3)/0.9)})`;}};
"""


def numeros():
    scenes = [
        ('<span class="badge">1 ANO DE FONI BR</span><div class="mid">27/11<br>2025</div><div class="sub">O dia em que a Foni BR nasceu.</div><div class="line"></div>', 2.8),
        ('<div class="big g" data-count="180">0</div><div class="sub">aparelhos entregues.</div>', 2.6),
        ('<div class="big g" data-count="15" data-pre="+">+0</div><div class="sub">cidades atendidas.</div>', 2.6),
        ('<div class="big g" data-count="40" data-pre="+">+0</div><div class="sub">trocas no Foni Upgrade.</div>', 2.6),
        ('<span class="badge">SEMINOVOS</span><div class="h"><span class="g">8 meses</span> de garantia.</div><div class="sub">Em cada seminovo.</div>', 2.6),
        (f'<div class="h">1 ano.<br><span class="g">Apple ao seu alcance.</span></div><div class="cta">Dia 27 o presente é seu.</div><img class="logo" src="data:image/png;base64,{LOGO}"><div class="line"></div>', 3.4),
    ]
    return scenes


def vitrine():
    scenes = [(f'<span class="badge">1 ANO</span><div class="h">A vitrine<br><span class="g">abriu.</span></div><div class="sub">R$ 300 OFF em qualquer iPhone.</div><div class="line"></div>', 2.6)]
    for m, g, b, c, de, por in VITRINE:
        scenes.append((f'<span class="badge">VITRINE 1 ANO</span><div class="model">{m}</div><div class="spec">{g} &nbsp;·&nbsp; Bateria {b}</div>'
                       f'<div class="de">De <s>{brl(de)}</s> por</div><div class="por">{brl(por)}</div><span class="off">R$ 300 OFF</span>', 1.25))
    scenes.append((f'<div class="h">Até <span class="g">30/11.</span></div><div class="sub">8 meses de garantia.<br>Kit 1 Ano: capa + película.<br>Cupom FONI1ANO no site.</div>'
                   f'<div class="cta">Chame no direct.</div><img class="logo" src="data:image/png;base64,{LOGO}"><div class="line"></div>', 3.6))
    return scenes


def html(scenes):
    divs, S, t = [], [], 0.0
    for i, (inner, d) in enumerate(scenes):
        divs.append(f'<div class="s" id="s{i}">{inner}</div>')
        S.append(f'["s{i}",{t:.3f},{t + d:.3f},{"true" if i == len(scenes) - 1 else "false"}]')
        t += d
    js = "const S=[" + ",".join(S) + "];" + ANIM_JS
    return f'<html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>{"".join(divs)}<script>{js}</script></body></html>', t


async def render(scenes, out_path):
    page_html, dur = html(scenes)
    fr = os.path.join(HERE, "frames"); shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.set_content(page_html)
        for f in range(int(FPS * dur)):
            await pg.evaluate(f"render({f / FPS})")
            await pg.screenshot(path=os.path.join(fr, f"{f:04d}.jpg"), type="jpeg", quality=90)
        await b.close()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fr, "%04d.jpg"),
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac",
                    "-movflags", "+faststart", out_path], check=True)
    shutil.rmtree(fr)
    print(out_path, f"{dur:.1f}s")


async def main():
    which = sys.argv[1:] or ["numeros", "vitrine"]
    if "numeros" in which:
        await render(numeros(), os.path.join(ROOT, "posts", "2026-11-21", "foni_reel_12h_1ano_numeros.mp4"))
    if "vitrine" in which:
        await render(vitrine(), os.path.join(ROOT, "posts", "2026-11-27", "foni_reel_18h_1ano_vitrine.mp4"))

if __name__ == "__main__":
    asyncio.run(main())
