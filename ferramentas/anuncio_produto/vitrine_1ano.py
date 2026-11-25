"""Vitrine 1 Ano (27/11/2026) refeita no PADRÃO OFICIAL de anúncio (25/11/2026).

Gera em posts/2026-11-27/:
  foni_12h_1ano_vitrine_01..NN.jpg  carrossel 1080x1350 (capa + 1 slide por modelo + fechamento)
  foni_story_12h_1ano_tabela.jpg    story 1080x1920 com a lista de preços
  foni_12h_1ano_tabela.jpg          a mesma lista em 1080x1350
Os slides de produto são o story oficial reduzido para caber no feed (fundo preto, sem corte).
Só entram modelos com foto em produtos/ e preço em estoque/precos.md. Fora por ora: iPhone 11 e
seminovos 16/16 Pro/16 Pro Max (Leonardo: seminovos só 12 a 15), iPhone 13 (falta foto real).

Uso: python3 vitrine_1ano.py
"""
import os, sys, glob, asyncio, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from fichas import FICHAS
from campanha_1ano import gerar as gerar_story, POSTS, OFF
from gerar import luz, LOGO_URI, H

DIA = os.path.join(POSTS, "2026-11-27")
MODELOS = ["iphone14", "iphone14pro", "iphone14promax", "iphone15", "iphone15pro", "iphone15promax",
           "iphone17", "iphone17pro", "iphone17promax", "iphone18pro", "iphone18promax"]

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:%dpx;background:#000;color:#F5F5F7;font-family:'Inter',sans-serif;overflow:hidden;position:relative;-webkit-font-smoothing:antialiased;text-align:center}
.glow{position:absolute;left:0;top:0}
.logo{position:absolute;top:120px;left:0;right:0}.logo img{width:360px}
h1{font-size:150px;font-weight:700;letter-spacing:-5px;line-height:1.05}
.eb{font-size:40px;font-weight:600;color:#2FD35A}
.sub{font-size:40px;color:#A1A1A6;line-height:1.35}
.cta{display:inline-block;background:#2FD35A;color:#000;font-size:34px;font-weight:600;padding:22px 56px;border-radius:999px}
.rows{width:820px;margin:0 auto;text-align:left}
.rows div{display:flex;justify-content:space-between;font-size:38px;padding:20px 0;border-bottom:1.5px solid #2C2C2E}
.rows div b{font-weight:600}.rows div span{color:#F5F5F7;font-weight:700}
.rows .grp{border:none;color:#2FD35A;font-size:30px;font-weight:600;padding:34px 0 6px}
.note{font-size:28px;color:#6E6E73}
"""


def pagina(corpo, h=H, linha_y=None):
    palco = luz("base", h, .9)
    if linha_y:
        palco = palco.replace(f"M-60 {h-200} Q540 {h-340} 1140 {h-260}", f"M-60 {linha_y+60} Q540 {linha_y-60} 1140 {linha_y}")
    return (f'<html><head><meta charset="utf-8"><style>{CSS % h}</style></head><body>{palco}'
            f'<div class="logo"><img src="{LOGO_URI}"></div>{corpo}</body></html>')


def preco(ficha):
    f = FICHAS[ficha]
    v = float(f["preco"]) - OFF
    s = "R$ " + f"{v:,.0f}".replace(",", ".")
    return ("a partir de " + s) if "a partir" in f.get("de", "") else s


def capa():
    return pagina('<div style="position:absolute;top:560px;left:0;right:0">'
                  '<div class="eb">1 ano de Foni BR</div><h1 style="margin-top:24px">A vitrine<br>abriu</h1>'
                  '<p class="sub" style="margin-top:48px">R$ 300 OFF em qualquer iPhone<br>novo ou seminovo</p></div>'
                  '<div style="position:absolute;top:1420px;left:0;right:0"><p class="sub">Arraste para ver os modelos</p></div>',
                  linha_y=1300)


def fechamento():
    itens = ["R$ 300 OFF em qualquer iPhone", "8 meses de garantia nos seminovos",
             "Capa + película de brinde", "Cupom FONI1ANO no fonibr.com.br"]
    lista = "".join(f'<p class="item">{t}</p>' for t in itens)
    return pagina('<style>.item{font-size:40px;font-weight:600;padding:20px 0}.item+.item{border-top:1.5px solid #2C2C2E}'
                  '.lista{width:760px;margin:70px auto 0}</style>'
                  '<div style="position:absolute;top:430px;left:0;right:0">'
                  '<h1 style="font-size:130px">Até 30/11</h1><p class="sub" style="margin-top:16px">ou enquanto durar o estoque</p>'
                  f'<div class="lista">{lista}</div></div>'
                  '<div style="position:absolute;top:1330px;left:0;right:0"><span class="cta">Chame no WhatsApp</span>'
                  '<p class="note" style="margin-top:26px">Link na bio</p></div>', linha_y=1200)


def tabela(h):
    semi = [m for m in MODELOS if FICHAS[m].get("cond", "Seminovo") == "Seminovo"]
    novo = [m for m in MODELOS if m not in semi]
    linhas = '<div class="grp">Seminovos, 8 meses de garantia</div>' + "".join(
        f'<div><b>{FICHAS[m]["modelo"]}</b><span>{preco(m)}</span></div>' for m in semi)
    linhas += '<div class="grp">Novos, lacrados</div>' + "".join(
        f'<div><b>{FICHAS[m]["modelo"]}</b><span>{preco(m)}</span></div>' for m in novo)
    if h == H:
        topo, fim = 300, 1610
    else:
        topo, fim = 260, 1190
        linhas = linhas.replace("padding:20px 0", "")
    corpo = (f'<div style="position:absolute;top:{topo}px;left:0;right:0"><div class="eb">Vitrine 1 Ano</div>'
             f'<h1 style="font-size:{84 if h == H else 72}px;margin-top:10px">Preços com R$ 300 OFF</h1>'
             f'<div class="rows" style="margin-top:10px">{linhas}</div></div>'
             f'<div style="position:absolute;top:{fim}px;left:0;right:0"><span class="cta">Chame no WhatsApp</span>'
             f'<p class="note" style="margin-top:22px">À vista. Até 30/11 ou enquanto durar o estoque</p></div>')
    css_feed = "" if h == H else "<style>.rows div{font-size:30px;padding:11px 0}.rows .grp{font-size:24px;padding:20px 0 2px}.logo{top:70px}.logo img{width:280px}</style>"
    html = pagina(corpo, h).replace("</head>", css_feed + "</head>")
    i = html.index('<svg class="glow"'); j = html.index("</svg>", i) + 6
    return html[:i] + html[j:]  # sem linha verde: ela cruzava a lista


async def render(html, saida, h):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width": 1080, "height": h})
        await pg.set_content(html, wait_until="load")
        await pg.screenshot(path=saida, type="jpeg", quality=95)
        await b.close()


def para_feed(story_jpg, saida):
    """Story 1080x1920 -> slide 1080x1350 (reduz e centraliza no fundo preto, sem cortar nada)."""
    im = Image.open(story_jpg).convert("RGB")
    w = round(1080 * 1350 / 1920)
    im = im.resize((w, 1350), Image.LANCZOS)
    out = Image.new("RGB", (1080, 1350), (0, 0, 0)); out.paste(im, ((1080 - w) // 2, 0))
    out.save(saida, "JPEG", quality=95)


def main():
    os.makedirs(DIA, exist_ok=True)
    for f in glob.glob(os.path.join(DIA, "foni_12h_1ano_vitrine_*.jpg")):
        os.remove(f)
    tmp = tempfile.mkdtemp()
    slides = []
    asyncio.run(render(capa(), os.path.join(tmp, "capa.jpg"), H)); slides.append(os.path.join(tmp, "capa.jpg"))
    for m in MODELOS:
        gerar_story(os.path.relpath(tmp, POSTS), f"{m}.jpg", m, True)
        slides.append(os.path.join(tmp, f"{m}.jpg"))
    asyncio.run(render(fechamento(), os.path.join(tmp, "fim.jpg"), H)); slides.append(os.path.join(tmp, "fim.jpg"))
    for i, s in enumerate(slides, 1):
        para_feed(s, os.path.join(DIA, f"foni_12h_1ano_vitrine_{i:02d}.jpg"))
    asyncio.run(render(tabela(H), os.path.join(DIA, "foni_story_12h_1ano_tabela.jpg"), H))
    asyncio.run(render(tabela(1350), os.path.join(DIA, "foni_12h_1ano_tabela.jpg"), 1350))
    print(len(slides), "slides")


if __name__ == "__main__":
    main()
