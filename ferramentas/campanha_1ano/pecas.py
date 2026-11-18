"""Gera posts do feed (1080x1350) e stories (1080x1920) da campanha FONI BR 1 ANO.
Uso: python3 pecas.py  -> grava em ../../posts/<data>/
"""
import os, base64, asyncio
from playwright.async_api import async_playwright
from dados import VITRINE, brl

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
LOGO = base64.b64encode(open(os.path.join(ROOT, "marca", "logo_transparente.png"), "rb").read()).decode()
SIG = "linear-gradient(90deg,rgba(29,179,60,0) 0%,#1DB33C 12%,#1DB33C 33%,#F2E205 33%,#F2E205 66%,#1F7BEA 66%,#1F7BEA 88%,rgba(31,123,234,0) 100%)"

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:%(H)dpx;background:#000;color:#fff;font-family:'Inter',sans-serif;overflow:hidden;position:relative}
.wrap{position:absolute;left:96px;right:96px;top:%(TOP)dpx}
.badge{display:inline-block;border:2px solid #22C55E;color:#22C55E;font-weight:700;font-size:26px;letter-spacing:6px;padding:14px 28px;border-radius:999px}
.page{position:absolute;top:%(PTOP)dpx;right:96px;font-weight:300;font-size:26px;color:#777;letter-spacing:3px}
.g{color:#22C55E}
.sig{height:3px;width:100%%;background:%(SIG)s}
h1{font-weight:800;letter-spacing:-1.5px;line-height:1.06}
.one{font-weight:900;font-size:%(ONE)dpx;line-height:.8;letter-spacing:-20px;margin-top:%(ONEMT)dpx;display:block}
.one + .sig{width:300px;height:6px;margin-top:28px}
.h1xl{font-size:%(XL)dpx;margin-top:%(H1MT)dpx}
.h1l{font-size:84px;margin-top:%(H1MT)dpx}
.sub{font-weight:300;font-size:40px;color:#cfcfcf;margin-top:48px;line-height:1.35}
.cta{font-weight:700;font-size:36px;margin-top:56px;line-height:1.35;letter-spacing:.5px}
.num{font-weight:200;font-size:200px;color:#22C55E;line-height:1;margin-top:90px;letter-spacing:-6px}
.item h1{font-size:76px;margin-top:30px}
.body{font-weight:300;font-size:42px;line-height:1.38;margin-top:48px;color:#eee}
.body b{font-weight:700;color:#fff}
.note{font-weight:300;font-size:31px;line-height:1.4;margin-top:44px;color:#9a9a9a;border-left:3px solid #22C55E;padding-left:28px}
ul{list-style:none;margin-top:64px}
li{font-weight:300;font-size:38px;line-height:1.35;padding:24px 0;border-bottom:1px solid #222;display:flex;gap:28px}
li:before{content:"";flex:0 0 14px;height:14px;margin-top:16px;background:#22C55E;border-radius:50%%}
li b{font-weight:700}
.model h1{font-size:%(MODEL)dpx;margin-top:%(MODELMT)dpx}
.spec{font-weight:600;font-size:38px;margin-top:30px;letter-spacing:.5px}
.cores{font-weight:300;font-size:32px;color:#9a9a9a;margin-top:18px;line-height:1.35}
.de{font-weight:300;font-size:40px;color:#8a8a8a;margin-top:%(DEMT)dpx}
.de s{text-decoration-thickness:2px}
.por{font-weight:800;font-size:%(POR)dpx;color:#22C55E;letter-spacing:-3px;line-height:1;margin-top:8px}
.off{display:inline-block;background:#22C55E;color:#000;font-weight:800;font-size:30px;letter-spacing:4px;padding:10px 22px;border-radius:999px;margin-top:36px}
.perks{font-weight:300;font-size:30px;color:#cfcfcf;margin-top:40px;line-height:1.5;border-left:3px solid #22C55E;padding-left:28px}
table{width:100%%;border-collapse:collapse;margin-top:40px}
td,th{font-size:25px;padding:8px 0;border-bottom:1px solid #1f1f1f;text-align:left}
th{font-weight:600;color:#777;letter-spacing:2px;font-size:20px}
td{font-weight:300}
td.m{font-weight:600}
td.r,th.r{text-align:right}
td.p{font-weight:800;color:#22C55E;text-align:right}
td.d{color:#777;text-align:right}
.foot{position:absolute;left:96px;right:96px;bottom:%(FOOT)dpx;display:flex;align-items:flex-end;justify-content:space-between}
.foot img{height:70px}
.slogan{font-weight:600;font-size:24px;letter-spacing:5px}
.swipe{position:absolute;right:96px;bottom:%(SWIPE)dpx;font-weight:300;font-size:26px;color:#888;letter-spacing:4px}
.space{height:%(SPACE)dpx}
"""

FEED = dict(H=1350, TOP=110, PTOP=118, ONE=400, ONEMT=70, XL=96, H1MT=60, MODEL=96, MODELMT=120,
            DEMT=90, POR=150, FOOT=84, SWIPE=200, SPACE=0, SIG=SIG)
STORY = dict(H=1920, TOP=330, PTOP=338, ONE=520, ONEMT=90, XL=110, H1MT=70, MODEL=92, MODELMT=90,
             DEMT=80, POR=170, FOOT=330, SWIPE=420, SPACE=60, SIG=SIG)


def page(inner, fmt, badge="1 ANO", pg=None, swipe=False):
    P = FEED if fmt == "feed" else STORY
    css = CSS % P
    pgh = f'<div class="page">{pg}</div>' if pg else ""
    sw = '<div class="swipe">DESLIZE &rarr;</div>' if swipe else ""
    return (f'<html><head><meta charset="utf-8"><style>{css}</style></head><body>'
            f'<div class="wrap"><span class="badge">{badge}</span>{pgh}{inner}</div>{sw}'
            f'<div class="foot"><img src="data:image/png;base64,{LOGO}"><div class="slogan">APPLE AO SEU ALCANCE.</div></div>'
            f'</body></html>')


def one(h1, sub="", cta="", cls="h1xl"):
    s = f'<p class="sub">{sub}</p>' if sub else ""
    c = f'<p class="cta">{cta}</p>' if cta else ""
    return f'<div class="one">1</div><div class="sig"></div><h1 class="{cls}">{h1}</h1>{s}{c}'


def hero(h1, sub="", cta="", cls="h1xl", mt=150):
    s = f'<p class="sub">{sub}</p>' if sub else ""
    c = f'<p class="cta">{cta}</p>' if cta else ""
    return f'<h1 class="{cls}" style="margin-top:{mt}px">{h1}</h1>{s}{c}'


def item(num, title, body, note):
    return f'<div class="item"><div class="num">{num}</div><h1>{title}</h1><p class="body">{body}</p><p class="note">{note}</p></div>'


def lista(h1, items, cta="", mt=110):
    lis = "".join(f"<li><span>{x}</span></li>" for x in items)
    c = f'<p class="cta">{cta}</p>' if cta else ""
    return f'<h1 class="h1l" style="margin-top:{mt}px">{h1}</h1><ul>{lis}</ul>{c}'


def modelo(m, g, b, c, de, por):
    return (f'<div class="model"><h1>{m}</h1><div class="spec">{g} &nbsp;·&nbsp; Bateria {b}</div>'
            f'<div class="cores">{c}</div><div class="de">De <s>{brl(de)}</s> por</div>'
            f'<div class="por">{brl(por)}</div><span class="off">20% OFF</span>'
            f'<div class="perks">8 meses de garantia<br>Kit 1 Ano: capa + película</div></div>')


def tabela():
    rows = "".join(
        f'<tr><td class="m">{m}</td><td>{g}</td><td>{b}</td><td class="d"><s>{brl(de)}</s></td><td class="p">{brl(por)}</td></tr>'
        for m, g, b, c, de, por in VITRINE)
    return (f'<h1 style="font-size:64px;margin-top:44px">Vitrine 1 ano. <span class="g">20% OFF.</span></h1>'
            f'<table><tr><th>MODELO</th><th>ARMAZ.</th><th>BATERIA</th><th class="r">DE</th><th class="r">POR</th></tr>{rows}</table>'
            f'<p class="note" style="margin-top:24px;font-size:24px">8 meses de garantia e Kit 1 Ano em toda compra. Até 30/11.</p>')


# ---------------------------------------------------------------- peças
def build():
    P = []  # (data, arquivo, fmt, html)
    def add(d, nome, fmt, html): P.append((d, nome, fmt, html))

    # 18/11 teaser
    add("2026-11-18", "foni_18h_1ano_teaser.jpg", "feed",
        page(one('Algo completa <span class="g">1 ano</span> no dia 27.', "Ative as notificações. O presente é seu."), "feed"))
    add("2026-11-18", "foni_story_18h_1ano_teaser.jpg", "story",
        page(one('Algo completa <span class="g">1 ano</span> no dia 27.', "Ative o lembrete na contagem regressiva abaixo.") + '<div class="space" style="height:260px"></div>', "story"))

    # 19/11 caixinha
    add("2026-11-19", "foni_story_1ano_primeiro_iphone.jpg", "story",
        page(hero('Qual foi o seu <span class="g">primeiro iPhone?</span>', "Responda na caixinha. As melhores respostas a gente reposta.", mt=90), "story", badge="1 ANO DE FONI BR"))

    # 20/11 história
    add("2026-11-20", "foni_18h_1ano_historia.jpg", "feed",
        page(hero('27/11/2025.<br>O dia em que a <span class="g">Foni BR</span> nasceu.',
                  "Um ano depois, cada cliente que confiou na gente faz parte dessa história. Obrigado. Dia 27 tem mais.", mt=170), "feed"))
    add("2026-11-20", "foni_story_18h_1ano_historia.jpg", "story",
        page(hero('27/11/2025.<br>O dia em que a <span class="g">Foni BR</span> nasceu.', "", "TOQUE NO PERFIL PARA VER &rarr;", mt=90), "story", badge="NOVO POST"))

    # 21/11 enquete + chamada do reel
    add("2026-11-21", "foni_story_1ano_enquete.jpg", "story",
        page(hero('Qual iPhone você quer <span class="g">no dia 27?</span>', "Vote na enquete abaixo.", mt=90) + '<div class="space" style="height:300px"></div>', "story", badge="1 ANO"))
    add("2026-11-21", "foni_story_12h_1ano_numeros.jpg", "story",
        page(hero('Nosso primeiro ano <span class="g">em números.</span>', "180 aparelhos, +15 cidades, +40 trocas.", "TOQUE NO PERFIL PARA VER &rarr;", mt=90), "story", badge="NOVO REEL"))

    # 23/11 revelação (carrossel 5)
    rev = [
        page(hero('Nosso aniversário.<br><span class="g">Sua Black Friday.</span>', "De 27 a 30/11. Deslize para ver o presente.", mt=170), "feed", pg="01/05", swipe=True),
        page(item("20%", "OFF em todos os seminovos", "São <b>16 modelos</b>, do iPhone 11 ao iPhone 16 Pro Max, todos com <b>8 meses de garantia</b>.", "Estoque limitado por modelo."), "feed", pg="02/05"),
        page(item("+", "Kit 1 Ano em toda compra", "<b>Capa + película</b> de presente em qualquer aparelho comprado na campanha.", "Válido de 27 a 30/11."), "feed", pg="03/05"),
        page(item("%", "Cupom FONI1ANO no site", "Os mesmos <b>20% OFF</b> para quem compra pelo <b>fonibr.com.br</b>.", "O cupom não soma com o desconto da vitrine."), "feed", pg="04/05"),
        page(lista('Quer ver os preços <span class="g">antes de todo mundo?</span>',
                   ["Comente <b>VIP</b> neste post", "Ou chame no direct", "A lista VIP recebe a vitrine na noite de 26/11"],
                   "Vitrine aberta dia 27, às 07h43."), "feed", pg="05/05"),
    ]
    for i, h in enumerate(rev, 1):
        add("2026-11-23", f"foni_12h_1ano_revelacao_{i:02d}.jpg", "feed", h)
    sr = [
        ('Nosso aniversário.<br><span class="g">Sua Black Friday.</span>', "De 27 a 30/11."),
        ('<span class="g">20% OFF</span> em todos os seminovos.', "16 modelos, 8 meses de garantia."),
        ('<span class="g">Kit 1 Ano</span> em toda compra.', "Capa + película de presente."),
        ('Cupom <span class="g">FONI1ANO</span> no site.', "20% OFF no fonibr.com.br."),
    ]
    for i, (h, s) in enumerate(sr, 1):
        cta = "RESPONDA VIP PARA ENTRAR NA LISTA &rarr;" if i == 4 else ""
        add("2026-11-23", f"foni_story_12h_1ano_revelacao_{i:02d}.jpg", "story", page(hero(h, s, cta, mt=90), "story"))

    # 25/11 garantia (carrossel 5)
    gar = [
        page(hero('Por que seminovo <span class="g">na Foni BR?</span>', "Três motivos para comprar tranquilo.", mt=170), "feed", pg="01/05", swipe=True),
        page(item("01", "8 meses de garantia", "Todo seminovo sai com <b>8 meses de garantia</b>.", "Comprou, está coberto."), "feed", pg="02/05"),
        page(item("02", "Bateria informada", "A <b>saúde da bateria</b> de cada aparelho vem informada antes da compra.", "Você sabe exatamente o que está levando."), "feed", pg="03/05"),
        page(item("03", "Foni Upgrade", "<b>Recompra garantida</b> em até 12 meses. O valor vira crédito na troca por outro aparelho da Foni BR.", "Aparelho em bom estado."), "feed", pg="04/05"),
        page(lista('Dia 27, tudo isso com <span class="g">20% OFF.</span>',
                   ["16 modelos de seminovos", "Kit 1 Ano: capa + película", "Cupom FONI1ANO no site"],
                   "De 27 a 30/11."), "feed", pg="05/05"),
    ]
    for i, h in enumerate(gar, 1):
        add("2026-11-25", f"foni_18h_1ano_garantia_{i:02d}.jpg", "feed", h)
    add("2026-11-25", "foni_story_18h_1ano_garantia.jpg", "story",
        page(hero('Por que seminovo <span class="g">na Foni BR?</span>', "Garantia, bateria informada e Foni Upgrade.", "TOQUE NO PERFIL PARA VER &rarr;", mt=90), "story", badge="NOVO POST"))

    # 26/11 véspera
    add("2026-11-26", "foni_18h_1ano_vespera.jpg", "feed",
        page(hero('Amanhã,<br><span class="g">07h43.</span>', "A vitrine de aniversário abre amanhã cedo. Estoque limitado por modelo. A lista VIP recebe os preços hoje à noite.", mt=190), "feed"))
    add("2026-11-26", "foni_story_18h_1ano_vespera.jpg", "story",
        page(hero('Amanhã,<br><span class="g">07h43.</span>', "A vitrine de aniversário abre amanhã cedo.", "RESPONDA VIP PARA RECEBER OS PREÇOS HOJE &rarr;", mt=90), "story"))

    # 27/11 vitrine (carrossel 18)
    n = len(VITRINE) + 2
    vit = [page(one('A vitrine <span class="g">abriu.</span>', "Hoje a Foni BR faz um ano e o presente é seu. 20% OFF em todos os seminovos.", cls="h1xl"),
                "feed", badge="1 ANO", pg=f"01/{n:02d}", swipe=True)]
    for i, r in enumerate(VITRINE, 2):
        vit.append(page(modelo(*r), "feed", badge="VITRINE 1 ANO", pg=f"{i:02d}/{n:02d}"))
    vit.append(page(lista('Até 30/11 ou <span class="g">enquanto durar.</span>',
                          ["20% OFF em todos os seminovos", "8 meses de garantia", "Kit 1 Ano: capa + película",
                           "Cupom FONI1ANO no fonibr.com.br"], "Chame no direct ou compre pelo site."),
                    "feed", pg=f"{n:02d}/{n:02d}"))
    for i, h in enumerate(vit, 1):
        add("2026-11-27", f"foni_0743_1ano_vitrine_{i:02d}.jpg", "feed", h)
    add("2026-11-27", "foni_12h_1ano_tabela.jpg", "feed", page(tabela(), "feed", badge="VITRINE 1 ANO"))
    add("2026-11-27", "foni_story_0743_1ano_abertura.jpg", "story",
        page(one('A vitrine <span class="g">abriu.</span>', "20% OFF em todos os seminovos até 30/11.", "DESLIZE PARA VER OS MODELOS &rarr;"), "story"))
    for i, r in enumerate(VITRINE, 1):
        add("2026-11-27", f"foni_story_1ano_modelo_{i:02d}.jpg", "story", page(modelo(*r), "story", badge="VITRINE 1 ANO"))

    # 28/11 Foni Upgrade
    add("2026-11-28", "foni_12h_1ano_upgrade.jpg", "feed",
        page(hero('Seu iPhone antigo <span class="g">vira crédito.</span>',
                  "Comprou com a gente nos últimos 12 meses? Pelo Foni Upgrade ele vira crédito na troca por um mais novo. E até 30/11 o modelo novo sai com 20% OFF.",
                  mt=170), "feed", badge="FONI UPGRADE"))
    add("2026-11-28", "foni_story_12h_1ano_upgrade.jpg", "story",
        page(hero('Seu iPhone antigo <span class="g">vira crédito.</span>', "Troque pelo Foni Upgrade. Modelo novo com 20% OFF até 30/11.", "CHAME NO DIRECT &rarr;", mt=90), "story", badge="FONI UPGRADE"))

    # 29/11 domingo (exceção Black Friday)
    add("2026-11-29", "foni_story_12h_1ano_ate_amanha.jpg", "story",
        page(hero('Só até <span class="g">amanhã.</span>', "20% OFF em todos os seminovos, Kit 1 Ano e cupom FONI1ANO.", "CHAME NO DIRECT &rarr;", mt=90), "story"))

    # 30/11 último dia
    add("2026-11-30", "foni_0743_1ano_ultimo_dia.jpg", "feed",
        page(hero('Último <span class="g">dia.</span>', "A campanha de 1 ano termina hoje. Depois disso, os preços voltam ao normal.", "20% OFF em todos os seminovos até meia-noite.", mt=220), "feed"))
    add("2026-11-30", "foni_18h_1ano_meia_noite.jpg", "feed",
        page(hero('Até <span class="g">meia-noite.</span>', "Últimas horas de 20% OFF, Kit 1 Ano e cupom FONI1ANO.", "Chame no direct ou compre pelo site.", mt=220), "feed"))
    add("2026-11-30", "foni_story_1ano_ultimo_dia.jpg", "story",
        page(hero('Último dia.<br><span class="g">Até meia-noite.</span>', "20% OFF em todos os seminovos.", "CHAME NO DIRECT &rarr;", mt=90), "story"))

    # 01/12 agradecimento
    add("2026-12-01", "foni_12h_1ano_obrigado.jpg", "feed",
        page(one('Obrigado pelo <span class="g">primeiro ano.</span>', "Foram 12 meses e uma semana de aniversário que só aconteceram por causa de você. O ano 2 começa agora."), "feed"))
    add("2026-12-01", "foni_story_12h_1ano_obrigado.jpg", "story",
        page(one('Obrigado pelo <span class="g">primeiro ano.</span>', "O ano 2 começa agora."), "story"))
    return P


async def main():
    pecas = build()
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pages = {"feed": await b.new_page(viewport={"width": 1080, "height": 1350}),
                 "story": await b.new_page(viewport={"width": 1080, "height": 1920})}
        for d, nome, fmt, html in pecas:
            out = os.path.join(ROOT, "posts", d); os.makedirs(out, exist_ok=True)
            pg = pages[fmt]
            await pg.set_content(html, wait_until="load")
            await pg.screenshot(path=os.path.join(out, nome), type="jpeg", quality=95)
        await b.close()
    print(len(pecas), "peças")

if __name__ == "__main__":
    asyncio.run(main())
