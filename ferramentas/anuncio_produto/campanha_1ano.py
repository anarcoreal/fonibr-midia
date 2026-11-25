"""Stories de produto da campanha 1 Ano (26 a 29/11/2026) no PADRÃO OFICIAL de anúncio (aprovado em 25/11/2026).

Regra do Leonardo (25/11/2026): anúncio com preço só sobe no formato aprovado hoje. Os stories antigos
(foni_story_1ano_modelo_XX, foni_story_0743_produto_*) não são mais publicados. Só entram modelos com foto
em produtos/ e preço em estoque/precos.md.

Uso: python3 campanha_1ano.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fichas import FICHAS, PROD, AQUI
import subprocess

POSTS = os.path.join(AQUI, "..", "..", "posts")
OFF = 300
ANTES = "Dia 27: R$ 300 OFF em qualquer iPhone"
DURANTE = "Até 30/11 ou enquanto durar o estoque"

# (data, arquivo, ficha, durante a campanha?)
GRADE = [
    ("2026-11-26", "foni_story_0743_anuncio_iphone14.jpg", "iphone14", False),
    ("2026-11-27", "foni_story_0743_anuncio_iphone14.jpg", "iphone14", True),
    ("2026-11-27", "foni_story_0743_anuncio_iphone15.jpg", "iphone15", True),
    ("2026-11-27", "foni_story_18h_anuncio_iphone17.jpg", "iphone17", True),
    ("2026-11-27", "foni_story_18h_anuncio_iphone17promax.jpg", "iphone17promax", True),
    ("2026-11-27", "foni_story_18h_anuncio_iphone18promax.jpg", "iphone18promax", True),
    ("2026-11-28", "foni_story_0743_anuncio_iphone18pro.jpg", "iphone18pro", True),
    ("2026-11-29", "foni_story_0743_anuncio_iphone17pro.jpg", "iphone17pro", True),
]


def gerar(data, nome, ficha, durante):
    f = dict(FICHAS[ficha])
    if durante:
        f["preco"] = float(f["preco"]) - OFF
        f["de"] = "À vista, com R$ 300 OFF" + (", a partir de" if "a partir" in f.get("de", "") else "")
        f["promo"] = DURANTE
    else:
        f["promo"] = ANTES
    out = os.path.join(POSTS, data); os.makedirs(out, exist_ok=True)
    args = [sys.executable, os.path.join(AQUI, "gerar.py"), "--foto", os.path.join(PROD, f.pop("foto")),
            "--saida", os.path.join(out, nome)]
    for k, v in f.items():
        args += (["--esfumar"] if v else []) if k == "esfumar" else [f"--{k}", str(v)]
    subprocess.run(args, check=True)


if __name__ == "__main__":
    for g in GRADE:
        gerar(*g)
