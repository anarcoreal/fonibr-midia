"""Anúncio de iPhone Foni BR — PADRÃO OFICIAL DE ANÚNCIOS DE IPHONES, definido em 25/11/2026 (estilo Apple).

Story 1080x1920, tudo centralizado:
  logo grande no alto · nome do modelo gigante · condição em verde (Seminovo/Novo)
  · armazenamento e saúde da bateria em dois blocos (valor + rótulo) · UM aparelho grande no centro · linha verde como "palco" sob o aparelho
  · "À vista" + preço forte · bolinhas de cor com o nome · garantia em linha própria · botão verde "Chame no WhatsApp"
  · promoção discreta no rodapé. Sem ponto final nas frases. Rodapé livre (campo de resposta do story).

Foto: recorte de UM aparelho (ex.: produtos/iphone-14/iphone14_preto.png). O fundo é removido por
transparência (o aparelho mantém as cores originais) e a ampliação é feita com Lanczos + nitidez leve.
Nunca escurecer a foto inteira para "pretear" o fundo: isso mata a qualidade do aparelho.

Uso:
  python3 gerar.py --modelo "iPhone 14" --memoria "128 GB" --bateria "100%" --preco 2850 \
      --cores "Preto, Branco, Lilás ou Azul" --foto ../../produtos/iphone-14/iphone14_preto.png \
      --saida ../../posts/AAAA-MM-DD/foni_story_produto_iphone14.jpg
Preço, cores e bateria: sempre de estoque/precos.md (não inventar).
"""
import os, sys, argparse, asyncio, base64, io
import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "campanha_1ano"))
from pecas import luz, LOGO_URI  # noqa: E402
from dados import brl  # noqa: E402

H = 1920
# Bolinhas de cor (estilo página de produto da Apple). Nome fora da lista -> bolinha cinza.
CORES = {"preto": "#2b2b2e", "branco": "#f2f1ec", "white": "#f2f1ec", "rosa": "#f4b8c8", "azul": "#a9c1dd",
         "verde": "#b9d9c3", "lilás": "#cbb9e2", "lavender": "#cbb9e2", "amarelo": "#f3e08a", "vermelho": "#d0202e",
         "dourado": "#e9d4a9", "prata": "#e3e4e5", "silver": "#e3e4e5", "roxo": "#5d4b70", "laranja": "#f08a3c",
         "titânio natural": "#bab4a9", "titânio deserto": "#c9b49b", "glacier": "#dfe8ee", "burgundy": "#6e1f2b"}
FOTO_ALT = 620  # altura do aparelho na arte (px)


def preparar_foto(caminho, altura=FOTO_ALT):
    """Fundo -> transparente (pela cor do canto), aparelho intacto, ampliação Lanczos + nitidez leve."""
    a = np.asarray(Image.open(caminho).convert("RGB")).astype(float)
    cantos = np.concatenate([a[:8, :8].reshape(-1, 3), a[:8, -8:].reshape(-1, 3)])
    bg = cantos.mean(0)
    alpha = np.clip((np.abs(a - bg).max(2) - 6) / 10, 0, 1)
    im = Image.fromarray(a.astype("uint8")).convert("RGBA")
    im.putalpha(Image.fromarray((alpha * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.6)))
    big = im.resize((round(im.width * altura / im.height), altura), Image.LANCZOS)
    rgb = big.convert("RGB").filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    rgb.putalpha(big.getchannel("A"))
    buf = io.BytesIO(); rgb.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def chips(cores):
    """"Preto, Rosa ou Branco" -> bolinha + nome de cada cor, numa linha."""
    import re
    nomes = [c.strip() for c in re.split(r",| ou | e ", cores) if c.strip()]
    return "".join(f'<span class="chip"><i style="background:{CORES.get(n.lower(), "#8e8e93")}"></i>{n}</span>' for n in nomes)


def html(modelo, cond, memoria, bateria, preco, cores, foto_uri, promo, garantia):
    gar_div = f'<div class="gar">{garantia}</div>' if garantia else ""
    palco = luz("base", H, .9).replace(f"M-60 {H-200} Q540 {H-340} 1140 {H-260}", "M-60 1370 Q540 1250 1140 1310")
    promo_div = f'<div class="promo">{promo}</div>' if promo else ""
    return f"""<html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:{H}px;background:#000;color:#F5F5F7;font-family:'Inter',sans-serif;overflow:hidden;position:relative;-webkit-font-smoothing:antialiased;text-align:center}}
.glow{{position:absolute;left:0;top:0}}
.logo{{position:absolute;top:120px;left:0;right:0}} .logo img{{width:360px}}
.top{{position:absolute;top:235px;left:0;right:0}}
h1{{font-size:150px;font-weight:700;letter-spacing:-5px}}
.eb{{font-size:40px;font-weight:600;color:#2FD35A;margin-top:4px}}
.specs{{display:flex;justify-content:center;margin-top:26px}}
.spec{{padding:0 54px}} .spec+.spec{{border-left:1.5px solid #3A3A3C}}
.spec b{{display:block;font-size:50px;font-weight:600;letter-spacing:-1px}}
.spec span{{display:block;font-size:24px;color:#A1A1A6;margin-top:6px}}
.foto{{position:absolute;top:660px;left:50%;transform:translateX(-50%);height:{FOTO_ALT}px;-webkit-mask-image:linear-gradient(#000 88%,transparent)}}
.base{{position:absolute;top:1345px;left:0;right:0}}
.de{{font-size:30px;color:#A1A1A6}}
.preco{{font-size:104px;font-weight:700;letter-spacing:-3px;margin-top:4px}}
.cores{{margin-top:14px;display:flex;justify-content:center;gap:34px}}
.chip{{font-size:30px;color:#D2D2D7;display:flex;align-items:center;gap:12px}}
.chip i{{width:28px;height:28px;border-radius:50%;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.35)}}
.gar{{font-size:30px;color:#A1A1A6;margin-top:12px}}
.cta{{display:inline-block;margin-top:30px;background:#2FD35A;color:#000;font-size:34px;font-weight:600;padding:22px 56px;border-radius:999px}}
.promo{{position:absolute;top:1760px;left:0;right:0;font-size:28px;color:#6E6E73}}
</style></head><body>
{palco}
<div class="logo"><img src="{LOGO_URI}"></div>
<div class="top"><h1>{modelo}</h1><div class="eb">{cond}</div><div class="specs"><div class="spec"><b>{memoria}</b><span>Armazenamento</span></div><div class="spec"><b>{bateria}</b><span>Saúde da bateria</span></div></div></div>
<img class="foto" src="{foto_uri}">
<div class="base"><div class="de">À vista</div><div class="preco">{brl(preco)}</div>
<div class="cores">{chips(cores)}</div>{gar_div}
<div class="cta">Chame no WhatsApp</div></div>
{promo_div}
</body></html>"""


async def render(doc, saida):
    from playwright.async_api import async_playwright
    os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width": 1080, "height": H})
        await pg.set_content(doc, wait_until="load")
        await pg.screenshot(path=saida, type="jpeg", quality=95)
        await b.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelo", required=True)
    ap.add_argument("--cond", default="Seminovo")
    ap.add_argument("--memoria", required=True, help='ex.: "128 GB"')
    ap.add_argument("--bateria", required=True, help='ex.: "100%%" ou "87%%+"')
    ap.add_argument("--preco", type=float, required=True)
    ap.add_argument("--cores", required=True, help='use "ou": "Preto ou Azul"')
    ap.add_argument("--garantia", default="8 meses de garantia")
    ap.add_argument("--promo", default="", help="linha discreta no rodapé (opcional)")
    ap.add_argument("--foto", required=True)
    ap.add_argument("--saida", required=True)
    a = ap.parse_args()
    asyncio.run(render(html(a.modelo, a.cond, a.memoria, a.bateria, a.preco, a.cores, preparar_foto(a.foto), a.promo, a.garantia), a.saida))
    print(a.saida)


if __name__ == "__main__":
    main()
