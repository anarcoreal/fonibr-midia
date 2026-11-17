import os, base64, asyncio
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = "/home/claude/fonibr-midia/marca/logo_transparente.png"

slides = [
    dict(badge="IPHONE SEMINOVO", kind="cover",
         title='Antes de comprar um iPhone seminovo, confira <span class="g">5 pontos.</span>',
         sub="Salve este post para usar na hora da compra."),
    dict(badge="CHECKLIST", num="01", title="Saúde da bateria",
         body='Em <b>Ajustes &gt; Bateria &gt; Saúde</b>, veja a capacidade máxima.',
         note="Abaixo de 80%, o próprio iPhone passa a recomendar a troca da bateria."),
    dict(badge="CHECKLIST", num="02", title="Peças e histórico",
         body='Em <b>Ajustes &gt; Geral &gt; Sobre</b>, os modelos recentes mostram se tela, bateria ou câmera foram trocadas.',
         note="Peça desconhecida pode significar reparo sem procedência."),
    dict(badge="CHECKLIST", num="03", title="Conta iCloud desvinculada",
         body='O aparelho precisa estar <b>fora da conta do antigo dono</b>, com o Buscar iPhone desativado.',
         note="Sem isso, o iPhone pode ser bloqueado a qualquer momento."),
    dict(badge="CHECKLIST", num="04", title="IMEI e procedência",
         body='Disque <b>*#06#</b> e confira se o IMEI bate com a caixa e a nota.',
         note="Consulte também se o aparelho não tem restrição por roubo ou perda."),
    dict(badge="CHECKLIST", num="05", title="Garantia por escrito",
         body='Quem vende seminovo com confiança <b>oferece garantia</b>.',
         note="Sem garantia, o risco fica todo com você."),
    dict(badge="FONI BR", kind="final",
         title='Na Foni BR, <span class="g">você compra tranquilo.</span>',
         items=["8 meses de garantia nos seminovos",
                "Foni Upgrade: recompra garantida em até 12 meses, com crédito na troca",
                "Envio para todo o Brasil"],
         cta="Black Friday até 30/11. Chame no WhatsApp pelo link da bio."),
]

def logo_html():
    if os.path.exists(LOGO):
        b = base64.b64encode(open(LOGO, "rb").read()).decode()
        return f'<img class="logo" src="data:image/png;base64,{b}">'
    return '<div class="logo ph">LOGO FONI BR</div>'

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#000;color:#fff;font-family:'Inter',sans-serif;overflow:hidden}
.wrap{position:absolute;inset:0;padding:110px 96px 0 96px}
.badge{display:inline-block;border:2px solid #22C55E;color:#22C55E;font-weight:700;font-size:26px;letter-spacing:6px;padding:14px 28px;border-radius:999px}
.sig{height:3px;width:100%;background:linear-gradient(90deg,rgba(29,179,60,0) 0%,#1DB33C 12%,#1DB33C 33%,#F2E205 33%,#F2E205 66%,#1F7BEA 66%,#1F7BEA 88%,rgba(31,123,234,0) 100%)}
.g{color:#22C55E}
h1{font-weight:800;letter-spacing:-1.5px;line-height:1.08}
.cover h1{font-size:96px;margin-top:150px}
.cover .sub{font-weight:300;font-size:38px;color:#cfcfcf;margin-top:56px;line-height:1.35}
.num{font-weight:200;font-size:220px;color:#22C55E;line-height:1;margin-top:90px;letter-spacing:-6px}
.item h1{font-size:76px;margin-top:30px}
.item .body{font-weight:300;font-size:44px;line-height:1.38;margin-top:52px;color:#eee}
.item .body b{font-weight:700;color:#fff}
.item .note{font-weight:300;font-size:32px;line-height:1.4;margin-top:44px;color:#9a9a9a;border-left:3px solid #22C55E;padding-left:28px}
.final h1{font-size:84px;margin-top:120px}
.final ul{list-style:none;margin-top:70px}
.final li{font-weight:300;font-size:38px;line-height:1.35;padding:26px 0;border-bottom:1px solid #222;display:flex;gap:28px}
.final li:before{content:"";flex:0 0 14px;height:14px;margin-top:16px;background:#22C55E;border-radius:50%}
.final .cta{font-weight:700;font-size:36px;margin-top:60px;line-height:1.35}
.foot{position:absolute;left:96px;right:96px;bottom:84px;display:flex;align-items:flex-end;justify-content:space-between}
.foot .sig{position:absolute;top:-40px;left:0}
.logo{height:70px}
.logo.ph{height:70px;width:260px;border:2px dashed #555;color:#777;font-size:20px;letter-spacing:3px;display:flex;align-items:center;justify-content:center}
.slogan{font-weight:600;font-size:24px;letter-spacing:5px;color:#fff}
.page{position:absolute;top:118px;right:96px;font-weight:300;font-size:26px;color:#777;letter-spacing:3px}
.swipe{position:absolute;right:96px;bottom:200px;font-weight:300;font-size:26px;color:#888;letter-spacing:4px}
"""

def html(i, s):
    total = len(slides)
    if s.get("kind") == "cover":
        inner = f'<div class="cover"><h1>{s["title"]}</h1><p class="sub">{s["sub"]}</p></div><div class="swipe">DESLIZE &rarr;</div>'
    elif s.get("kind") == "final":
        lis = "".join(f"<li><span>{x}</span></li>" for x in s["items"])
        inner = f'<div class="final"><h1>{s["title"]}</h1><ul>{lis}</ul><p class="cta">{s["cta"]}</p></div>'
    else:
        inner = f'<div class="item"><div class="num">{s["num"]}</div><h1>{s["title"]}</h1><p class="body">{s["body"]}</p><p class="note">{s["note"]}</p></div>'
    return f"""<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="wrap"><span class="badge">{s["badge"]}</span><div class="page">{i+1:02d}/{total:02d}</div>{inner}</div>
<div class="foot">{logo_html()}<div class="slogan">APPLE AO SEU ALCANCE.</div></div>
</body></html>"""

async def main():
    out = os.path.join(HERE, "out"); os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":1080,"height":1350})
        for i, s in enumerate(slides):
            await pg.set_content(html(i, s), wait_until="load")
            await pg.screenshot(path=os.path.join(out, f"foni_checklist_{i+1:02d}.jpg"), type="jpeg", quality=95)
        await b.close()

asyncio.run(main())
