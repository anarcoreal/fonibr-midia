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
ANTES = "Amanhã tem R$ 300 OFF em qualquer iPhone"
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

# As tarefas agendadas de 26 a 29/11 publicam pelos nomes ANTIGOS (não dá para mudar o texto delas desta conversa).
# Por isso os arquivos antigos foram SOBRESCRITOS com as artes novas (25/11/2026):
#   2026-11-26/foni_story_0743_produto_iphone16pro.jpg -> iPhone 14 (antes da campanha)
#   2026-11-27/foni_story_1ano_modelo_01 -> iPhone 14 | _02 -> iPhone 15 | _05 -> iPhone 17
#   2026-11-27/foni_story_1ano_modelo_11 -> 17 Pro Max | _13 -> 18 Pro Max | _16 -> 18 Pro
#   2026-11-27/foni_story_1ano_modelo_06 (sai 28/11) -> 17 Pro | _12 (sai 29/11) -> iPhone 17
