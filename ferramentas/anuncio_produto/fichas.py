"""Fichas dos anúncios já montados (layout aprovado em 25/11/2026). Gera tudo com o gerar.py.

Uso:
  python3 fichas.py                 # lista as fichas
  python3 fichas.py iphone16 ...    # gera as fichas pedidas em previas/
  python3 fichas.py todas           # gera todas

PENDENTE = preço/condição/cores ainda não informados pelo Leonardo (não inventar).
Ao receber os dados: troque o "preco" (e "cond"/"cores" se mudar) e gere de novo.
Preço, cores e bateria dos iPhones vêm de estoque/precos.md.
"""
import os, sys, subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.join(AQUI, "..", "..", "produtos")
PROMO = "Dia 27: R$ 300 OFF em qualquer iPhone"  # campanha só de iPhone (27 a 30/11)
PENDENTE = "R$ ?.???"

FICHAS = {
    # ---------------- iPhones seminovos
    "iphone14": dict(modelo="iPhone 14", memoria="128 GB", bateria="100%", preco=2850,
                     cores="Preto, Branco, Lilás ou Azul", promo=PROMO, foto="iphone-14/iphone14_preto.png"),
    "iphone15": dict(modelo="iPhone 15", memoria="128 GB", bateria="85%+", preco=3450,
                     cores="Preto ou Azul", promo=PROMO, foto="iphone-15/iphone15_preto.png"),
    "iphone16": dict(modelo="iPhone 16", memoria="128 GB", bateria="87%+", preco=4300,
                     cores="Preto, Rosa ou Branco", promo=PROMO, foto="iphone-16/iphone16_preto.png"),
    # ---------------- iPhones novos (lacrados)
    "iphone17": dict(modelo="iPhone 17", cond="Novo", memoria="256 GB", bateria="Lacrado", rotulo2="Condição",
                     de="À vista, a partir de", preco=6380, cores="Preto, Branco, Azul, Verde ou Lavanda", garantia="",
                     promo=PROMO, foto="iphone-17/iphone17_preto.png"),
    "iphone17pro": dict(modelo="iPhone 17 Pro", cond="Novo", memoria="256 GB", bateria="Lacrado", rotulo2="Condição",
                        preco=8100, cores="Laranja:#f07a2a", garantia="", promo=PROMO, tamanho="pro",
                        foto="iphone-17-pro/iphone17pro_laranja.png"),
    "iphone17promax": dict(modelo="iPhone 17 Pro Max", cond="Novo", memoria="256 GB", bateria="Lacrado", rotulo2="Condição",
                           de="À vista, a partir de", preco=8450, cores="Laranja:#f07a2a, Azul:#2f4a7a ou Prata",
                           garantia="", promo=PROMO, tamanho="promax", foto="iphone-17-pro/iphone17pro_azul.png"),
    "iphone18pro": dict(modelo="iPhone 18 Pro", cond="Novo", memoria="256 GB", bateria="Lacrado", rotulo2="Condição",
                        de="À vista, a partir de", preco=9100, cores="Preto, Prata, Glacier:#b7cbe0 ou Burgundy:#6e2335",
                        garantia="", promo=PROMO, tamanho="pro", esticar=1.05, foto="iphone-18-pro/iphone18pro_burgundy.png"),
    "iphone18promax": dict(modelo="iPhone 18 Pro Max", cond="Novo", memoria="256 GB", bateria="Lacrado", rotulo2="Condição",
                           de="À vista, a partir de", preco=9700, cores="Preto, Prata, Glacier:#b7cbe0 ou Burgundy:#6e2335",
                           garantia="", promo=PROMO, tamanho="promax", esticar=1.05, foto="iphone-18-pro/iphone18pro_glacier.png"),
    # ---------------- PENDENTES (layout aprovado, aguardando preço, condição e cores)
    "macbookneo": dict(modelo="MacBook Neo", cond="13 polegadas", specs="A18 Pro:Chip|8 GB:Memória|256 GB:SSD",
                       preco=PENDENTE, cores="Prata, Rosa:#f2b8c6, Amarelo:#e8e48c ou Índigo:#4f5290", garantia="",
                       tamanho="mac", foto="macbook-neo/macbookneo_prata.png"),
    "macbookneo_grande": dict(modelo="MacBook Neo", cond="13 polegadas", specs="A18 Pro:Chip|8 GB:Memória|256 GB:SSD",
                              preco=PENDENTE, cores="Prata, Rosa:#f2b8c6, Amarelo:#e8e48c ou Índigo:#4f5290", garantia="",
                              tamanho="mac_grande", foto="macbook-neo/macbookneo_prata.png"),
    "watchultra4": dict(modelo="Apple Watch Ultra 4", cond="GPS + Cellular", specs="49 mm:Caixa|Titânio:Material",
                        preco=PENDENTE, cores="Natural:#c9c2b6 ou Preto", garantia="", tamanho="pro", esfumar=True,
                        foto="apple-watch-ultra-4/watchultra4_natural.png"),
    "watchs12": dict(modelo="Apple Watch Series 12", cond="GPS", specs="46 mm:Caixa", preco=PENDENTE,
                     cores="Cinza:#5a5a5e, Preto, Estelar:#e6dccb ou Bronze:#7a6352", garantia="", tamanho="pro",
                     esfumar=True, foto="apple-watch-s12/watchs12_bronze.png"),
    "fonte_cabo_usbc": dict(modelo="Fonte + Cabo USB-C", cond="Carregador completo", specs="USB-C:Fonte|USB-C para USB-C:Cabo",
                            preco=PENDENTE, cores="Branco", garantia="", tamanho="mac",
                            foto="fonte-cabo-usbc/fonte_cabo_usbc.png"),
}


def gerar(nome, saida_dir):
    f = dict(FICHAS[nome])
    args = [sys.executable, os.path.join(AQUI, "gerar.py"),
            "--foto", os.path.join(PROD, f.pop("foto")),
            "--saida", os.path.join(saida_dir, f"anuncio_{nome}.jpg")]
    for k, v in f.items():
        if k == "esfumar":
            args += ["--esfumar"] if v else []
        else:
            args += [f"--{k}", str(v)]
    subprocess.run(args, check=True)


if __name__ == "__main__":
    pedidos = sys.argv[1:]
    if not pedidos:
        for n, f in FICHAS.items():
            print(f"{n:20s} {'PENDENTE' if f['preco'] == PENDENTE else f['preco']}")
        sys.exit()
    if pedidos == ["todas"]:
        pedidos = list(FICHAS)
    out = os.path.join(AQUI, "previas"); os.makedirs(out, exist_ok=True)
    for n in pedidos:
        gerar(n, out)
