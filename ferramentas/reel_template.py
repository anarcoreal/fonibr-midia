import base64, asyncio, os, subprocess, shutil
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(HERE, "frames")
shutil.rmtree(FR, ignore_errors=True); os.makedirs(FR)
logo = base64.b64encode(open("/home/claude/fonibr-midia/marca/logo_transparente.png", "rb").read()).decode()
FPS, DUR = 30, 15.0

HTML = f"""<html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;background:#000;color:#fff;font-family:'Inter',sans-serif;overflow:hidden;position:relative}}
.s{{position:absolute;left:96px;right:150px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;opacity:0}}
.badge{{align-self:flex-start;border:2px solid #22C55E;color:#22C55E;font-weight:700;font-size:30px;letter-spacing:7px;padding:14px 30px;border-radius:999px;margin-bottom:60px}}
.big{{font-weight:900;font-size:190px;line-height:.92;letter-spacing:-6px}}
.h{{font-weight:800;font-size:112px;line-height:1.02;letter-spacing:-3px}}
.sub{{font-weight:300;font-size:48px;color:#cfcfcf;margin-top:50px;line-height:1.3}}
.g{{color:#22C55E}}
.line{{height:4px;margin-top:70px;background:linear-gradient(90deg,rgba(29,179,60,0),#1DB33C 15%,#1DB33C 33%,#F2E205 33%,#F2E205 66%,#1F7BEA 66%,#1F7BEA 85%,rgba(31,123,234,0));transform-origin:left;width:100%}}
.logo{{height:96px;margin-top:90px;align-self:flex-start}}
.cta{{font-weight:700;font-size:52px;margin-top:60px}}
</style></head><body>
<div class="s" id="s1"><span class="badge">FONI BR</span><div class="big">BLACK<br>FRIDAY</div><div class="line" id="l1"></div></div>
<div class="s" id="s2"><div class="h">iPhones lacrados e <span class="g">seminovos.</span></div><div class="sub">MacBooks, iPads e Apple Watch também.</div></div>
<div class="s" id="s3"><span class="badge">SEMINOVOS</span><div class="h"><span class="g">8 meses</span> de garantia.</div><div class="sub">Comprou, está coberto.</div></div>
<div class="s" id="s4"><span class="badge">FONI UPGRADE</span><div class="h">Seu iPhone <span class="g">na troca.</span></div><div class="sub">Recompra garantida em até 12 meses, com crédito no próximo aparelho.</div></div>
<div class="s" id="s5"><div class="h">Black Friday<br><span class="g">até 30/11.</span></div><div class="cta">Chame no WhatsApp.<br>Link na bio.</div><img class="logo" src="data:image/png;base64,{logo}"></div>
<script>
const S=[["s1",0,3.2],["s2",3.2,6.2],["s3",6.2,9.2],["s4",9.2,12.0],["s5",12.0,15.1]];
const ease=x=>1-Math.pow(1-Math.min(Math.max(x,0),1),3);
window.render=t=>{{for(const [id,a,b] of S){{const e=document.getElementById(id);
 const i=ease((t-a)/0.45), o=id==="s5"?1:1-ease((t-(b-0.35))/0.35);
 const v=(t>=a&&t<b)?Math.min(i,o):0;
 e.style.opacity=v; e.style.transform=`translateY(${{(1-i)*60}}px)`;}}
 document.getElementById("l1").style.transform=`scaleX(${{ease((t-0.6)/0.9)}})`;}};
</script></body></html>"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":1080,"height":1920})
        await pg.set_content(HTML)
        n = int(FPS*DUR)
        for f in range(n):
            await pg.evaluate(f"render({f/FPS})")
            await pg.screenshot(path=os.path.join(FR, f"{f:04d}.jpg"), type="jpeg", quality=92)
        await b.close()
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",os.path.join(FR,"%04d.jpg"),
        "-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest",
        "-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-movflags","+faststart",
        os.path.join(HERE,"foni_reel_blackfriday.mp4")], check=True)

asyncio.run(main())
