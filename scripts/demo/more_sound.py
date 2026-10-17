"""More of Biblo's demo files, the ones that speak: twenty recordings and twelve narrated videos.

make_demo.py imports this module, so its builders are groups like any other (scripts/make-demo.sh more_audio). They
tell more of the same made-up story: Contoso Outdoor's returns assistant, the Trailhead 3 tent's launch, the team's
offsite in Lisbon and the Data Summit in Madrid. Every fact about a product is public; every company, person and
number is invented. Videos are words and shapes only, never logos (assets/SOURCES.md)."""
from __future__ import annotations

import math
from pathlib import Path

from make_demo import (DATES, EXPLAINER_CSS, FFMPEG, FOUNDRY_CSS, WORK, builder, conversation, esc, explainer, out,
                       page, render, run, say, slideshow, stopwatch, voice)

# Who speaks: English voices for the English recordings, Spanish ones for the Spanish recordings. A recording is
# transcribed in one language, the one most of it is in, so none of them mixes the two.
SAMANTHA, DANIEL, KAREN, MOIRA = ("Samantha", "en_US"), ("Daniel", "en_GB"), ("Karen", "en_AU"), ("Moira", "en_IE")
TESSA, RISHI, AMAN = ("Tessa", "en_ZA"), ("Rishi", "en_IN"), ("Aman", "en_IN")
MONICA, PAULINA = ("Mónica", "es_ES"), ("Paulina", "es_MX")
REED_ES, EDDY_ES = ("Reed", "es_ES"), ("Eddy", "es_ES")

DATES.update({
    "Audio/Daily standup – returns pilot (Oct 14).m4a": "2026-10-14 09:31",
    "Audio/Retrospectiva – sprint 14.m4a": "2026-10-14 17:48",
    "Audio/Voicemail – Tom Becker, Fabrikam Logistics.m4a": "2026-10-13 15:12",
    "Audio/Nota de voz – cena del offsite en Lisboa.m4a": "2026-10-13 19:22",
    "Audio/Keynote rehearsal – Data Summit.m4a": "2026-10-12 18:05",
    "Audio/AI in Two Minutes – Ep. 13 – What is RAG.m4a": "2026-09-25 07:30",
    "Audio/AI in Two Minutes – Ep. 14 – How to evaluate an agent.m4a": "2026-10-02 07:30",
    "Audio/AI in Two Minutes – Ep. 15 – What is MCP.m4a": "2026-10-09 07:30",
    "Audio/Datos con café – Ep. 7 – Lakehouse o warehouse.m4a": "2026-09-24 08:00",
    "Audio/Datos con café – Ep. 8 – Direct Lake.m4a": "2026-10-01 08:00",
    "Audio/Datos con café – Ep. 9 – Mirroring.m4a": "2026-10-08 08:00",
    "Audio/Voicemail – IT service desk.m4a": "2026-10-12 16:47",
    "Audio/Call – Northwind Traders, Trailhead 3 order.m4a": "2026-10-13 12:10",
    "Audio/Interview – Ana, support team.m4a": "2026-10-09 12:30",
    "Audio/Voice memo – Trailhead 3 launch page.m4a": "2026-10-07 08:52",
    "Audio/Nota de voz – ideas para el taller.m4a": "2026-10-12 21:03",
    "Audio/Phishing simulation – September results.m4a": "2026-10-05 10:02",
    "Audio/Resumen semanal – piloto de agentes (15 oct).m4a": "2026-10-15 18:05",
    "Audio/Voice memo – expenses, lunch with Fabrikam.m4a": "2026-10-13 14:40",
    "Audio/Llamada – Fourth Coffee, catering del Data Summit.m4a": "2026-10-15 11:30",
    "Video/Q3 town hall – highlights.mp4": "2026-10-08 18:30",
    "Video/Sprint review – returns assistant v0.4.mp4": "2026-10-14 16:45",
    "Video/Microsoft Fabric in 90 seconds.mp4": "2026-09-30 10:12",
    "Video/GitHub Copilot – 5 tips.mp4": "2026-10-01 13:20",
    "Video/RAG en 1 minuto.mp4": "2026-09-28 12:00",
    "Video/Evaluaciones de agentes en 45 segundos.mp4": "2026-10-05 12:00",
    "Video/Bienvenida a Contoso – onboarding.mp4": "2026-09-22 09:00",
    "Video/Trailhead 3 – teaser.mp4": "2026-10-12 11:00",
    "Video/Phishing – 3 señales para detectarlo.mp4": "2026-10-05 09:30",
    "Video/Trailhead 3 – setup guide.mp4": "2026-10-15 15:00",
    "Video/Offsite Lisboa – información práctica.mp4": "2026-10-15 13:40",
    "Video/Data Summit Madrid – save the date.mp4": "2026-10-02 10:00",
})


def phone(path: Path) -> None:
    """A call or a voicemail sounds like one: only the telephone band, 300 to 3,400 Hz."""
    narrow = WORK / f"phone-{path.stem[:24]}.m4a"
    run(FFMPEG, "-v", "error", "-y", "-i", path, "-af", "highpass=f=300,lowpass=f=3400,loudnorm=I=-18:TP=-2",
        "-map_metadata", "-1", "-c:a", "aac", "-b:a", "48k", "-movflags", "+faststart", narrow)
    narrow.replace(path)


def theme(bg: str, ink: str, accent: str, soft: str, muted: str, glow: str,
          title: str = "700 56px/1.06 system-ui", extra: str = "") -> str:
    """A narrated video's look. Colors are #rrggbb, so that the chips can take the accent with some transparency."""
    return EXPLAINER_CSS + f"""body{{background:{bg};color:{ink}}}
.glow{{position:absolute;inset:0;background:{glow}}}
.text{{left:96px;width:640px}}.kicker{{color:{accent}}}
h1{{font:{title};letter-spacing:-.02em;color:{ink}}}.cover h1{{font-size:74px}}
p{{color:{soft};max-width:610px}}
.chip{{border:1px solid {accent}5c;background:{accent}17;color:{ink}}}
.big{{position:absolute;right:96px;top:50%;width:440px;transform:translateY(-50%);text-align:right}}
.big b{{display:block;font-family:system-ui;font-weight:200;line-height:1;letter-spacing:-.04em;color:{accent}}}
.big span{{display:block;margin-top:22px;font:500 21px/1.3 system-ui;color:{muted}}}
.art{{position:absolute;right:112px;top:50%;width:380px;height:380px;transform:translateY(-50%)}}
.foot{{left:96px;right:96px;color:{muted}}}{extra}"""


def show(slides: list[tuple], css: str, foot: str, path: Path, art: str = "") -> None:
    """A narrated video with a voice for every slide: (kicker, title, line, chips, big, speaker, narration). `big` is
    a figure and its caption, drawn large beside the words; slides without one get `art` there instead."""
    voices = [say(slide[-1], voice(*slide[-2])) for slide in slides]
    images = []
    for index, (kicker, title, line, chips, big, _, _) in enumerate(slides):
        if big:
            figure, caption = big
            size = min(150, int(430 / (0.56 * len(figure))))
            side = f'<div class="big"><b style="font-size:{size}px">{esc(figure)}</b><span>{esc(caption)}</span></div>'
        else:
            side = art
        tags = "".join(f'<span class="chip">{esc(chip)}</span>' for chip in chips)
        body = (f'<div class="glow"></div>{side}<div class="text{" cover" if index == 0 else ""}">'
                f'<div class="kicker">{esc(kicker)}</div><h1>{esc(title)}</h1>'
                f'{f"<p>{esc(line)}</p>" if line else ""}{f"<div class=chips>{tags}</div>" if tags else ""}</div>'
                f'<div class="foot"><span>{esc(foot)}</span><span>{index + 1:02d} / {len(slides):02d}</span></div>')
        images.append(render(page(body, css), (1280, 720), 1.5))
    slideshow(list(zip(images, voices, strict=True)), path, fade=0.5, pad=0.8)


def recolor(text: str, pairs: dict[str, str]) -> str:
    for old, new in pairs.items():
        text = text.replace(old, new)
    return text


# The Foundry explainer's look and dial, in other colors, for the two Spanish explainers against the clock.
TEAL = {"#0a0e24": "#03201b", "#eef2ff": "#ecfdf5", "99,102,241": "16,185,129", "56,189,248": "45,212,191",
        "#a5b4fc": "#6ee7b7", "#c7d2fe": "#a7f3d0", "165,180,252": "110,231,183", "#e0e7ff": "#d1fae5",
        "#6870a6": "#4b8f7c", "#818cf8": "#34d399"}
AMBER = {"#0a0e24": "#1a1206", "#eef2ff": "#fffbeb", "99,102,241": "245,158,11", "56,189,248": "251,113,133",
         "#a5b4fc": "#fcd34d", "#c7d2fe": "#fde68a", "165,180,252": "252,211,77", "#e0e7ff": "#fef3c7",
         "#6870a6": "#a08a5a", "#818cf8": "#fbbf24"}


# MARK: Audio


@builder
def more_audio():
    """Audio/: meetings, calls, voicemails, voice notes and two podcasts, in English and Spanish."""
    team = {"L": SAMANTHA, "J": DANIEL, "A": KAREN, "S": MOIRA, "M": RISHI}
    conversation([
        ("L", "Morning, everyone. Quick standup today, because the Foundry workshop starts at ten in Sala Ártico. "
              "Javier, you start."),
        ("J", "Yesterday I re-ran the clean returns notebook. The order history shortcut works now, so orders older "
              "than a year show up. Today I'm building the CSAT by week notebook for Thursday's report."),
        ("A", "On the support side: two hundred and twelve conversations yesterday, and only twelve of them were "
              "escalated to a person. Two customers asked about pickup slots, which the assistant can't book yet."),
        ("S", "Yesterday, just after eleven, we hit the model's rate limit: a run of 429 errors for about twenty "
              "minutes. I added a retry with exponential backoff, in retry dot py, published version nine and "
              "re-ran the evaluations. Groundedness is four point one now, above our bar of four."),
        ("L", "Great news. Any blockers?"),
        ("M", "One from me. The old staging key is still in a pipeline variable. I'll rotate it on Thursday, and then "
              "we move the web app to managed identity, as the decision record says. No more keys."),
        ("L", "Perfect. Ana, keep a list of the pickup slot questions for the sprint review. See you all at ten."),
    ], team, out("Audio/Daily standup – returns pilot (Oct 14).m4a"))

    conversation([
        ("L", "Retrospectiva del sprint catorce. Empezamos por lo que ha ido bien."),
        ("S", "El índice nuevo de políticas. Desde que lo reconstruimos, la fundamentación ya está por encima del "
              "objetivo: cuatro coma uno sobre cinco."),
        ("A", "Y en soporte se nota: ya casi nadie se queja de respuestas con la política antigua."),
        ("L", "¿Y qué ha ido mal?"),
        ("J", "El martes tuvimos dos caídas porque el modelo llegó al límite de su cuota. Errores cuatrocientos "
              "veintinueve durante unos veinte minutos. Y nos dimos cuenta por las quejas de los clientes, no por "
              "una alerta."),
        ("L", "Eso no puede volver a pasar. ¿Acciones?"),
        ("S", "Dos alertas. La primera, si el asistente tarda más de ocho segundos en responder. La segunda, si hay "
              "más de diez errores en cinco minutos. Las preparo yo para el viernes."),
        ("J", "Y también hay que pedir más cuota para el modelo, antes de ampliar el piloto al equipo comercial."),
        ("A", "Una idea más: que el asistente pase la conversación a una persona antes, cuando el cliente está "
              "enfadado. Hoy tarda demasiado."),
        ("L", "Apuntado para el próximo sprint. Gracias a todos."),
    ], {"L": MONICA, "S": EDDY_ES, "A": PAULINA, "J": REED_ES}, out("Audio/Retrospectiva – sprint 14.m4a"))

    voicemail = out("Audio/Voicemail – Tom Becker, Fabrikam Logistics.m4a")
    conversation([("T", "Hi Lucía, it's Tom Becker from Fabrikam Logistics, Tuesday, around three. Thanks again for "
                        "lunch. I'm afraid I have bad news about purchase order 5518, the tent poles for the "
                        "Trailhead 3. The container missed its vessel in Rotterdam, so the delivery to your "
                        "Zaragoza warehouse moves from today to next Tuesday, October twentieth. Everything else in "
                        "the order is on schedule. I'll email you the new tracking number tomorrow. If you need me, "
                        "call me on four two five, five five five, zero one four two. Sorry about this. Talk soon.")],
                 {"T": DANIEL}, voicemail)
    phone(voicemail)

    conversation([("L", "Nota para la cena del equipo en Lisboa. Es el jueves veintidós, a las ocho treinta de la "
                        "noche, en un restaurante del barrio de Alfama, al lado del mirador. Hemos reservado para "
                        "catorce personas. Hay tres personas vegetarianas y una celíaca, así que hay "
                        "que avisar al restaurante. Que todo el mundo confirme si viene antes del martes a las doce "
                        "del mediodía. El restaurante está a diez minutos andando del hotel, pero la cuesta es "
                        "fuerte: calzado cómodo.")],
                 {"L": MONICA}, out("Audio/Nota de voz – cena del offsite en Lisboa.m4a"))

    conversation([
        ("L", "Good morning, Madrid! Six months ago, every return at Contoso Outdoor was handled by hand: emails, "
              "phone calls, spreadsheets. It took eleven minutes, on average. Today, an AI agent resolves sixty-two "
              "percent of return requests on its own, in four minutes."),
        ("C", "Stop there. Good start. Two notes: slow down on the numbers, and pause after sixty-two percent. Let "
              "it land."),
        ("L", "Okay. How did we do it? Three things. One copy of the data, in OneLake: orders and returns, no "
              "exports. An agent on Microsoft Foundry, with tools to look up orders and open returns. And "
              "evaluations before every release."),
        ("C", "Better. But you're at fourteen minutes, and the slot is twelve. Cut the architecture slide, keep the "
              "live demo, and end with the Trailhead 3 story. People remember stories."),
        ("L", "Cut the architecture, keep the demo, end with the tent. Got it. Same time tomorrow?"),
        ("C", "Tomorrow at nine. And bring the clicker."),
    ], {"L": SAMANTHA, "C": TESSA}, out("Audio/Keynote rehearsal – Data Summit.m4a"))

    more_podcasts()
    more_calls()


def more_podcasts() -> None:
    hosts = {"S": SAMANTHA, "D": DANIEL}
    conversation([
        ("S", "Welcome back to AI in Two Minutes. I'm Sam."),
        ("D", "And I'm Daniel. Today: RAG, retrieval augmented generation. It sounds scary."),
        ("S", "It isn't. A language model only knows what it saw in training. RAG lets it look things up first. "
              "Before answering, the app searches your own documents, finds the most relevant passages, and puts "
              "them in the prompt."),
        ("D", "So the model answers with your documents open in front of it."),
        ("S", "Exactly, like an open-book exam. Ask about the return policy, and it reads the current policy instead "
              "of guessing."),
        ("D", "And how does it find the right passages?"),
        ("S", "Usually with embeddings. Every chunk of text becomes a vector, a list of numbers that captures its "
              "meaning. Your question becomes a vector too, and you take the chunks closest to it. Many apps "
              "combine that with keyword search. That's called hybrid search."),
        ("D", "Why do people love it?"),
        ("S", "Three reasons. The answers are grounded in your data, they can cite their sources, and when a "
              "document changes, you update the index, not the model."),
        ("D", "Look it up, then answer. That's our two minutes!"),
    ], hosts, out("Audio/AI in Two Minutes – Ep. 13 – What is RAG.m4a"))

    conversation([
        ("D", "This is AI in Two Minutes. I'm Daniel."),
        ("S", "And I'm Sam. Today: how do you know your agent is any good?"),
        ("D", "You test it, like any software. Start with a golden set: fifty or a hundred real questions, each with "
              "what a good answer looks like."),
        ("S", "And then?"),
        ("D", "Run the agent on all of them and score every answer. Groundedness: is it supported by the documents? "
              "Relevance: does it answer the question? Tool call accuracy: did it call the right tool, with the "
              "right arguments? And safety."),
        ("S", "Who does the scoring?"),
        ("D", "Mostly another model, an AI judge, with a clear rubric, say from one to five. Plus a few people "
              "checking a sample, to make sure the judge agrees with humans."),
        ("S", "When do you run it?"),
        ("D", "Before every release, as a gate. If groundedness drops below your bar, say four out of five, that "
              "version doesn't ship. And after launch, on a sample of real conversations."),
        ("S", "Golden set, metrics, a gate. Thanks for listening!"),
    ], hosts, out("Audio/AI in Two Minutes – Ep. 14 – How to evaluate an agent.m4a"))

    conversation([
        ("S", "AI in Two Minutes, episode fifteen. I'm Sam."),
        ("D", "I'm Daniel. Today, the three letters everyone is talking about: MCP."),
        ("S", "The Model Context Protocol. It's an open standard for connecting AI apps to tools and data. Think of "
              "it as a USB-C port for AI."),
        ("D", "Meaning?"),
        ("S", "Before MCP, every app wrote its own connector for every tool. With MCP, you write a server once, say "
              "for your order system, and any app that speaks MCP can use it: an agent, a code editor, a chat "
              "assistant."),
        ("D", "What does a server offer?"),
        ("S", "Tools the model can call, resources it can read, and prompts. The app asks the server what it has, "
              "and the model decides when to use it."),
        ("D", "Any risks?"),
        ("S", "Treat a server like any third-party code. Only install the ones you trust, give them the least "
              "access they need, and ask the user before anything with side effects, like refunding an order."),
        ("D", "One protocol, many tools. See you next week!"),
    ], hosts, out("Audio/AI in Two Minutes – Ep. 15 – What is MCP.m4a"))

    hosts = {"M": MONICA, "P": PAULINA}
    conversation([
        ("M", "Bienvenidos a Datos con café. Soy Mónica."),
        ("P", "Y yo soy Paulina. Hoy, la pregunta del millón en Microsoft Fabric: ¿lakehouse o almacén de datos?"),
        ("M", "Los dos guardan sus tablas en OneLake, en formato abierto. La diferencia es cómo trabajas con ellas."),
        ("P", "El lakehouse es para quien trabaja con Spark y cuadernos: tablas, pero también archivos y datos sin "
              "estructura."),
        ("M", "Y el almacén de datos es para quien vive en SQL: tablas, transacciones y procedimientos almacenados."),
        ("P", "¿Y si en mi empresa hay un equipo de cada tipo?"),
        ("M", "Pues usas los dos. El lakehouse tiene un punto de conexión SQL de solo lectura, y desde el almacén "
              "puedes consultar las tablas del lakehouse sin copiarlas."),
        ("P", "Resumen: Spark y archivos, lakehouse. SQL y transacciones, almacén de datos. Y todo con una sola "
              "copia de los datos."),
        ("M", "¡Hasta la semana que viene!"),
    ], hosts, out("Audio/Datos con café – Ep. 7 – Lakehouse o warehouse.m4a"))

    conversation([
        ("P", "Datos con café, episodio ocho. Hoy hablamos de Direct Lake."),
        ("M", "Es un modo de los modelos semánticos de Power BI en Fabric. Hasta ahora había dos opciones: importar "
              "los datos, que es rápido pero duplica los datos y hay que actualizarlos, o consultarlos en directo, "
              "que siempre está al día pero es más lento."),
        ("P", "¿Y Direct Lake?"),
        ("M", "Lee las tablas directamente de OneLake y las carga en memoria cuando hacen falta. Casi tan rápido como "
              "importar, sin copiar los datos y sin esperar a una actualización programada."),
        ("P", "O sea, que el informe de devoluciones está al día en cuanto el cuaderno escribe las tablas."),
        ("M", "Eso es. Ojo con una cosa: si una consulta no se puede resolver así, puede pasar a consulta directa, y "
              "va más lenta. Conviene vigilarlo."),
        ("P", "Apuntado. ¡Hasta la próxima!"),
    ], hosts, out("Audio/Datos con café – Ep. 8 – Direct Lake.m4a"))

    conversation([
        ("M", "Datos con café, episodio nueve: la replicación de bases de datos en Fabric, lo que en inglés llaman "
              "mirroring."),
        ("P", "¿Qué problema resuelve?"),
        ("M", "Tienes una base de datos operativa, por ejemplo Azure SQL, Cosmos DB o Snowflake, y quieres analizarla "
              "sin montar un proceso de extracción y carga."),
        ("P", "¿Y cómo funciona?"),
        ("M", "Fabric replica los datos en OneLake casi en tiempo real. Configuras la conexión, eliges las tablas y "
              "listo."),
        ("P", "¿Y cuánto cuesta?"),
        ("M", "El cómputo de la replicación no se cobra, y hay almacenamiento gratuito según la capacidad que "
              "tengas. Pagas cuando consultas esos datos."),
        ("P", "Datos al día y sin procesos de carga. ¡Nos vemos la semana que viene!"),
    ], hosts, out("Audio/Datos con café – Ep. 9 – Mirroring.m4a"))


def more_calls() -> None:
    # She stops for breath around the code, so the transcript has it on a line of its own: what a search lands on.
    voicemail = out("Audio/Voicemail – IT service desk.m4a")
    conversation([("I", "Hi Lucía, this is Megan from the IT service desk, about your ticket for a new laptop. Good "
                        "news: it's ready. We left it in locker fourteen, on the third floor, next to the "
                        "kitchen.", 1.5),
                  ("I", "The code for the locker is four, four, seven, one.", 1.6),
                  ("I", "Once you've moved your files, please bring the old laptop back to the IT desk before Friday. "
                        "Thanks, and have a nice afternoon.")],
                 {"I": TESSA}, voicemail)
    phone(voicemail)

    call = out("Audio/Call – Northwind Traders, Trailhead 3 order.m4a")
    conversation([
        ("E", "Good morning, sales team, this is Emma."),
        ("R", "Hi Emma, it's Raj, from Northwind Traders. We'd like to order the new tent, the Trailhead 3, for our "
              "spring catalog."),
        ("E", "Great. How many units?"),
        ("R", "Three hundred. Delivered to our warehouse in France, in the first week of March."),
        ("E", "No problem. The list price is two hundred and forty-nine euros a unit, and over two hundred and fifty "
              "units there's a twelve percent discount. So your three hundred qualify."),
        ("R", "Twelve percent, perfect. Can we split it into two deliveries?"),
        ("E", "Sure. One hundred and fifty in the first week of March, and one hundred and fifty in the first week "
              "of April, with the same discount."),
        ("R", "Great. Send me the quote, and I'll get the purchase order signed this week."),
        ("E", "I'll send it today. Thanks, Raj."),
    ], {"E": MOIRA, "R": AMAN}, call)

    conversation([
        ("C", "This is Marta, from internal comms. I'm with Ana, from the support team, who has used the returns "
              "assistant for six weeks. Ana, what has changed?"),
        ("A", "Honestly? The boring part of my job is gone. A return used to take eleven minutes of back and forth: "
              "find the order, check the policy, fill in the form. Now it takes four, and most of the time the "
              "assistant does it on its own."),
        ("C", "So what do you do now?"),
        ("A", "The tricky cases. A tent that broke on a mountain, a customer who's really upset. I have time to call "
              "them back."),
        ("C", "Any favorite moment?"),
        ("A", "Last week a customer opened a return at two in the morning, and then wrote: thank you, you're faster "
              "than my bank. He was thanking the bot!"),
        ("C", "And what would you improve?"),
        ("A", "Two things. Let customers book a pickup slot for the courier. And hand the conversation to a person "
              "earlier when someone is angry."),
    ], {"C": TESSA, "A": KAREN}, out("Audio/Interview – Ana, support team.m4a"))

    conversation([("C", "Memo for the Trailhead 3 launch page. Lead with the weight: nineteen hundred grams, three "
                        "hundred grams lighter than the previous model. It sleeps three, and it goes up in three "
                        "minutes with color-coded poles and clips. The price is two hundred and forty-nine euros, and "
                        "it launches on November third, in two colors: forest green and sand. The fly is made from "
                        "recycled polyester, so mention that too.", 1.6),
                  ("C", "And no claims about being the lightest tent on the market. The legal team said no.")],
                 {"C": TESSA}, out("Audio/Voice memo – Trailhead 3 launch page.m4a"))

    conversation([("A", "Ideas para el taller del miércoles. Uno: la sala Ártico tiene wifi de invitados, pero la "
                        "contraseña hay que pedirla en recepción, así que la pido el martes. Dos: llevar adaptadores "
                        "de vídeo para los portátiles, que siempre falta alguno. Tres: que cada persona venga con su "
                        "portátil y con acceso a la suscripción de pruebas. Cuatro: empezar con la demo del asistente "
                        "de devoluciones, y terminar con un ejercicio de evaluaciones. El café es a las once y cuarto, "
                        "y acabamos a la una.")],
                 {"A": PAULINA}, out("Audio/Nota de voz – ideas para el taller.m4a"))

    conversation([("M", "Hi everyone, Marc from security, with the results of our September phishing simulation. We "
                        "sent a fake parcel delivery email to every employee. Eighteen percent clicked the link. "
                        "That's down from thirty-one percent in June, so the training is working. Even better, "
                        "sixty-four percent of you reported the email with the Report button. Remember the three "
                        "signs: an urgent tone, a sender address that doesn't quite match, and a link that asks you "
                        "to sign in. And if you do click, don't panic: report it, and change your password straight "
                        "away. The next simulation is in December. Thanks!")],
                 {"M": RISHI}, out("Audio/Phishing simulation – September results.m4a"))

    conversation([
        ("M", "Resumen de la semana del piloto del asistente de devoluciones."),
        ("R", "Buena semana. El asistente resolvió el sesenta y siete por ciento de las consultas sin pasarlas a una "
              "persona, cinco puntos más que la semana pasada. En total, mil ciento ochenta y seis conversaciones."),
        ("M", "¿Y la satisfacción?"),
        ("R", "Cuatro coma seis sobre cinco. Y el tiempo medio de resolución, tres minutos y medio."),
        ("M", "¿Y la calidad de las respuestas?"),
        ("R", "La fundamentación está en cuatro coma uno, desde que reconstruimos el índice de políticas. El único "
              "problema fue el martes: errores por el límite de peticiones del modelo. Ya está resuelto con "
              "reintentos."),
        ("M", "Perfecto. Entonces está decidido: el dos de noviembre ampliamos el piloto al equipo de ventas."),
        ("R", "De acuerdo. Hablamos la semana que viene."),
    ], {"M": MONICA, "R": PAULINA}, out("Audio/Resumen semanal – piloto de agentes (15 oct).m4a"))

    conversation([("L", "Expense note, before I forget. Lunch with Fabrikam Logistics at La Huerta, today, Tuesday "
                        "the thirteenth. One hundred and twenty-eight euros and fifty cents, for four people: me, "
                        "Pablo from operations, and Tom Becker and Ingrid from Fabrikam. Project code: T H 3 launch. "
                        "The photo of the receipt is on my phone. And for Lisbon: the travel policy says the hotel "
                        "can't go over one hundred and forty euros a night, so book before prices go up.")],
                 {"L": SAMANTHA}, out("Audio/Voice memo – expenses, lunch with Fabrikam.m4a"))

    call = out("Audio/Llamada – Fourth Coffee, catering del Data Summit.m4a")
    conversation([
        ("V", "Catering para eventos, le atiende Valeria."),
        ("C", "Hola, Valeria. Soy Carmen, de Contoso. Te llamo por el evento Data Summit, el doce de noviembre en "
              "Madrid."),
        ("V", "¡Hola, Carmen! Dime, ¿cuántas personas sois al final?"),
        ("C", "Novecientas inscritas. De ellas, cuarenta personas son celíacas, y unas sesenta, vegetarianas."),
        ("V", "Perfecto. ¿Mantenemos los horarios?"),
        ("C", "Sí: café a las diez y media y a las cuatro de la tarde, y la comida, de pie, a las dos."),
        ("V", "Para novecientas personas, te recomiendo seis puntos de café, para que no se formen colas."),
        ("C", "De acuerdo, seis puntos. ¿Me mandas el presupuesto actualizado antes del viernes?"),
        ("V", "Claro, te lo envío el jueves. ¡Gracias, Carmen!"),
    ], {"V": PAULINA, "C": MONICA}, call)
    phone(call)


# MARK: Videos
# Shapes beside the words, on the slides without a big figure: drawn here, never anybody's logo.


def audience(color: str) -> str:
    """A town hall seen from above: a stage, and rows of seats around it."""
    seats = []
    for row in range(5):
        radius, count = 92 + row * 46, 9 + row * 3
        for i in range(count):
            angle = math.pi * (0.12 + 0.76 * (i + 0.5) / count)
            x, y = 190 + radius * math.cos(angle), 70 + radius * math.sin(angle)
            seats.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{color}" opacity="{0.95 - row * 0.15:.2f}"/>')
    return (f'<svg class="art" viewBox="0 0 380 380"><rect x="120" y="40" width="140" height="22" rx="11" '
            f'fill="none" stroke="{color}" stroke-width="3"/>{"".join(seats)}</svg>')


def burndown(color: str, grid: str) -> str:
    left = [60, 70, 108, 118, 166, 186, 230, 248, 300, 322, 350]
    points = " ".join(f"{30 + 33 * i},{y}" for i, y in enumerate(left))
    dots = "".join(f'<circle cx="{30 + 33 * i}" cy="{y}" r="6" fill="{color}"/>' for i, y in enumerate(left))
    return (f'<svg class="art" viewBox="0 0 380 380" fill="none"><path d="M30 24 V350 H364" stroke="{grid}" '
            f'stroke-width="3"/><path d="M30 60 L360 350" stroke="{grid}" stroke-width="2" stroke-dasharray="6 9"/>'
            f'<polyline points="{points}" stroke="{color}" stroke-width="5" stroke-linejoin="round"/>{dots}</svg>')


def weave(color: str) -> str:
    """Strips over and under each other, like a woven cloth."""
    strips = [f'<rect x="16" y="{34 + i * 54}" width="348" height="30" rx="15" fill="{color}" '
              f'opacity="{0.22 + 0.12 * (i % 3):.2f}"/>' for i in range(6)]
    strips += [f'<rect x="{34 + i * 54}" y="16" width="30" height="348" rx="15" fill="{color}" '
               f'opacity="{0.16 + 0.12 * ((i + 1) % 3):.2f}"/>' for i in range(6)]
    return f'<svg class="art" viewBox="0 0 380 380">{"".join(strips)}</svg>'


def braces(color: str) -> str:
    return (f'<div class="art" style="display:flex;align-items:center;justify-content:center;color:{color};'
            f'font:200 190px/1 \'SF Mono\',Menlo,monospace;letter-spacing:-.06em">{{ }}</div>')


def badge(color: str, paper: str) -> str:
    return (f'<svg class="art" viewBox="0 0 380 380" fill="none" stroke="{color}" stroke-width="5" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="M146 12 L190 112 L234 12"/>'
            f'<rect x="100" y="112" width="180" height="246" rx="20"/><rect x="160" y="98" width="60" height="30" '
            f'rx="9" fill="{paper}"/><circle cx="190" cy="204" r="40"/><path d="M140 290 H240 M162 320 H218"/></svg>')


def tent(color: str) -> str:
    return (f'<svg class="art" viewBox="0 0 380 380" fill="none" stroke="{color}" stroke-linecap="round" '
            f'stroke-linejoin="round"><path d="M44 300 L190 74 L336 300 Z" stroke-width="5"/>'
            f'<path d="M190 74 L190 300" stroke-width="2" opacity=".45"/><path d="M150 300 Q190 196 230 300" '
            f'stroke-width="4"/><path d="M16 300 H364" stroke-width="3" opacity=".45"/>'
            f'<path d="M190 74 L172 40 M190 74 L208 40" stroke-width="4"/><circle cx="302" cy="92" r="20" '
            f'stroke-width="3" opacity=".7"/></svg>')


def hook(color: str) -> str:
    return (f'<svg class="art" viewBox="0 0 380 380" fill="none" stroke="{color}" stroke-width="6" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="M190 8 V112 A30 30 0 0 1 130 112 V92 l16 14"/>'
            f'<rect x="40" y="176" width="300" height="180" rx="16"/><path d="M42 190 L190 284 L338 190"/></svg>')


def tiles(blue: str, yellow: str) -> str:
    """Azulejos: a diamond and a sun on every tile, and a circle where four tiles meet."""
    cells = "".join(f'<g transform="translate({c * 95} {r * 95})"><rect width="95" height="95" fill="#fff" '
                    f'stroke="#c7d2fe"/><path d="M47.5 10 L85 47.5 L47.5 85 L10 47.5 Z" fill="none" '
                    f'stroke="{blue}" stroke-width="5"/><circle cx="47.5" cy="47.5" r="13" fill="{yellow}"/></g>'
                    for r in range(4) for c in range(4))
    joints = "".join(f'<circle cx="{c * 95}" cy="{r * 95}" r="19" fill="{blue}"/>' for r in range(5) for c in range(5))
    return f'<svg class="art" viewBox="0 0 380 380">{cells}{joints}</svg>'


def halftone(color: str) -> str:
    dots = []
    for row in range(10):
        for col in range(10):
            radius = 16 - math.hypot(col - 6.5, row - 3) * 2.2
            if radius > 1.2:
                dots.append(f'<circle cx="{19 + col * 38}" cy="{19 + row * 38}" r="{radius:.1f}" fill="{color}"/>')
    return f'<svg class="art" viewBox="0 0 380 380">{"".join(dots)}</svg>'


TOWN_HALL = [
    ("Contoso · Q3 2026 town hall", "Q3 town hall: the highlights", "Thursday, October 8.", [], None, MOIRA,
     "Hi everyone. In case you missed today's town hall, here are the highlights, in under two minutes."),
    ("Results", "Our best third quarter yet.", "Led by online sales. And fewer returns.",
     ["Online +22 %", "Stores +6 %", "Returns −9 %"], ("+14 %", "revenue vs Q3 2025"), DANIEL,
     "Revenue grew fourteen percent on the third quarter of last year. Online sales were up twenty-two percent, "
     "stores six percent, and returns went down by nine percent."),
    ("Customers", "An AI agent now resolves most returns.", "The pilot started in September, with the support team.",
     ["11 → 4 minutes", "CSAT 4.5 / 5"], ("62 %", "of return requests, resolved by the agent"), SAMANTHA,
     "The returns assistant pilot is going really well. The agent resolves sixty-two percent of return requests on "
     "its own, and a return takes four minutes instead of eleven. If the numbers hold, the sales team is next."),
    ("People", "1,500 € a year for your training.", "From January 2027, for everyone: courses, books, conferences, "
     "certifications.", ["No approval under 500 €"], ("1,500 €", "per person, per year, from 2027"), KAREN,
     "And now, the question you asked the most. From January, every employee has a training budget of fifteen "
     "hundred euros a year, for courses, books, conferences or certifications. Anything under five hundred euros "
     "doesn't need approval: just book it, and expense it."),
    ("Products", "Trailhead 3 launches on November 3.", "Our lightest tent ever. Sleeps three.",
     ["Forest green", "Sand"], ("1.9 kg", "300 g lighter than Trailhead 2"), MOIRA,
     "On November third we launch Trailhead 3, our lightest tent ever: one point nine kilos, for two hundred and "
     "forty-nine euros."),
    ("Growing", "Lisbon opens in March 2027.", "Our second office: product and engineering.", [],
     ("40", "people in Lisbon by the end of 2027"), MOIRA,
     "And in March, we open our second office, in Lisbon, with forty people by the end of next year, mostly product "
     "and engineering."),
    ("Next", "Next town hall: January 14.", "Send your questions any time, with the town hall form.", [], None, MOIRA,
     "That's all. Thank you for an amazing quarter. The next town hall is on January fourteenth."),
]
SPRINT_REVIEW = [
    ("Sprint 14 review · October 14", "Returns assistant v0.4", "What we shipped in the last two weeks.", [], None,
     SAMANTHA, "Welcome to the sprint fourteen review of the returns assistant. Version zero point four is live. "
     "Here's what's in it."),
    ("Faster", "Answers in 6.2 seconds, not 9.8.", "We cache the policy lookups and stream the replies.", [],
     ("6.2 s", "p95 latency, down from 9.8 s"), MOIRA,
     "First, speed. Ninety-five percent of answers now arrive within six point two seconds, down from nine point "
     "eight. We cache the policy lookups, and we stream the replies."),
    ("Sturdier", "Rate limits don't break the chat anymore.", "Retry with exponential backoff and jitter.",
     ["retry.py", "429 Too Many Requests", "Retry-After"], ("5×", "attempts, with backoff and jitter"), MOIRA,
     "Second, after yesterday's outage. When the model answers with a four two nine error, too many requests, the "
     "assistant now waits and tries again, with exponential backoff and jitter, up to five times. Customers just "
     "get a slightly slower answer."),
    ("Tools", "Orders behind an MCP server.", "One server for the order system, for every app that needs it.",
     ["lookup_order", "create_return", "book_pickup"], None, DANIEL,
     "Third, the order tools are now an MCP server as well: look up an order, open a return, book a pickup. When "
     "the sales team joins, their agent will use the same server."),
    ("New", "Book a courier pickup in the chat.", "No labels to print, no queues at the post office.",
     ["Monday to Saturday", "8:00 to 20:00"], ("2 h", "pickup slots, Monday to Saturday"), KAREN,
     "And the feature customers asked for the most: they can book a courier pickup right in the chat, in two-hour "
     "slots, Monday to Saturday. No labels to print, no queues at the post office."),
    ("Quality", "Version 9 passes the bar.", "Evaluated on 120 golden questions before the release.",
     ["Relevance 4.4", "Tool calls 96 %"], ("4.1", "groundedness; the bar is 4"), MOIRA,
     "Quality: we evaluated version nine on our hundred and twenty golden questions. Groundedness is four point "
     "one, above our bar of four, and relevance is four point four."),
    ("Next sprint", "Alerts, quota, and the sales team.", "If the numbers hold, sales joins on November 2.",
     ["Latency alert", "429 alert", "More model quota"], None, SAMANTHA,
     "Next sprint: alerts for latency and rate limits, and more model quota. If the numbers hold, the sales team "
     "joins the pilot on November second. Thank you, everyone!"),
]
FABRIC_VIDEO = [
    ("Explainer", "Microsoft Fabric in 90 seconds", "", [], None, DANIEL, "Microsoft Fabric, in ninety seconds."),
    ("What it is", "All your analytics, in one platform.", "Software as a service: nothing to install or wire up.",
     [], None, DANIEL,
     "Microsoft Fabric is an analytics platform, delivered as software as a service. Data integration, engineering, "
     "data science, real-time analytics and business intelligence, all in one place."),
    ("OneLake", "One copy of the data, for every engine.", "Open Delta Parquet tables: a OneDrive for data.",
     ["Lakehouse", "Warehouse", "Power BI"], None, DANIEL,
     "Everything lands in OneLake, one data lake for the whole organization, in the open Delta Parquet format. "
     "Every engine reads the same copy."),
    ("Workloads", "The right tool for every job.", "",
     ["Data Factory", "Data Engineering", "Data Warehouse", "Data Science", "Real-Time Intelligence", "Databases",
      "Power BI"], None, DANIEL,
     "Pick the right tool for the job: Data Factory pipelines, Spark notebooks, a SQL warehouse, data science, "
     "real-time intelligence, operational databases, and Power BI."),
    ("No more copies", "Use data where it already lives.", "Shortcuts point to it; mirroring replicates it.",
     ["Shortcuts", "Mirroring"], None, DANIEL,
     "Shortcuts let you use data in Azure, Amazon S3 or Google Cloud without copying it, and mirroring replicates "
     "your operational databases into OneLake, in near real time."),
    ("Copilot", "Ask your data in plain language.", "Copilot writes code, builds reports and answers questions.",
     [], None, DANIEL,
     "Copilot helps in every workload: it writes notebook code and SQL, builds Power BI reports, and answers "
     "questions about your data in plain language."),
    ("Governed", "Secure and governed by default.", "The OneLake catalog and Microsoft Purview, in one place.",
     [], None, DANIEL, "And it's all governed in one place, with the OneLake catalog and Microsoft Purview."),
    ("Try it", "app.fabric.microsoft.com", "Start a free trial.", [], None, DANIEL,
     "Start a free trial today, at app dot fabric dot microsoft dot com."),
]


COPILOT_VIDEO = [
    ("GitHub Copilot", "5 tips to get more out of Copilot", "", [], None, TESSA,
     "Five tips to get more out of GitHub Copilot."),
    ("Tip 1", "Let agent mode do the busywork.", "It edits files, runs commands and fixes its own errors.",
     ["VS Code", "Visual Studio", "JetBrains"], ("01", "agent mode"), TESSA,
     "Tip one: use agent mode for tasks with many steps. Describe the change, and Copilot edits the files, runs "
     "commands in the terminal and fixes its own errors, while you review each step."),
    ("Tip 2", "Teach it your conventions once.", ".github/copilot-instructions.md", ["Style", "Libraries", "Tests"],
     ("02", "custom instructions"), TESSA,
     "Tip two: add a copilot instructions file to your repository. Tell Copilot your coding style, the libraries "
     "you use and how to run the tests, and every chat follows them."),
    ("Tip 3", "Ask Copilot for a code review.", "Add it as a reviewer on any pull request.", [],
     ("03", "code review"), TESSA,
     "Tip three: ask Copilot for a code review. Add it as a reviewer on a pull request, and it leaves comments with "
     "suggested changes you can apply in one click."),
    ("Tip 4", "Assign an issue to Copilot.", "The coding agent works on it in the background, then opens a pull "
     "request.", [], ("04", "coding agent"), TESSA,
     "Tip four: assign an issue to Copilot. The coding agent works on it in the background, and opens a pull "
     "request for you to review."),
    ("Tip 5", "Give it tools, and reusable prompts.", "MCP servers, and prompt files in .github/prompts.",
     ["GitHub MCP server", "Prompt files"], ("05", "MCP and prompt files"), TESSA,
     "Tip five: give Copilot more tools with MCP servers, and save the prompts you repeat as prompt files that the "
     "whole team can reuse."),
    ("That's it", "Happy coding!", "docs.github.com/copilot", [], None, TESSA,
     "That's it. All the details are at docs dot github dot com. Happy coding!"),
]
# explainer() slides: kicker, title, line, chips, narration; one voice, against the clock.
RAG_VIDEO = [
    ("Explicación", "RAG en 1 minuto", "", [], "RAG, en un minuto."),
    ("El problema", "Un modelo solo sabe lo que vio al entrenarse.", "No conoce tus documentos, ni lo que cambió ayer.",
     [], "Un modelo de lenguaje solo sabe lo que vio cuando lo entrenaron. No conoce tus documentos, ni lo que "
         "cambió ayer."),
    ("La idea", "Primero busca. Después responde.", "Generación aumentada por recuperación: RAG.", [],
     "La solución es RAG: generación aumentada por recuperación. Antes de responder, la aplicación busca en tus "
     "documentos."),
    ("Cómo busca", "El significado, convertido en números.", "Cada fragmento de texto, y la pregunta, se convierten "
     "en vectores.", ["Embeddings", "Búsqueda híbrida", "Reordenación"],
     "Cada fragmento de tus documentos se convierte en un vector, una lista de números que representa su "
     "significado. La pregunta también. Y se eligen los fragmentos más parecidos."),
    ("Cómo responde", "Con las fuentes delante.", "Los fragmentos van en el prompt, y la respuesta los cita.", [],
     "Esos fragmentos se añaden al prompt, y el modelo responde con tus documentos delante, citando las fuentes."),
    ("Por qué", "Respuestas fundamentadas, y al día.", "Si cambia un documento, actualizas el índice, no el modelo.",
     ["Menos invenciones", "Con citas", "Siempre al día"],
     "¿La ventaja? Respuestas basadas en tus datos, con citas, y siempre al día: si cambia un documento, actualizas "
     "el índice, no el modelo."),
]
EVALS_VIDEO = [
    ("Explicación", "Evaluar un agente en 45 segundos", "", [],
     "Cómo evaluar un agente, en cuarenta y cinco segundos."),
    ("Paso 1", "Un conjunto de preguntas de referencia.", "Preguntas reales, con la respuesta que esperas.", [],
     "Primero, un conjunto de referencia: cien preguntas reales, cada una con la respuesta que esperas."),
    ("Paso 2", "Puntúa cada respuesta.", "", ["Fundamentación", "Relevancia", "Herramientas", "Seguridad"],
     "Después, ejecutas el agente y puntúas cada respuesta: fundamentación, relevancia, uso de herramientas y "
     "seguridad."),
    ("Paso 3", "Un modelo hace de juez.", "Con una rúbrica del 1 al 5, y personas que revisan una muestra.", [],
     "Normalmente otro modelo hace de juez, con una rúbrica del uno al cinco, y unas personas revisan una muestra."),
    ("Paso 4", "Si no aprueba, no se publica.", "Por ejemplo: fundamentación de 4 o más en cada versión.", [],
     "Y por último, una barrera: si la fundamentación baja de cuatro, esa versión no se publica."),
]
ONBOARDING_VIDEO = [
    ("Contoso · Te damos la bienvenida", "Bienvenida a Contoso", "Tu primera semana, en dos minutos.", [], None,
     MONICA, "¡Hola, y bienvenida a Contoso! En dos minutos, te contamos lo que necesitas para tu primera semana."),
    ("Día 1 · 8:30", "Recoge tu tarjeta en recepción.", "Planta baja, de 8:30 a 10:00. Trae tu DNI o pasaporte.",
     [], ("8:30", "recepción, planta baja"), PAULINA,
     "El primer día, recoge tu tarjeta de acceso en la recepción de la planta baja, entre las ocho y media y las "
     "diez. No olvides tu DNI o tu pasaporte."),
    ("Día 1 · 10:00", "Tu portátil te espera en el puesto de IT.", "Tercera planta, al lado de la cocina.", [],
     ("3.ª", "planta, puesto de IT"), MONICA,
     "Después, sube a la tercera planta. En el puesto de IT, al lado de la cocina, te dan tu portátil y te ayudan a "
     "configurarlo."),
    ("Semana 1", "Curso de seguridad: 30 minutos.", "Antes del viernes, en la plataforma de formación.", [],
     ("30 min", "curso de seguridad, antes del viernes"), PAULINA,
     "Antes del viernes, haz el curso de seguridad. Son treinta minutos, y aprenderás a reconocer correos "
     "fraudulentos."),
    ("Mes 1", "Tendrás un compañero de acogida.", "Alguien de tu equipo, para las dudas del día a día.", [], None,
     MONICA, "Durante el primer mes tendrás un compañero de acogida: alguien de tu equipo para todas esas dudas que "
     "no vienen en ningún manual."),
    ("Comunidad", "Preséntate en el canal #bienvenida.", "En Teams. Y los viernes a las 10, café para recién "
     "llegados.", [], None, PAULINA,
     "Y preséntate en el canal de bienvenida de Teams. Los viernes a las diez hay un café para las personas recién "
     "llegadas."),
    ("Eso es todo", "¡Nos alegra tenerte aquí!", "¿Dudas? personas@contoso.com", [], None, MONICA,
     "Eso es todo. Si tienes dudas, escríbenos. ¡Nos alegra mucho tenerte aquí!"),
]
TEASER_VIDEO = [
    ("Contoso Outdoor · new", "Trailhead 3", "Lighter. Faster. Roomier.", [], None, SAMANTHA,
     "Introducing Trailhead 3."),
    ("Lighter", "Our lightest tent yet.", "300 grams lighter than Trailhead 2.", [], ("1.9 kg", "the whole tent"),
     SAMANTHA, "Our lightest tent yet: one point nine kilos. Three hundred grams lighter than Trailhead 2."),
    ("Faster", "Pitched in three minutes.", "Color-coded poles and clips.", [], ("3 min", "to pitch, on your own"),
     SAMANTHA, "Pitch it in three minutes, on your own, with color-coded poles and clips."),
    ("Roomier", "Sleeps three.", "Two doors, two vestibules: nobody climbs over anybody.", [],
     ("3", "people, two doors"), SAMANTHA, "Room for three, and two doors, so nobody climbs over anybody at night."),
    ("Kinder", "A fly made from recycled polyester.", "", ["Forest green", "Sand"], None, SAMANTHA,
     "And a fly made from recycled polyester, in forest green or sand."),
    ("November 3", "Trailhead 3. 249 €.", "In stores and online from November 3.", [], ("249 €", "from November 3"),
     SAMANTHA, "Trailhead 3. Two hundred and forty-nine euros, from November third."),
]


PHISHING_VIDEO = [
    ("Seguridad · 1 minuto", "Phishing: 3 señales para detectarlo", "", [], None, MONICA,
     "Tres señales para detectar un correo fraudulento, en un minuto."),
    ("Señal 1", "Te mete prisa.", "«Tu cuenta se bloqueará en 24 horas.»", [], ("1", "la urgencia"), MONICA,
     "Una: la urgencia. Si un correo te mete prisa, o amenaza con bloquear tu cuenta, desconfía."),
    ("Señal 2", "El remitente casi coincide.", "contoso-soporte.co no es contoso.com.", [], ("2", "el remitente"),
     MONICA, "Dos: el remitente. Lee la dirección entera: contoso guion soporte punto co no es contoso punto com."),
    ("Señal 3", "Te pide iniciar sesión.", "Un enlace a una página idéntica a la de siempre.", [], ("3", "el enlace"),
     MONICA, "Tres: un enlace que te pide iniciar sesión. Pasa el ratón por encima antes de hacer clic, y nunca "
     "escribas tu contraseña en una página a la que has llegado desde un correo."),
    ("¿Has hecho clic?", "Repórtalo y cambia tu contraseña.", "Con el botón Informar de Outlook. Sin miedo: es lo "
     "correcto.", [], None, MONICA,
     "¿Y si ya has hecho clic? Tranquilidad: repórtalo con el botón Informar de Outlook, y cambia tu contraseña "
     "enseguida."),
]
SETUP_VIDEO = [
    ("Trailhead 3 · setup guide", "How to pitch your Trailhead 3", "Five steps, about three minutes.", [], None,
     KAREN, "How to pitch your Trailhead 3 tent, in five steps."),
    ("Step 1", "Lay out the inner tent.", "Door away from the wind. Stake the four corners.", [],
     ("1", "inner tent"), KAREN, "Step one: lay out the inner tent, with the door facing away from the wind, and "
     "stake the four corners."),
    ("Step 2", "Assemble the poles.", "They're color-coded: green to green, sand to sand.", [], ("2", "poles"),
     KAREN, "Step two: assemble the poles. They're color-coded: the green pole goes in the green corners, and the "
     "sand pole in the sand corners."),
    ("Step 3", "Clip the tent to the poles.", "From the corners up to the top.", [], ("3", "clips"), KAREN,
     "Step three: clip the inner tent to the poles, from the corners up to the top. Now it stands on its own."),
    ("Step 4", "Throw the fly over.", "Match the colored tabs, then buckle the corners.", [], ("4", "fly"), KAREN,
     "Step four: throw the fly over the tent, match its colored tabs to the poles, and buckle it at the corners."),
    ("Step 5", "Tension the guy lines.", "The fly shouldn't touch the inner tent.", [], ("5", "guy lines"), KAREN,
     "Step five: stake out the guy lines and tension them, so the fly doesn't touch the inner tent. That's it."),
    ("If a pole breaks", "There's a repair sleeve in the bag.", "Slide it over the break, tape it, and contact "
     "support.", [], None, KAREN,
     "And if a pole ever breaks on a trip, there's a repair sleeve in the bag. Slide it over the break, tape it, "
     "and contact our support team for a replacement."),
]
OFFSITE_VIDEO = [
    ("Offsite del equipo · 21–23 de octubre", "Lisboa: todo lo práctico", "", [], None, MONICA,
     "Todo lo práctico sobre el viaje del equipo a Lisboa, en un minuto."),
    ("Ida · miércoles 21", "Vuelo a las 8:35 desde Madrid.", "Blue Yonder Airlines · vuelo 471. Llegada a las 8:55, "
     "hora de Lisboa.", [], ("8:35", "salida de Madrid"), MONICA,
     "La ida es el miércoles veintiuno. El vuelo sale de Madrid a las ocho y treinta y cinco de la mañana, y llega a "
     "Lisboa a las ocho y cincuenta y cinco, hora local. Recordad que en Lisboa es una hora menos."),
    ("Hotel", "En la Baixa, con las sesiones en el mismo hotel.", "Máximo 140 € por noche, según la política de "
     "viajes.", [], ("140 €", "máximo por noche"), PAULINA,
     "Dormimos en un hotel de la Baixa, y las sesiones son en el mismo hotel. La política de viajes permite hasta "
     "ciento cuarenta euros por noche."),
    ("Jueves 22", "Sesiones de 9:00 a 17:00.", "Por la mañana, la estrategia de 2027; por la tarde, visita a la "
     "futura oficina.", [], ("9–17 h", "sesiones del jueves"), MONICA,
     "El jueves hay sesiones de nueve a cinco: por la mañana, la estrategia de dos mil veintisiete, y por la tarde "
     "visitamos la futura oficina de Lisboa."),
    ("Cena · jueves 22", "A las 20:30, en Alfama.", "Avisad de alergias e intolerancias antes del martes a las 12:00.",
     ["14 personas", "3 vegetarianos", "1 celíaco"], ("20:30", "cena del equipo, en Alfama"), PAULINA,
     "La cena del equipo es el jueves a las ocho y media de la noche, en Alfama. Somos catorce. Si tienes alguna "
     "alergia, avisa antes del martes a las doce."),
    ("Vuelta · viernes 23", "Vuelo a las 19:40.", "Vuelo 476. Y calzado cómodo: Lisboa es todo cuestas.", [],
     ("19:40", "vuelta, viernes 23"), PAULINA,
     "Y la vuelta, el viernes veintitrés a las siete y cuarenta de la tarde. Un último consejo: calzado cómodo, "
     "porque Lisboa es todo cuestas."),
]
SUMMIT_VIDEO = [
    ("Save the date", "Data Summit Madrid", "Thursday, November 12, 2026.", [], None, DANIEL,
     "Save the date: the Data Summit comes to Madrid on November twelfth."),
    ("Who", "900 people who work with data and AI.", "Engineers, analysts and leaders, for one day.", [],
     ("900", "registered, and counting"), DANIEL,
     "Nine hundred people who work with data and AI have already registered: engineers, analysts and leaders."),
    ("What", "Real stories. Live demos.", "", ["Microsoft Fabric", "Microsoft Foundry", "GitHub Copilot"], None,
     DANIEL, "Expect real customer stories, and live demos of Microsoft Fabric, Microsoft Foundry and GitHub "
     "Copilot."),
    ("Keynote", "How Contoso Outdoor handles returns with an AI agent.", "Twelve minutes, one tent, a live demo.",
     [], None, DANIEL, "The opening keynote: how Contoso Outdoor handles its customers' returns with an AI agent."),
    ("When", "Thursday, November 12.", "Doors open at 8:00. Coffee and lunch included.", [],
     ("Nov 12", "Madrid · doors open at 8:00"), DANIEL,
     "Doors open at eight, the first session starts at nine, and coffee and lunch are on us. See you in Madrid!"),
]

SERIF = '600 58px/1.08 "Iowan Old Style",Charter,Georgia,serif'
AVENIR = '650 56px/1.06 "Avenir Next",system-ui'


def glow(color: str, second: str = "") -> str:
    """A soft light behind the figure; `color` and `second` are "r,g,b,alpha"."""
    light = f"radial-gradient(760px 560px at 80% 50%,rgba({color}),transparent 62%)"
    return light + (f",radial-gradient(640px 420px at 0% 110%,rgba({second}),transparent 60%)" if second else "")


@builder
def more_videos():
    """Video/: ten narrated slideshows and two explainers against the clock, in English and Spanish."""
    show(TOWN_HALL, theme("#160f2e", "#fdf4ff", "#f0abfc", "#e9d5ff", "#9d86b8",
                          glow("240,171,252,.20", "129,140,248,.16")),
         "Contoso · Q3 2026 town hall", out("Video/Q3 town hall – highlights.mp4"), audience("#f0abfc"))
    show(SPRINT_REVIEW, theme("#0f1115", "#f4f4f5", "#a3e635", "#d4d4d8", "#71717a", glow("163,230,53,.12")),
         "Returns assistant · sprint 14 review", out("Video/Sprint review – returns assistant v0.4.mp4"),
         burndown("#a3e635", "#3f3f46"))
    show(FABRIC_VIDEO, theme("#f1f7f5", "#0b3b36", "#0d9488", "#3f6b65", "#6d958f", glow("13,148,136,.10"), AVENIR),
         "Microsoft Fabric · explainer", out("Video/Microsoft Fabric in 90 seconds.mp4"), weave("#0d9488"))
    show(COPILOT_VIDEO, theme("#0d1117", "#f0f6fc", "#a371f7", "#c9d1d9", "#7d8590",
                              glow("163,113,247,.18", "56,139,253,.10"), '600 50px/1.12 "SF Mono",Menlo,monospace',
                              ".cover h1{font-size:62px}"),
         "GitHub Copilot · tips", out("Video/GitHub Copilot – 5 tips.mp4"), braces("#a371f7"))
    explainer(RAG_VIDEO, recolor(FOUNDRY_CSS, TEAL),
              lambda index, start: f'<div class="glow"></div>{recolor(stopwatch(start), TEAL)}',
              "IA generativa · explicación", MONICA, 185, 60, out("Video/RAG en 1 minuto.mp4"))
    explainer(EVALS_VIDEO, recolor(FOUNDRY_CSS, AMBER),
              lambda index, start: f'<div class="glow"></div>{recolor(stopwatch(start), AMBER)}',
              "Agentes · explicación", PAULINA, 190, 45, out("Video/Evaluaciones de agentes en 45 segundos.mp4"))
    show(ONBOARDING_VIDEO, theme("#fff8ef", "#3b1d0e", "#ea580c", "#7c4a2d", "#b08968", glow("234,88,12,.10"), SERIF),
         "Contoso · personas", out("Video/Bienvenida a Contoso – onboarding.mp4"), badge("#ea580c", "#fff8ef"))
    show(TEASER_VIDEO, theme("#0e2118", "#f5efe0", "#e9d8a6", "#d6ccb0", "#7f8f78", glow("233,216,166,.13"),
                             '700 64px/1.02 "Avenir Next Condensed","Avenir Next",system-ui'),
         "Contoso Outdoor · Trailhead 3", out("Video/Trailhead 3 – teaser.mp4"), tent("#e9d8a6"))
    show(PHISHING_VIDEO, theme("#ffffff", "#111827", "#dc2626", "#374151", "#9ca3af", glow("220,38,38,.07")),
         "Contoso · seguridad", out("Video/Phishing – 3 señales para detectarlo.mp4"), hook("#dc2626"))
    show(SETUP_VIDEO, theme("#f6f1e7", "#1f3a2e", "#2f6b4f", "#4b5e52", "#8a8f7c", glow("47,107,79,.10"), AVENIR),
         "Trailhead 3 · setup guide", out("Video/Trailhead 3 – setup guide.mp4"), tent("#2f6b4f"))
    show(OFFSITE_VIDEO, theme("#f8f5ec", "#14213d", "#1d4ed8", "#3d4a6b", "#8a8fa3", glow("242,183,5,.12"), SERIF),
         "Offsite Lisboa · 21–23 oct", out("Video/Offsite Lisboa – información práctica.mp4"),
         tiles("#1d4ed8", "#f2b705"))
    show(SUMMIT_VIDEO, theme("#050510", "#f0fdff", "#22d3ee", "#bae6fd", "#5b7a8c",
                             glow("34,211,238,.16", "168,85,247,.12"), '700 60px/1.04 "Avenir Next",system-ui'),
         "Data Summit · Madrid · Nov 12", out("Video/Data Summit Madrid – save the date.mp4"), halftone("#22d3ee"))
