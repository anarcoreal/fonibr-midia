"""Story 26/11 18h (véspera) no estilo centralizado dos anúncios. Mesmo nome de arquivo da tarefa agendada."""
import os, sys, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vitrine_1ano import pagina, render, PROD, POSTS
from gerar import preparar_foto, H

uri = preparar_foto(os.path.join(PROD, "iphone-17/iphone17_preto.png"), 730)
html = pagina('<style>.foto{position:absolute;top:560px;left:50%;transform:translateX(-50%);height:730px;'
              '-webkit-mask-image:linear-gradient(#000 88%,transparent)}</style>'
              '<div style="position:absolute;top:255px;left:0;right:0"><h1>Amanhã</h1>'
              '<div class="eb" style="margin-top:14px;font-size:56px;font-weight:700;color:#3DF06E">A vitrine de 1 ano abre</div></div>'
              f'<img class="foto" src="{uri}">'
              '<div style="position:absolute;top:1350px;left:0;right:0">'
              '<p class="sub" style="font-size:34px">R$ 300 OFF em qualquer iPhone</p>'
              '<p class="sub" style="font-size:34px;margin-top:10px">Quer os preços hoje à noite?</p>'
              '<div style="margin-top:44px"><span class="cta">Responda VIP</span></div></div>', linha_y=1285)
asyncio.run(render(html, os.path.join(POSTS, "2026-11-26", "foni_story_18h_1ano_vespera.jpg"), H))
