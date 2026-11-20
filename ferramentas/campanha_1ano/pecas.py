"""Gera posts do feed (1080x1350) e stories (1080x1920) da campanha FONI BR 1 ANO.
Sistema editorial (aprovado em 20/11/2026): uma margem (96px), tudo alinhado à esquerda, uma escala de texto;
logo pequena no alto à esquerda; variação só na altura do bloco e na linha de luz; frases grandes sem ponto final.
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
PROTEGIDOS = set()  # as capas aprovadas vêm de ferramentas/novo_padrao/capas_aprovadas.py
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


G2 = "#30D158"
M = 96


def luz(kind, H, op=1.0):
    if not kind:
        return ""
    k = H / 1350
    d = {"base": f"M-60 {H-200} Q540 {H-340} 1140 {H-260}", "meio": f"M-60 {int(760*k)} Q560 {int(610*k)} 1140 {int(700*k)}",
         "topo": f"M-60 {int(330*k)} Q500 {int(150*k)} 1140 {int(120*k)}", "lado": f"M1000 160 Q900 {H//2} 1010 {H+50}"}[kind]
    return (f'<svg class="glow" width="1080" height="{H}" viewBox="0 0 1080 {H}" style="opacity:{op}">'
            f'<defs><linearGradient id="sg" x1="0" x2="1"><stop offset="0" stop-color="{GL}" stop-opacity="0"/>'
            f'<stop offset=".55" stop-color="{GL}"/><stop offset="1" stop-color="{GL}" stop-opacity="0"/></linearGradient>'
            f'<filter id="sb" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter></defs>'
            f'<path d="{d}" stroke="url(#sg)" stroke-width="20" fill="none" filter="url(#sb)" opacity=".6"/>'
            f'<path d="{d}" stroke="url(#sg)" stroke-width="2.5" fill="none"/></svg>')


def brilho(op=.8):
    sp = [(-200, 980, "#1DB33C", .5), (260, 1100, "#F2C230", .25), (560, 1040, "#2F6BEA", .42)]
    return ('<div style="position:absolute;inset:0;filter:blur(140px);opacity:%s">' % op +
            "".join(f'<div style="position:absolute;left:{x}px;top:{y}px;width:560px;height:520px;border-radius:50%;background:{c};opacity:{o}"></div>'
                    for x, y, c, o in sp) + "</div>")


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:%(H)dpx;background:#000;color:#F5F5F7;font-family:'Inter',sans-serif;overflow:hidden;position:relative;-webkit-font-smoothing:antialiased}
.glow{position:absolute;left:0;top:0;pointer-events:none}
.logo{position:absolute;left:96px;top:%(LT)dpx}.logo img{width:200px;display:block}
.count{position:absolute;right:96px;top:%(CT)dpx;font-size:24px;letter-spacing:.12em;color:#48484A}
.blk{position:absolute;left:96px;right:96px}
.eb{font-size:24px;letter-spacing:.2em;font-weight:500;color:#8E8E93;text-transform:uppercase}
.eb.g{color:%(G2)s;letter-spacing:.04em;text-transform:none;font-size:28px}
.dp{font-size:210px;font-weight:300;letter-spacing:-0.055em;line-height:.95;white-space:nowrap;margin-top:28px}
h1{font-size:%(HD)dpx;font-weight:600;letter-spacing:-0.04em;line-height:1.06;margin-top:28px}
h1.first{margin-top:0}
.tail{display:block;color:#86868B}
.bd{font-size:34px;font-weight:400;line-height:1.45;color:#A1A1A6;margin-top:32px;max-width:840px}
.bd.w{color:#E5E5EA}
.bd b{color:#F5F5F7;font-weight:600}
.note{font-size:28px;font-weight:400;line-height:1.45;color:#6E6E73;margin-top:20px;max-width:840px}
.tap{font-size:24px;letter-spacing:.2em;font-weight:500;color:#8E8E93;margin-top:56px;text-transform:uppercase}
.cta{font-size:34px;font-weight:500;color:#F5F5F7;margin-top:40px}
.rows{margin-top:40px}.rows div{padding:22px 0;border-bottom:1px solid #1C1C1E;font-size:34px;color:#E5E5EA}
.slogan{font-size:22px;letter-spacing:.3em;color:#8E8E93;margin-top:64px}
.spec{font-size:34px;font-weight:500;margin-top:20px;color:#E5E5EA}
.cores{font-size:28px;color:#8E8E93;margin-top:10px}
.de{font-size:34px;color:#8E8E93;margin-top:60px}
.por{font-size:170px;font-weight:300;letter-spacing:-0.05em;line-height:1;color:%(G2)s;margin-top:6px;white-space:nowrap}
.off{font-size:24px;letter-spacing:.2em;font-weight:500;color:%(G2)s;margin-top:24px}
.perks{font-size:30px;color:#A1A1A6;margin-top:30px;line-height:1.5}
table{width:100%%;border-collapse:collapse;margin-top:30px}
td,th{font-size:25px;padding:8px 0;border-bottom:1px solid #1C1C1E;text-align:left}
th{font-weight:500;color:#6E6E73;letter-spacing:2px;font-size:19px}
td{color:#D1D1D6}td.m{font-weight:600;color:#F5F5F7}td.r,th.r{text-align:right}
td.p{font-weight:600;color:%(G2)s;text-align:right}td.d{color:#6E6E73;text-align:right}
"""

FEED = dict(H=1350, LT=96, CT=100, HD=80, G2=G2)
STORY = dict(H=1920, LT=250, CT=254, HD=88, G2=G2)

# a variação vem só da altura do bloco e da linha de luz
CAPAS = [("baixo", "topo"), ("topo", "base"), ("meio", "lado"), ("baixo", "meio"), ("topo", "base")]
DENTRO = [("topo", "base"), ("meio", "lado"), ("baixo", "topo")]
_n = [0]


def _kind(pg):
    if not pg:
        return "cover"
    a, b = pg.split("/")
    return "cover" if a == "01" else ("last" if a == b else "inner")


def _pos(where, H):
    if where == "baixo":
        return f"bottom:{150 if H == 1350 else 520}px"
    if where == "topo":
        return f"top:{300 if H == 1350 else 460}px"
    return "top:50%;transform:translateY(-50%)"


def page(inner, fmt, badge=None, pg=None, swipe=False, kind=None):
    P = FEED if fmt == "feed" else STORY
    H = P["H"]
    kind = kind or _kind(pg)
    eb = f'<div class="eb">{badge}</div>' if badge and kind == "cover" else ""
    if fmt == "story":
        where, lz = "meio", ("base" if _n[0] % 2 else "topo")
    elif kind == "cover":
        where, lz = CAPAS[_n[0] % len(CAPAS)]
    elif kind == "tabela":
        where, lz = "topo", None
    else:
        i = int(pg.split("/")[0]) if pg else 0
        where, lz = ("topo", "base") if kind == "last" else DENTRO[i % len(DENTRO)]
    _n[0] += 1
    inner = inner.replace("<!--EB-->", eb)
    if kind == "tabela":
        blk = f'<div class="blk" style="top:220px">{inner}</div>'
    else:
        blk = f'<div class="blk" style="{_pos(where, H)}">{inner}</div>'
    cnt = f'<div class="count">{pg}</div>' if pg and kind != "cover" else ""
    glow = brilho() if (fmt == "feed" and badge and "1 ANO" in badge.upper() and kind == "cover") else luz(lz, H, .5 if kind == "inner" else .9)
    return (f'<html><head><meta charset="utf-8"><style>{CSS % P}</style></head><body>{glow}'
            f'<div class="logo"><img src="{LOGO_URI}"></div>{cnt}{blk}</body></html>')


def _cover(h1, sub="", cta=""):
    s = f'<p class="bd">{sub}</p>' if sub else ""
    c = ""
    if cta:
        plain = cta.replace("&rarr;", "").strip()
        c = f'<p class="tap">{plain}</p>' if plain.isupper() else f'<p class="cta">{cta}</p>'
    return f'<!--EB--><h1>{titulo(h1)}</h1>{s}{c}'


def one(h1, sub="", cta="", cls="h1xl"):
    return _cover(h1, sub, cta)


def hero(h1, sub="", cta="", cls="h1xl", mt=150):
    return _cover(h1, sub, cta)


def item(num, title, body, note):
    return (f'<div class="eb g">{num}</div><h1>{titulo(title)}</h1>'
            f'<p class="bd w">{body}</p><p class="note">{note}</p>')


def lista(h1, items, cta="", mt=110):
    rows = "".join(f"<div>{x}</div>" for x in items)
    c = f'<p class="cta">{cta}</p>' if cta else ""
    return f'<h1 class="first">{titulo(h1)}</h1><div class="rows">{rows}</div>{c}<div class="slogan">APPLE AO SEU ALCANCE.</div>'


def modelo(m, g, b, c, de, por):
    return (f'<div class="eb">Vitrine 1 ano</div><h1>{m}</h1><div class="spec">{g} · Bateria {b}</div>'
            f'<div class="cores">{c}</div><div class="de">De <s>{brl(de)}</s> por</div>'
            f'<div class="por">{brl(por)}</div><div class="off">R$ 300 OFF</div>'
            f'<div class="perks">8 meses de garantia<br>Capa + película de brinde</div>')


def tabela():
    rows = "".join(
        f'<tr><td class="m">{m}</td><td>{g}</td><td>{b}</td><td class="d"><s>{brl(de)}</s></td><td class="p">{brl(por)}</td></tr>'
        for m, g, b, c, de, por in VITRINE)
    return (f'<div class="eb">Vitrine 1 ano</div><h1 style="font-size:60px">R$ 300 OFF em qualquer iPhone</h1>'
            f'<table><tr><th>MODELO</th><th>ARMAZ.</th><th>BATERIA</th><th class="r">DE</th><th class="r">POR</th></tr>{rows}</table>'
            f'<p class="note" style="font-size:24px">8 meses de garantia e capa + película de brinde em toda compra. Até 30/11.</p>')


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
    # 01/12 story do reel de AirPods (antes sem gerador)
    add("2026-12-01", "foni_story_18h_airpods.jpg", "story",
        page(hero('Seus AirPods <span class="g">traduzem conversas ao vivo.</span>', "Veja 3 funções que pouca gente usa.",
                  "TOQUE NO PERFIL PARA VER &rarr;"), "story", badge="NOVO REEL"))
    # a pergunta do primeiro iPhone foi para 20/11
    add("2026-11-20", "foni_story_1ano_primeiro_iphone.jpg", "story",
        page(hero('Qual foi o seu <span class="g">primeiro iPhone?</span>', "Responda na caixinha. As melhores respostas a gente reposta."), "story", badge="1 ANO DE FONI BR"))
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
