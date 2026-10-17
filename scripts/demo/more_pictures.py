"""More of Biblo's demo files, the ones to look at: fourteen pictures, nine screenshots and two screen recordings.

make_demo.py imports this module, so its builders are groups like any other (scripts/make-demo.sh more_images). They
show the same made-up story as more_sound.py: photos are drawings put in perspective and given a phone camera's light,
and screenshots are named the way macOS names them, which also dates them. Every company, person and number is
invented, and no logo appears here (assets/SOURCES.md)."""
from __future__ import annotations

import datetime as dt
import math
import random
from pathlib import Path

from PIL import Image

from make_demo import (BADGES, CHAT_CSS, CHEVRON, DATES, EDITOR_CSS, GREETING, OUT, TERMINAL_CSS, WORK, builder,
                       colored, esc, indent_levels, minimap, out, page, perspective, photographed, record_chat, render,
                       save_jpg, save_png, tool, window)
from more_sound import TOWN_HALL, audience, glow, theme

DATES.update({
    "Images/Trailhead 3 – launch banner.png": "2026-10-12 10:40",
    "Images/Trailhead 3 – colors.png": "2026-10-07 12:15",
    "Images/IMG_4251.jpg": "2026-10-08 16:21",
    "Images/IMG_4203.jpg": "2026-10-13 14:33",
    "Images/IMG_4210.jpg": "2026-10-13 14:36",
    "Images/Plano – planta 3.png": "2026-09-23 10:05",
    "Images/Org chart – Customer Experience.png": "2026-10-01 11:20",
    "Images/Roadmap Q4 – returns assistant.png": "2026-10-15 09:50",
    "Images/Returns by reason – September.png": "2026-10-02 16:10",
    "Images/CSAT by week – pilot.png": "2026-10-15 17:30",
    "Images/Data Summit Madrid – poster.png": "2026-10-02 09:15",
    "Images/IMG_4231.jpg": "2026-10-14 17:52",
    "Images/IMG_4244.jpg": "2026-10-14 13:10",
    "Images/Certificate – Foundry agents workshop.png": "2026-10-14 13:20",
})

HAND = '"Marker Felt"'
NOTE = "Noteworthy"
MONO = '"SF Mono",Menlo,monospace'


def snapshot(document: str, corners: list[tuple[float, float]], seed: int, path: Path) -> None:
    """A 2400×1600 page as a phone photo of it: in perspective, in a room's light, 2000×1333 and JPEG."""
    shot = perspective(render(document, (2400, 1600)), corners)
    save_jpg(photographed(shot, seed).resize((2000, 1333), Image.Resampling.LANCZOS), path, 84)


def dome(fly: str, shade: str, door: str, pole: str, key: str) -> str:
    """A small dome tent from the side, as an SVG 600×380: the fly, its door and the two crossing poles."""
    return f"""<svg viewBox="0 0 600 380"><defs><linearGradient id="fly{key}" x1="0" x2="1">
<stop offset=".35" stop-color="{fly}"/><stop offset="1" stop-color="{shade}"/></linearGradient></defs>
<ellipse cx="300" cy="350" rx="290" ry="18" fill="rgba(40,30,20,.16)"/>
<path d="M95 296 L18 352 M505 296 L582 352" stroke="#8b7d6b" stroke-width="2"/>
<path d="M60 340 Q300 -10 540 340 Z" fill="url(#fly{key})"/>
<path d="M140 340 Q300 40 460 340" fill="none" stroke="{pole}" stroke-width="4" opacity=".55"/>
<path d="M60 340 Q300 -10 540 340" fill="none" stroke="{pole}" stroke-width="5"/>
<path d="M228 340 Q300 150 372 340 Z" fill="{door}"/>
<path d="M300 246 V340" stroke="rgba(0,0,0,.28)" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M270 168 L300 150 L330 168 Z" fill="{door}" opacity=".7"/></svg>"""


# MARK: Images


def banner() -> None:
    """Trailhead 3's launch banner: a tent glowing at dusk, below the mountains."""
    rng = random.Random(3)
    stars = "".join(f'<circle cx="{rng.uniform(0, 1920):.0f}" cy="{560 * rng.random() ** 1.7:.0f}" '
                    f'r="{rng.choice([0.8, 1.1, 1.4, 1.9])}" fill="#fff" opacity="{rng.uniform(.25, .9):.2f}"/>'
                    for _ in range(170))
    document = page(f"""<svg class="sky" viewBox="0 0 1920 1080"><defs>
<radialGradient id="tent" cx="50%" cy="72%" r="70%"><stop offset="0" stop-color="#fff1c7"/>
<stop offset=".45" stop-color="#fbbf24"/><stop offset="1" stop-color="#c2410c"/></radialGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#fbbf24" stop-opacity=".5"/>
<stop offset="1" stop-color="#fbbf24" stop-opacity="0"/></radialGradient>
<radialGradient id="moon"><stop offset=".55" stop-color="#fde7c7" stop-opacity=".35"/>
<stop offset="1" stop-color="#fde7c7" stop-opacity="0"/></radialGradient></defs>
{stars}<circle cx="1590" cy="190" r="120" fill="url(#moon)"/><circle cx="1590" cy="190" r="40" fill="#fdf0d9"/>
<path d="M0 640 L180 520 L330 590 L520 452 L700 560 L860 498 L1040 600 L1240 468 L1420 560 L1600 500 L1780 572
L1920 520 V1080 H0Z" fill="#3a2048"/>
<path d="M0 770 L220 640 L420 724 L640 606 L880 734 L1100 650 L1330 742 L1560 662 L1760 724 L1920 684 V1080 H0Z"
fill="#24122f"/>
<path d="M0 884 C400 826 900 864 1300 834 S1800 852 1920 842 V1080 H0Z" fill="#12091a"/>
<ellipse cx="1450" cy="862" rx="460" ry="170" fill="url(#halo)"/>
<path d="M1262 812 L1196 888 M1638 812 L1704 888" stroke="#f5c77e" stroke-width="1.6" opacity=".55"/>
<path d="M1230 880 Q1450 520 1670 880 Z" fill="url(#tent)"/>
<path d="M1300 880 Q1450 600 1600 880" fill="none" stroke="#7c2d12" stroke-width="3" opacity=".55"/>
<path d="M1230 880 Q1450 520 1670 880" fill="none" stroke="#1c0f12" stroke-width="5"/>
<path d="M1398 880 Q1450 742 1502 880 Z" fill="#9a3412" opacity=".55"/></svg>
<div class="copy"><div class="kicker">Contoso Outdoor · New</div><h1>Trailhead 3</h1>
<p>1.9 kg. Sleeps three. Up in three minutes.</p>
<div class="chips"><span><i style="background:#2f5d46"></i>Forest green</span>
<span><i style="background:#d8c3a0"></i>Sand</span></div>
<div class="price">From 249 € · Out November 3</div></div>""", """
body{background:linear-gradient(#150c2c 0%,#3b1a4c 40%,#a63d2a 74%,#f08a24 90%)}
.sky{position:absolute;inset:0;width:1920px;height:1080px}
.copy{position:absolute;left:128px;top:250px;color:#fff7ed}
.kicker{font:600 22px/1 "Avenir Next",system-ui;letter-spacing:.24em;text-transform:uppercase;color:#fbbf24}
h1{margin:26px 0 0;font:700 168px/0.95 "Avenir Next Condensed","Avenir Next",system-ui;letter-spacing:-.02em}
p{margin:28px 0 0;font:500 40px/1.3 "Avenir Next",system-ui;color:#fde7c7}
.chips{display:flex;gap:14px;margin-top:40px}
.chips span{display:flex;align-items:center;gap:12px;padding:12px 22px 12px 14px;border-radius:999px;
background:rgba(255,247,237,.1);border:1px solid rgba(255,247,237,.28);font:600 24px "Avenir Next",system-ui}
.chips i{width:26px;height:26px;border-radius:50%;box-shadow:0 0 0 2px rgba(255,255,255,.5)}
.price{margin-top:44px;font:600 30px "Avenir Next",system-ui;color:#fbbf24}""", (1920, 1080))
    save_png(render(document, (1920, 1080)), out("Images/Trailhead 3 – launch banner.png"))


def colors() -> None:
    """The tent in its two colors, side by side, as on the product page."""
    tents = "".join(f"""<figure>{dome(fly, shade, door, pole, key)}<figcaption><i style="background:{fly}"></i>
<b>{name}</b><span>{note}</span></figcaption></figure>"""
                    for key, (name, fly, shade, door, pole, note) in enumerate([
                        ("Forest green", "#3d7358", "#24493a", "#1d3a2e", "#16261f", "Fly in recycled polyester"),
                        ("Sand", "#e2cfad", "#bfa57c", "#a68b62", "#6b5a40", "Same tent, lighter on the eye")]))
    document = page(f"""<header><span>Contoso Outdoor · Trailhead 3</span><h1>Two colors. Same 1.9 kg.</h1></header>
<main>{tents}</main><footer><span>Sleeps 3</span><span>Packed: 46 × 15 cm</span><span>Up in 3 minutes</span>
<span>249 €</span><span>From November 3</span></footer>""", """
body{background:radial-gradient(1200px 700px at 50% 60%,#fbf8f1,#efe8da)}
header{position:absolute;left:110px;top:90px}
header span{font:600 20px "Avenir Next",system-ui;letter-spacing:.2em;text-transform:uppercase;color:#8a7a5c}
h1{margin:18px 0 0;font:700 70px/1 "Avenir Next",system-ui;letter-spacing:-.02em;color:#1f2a24}
main{position:absolute;left:70px;right:70px;top:300px;display:flex;justify-content:space-around}
figure{margin:0;width:640px}figure svg{width:640px;height:405px}
figcaption{display:grid;grid-template-columns:34px 1fr;align-items:center;column-gap:16px;margin:26px 0 0 70px}
figcaption i{width:34px;height:34px;border-radius:50%;box-shadow:0 0 0 3px #fff,0 0 0 4px #d6cdb9}
figcaption b{font:700 36px "Avenir Next",system-ui;color:#1f2a24}
figcaption span{grid-column:2;font:400 23px "Avenir Next",system-ui;color:#7a6f5c}
footer{position:absolute;left:110px;right:110px;bottom:70px;display:flex;justify-content:space-between;
padding-top:26px;border-top:1px solid #d9cfbd;font:600 24px "Avenir Next",system-ui;color:#4b5e52}""", (1600, 1000))
    save_png(render(document, (1600, 1000)), out("Images/Trailhead 3 – colors.png"))


def projected(slide: tuple, index: int, count: int, css: str, foot: str, art: str) -> Path:
    """One slide of a narrated video, the way show() draws it, as a picture for a projector."""
    kicker, title, line, chips, big, _, _ = slide
    if big:
        figure, caption = big
        size = min(150, int(430 / (0.56 * len(figure))))
        side = f'<div class="big"><b style="font-size:{size}px">{esc(figure)}</b><span>{esc(caption)}</span></div>'
    else:
        side = art
    tags = "".join(f'<span class="chip">{esc(chip)}</span>' for chip in chips)
    body = (f'<div class="glow"></div>{side}<div class="text"><div class="kicker">{esc(kicker)}</div>'
            f'<h1>{esc(title)}</h1>{f"<p>{esc(line)}</p>" if line else ""}'
            f'{f"<div class=chips>{tags}</div>" if tags else ""}</div>'
            f'<div class="foot"><span>{esc(foot)}</span><span>{index + 1:02d} / {count:02d}</span></div>')
    path = WORK / f"projected-{index}.png"
    render(page(body, css), (1280, 720), 1.5).save(path)
    return path


def town_hall_photo() -> None:
    """IMG_4251: the training budget slide, photographed from the audience at the town hall."""
    css = theme("#160f2e", "#fdf4ff", "#f0abfc", "#e9d5ff", "#9d86b8", glow("240,171,252,.20", "129,140,248,.16"))
    slide = projected(TOWN_HALL[3], 3, len(TOWN_HALL), css, "Contoso · Q3 2026 town hall", audience("#f0abfc"))
    rng = random.Random(42)
    heads = []
    # Back to front, each row a little darker: heads and shoulders against the light the screen throws on the room.
    for (y, r, gap), tone in zip([(1290, 46, 128), (1420, 64, 176), (1590, 92, 240)],
                                 ["#1d1826", "#110e17", "#060408"], strict=True):
        x = rng.uniform(-60, 40)
        while x < 2460:
            cx, cy = x + rng.uniform(-16, 16), y + rng.uniform(-16, 16)
            heads.append(f'<rect x="{cx - 1.9 * r:.0f}" y="{cy + 0.95 * r:.0f}" width="{3.8 * r:.0f}" height="700" '
                         f'rx="{1.3 * r:.0f}" fill="{tone}"/><ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{0.86 * r:.0f}" '
                         f'ry="{r}" fill="{tone}"/>')
            x += gap * rng.uniform(0.8, 1.15)
    document = page(f"""<div class="room"></div><div class="screen"><img src="{slide.as_uri()}"></div>
<div class="stage"></div><svg class="speaker" viewBox="0 0 120 340"><circle cx="60" cy="40" r="30"/>
<path d="M18 340 L22 150 Q24 86 60 82 Q96 86 98 150 L102 340 Z"/><path d="M96 120 L130 168" stroke="#08060b"
stroke-width="14" stroke-linecap="round"/></svg><svg class="crowd" viewBox="0 0 2400 1600">{"".join(heads)}</svg>""",
                    """.room{position:absolute;inset:0;background:radial-gradient(1300px 760px at 50% 36%,#2a2236 0%,
#0e0b14 58%,#050407 100%)}
.screen{position:absolute;left:470px;top:150px;width:1460px;height:821px;
box-shadow:0 0 0 6px #1a1620,0 0 180px 40px rgba(190,150,255,.20)}
.screen img{width:100%;height:100%;display:block;filter:brightness(1.12) contrast(.9) saturate(.92) blur(.6px)}
.stage{position:absolute;left:0;right:0;top:1060px;bottom:0;background:linear-gradient(#3a3150,#2a2338 30%,#1a1522)}
.speaker{position:absolute;left:300px;top:760px;width:120px;height:340px;fill:#0a080d}
.crowd{position:absolute;inset:0;width:2400px;height:1600px}""", (2400, 1600), "#050407")
    snapshot(document, [(-0.01, 0.02), (1.012, -0.008), (1.016, 1.004), (0.0, 0.988)], 11, out("Images/IMG_4251.jpg"))


RECEIPT = """          LA HUERTA
   Cocina de mercado · Madrid
       Tel. 910 555 014
--------------------------------
FACTURA SIMPLIFICADA  T-0004812
Fecha: 13/10/2026   Hora: 14:31
Mesa: 12        Comensales: 4
Le atendió: Luis
--------------------------------
Ud Concepto        P.U.  Importe
 4 Menú del día   22,50    90,00
 1 Vino tinto     24,00    24,00
 2 Agua mineral    3,25     6,50
 4 Café solo       2,00     8,00
--------------------------------
Base imponible            116,82
IVA 10 %                   11,68
<b>TOTAL EUR                 128,50</b>
--------------------------------
Tarjeta ···· 4417         128,50

    ¡Gracias por su visita!
"""


def receipt() -> None:
    """IMG_4203: the receipt from lunch with Fabrikam, on the restaurant's wooden table."""
    teeth = " ".join(f"{x}% {100 if i % 2 else 98.6}%" for i, x in enumerate(range(0, 101, 2)))
    document = page(f"""<div class="table"></div><div class="saucer"><div class="cup"></div></div>
<div class="paper"><pre>{RECEIPT}</pre></div>""", """
.table{position:absolute;inset:0;
background:repeating-linear-gradient(91deg,rgba(50,24,8,.13) 0 3px,transparent 3px 23px),
repeating-linear-gradient(89deg,rgba(255,222,180,.07) 0 2px,transparent 2px 41px),
linear-gradient(170deg,#93603a,#714628 55%,#5a361d)}
.paper{position:absolute;left:830px;top:96px;width:730px;height:1420px;padding:70px 56px;
background:linear-gradient(178deg,#fbfaf5,#f1efe7);transform:rotate(-3.2deg);
box-shadow:0 34px 60px rgba(0,0,0,.38),0 2px 4px rgba(0,0,0,.2);clip-path:polygon(""" + teeth + """,0 0,100% 0)}
pre{margin:0;font:29px/1.42 "Menlo",monospace;color:#3a3a3a;opacity:.86;letter-spacing:-.3px}
pre b{font-weight:700;color:#1f1f1f}
.saucer{position:absolute;left:1830px;top:120px;width:470px;height:470px;border-radius:50%;
background:radial-gradient(circle,#ffffff 0 55%,#ecebe6 56% 70%,#f7f6f2 71%);box-shadow:0 26px 50px rgba(0,0,0,.35)}
.cup{position:absolute;inset:95px;border-radius:50%;background:radial-gradient(circle,#2b170c 0 58%,#4a2a16 66%,
#fafafa 67% 88%,#e8e6e0 89%);box-shadow:0 8px 18px rgba(0,0,0,.25)}""", (2400, 1600))
    snapshot(document, [(0.02, 0.0), (0.985, 0.03), (1.02, 1.015), (-0.015, 0.99)], 5, out("Images/IMG_4203.jpg"))


def business_card() -> None:
    """IMG_4210: Tom Becker's business card, on a desk next to a laptop and a pen."""
    document = page("""<div class="desk"></div><div class="laptop"><i></i></div><div class="pen"></div>
<div class="card"><svg class="mark" viewBox="0 0 64 64"><path d="M6 40 L32 20 L58 40" fill="none" stroke="#0f766e"
stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><path d="M6 56 L32 36 L58 56" fill="none"
stroke="#5eead4" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>
<div class="word"><b>FABRIKAM</b><span>LOGISTICS</span></div>
<div class="name"><b>Tom Becker</b><span>Key Account Manager · Europe</span></div>
<div class="contact"><span>+1 425 555 0142</span><span>tom.becker@fabrikam.com</span>
<span>fabrikam.com · Rotterdam · Zaragoza</span></div><div class="stripe"></div></div>""", """
.desk{position:absolute;inset:0;background:repeating-linear-gradient(178deg,rgba(0,0,0,.10) 0 2px,transparent 2px 19px),
radial-gradient(1500px 1000px at 55% 45%,#5b4636,#33261c 70%,#211810)}
.laptop{position:absolute;left:-200px;top:-260px;width:1100px;height:760px;border-radius:40px;background:#3b3d42;
transform:rotate(-8deg);box-shadow:0 30px 60px rgba(0,0,0,.5)}
.laptop i{position:absolute;inset:60px 70px;border-radius:12px;
background:repeating-linear-gradient(90deg,#26282c 0 78px,
#3b3d42 78px 86px)}
.pen{position:absolute;left:1700px;top:980px;width:620px;height:30px;border-radius:15px;transform:rotate(-28deg);
background:linear-gradient(#2e3138,#111317);box-shadow:0 14px 20px rgba(0,0,0,.45)}
.card{position:absolute;left:640px;top:430px;width:1100px;height:630px;border-radius:14px;transform:rotate(4deg);
background:linear-gradient(160deg,#ffffff,#f3f2ee);box-shadow:0 36px 60px rgba(0,0,0,.5),0 2px 3px rgba(0,0,0,.3);
overflow:hidden;font-family:"Avenir Next",system-ui;color:#1f2933}
.mark{position:absolute;left:80px;top:76px;width:84px;height:84px}
.word{position:absolute;left:186px;top:80px}.word b{display:block;font:700 44px/1 "Avenir Next";letter-spacing:.2em}
.word span{display:block;margin-top:8px;font:600 22px/1 "Avenir Next";letter-spacing:.62em;color:#0f766e}
.name{position:absolute;left:80px;top:270px}.name b{display:block;font:600 66px/1.1 "Avenir Next"}
.name span{display:block;margin-top:10px;font:400 31px "Avenir Next";color:#52606d}
.contact{position:absolute;left:80px;bottom:74px;display:flex;flex-direction:column;gap:8px;
font:500 27px "Avenir Next";color:#3e4c59}
.stripe{position:absolute;right:0;top:0;bottom:0;width:26px;background:linear-gradient(#0f766e,#5eead4)}""",
                    (2400, 1600))
    snapshot(document, [(0.0, 0.03), (1.0, -0.01), (1.03, 1.0), (-0.02, 1.02)], 8, out("Images/IMG_4210.jpg"))


def table(x: int, y: int, w: int, h: int, side: int, ends: bool) -> str:
    """A meeting table seen from above with `side` chairs along each long side, and one at each end if `ends`."""
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="table"/>']
    for index in range(side):
        cx = x + w * (index + 0.5) / side
        parts += [f'<circle cx="{cx:.0f}" cy="{y - 20}" r="13" class="chair"/>',
                  f'<circle cx="{cx:.0f}" cy="{y + h + 20}" r="13" class="chair"/>']
    if ends:
        parts += [f'<circle cx="{x - 20}" cy="{y + h // 2}" r="13" class="chair"/>',
                  f'<circle cx="{x + w + 20}" cy="{y + h // 2}" r="13" class="chair"/>']
    return "".join(parts)


def round_table(cx: int, cy: int) -> str:
    chairs = "".join(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="13" class="chair"/>'
                     for dx, dy in [(0, -64), (64, 0), (0, 64), (-64, 0)])
    return chairs + f'<circle cx="{cx}" cy="{cy}" r="44" class="table"/>'


def door(x: int, y: int, down: bool = False) -> str:
    """A 50 cm door in the wall at height y, swinging up into the room above (or down into the one below)."""
    swing = f"M{x} {y} L{x} {y + 50} A50 50 0 0 0 {x + 50} {y}" if down else \
        f"M{x} {y} L{x} {y - 50} A50 50 0 0 1 {x + 50} {y}"
    return f'<rect x="{x}" y="{y - 5}" width="50" height="10" class="gap"/><path d="{swing}" class="door"/>'


def room(x: int, y: int, name: str, note: str = "", size: int = 25) -> str:
    return (f'<text x="{x + (22 if size == 25 else 16)}" y="{y + 44}" class="name" style="font-size:{size}px">'
            f'{esc(name)}</text>'
            + (f'<text x="{x + 22}" y="{y + 70}" class="cap">{esc(note)}</text>' if note else ""))


def floor_plan() -> None:
    """The third floor's plan, as it hangs next to the lifts: the meeting rooms, the kitchen and locker 14."""
    fills = [(80, 150, 440, 300, "#f1edff"), (520, 150, 300, 300, "#f1edff"), (820, 150, 240, 300, "#f1edff"),
             (1060, 150, 180, 300, "#f1edff"), (1240, 150, 180, 300, "#f1f5f9"), (1420, 150, 140, 300, "#f1f5f9"),
             (1560, 150, 160, 300, "#f1f5f9"), (1060, 540, 340, 280, "#fff6dc"), (1400, 540, 320, 280, "#e3f8f2"),
             (1060, 820, 340, 280, "#e6f0ff"), (1400, 820, 320, 280, "#fdf0f7")]
    rooms = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>' for x, y, w, h, color in fills)
    desks = []
    for left in (150, 465, 780):
        for top in (660, 900):
            for column in range(3):
                for row in range(2):
                    x, y = left + column * 70, top + row * 46
                    desks.append(f'<rect x="{x}" y="{y}" width="70" height="46" class="desk"/>')
                desks += [f'<circle cx="{left + column * 70 + 35}" cy="{top - 18}" r="12" class="chair"/>',
                          f'<circle cx="{left + column * 70 + 35}" cy="{top + 110}" r="12" class="chair"/>']
    lockers = []
    for number in range(1, 17):
        row, column = divmod(number - 1, 8)
        x, y = 1424 + column * 36, 640 + row * 60
        lit = number == 14
        lockers.append(f'<rect x="{x}" y="{y}" width="34" height="56" rx="3" class="{"lit" if lit else "locker"}"/>'
                       f'<text x="{x + 17}" y="{y + 34}" class="num{" on" if lit else ""}">{number}</text>')
    stairs = "".join(f'<path d="M1440 {y} H1540" class="step"/>' for y in range(222, 440, 22))
    windows = "".join(f'<rect x="{x}" y="144" width="110" height="12" class="glass"/>' for x in range(120, 1560, 170))
    windows += "".join(f'<rect x="74" y="{y}" width="12" height="110" class="glass"/>' for y in (600, 800, 960))
    walls = """<path d="M80 450 H1720 M80 540 H260 M900 540 H1720 M520 150 V450 M820 150 V450 M1060 150 V450
M1240 150 V450 M1420 150 V450 M1560 150 V450 M1060 540 V1100 M1400 540 V1100 M1060 820 H1720" class="wall"/>"""
    openings = ('<rect x="1576" y="444" width="128" height="12" class="gap"/>'
                '<rect x="1054" y="900" width="12" height="80" class="gap"/>'
                '<rect x="1636" y="814" width="64" height="12" class="gap"/>')
    doors = "".join(door(x, 450) for x in (440, 740, 990, 1170, 1340, 1480)) + door(1300, 540, True) + \
        door(1660, 540, True)
    plan = f"""<svg class="plan" viewBox="0 0 1800 1200">
<text x="80" y="88" class="title">Contoso Madrid · Planta 3</text>
<text x="80" y="122" class="sub">Plano de planta · salas de reuniones, servicios y puestos de trabajo</text>
<g transform="translate(1690 84)"><circle r="36" class="compass"/><path d="M0 -26 L10 8 L0 2 L-10 8 Z" fill="#0f172a"/>
<text y="26" class="cap" text-anchor="middle">N</text></g>
<rect x="80" y="150" width="1640" height="950" class="outer"/>{rooms}{windows}
{table(160, 290, 280, 90, 5, True)}{table(580, 290, 180, 80, 3, True)}{table(880, 294, 120, 72, 2, True)}
{round_table(1150, 340)}
<ellipse cx="1290" cy="300" rx="16" ry="22" class="chair"/><ellipse cx="1340" cy="300" rx="16" ry="22" class="chair"/>
<ellipse cx="1390" cy="300" rx="16" ry="22" class="chair"/>
{stairs}<path d="M1490 420 V230 M1476 248 L1490 228 L1504 248" class="arrow"/>
<rect x="1580" y="230" width="58" height="58" class="lift"/><path d="M1580 230 L1638 288 M1638 230 L1580 288"
class="x"/>
<rect x="1648" y="230" width="58" height="58" class="lift"/><path d="M1648 230 L1706 288 M1706 230 L1648 288"
class="x"/>
{"".join(desks)}
<rect x="1076" y="776" width="308" height="30" class="counter"/><rect x="1300" y="779" width="56" height="24" rx="6"
class="sink"/>{round_table(1290, 694)}
{"".join(lockers)}<rect x="1598" y="694" width="46" height="68" rx="8" class="ring"/>
<text x="1424" y="792" class="cap strong">Taquilla 14 · equipos de IT</text>
<rect x="1100" y="950" width="260" height="62" rx="6" class="desk"/><rect x="1180" y="958" width="70" height="12"
class="screen"/><circle cx="1230" cy="1036" r="14" class="chair"/>
<rect x="1424" y="914" width="84" height="120" rx="8" class="booth"/><rect x="1518" y="914" width="84" height="120"
rx="8" class="booth"/><rect x="1612" y="914" width="84" height="120" rx="8" class="booth"/>
{walls}{openings}{doors}
{room(80, 150, "Sala Ártico", "12 personas · pantalla y cámara")}{room(520, 150, "Sala Sáhara", "8 personas")}
{room(820, 150, "Sala Atlas", "6 personas")}{room(1060, 150, "Amazonas", "4 personas")}{room(1240, 150, "Aseos")}
{room(1420, 150, "Escaleras", size=21)}{room(1560, 150, "Ascensores", size=21)}
{room(80, 540, "Open space · Customer Experience", "Soporte, datos y operaciones")}
{room(1060, 540, "Cocina", "Café, agua y microondas")}{room(1400, 540, "Taquillas")}
{room(1060, 820, "Puesto de IT", "Megan · de 9:00 a 18:00")}{room(1400, 820, "Cabinas de llamada")}
<circle cx="1640" cy="496" r="13" fill="#dc2626"/><circle cx="1640" cy="496" r="24" fill="none" stroke="#dc2626"
stroke-width="3" opacity=".45"/><text x="1612" y="503" class="here" text-anchor="end">Usted está aquí</text>
<g transform="translate(80 1150)"><path d="M0 0 H200 M0 -10 V10 M100 -8 V8 M200 -10 V10" class="scale"/>
<text x="0" y="36" class="cap">0</text><text x="100" y="36" class="cap" text-anchor="middle">5 m</text>
<text x="200" y="36" class="cap" text-anchor="middle">10 m</text></g>
<g transform="translate(860 1142)" class="legend"><rect width="22" height="22" rx="4" fill="#f1edff" stroke="#c4b5fd"/>
<text x="34" y="18">Salas · resérvalas en Outlook</text><rect x="330" width="22" height="22" rx="4" fill="#fff6dc"
stroke="#fcd34d"/><text x="364" y="18">Servicios</text><rect x="500" width="22" height="22" rx="4" fill="#e3f8f2"
stroke="#5eead4"/><text x="534" y="18">Taquillas e IT</text></g></svg>"""
    css = """.plan{position:absolute;inset:0;width:1800px;height:1200px}
.title{font:800 40px system-ui;fill:#0f172a;letter-spacing:-.01em}.sub{font:400 22px system-ui;fill:#64748b}
.outer{fill:#fbfaf8;stroke:#1e293b;stroke-width:14}.wall{fill:none;stroke:#334155;stroke-width:6}
.glass{fill:#bae6fd}.gap{fill:#fbfaf8}.door{fill:none;stroke:#94a3b8;stroke-width:2}
.table{fill:#e2e8f0;stroke:#94a3b8;stroke-width:2}.chair{fill:#fff;stroke:#94a3b8;stroke-width:2}
.desk{fill:#fff;stroke:#94a3b8;stroke-width:2}.counter{fill:#fde68a;stroke:#d97706;stroke-width:2}
.sink{fill:#fff;stroke:#94a3b8;stroke-width:2}.screen{fill:#334155}.booth{fill:#fff;stroke:#f0abfc;stroke-width:3}
.locker{fill:#fff;stroke:#5eead4;stroke-width:2}.lit{fill:#7c3aed;stroke:#5b21b6;stroke-width:2}
.num{font:600 15px system-ui;fill:#0f766e;text-anchor:middle}.num.on{fill:#fff;font-weight:800}
.ring{fill:none;stroke:#7c3aed;stroke-width:4;stroke-dasharray:8 6}
.step{stroke:#94a3b8;stroke-width:2}.arrow{fill:none;stroke:#475569;stroke-width:3}
.lift{fill:#fff;stroke:#64748b;stroke-width:2}.x{stroke:#cbd5e1;stroke-width:2}
.name{font:700 25px system-ui;fill:#0f172a}.cap{font:500 18px system-ui;fill:#64748b}
.cap.strong{fill:#5b21b6;font-weight:700}.here{font:700 20px system-ui;fill:#dc2626}
.compass{fill:#fff;stroke:#cbd5e1;stroke-width:2}.scale{stroke:#334155;stroke-width:3;fill:none}
.legend text{font:500 19px system-ui;fill:#475569}"""
    save_png(render(page(plan, css, (1800, 1200), "#ffffff"), (1800, 1200)), out("Images/Plano – planta 3.png"))


PEOPLE = [("LR", "Lucía Romero", "Head of Customer Experience", "Owner of the returns assistant pilot", "#7c3aed"),
          ("AC", "Ana Castillo", "Support Team Lead", "9 agents · Madrid", "#db2777"),
          ("JM", "Javier Molina", "Data Engineer", "Fabric · OneLake · reports", "#0d9488"),
          ("SN", "Sara Navarro", "Software Engineer", "Returns assistant", "#2563eb"),
          ("PS", "Pablo Serrano", "Operations Manager", "Logistics · Zaragoza", "#ea580c"),
          ("MP", "Marc Puig", "Security Engineer", "IT Security team", "#475569")]


def org_chart() -> None:
    """Customer Experience's org chart: Lucía, her four leads, and Marc from IT Security on a dotted line."""
    def card(person: tuple, x: int, y: int, w: int, extra: str = "") -> str:
        initials, name, role, note, color = person
        return (f'<div class="card{extra}" style="left:{x - w // 2}px;top:{y}px;width:{w}px">'
                f'<i style="background:{color}">{initials}</i><b>{esc(name)}</b><span>{esc(role)}</span>'
                f'<em>{esc(note)}</em></div>')
    centers = [270, 690, 1110, 1530]
    lines = ('<path d="M900 330 V440 M270 440 H1530 ' + " ".join(f"M{x} 440 V520" for x in centers)
             + '" class="line"/><path d="M1110 250 H1350" class="dotted"/>')
    body = (f'<header><span>Contoso Outdoor · People</span><h1>Customer Experience</h1>'
            f'<p>Who does what · October 2026</p></header><svg class="lines" viewBox="0 0 1800 900">{lines}</svg>'
            f'<div class="tag">dotted line · IT Security</div>'
            + card(PEOPLE[0], 900, 160, 420, " lead") + card(PEOPLE[5], 1530, 170, 360, " guest")
            + "".join(card(person, x, 520, 360) for person, x in zip(PEOPLE[1:5], centers, strict=True))
            + '<footer><span>Questions about the team: Lucía Romero</span>'
              '<span>Updated October 1, 2026</span></footer>')
    css = """body{background:linear-gradient(180deg,#faf9ff,#f3f1fb)}
header{position:absolute;left:80px;top:60px}
header span{font:600 18px system-ui;letter-spacing:.18em;text-transform:uppercase;color:#7c3aed}
h1{margin:12px 0 0;font:800 50px/1 system-ui;letter-spacing:-.02em;color:#1e1b4b}
header p{margin:10px 0 0;font:400 22px system-ui;color:#6b7280}
.lines{position:absolute;inset:0;width:1800px;height:900px}
.line{fill:none;stroke:#c4b5fd;stroke-width:3}.dotted{fill:none;stroke:#94a3b8;stroke-width:3;stroke-dasharray:4 9;
stroke-linecap:round}
.tag{position:absolute;left:1132px;top:212px;font:600 16px system-ui;color:#64748b}
.card{position:absolute;padding:26px 24px 24px 120px;min-height:150px;border-radius:20px;background:#fff;
box-shadow:0 1px 2px rgba(30,27,75,.06),0 12px 32px rgba(30,27,75,.08);border:1px solid #ece9f8}
.card i{position:absolute;left:24px;top:28px;width:74px;height:74px;border-radius:50%;display:grid;place-items:center;
font:700 26px system-ui;color:#fff;font-style:normal}
.card b{display:block;font:700 27px/1.15 system-ui;color:#111827}
.card span{display:block;margin-top:6px;font:500 19px/1.3 system-ui;color:#4b5563}
.card em{display:block;margin-top:10px;font:500 16px/1.3 system-ui;font-style:normal;color:#7c3aed}
.lead{border:2px solid #a78bfa;min-height:170px}.lead b{font-size:31px}
.guest{border:1.5px dashed #cbd5e1;background:#fbfbfd}
footer{position:absolute;left:80px;right:80px;bottom:44px;display:flex;justify-content:space-between;
padding-top:20px;border-top:1px solid #e4e1f3;font:400 18px system-ui;color:#9ca3af}"""
    save_png(render(page(body, css, (1800, 900)), (1800, 900)), out("Images/Org chart – Customer Experience.png"))


def roadmap() -> None:
    """The returns assistant's Q4 roadmap as a Gantt chart, with today (October 15) marked."""
    start, days, left, width = dt.date(2026, 10, 1), 92, 470, 1360

    def x(day: dt.date) -> float:
        return left + (day - start).days / days * width
    rows = [("v0.4 · speed, retries, pickups", (dt.date(2026, 10, 1), dt.date(2026, 10, 14)), "done", "Live Oct 14"),
            ("Alerts and more model quota", (dt.date(2026, 10, 15), dt.date(2026, 10, 23)), "doing", "Sara · Javier"),
            ("Managed identity · ADR 0007", (dt.date(2026, 10, 15), dt.date(2026, 10, 30)), "doing", "Marc"),
            ("Courier pickups in production", (dt.date(2026, 10, 19), dt.date(2026, 10, 30)), "next", "Pablo"),
            ("Sales team joins the pilot", dt.date(2026, 11, 2), "mile", "Nov 2"),
            ("Order-ownership check", (dt.date(2026, 10, 26), dt.date(2026, 11, 13)), "next",
             "Must ship before the beta"),
            ("Data Summit keynote · Madrid", dt.date(2026, 11, 12), "mile", "Nov 12"),
            ("Public beta", dt.date(2026, 12, 1), "mile", "Dec 1")]
    parts = []
    for index, (name, when, kind, note) in enumerate(rows):
        y = 250 + index * 82
        parts.append(f'<div class="name" style="top:{y}px">{esc(name)}</div>')
        if kind == "mile":
            parts.append(f'<div class="mile" style="left:{x(when) - 15:.0f}px;top:{y + 7}px"></div>'
                         f'<div class="note" style="left:{x(when) + 26:.0f}px;top:{y + 6}px">{esc(note)}</div>')
        else:
            first, last = when
            parts.append(f'<div class="bar {kind}" style="left:{x(first):.0f}px;top:{y}px;'
                         f'width:{x(last + dt.timedelta(days=1)) - x(first):.0f}px"></div>'
                         f'<div class="note" style="left:{x(last + dt.timedelta(days=1)) + 14:.0f}px;top:{y + 6}px">'
                         f'{esc(note)}</div>')
    months = "".join(f'<div class="month" style="left:{x(day):.0f}px;width:{x(end) - x(day):.0f}px">{label}</div>'
                     for day, end, label in [(dt.date(2026, 10, 1), dt.date(2026, 11, 1), "October"),
                                             (dt.date(2026, 11, 1), dt.date(2026, 12, 1), "November"),
                                             (dt.date(2026, 12, 1), dt.date(2027, 1, 1), "December")])
    weeks = "".join(f'<div class="week" style="left:{x(start + dt.timedelta(days=n)):.0f}px"></div>'
                    for n in range(days) if (start + dt.timedelta(days=n)).weekday() == 0)
    today = x(dt.date(2026, 10, 15))
    body = (f'<header><span>Returns assistant</span><h1>Roadmap · Q4 2026</h1></header>'
            f'<div class="legend"><span><i class="done"></i>Done</span><span><i class="doing"></i>In progress</span>'
            f'<span><i class="next"></i>Planned</span><span><i class="dia"></i>Milestone</span></div>'
            f'{months}{weeks}<div class="today" style="left:{today:.0f}px"><b>Today · Oct 15</b></div>{"".join(parts)}')
    css = """body{background:#fcfcfd}
header{position:absolute;left:70px;top:56px}
header span{font:600 18px system-ui;letter-spacing:.18em;text-transform:uppercase;color:#7c3aed}
h1{margin:10px 0 0;font:800 48px/1 system-ui;letter-spacing:-.02em;color:#111827}
.legend{position:absolute;right:70px;top:84px;display:flex;gap:26px;font:500 18px system-ui;color:#4b5563}
.legend span{display:flex;align-items:center;gap:10px}.legend i{width:30px;height:14px;border-radius:7px}
.legend i.dia{width:16px;height:16px;border-radius:2px;background:#111827;transform:rotate(45deg)}
.month{position:absolute;top:176px;height:40px;padding-left:12px;border-left:2px solid #e5e7eb;
font:700 19px/40px system-ui;color:#374151;background:#f5f3ff}
.week{position:absolute;top:216px;bottom:70px;width:1px;background:#eef0f4}
.today{position:absolute;top:216px;bottom:60px;width:2px;background:#ef4444}
.today b{position:absolute;bottom:-30px;left:-60px;width:120px;text-align:center;font:700 16px system-ui;color:#ef4444}
.name{position:absolute;left:70px;width:380px;height:40px;font:600 20px/40px system-ui;color:#1f2937}
.bar{position:absolute;height:40px;border-radius:10px}
.done,.legend .done{background:#10b981}.doing,.legend .doing{background:linear-gradient(90deg,#7c3aed,#a78bfa)}
.next,.legend .next{background:#fff;border:2px dashed #a78bfa}
.mile{position:absolute;width:26px;height:26px;background:#111827;transform:rotate(45deg);border-radius:3px}
.note{position:absolute;font:500 17px/28px system-ui;color:#6b7280;white-space:nowrap}"""
    save_png(render(page(body, css, (1900, 1000)), (1900, 1000)), out("Images/Roadmap Q4 – returns assistant.png"))


def returns_chart() -> None:
    """September's returns by reason, as a column chart."""
    reasons = [("Damaged", 31), ("Wrong size", 22), ("Not as described", 18), ("Changed mind", 12),
               ("Wrong item", 9), ("Late delivery", 8)]
    columns = "".join(f'<div class="col{" top" if index == 0 else ""}"><b>{share} %</b>'
                      f'<div class="bar" style="height:{share * 16}px"></div><span>{esc(reason)}</span></div>'
                      for index, (reason, share) in enumerate(reasons))
    body = (f'<header><span>Contoso Outdoor · Returns</span><h1>Why customers sent things back in September</h1>'
            f'<p>Share of 2,914 returns, online and in stores</p></header><div class="plot">{columns}</div>'
            f'<aside><b>Damaged in transit</b>Mostly tent poles bent in the parcel. Pablo is testing sturdier boxes '
            f'with the warehouse.</aside><footer>Source: returns system, September 1–30, 2026</footer>')
    css = """body{background:#fffaf5}
header{position:absolute;left:84px;top:64px}
header span{font:600 18px system-ui;letter-spacing:.18em;text-transform:uppercase;color:#c2410c}
h1{margin:14px 0 0;font:800 50px/1.08 system-ui;letter-spacing:-.02em;color:#1c1917;max-width:1100px}
header p{margin:12px 0 0;font:400 23px system-ui;color:#78716c}
.plot{position:absolute;left:84px;right:440px;bottom:130px;height:620px;display:flex;align-items:flex-end;gap:26px;
border-bottom:2px solid #d6d3d1}
.col{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;position:relative}
.col b{font:700 30px system-ui;color:#57534e;margin-bottom:12px}
.bar{width:100%;border-radius:12px 12px 0 0;background:#fed7aa}
.col.top .bar{background:linear-gradient(#ea580c,#c2410c)}.col.top b{color:#c2410c;font-size:40px}
.col span{position:absolute;bottom:-50px;font:600 19px system-ui;color:#44403c;white-space:nowrap}
aside{position:absolute;right:84px;top:360px;width:310px;padding:26px 28px;border-radius:18px;background:#fff;
border:1px solid #fed7aa;font:400 20px/1.45 system-ui;color:#57534e}
aside b{display:block;margin-bottom:8px;font:700 22px system-ui;color:#c2410c}
footer{position:absolute;left:84px;bottom:36px;font:400 17px system-ui;color:#a8a29e}"""
    save_png(render(page(body, css, (1600, 1000)), (1600, 1000)), out("Images/Returns by reason – September.png"))


def csat_chart() -> None:
    """The pilot's customer satisfaction by week, as a line chart against the 4.5 target."""
    weeks = [("Sep 14", 4.1), ("Sep 21", 4.2), ("Sep 28", 4.3), ("Oct 5", 4.5), ("Oct 12", 4.6)]
    left, right, top, bottom = 150, 1480, 260, 820

    def y(score: float) -> float:
        return bottom - (score - 3.8) / 1.0 * (bottom - top)
    xs = [left + 60 + index * (right - left - 120) / (len(weeks) - 1) for index in range(len(weeks))]
    points = " ".join(f"{px:.0f},{y(score):.0f}" for px, (_, score) in zip(xs, weeks, strict=True))
    grid = "".join(f'<path d="M{left} {y(v):.0f} H{right}" class="grid"/><text x="{left - 20}" y="{y(v) + 7:.0f}" '
                   f'class="tick" text-anchor="end">{v:.1f}</text>' for v in (3.8, 4.0, 4.2, 4.4, 4.6, 4.8))
    dots = "".join(f'<circle cx="{px:.0f}" cy="{y(score):.0f}" r="{12 if index == 4 else 9}" class="dot"/>'
                   f'<text x="{px:.0f}" y="{y(score) - 26:.0f}" class="value" text-anchor="middle">{score:.1f}</text>'
                   f'<text x="{px:.0f}" y="{bottom + 44}" class="tick" text-anchor="middle">{label}</text>'
                   for index, (px, (label, score)) in enumerate(zip(xs, weeks, strict=True)))
    chart = f"""<svg class="chart" viewBox="0 0 1600 1000"><defs><linearGradient id="area" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#8b5cf6" stop-opacity=".35"/><stop offset="1" stop-color="#8b5cf6" stop-opacity="0"/>
</linearGradient></defs>{grid}
<polygon points="{xs[0]:.0f},{bottom} {points} {xs[-1]:.0f},{bottom}" fill="url(#area)"/>
<path d="M{left} {y(4.5):.0f} H{right}" class="target"/><text x="{right}" y="{y(4.5) + 30:.0f}" class="goal"
text-anchor="end">Target 4.5</text>
<polyline points="{points}" class="line"/>{dots}</svg>"""
    body = (f'<header><span>Returns assistant pilot</span><h1>Customer satisfaction, week by week</h1>'
            f'<p>Average rating from 1 to 5 after a conversation with the agent</p></header>{chart}'
            f'<footer><span>Week starting on the date shown</span><span>Source: post-chat survey · 1,186 '
            f'conversations in the week of Oct 12</span></footer>')
    css = """body{background:#ffffff}
header{position:absolute;left:84px;top:60px}
header span{font:600 18px system-ui;letter-spacing:.18em;text-transform:uppercase;color:#7c3aed}
h1{margin:14px 0 0;font:800 50px/1.05 system-ui;letter-spacing:-.02em;color:#111827}
header p{margin:12px 0 0;font:400 23px system-ui;color:#6b7280}
.chart{position:absolute;inset:0;width:1600px;height:1000px}
.grid{stroke:#f1f1f4;stroke-width:2}.tick{font:500 20px system-ui;fill:#9ca3af}
.target{stroke:#10b981;stroke-width:3;stroke-dasharray:10 8}.goal{font:700 20px system-ui;fill:#059669}
.line{fill:none;stroke:#7c3aed;stroke-width:6;stroke-linejoin:round;stroke-linecap:round}
.dot{fill:#fff;stroke:#7c3aed;stroke-width:5}.value{font:800 26px system-ui;fill:#4c1d95}
footer{position:absolute;left:84px;right:84px;bottom:40px;display:flex;justify-content:space-between;
font:400 17px system-ui;color:#9ca3af}"""
    save_png(render(page(body, css, (1600, 1000)), (1600, 1000)), out("Images/CSAT by week – pilot.png"))


def summit_poster() -> None:
    """The Data Summit's poster: type and halftone dots, no logos."""
    body = """<div class="dots"></div><div class="beam"></div>
<div class="top"><span>Contoso Outdoor presents</span><span>12 · 11 · 2026</span></div>
<h1>DATA<br>SUMMIT</h1><h2>MADRID</h2>
<div class="when"><b>Thursday, November 12</b><span>Doors open 8:00 · First session 9:00</span></div>
<div class="keynote"><em>Opening keynote</em>How Contoso Outdoor handles returns with an AI agent</div>
<ul><li>Microsoft Fabric</li><li>Microsoft Foundry</li><li>GitHub Copilot</li><li>Live demos</li></ul>
<div class="foot"><span>900+ registered</span><span>Free · coffee and lunch included</span></div>"""
    css = """body{background:#050510;color:#f0fdff;font-family:"Avenir Next",system-ui}
.dots{position:absolute;inset:0;
background:radial-gradient(circle,rgba(34,211,238,.55) 2.2px,transparent 2.6px) 0 0/22px 22px;
-webkit-mask-image:radial-gradient(900px 900px at 100% 18%,#000 0%,transparent 70%)}
.beam{position:absolute;inset:0;background:radial-gradient(700px 520px at 0% 100%,rgba(168,85,247,.35),transparent 70%)}
.top{position:absolute;left:90px;right:90px;top:84px;display:flex;justify-content:space-between;
font:600 24px "Avenir Next";letter-spacing:.16em;text-transform:uppercase;color:#7dd3fc}
h1{position:absolute;left:84px;top:220px;margin:0;font:800 250px/.86 "Avenir Next Condensed","Avenir Next";
letter-spacing:-.02em}
h2{position:absolute;left:88px;top:700px;margin:0;font:800 180px/1 "Avenir Next Condensed","Avenir Next";
color:transparent;-webkit-text-stroke:3px #22d3ee;letter-spacing:.02em}
.when{position:absolute;left:92px;top:930px}.when b{display:block;font:700 54px/1.1 "Avenir Next";color:#22d3ee}
.when span{display:block;margin-top:14px;font:500 32px "Avenir Next";color:#bae6fd}
.keynote{position:absolute;left:92px;right:92px;top:1110px;padding-top:30px;border-top:2px solid rgba(186,230,253,.3);
font:600 44px/1.2 "Avenir Next";color:#f0fdff}
.keynote em{display:block;margin-bottom:12px;font:600 22px "Avenir Next";font-style:normal;letter-spacing:.18em;
text-transform:uppercase;color:#c084fc}
ul{position:absolute;left:92px;right:92px;top:1340px;margin:0;padding:0;list-style:none;display:flex;flex-wrap:wrap;
gap:14px}
li{padding:12px 24px;border-radius:999px;border:1.5px solid rgba(34,211,238,.5);font:600 26px "Avenir Next";
color:#cffafe}
.foot{position:absolute;left:92px;right:92px;bottom:80px;display:flex;justify-content:space-between;
font:700 30px "Avenir Next";color:#7dd3fc}"""
    save_png(render(page(body, css, (1200, 1700), "#050510"), (1200, 1700)),
             out("Images/Data Summit Madrid – poster.png"))


BOARD_CSS = """.wall{position:absolute;inset:0;background:radial-gradient(circle at 40% 30%,#d9d2c5,#a99f8f)}
.board{position:absolute;left:110px;top:90px;right:110px;bottom:150px;border-radius:10px;
background:radial-gradient(ellipse at 35% 25%,#ffffff 0%,#f6f7f5 45%,#e6e8e4 100%);
border:22px solid #c9ccd0;box-shadow:inset 0 0 0 3px #9ca3af,0 30px 60px rgba(0,0,0,.35)}
.board:before{content:"";position:absolute;inset:0;background:
radial-gradient(ellipse at 70% 60%,rgba(120,130,140,.10),transparent 40%),
radial-gradient(ellipse at 20% 80%,rgba(120,130,140,.08),transparent 35%)}
.note{position:absolute;width:300px;min-height:250px;padding:26px 24px;font:400 34px/1.22 Noteworthy;color:#1f2937;
box-shadow:0 10px 18px rgba(0,0,0,.22)}
.yellow{background:#fde68a}.pink{background:#fbcfe8}.blue{background:#bfdbfe}.green{background:#bbf7d0}
.orange{background:#fed7aa}
.tray{position:absolute;left:-22px;right:-22px;bottom:-60px;height:38px;background:linear-gradient(#d1d5db,#9ca3af);
border-radius:0 0 8px 8px}
.tray i{position:absolute;top:-14px;width:150px;height:22px;border-radius:11px}
.m1{left:300px;background:#1f2937}.m2{left:480px;background:#dc2626}.m3{left:660px;background:#2563eb}
.m4{left:840px;background:#15803d}"""

RETRO = [
    ("BIEN", "#15803d", "yellow", ["v0.4 salió a tiempo", "p95: 6,2 s<br>(antes 9,8)", "retry.py nos salvó el martes",
                                   "¡Taller de Foundry top!"]),
    ("MEJORAR", "#dc2626", "pink", ["Nos enteramos del 429 por los clientes", "Poca cuota del modelo",
                                    "Handoff tarde con clientes enfadados", "Demasiadas reuniones los miércoles"]),
    ("ACCIONES", "#1d4ed8", "green", ["Alertas: latencia &gt; 8 s y &gt; 10 errores en 5 min → Sara (viernes)",
                                      "Pedir más cuota del modelo → Javier",
                                      "Pasar antes a una persona si el cliente se enfada → Ana"]),
]


def retro_photo() -> None:
    """IMG_4231: sprint 14's retrospective, three columns of sticky notes on the whiteboard."""
    rng = random.Random(14)
    columns = []
    for column, (title, color, paper, notes) in enumerate(RETRO):
        x0 = 90 + column * 720
        columns.append(f'<h2 style="left:{x0 + 20}px;color:{color}">{title}</h2>')
        for index, text in enumerate(notes):
            row, side = divmod(index, 2)
            x = x0 + side * 330 + rng.randint(-14, 14)
            y = 300 + row * 330 + rng.randint(-12, 12)
            votes = "".join(f'<i class="vote" style="left:{24 + 30 * n}px;background:{hue}"></i>'
                            for n, hue in enumerate(["#ef4444", "#3b82f6", "#ef4444", "#22c55e", "#a855f7"]
                                                    [:5 if text.startswith("Nos") else 2 if "cuota" in text else 0]))
            columns.append(f'<div class="note {paper}" style="left:{x}px;top:{y}px;'
                           f'transform:rotate({rng.uniform(-4.5, 4.5):.1f}deg)">{text}{votes}</div>')
    lines = "".join(f'<path d="M{x} 210 C{x + 6} 600,{x - 8} 900,{x + 4} 1170" class="split"/>' for x in (800, 1520))
    document = page(f"""<div class="wall"><div class="board">
<h1>Retro · sprint 14 · 14/10</h1><svg class="lines" viewBox="0 0 2136 1316">{lines}</svg>{"".join(columns)}
<div class="tray"><i class="m1"></i><i class="m2"></i><i class="m3"></i><i class="m4"></i></div></div></div>""",
                    BOARD_CSS + """
h1{position:absolute;left:110px;top:44px;margin:0;font:400 92px "Marker Felt";color:#1f2937;transform:rotate(-1.2deg)}
h2{position:absolute;top:190px;margin:0;font:400 70px "Marker Felt";text-decoration:underline;
text-decoration-thickness:5px;text-underline-offset:12px}
.lines{position:absolute;inset:0;width:2136px;height:1316px}
.split{fill:none;stroke:#374151;stroke-width:6;stroke-linecap:round}
.note .vote{position:absolute;bottom:16px;width:22px;height:22px;border-radius:50%;
box-shadow:0 1px 2px rgba(0,0,0,.3)}""",
                    (2400, 1600))
    snapshot(document, [(0.015, 0.02), (0.99, -0.015), (1.02, 1.01), (-0.02, 0.995)], 21, out("Images/IMG_4231.jpg"))


def mcp_photo() -> None:
    """IMG_4244: the orders MCP server, drawn on the whiteboard at the end of the Foundry workshop."""
    document = page("""<div class="wall"><div class="board">
<h1>MCP · orders server</h1>
<svg class="flow" viewBox="0 0 2136 1316"><g fill="none" stroke="#1f2937" stroke-width="6" stroke-linecap="round"
stroke-linejoin="round">
<path d="M90 300 L560 292 L566 430 L96 438 Z"/><path d="M90 560 L560 556 L564 680 L94 686 Z"/>
<path d="M90 810 L560 806 L566 930 L96 936 Z" stroke-dasharray="18 14"/>
<path d="M800 330 L1330 318 L1342 900 L806 912 Z" stroke="#1d4ed8" stroke-width="8"/>
<path d="M1580 330 L2030 324 L2036 460 L1586 468 Z"/><path d="M1580 700 L2030 694 L2034 830 L1584 836 Z"/>
<path d="M570 366 C650 380 720 420 792 470 M760 446 L796 474 L752 490"/>
<path d="M572 620 C650 618 720 616 792 614 M758 594 L796 614 L758 636"/>
<path d="M574 870 C650 850 720 810 792 770 M748 764 L796 766 L770 806"/>
<path d="M1350 420 C1420 410 1500 400 1572 396 M1536 374 L1574 396 L1538 420"/>
<path d="M1350 760 C1420 762 1500 764 1572 766 M1536 744 L1574 766 L1536 788"/></g>
<g font-family="Marker Felt" fill="#1f2937"><text x="120" y="358" font-size="46">Returns assistant</text>
<text x="120" y="412" font-size="36" fill="#6b7280">Foundry agent</text>
<text x="120" y="636" font-size="46">Web chat</text>
<text x="120" y="886" font-size="46">Sales app</text><text x="370" y="886" font-size="36" fill="#6b7280">(Nov)</text>
<text x="840" y="410" font-size="60" fill="#1d4ed8">ORDERS MCP</text>
<text x="840" y="476" font-size="60" fill="#1d4ed8">SERVER</text>
<text x="850" y="600" font-size="44">• lookup_order</text><text x="850" y="690" font-size="44">• create_return</text>
<text x="850" y="780" font-size="44">• book_pickup</text>
<text x="1610" y="408" font-size="46">Order system</text><text x="1610" y="446" font-size="34" fill="#6b7280">ERP</text>
<text x="1610" y="778" font-size="46">Courier API</text>
<text x="1610" y="816" font-size="34" fill="#6b7280">pickups</text>
<text x="800" y="1010" font-size="44" fill="#15803d">slots: 2 h · Mon–Sat · 8–20</text>
<text x="800" y="1080" font-size="44" fill="#1d4ed8">auth: managed identity → no keys!</text>
<text x="1500" y="1010" font-size="44" fill="#dc2626">check the order is the</text>
<text x="1500" y="1062" font-size="44" fill="#dc2626">customer's !!</text></g>
<path d="M1446 946 C1500 896 2084 906 2100 1010 C2114 1122 1484 1122 1446 1048 C1432 1018 1434 978 1446 946 Z"
fill="none" stroke="#dc2626" stroke-width="5" stroke-linecap="round"/></svg>
<div class="note yellow" style="left:150px;top:1010px;transform:rotate(-3deg)">Who owns the server? → Sara</div>
<div class="note orange" style="left:480px;top:1030px;transform:rotate(2.5deg)">Rate limits per app?</div>
<div class="tray"><i class="m1"></i><i class="m2"></i><i class="m3"></i><i class="m4"></i></div></div></div>""",
                    BOARD_CSS + """
h1{position:absolute;left:96px;top:56px;margin:0;font:400 104px "Marker Felt";color:#1d4ed8;transform:rotate(-1.4deg)}
.flow{position:absolute;inset:0;width:2136px;height:1316px;transform:rotate(.5deg)}
.note{width:280px;min-height:210px}""", (2400, 1600))
    snapshot(document, [(-0.015, 0.025), (1.015, 0.0), (1.02, 1.02), (0.0, 0.985)], 33, out("Images/IMG_4244.jpg"))


def certificate() -> None:
    """Ana's certificate for the Foundry agents workshop: Contoso's own training, as the small print says."""
    seal = "".join(f'<path d="M100 100 L{100 + 92 * math.cos(i * math.tau / 48):.1f} '
                   f'{100 + 92 * math.sin(i * math.tau / 48):.1f}" class="ray"/>' for i in range(48))
    body = f"""<div class="paper"><div class="frame"><div class="inner">
<div class="brand"><svg viewBox="0 0 64 48" class="mark"><path d="M4 44 L32 6 L60 44 Z" fill="none" stroke="#7c3aed"
stroke-width="5" stroke-linejoin="round"/><path d="M24 44 L32 28 L40 44" fill="#7c3aed"/></svg>CONTOSO ACADEMY</div>
<h1>Certificate of completion</h1><p class="lead">This certifies that</p><div class="name">Ana Castillo</div>
<p>has completed the hands-on workshop</p><h2>Building agents with Microsoft Foundry</h2>
<p class="meta">3 hours · Madrid, 14 October 2026</p>
<div class="signs"><div><span class="sig">Sara Navarro</span><b>Sara Navarro</b><em>Instructor</em></div>
<div><span class="sig date">14 October 2026</span><b>Date</b><em>Sala Ártico, Contoso Madrid</em></div></div>
<svg class="seal" viewBox="0 0 200 200"><defs><radialGradient id="gold"><stop offset="0" stop-color="#f4dd9a"/>
<stop offset=".7" stop-color="#d4a83a"/><stop offset="1" stop-color="#a67c1b"/></radialGradient></defs>
<g>{seal}</g><circle cx="100" cy="100" r="78" fill="url(#gold)"/><circle cx="100" cy="100" r="64" fill="none"
stroke="#fff6d8" stroke-width="2" stroke-dasharray="3 4"/><text x="100" y="94" class="s1">CONTOSO</text>
<text x="100" y="118" class="s2">ACADEMY · 2026</text></svg>
<div class="fine">Internal training. Not a Microsoft certification.</div></div></div></div>"""
    css = """body{background:#e9e5dc}
.paper{position:absolute;inset:0;background:radial-gradient(1400px 900px at 50% 40%,#fffdf7,#f6f1e4)}
.frame{position:absolute;inset:46px;border:3px solid #c9b37a}
.inner{position:absolute;inset:14px;border:1px solid #d9c899;text-align:center;color:#2a2340;
font-family:"Iowan Old Style",Charter,Georgia,serif}
.brand{margin-top:92px;display:flex;justify-content:center;align-items:center;gap:18px;
font:600 26px "Avenir Next",system-ui;letter-spacing:.42em;color:#5b21b6}
.mark{width:58px;height:44px}
h1{margin:60px 0 0;font:400 92px/1 "Iowan Old Style",Georgia,serif;letter-spacing:.01em;color:#1e1b4b}
p{margin:26px 0 0;font:italic 400 32px "Iowan Old Style",Georgia,serif;color:#5b5670}
.name{margin-top:24px;font:400 128px/1.1 "Snell Roundhand","Apple Chancery",cursive;color:#4c1d95}
h2{margin:18px 0 0;font:600 52px "Iowan Old Style",Georgia,serif;color:#1e1b4b}
.meta{font-style:normal;font-family:"Avenir Next",system-ui;font-size:26px;letter-spacing:.06em;color:#6b6585}
.signs{position:absolute;left:220px;right:220px;bottom:150px;display:flex;justify-content:space-between}
.signs div{width:460px;border-top:2px solid #3f3a56;padding-top:14px;position:relative}
.sig{position:absolute;left:0;right:0;bottom:84px;font:400 64px "Snell Roundhand","Apple Chancery",cursive;
color:#1e3a8a}
.sig.date{font:400 34px "Iowan Old Style",Georgia,serif;bottom:92px;color:#2a2340}
.signs b{display:block;font:600 26px "Avenir Next",system-ui;color:#2a2340}
.signs em{display:block;margin-top:4px;font:400 21px "Avenir Next",system-ui;font-style:normal;color:#77728c}
.seal{position:absolute;left:50%;bottom:118px;width:230px;height:230px;margin-left:-115px}
.ray{stroke:#c9a13b;stroke-width:5}
.s1{font:700 22px "Avenir Next",system-ui;letter-spacing:.2em;fill:#5a3e05;text-anchor:middle}
.s2{font:600 13px "Avenir Next",system-ui;letter-spacing:.16em;fill:#5a3e05;text-anchor:middle}
.fine{position:absolute;left:0;right:0;bottom:44px;font:400 19px "Avenir Next",system-ui;color:#8a849c}"""
    save_png(render(page(body, css, (2000, 1414)), (2000, 1414)),
             out("Images/Certificate – Foundry agents workshop.png"))


@builder
def more_images():
    """Images/: fourteen more pictures: phone photos, charts, a floor plan, an org chart, a poster and a certificate."""
    for draw in (banner, colors, town_hall_photo, receipt, business_card, floor_plan, org_chart, roadmap,
                 returns_chart, csat_chart, summit_poster, retro_photo, mcp_photo, certificate):
        draw()


# MARK: Screenshots

DATES.update({
    "Code/contoso-support-agent/tests/test_retry.py": "2026-10-13 11:16",
    "Code/contoso-support-agent/src/agent.py": "2026-10-13 11:18",
    "Code/contoso-support-agent/src/retry.py": "2026-10-13 11:19",
})

BROWSER_CSS = CHAT_CSS.split("\n.app{")[0]  # the browser's toolbar: back, forward and the address
LOCK = ('<svg width="10" height="12" viewBox="0 0 10 12" style="margin-right:7px"><rect x=".5" y="5" width="9" '
        'height="6.5" rx="1.6" fill="#6e6e73"/><path d="M2.6 5V3.7a2.4 2.4 0 0 1 4.8 0V5" fill="none" '
        'stroke="#6e6e73" stroke-width="1.3"/></svg>')
COLUMNS, ROWS = 124, 37  # Sara's terminal, as its title says
REPO = "/Users/sara/src/contoso-support-agent"
SITE = f"{REPO}/.venv/lib/python3.12/site-packages/openai"


class Markup(str):
    """A terminal line already in HTML, with its colors: shown as it is, neither escaped nor wrapped."""


def prompt(branch: str, command: str = "", cursor: bool = False) -> Markup:
    """Sara's zsh prompt in the support agent's folder, on `branch`, and what she typed after it."""
    return Markup(f'<span class="p">~/src/contoso-support-agent</span> <span class="m">{branch}</span> '
                  f'<span class="g">❯</span> {esc(command)}' + ('<span class="cursor"> </span>' if cursor else ""))


def terminal(lines: list[str]) -> str:
    """What a 124×37 terminal shows of `lines`: each wrapped at 124 columns, and the last 37 rows of them all."""
    rows: list[str] = []
    for line in lines:
        if isinstance(line, Markup):
            rows.append(line)
        else:
            rows += [esc(line[start:start + COLUMNS]) for start in range(0, max(len(line), 1), COLUMNS)]
    return "\n".join(rows[-ROWS:])


def terminal_window(lines: list[str]) -> str:
    return window(f"<pre>{terminal(lines)}</pre>", f"contoso-support-agent — -zsh — {COLUMNS}×{ROWS}", (1080, 770),
                  True, TERMINAL_CSS + "\n.r{color:#ff6b68}")


def browser(content: str, size: tuple[int, int], address: str, css: str) -> str:
    """A web page in the browser, at `address`, as in the support chat's screenshots."""
    toolbar = f'<div class="nav"><b>‹</b><b>›</b></div><div class="url">{LOCK}{esc(address)}</div>'
    return window(content, "", size, False, f"{BROWSER_CSS}\n{css}", toolbar)


def screenshot(document: str, size: tuple[int, int], when: str) -> None:
    """A window of `size` as ⇧⌘4 then Space takes it on a Retina screen, named as macOS names it on `when`, which is
    like "10-13 11.02.47"."""
    day, clock = when.split()
    save_png(render(document, (size[0] + 112, size[1] + 112), 2, True),
             out(f"Screenshots/Screenshot 2026-{day} at {clock}.png"))


def frame(path: str, line: int, function: str, code: str = "", failing: str = "") -> list[str]:
    """One frame of a Python 3.12 traceback: the place, its line of code, and carets under the part that failed when
    that isn't the whole line."""
    rows = [f'  File "{path}", line {line}, in {function}'] + ([f"    {code}"] if code else [])
    if failing:
        rows.append(" " * (4 + code.index(failing)) + "^" * len(failing))
    return rows


RATE_LIMITED = ("openai.RateLimitError: Error code: 429 - {'error': {'code': '429', 'message': 'Requests to the "
                "Responses_Create Operation under Azure OpenAI API version v1 have exceeded token rate limit of your "
                "current AIServices S0 pricing tier. Please retry after 12 seconds. Please contact Azure support "
                "service if you would like to further increase the default rate limit.'}}")


def outage() -> None:
    """Sara reproducing the outage at 11:02 on October 13, before the fix: the terminal chat dies on the model's 429.
    The line numbers are agent.py's before retry.py."""
    agent = f"{REPO}/src/agent.py"
    create = "openai.responses.create(conversation=conversation_id, input=text, extra_body=extra)"
    request = "self.request(cast_to, opts, stream=stream, stream_cls=stream_cls)"
    lines = [prompt("main", "git pull"), "Already up to date.", prompt("main", "uv run python -m src.agent chat"), "",
             "you › Where's my order 50342?", "Traceback (most recent call last):",
             *frame("<frozen runpy>", 198, "_run_module_as_main"), *frame("<frozen runpy>", 88, "_run_code"),
             *frame(agent, 188, "<module>", "main()"), *frame(agent, 184, "main", "chat()"),
             *frame(agent, 159, "chat", "for event in turn(openai, conversation.id, text):",
                    "turn(openai, conversation.id, text)"),
             *frame(agent, 101, "turn", f"response = {create}", create),
             *frame(f"{SITE}/_utils/_utils.py", 286, "wrapper", "return func(*args, **kwargs)",
                    "func(*args, **kwargs)"),
             *frame(f"{SITE}/resources/responses/responses.py", 840, "create", "return self._post(", "self._post("),
             *frame(f"{SITE}/_base_client.py", 1259, "post", f"return cast(ResponseT, {request})", request),
             *frame(f"{SITE}/_base_client.py", 1047, "request",
                    "raise self._make_status_error_from_response(err.response) from None"),
             RATE_LIMITED, prompt("main", cursor=True)]
    screenshot(terminal_window(lines), (1080, 770), "10-13 11.02.47")


REPORT = ("https://ai.azure.com/resource/build/evaluation/evalrun_68ecb3f2a01c8190b8d24e6f57a9c3d1?wsid=/subscriptions/"
          "00000000-0000-0000-0000-000000000000/resourceGroups/rg-contoso-support-dev/providers/"
          "Microsoft.CognitiveServices/accounts/ai-contoso-k3x7q/projects/proj-support")
SCORES = [("intent_resolution", 4.5, 4.0), ("tool_call_accuracy", 4.8, 4.0), ("task_adherence", 0.94, 0.90),
          ("groundedness", 4.1, 4.0), ("relevance", 4.4, 4.0)]
CHANGED = [("src/agent.py", 4, 2), ("src/retry.py", 89, 0), ("tests/test_retry.py", 76, 0)]
COMMIT = "Retry the model's 429s with backoff"


def evaluation() -> None:
    """At 16:20 on October 13: the retries committed, merged into main, and version 9 scored on the golden set, as
    src/evaluate.py prints it."""
    stat = [Markup(f' {esc(name):<19} | {plus + minus:>2} <span class="g">{"+" * plus}</span>'
                   f'<span class="r">{"-" * minus}</span>') for name, plus, minus in CHANGED]
    summary = [" 3 files changed, 169 insertions(+), 2 deletions(-)", " create mode 100644 src/retry.py",
               " create mode 100644 tests/test_retry.py"]
    scores = []
    for name, value, target in SCORES:
        shown, wanted = ((f"{value:.0%}", f"≥ {target:.0%}") if name == "task_adherence"
                         else (f"{value:.1f}", f"≥ {target:.1f}"))
        scores.append(f"  {name:<20} {shown:>5}   {wanted:<6} ok")
    lines = [prompt("hotfix/429-retries", f'git add -A && git commit -m "{COMMIT}"'),
             f"[hotfix/429-retries 9b8e4d0] {COMMIT}", *summary,
             prompt("hotfix/429-retries", "git switch main"), "Switched to branch 'main'",
             "Your branch is up to date with 'origin/main'.", prompt("main", "git merge --ff-only hotfix/429-retries"),
             "Updating 3f2c1a7..9b8e4d0", "Fast-forward", *stat, *summary,
             prompt("main", "uv run python -m src.evaluate --version 9"),
             "returns-assistant v9 answers evals/golden.jsonl…", "  120/120 talla-equivocada", "Grading 120 answers…",
             f"Report: {REPORT}", *scores, "", "Every target met. Next: python -m src.agent promote 9",
             prompt("main", cursor=True)]
    screenshot(terminal_window(lines), (1080, 770), "10-13 16.20.11")


# The editor's activity bar (explorer, search, source control, run, extensions) and status bar icons, as in
# make_demo's editor().
ACTS = ['<path d="M13.5 3H6.5v18h11V7zM13.5 3v4h4"/>',
        '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5.5 5.5"/>',
        '<circle cx="6" cy="5" r="2.2"/><circle cx="6" cy="19" r="2.2"/><circle cx="18" cy="8" r="2.2"/>'
        '<path d="M6 7.2v9.6M18 10.2c0 4-5 4-11 7"/>', '<path d="M7 4.5l12 7.5-12 7.5z"/>',
        '<rect x="3.5" y="3.5" width="7" height="7"/><rect x="13.5" y="3.5" width="7" height="7"/>'
        '<rect x="3.5" y="13.5" width="7" height="7"/><rect x="13.5" y="13.5" width="7" height="7"/>']
BRANCH = ('<svg viewBox="0 0 16 16"><circle cx="4.5" cy="3.5" r="1.6"/><circle cx="4.5" cy="12.5" r="1.6"/>'
          '<circle cx="11.5" cy="5" r="1.6"/><path d="M4.5 5.1v5.8M11.5 6.6c0 2.6-3.5 2.6-7 4.6"/></svg>')
ERRORS = '<svg viewBox="0 0 16 16"><circle cx="8" cy="8" r="6"/><path d="M5.8 5.8l4.4 4.4M10.2 5.8l-4.4 4.4"/></svg>'
WARNINGS = '<svg viewBox="0 0 16 16"><path d="M8 2.2l6.3 11.3H1.7zM8 6.5v3.4M8 11.6v.3"/></svg>'
GIT = {"M": "#e2c08d", "U": "#73c991"}  # modified, untracked
EDITOR_MORE = """.acts div{position:relative}.acts em{position:absolute;right:7px;bottom:8px;min-width:16px;height:16px;
padding:0 4px;border-radius:8px;background:#4d78cc;color:#fff;font:600 9.5px/16px system-ui;text-align:center}
.row em,.tab em{font:600 11px system-ui;font-style:normal}.row em{margin-left:auto;padding-right:16px}
.tab em{margin-left:8px}"""
# The explorer on October 13, after the tests ran: (depth, open folder?, name, file type badge, ignored?, git status).
TREE_OCT_13 = [
    (0, False, ".azure", "", True, ""), (0, False, ".pytest_cache", "", True, ""), (0, False, ".venv", "", True, ""),
    (0, False, "evals", "", False, ""), (0, False, "infra", "", False, ""), (0, False, "prompts", "", False, ""),
    (0, True, "src", "", False, "M"), (1, False, "__pycache__", "", True, ""),
    (1, None, "__init__.py", "py", False, ""), (1, None, "agent.py", "py", False, "M"),
    (1, None, "app.py", "py", False, ""), (1, None, "evaluate.py", "py", False, ""),
    (1, None, "pickup_slots.py", "py", False, ""), (1, None, "retry.py", "py", False, "U"),
    (1, None, "tools.py", "py", False, ""), (0, True, "tests", "", False, "U"),
    (1, False, "__pycache__", "", True, ""), (1, None, "test_retry.py", "py", False, "U"),
    (1, None, "test_tools.py", "py", False, ""), (0, False, "web", "", False, ""),
    (0, None, ".gitignore", "git", False, ""), (0, None, "azure.yaml", "yml", False, ""),
    (0, None, "Dockerfile", "dk", False, ""), (0, None, "pyproject.toml", "tml", False, ""),
    (0, None, "README.md", "md", False, "")]


def code_editor(path: str, first: int, current: int, column: int, function: str, tabs: list[str], tree: list[tuple],
                branch: str, shell: list[str]) -> str:
    """The support agent's code in the editor, as in make_demo's screenshot of October 8: `path` from line `first`,
    the cursor on `current`, git's marks in the explorer and the tabs, and `shell` in the terminal below."""
    source = (OUT / "Code/contoso-support-agent" / path).read_text(encoding="utf-8")
    lines = source.splitlines()
    rows = colored(source)
    levels = indent_levels(lines)
    name = path.rsplit("/", 1)[-1]
    marks = {item[2]: item[5] for item in tree if item[3]}
    code = []
    for number in range(first, min(first + 32, len(lines) + 1)):
        text = "".join(f'<span style="color:#{color}{";font-style:italic" if italic else ""}">{esc(piece)}</span>'
                       for piece, color, italic in rows[number - 1])
        guides = "".join(f'<i style="left:{4 * k}ch"></i>' for k in range(levels[number - 1]))
        code.append(f'<div class="ln{" on" if number == current else ""}"><b>{number}</b>'
                    f'<span class="t">{guides}{text}</span></div>')
    changed = sum(1 for mark in marks.values() if mark)
    acts = "".join(f'<div{" class=on" if index == 0 else ""}><svg viewBox="0 0 24 24">{icon}</svg>'
                   f'{f"<em>{changed}</em>" if index == 2 and changed else ""}</div>'
                   for index, icon in enumerate(ACTS))
    explorer = []
    for depth, open_, label, kind, ignored, mark in tree:
        color = f";color:{GIT[mark]}" if mark else ""
        badge = f'<s style="color:{BADGES[kind]}">{kind}</s>' if kind else ""
        flag = f'<em style="color:{GIT[mark]}">{mark if kind else "•"}</em>' if mark else ""
        explorer.append(f'<div class="row{" on" if label == name else ""}{" dim" if ignored else ""}" '
                        f'style="padding-left:{10 + 12 * depth}px{color}">{CHEVRON[open_]}{badge}{esc(label)}{flag}'
                        '</div>')
    tab_html = []
    for index, tab in enumerate(tabs):
        mark = marks.get(tab, "")
        kind = "py" if tab.endswith(".py") else "md"
        tab_html.append(f'<div class="tab{" on" if index == 0 else ""}"'
                        f'{f" style=color:{GIT[mark]}" if mark else ""}><s style="color:{BADGES[kind]}">{kind}</s>'
                        f'{esc(tab)}{f"<em>{mark}</em>" if mark else ""}'
                        f'{"<span class=x>×</span>" if index == 0 else ""}</div>')
    crumbs = "<span>›</span>".join(path.split("/")) + f'<span>›</span><span class="fn">ƒ</span>{function}'
    terminal_html = "\n".join(line if isinstance(line, Markup) else esc(line) for line in shell)
    body = f"""<div class="acts">{acts}</div>
<div class="side"><h4>EXPLORER</h4><div class="row root" style="padding-left:2px">{CHEVRON[True]}CONTOSO-SUPPORT-AGENT
</div>{"".join(explorer)}</div>
<div class="main"><div class="tabs">{"".join(tab_html)}</div><div class="crumbs">{crumbs}</div>
<div class="editor">{"".join(code)}{minimap(rows, first, len(code))}</div>
<div class="term"><h5><span>PROBLEMS</span><span>OUTPUT</span><span>DEBUG CONSOLE</span><b>TERMINAL</b>
<span>PORTS</span></h5><pre>{terminal_html}</pre></div></div>
<div class="status"><span>{BRANCH}{branch}{"*" if changed else ""}</span><span>{ERRORS}0&nbsp;&nbsp;{WARNINGS}0</span>
<div class="end"><span>Ln {current}, Col {column}</span><span>Spaces: 4</span><span>UTF-8</span><span>LF</span>
<span>Python</span><span>3.12.7 ('.venv': venv)</span></div></div>"""
    return window(body, f"{name} — contoso-support-agent", (1440, 900), True, EDITOR_CSS + EDITOR_MORE)


def retries() -> None:
    """The fix at 11:20 on October 13: retry.py open where it waits, the tests passing, and version 9 published."""
    source = (OUT / "Code/contoso-support-agent/src/retry.py").read_text(encoding="utf-8").splitlines()
    current = next(number for number, line in enumerate(source, start=1) if line.strip() == "sleep(pause)")
    column = source[current - 1].index("sleep") + 1
    branch = "hotfix/429-retries"
    shell = [prompt("main", f"git switch -c {branch}"), f"Switched to a new branch '{branch}'",
             prompt(branch, "uv run pytest -q"),
             Markup(f'<span class="g">{"." * 13}{" " * (154 - 13 - 6)}[100%]</span>'),
             Markup('<span class="g"><b>13 passed</b> in 0.41s</span>'),
             prompt(branch, "uv run python -m src.agent publish"),
             "Published returns-assistant version 9. Next: python -m src.evaluate --version 9",
             prompt(branch, cursor=True)]
    shot = code_editor("src/retry.py", current - 29, current, column, "with_retry",
                       ["retry.py", "test_retry.py", "agent.py"], TREE_OCT_13, branch, shell)
    screenshot(shot, (1440, 900), "10-13 11.20.31")


# MARK: Web pages

PLANE = ('<svg viewBox="0 0 24 24"><path d="M23 12l-1.5-1H15l-4.5-7h-2l2.5 7H6L4.2 8.5H2.8l.8 3v1l-.8 3h1.4L6 13h5'
         'l-2.5 7h2l4.5-7h6.5z"/></svg>')
TICK = '<svg viewBox="0 0 24 24"><path d="M6 12.5l4 4 8-9"/></svg>'
AIRLINE_CSS = """.by{position:absolute;inset:0;background:#f1f4f9;font:14px/1.45 system-ui;color:#13213f}
.by svg{display:block}
.by .mast{height:64px;background:#0b2d6b;display:flex;align-items:center;gap:46px;padding:0 40px;color:#fff}
.by .logo{display:flex;align-items:center;gap:11px;line-height:1}
.by .logo b{display:block;font:800 15px system-ui;letter-spacing:.17em}
.by .logo small{display:block;margin-top:4px;font:600 9px system-ui;letter-spacing:.5em;color:#8fc1ff}
.by .links{display:flex;gap:30px;align-self:stretch;font:600 14px system-ui;color:#c4d3ef}
.by .links span{display:flex;align-items:center}.by .links .on{color:#fff;box-shadow:inset 0 -3px #5fb3ff}
.by .me{margin-left:auto;display:flex;align-items:center;gap:10px;font:600 13.5px system-ui}
.by .me i,.by .pax i{border-radius:50%;display:grid;place-items:center;font:800 12px system-ui;font-style:normal}
.by .me i{width:32px;height:32px;background:#5fb3ff;color:#0b2d6b}
.by .page{width:1120px;margin:0 auto;padding:18px 0}
.by .trail{margin-bottom:12px;font:500 13px system-ui;color:#5b6b8c}
.by .ok,.by .leg,.by .card,.by .extra{background:#fff;border-radius:14px;box-shadow:0 1px 3px rgba(11,45,107,.08)}
.by .ok{display:flex;align-items:center;gap:18px;padding:18px 26px}
.by .tick{width:44px;height:44px;flex:none;border-radius:50%;background:#16a34a;display:grid;place-items:center}
.by .tick svg{width:26px;height:26px;fill:none;stroke:#fff;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}
.by h1{margin:0;font:750 23px system-ui;letter-spacing:-.01em}.by .ok p{margin:2px 0 0;color:#4a5a7a}
.by .ref{margin-left:auto;text-align:right}
.by .ref small,.by h3{display:block;font:700 11px system-ui;letter-spacing:.08em;text-transform:uppercase;color:#6b7a99}
.by .ref b{font:700 24px "SF Mono",Menlo,monospace;letter-spacing:.08em;color:#0b2d6b}
.by .grid{display:grid;grid-template-columns:1fr 340px;gap:20px;margin-top:16px}
.by .legs,.by aside{display:flex;flex-direction:column;gap:14px}
.by .leg{padding:16px 24px 18px}.by .card{padding:18px 22px}
.by .head{display:flex;align-items:baseline;gap:12px;font:600 14px system-ui}
.by .dir{font:700 11px system-ui;letter-spacing:.1em;text-transform:uppercase;color:#1d64d8}
.by .fl{margin-left:auto;font:600 13px "SF Mono",Menlo,monospace;color:#5b6b8c}
.by .route{display:grid;grid-template-columns:190px 1fr 190px;align-items:center;margin:12px 0 14px}
.by .end b{display:block;font:700 32px/1.15 system-ui;letter-spacing:-.02em}
.by .end span{margin-right:6px;font:700 15px system-ui;color:#0b2d6b}.by .end small{font-size:13px;color:#5b6b8c}
.by .arrive{text-align:right}.by .path{text-align:center;font-size:12.5px;color:#5b6b8c}
.by .line{position:relative;height:22px;margin:4px 24px}
.by .line:before{content:"";position:absolute;left:0;right:0;top:50%;border-top:2px dotted #b8c4dc}
.by .line svg{position:relative;width:22px;height:22px;margin:0 auto;padding:0 4px;background:#fff;fill:#1d64d8;
box-sizing:content-box}
.by .tags{display:flex;flex-wrap:wrap;gap:8px}
.by .tags span{padding:4px 10px;border-radius:7px;background:#eef3fb;font:600 12.5px system-ui;color:#2b3f66}
.by h3{margin:0 0 12px}
.by .pax{display:flex;align-items:center;gap:12px}.by .pax i{width:40px;height:40px;background:#e3ecfb;color:#0b2d6b}
.by .pax b{display:block;font-size:15px}.by .pax small,.by .paid,.by .hint,.by .extra small{font-size:12.5px;
color:#5b6b8c}
.by dl{display:grid;grid-template-columns:1fr auto;gap:8px;margin:0;color:#3a4a6a}
.by dd{margin:0;font-variant-numeric:tabular-nums}
.by .total{display:flex;justify-content:space-between;align-items:baseline;margin-top:12px;padding-top:12px;
border-top:1px solid #e3e8f2;font-weight:700}.by .total b{font:800 22px system-ui;font-variant-numeric:tabular-nums}
.by .paid{margin:8px 0 0}
.by .btn{height:44px;border-radius:10px;display:grid;place-items:center;border:1.5px solid #0b2d6b;background:#fff;
font:700 14px system-ui;color:#0b2d6b}.by .btn.go{background:#0b2d6b;color:#fff}
.by .hint{margin:0 4px}
.by .extras{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.by .extra{padding:14px 18px}.by .extra b{display:block}"""
# (direction, day, flight, (time, airport, city and terminal) leaving, the same landing, duration). Lisbon is an
# hour behind Madrid.
LEGS = [("Outbound", "Wednesday, October 21", "BY 471", ("08:35", "MAD", "Madrid · Terminal 4"),
         ("08:55", "LIS", "Lisbon · Terminal 1"), "1 h 20 min"),
        ("Return", "Friday, October 23", "BY 476", ("19:40", "LIS", "Lisbon · Terminal 1"),
         ("21:55", "MAD", "Madrid · Terminal 4"), "1 h 15 min")]


def booking() -> None:
    """Lucía's flights to the Lisbon offsite, booked at 9:14 on October 12, a holiday, as her calendar planned. Blue
    Yonder Airlines is one of Microsoft's fictitious companies; its wing is drawn here, not anyone's logo."""
    legs = "".join(f"""<div class="leg"><div class="head"><span class="dir">{direction}</span>{day}<span class="fl">
{flight}</span></div><div class="route"><div class="end"><b>{leave[0]}</b><span>{leave[1]}</span><small>{leave[2]}
</small></div><div class="path">{length}<div class="line">{PLANE}</div>Direct</div><div class="end arrive">
<b>{land[0]}</b><span>{land[1]}</span><small>{land[2]}</small></div></div><div class="tags"><span>Economy</span>
<span>Seat 14C</span><span>1 cabin bag · 10 kg</span><span>Operated by Blue Yonder Airlines</span></div></div>"""
                   for direction, day, flight, leave, land, length in LEGS)
    wing = ('<svg width="36" height="26" viewBox="0 0 36 26"><path d="M2 21C11 21 23 15 34 3c-4 10-13 18-26 20z" '
            'fill="#5fb3ff"/><path d="M9 25c8-1 15-5 21-12-2 7-9 12-18 13z" fill="#fff" fill-opacity=".85"/></svg>')
    content = f"""<div class="by"><div class="mast">
<div class="logo">{wing}<div><b>BLUE YONDER</b><small>AIRLINES</small>
</div></div><div class="links"><span>Book</span><span class="on">My trips</span><span>Check in</span><span>Flight status
</span></div><div class="me"><i>LR</i>Lucía R.</div></div><div class="page"><div class="trail">My trips › MT-4Q7ZK</div>
<div class="ok"><div class="tick">{TICK}</div><div><h1>Your trip is confirmed</h1><p>We've sent the details to
<b>lucia.romero@contoso.com</b>.</p></div><div class="ref"><small>Booking reference</small><b>MT-4Q7ZK</b></div></div>
<div class="grid"><div class="legs">{legs}<div class="extras"><div class="extra"><b>Add a checked bag</b><small>From
25 € per flight</small></div><div class="extra"><b>Extra legroom</b><small>Seats from 12 €</small></div>
<div class="extra"><b>Hotels in Lisbon</b><small>Deals near Alfama and Baixa</small></div></div></div><aside>
<div class="card"><h3>Passenger</h3><div class="pax"><i>LR</i><div><b>Lucía Romero</b><small>Adult · Economy</small>
</div></div></div><div class="card"><h3>Price summary</h3><dl><dt>Fare · 1 adult</dt><dd>142.00 €</dd>
<dt>Taxes and charges</dt><dd>44.40 €</dd></dl><div class="total"><span>Total paid</span><b>186.40 €</b></div>
<p class="paid">Visa •••• 0119 · October 12, 2026</p></div><div class="btn go">Add to calendar</div>
<div class="btn">Change or cancel</div><p class="hint">Online check-in opens 24 hours before departure: Tuesday,
October 20 at 08:35.</p></aside></div></div></div>"""
    screenshot(browser(content, (1280, 820), "blueyonderairlines.com/trips/MT-4Q7ZK", AIRLINE_CSS), (1280, 820),
               "10-12 09.14.03")


TASKS_CSS = """.tk{position:absolute;inset:0;display:grid;grid-template-columns:232px 1fr;background:#f7f7f8;
font:13.5px/1.4 system-ui;color:#1f2328}
.tk svg{display:block}
.tk aside{background:#fbfbfc;border-right:1px solid #e6e6e9;padding:18px 12px}
.tk .logo{display:flex;align-items:center;gap:10px;margin:0 8px 22px;font:800 15px system-ui;letter-spacing:-.01em}
.tk .logo i{width:26px;height:26px;border-radius:7px;background:#0f766e;display:grid;place-items:center}
.tk .logo svg{width:18px;height:18px;fill:none;stroke:#fff;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}
.tk aside h6{margin:20px 10px 6px;font:600 11px system-ui;letter-spacing:.07em;text-transform:uppercase;color:#8b8f97}
.tk .go{display:flex;align-items:center;gap:10px;height:32px;padding:0 10px;border-radius:7px;color:#3d434b}
.tk .go i{width:10px;height:10px;border-radius:3px}.tk .go em{margin-left:auto;font:600 11.5px system-ui;
font-style:normal;color:#6b7078}
.tk .go.on{background:#e6f2f0;color:#0f5f58;font-weight:600}.tk .go.sub{height:28px;padding-left:30px;font-size:13px}
.tk .go.sub.on{background:none;color:#0f766e;box-shadow:inset 2px 0 #0f766e}
.tk main{display:flex;flex-direction:column;min-width:0;padding:20px 26px 22px}
.tk .trail{font:500 12.5px system-ui;color:#6b7078}.tk .trail span{margin:0 6px;color:#b0b4bb}
.tk h1{margin:4px 0 8px;font:750 25px system-ui;letter-spacing:-.015em}
.tk .meta{display:flex;align-items:center;gap:14px;color:#5c6370}
.tk .goal{padding:4px 11px;border-radius:999px;border:1px solid #fde1a6;background:#fff8e8;color:#8a5a00;
font-weight:600}
.tk .team{margin-left:auto;display:flex}.tk .team b{margin-left:-6px;border:2px solid #f7f7f8}
.tk .face{width:26px;height:26px;border-radius:50%;display:grid;place-items:center;font:700 10px system-ui;color:#fff}
.tk .tools{display:flex;gap:10px;margin:16px 0 14px}
.tk .search,.tk .btn{height:34px;border:1px solid #dcdde1;border-radius:8px;background:#fff;display:flex;
align-items:center;padding:0 12px}
.tk .search{width:280px;color:#8b8f97}.tk .btn{font-weight:600;color:#3d434b}
.tk .btn.new{margin-left:auto;border-color:#0f766e;background:#0f766e;color:#fff}
.tk .cols{flex:1;min-height:0;display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.tk .col{border-radius:12px;background:#eef0f2;padding:12px 10px;display:flex;flex-direction:column;gap:9px}
.tk .col h2{display:flex;align-items:center;gap:8px;margin:2px 4px 3px;font:700 11.5px system-ui;letter-spacing:.06em;
text-transform:uppercase;color:#5c6370}
.tk .col h2 em{padding:0 8px;border-radius:999px;background:#dde0e4;font-style:normal;color:#3d434b}
.tk .col h2 small{margin-left:auto;font:500 12px system-ui;letter-spacing:0;text-transform:none;color:#8b8f97}
.tk .card{background:#fff;border:1px solid #e3e5e8;border-radius:10px;padding:11px 12px;
box-shadow:0 1px 2px rgba(16,24,40,.05)}
.tk .card p{margin:0 0 9px;font:600 14px/1.35 system-ui}
.tk .done p{color:#5c6370}
.tk .labels{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:9px}
.tk .labels span{padding:1px 8px;border-radius:6px;font:600 11.5px/18px system-ui}
.tk .foot{display:flex;align-items:center;gap:8px;font-size:12.5px;color:#6b7078}
.tk .key{display:flex;align-items:center;gap:5px;font:600 12px "SF Mono",Menlo,monospace}
.tk .key svg{width:14px;height:14px;fill:none;stroke:#16a34a;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
.tk .extra{padding:1px 7px;border-radius:6px;background:#f1f2f4;font:600 11.5px/18px system-ui;color:#3d434b}
.tk .extra.today{background:#fff1e0;color:#b45309}
.tk .pts{margin-left:auto;min-width:20px;height:20px;border-radius:10px;background:#eef0f2;display:grid;
place-items:center;font:700 11px system-ui;color:#3d434b}"""
FACES = {"LR": "#7c3aed", "AC": "#db2777", "SN": "#2563eb", "PS": "#ea580c", "JM": "#0891b2", "MP": "#475569",
          "MG": "#16a34a"}
LABELS = {"agent": ("#ede9fe", "#5b21b6"), "ops": ("#ffedd5", "#9a3412"), "security": ("#fee2e2", "#991b1b"),
          "infra": ("#e0f2fe", "#075985"), "evals": ("#dcfce7", "#166534"), "report": ("#fef9c3", "#854d0e"),
          "before beta": ("#dc2626", "#fff")}
# Sprint 15 of the returns assistant on its first morning, from the retro of October 14 and the review before it:
# (column, [(number, title, labels, owner, points, due date, pull request or version)]).
SPRINT = [
    ("To do", [(151, "Hand off to a person after 2 failed answers", ["agent"], "AC", 3, ""),
               (149, "Check that the order belongs to the customer", ["security", "before beta"], "SN", 3, ""),
               (152, "Courier pickups in production", ["ops"], "PS", 5, ""),
               (153, "Double the model quota before the sales beta", ["infra"], "JM", 1, "")]),
    ("In progress", [(147, "Alerts: p95 over 8 s, or more than 10 errors in 5 minutes", ["ops"], "SN", 3,
                      "Due Fri, Oct 16"),
                     (148, "Staging: from an API key to managed identity (ADR 0007)", ["security"], "MP", 5, ""),
                     (140, "Weekly pilot report", ["report"], "AC", 1, "Due today, 17:00")]),
    ("In review", [(145, "Evals in CI: fail the build if a metric drops more than 5%", ["evals"], "SN", 3, "PR #59")]),
    ("Done · last 7 days", [(144, "MCP server for orders: lookups, returns and pickups", ["agent"], "SN", 5, "PR #58"),
                            (141, "Retry the model's 429s with backoff", ["agent"], "SN", 2, "Version 9"),
                            (139, "Golden set: 120 conversations", ["evals"], "AC", 3, ""),
                            (138, "Pickup slots: 2 hours, Mon–Sat 8:00–20:00", ["ops"], "PS", 2, "")]),
]


def sprint_board() -> None:
    """Sprint 15's board at 10:31 on October 15, during its planning: what the retro and the review decided."""
    columns = []
    for name, cards in SPRINT:
        done = name.startswith("Done")
        html = []
        for number, title, labels, owner, points, extra in cards:
            tags = "".join(f'<span style="background:{LABELS[label][0]};color:{LABELS[label][1]}">{label}</span>'
                           for label in labels)
            note = f'<span class="extra{" today" if "today" in extra else ""}">{esc(extra)}</span>' if extra else ""
            html.append(f'<div class="card{" done" if done else ""}"><p>{esc(title)}</p><div class="labels">{tags}'
                        f'</div><div class="foot"><span class="key">{TICK if done else ""}CX-{number}</span>{note}'
                        f'<span class="pts">{points}</span><b class="face" style="background:{FACES[owner]}">'
                        f'{owner}</b></div></div>')
        limit = "<small>limit 4</small>" if name == "In progress" else ""
        columns.append(f'<div class="col"><h2>{esc(name)}<em>{len(cards)}</em>{limit}</h2>{"".join(html)}</div>')
    team = "".join(f'<b class="face" style="background:{color}">{who}</b>' for who, color in FACES.items())
    points = sum(card[4] for name, cards in SPRINT if not name.startswith("Done") for card in cards)
    projects = [("Trailhead 3 launch", "#ea580c"), ("Data platform", "#0891b2"), ("Data Summit 2026", "#7c3aed")]
    content = f"""<div class="tk"><aside><div class="logo"><i>{TICK}</i>Contoso Tasks</div><div class="go">My work</div>
<div class="go">Inbox<em>3</em></div><h6>Projects</h6><div class="go on"><i style="background:#0f766e"></i>Returns
assistant</div><div class="go sub on">Board</div><div class="go sub">Backlog</div><div class="go sub">Sprints</div>
<div class="go sub">Reports</div>
{"".join(f'<div class="go"><i style="background:{c}"></i>{p}</div>' for p, c in projects)}
</aside><main><div class="trail">Customer experience<span>/</span>Returns assistant<span>/</span>Board</div>
<h1>Sprint 15</h1><div class="meta"><span>Oct 15 – Oct 28, 2026 · day 1 of 10 · {points} points</span>
<span class="goal">Goal: ready for the sales beta on Nov 2</span><div class="team">{team}</div></div><div class="tools">
<div class="search">Search this board</div><div class="btn">Only my tasks</div><div class="btn">Group by: none</div>
<div class="btn new">+ New task</div></div><div class="cols">{"".join(columns)}</div></main></div>"""
    screenshot(browser(content, (1440, 900), "tasks.contoso.com/cx/returns-assistant/sprint-15", TASKS_CSS),
               (1440, 900), "10-15 10.31.56")


REPORT_CSS = """.rp{position:absolute;inset:0;background:#f5f6fa;padding:24px 40px;font:14px/1.45 system-ui;
color:#101828}
.rp .top2{display:flex;align-items:center;gap:10px;font:600 12.5px system-ui;color:#475467}
.rp .top2 i{width:22px;height:22px;border-radius:6px;background:#1d4ed8}
.rp .top2 span{margin-left:auto;height:32px;padding:0 13px;border:1px solid #d0d5dd;border-radius:8px;background:#fff;
display:flex;align-items:center;color:#344054}.rp .top2 span+span{margin-left:0}
.rp h1{margin:16px 0 4px;font:750 27px system-ui;letter-spacing:-.02em}
.rp .sub{color:#475467}
.rp .kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin:20px 0 16px}
.rp .kpi,.rp .panel{background:#fff;border:1px solid #e4e7ec;border-radius:14px;box-shadow:0 1px 2px rgba(16,24,40,.04)}
.rp .kpi{padding:16px 18px}
.rp .kpi small{display:block;font:600 12.5px system-ui;color:#475467}
.rp .kpi b{display:block;margin:6px 0 4px;font:750 34px/1.1 system-ui;letter-spacing:-.02em;
font-variant-numeric:tabular-nums}.rp .kpi b i{margin-left:5px;font:600 15px system-ui;font-style:normal;color:#667085}
.rp .kpi span{font:600 12.5px system-ui;color:#667085}.rp .kpi .good{color:#067647}
.rp .row2{display:grid;grid-template-columns:1.55fr 1fr;gap:14px}
.rp .panel{padding:18px 22px}
.rp h2{margin:0 0 4px;font:700 15px system-ui}.rp .panel>p{margin:0;color:#667085;font-size:13px}
.rp .bars{display:flex;align-items:flex-end;gap:26px;height:268px;margin-top:14px;padding:0 10px;
border-bottom:1px solid #d0d5dd;background:repeating-linear-gradient(to top,transparent 0 66px,#f0f1f4 66px 67px)}
.rp .bar2{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px}
.rp .bar2 em{font:700 13px system-ui;font-style:normal;color:#344054}
.rp .bar2 i{width:100%;border-radius:8px 8px 0 0;background:#c7d7fe}.rp .bar2.now i{background:#1d4ed8}
.rp .bar2.now em{color:#1d4ed8}
.rp .weeks{display:flex;gap:26px;padding:8px 10px 0;font:600 12.5px system-ui;color:#667085}
.rp .weeks span{flex:1;text-align:center}
.rp .incident{margin:10px 0 18px;padding:12px 14px;border-radius:10px;border:1px solid #fecdca;background:#fef3f2}
.rp .incident b{display:block;color:#b42318;font-size:13.5px}.rp .incident p{margin:3px 0 0;color:#7a271a;
font-size:13px}
.rp ul{margin:8px 0 0;padding:0;list-style:none;display:flex;flex-direction:column;gap:9px}
.rp li{display:flex;justify-content:space-between;gap:12px;padding-bottom:9px;border-bottom:1px solid #f0f1f4;
font-weight:600}.rp li span{flex:none;font-weight:500;color:#667085}
.rp .foot2{margin-top:14px;font-size:12px;color:#98a2b3}"""
# Resolved without a person, by week: up to the town hall's 62% for the week of October 5, and this week's 67%.
WEEKS = [("Sep 14", 41), ("Sep 21", 49), ("Sep 28", 55), ("Oct 5", 62), ("Oct 12", 67)]


def weekly_report() -> None:
    """Ana's weekly pilot report at 17:44 on October 15, as the meeting about it ends. Its numbers are the ones the
    weekly summary recording says, and the town hall's before them."""
    bars = "".join(f'<div class="bar2{" now" if index == len(WEEKS) - 1 else ""}"><em>{value}%</em>'
                   f'<i style="height:{value * 3.3:.0f}px"></i></div>' for index, (_, value) in enumerate(WEEKS))
    weeks = "".join(f"<span>{week}</span>" for week, _ in WEEKS)
    kpis = [("Resolved without a person", "67%", "", "▲ 5 pts vs last week", True),
            ("Conversations", "1,186", "", "Monday to Thursday", False),
            ("Customer satisfaction", "4.6", "/ 5", "Target 4.5 ✓", True),
            ("Average time to resolve", "3.5", "min", "▼ from 4 min", True),
            ("Groundedness", "4.1", "", "Bar 4.0 · new policy index", False)]
    tiles = "".join(f'<div class="kpi"><small>{label}</small><b>{value}{f"<i>{unit}</i>" if unit else ""}</b>'
                    f'<span{" class=good" if good else ""}>{note}</span></div>'
                    for label, value, unit, note, good in kpis)
    steps = [("MCP server permissions (CX-150)", "Sara · by Nov 2"),
             ("Staging: managed identity, ADR 0007", "Marc · by Oct 30"),
             ("Courier pickups in production", "Pablo · sprint 15"),
             ("Sales team joins the pilot", "Mon, Nov 2")]
    todo = "".join(f"<li>{what}<span>{who}</span></li>" for what, who in steps)
    content = f"""<div class="rp"><div class="top2"><i></i>Contoso · Customer experience reports<span>Share</span>
<span>Export PDF</span></div><h1>Returns assistant · weekly pilot report</h1><div class="sub">Week of October 12, 2026
· Monday to Thursday · prepared by Ana Castillo</div><div class="kpis">{tiles}</div>
<div class="row2"><div class="panel">
<h2>Resolved without a person, by week</h2><p>Share of conversations the assistant closed on its own. Week starting:
</p><div class="bars">{bars}</div><div class="weeks">{weeks}</div></div><div class="panel"><h2>Incident</h2>
<div class="incident"><b>Tue, Oct 13 · 11:00–11:20 · 429 from the model</b><p>Two drops from the model's rate limit.
Customers saw an error and no alert fired. Fixed with retries in version 9.</p></div><h2>Next</h2><ul>{todo}</ul></div>
</div><div class="foot2">Source: conversation logs and evaluation runs · updated Oct 15, 2026, 17:40</div></div>"""
    screenshot(browser(content, (1280, 860), "reports.contoso.com/cx/returns-assistant/weekly", REPORT_CSS),
               (1280, 860), "10-15 17.44.09")


# MARK: Apps

# Lucía's Mac is in Spanish: her week in Calendar, Tom's email in Mail and Pablo's messages. Their windows have a
# toolbar 52 points tall, with the traffic lights over the sidebar.
NATIVE_CSS = """.bar{position:absolute;left:0;right:0;top:0;height:52px;padding:0 20px;background:none;border:0;
z-index:4}"""
ICONS = {
    "sidebar": '<rect x="1.5" y="2.5" width="17" height="15" rx="3.5"/><path d="M7.5 2.5v15"/>',
    "inbox": '<path d="M2 11.5L4.5 4h11l2.5 7.5V17H2zM2 11.5h5l1 2h4l1-2h5"/>',
    "plus": '<path d="M10 3v14M3 10h14"/>',
    "search": '<circle cx="8.5" cy="8.5" r="5.5"/><path d="M12.6 12.6L17 17"/>',
    "archive": '<path d="M2.5 3.5h15v4h-15zM4 7.5v9h12v-9M8 11h4"/>',
    "trash": '<path d="M3 5.5h14M8 5.5v-2h4v2M5 5.5l1 11.5h8l1-11.5"/>',
    "junk": '<path d="M3 5.5h14M5 5.5l1 11.5h8l1-11.5M8 9l4 4M12 9l-4 4"/>',
    "reply": '<path d="M8 4L3 9l5 5M3 9h8.5a5.5 5.5 0 0 1 5.5 5.5V16"/>',
    "reply_all": '<path d="M7 4L2 9l5 5M11 4L6 9l5 5M6 9h6.5a5.5 5.5 0 0 1 5.5 5.5V16"/>',
    "forward": '<path d="M12 4l5 5-5 5M17 9H8.5A5.5 5.5 0 0 0 3 14.5V16"/>',
    "flag": '<path d="M4.5 18V2.5M4.5 3h11l-2.5 4 2.5 4h-11"/>',
    "compose": '<path d="M13.5 3.5l3 3-8 8h-3v-3zM3 17.5h14"/>',
    "filter": '<circle cx="10" cy="10" r="7.5"/><path d="M6.5 8h7M7.8 10.8h4.4M9.1 13.6h1.8"/>',
    "sent": '<path d="M2.5 9.5L17.5 3l-5.5 15-2.5-6.5zM9.5 11.5L17.5 3"/>',
    "draft": '<path d="M5 2.5h7l3.5 3.5v11.5H5zM12 2.5V6h3.5M7.5 10h5M7.5 13h5"/>',
    "folder": '<path d="M2.5 5.5v10.5h15V7H9.5L8 4.5H3z"/>',
    "video": '<rect x="1.5" y="5" width="12" height="10" rx="2.5"/><path d="M13.5 9l5-3v8l-5-3"/>',
    "info": '<circle cx="10" cy="10" r="7.5"/><path d="M10 9v5M10 6.2v.3"/>',
    "mic": '<rect x="7.5" y="2.5" width="5" height="9" rx="2.5"/><path d="M4.5 9.5a5.5 5.5 0 0 0 11 0M10 15v2.5"/>',
    "clip": ('<path d="M14.5 9l-5.6 5.6a3.2 3.2 0 0 1-4.5-4.5l6-6a2.1 2.1 0 0 1 3 3l-5.9 5.9a1 1 0 0 1-1.5-1.5'
             'L11.5 6"/>'),
}
SIDEBAR_CSS = """.os svg{display:block;width:20px;height:20px;fill:none;stroke:#717176;stroke-width:1.5;
stroke-linecap:round;stroke-linejoin:round}
.os aside{position:relative;background:#eaeaec;border-right:1px solid #d6d6d9}
.os h6{margin:12px 10px 4px;font:600 11px system-ui;color:#8a8a8f}
.os .find{height:30px;border-radius:8px;background:#e3e3e6;display:flex;align-items:center;gap:7px;padding:0 9px;
font:13px system-ui;color:#8a8a8f}.os .find svg{width:15px;height:15px;stroke:#8a8a8f}
.os .face{flex:none;border-radius:50%;background:linear-gradient(#a9a9ae,#86868b);display:grid;place-items:center;
font-weight:600;color:#fff}"""


def icon(name: str) -> str:
    return f'<svg viewBox="0 0 20 20">{ICONS[name]}</svg>'


def native(content: str, size: tuple[int, int], css: str) -> str:
    """A window of one of macOS's own apps, light, with `content` under its toolbar."""
    return window(f'<div class="os">{content}</div>', "", size, False, f"{NATIVE_CSS}\n{SIDEBAR_CSS}\n{css}")


# Lucía's calendars, colored as Calendar colors them.
CALENDARS = {"Trabajo": "#007aff", "Equipo CX": "#af52de", "Personal": "#34c759", "Viajes": "#ff9500",
             "Festivos en España": "#ff3b30"}
# Her week of October 12, where the recordings and screenshots come from: (day, start, end, title, calendar, place).
WEEK = [
    (12, "9:00", "9:30", "Reservar vuelos Lisboa", "Viajes", ""),
    (13, "9:30", "9:45", "Standup", "Equipo CX", ""),
    (13, "12:00", "12:45", "Llamada Northwind Traders", "Trabajo", ""),
    (13, "13:30", "15:00", "Comida con Fabrikam", "Trabajo", "La Huerta"),
    (13, "16:15", "16:45", "Evaluación v9", "Equipo CX", ""),
    (14, "9:30", "9:45", "Standup", "Equipo CX", ""),
    (14, "10:00", "13:00", "Taller: agentes con Microsoft Foundry", "Trabajo", "Sala Ártico"),
    (14, "16:45", "17:30", "Sprint review v0.4", "Equipo CX", ""),
    (14, "17:45", "18:15", "Retro sprint 14", "Equipo CX", ""),
    (15, "9:30", "9:45", "Standup", "Equipo CX", ""),
    (15, "10:00", "11:00", "Planificación sprint 15", "Equipo CX", "Sala Ártico"),
    (15, "11:30", "12:00", "Staging: identidad administrada · Marc", "Trabajo", ""),
    (15, "17:00", "17:45", "Resumen semanal del piloto", "Equipo CX", ""),
    (15, "18:30", "19:15", "Natación · Leo", "Personal", ""),
    (16, "9:30", "9:45", "Standup", "Equipo CX", ""),
    (16, "10:30", "11:30", "Data Summit · agenda con la agencia", "Trabajo", ""),
    (16, "12:00", "13:00", "Comité de seguridad", "Trabajo", "Sala Ártico"),
    (16, "15:00", "15:30", "Offsite Lisboa · hoteles (≤ 140 €/noche)", "Viajes", ""),
]
CALENDAR_CSS = """.cal{position:absolute;inset:0;display:grid;grid-template-columns:232px 1fr;font:13px system-ui;
color:#1d1d1f}
.cal aside{padding:58px 10px 16px;display:flex;flex-direction:column}
.cal .tools{position:absolute;top:16px;left:94px;display:flex;gap:20px}
.cal .it{display:flex;align-items:center;gap:9px;height:26px;padding:0 10px}
.cal .it i{width:15px;height:15px;border-radius:4px;background:var(--c);display:grid;place-items:center}
.cal .it i svg{width:13px;height:13px;stroke:#fff;stroke-width:3.4}
.cal .mini{margin-top:auto;padding:0 4px}
.cal .mini header{display:flex;align-items:center;margin:0 6px 6px;font:600 13px system-ui}
.cal .mini header span{margin-left:auto;font:500 15px system-ui;letter-spacing:12px;color:#717176}
.cal .mini .w,.cal .mini .r{display:grid;grid-template-columns:repeat(7,1fr);text-align:center}
.cal .mini .w{margin-bottom:2px;font:600 10.5px system-ui;color:#8a8a8f}
.cal .mini .r{height:26px;align-items:center;border-radius:7px;font:500 11.5px system-ui}
.cal .mini .r.sel{background:#d9d9de}
.cal .mini .r span{width:22px;height:22px;margin:auto;border-radius:50%;display:grid;place-items:center}
.cal .mini .out{color:#aeaeb2}.cal .mini .on{background:#ff3b30;color:#fff;font-weight:700}
.cal main{display:flex;flex-direction:column;min-width:0;background:#fff}
.cal .tb{position:relative;height:52px;flex:none}
.cal .add{position:absolute;left:14px;top:16px}
.cal .seg{position:absolute;left:50%;top:11px;transform:translateX(-50%);display:flex;padding:2px;border-radius:8px;
background:#e5e5e8}
.cal .seg span{width:76px;height:26px;border-radius:6px;display:grid;place-items:center;font:500 13px system-ui;
color:#3c3c43}
.cal .seg .on{background:#fff;color:#1d1d1f;box-shadow:0 1px 2px rgba(0,0,0,.18),0 0 0 .5px rgba(0,0,0,.06)}
.cal .tb .find{position:absolute;right:16px;top:11px;width:200px}
.cal .head{height:50px;flex:none;display:flex;align-items:center;padding:0 18px 0 20px}
.cal h1{margin:0;font:400 26px system-ui;letter-spacing:-.01em}.cal h1 b{font-weight:700}
.cal .go{margin-left:auto;display:flex;border:1px solid #d6d6d9;border-radius:7px;overflow:hidden}
.cal .go span{height:26px;padding:0 11px;display:grid;place-items:center;font:500 13px system-ui;color:#3c3c43}
.cal .go span+span{border-left:1px solid #d6d6d9}
.cal .days,.cal .allday,.cal .grid{display:grid;grid-template-columns:64px repeat(5,minmax(0,1fr))}
.cal .days{height:34px;flex:none;align-items:center}
.cal .dh{padding-left:9px;font:500 13.5px system-ui;color:#3c3c43}.cal .dh b{font-weight:600}
.cal .dh.today{color:#ff3b30}
.cal .dh.today b{display:inline-grid;place-items:center;min-width:26px;height:24px;margin-left:2px;padding:0 5px;
border-radius:12px;background:#ff3b30;color:#fff}
.cal .allday{flex:none;height:30px;border-top:1px solid #e4e4e7;border-bottom:1px solid #cfcfd4}
.cal .allday>div{border-left:1px solid #e4e4e7;padding:4px 5px 0 2px}
.cal .allday .gut{border-left:0;padding:9px 6px 0 0;text-align:right;white-space:nowrap;font:500 10px system-ui;
color:#8a8a8f}
.cal .ad,.cal .ev{background:color-mix(in srgb,var(--c) 17%,#fff);color:color-mix(in srgb,var(--c) 62%,#000)}
.cal .ad{display:flex;align-items:center;height:20px;padding:0 7px;border-radius:4px;font:600 11.5px system-ui}
.cal .grid{flex:1;min-height:0;position:relative;overflow:hidden}
.cal .hours{position:relative}
.cal .hours span{position:absolute;right:8px;font:500 10.5px/14px system-ui;color:#8a8a8f}
.cal .hours .nowl{color:#ff3b30;font-weight:700}
.cal .col{position:relative;z-index:1;border-left:1px solid #e4e4e7}
.cal .lines{position:absolute;left:64px;right:0;top:0;bottom:0}
.cal .lines i{position:absolute;left:0;right:0;height:1px;background:#ececef}
.cal .ev{position:absolute;left:2px;right:5px;overflow:hidden;padding:1px 6px 0 7px;border-left:3px solid var(--c);
border-radius:4px;font:11.5px/13px system-ui}
.cal .ev b{display:block;font-weight:600}.cal .ev span{display:block}
.cal .ev.short{padding-top:0;white-space:nowrap;font-size:10.5px}
.cal .now{position:absolute;left:-1px;right:0;z-index:2;height:2px;margin-top:-1px;background:#ff3b30}
.cal .now:before{content:"";position:absolute;left:-4px;top:-4px;width:10px;height:10px;border-radius:50%;
background:#ff3b30}"""


def clock(text: str) -> int:
    """Minutes since midnight, of "9:30"."""
    hours, minutes = text.split(":")
    return int(hours) * 60 + int(minutes)


def calendar() -> None:
    """Lucía's week in Calendar at 8:47 on October 14, the morning of the workshop."""
    top, now, today = clock("7:45"), clock("8:47"), 14  # the grid starts at 7:45, one point a minute
    days = [(12, "lun"), (13, "mar"), (14, "mié"), (15, "jue"), (16, "vie")]
    groups = [("Contoso", ["Trabajo", "Equipo CX"]), ("iCloud", ["Personal", "Viajes"]),
              ("Otros", ["Festivos en España"])]
    side = "".join(f"<h6>{group}</h6>" + "".join(f'<div class="it"><i style="--c:{CALENDARS[name]}">{TICK}</i>'
                                                 f"{esc(name)}</div>" for name in names) for group, names in groups)
    first = dt.date(2026, 9, 28)  # the Monday before October 1
    weeks = []
    for week in range(6):
        cells = []
        for offset in range(7):
            date = first + dt.timedelta(days=7 * week + offset)
            kind = "on" if date == dt.date(2026, 10, today) else "out" if date.month != 10 else ""
            cells.append(f'<span class="{kind}">{date.day}</span>' if kind else f"<span>{date.day}</span>")
        shown = first + dt.timedelta(days=7 * week) == dt.date(2026, 10, 12)
        weeks.append(f'<div class="r{" sel" if shown else ""}">{"".join(cells)}</div>')
    initials = "".join(f"<span>{letter}</span>" for letter in "LMXJVSD")
    heads = "".join(f'<div class="dh{" today" if day == today else ""}">{name} <b>{day}</b></div>'
                    for day, name in days)
    holiday = f'<span class="ad" style="--c:{CALENDARS["Festivos en España"]}">Fiesta Nacional de España</span>'
    allday = "".join(f"<div>{holiday if day == 12 else ''}</div>" for day, _ in days)
    columns = []
    for day, _ in days:
        events = []
        for when, start, end, title, name, place in WEEK:
            if when != day:
                continue
            length = clock(end) - clock(start)
            lines = (f"<b>{esc(title)}</b>" + (f"<span>{start}–{end}</span>" if length >= 45 else "")
                     + (f"<span>{esc(place)}</span>" if place and length >= 60 else ""))
            events.append(f'<div class="ev{" short" if length < 30 else ""}" style="top:{clock(start) - top}px;'
                          f'height:{length - 1}px;--c:{CALENDARS[name]}">{lines}</div>')
        if day == today:
            events.append(f'<div class="now" style="top:{now - top}px"></div>')
        columns.append(f'<div class="col">{"".join(events)}</div>')
    hours = range(8, 20)
    labels = "".join(f'<span style="top:{60 * hour - top - 7}px">{hour}:00</span>' for hour in hours
                     if abs(60 * hour - now) > 15)  # the time now hides the hour it's close to
    labels += f'<span class="nowl" style="top:{now - top - 7}px">{now // 60}:{now % 60:02}</span>'
    lines = "".join(f'<i style="top:{60 * hour - top}px"></i>' for hour in hours)
    content = f"""<div class="cal"><aside><div class="tools">{icon("sidebar")}{icon("inbox")}</div>{side}
<div class="mini"><header>octubre 2026<span>‹›</span></header><div class="w">{initials}</div>{"".join(weeks)}</div>
</aside><main><div class="tb"><div class="add">{icon("plus")}</div><div class="seg"><span>Día</span>
<span class="on">Semana</span><span>Mes</span><span>Año</span></div><div class="find">{icon("search")}Buscar</div>
</div><div class="head"><h1><b>octubre</b> 2026</h1><div class="go"><span>‹</span><span>Hoy</span><span>›</span></div>
</div><div class="days"><div></div>{heads}</div><div class="allday"><div class="gut">todo el día</div>{allday}</div>
<div class="grid"><div class="hours">{labels}</div>{"".join(columns)}<div class="lines">{lines}</div></div></main>
</div>"""
    screenshot(native(content, (1440, 900), CALENDAR_CSS), (1440, 900), "10-14 08.47.30")


# Lucía's inbox at 19:05 on October 14: (sender, when, subject, preview, unread, attachment). Tom's email is open.
# The IT service desk's email doesn't say the locker's code: only its voicemail does.
INBOX = [
    ("Tom Becker", "19:03", "PO 5518 – new delivery date and tracking",
     "Hi Lucía, as I said in my voicemail yesterday, the container with the aluminum poles for your Trailhead 3 "
     "tents missed its vessel in Rotterdam.", False, False),
    ("Marta Gil", "18:20", "Nota de prensa Trailhead 3 – borrador v2",
     "Hola, Lucía: te paso la segunda versión con el peso (1,9 kg) y el precio, 249 €. ¿Puedes revisarla antes del "
     "viernes?", True, True),
    ("Sara Navarro", "17:55", "Retro sprint 14 – foto de la pizarra",
     "Os dejo la foto de la pizarra. Acciones: alertas de latencia y errores (yo, el viernes), más cuota del modelo "
     "(Javier) y pasar antes a una persona (Ana).", True, True),
    ("Contoso Academy", "13:22", "Tu certificado: Agentes con Microsoft Foundry",
     "Enhorabuena, Lucía. Has completado el taller práctico de hoy. Descarga tu certificado y compártelo.", False,
     True),
    ("Ana Castillo", "Ayer", "Golden set: ya son 120 conversaciones",
     "Hemos cerrado el golden set con 120 conversaciones reales del piloto, cada una con su respuesta esperada.",
     False, False),
    ("IT Service Desk", "lunes", "Tu portátil nuevo está listo – taquilla 14",
     "Te hemos dejado un mensaje de voz con el código de la taquilla. Recoge el portátil antes del viernes, por "
     "favor.", False, False),
    ("Blue Yonder Airlines", "lunes", "Your trip MT-4Q7ZK is confirmed",
     "Madrid → Lisbon · Wed, Oct 21 · BY 471 · 08:35. Return Fri, Oct 23 · BY 476 · 19:40.", False, False),
    ("Data Summit Madrid", "2/10/26", "Save the date: 12 de noviembre",
     "Data Summit Madrid vuelve el jueves 12 de noviembre: 900 profesionales de datos e IA en un solo día.", False,
     False),
]
TOM = """<p>Hi Lucía,</p><p>As I said in my voicemail yesterday, the container with the aluminum poles for your
Trailhead 3 tents (purchase order 5518) missed its vessel in Rotterdam. It's booked on the next sailing, so the delivery
moves to next week:</p><p><b>New delivery date:</b> Tuesday, October 20, between 8:00 and 12:00<br><b>Delivery to:</b>
Contoso Outdoor warehouse, Zaragoza<br><b>Tracking number:</b> FBK-RTM-772041</p><p>The driver will need a signature on
delivery. Everything else in the order is still on schedule.</p><p>Again, my apologies for the delay. Call me if
anything changes on your side.</p><p>Best,<br>Tom</p><div class="sig">Tom Becker<br>Key Account Manager · Europe<br>
Fabrikam Logistics · Rotterdam · Zaragoza<br>+1 425 555 0142</div>"""
MAIL_CSS = """.ml{position:absolute;inset:0;display:grid;grid-template-columns:216px 372px 1fr;font:13px system-ui;
color:#1d1d1f}
.ml aside{padding:56px 10px 0}
.ml .it{display:flex;align-items:center;gap:9px;height:28px;padding:0 10px;border-radius:7px}
.ml .it svg{width:17px;height:17px;stroke:#0a7aff}
.ml .it em{margin-left:auto;font:600 12px system-ui;font-style:normal;color:#8a8a8f}
.ml .it.on{background:#d9d9de}
.ml .list{display:flex;flex-direction:column;min-width:0;background:#fff;border-right:1px solid #e1e1e4}
.ml .lh{height:52px;flex:none;display:flex;align-items:center;gap:16px;padding:0 16px 0 22px}
.ml .lh div{margin-right:auto}.ml .lh b{display:block;font:700 15px/1.2 system-ui}
.ml .lh small{font:500 11.5px system-ui;color:#8a8a8f}
.ml .msg{position:relative;margin:0 8px;padding:9px 12px 10px 22px;border-radius:9px}
.ml .msg+.msg:before{content:"";position:absolute;left:22px;right:4px;top:0;border-top:1px solid #e8e8eb}
.ml .msg.on:before,.ml .msg.on+.msg:before{display:none}
.ml .msg.on{background:#0a64d8;color:#fff}
.ml .hd{display:flex;align-items:center;gap:6px}
.ml .hd b{flex:1;font:700 13.5px system-ui}
.ml .hd svg{width:13px;height:13px}
.ml .hd time{font:500 12px system-ui;color:#8a8a8f}
.ml .msg h4{margin:1px 0 2px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;font:500 13px system-ui}
.ml .msg p{margin:0;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;
font:12.5px/1.38 system-ui;color:#717176}
.ml .msg.on time,.ml .msg.on p{color:rgba(255,255,255,.85)}.ml .msg.on svg{stroke:#fff}
.ml .dot{position:absolute;left:7px;top:15px;width:9px;height:9px;border-radius:50%;background:#0a7aff}
.ml .read{display:flex;flex-direction:column;min-width:0;background:#fff}
.ml .tb{height:52px;flex:none;display:flex;align-items:center;gap:20px;padding:0 16px 0 24px;
border-bottom:1px solid #e8e8eb}
.ml .tb i{width:10px}.ml .tb .find{margin-left:auto;width:200px}
.ml .sheet{padding:22px 32px 0 28px}
.ml .from{display:flex;gap:14px;padding-bottom:16px;border-bottom:1px solid #e8e8eb}
.ml .from .face{width:44px;height:44px;font-size:17px}
.ml .from b{display:block;font:700 15px/1.3 system-ui}
.ml .from h2{margin:2px 0 4px;font:600 13.5px system-ui}
.ml .from p{margin:1px 0 0;font:12.5px system-ui;color:#3c3c43}.ml .from p span{color:#8a8a8f}
.ml .from time{margin-left:auto;font:500 12px system-ui;color:#8a8a8f}
.ml .body{max-width:660px;padding:20px 0;font:14px/1.6 system-ui}
.ml .body p{margin:0 0 13px}
.ml .sig{margin-top:18px;font-size:13px;line-height:1.5;color:#6e6e73}"""


def mail() -> None:
    """Tom's email in Lucía's Mail at 19:05 on October 14: the tracking number his voicemail promised."""
    boxes = [("Favoritos", [("inbox", "Entrada", "2"), ("sent", "Enviados", ""), ("draft", "Borradores", "1"),
                            ("flag", "Marcados", "")]),
             ("Contoso", [("folder", "Proveedores", ""), ("folder", "Trailhead 3", ""),
                          ("folder", "Piloto asistente", ""), ("archive", "Archivo", ""), ("junk", "No deseado", ""),
                          ("trash", "Papelera", "")])]
    side = "".join(f"<h6>{group}</h6>" + "".join(
        f'<div class="it{" on" if name == "Entrada" else ""}">{icon(kind)}{name}{f"<em>{count}</em>" if count else ""}'
        "</div>" for kind, name, count in items) for group, items in boxes)
    rows = []
    for index, (sender, when, subject, preview, unread, attached) in enumerate(INBOX):
        rows.append(f'<div class="msg{" on" if index == 0 else ""}">{"<i class=dot></i>" if unread else ""}'
                    f'<div class="hd"><b>{esc(sender)}</b>{icon("clip") if attached else ""}<time>{when}</time></div>'
                    f"<h4>{esc(subject)}</h4><p>{esc(preview)}</p></div>")
    unread = sum(1 for message in INBOX if message[4])
    tools = "".join(icon(name) for name in ("archive", "trash", "junk")) + "<i></i>" + "".join(
        icon(name) for name in ("reply", "reply_all", "forward")) + "<i></i>" + icon("flag")
    content = f"""<div class="ml"><aside>{side}</aside><div class="list"><div class="lh"><div><b>Entrada</b>
<small>{unread} sin leer</small></div>{icon("filter")}{icon("compose")}</div>{"".join(rows)}</div><div class="read">
<div class="tb">{tools}<div class="find">{icon("search")}Buscar</div></div><div class="sheet"><div class="from">
<div class="face">TB</div><div><b>Tom Becker</b><h2>{esc(INBOX[0][2])}</h2><p><span>Para:</span> Lucía Romero</p>
<p><span>Cc:</span> Pablo Serrano</p></div><time>19:03</time></div><div class="body">{TOM}</div></div></div></div>"""
    screenshot(native(content, (1440, 900), MAIL_CSS), (1440, 900), "10-14 19.05.12")


# Lucía's conversations at 12:08 on October 15: (initials, name, when, last message). Pablo's is open.
CHATS = [("PS", "Pablo Serrano", "12:08", "Perfecto. Se lo digo a Marta para la nota de prensa."),
         ("AC", "Ana Castillo", "11:05", "Planificación cerrada: 24 puntos, y el objetivo es la beta de ventas del 2 "
                                         "de noviembre."),
         ("MG", "Marta Gil", "10:12", "¿Tienes un minuto hoy? Quiero cerrar la fecha de lanzamiento de la nota de "
                                      "prensa."),
         ("JM", "Javier Molina", "Ayer", "El informe de CSAT ya lee directamente de OneLake 👍"),
         ("SN", "Sara Navarro", "Ayer", "¡Gracias por la retro! Te he mandado la foto de la pizarra por correo."),
         ("MP", "Marc Puig", "martes", "Recuerda: el jueves quitamos la clave de staging. Nada de secretos en el "
                                       ".env 🙂")]
WITH_PABLO = [
    ("them", "Buenas noticias: Fabrikam confirma las varillas. Llegan al almacén de Zaragoza el martes 20, entre las 8 "
             "y las 12."),
    ("them", "Seguimiento: FBK-RTM-772041"),
    ("them", "El montaje son 8 días laborables, así que estarían listas el 30 de octubre."),
    ("me", "¿Llegamos al lanzamiento del 3 de noviembre?"),
    ("them", "Sí, con margen."),
    ("me", "Perfecto. Se lo digo a Marta para la nota de prensa."),
]
MESSAGES_CSS = """.im{position:absolute;inset:0;display:grid;grid-template-columns:300px 1fr;font:13px system-ui;
color:#1d1d1f}
.im aside{padding:52px 10px 0}
.im .new{position:absolute;top:16px;right:16px}
.im aside .find{margin:0 6px 10px}
.im .chat{display:flex;gap:11px;padding:9px 10px;border-radius:9px}
.im .chat.on{background:#0a7aff;color:#fff}
.im .chat .face{width:42px;height:42px;font-size:16px}
.im .tx{flex:1;min-width:0}
.im .hd{display:flex;align-items:baseline}
.im .hd b{font:600 13.5px system-ui}.im .hd time{margin-left:auto;font:12px system-ui;color:#8a8a8f}
.im .chat p{margin:1px 0 0;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;
font:12.5px/1.35 system-ui;color:#717176}
.im .chat.on time,.im .chat.on p{color:rgba(255,255,255,.85)}
.im main{display:flex;flex-direction:column;min-width:0;background:#fff}
.im .to{height:52px;flex:none;display:flex;align-items:center;gap:20px;padding:0 18px 0 20px;
border-bottom:1px solid #e8e8eb}
.im .to span{margin-right:-14px;color:#8a8a8f}.im .to b{margin-right:auto;font-weight:500}
.im .thread{flex:1;display:flex;flex-direction:column;justify-content:flex-end;padding:0 24px 14px}
.im .when{align-self:center;margin:0 0 10px;font:11px system-ui;color:#8a8a8f}.im .when b{font-weight:600}
.im .b{position:relative;max-width:440px;margin-top:2px;padding:7px 13px;border-radius:18px;font:14px/1.38 system-ui}
.im .them{align-self:flex-start;background:#e9e9eb;color:#000}
.im .me{align-self:flex-end;background:#0a84ff;color:#fff}
.im .gap{margin-top:12px}
.im .tail:before,.im .tail:after{content:"";position:absolute;bottom:0;height:20px}
.im .them.tail:before{left:-7px;width:20px;background:#e9e9eb;border-bottom-right-radius:15px}
.im .them.tail:after{left:-10px;width:10px;background:#fff;border-bottom-right-radius:10px}
.im .me.tail:before{right:-8px;width:20px;background:#0a84ff;border-bottom-left-radius:16px 14px}
.im .me.tail:after{right:-10px;width:10px;background:#fff;border-bottom-left-radius:10px}
.im .seen{align-self:flex-end;margin-top:3px;font:600 11px system-ui;color:#8a8a8f}
.im .cmp{flex:none;display:flex;align-items:center;gap:12px;padding:0 18px 16px}
.im .plus{width:30px;height:30px;border-radius:50%;background:#ececef;display:grid;place-items:center}
.im .plus svg{width:16px;height:16px}
.im .field{flex:1;height:34px;border-radius:17px;border:1px solid #d6d6d9;display:flex;align-items:center;
padding:0 8px 0 14px;font:14px system-ui;color:#a1a1a6}.im .field svg{margin-left:auto;width:18px;height:18px}"""


def messages() -> None:
    """Pablo telling Lucía in Messages, at 12:08 on October 15, that the poles arrive in time for the launch."""
    chats = "".join(f'<div class="chat{" on" if index == 0 else ""}"><div class="face">{initials}</div>'
                    f'<div class="tx"><div class="hd"><b>{name}</b><time>{when}</time></div><p>{esc(text)}</p></div>'
                    "</div>" for index, (initials, name, when, text) in enumerate(CHATS))
    bubbles = []
    for index, (who, text) in enumerate(WITH_PABLO):
        first = index == 0 or WITH_PABLO[index - 1][0] != who
        last = index == len(WITH_PABLO) - 1 or WITH_PABLO[index + 1][0] != who
        classes = ["b", who] + (["gap"] if first and index else []) + (["tail"] if last else [])
        bubbles.append(f'<div class="{" ".join(classes)}">{esc(text)}</div>')
    content = f"""<div class="im"><aside><div class="new">{icon("compose")}</div><div class="find">{icon("search")}
Buscar</div>{chats}</aside><main><div class="to"><span>Para:</span><b>Pablo Serrano</b>{icon("video")}{icon("info")}
</div><div class="thread"><div class="when"><b>Hoy</b> 11:52</div>{"".join(bubbles)}<div class="seen">Leído 12:08
</div></div><div class="cmp"><div class="plus">{icon("plus")}</div><div class="field">iMessage{icon("mic")}</div>
</div></main></div>"""
    screenshot(native(content, (1100, 760), MESSAGES_CSS), (1100, 760), "10-15 12.08.40")


# MARK: Recordings

# What a customer saw at 11:04 on October 13, while the model answered 429: no answer, then an error, twice.
WHERE = "Where's my order 50342? It said 2-3 days."
FAILED = ("notice", "Something went wrong on our side. Please try again, or tap Talk to a person.")
AFTER_ERROR = ["Try again", "Talk to a person"]
OUTAGE_STATES = [
    ([GREETING], "", True, 1.6),
    ([GREETING], WHERE[:16], True, 0.6),
    ([GREETING], WHERE[:30], True, 0.6),
    ([GREETING], WHERE, True, 0.9),
    ([GREETING, ("user", WHERE), ("typing",)], "", False, 4.5),
    ([GREETING, ("user", WHERE), FAILED], "", AFTER_ERROR, 2.4),
    ([GREETING, ("user", WHERE), FAILED], "Hello?", AFTER_ERROR, 0.9),
    ([GREETING, ("user", WHERE), FAILED, ("user", "Hello?"), ("typing",)], "", False, 3.6),
    ([GREETING, ("user", WHERE), FAILED, ("user", "Hello?"), FAILED], "", AFTER_ERROR, 3.4),
]
# Ana trying v0.4's courier pickups at 16:31 on October 14, before the sprint review, with Alex's return of his
# Trailhead 2 (the first recording's).
PICKUP = "Can a courier pick up my return? Order 48213."
SLOTS = ("agent", "Yes: returns of damaged items get a free courier pickup. I found order <b>#48213</b> and its return "
                  "<b>RMA-20931</b>. The courier comes Monday to Saturday, 8:00 to 20:00, in 2-hour slots. Which day "
                  "and time suit you?", ["Shipping options.pdf · p. 2"])
FRIDAY = "Friday morning, 10 to 12."
BOOKING = 'order_id="48213", date="2026-10-16", slot="10:00–12:00"'
BOOKED = ("agent", "Booked! A courier will pick up the tent on <b>Friday, October 16, between 10:00 and 12:00</b>. "
                   "Have the box ready with the <b>RMA-20931</b> label on it: we'll text you 30 minutes before they "
                   "arrive.", [])
ASKED = [("user", PICKUP), tool("lookup_order", 'order_id="48213"'), SLOTS]
PICKUP_STATES = [
    ([GREETING], "", True, 1.4),
    ([GREETING], PICKUP[:18], True, 0.6),
    ([GREETING], PICKUP[:33], True, 0.6),
    ([GREETING], PICKUP, True, 0.9),
    ([GREETING, ("user", PICKUP), tool("lookup_order", 'order_id="48213"', True)], "", False, 1.2),
    ([GREETING, *ASKED], "", False, 3.8),
    ([GREETING, *ASKED], FRIDAY[:14], False, 0.6),
    ([GREETING, *ASKED], FRIDAY, False, 0.9),
    ([GREETING, *ASKED, ("user", FRIDAY), tool("book_pickup", BOOKING, True)], "", False, 1.3),
    ([*ASKED, ("user", FRIDAY), tool("book_pickup", BOOKING), BOOKED], "", False, 4.0),
]


@builder
def more_screenshots():
    """Screenshots/: the outage in Sara's terminal and its fix, the evaluation, the pages Lucía's team keep open, and
    her Calendar, Mail and Messages."""
    for shot in (outage, evaluation, retries, booking, sprint_board, weekly_report, calendar, mail, messages):
        shot()


@builder
def more_recordings():
    """Video/: the support chat failing during the outage, and booking a courier pickup with v0.4."""
    record_chat(OUTAGE_STATES, out("Video/Screen Recording 2026-10-13 at 11.04.10.mov"))
    record_chat(PICKUP_STATES, out("Video/Screen Recording 2026-10-14 at 16.31.52.mov"))
