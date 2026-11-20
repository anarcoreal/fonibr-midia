"""Capas aprovadas em 20/11/2026 (rodar DEPOIS de pecas.py e pauta.py, sobrescreve as capas automáticas).
Foni BR — sistema editorial: uma margem, um alinhamento (esquerda), uma escala tipográfica.
A variação vem da posição vertical do bloco e da linha de luz, não de alinhamentos diferentes."""
import os, sys, asyncio
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "ferramentas", "campanha_1ano"))
from pecas import LOGO_URI
from playwright.async_api import async_playwright


G = "#30D158"; GL = "#5CFF9A"
M = 96  # margem única
CSS = f"""*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;background:#000;color:#F5F5F7;font-family:'Inter',sans-serif;overflow:hidden;position:relative;-webkit-font-smoothing:antialiased}}
.a{{position:absolute}}
.blk{{position:absolute;left:{M}px;right:{M}px}}
.eb{{font-size:24px;letter-spacing:.2em;font-weight:500;color:#8E8E93;text-transform:uppercase}}
.eb.g{{color:{G};letter-spacing:.04em;text-transform:none;font-size:28px}}
.dp{{font-size:210px;font-weight:300;letter-spacing:-0.055em;line-height:.95;white-space:nowrap;margin-top:28px}}
.hd{{font-size:80px;font-weight:600;letter-spacing:-0.04em;line-height:1.06;margin-top:28px}}
.hd .t{{display:block;color:#86868B}}
.bd{{font-size:34px;font-weight:400;line-height:1.45;color:#A1A1A6;margin-top:32px;max-width:820px}}
.rows{{margin-top:44px}} .rows div{{display:flex;justify-content:space-between;align-items:baseline;padding:22px 0;border-bottom:1px solid #1C1C1E;font-size:34px}}
.rows b{{font-weight:600}} .rows span{{color:#8E8E93;font-size:30px}}
"""
LOGO = f'<div class="a" style="left:{M}px;top:{M}px"><img src="{LOGO_URI}" style="width:200px;display:block"></div>'
def cnt(t): return f'<div class="a" style="right:{M}px;top:{M + 4}px;font-size:24px;letter-spacing:.12em;color:#48484A">{t}</div>'

_i = [0]
def luz(kind, op=1.0):
    if not kind: return ""
    d = {"base": "M-60 1150 Q540 1010 1140 1090", "meio": "M-60 760 Q560 610 1140 700",
         "topo": "M-60 330 Q500 150 1140 120", "lado": "M1000 160 Q900 700 1010 1400"}[kind]
    _i[0] += 1; i = _i[0]
    return (f'<svg class="a" style="left:0;top:0;opacity:{op}" width="1080" height="1350" viewBox="0 0 1080 1350" aria-hidden="true">'
            f'<defs><linearGradient id="g{i}" x1="0" x2="1"><stop offset="0" stop-color="{GL}" stop-opacity="0"/><stop offset=".55" stop-color="{GL}"/>'
            f'<stop offset="1" stop-color="{GL}" stop-opacity="0"/></linearGradient><filter id="f{i}" x="-20%" y="-20%" width="140%" height="140%">'
            f'<feGaussianBlur stdDeviation="14"/></filter></defs><path d="{d}" stroke="url(#g{i})" stroke-width="20" fill="none" filter="url(#f{i})" opacity=".6"/>'
            f'<path d="{d}" stroke="url(#g{i})" stroke-width="2.5" fill="none"/></svg>')
def brilho(op=.8):
    sp = [(-200, 980, "#1DB33C", .5), (260, 1100, "#F2C230", .25), (560, 1040, "#2F6BEA", .42)]
    return ('<div class="a" style="inset:0;filter:blur(140px);opacity:%s">' % op +
            "".join(f'<div class="a" style="left:{x}px;top:{y}px;width:560px;height:520px;border-radius:50%;background:{c};opacity:{o}"></div>' for x, y, c, o in sp) + "</div>")

def peca(eb="", dp="", dp_cor="", hd="", t="", bd="", pos="baixo", fundo="", extra="", ebg=False, contador=""):
    dpx = f'<div class="dp" style="color:{dp_cor or "#F5F5F7"}">{dp}</div>' if dp else ""
    hdx = f'<div class="hd">{hd}{f"<span class=t>{t}</span>" if t else ""}</div>' if hd else ""
    bdx = f'<p class="bd">{bd}</p>' if bd else ""
    ebx = f'<div class="eb{" g" if ebg else ""}">{eb}</div>' if eb else ""
    where = {"baixo": "bottom:150px", "topo": "top:300px", "meio": "top:50%;transform:translateY(-50%)"}[pos]
    return (f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{fundo}{LOGO}{cnt(contador) if contador else ''}"
            f'<div class="blk" style="{where}">{ebx}{dpx}{hdx}{bdx}{extra}</div></body></html>')

S = {}
# carrossel Apple Watch
S["aw_01"] = peca("Apple Watch", "SOS", "", "Ele pede ajuda", "por você", "Três recursos para ativar hoje.", "baixo", luz("topo"))
S["aw_02"] = peca("01 · Detecção de Queda", hd="Caiu?", t="Ele pergunta se você está bem", bd="Sem resposta, ele liga para a emergência e avisa seus contatos.", pos="topo", fundo=luz("base", .5), ebg=True, contador="02/05")
S["aw_03"] = peca("02 · SOS de Emergência", hd="Segure o", t="botão lateral", bd="Ele liga para a emergência e envia a sua localização para os contatos.", pos="meio", fundo=luz("lado", .7), ebg=True, contador="03/05")
S["aw_04"] = peca("03 · Alertas do coração", hd="Ele avisa quando", t="o coração sai do ritmo", bd="Frequência alta, baixa e ritmo irregular. Os recursos variam conforme o modelo.", pos="baixo", fundo=luz("topo", .5), ebg=True, contador="04/05")
rows = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in [("Detecção de Queda", "SOS de Emergência"), ("Contatos", "Saúde &gt; Ficha Médica"), ("Coração", "Apple Watch &gt; Coração")])
S["aw_05"] = peca("Como ativar", hd="Configure pelo iPhone", bd="No app Apple Watch, em poucos toques.", pos="topo", fundo=luz("base", .4), contador="05/05",
                  extra=f'<div class="rows">{rows}</div><div style="margin-top:70px;font-size:22px;letter-spacing:.3em;color:#8E8E93">APPLE AO SEU ALCANCE.</div>')
# capas da semana
S["c_macbook"] = peca("MacBook", hd="Air ou Pro?", t="Qual é para você", bd="Três diferenças que importam na escolha.", pos="baixo", fundo=luz("topo"))
S["c_historia"] = peca("27/11/2025", "1 ano", "", "O dia em que", "a Foni BR nasceu", "Obrigado a cada cliente que confiou na gente.", "meio", luz("base"))
S["c_camera"] = peca("Câmera do iPhone", hd="Quatro recursos", t="que pouca gente usa", bd="Salve e teste hoje.", pos="topo", fundo=luz("base"))
S["c_revelacao"] = peca("27 a 30/11 · 1 ano de Foni BR", "R$ 300", "", "OFF em qualquer iPhone", "", "Novos e seminovos.", "topo", brilho())
S["c_tipos"] = peca("Antes de comprar", hd="Lacrado, seminovo", t="ou recondicionado", bd="Entenda a diferença. Deslize.", pos="baixo", fundo=luz("meio", .8))
S["c_primeiro"] = peca("Curiosidade Apple", "2007", G, "O primeiro iPhone", "não tinha App Store", "", "topo", luz("base", .4))
S["c_ipad"] = peca("iPad para estudar", hd="Quatro usos", t="que fazem diferença", bd="Salve para a próxima prova.", pos="meio", fundo=luz("lado", .7))
S["c_garantia"] = peca("Seminovo Foni BR", "8 meses", "", "de garantia", "", "A lei exige 90 dias.", "topo", luz("base"))
S["c_roubado"] = peca("Proteção de Dispositivo Roubado", "1 hora", "", "é o que o ladrão espera", "para trocar sua senha", "", "baixo", luz("topo", .8))
S["c_magsafe"] = peca("Curiosidade Apple", "2006", G, "O MagSafe nasceu", "no MacBook", "", "baixo", luz("topo", .4))
S["c_vespera"] = peca("Amanhã", "07h43", "", "a vitrine abre", "", "Vitrine de aniversário. Estoque limitado por modelo.", "meio", brilho(.7))

DEST = {"aw_01": "2026-11-20/foni_12h_apple_watch_01", "aw_02": "2026-11-20/foni_12h_apple_watch_02",
        "aw_03": "2026-11-20/foni_12h_apple_watch_03", "aw_04": "2026-11-20/foni_12h_apple_watch_04",
        "aw_05": "2026-11-20/foni_12h_apple_watch_05", "c_historia": "2026-11-20/foni_18h_1ano_historia",
        "c_macbook": "2026-11-20/foni_0743_macbook_01", "c_camera": "2026-11-23/foni_0743_camera_01",
        "c_revelacao": "2026-11-23/foni_12h_1ano_revelacao_01", "c_tipos": "2026-11-24/foni_0743_tipos_iphone_01",
        "c_primeiro": "2026-11-24/foni_12h_curiosidade_primeiro_iphone_01", "c_ipad": "2026-11-25/foni_0743_ipad_estudo_01",
        "c_garantia": "2026-11-25/foni_18h_1ano_garantia_01", "c_roubado": "2026-11-26/foni_0743_dispositivo_roubado_01",
        "c_magsafe": "2026-11-26/foni_12h_curiosidade_magsafe_01", "c_vespera": "2026-11-26/foni_18h_1ano_vespera"}


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for k, h in S.items():
            await pg.set_content(h); await pg.wait_for_timeout(120)
            await pg.screenshot(path=f"{ROOT}/posts/{DEST[k]}.jpg", type="jpeg", quality=93)
        await b.close()
    print(len(S), "capas aprovadas gravadas")

asyncio.run(main())
