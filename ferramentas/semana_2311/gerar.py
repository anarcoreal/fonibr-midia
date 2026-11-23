"""Pauta de 23 a 29/11/2026 (aprovada): peças que a tarefa de domingo gerou e não chegaram ao GitHub,
refeitas em 23/11 com o sistema editorial aprovado. CTA de venda sempre para o WhatsApp (link da bio).
Uso: python3 gerar.py [--reel]
"""
import os, sys, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "campanha_1ano"))
from playwright.async_api import async_playwright
from pecas import page, hero, one, item, lista, modelo, tabela, titulo, ROOT
from dados import VITRINE, brl
import reels

G = '<span class="g">{}</span>'.format
WA = "CHAME NO WHATSAPP, LINK DA BIO &rarr;"
ESPACO = '<div style="height:330px"></div>'  # área livre para a figurinha de enquete

P = []  # (data, arquivo, fmt, html)


def add(d, nome, fmt, html):
    P.append((d, nome, fmt, html))


def produto(m, g, b, cores, preco, extra=""):
    return (f'<div class="eb">Seminovo do dia</div><h1>{m}</h1><div class="spec">{g} · Bateria {b}</div>'
            f'<div class="cores">{cores}</div>' + (f'<div class="cores">{extra}</div>' if extra else "") + '<div class="de">À vista</div>'
            f'<div class="por">{brl(preco)}</div>'
            f'<div class="perks">8 meses de garantia<br>Dia 27: R$ 300 OFF em qualquer iPhone</div>'
            f'<p class="tap">{WA}</p>')


# ---------------------------------------------------------------- 23/11
add("2026-11-23", "foni_12h_1ano_revelacao_05.jpg", "feed",
    page(lista(f'Quer ver os preços {G("antes de todo mundo?")}',
               ["Comente <b>VIP</b> neste post", "Ou chame no WhatsApp, link da bio",
                "A lista VIP recebe a vitrine na noite de 26/11"],
               "Vitrine aberta dia 27, às 07h43."), "feed", pg="05/05"))
add("2026-11-23", "foni_story_18h_loja_de_verdade.jpg", "story",
    page(lista(f'Loja de verdade. {G("Pode conferir.")}',
               ["FONI BR LTDA · CNPJ 69.207.688/0001-81", "Página no Reclame Aqui",
                "8 meses de garantia nos seminovos", "Envio para todo o Brasil"], "Chame no WhatsApp, link da bio."),
         "story", kind="inner"))

# ---------------------------------------------------------------- 24/11
add("2026-11-24", "foni_story_0743_produto_iphone14promax.jpg", "story",
    page(produto("iPhone 14 Pro Max", "128 GB", "90%", "Dourado e Branco", 3900,
                 "Também 256 GB em Preto e Roxo: R$ 4.120"), "story", kind="inner"))
add("2026-11-24", "foni_story_12h_curiosidade_app_store.jpg", "story",
    page(hero(f'A App Store abriu {G("com 500 apps.")}',
              "Foi em julho de 2008. Hoje são milhões, e o seu iPhone baixa todos eles."), "story", badge="CURIOSIDADE"))
add("2026-11-24", "foni_story_18h_enquete_14promax_15.jpg", "story",
    page(hero(f'14 Pro Max {G("ou 15?")}', "Vote na enquete. Dia 27 os dois saem com R$ 300 OFF.") + ESPACO,
         "story", badge="ENQUETE"))

# ---------------------------------------------------------------- 25/11
add("2026-11-25", "foni_story_0743_produto_iphone15promax.jpg", "story",
    page(produto("iPhone 15 Pro Max", "256 GB", "90%+", "Titânio Natural", 4700), "story", kind="inner"))
add("2026-11-25", "foni_story_18h_como_comprar.jpg", "story",
    page(lista(f'Como comprar {G("na Foni BR")}',
               ["01 · Chame no WhatsApp, link da bio", "02 · Escolha modelo, cor e armazenamento",
                "03 · Pague e receba o termo de garantia digital", "04 · Receba em casa, com envio para todo o Brasil"],
               "Dúvida? É só chamar."), "story", kind="inner"))

# ---------------------------------------------------------------- 26/11
add("2026-11-26", "foni_story_0743_produto_iphone16pro.jpg", "story",
    page(produto("iPhone 16 Pro", "128 GB", "89%+", "Titânio Deserto e Natural", 4820,
                 "Também 256 GB, bateria 100%: R$ 5.120"), "story", kind="inner"))
add("2026-11-26", "foni_story_12h_curiosidade_magsafe.jpg", "story",
    page(hero(f'O MagSafe {G("nasceu no MacBook.")}',
              "Estreou no MacBook Pro em 2006 e voltou no iPhone 12, em 2020, para carregadores e acessórios magnéticos."),
         "story", badge="CURIOSIDADE"))

# ---------------------------------------------------------------- 27/11
add("2026-11-27", "foni_story_12h_1ano_tabela.jpg", "story", page(tabela(), "story", kind="tabela").replace('class="blk" style="top:220px"', 'class="blk" style="top:420px"'))
n = len(VITRINE) + 3
vit = [page(one(f'A vitrine {G("abriu.")}', "Hoje a Foni BR faz um ano e o presente é seu. R$ 300 OFF em qualquer iPhone."),
            "feed", badge="1 ANO", pg=f"01/{n:02d}", swipe=True)]
for i, r in enumerate(VITRINE, 2):
    vit.append(page(modelo(*r), "feed", badge="VITRINE 1 ANO", pg=f"{i:02d}/{n:02d}"))
vit.append(page(lista(f'iPhones novos {G("também.")}',
                      ["Lacrados, a partir do iPhone 16", "R$ 300 OFF em qualquer modelo", "Consulte cores e preços"],
                      "Chame no WhatsApp, link da bio."), "feed", pg=f"{n-1:02d}/{n:02d}"))
vit.append(page(lista(f'Até 30/11 ou {G("enquanto durar.")}',
                      ["R$ 300 OFF em qualquer iPhone", "8 meses de garantia nos seminovos", "Capa + película de brinde",
                       "Cupom FONI1ANO no fonibr.com.br"], "Chame no WhatsApp, link da bio."), "feed", pg=f"{n:02d}/{n:02d}"))
for i, h in enumerate(vit, 1):
    add("2026-11-27", f"foni_12h_1ano_vitrine_{i:02d}.jpg", "feed", h)

# ---------------------------------------------------------------- 28/11
add("2026-11-28", "foni_story_12h_1ano_upgrade.jpg", "story",
    page(hero(f'Seu iPhone antigo {G("vira crédito.")}', "Troque pelo Foni Upgrade. Modelo novo com R$ 300 OFF até 30/11.", WA),
         "story", badge="FONI UPGRADE"))
add("2026-11-28", "foni_story_18h_enquete_garantiu.jpg", "story",
    page(hero(f'Já garantiu {G("o seu?")}', "R$ 300 OFF em qualquer iPhone até 30/11.") + ESPACO, "story", badge="ENQUETE"))

# ---------------------------------------------------------------- 29/11
add("2026-11-29", "foni_story_12h_1ano_ate_amanha.jpg", "story",
    page(hero(f'Só até {G("amanhã.")}', "R$ 300 OFF em qualquer iPhone, capa + película de brinde e cupom FONI1ANO.", WA), "story"))
add("2026-11-29", "foni_story_12h_reel_ultimos_dias.jpg", "story",
    page(hero(f'Últimos dias {G("da vitrine.")}', "R$ 300 OFF em qualquer iPhone até 30/11.", "TOQUE NO PERFIL PARA VER &rarr;"),
         "story", badge="NOVO REEL"))


def reel_ultimos():
    def h(t, s=""):
        return f'<div class="h">{titulo(t)}</div>' + (f'<div class="sub">{s}</div>' if s else "")
    return [
        (h(f'Só até {G("amanhã")}', "A vitrine de 1 ano da Foni BR fecha dia 30/11."), 2.8),
        ('<div class="big">R$300</div><div class="sub">OFF em qualquer iPhone, novo ou seminovo.</div>', 2.8),
        (h(f'16 seminovos {G("na vitrine")}', "Do iPhone 11 ao 16 Pro Max, com 8 meses de garantia."), 2.8),
        (h(f'Capa + película {G("de brinde")}', "Em toda compra da campanha."), 2.6),
        (h(f'No site, cupom {G("FONI1ANO")}', "Os mesmos R$ 300 OFF no fonibr.com.br."), 2.6),
        ('<div class="h">Chame no WhatsApp<span class="tail">link da bio</span></div><div class="slogan">APPLE AO SEU ALCANCE.</div>', 3.4),
    ]


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pages = {"feed": await b.new_page(viewport={"width": 1080, "height": 1350}),
                 "story": await b.new_page(viewport={"width": 1080, "height": 1920})}
        for d, nome, fmt, html in P:
            out = os.path.join(ROOT, "posts", d); os.makedirs(out, exist_ok=True)
            await pages[fmt].set_content(html, wait_until="load")
            await pages[fmt].screenshot(path=os.path.join(out, nome), type="jpeg", quality=95)
        await b.close()
    print(len(P), "imagens")
    if "--reel" in sys.argv:
        await reels.render(reel_ultimos(), os.path.join(ROOT, "posts", "2026-11-29", "foni_reel_12h_1ano_ultimos_dias.mp4"))

if __name__ == "__main__":
    asyncio.run(main())
