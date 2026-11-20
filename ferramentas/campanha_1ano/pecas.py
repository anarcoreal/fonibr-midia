"""Gera posts do feed (1080x1350) e stories (1080x1920) da campanha FONI BR 1 ANO.
Novo padrão visual (aprovado em 19/11/2026): capa centralizada com logo no topo e linha de luz,
sem etiqueta e sem rodapé em todo slide; slogan só no último slide; frases grandes sem ponto final.
Uso: python3 pecas.py  -> grava em ../../posts/<data>/ (a partir de 21/11; 20/11 só stories)
"""
import os, re, base64, asyncio
from playwright.async_api import async_playwright
from dados import VITRINE, brl

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
LOGO = base64.b64encode(open(os.path.join(ROOT, "marca", "logo_transparente.png"), "rb").read()).decode()
LOGO_URI = "data:image/png;base64," + LOGO
G1 = "#22C55E"   # verde da marca
GL = "#5CFF9A"   # brilho da linha de luz
DIM = "#8E8E93"

# peças aprovadas manualmente (ferramentas/novo_padrao/gerar.py) que não devem ser sobrescritas
PROTEGIDOS = {("2026-11-20", n) for n in
              [f"foni_12h_apple_watch_{i:02d}.jpg" for i in range(1, 6)] + ["foni_18h_1ano_historia.jpg"]}
INICIO = "2026-11-20"
EXTRA = {"foni_story_1ano_primeiro_iphone.jpg"}  # postado em 20/11


def titulo(h):
    """Frases grandes: sem ponto final; trecho final destacado vira segunda linha em cinza; demais destaques saem."""
    h = re.sub(r'\.(\s*(?:</span>)?\s*)(?=<br>|$)', r'\1', h.strip())
    h = re.sub(r'\.(\s*</span>)?\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ<])', lambda m: (m.group(1) or "") + "<br>", h)
    m = re.search(r'<span class="g">((?:(?!</span>).)*)</span>\s*$', h)
    if m:
        h = h[:m.start()] + f'<span class="tail">{m.group(1)}</span>'
    h = re.sub(r'<span class="g">((?:(?!</span>).)*)</span>', r'\1', h)
    return re.sub(r'<br>\s*(?=<span class="tail">)', '', h)


def streak(bottom, opacity=1.0, d="M-60 300 Q560 70 1140 230"):
    return (f'<svg class="glow" style="bottom:{bottom}px;opacity:{opacity}" width="1080" height="360" viewBox="0 0 1080 360">'
            f'<defs><linearGradient id="sg" x1="0" x2="1"><stop offset="0" stop-color="{GL}" stop-opacity="0"/>'
            f'<stop offset=".55" stop-color="{GL}"/><stop offset="1" stop-color="{GL}" stop-opacity="0"/></linearGradient>'
            f'<filter id="sb" x="-10%" y="-200%" width="120%" height="500%"><feGaussianBlur stdDeviation="14"/></filter></defs>'
            f'<path d="{d}" stroke="url(#sg)" stroke-width="22" fill="none" filter="url(#sb)" opacity=".75"/>'
            f'<path d="{d}" stroke="url(#sg)" stroke-width="3" fill="none"/></svg>')


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:%(H)dpx;background:#000;color:#fff;font-family:'Inter',sans-serif;overflow:hidden;position:relative}
.glow{position:absolute;left:0;width:1080px;height:360px;pointer-events:none}
.toplogo{position:absolute;top:%(LOGOTOP)dpx;left:0;right:0;display:flex;justify-content:center}
.toplogo img{width:330px}
.botlogo{position:absolute;bottom:%(BOT)dpx;left:0;right:0;display:flex;justify-content:center}
.botlogo img{width:220px;opacity:.9}
.slogan{position:absolute;bottom:%(BOT)dpx;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:26px}
.slogan img{width:300px}
.slogan span{font-size:24px;letter-spacing:.32em;font-weight:500;color:#BDBDBD}
.count{position:absolute;top:%(CTOP)dpx;right:96px;font-size:26px;letter-spacing:.12em;color:#5A5A5A}
.swipe{position:absolute;bottom:%(BOT)dpx;left:0;right:0;text-align:center;font-size:24px;letter-spacing:.24em;color:#6E6E6E;font-weight:500}
.tail{color:%(DIM)s;display:block}
h1{font-weight:600;letter-spacing:-0.045em;line-height:1.04}
b{font-weight:600;color:#fff}
.cover{position:absolute;left:80px;right:80px;top:%(CVTOP)dpx;bottom:%(CVBOT)dpx;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.cover h1{font-size:%(XL)dpx}
.cover h1.huge{font-size:%(HUGE)dpx;letter-spacing:-0.06em;line-height:.92}
.cover .sub{font-weight:400;font-size:%(SUB)dpx;color:#A8A8A8;line-height:1.35;margin-top:36px;max-width:880px}
.cover .cta{font-weight:500;font-size:%(CTA)dpx;color:#fff;margin-top:48px;line-height:1.35}
.cover .tap{font-weight:500;font-size:26px;letter-spacing:.2em;color:#8A8A8A;margin-top:70px}
.inner{position:absolute;left:96px;right:96px;top:%(INTOP)dpx}
.num{font-weight:200;font-size:200px;line-height:1;color:%(G1)s;letter-spacing:-0.04em}
.num.word{font-size:150px}
.inner h1{font-size:84px;margin-top:40px}
.inner h1.first{margin-top:0}
.body{font-weight:400;font-size:44px;line-height:1.38;margin-top:44px;color:#EDEDED}
.note{font-weight:400;font-size:32px;line-height:1.45;margin-top:36px;color:#8A8A8A}
.rows{margin-top:44px}
.rows div{font-size:36px;line-height:1.35;padding:22px 0;border-bottom:1px solid #1E1E1E;color:#E6E6E6}
.inner .cta{font-weight:500;font-size:36px;margin-top:44px;color:#fff;line-height:1.35}
.model h1{font-size:96px;margin-top:0}
.spec{font-weight:500;font-size:38px;margin-top:28px;color:#EDEDED}
.cores{font-weight:400;font-size:32px;color:#8A8A8A;margin-top:16px;line-height:1.35}
.de{font-weight:400;font-size:38px;color:#8A8A8A;margin-top:%(DEMT)dpx}
.de s{text-decoration-thickness:2px}
.por{font-weight:600;font-size:%(POR)dpx;color:%(G1)s;letter-spacing:-0.04em;line-height:1;margin-top:10px}
.off{font-weight:600;font-size:28px;letter-spacing:.24em;color:%(G1)s;margin-top:30px}
.perks{font-weight:400;font-size:30px;color:#A8A8A8;margin-top:36px;line-height:1.5}
table{width:100%%;border-collapse:collapse;margin-top:36px}
td,th{font-size:25px;padding:8px 0;border-bottom:1px solid #1A1A1A;text-align:left}
th{font-weight:500;color:#6E6E6E;letter-spacing:2px;font-size:20px}
td{font-weight:400;color:#DDD}
td.m{font-weight:600;color:#fff}
td.r,th.r{text-align:right}
td.p{font-weight:600;color:%(G1)s;text-align:right}
td.d{color:#6E6E6E;text-align:right}
"""

FEED = dict(H=1350, LOGOTOP=92, BOT=76, CTOP=104, CVTOP=200, CVBOT=150, XL=100, HUGE=300, SUB=38, CTA=36,
            INTOP=300, DEMT=70, POR=150, GLOWB=170, G1=G1, DIM=DIM)
STORY = dict(H=1920, LOGOTOP=260, BOT=300, CTOP=272, CVTOP=380, CVBOT=420, XL=112, HUGE=340, SUB=42, CTA=40,
             INTOP=420, DEMT=70, POR=170, GLOWB=400, G1=G1, DIM=DIM)


def _kind(pg):
    if not pg:
        return "cover"
    a, b = pg.split("/")
    return "cover" if a == "01" else ("last" if a == b else "inner")


def page(inner, fmt, badge=None, pg=None, swipe=False, kind=None):
    """badge é ignorado no novo padrão (sem etiqueta)."""
    P = FEED if fmt == "feed" else STORY
    kind = kind or _kind(pg)
    body = ""
    if kind == "cover":
        body += f'<div class="toplogo"><img src="{LOGO_URI}"></div>{streak(P["GLOWB"])}{inner}'
        if swipe:
            body += '<div class="swipe">DESLIZE</div>'
    elif kind == "tabela":
        body += f'<div class="toplogo"><img src="{LOGO_URI}" style="width:260px"></div>{inner}'
    else:
        body += f'<div class="count">{pg}</div>{streak(P["GLOWB"] - 20, .35, "M-60 320 Q560 200 1140 300")}{inner}'
        body += (f'<div class="slogan"><img src="{LOGO_URI}"><span>APPLE AO SEU ALCANCE.</span></div>' if kind == "last"
                 else f'<div class="botlogo"><img src="{LOGO_URI}"></div>')
    return f'<html><head><meta charset="utf-8"><style>{CSS % P}</style></head><body>{body}</body></html>'


def _cover(h1, sub="", cta="", huge=False):
    s = f'<p class="sub">{sub}</p>' if sub else ""
    c = ""
    if cta:
        plain = cta.replace("&rarr;", "").strip()
        c = f'<p class="tap">{plain}</p>' if plain.isupper() else f'<p class="cta">{cta}</p>'
    cls = ' class="huge"' if huge else ""
    return f'<div class="cover"><h1{cls}>{titulo(h1)}</h1>{s}{c}</div>'


def one(h1, sub="", cta="", cls="h1xl"):
    return _cover(h1, sub, cta)


def hero(h1, sub="", cta="", cls="h1xl", mt=150):
    return _cover(h1, sub, cta)


def item(num, title, body, note):
    word = " word" if not num.isdigit() or len(num) > 2 else ""
    return (f'<div class="inner"><div class="num{word}">{num}</div><h1>{titulo(title)}</h1>'
            f'<p class="body">{body}</p><p class="note">{note}</p></div>')


def lista(h1, items, cta="", mt=110):
    rows = "".join(f"<div>{x}</div>" for x in items)
    c = f'<p class="cta">{cta}</p>' if cta else ""
    return f'<div class="inner"><h1 class="first">{titulo(h1)}</h1><div class="rows">{rows}</div>{c}</div>'


def modelo(m, g, b, c, de, por):
    return (f'<div class="inner model"><h1>{m}</h1><div class="spec">{g} &nbsp;·&nbsp; Bateria {b}</div>'
            f'<div class="cores">{c}</div><div class="de">De <s>{brl(de)}</s> por</div>'
            f'<div class="por">{brl(por)}</div><div class="off">R$ 300 OFF</div>'
            f'<div class="perks">8 meses de garantia<br>Capa + película de brinde</div></div>')


def tabela():
    rows = "".join(
        f'<tr><td class="m">{m}</td><td>{g}</td><td>{b}</td><td class="d"><s>{brl(de)}</s></td><td class="p">{brl(por)}</td></tr>'
        for m, g, b, c, de, por in VITRINE)
    return (f'<div class="inner" style="top:200px"><h1 class="first" style="font-size:60px">Vitrine 1 ano'
            f'<span class="tail">R$ 300 OFF em qualquer iPhone</span></h1>'
            f'<table><tr><th>MODELO</th><th>ARMAZ.</th><th>BATERIA</th><th class="r">DE</th><th class="r">POR</th></tr>{rows}</table>'
            f'<p class="note" style="margin-top:22px;font-size:24px">8 meses de garantia e capa + película de brinde em toda compra. Até 30/11.</p></div>')


# ---------------------------------------------------------------- peças
def build():
    P = []  # (data, arquivo, fmt, html)
    def add(d, nome, fmt, html): P.append((d, nome, fmt, html))

    # 18/11 teaser
    add("2026-11-18", "foni_18h_1ano_teaser.jpg", "feed",
        page(one('Dia 27 a gente faz aniversário. <span class="g">Quem ganha presente é você.</span>', "Ative as notificações.", cls="h1l"), "feed"))
    add("2026-11-18", "foni_story_18h_1ano_teaser.jpg", "story",
        page(hero('Dia 27 a gente faz aniversário. <span class="g">Quem ganha presente é você.</span>', "Ative o lembrete na contagem regressiva abaixo.", mt=60), "story"))

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
        page(item("R$300", "OFF em qualquer iPhone", "Vale para os <b>16 seminovos</b>, do iPhone 11 ao 16 Pro Max, e para os <b>iPhones novos</b>.", "Estoque limitado por modelo."), "feed", pg="02/05"),
        page(item("+", "Capa + película de brinde", "Em <b>qualquer iPhone</b> comprado na campanha, novo ou seminovo.", "Válido de 27 a 30/11."), "feed", pg="03/05"),
        page(item("%", "Cupom FONI1ANO no site", "Os mesmos <b>R$ 300 OFF</b> para quem compra pelo <b>fonibr.com.br</b>.", "O cupom não soma com o desconto da vitrine."), "feed", pg="04/05"),
        page(lista('Quer ver os preços <span class="g">antes de todo mundo?</span>',
                   ["Comente <b>VIP</b> neste post", "Ou chame no direct", "A lista VIP recebe a vitrine na noite de 26/11"],
                   "Vitrine aberta dia 27, às 07h43."), "feed", pg="05/05"),
    ]
    for i, h in enumerate(rev, 1):
        add("2026-11-23", f"foni_12h_1ano_revelacao_{i:02d}.jpg", "feed", h)
    sr = [
        ('Nosso aniversário.<br><span class="g">Sua Black Friday.</span>', "De 27 a 30/11."),
        ('<span class="g">R$ 300 OFF</span> em qualquer iPhone.', "Novos e seminovos. 8 meses de garantia nos seminovos."),
        ('<span class="g">Capa + película</span> de brinde.', "Em qualquer iPhone da campanha."),
        ('Cupom <span class="g">FONI1ANO</span> no site.', "R$ 300 OFF no fonibr.com.br."),
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
        page(lista('Dia 27, tudo isso com <span class="g">R$ 300 OFF.</span>',
                   ["16 modelos de seminovos", "Capa + película de brinde", "Cupom FONI1ANO no site"],
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
    vit = [page(one('A vitrine <span class="g">abriu.</span>', "Hoje a Foni BR faz um ano e o presente é seu. R$ 300 OFF em qualquer iPhone.", cls="h1xl"),
                "feed", badge="1 ANO", pg=f"01/{n:02d}", swipe=True)]
    for i, r in enumerate(VITRINE, 2):
        vit.append(page(modelo(*r), "feed", badge="VITRINE 1 ANO", pg=f"{i:02d}/{n:02d}"))
    vit.append(page(lista('Até 30/11 ou <span class="g">enquanto durar.</span>',
                          ["R$ 300 OFF em qualquer iPhone", "8 meses de garantia", "Capa + película de brinde",
                           "Cupom FONI1ANO no fonibr.com.br"], "Chame no direct ou compre pelo site."),
                    "feed", pg=f"{n:02d}/{n:02d}"))
    for i, h in enumerate(vit, 1):
        add("2026-11-27", f"foni_0743_1ano_vitrine_{i:02d}.jpg", "feed", h)
    add("2026-11-27", "foni_12h_1ano_tabela.jpg", "feed", page(tabela(), "feed", kind="tabela"))
    add("2026-11-27", "foni_story_0743_1ano_abertura.jpg", "story",
        page(one('A vitrine <span class="g">abriu.</span>', "R$ 300 OFF em qualquer iPhone até 30/11.", "DESLIZE PARA VER OS MODELOS &rarr;"), "story"))
    for i, r in enumerate(VITRINE, 1):
        add("2026-11-27", f"foni_story_1ano_modelo_{i:02d}.jpg", "story", page(modelo(*r), "story", badge="VITRINE 1 ANO"))

    # 28/11 Foni Upgrade
    add("2026-11-28", "foni_12h_1ano_upgrade.jpg", "feed",
        page(hero('Seu iPhone antigo <span class="g">vira crédito.</span>',
                  "Comprou com a gente nos últimos 12 meses? Pelo Foni Upgrade ele vira crédito na troca por um mais novo. E até 30/11 o modelo novo sai com R$ 300 OFF.",
                  mt=170), "feed", badge="FONI UPGRADE"))
    add("2026-11-28", "foni_story_12h_1ano_upgrade.jpg", "story",
        page(hero('Seu iPhone antigo <span class="g">vira crédito.</span>', "Troque pelo Foni Upgrade. Modelo novo com R$ 300 OFF até 30/11.", "CHAME NO DIRECT &rarr;", mt=90), "story", badge="FONI UPGRADE"))

    # 29/11 domingo (exceção Black Friday)
    add("2026-11-29", "foni_story_12h_1ano_ate_amanha.jpg", "story",
        page(hero('Só até <span class="g">amanhã.</span>', "R$ 300 OFF em qualquer iPhone, capa + película de brinde e cupom FONI1ANO.", "CHAME NO DIRECT &rarr;", mt=90), "story"))

    # 30/11 último dia
    add("2026-11-30", "foni_0743_1ano_ultimo_dia.jpg", "feed",
        page(hero('Último <span class="g">dia.</span>', "A campanha de 1 ano termina hoje. Depois disso, os preços voltam ao normal.", "R$ 300 OFF em qualquer iPhone até meia-noite.", mt=220), "feed"))
    add("2026-11-30", "foni_18h_1ano_meia_noite.jpg", "feed",
        page(hero('Até <span class="g">meia-noite.</span>', "Últimas horas de R$ 300 OFF, capa + película de brinde e cupom FONI1ANO.", "Chame no direct ou compre pelo site.", mt=220), "feed"))
    add("2026-11-30", "foni_story_1ano_ultimo_dia.jpg", "story",
        page(hero('Último dia.<br><span class="g">Até meia-noite.</span>', "R$ 300 OFF em qualquer iPhone.", "CHAME NO DIRECT &rarr;", mt=90), "story"))

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
            if (d < INICIO and nome not in EXTRA) or (d, nome) in PROTEGIDOS:
                continue
            out = os.path.join(ROOT, "posts", d); os.makedirs(out, exist_ok=True)
            pg = pages[fmt]
            await pg.set_content(html, wait_until="load")
            await pg.screenshot(path=os.path.join(out, nome), type="jpeg", quality=95)
        await b.close()
    print(len(pecas), "peças")

if __name__ == "__main__":
    asyncio.run(main())
