# Lote "variado" del 16/11/2026 (petición de Xavi): 5 vídeos de CONTENIDO (sin app), cada uno con
# un personaje distinto (looks.py), un escenario distinto (escenarios.py) y su propia animación ambiental.
# Uso: python3 pipeline/satira/lote_2026-11-16v.py [chk] [tema ...]
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["SRC_VIDEO"] = os.path.abspath(os.path.join(HERE, "..", "..", "procesadas", "grabacion_2026-11-02.mp4"))
sys.path.insert(0, HERE)
from animado import *
import animado as AN, escenarios as EC, voz_viva
from looks import LOOKS
EC.instalar(); voz_viva.patch(M)
M.SUBS += [("Naruto", "Narúto"), ("narutomaki", "narutomáki"), ("Uzumaki", "Uzumáki"), ("Ichiraku", "Ichiráku"), ("Los Simpson", "Los Símpson"),
           ("Bob Esponja", "Bob Esponja"), ("Pixar", "Píxar"), ("Sun Wukong", "Sun Ukong"), ("Goku", "Gokú"), ("Shonen Jump", "Shónen Yamp"), ("shonen", "shónen")]
ES.VOICE_CHAIN = "highpass=f=75,equalizer=f=3000:t=q:w=1.4:g=1.2,acompressor=threshold=0.15:ratio=2:attack=10:release=150,"
ES.MUSIC_VOL = 0.2
LOTE = "2026-11-16v"
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "videos"))
O = ("open", "open"); PR = ("fist", "point"); PL = ("point", "fist"); OR_ = ("fist", "open")
INK2 = (22, 16, 30)


def _wrap(txt, n=15):
    out, cur = [], ""
    for w in txt.split():
        if cur and len(cur) + 1 + len(w) > n: out.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    if cur: out.append(cur)
    return out


def A_preg2(txt, bgname, sub="TE LEO EN COMENTARIOS", pose=("present", "point_up_r")):
    """tarjeta final con la pregunta sobre el escenario del propio vídeo (difuminado), sin logo ni app"""
    tr = MO.Track([K(0.0, pose[0], "happy", OR_), K(0.55, pose[1], "wink", PR)])
    lines = _wrap(txt)
    def draw(T, d, o):
        im = AN.bg(bgname + ":blur", T); size = 118 if len(lines) <= 2 else 100; y0 = 520
        for i, l in enumerate(lines):
            paste_c(im, big(l, size, YEL, (110, 40, 0)), W / 2, y0 + i * size * 1.08, pop(T, 0.08 + 0.1 * i, 0.3), rot=-3 + 2 * (i % 2))
        yb = y0 + len(lines) * size * 1.08 + 70
        paste_c(im, pill(sub, 56, path=MB), W / 2, yb, pop(T, 0.5, 0.3) * (1 + 0.04 * math.sin(T * 6)))
        put(im, T, o, tr, cx=W / 2 - 150, sc=0.7, foot=1900)
        return im
    return draw, lambda d, o: [(0.08, "pop", 0.7), (0.5, "pop2", 0.8)]


# ---------------- props dibujados ----------------
def naruto_slice(im, x, y, r, rot=0.0):
    d = ImageDraw.Draw(im)
    pts = [(x + (r + (10 if k % 2 else 0)) * math.cos(k * math.pi / 16), y + (r + (10 if k % 2 else 0)) * math.sin(k * math.pi / 16)) for k in range(32)]
    d.polygon(pts, fill=(250, 250, 248)); d.ellipse((x - r, y - r, x + r, y + r), outline=(230, 225, 220), width=4)
    sp = [(x + (r * 0.8) * (a / 12) * math.cos(a + rot), y + (r * 0.8) * (a / 12) * math.sin(a + rot)) for a in [i * 0.15 for i in range(81)]]
    d.line(sp, fill=(240, 100, 150), width=max(6, int(r / 7)), joint="curve")


def bowl(im, T, u, x=W / 2, y=1000, s=1.0, slice_=True):
    d = ImageDraw.Draw(im)
    for k in range(5):   # vapor
        v = (T * 0.4 + k / 5) % 1; xx = x + (k - 2) * 50 * s + 25 * math.sin(T * 2 + k); yy = y - 120 * s - v * 260 * s; rr = (20 + 40 * v) * s
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(ov).ellipse((xx - rr, yy - rr, xx + rr, yy + rr), fill=(255, 255, 255, int(120 * (1 - v)))); im.alpha_composite(ov)
    d = ImageDraw.Draw(im)
    d.ellipse((x - 230 * s, y - 70 * s, x + 230 * s, y + 50 * s), fill=(240, 200, 120))                    # caldo
    for k in range(6): d.arc((x - 180 * s + k * 50 * s, y - 50 * s, x - 100 * s + k * 50 * s, y + 20 * s), 200, 340, fill=(255, 235, 170), width=int(10 * s))
    d.ellipse((x + 60 * s, y - 50 * s, x + 160 * s, y + 10 * s), fill=(255, 255, 250)); d.ellipse((x + 90 * s, y - 36 * s, x + 130 * s, y - 4 * s), fill=(255, 190, 40))   # huevo
    for k in range(5): d.line((x - 200 * s + k * 18 * s, y - 40 * s, x - 190 * s + k * 18 * s, y + 10 * s), fill=(90, 170, 70), width=int(8 * s))   # cebolleta
    if slice_: naruto_slice(im, x - 40 * s, y - 20 * s, 48 * s, T * 0.5)
    d.chord((x - 240 * s, y - 120 * s, x + 240 * s, y + 230 * s), 0, 180, fill=(210, 50, 45)); d.rectangle((x - 80 * s, y + 220 * s, x + 80 * s, y + 250 * s), fill=(150, 30, 30))
    for k in range(3): d.arc((x - 180 * s + k * 120 * s, y + 40 * s, x - 80 * s + k * 120 * s, y + 140 * s), 0, 360, fill=(250, 220, 120), width=int(6 * s))


def espiral(im, T, u, x=W / 2, y=980, r=260):
    d = ImageDraw.Draw(im); k = min(1, u / 0.4)
    sp = [(x + r * k * (a / 18.8) * math.cos(a - T * 3), y + r * k * (a / 18.8) * math.sin(a - T * 3)) for a in [i * 0.12 for i in range(157)]]
    d.line(sp, fill=(255, 225, 80), width=26, joint="curve")


def libro(im, T, u, x=W / 2, y=1050, s=1.0, dir_=-1, cover=None):
    """libro abierto; dir_=-1: la página pasa de izquierda a derecha (lectura japonesa)"""
    d = ImageDraw.Draw(im); w, h = 300 * s, 400 * s
    d.rounded_rectangle((x - w - 16, y - h / 2 - 12, x + w + 16, y + h / 2 + 16), radius=14, fill=cover or (60, 90, 170))
    d.rectangle((x - w, y - h / 2, x + w, y + h / 2), fill=(250, 248, 238)); d.line((x, y - h / 2, x, y + h / 2), fill=(200, 196, 186), width=6)
    for side in (-1, 1):
        for r_ in range(3):   # viñetas
            for c_ in range(2):
                bx = x + side * 30 * s + (side * c_ * 130 * s) + (0 if side > 0 else -120 * s); by = y - h / 2 + 25 * s + r_ * 125 * s
                d.rectangle((bx, by, bx + 115 * s, by + 105 * s), outline=INK2, width=4)
    ph = (T * 0.8) % 1; k = math.sin(math.pi * ph)   # página pasando
    xe = x - dir_ * w * math.cos(math.pi * ph)
    d.polygon([(x, y - h / 2), (xe, y - h / 2 - 30 * k * s), (xe, y + h / 2 - 30 * k * s), (x, y + h / 2)], fill=(238, 234, 222), outline=(190, 186, 176))


def flecha(im, T, u, y=820, dir_=-1):
    d = ImageDraw.Draw(im); k = ease_out(min(1, u / 0.6)); x0 = W / 2 - dir_ * 330; x1 = x0 + dir_ * 660 * k
    d.line((x0, y, x1, y), fill=YEL, width=30)
    d.polygon([(x1 + dir_ * 60, y), (x1 - dir_ * 10, y - 55), (x1 - dir_ * 10, y + 55)], fill=YEL)


def cola(im, T, u, x=W / 2 + 120, y=1500):
    d = ImageDraw.Draw(im); pts = [(x + 26 * i, y - 12 * i + 40 * math.sin(T * 5 + i * 0.5) * (i / 10)) for i in range(11)]
    d.line(pts, fill=(130, 84, 40), width=26, joint="curve")


def cine_carteles(im, T, u, names=("DISNEY", "PIXAR", "BOB ESPONJA")):
    for i, n in enumerate(names):
        t0 = i * 0.5
        if u > t0: paste_c(im, pill(n, 64, fg=DARK, bg=[(255, 140, 170), (130, 200, 255), (255, 220, 90)][i]), [300, 780, 540][i], [560, 650, 760][i], pop(u, t0, 0.3), rot=[-4, 4, -2][i])


def volteo(im, T, u):
    """libro que gira como en un espejo (escena de los mangas volteados)"""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); libro(lay, 0.0, u, x=W / 2, y=1000, s=0.55, cover=(60, 120, 200))
    box = lay.crop((W // 2 - 200, 760, W // 2 + 200, 1240)); c = math.cos(u * 2.4); wd = max(8, int(400 * abs(c)))
    b2 = box.resize((wd, box.height)); b2 = b2.transpose(Image.FLIP_LEFT_RIGHT) if c < 0 else b2
    im.alpha_composite(b2, (int(250 - wd / 2), 860))


def nube_pies(im, T, u): EC.nube(im, T, u, x=W / 2, y=1840)


V = {}
# 1) RAMEN — Kenji (chico cocinero), voz st5
V["01_naruto_ramen"] = ("kenji", "st5", "lofi11", [
    ("*Naruto* es un ingrediente del ramen.", "Naruto es un ingrediente del ramen."),
    ("El *narutomaki*: la rodaja blanca con una *espiral rosa*.", "El narutomaki: la rodaja blanca con una espiral rosa."),
    ("Y su apellido, *Uzumaki*, significa *espiral*.", "Y su apellido, Uzumaki, significa espiral."),
    ("Normal que su comida favorita sea *el ramen de Ichiraku*.", "Normal que su comida favorita sea el ramen de Ichiraku."),
    ("¿Ramen o sushi? Solo uno.", "¿Ramen o sushi? Solo puedes elegir uno.")], [
    ([0], A("ramen", [K(0.0, "point_l", "neutral", PL), K(q(0, 0.5), "shock", "shock", O)], cx=790, sc=0.86,
            props=[dict(k="draw", fn=lambda im, T, u: bowl(im, T, u, x=330, y=1320, s=0.9)), dict(k="big", txt="NARUTO =", y=580, size=150, t=0.0),
                   dict(k="pill", txt="¡UN INGREDIENTE!", y=740, t=q(0, 0.5))]), 0),
    ([1], A("cocina", [K(0.0, "present", "proud", OR_)], cx=800, sc=0.86,
            props=[dict(k="draw", fn=lambda im, T, u: naruto_slice(im, 340, 1050, 200 * min(1, 0.3 + u * 2), T * 0.8), front=True),
                   dict(k="pill", txt="NARUTOMAKI", y=620, t=q(0, 0.1), rot=-3)]), 0),
    ([2], A("ramen", [K(0.0, "finger_up", "smug", PR), K(q(0, 0.55), "dizzy", "dizzy")], cx=W / 2,
            props=[dict(k="draw", fn=lambda im, T, u: espiral(im, T, u, x=W / 2, y=960, r=300), t=q(0, 0.45)), dict(k="pill", txt="UZUMAKI = ESPIRAL", y=620, t=0.1)]), 0),
    ([3], A("ramen", [K(0.0, "present", "happy", OR_), K(q(0, 0.6), "clap", "happy")], cx=780, sc=0.86,
            props=[dict(k="draw", fn=lambda im, T, u: bowl(im, T, u, x=320, y=1300, s=1.0)), dict(k="stamp", txt="SU COMIDA FAVORITA", col=GREEN, t=q(0, 0.45), y=640, size=90)],
            fx=[dict(k="hearts", t=q(0, 0.5))]), 0),
    ([4], A_preg2("¿RAMEN O SUSHI?", "ramen", sub="SOLO PUEDES ELEGIR UNO"), 1.4)])

# 2) CINE — Yuna (chica de moños rosas), voz st0
V["02_simpson_anime"] = ("yuna", "st0", "lofi12", [
    ("En Japón, *Los Simpson* son anime.", "En Japón, Los Simpson son anime."),
    ("Allí *anime* significa *cualquier dibujo animado*, venga de donde venga.", "Allí, anime significa cualquier dibujo animado, venga de donde venga."),
    ("*Disney*, *Pixar*, *Bob Esponja*… para un japonés, *todo es anime*.", "Disney, Pixar, Bob Esponja… para un japonés, todo es anime."),
    ("Fuera de Japón, «anime» es solo la *animación japonesa*.", "Fuera de Japón, anime es solo la animación japonesa."),
    ("¿Los Simpson son anime? ¿Sí o no?", "Entonces… ¿Los Simpson son anime? ¿Sí o no?")], [
    ([0], A("cine", [K(0.0, "stand", "neutral"), K(q(0, 0.45), "shock", "shock", O)], foot=1760,
            props=[dict(k="big", txt="¿LOS SIMPSON", y=600, size=130, t=0.0), dict(k="big", txt="SON ANIME?", y=750, size=150, t=q(0, 0.35)),
                   dict(k="draw", fn=lambda im, T, u: EC.cine_butacas(im, T, u), front=True)]), 0),
    ([1], A("cine_hall", [K(0.0, "finger_up", "smug", PR), K(q(0, 0.55), "present", "proud", OR_)], cx=430, sc=0.9,
            props=[dict(k="pill", txt="ANIME = DIBUJOS ANIMADOS", y=760, t=0.1, rot=-3), dict(k="stamp", txt="DE DONDE SEA", col=GREEN, t=q(0, 0.6), y=960, size=90)]), 0),
    ([2], A("cine", [K(0.0, "sit_happy", "happy"), K(q(0, 0.7), "sit", "shock")], foot=1700,
            props=[dict(k="draw", fn=lambda im, T, u: cine_carteles(im, T, u), t=0.05), dict(k="stamp", txt="TODO ES ANIME", col=RED, t=q(0, 0.72), y=960),
                   dict(k="draw", fn=lambda im, T, u: EC.cine_butacas(im, T, u), front=True)]), 0),
    ([3], A("cine_hall", [K(0.0, "shrug", "confused", O)], cx=430, sc=0.9,
            props=[dict(k="pill", txt="FUERA: SOLO LO JAPONÉS", y=760, t=0.1, rot=3)], fx=[dict(k="qmarks", t=q(0, 0.4))]), 0),
    ([4], A_preg2("¿LOS SIMPSON SON ANIME?", "cine", sub="¿SÍ O NO?"), 1.4)])

# 3) BIBLIOTECA — Aiko (chica de pelo largo y gafas), voz st4
V["03_manga_al_reves"] = ("aiko", "st4", "lofi13", [
    ("Si lees manga, lo lees *al revés*.", "Si lees manga, lo lees al revés."),
    ("Se lee de *derecha a izquierda*: empiezas por la que para ti es *la última página*.", "Se lee de derecha a izquierda: empiezas por la que para ti es la última página."),
    ("Antes, aquí muchos mangas se publicaban *volteados*, como en un espejo… y los personajes salían *zurdos*.", "Antes, aquí muchos mangas se publicaban volteados, como en un espejo… y los personajes salían zurdos."),
    ("Hoy casi todos se publican *en su sentido original*.", "Hoy casi todos se publican en su sentido original."),
    ("¿Manga en papel o en el móvil?", "¿Tú lo lees en papel o en el móvil?")], [
    ([0], A("biblio", [K(0.0, "scratch", "confused"), K(q(0, 0.5), "shock", "shock", O)], cx=W / 2,
            props=[dict(k="big", txt="AL REVÉS", y=640, size=180, t=0.0, rot=180)]), 0),
    ([1], A("biblio_mesa", [K(0.0, "point_l", "proud", PL)], cx=850, sc=0.8,
            props=[dict(k="draw", fn=lambda im, T, u: libro(im, T, u, x=420, y=1000, s=0.8, dir_=-1)), dict(k="draw", fn=lambda im, T, u: flecha(im, T, u, y=700, dir_=-1), t=0.15),
                   dict(k="pill", txt="DE DERECHA A IZQUIERDA", y=560, t=0.1, rot=-2)]), 0),
    ([2], A("biblio", [K(0.0, "point_l", "smug", PL), K(q(0, 0.65), "shock", "shock", O)], cx=780, sc=0.88,
            props=[dict(k="pill", txt="VOLTEADOS", y=620, t=0.1, rot=-3), dict(k="draw", fn=volteo, front=True),
                   dict(k="stamp", txt="¿ZURDOS?", col=RED, t=q(0, 0.68), y=820)]), 0),
    ([3], A("biblio_mesa", [K(0.0, "clap", "happy")], cx=800, sc=0.82,
            props=[dict(k="draw", fn=lambda im, T, u: libro(im, T, u, x=380, y=1020, s=0.75, cover=(170, 50, 70))), dict(k="stamp", txt="SENTIDO ORIGINAL", col=GREEN, t=q(0, 0.35), y=640, size=96)],
            fx=[dict(k="sparkle", t=q(0, 0.3))]), 0),
    ([4], A_preg2("¿EN PAPEL O EN EL MÓVIL?", "biblio"), 1.4)])

# 4) MONTAÑA — Taro (chico moreno de pelo de punta), voz st5
V["04_goku_rey_mono"] = ("taro", "st5", "lofi14", [
    ("*Goku* está basado en un mono.", "Goku está basado en un mono."),
    ("En el *Rey Mono* de una novela china del siglo XVI: *Viaje al Oeste*.", "En el Rey Mono de una novela china del siglo dieciséis: Viaje al Oeste."),
    ("Allí se llama *Sun Wukong*… y en japonés se lee *Son Goku*.", "Allí se llama Sun Wukong… y en japonés se lee Son Goku."),
    ("Por eso tenía *cola*… y volaba en *una nube*.", "Por eso tenía cola… y volaba en una nube."),
    ("¿Goku o Vegeta? Solo uno.", "¿Goku o Vegeta? Solo puedes elegir uno.")], [
    ([0], A("montana", [K(0.0, "finger_up", "smug", PR), K(q(0, 0.5), "scratch", "confused")], cx=760, sc=0.9,
            props=[dict(k="big", txt="GOKU =", y=600, size=170, t=0.0), dict(k="pill", txt="¡UN MONO!", y=780, t=q(0, 0.5))]), 0),
    ([1], A("montana", [K(0.0, "present", "proud", OR_)], cx=780, sc=0.86,
            props=[dict(k="draw", fn=lambda im, T, u: libro(im, T, u, x=330, y=1180, s=0.6, cover=(170, 40, 40))), dict(k="pill", txt="VIAJE AL OESTE", y=620, t=q(0, 0.45), rot=-3),
                   dict(k="pill", txt="SIGLO XVI", y=760, t=q(0, 0.2), bg=WHITE, rot=3)]), 0),
    ([2], A("cielo", [K(0.0, "point_l", "neutral", PL), K(q(0, 0.6), "point_r", "proud", PR)], cx=W / 2,
            props=[dict(k="pill", txt="SUN WUKONG", x=320, y=700, t=0.05, rot=-3), dict(k="draw", fn=lambda im, T, u: flecha(im, T, u, y=860, dir_=1), t=q(0, 0.5)),
                   dict(k="pill", txt="SON GOKU", x=760, y=1010, t=q(0, 0.65), rot=3)]), 0),
    ([3], A("cielo", [K(0.0, "arms_up", "happy", O)], cx=W / 2, foot=1760,
            props=[dict(k="draw", fn=lambda im, T, u: cola(im, T, u, x=W / 2 + 60, y=1560)), dict(k="draw", fn=nube_pies, front=True),
                   dict(k="pill", txt="COLA", x=300, y=640, t=q(0, 0.3), rot=-4), dict(k="pill", txt="NUBE", x=780, y=760, t=q(0, 0.75), rot=4)]), 0),
    ([4], A_preg2("¿GOKU O VEGETA?", "montana", sub="SOLO PUEDES ELEGIR UNO"), 1.4)])

# 5) ESTADIO — Mika (chica deportista de coleta azul), voz st0
V["05_amistad_esfuerzo_victoria"] = ("mika", "st0", "lofi15", [
    ("Todo shonen sigue *tres palabras*.", "Todo shonen sigue tres palabras."),
    ("Es el lema de la revista *Shonen Jump*: *amistad, esfuerzo y victoria*.", "Es el lema de la revista Shonen Jump: amistad, esfuerzo y victoria."),
    ("*Amistad*: el grupo. *Esfuerzo*: el entrenamiento. *Victoria*: el combate final.", "Amistad: el grupo. Esfuerzo: el entrenamiento. Victoria: el combate final."),
    ("Piensa en tu shonen favorito… *están las tres*.", "Piensa en tu shonen favorito… están las tres."),
    ("Solo una: ¿amistad, esfuerzo o victoria?", "Solo puedes quedarte con una: ¿amistad, esfuerzo o victoria?")], [
    ([0], A("estadio", [K(0.0, "run", "proud"), K(q(0, 0.55), "finger_up", "smug", PR)], run_until=0.9, xmove=lambda T: -700 * max(0, 1 - T / 0.9),
            props=[dict(k="big", txt="3 PALABRAS", y=680, size=170, t=0.0)]), 0),
    ([1], A("podio", [K(0.0, "present", "proud", OR_)], cx=W / 2, foot=1120, sc=0.62,
            props=[dict(k="pill", txt="AMISTAD", x=275, y=1150, t=q(0, 0.45), bg=(200, 210, 230)), dict(k="pill", txt="ESFUERZO", x=565, y=1010, t=q(0, 0.62)),
                   dict(k="pill", txt="VICTORIA", x=855, y=1230, t=q(0, 0.8), bg=(240, 160, 100))]), 0),
    ([2], A("estadio", [K(0.0, "run", "proud")], run_until=99, xmove=lambda T: 220 * math.sin(T * 0.9),
            props=[dict(k="stamp", txt="AMISTAD", col=GREEN, t=0.05, y=640, size=100, t_out=q(0, 0.33)), dict(k="stamp", txt="ESFUERZO", col=(230, 140, 30), t=q(0, 0.36), y=640, size=100, t_out=q(0, 0.7)),
                   dict(k="stamp", txt="VICTORIA", col=RED, t=q(0, 0.72), y=640, size=100)]), 0),
    ([3], A("podio", [K(0.0, "scratch", "confused"), K(q(0, 0.5), "arms_up", "happy", O)], cx=W / 2, foot=1120, sc=0.62,
            props=[dict(k="rain", kind="confetti", t=q(0, 0.5)), dict(k="stamp", txt="LAS TRES", col=YEL, t=q(0, 0.55), y=640)]), 0),
    ([4], A_preg2("¿AMISTAD, ESFUERZO O VICTORIA?", "estadio", sub="SOLO UNA"), 1.4)])

VOZ = lambda v: "chico" if v == "st5" else "chica"

if __name__ == "__main__":
    args = sys.argv[1:]; chk = "chk" in args
    names = [a for a in args if a != "chk"]
    for key, (look, voice, mus, lines, scenes) in V.items():
        tema = key[3:]
        if names and tema not in names and key not in names: continue
        MO.set_look(**LOOKS[look])
        n = f"{LOTE}_{tema}_{VOZ(voice)}"
        if chk:
            print(render(n, voice, mus, lines, scenes, OUT, frames=[(si, T) for si in range(len(scenes)) for T in (0.05, 1.6)]), flush=True); continue
        if os.path.exists(f"{OUT}/{n}.mp4"): continue
        print(render(n, voice, mus, lines, scenes, OUT), flush=True)
