"""Pauta normal de 19 a 30/11/2026 (conteúdo, sem preço). Usa os templates da campanha 1 ano.
Uso: python3 pauta.py
"""
import os, sys, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "campanha_1ano"))
from playwright.async_api import async_playwright
from pecas import page, hero, item, lista, ROOT
import reels

G = '<span class="g">{}</span>'.format
FOLLOW = "Siga @fonibroficial para mais."


def carrossel(badge, slides):
    n = len(slides)
    out = []
    for i, s in enumerate(slides, 1):
        out.append(page(s, "feed", badge=badge, pg=f"{i:02d}/{n:02d}", swipe=(i == 1)))
    return out


def final_foni(h1, cta=FOLLOW):
    return lista(h1, ["8 meses de garantia nos seminovos", "Saúde da bateria informada em cada aparelho",
                      "Foni Upgrade: recompra garantida em até 12 meses"], cta)


def story(badge, h1, sub=""):
    return page(hero(h1, sub, "TOQUE NO PERFIL PARA VER &rarr;", mt=90), "story", badge=badge)


POSTS = []  # (data, nome_base, [htmls]) ; reels: (data, nome, scenes)
REELS = []
STORIES = []


def post(d, nome, badge, slides, st_h1, st_sub=""):
    POSTS.append((d, nome, carrossel(badge, slides)))
    STORIES.append((d, nome.replace("foni_", "foni_story_"), story("NOVO POST", st_h1, st_sub)))


def reel(d, nome, scenes, st_h1, st_sub=""):
    REELS.append((d, nome, scenes))
    STORIES.append((d, nome.replace("foni_reel_", "foni_story_"), story("NOVO REEL", st_h1, st_sub)))


def rs(badge, h, sub=""):
    b = f'<span class="badge">{badge}</span>' if badge else ""
    s = f'<div class="sub">{sub}</div>' if sub else ""
    return f'{b}<div class="h">{h}</div>{s}'


def rfinal():
    return (f'<div class="h">Siga para <span class="g">mais dicas.</span></div><div class="cta">@fonibroficial</div>'
            f'<img class="logo" src="data:image/png;base64,{reels.LOGO}"><div class="line"></div>')


# ------------------------------------------------------------------ 19/11
post("2026-11-19", "foni_0743_bateria", "BATERIA", [
    hero(f'Cinco hábitos que {G("preservam a bateria")} do seu iPhone.', "Salve este post para não esquecer."),
    item("01", "Carregamento otimizado", "Em <b>Ajustes &gt; Bateria</b>, mantenha o Carregamento Otimizado ativo.", "O iPhone aprende sua rotina e segura a carga final até perto da hora de usar."),
    item("02", "Fuja do calor", "Evite carregar no sol, no painel do carro ou jogando pesado na tomada.", "Temperatura alta desgasta a bateria mais rápido que o uso."),
    item("03", "Carregador de procedência", "Use cabos e carregadores <b>originais ou certificados</b>.", "Carregador sem procedência pode aquecer e danificar o aparelho."),
    item("04", "Não espere zerar", "Não precisa chegar a 0% para carregar.", "Baterias de lítio preferem cargas parciais ao longo do dia."),
    item("05", "iOS atualizado", "Atualizações trazem ajustes no gerenciamento de energia.", "Em Ajustes &gt; Geral &gt; Atualização de Software."),
    final_foni(f'Na Foni BR, a bateria {G("vem informada.")}'),
], f'Cinco hábitos que {G("preservam a bateria.")}')

post("2026-11-19", "foni_12h_curiosidade_941", "CURIOSIDADE", [
    hero(f'Por que o iPhone dos anúncios sempre marca {G("9:41?")}', "A resposta vem de 2007."),
    item("01", "A hora da revelação", "As apresentações da Apple começavam às 9h, e o produto era planejado para aparecer <b>cerca de 40 minutos depois</b>.", "Assim, o relógio na tela batia com o momento real da revelação."),
    item("02", "Virou tradição", "Desde então, iPhones e iPads nas imagens oficiais costumam mostrar <b>9:41</b>.", "Repare no próximo anúncio."),
    lista(f'Curiosidades da Apple {G("toda semana.")}', ["iPhone", "Mac e iPad", "Apple Watch e AirPods"], FOLLOW),
], f'Por que todo anúncio marca {G("9:41?")}')

reel("2026-11-19", "foni_reel_18h_toque_no_verso", [
    (rs("DICA", f'Seu iPhone tem um botão {G("escondido.")}', "Na traseira."), 2.6),
    (rs("", f'Ajustes &gt; Acessibilidade &gt; Toque &gt; {G("Tocar no Verso")}'), 3.0),
    (rs("", f'Escolha uma ação para {G("dois toques")} e outra para {G("três.")}'), 2.8),
    (rs("", f'Captura de tela, lanterna, câmera, {G("atalhos.")}', "Funciona do iPhone 8 em diante."), 3.0),
    (rfinal(), 3.0),
], f'Seu iPhone tem um botão {G("escondido.")}')

# ------------------------------------------------------------------ 20/11
post("2026-11-20", "foni_0743_macbook", "MAC", [
    hero(f'MacBook Air ou MacBook Pro: {G("qual é para você?")}', "Três diferenças que importam na escolha."),
    item("01", "MacBook Air", "Leve, silencioso e <b>sem ventoinha</b>.", "Ideal para estudo, trabalho de escritório e navegação."),
    item("02", "MacBook Pro", "Tem <b>ventoinha</b> e sustenta desempenho alto por mais tempo.", "Indicado para edição de vídeo, programação pesada e 3D."),
    item("03", "Portas", "O Pro tem <b>HDMI e leitor de cartão SD</b>; o Air tem só USB-C, e MagSafe nos modelos mais novos.", "Pense nos acessórios que você usa no dia a dia."),
    lista(f'Ficou na dúvida? {G("A gente ajuda.")}', ["Conte para que você vai usar", "Indicamos o modelo certo", "Sem empurrar o mais caro"], "Chame no direct."),
], f'MacBook Air ou Pro: {G("qual é para você?")}')

post("2026-11-20", "foni_12h_apple_watch", "APPLE WATCH", [
    hero(f'O Apple Watch pode {G("pedir ajuda")} por você.', "Três recursos de segurança para ativar hoje."),
    item("01", "Detecção de Queda", "Depois de uma queda forte, o relógio pergunta se você está bem.", "Sem resposta, ele liga para a emergência e avisa seus contatos."),
    item("02", "SOS de Emergência", "Segure o <b>botão lateral</b> para ligar para a emergência.", "Seus contatos de emergência recebem a sua localização."),
    item("03", "Alertas do coração", "Avisos de frequência cardíaca alta, baixa e de ritmo irregular.", "Os recursos de saúde variam conforme o modelo."),
    lista(f'Configure no app {G("Apple Watch")} do iPhone.', ["Detecção de Queda: em SOS de Emergência", "Contatos: no app Saúde, em Ficha Médica", "Coração: em Coração, no app Apple Watch"], FOLLOW),
], f'O Apple Watch pode {G("pedir ajuda")} por você.')

# ------------------------------------------------------------------ 23/11
post("2026-11-23", "foni_0743_camera", "IPHONE", [
    hero(f'Quatro recursos da câmera que {G("pouca gente usa.")}', "Salve e teste hoje."),
    item("01", "Grade e Nível", "Em <b>Ajustes &gt; Câmera</b>, ative a Grade e o Nível.", "Ajuda a alinhar o horizonte e compor melhor a foto."),
    item("02", "Travar o foco", "Toque e segure na tela até aparecer <b>Bloqueio AE/AF</b>.", "Foco e exposição ficam travados mesmo se a cena mudar."),
    item("03", "Texto ao Vivo", "Aponte para um texto e toque no ícone de texto para copiar.", "Funciona com cardápios, placas e documentos."),
    item("04", "Modo Noite", "Em ambientes escuros, ele liga sozinho a partir do iPhone 11.", "Segure o aparelho firme durante a contagem."),
    lista(f'Câmera boa {G("começa no aparelho certo.")}', ["Seminovos do iPhone 11 ao 16 Pro Max", "8 meses de garantia", "Bateria informada"], "Chame no direct."),
], f'Quatro recursos da câmera que {G("pouca gente usa.")}')

reel("2026-11-23", "foni_reel_18h_compartilhar_audio", [
    (rs("AIRPODS", f'Dois AirPods. Um iPhone. {G("A mesma música.")}'), 2.8),
    (rs("", f'Com seus AirPods conectados, abra a {G("Central de Controle.")}'), 2.8),
    (rs("", f'Toque no ícone de {G("AirPlay")} e em {G("Compartilhar Áudio.")}'), 3.0),
    (rs("", f'Aproxime o outro {G("AirPods")} do iPhone.', "Funciona com AirPods e fones Beats compatíveis."), 3.0),
    (rfinal(), 3.0),
], f'Dois AirPods, {G("a mesma música.")}')

# ------------------------------------------------------------------ 24/11
post("2026-11-24", "foni_0743_tipos_iphone", "IPHONE", [
    hero(f'Lacrado, seminovo ou recondicionado: {G("qual a diferença?")}', "Entenda antes de comprar."),
    item("01", "Lacrado", "Aparelho novo, na caixa fechada, <b>nunca ativado</b>.", "Preço mais alto e garantia do fabricante."),
    item("02", "Seminovo", "Já teve dono e foi usado. <b>Estado e bateria variam</b>.", "Na Foni BR, todo seminovo tem a bateria informada e 8 meses de garantia."),
    item("03", "Recondicionado", "Passou por <b>reparo ou troca de peças</b> para voltar a funcionar bem.", "Pergunte sempre quais peças foram trocadas."),
    final_foni(f'Na dúvida, {G("pergunte para a gente.")}', "Chame no direct."),
], f'Lacrado, seminovo ou recondicionado?')

post("2026-11-24", "foni_12h_curiosidade_primeiro_iphone", "CURIOSIDADE", [
    hero(f'O primeiro iPhone {G("não tinha App Store.")}', "Deslize para ver como começou."),
    item("2007", "O começo", "Lançado em 2007, com tela de <b>3,5 polegadas</b>.", "Vinha com 4 GB ou 8 GB de armazenamento."),
    item("2008", "Chega a App Store", "A loja de apps chegou um ano depois, junto com o <b>iPhone 3G</b>.", "Começou com cerca de 500 apps."),
    lista(f'Curiosidades da Apple {G("toda semana.")}', ["iPhone", "Mac e iPad", "Apple Watch e AirPods"], FOLLOW),
], f'O primeiro iPhone {G("não tinha App Store.")}')

# ------------------------------------------------------------------ 25/11
post("2026-11-25", "foni_0743_ipad_estudo", "IPAD", [
    hero(f'iPad para estudar: {G("quatro usos")} que fazem diferença.', "Salve para a próxima prova."),
    item("01", "Anotar à mão", "Com o <b>Apple Pencil</b>, escreva direto em PDFs e no app Notas.", "Confira qual Apple Pencil é compatível com o seu iPad."),
    item("02", "Letra vira texto", "Escreva à mão em campos de texto e o iPad <b>transforma em texto digitado</b>.", "Funciona com o Apple Pencil na maioria dos apps."),
    item("03", "Dois apps lado a lado", "Deixe o PDF de um lado e as anotações do outro com o <b>Split View</b>.", "Ideal para resumir conteúdo."),
    item("04", "Copiar da lousa", "Fotografe a lousa e copie o texto direto da imagem com o <b>Texto ao Vivo</b>.", "Sem digitar nada."),
    lista(f'Procurando um iPad? {G("Fale com a gente.")}', ["iPads com garantia", "Ajuda na escolha do modelo", "Envio para todo o Brasil"], "Chame no direct."),
], f'iPad para estudar: {G("quatro usos.")}')

reel("2026-11-25", "foni_reel_12h_escanear_documentos", [
    (rs("DICA", f'Seu iPhone é um {G("scanner.")}'), 2.4),
    (rs("", f'Abra o app {G("Notas")} e crie uma nota.'), 2.6),
    (rs("", f'Toque no ícone de anexo e escolha {G("Escanear Documentos.")}'), 3.0),
    (rs("", f'Ele recorta e {G("endireita a folha")} sozinho.', "Depois, salve em PDF ou compartilhe."), 3.0),
    (rfinal(), 3.0),
], f'Seu iPhone é um {G("scanner.")}')

# ------------------------------------------------------------------ 26/11
post("2026-11-26", "foni_0743_dispositivo_roubado", "SEGURANÇA", [
    hero(f'Ative hoje: {G("Proteção de Dispositivo Roubado.")}', "Se levarem seu iPhone com a senha, ela não basta."),
    item("01", "Biometria obrigatória", "Longe de locais conhecidos, ações sensíveis exigem <b>Face ID ou Touch ID</b>, sem a opção do código.", "Ver senhas salvas, por exemplo."),
    item("02", "Atraso de segurança", "Longe de locais conhecidos, mudar a senha da Conta Apple exige <b>uma hora de espera</b> e nova biometria.", "Tempo para você bloquear o aparelho à distância."),
    item("03", "Como ativar", "<b>Ajustes &gt; Face ID e Código &gt; Proteção de Dispositivo Roubado</b>.", "Disponível a partir do iOS 17.3."),
    lista(f'Comprou na Foni BR? {G("A gente configura com você.")}', ["Proteção de Dispositivo Roubado", "Buscar iPhone", "Contatos de emergência"], "Chame no direct."),
], f'Ative hoje: {G("Proteção de Dispositivo Roubado.")}')

post("2026-11-26", "foni_12h_curiosidade_magsafe", "CURIOSIDADE", [
    hero(f'O MagSafe {G("nasceu no MacBook.")}', "E não no iPhone."),
    item("2006", "Cabo que solta", "O conector magnético estreou no <b>MacBook Pro em 2006</b>.", "Se alguém tropeçasse no cabo, ele soltava sem derrubar o notebook."),
    item("2020", "Volta no iPhone", "O nome voltou no <b>iPhone 12</b>, agora para carregadores e acessórios magnéticos.", "Hoje o MagSafe está no iPhone e de novo nos MacBooks."),
    lista(f'Curiosidades da Apple {G("toda semana.")}', ["iPhone", "Mac e iPad", "Apple Watch e AirPods"], FOLLOW),
], f'O MagSafe {G("nasceu no MacBook.")}')

# ------------------------------------------------------------------ 30/11
post("2026-11-30", "foni_12h_inicio_rapido", "IPHONE", [
    hero(f'Trocou de iPhone? {G("Passe tudo em minutos.")}', "Use o Início Rápido."),
    item("01", "Lado a lado", "Ligue o iPhone novo <b>perto do antigo</b>.", "Os dois precisam estar com o Bluetooth ativo."),
    item("02", "Aponte a câmera", "No antigo, aponte a câmera para a <b>animação</b> que aparece no novo.", "Depois, digite o código do iPhone antigo no novo."),
    item("03", "Transfira", "Escolha transferir os dados <b>direto do iPhone antigo</b>.", "Deixe os dois carregando durante a transferência."),
    lista(f'Comprou na campanha? {G("A gente transfere com você.")}', ["Contatos, fotos e apps", "WhatsApp", "Configuração inicial"], "Chame no direct."),
], f'Trocou de iPhone? {G("Passe tudo em minutos.")}')


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        feed = await b.new_page(viewport={"width": 1080, "height": 1350})
        st = await b.new_page(viewport={"width": 1080, "height": 1920})
        n = 0
        for d, nome, htmls in POSTS:
            out = os.path.join(ROOT, "posts", d); os.makedirs(out, exist_ok=True)
            for i, h in enumerate(htmls, 1):
                await feed.set_content(h, wait_until="load")
                await feed.screenshot(path=os.path.join(out, f"{nome}_{i:02d}.jpg"), type="jpeg", quality=95); n += 1
        for d, nome, h in STORIES:
            await st.set_content(h, wait_until="load")
            await st.screenshot(path=os.path.join(ROOT, "posts", d, f"{nome}.jpg"), type="jpeg", quality=95); n += 1
        await b.close()
    for d, nome, scenes in REELS:
        await reels.render(scenes, os.path.join(ROOT, "posts", d, f"{nome}.mp4")); n += 1
    print(n, "arquivos")

if __name__ == "__main__":
    asyncio.run(main())
