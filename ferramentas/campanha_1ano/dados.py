"""Dados da campanha FONI BR 1 ANO (18/11 a 01/12/2026)."""

# Vitrine de aniversário: seminovos com R$ 300 OFF sobre o preço cheio (definido pelo dono em 18/11/2026: desconto fixo de R$ 300 em qualquer iPhone para manter lucro mínimo de R$ 700)
VITRINE = [
    ("iPhone 11",         "128 GB", "100%", "Branco",                                   2270, 1816),
    ("iPhone 13",         "128 GB", "100%", "Preto, Rosa e Branco",                     2630, 2104),
    ("iPhone 13 Pro",     "256 GB", "85%+", "Branco e Dourado",                         3400, 2720),
    ("iPhone 13 Pro Max", "128 GB", "100%", "Branco, Dourado, Preto e Azul",            3520, 2816),
    ("iPhone 14",         "128 GB", "100%", "Preto, Branco, Lilás e Azul",              2850, 2280),
    ("iPhone 14 Pro",     "128 GB", "85%+", "Prata e Dourado",                          3590, 2872),
    ("iPhone 14 Pro",     "256 GB", "85%+", "Preto",                                    3720, 2976),
    ("iPhone 14 Pro Max", "128 GB", "90%",  "Dourado e Branco",                         3900, 3120),
    ("iPhone 14 Pro Max", "256 GB", "90%",  "Preto e Roxo",                             4120, 3296),
    ("iPhone 15",         "128 GB", "85%+", "Preto e Azul",                             3450, 2760),
    ("iPhone 15 Pro",     "128 GB", "90%",  "Titânio Natural",                          4170, 3336),
    ("iPhone 15 Pro Max", "256 GB", "90%+", "Titânio Natural",                          4700, 3760),
    ("iPhone 16",         "128 GB", "87%+", "Preto, Rosa e Branco",                     4300, 3440),
    ("iPhone 16 Pro",     "128 GB", "89%+", "Titânio Deserto e Natural",                4820, 3856),
    ("iPhone 16 Pro",     "256 GB", "100%", "Titânio Deserto, Natural, Branco e Preto", 5120, 4096),
    ("iPhone 16 Pro Max", "256 GB", "85%+", "Titânio Natural e Deserto",                5570, 4456),
]

DESCONTO = 300
# recalcula o "por" a partir do preço cheio
VITRINE = [(m, g, b, c, de, de - DESCONTO) for m, g, b, c, de, _ in VITRINE]


def brl(v):
    return "R$ " + f"{v:,.0f}".replace(",", ".")
