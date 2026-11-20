# Lote del 20/11/2026 (petición de Xavi): 10 vídeos, cada uno con personaje, escenario, temática y animación distintos.
# Pensados para retener: algo moviéndose de forma llamativa desde el fotograma 0 (camión, tren, bola de energía, contador...)
# con un "punch" de cámara al empezar, gancho ≤ 8 palabras y pregunta cerrada al final. 4 de contenido + 6 con la app integrada.
# Uso: python3 pipeline/satira/lote_2026-11-20x.py [chk] [tema ...]
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["SRC_VIDEO"] = os.path.abspath(os.path.join(HERE, "..", "..", "procesadas", "grabacion_2026-11-02.mp4"))
sys.path.insert(0, HERE)
from animado import *
import animado as AN, escenarios as EC, escenarios2 as EC2, voz_viva
from looks import LOOKS
EC2.instalar2(); voz_viva.patch(M)
M.SUBS += [("Kamehameha", "Kamejaméja"), ("hawaiano", "jawaiano"), ("Toriyama", "Toriyáma"), ("Rasengan", "Raséngan"), ("Truck-kun", "Trak kun"), ("isekai", "isekái"),
           ("Re:Zero", "Re Zero"), ("Sword Art Online", "Sord Art Onláin"), ("Konosuba", "Konosúba"), ("One Piece", "Uan Pis"),
           ("Studio Ghibli", "Estudio Guíbli"), ("Ghibli", "Guíbli"), ("Chihiro", "Chijíro"), ("Totoro", "Totóro"), ("Pokémon", "Pokemon"),
           ("Satoshi Tajiri", "Satóshi Tayíri"), ("Charmander", "Charmánder"), ("Squirtle", "Escuírtel"), ("Bulbasaur", "Bulbasáur"), ("Top tier", "top táier")]
ES.VOICE_CHAIN = "highpass=f=75,equalizer=f=3000:t=q:w=1.4:g=1.2,acompressor=threshold=0.15:ratio=2:attack=10:release=150,"
ES.MUSIC_VOL = 0.2
LOTE = "2026-11-20x"
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "videos"))
O = ("open", "open"); PR = ("fist", "point"); PL = ("point", "fist"); OR_ = ("fist", "open")
INK2 = (22, 16, 30); GOLD2 = (250, 200, 60)
# clips de la grabación 2026-11-02 (ver README)
FILTROS = (27.4, 28.8); EPIS = (62.0, 66.0); TABS = (76.0, 80.0); PERFIL = (127.75, 127.85); LISTAS = (105.0, 107.2)


# ---------- sonido extra ----------
def _horn():
    t = np.arange(int(0.55 * SR)) / SR; env = np.minimum(1, t / 0.02) * np.minimum(1, (0.55 - t) / 0.08)
    y = sum(np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + np.sin(2 * np.pi * f * t) for f in (311, 392))
    return 0.09 * env * y
SFX["horn"] = _horn()


# ---------- utilidades de escena ----------
def punch(scene, z0=1.15, dur=0.45, shake=16):
    """gancho visual: la primera escena entra con un golpe de cámara (zoom que se asienta + pequeña sacudida que se apaga)"""
    draw0, sfx0 = scene
    def draw(T, d, o):
        im = draw0(T, d, o)
        if T >= dur: return im
        k = ease_out(T / dur); z = z0 + (1 - z0) * k; a = shake * (1 - k)
        dx = a * math.sin(T * 47); dy = a * math.cos(T * 39)
        w_, h_ = int(W / z), int(H / z); x0 = int(W / 2 - w_ / 2 + dx); y0 = int(H * 0.45 - h_ * 0.45 + dy)
        x0 = max(0, min(W - w_, x0)); y0 = max(0, min(H - h_, y0))
        return im.crop((x0, y0, x0 + w_, y0 + h_)).resize((W, H), Image.BILINEAR)
    return draw, lambda d, o: [(0.0, "boom", 0.8)] + sfx0(d, o)


def _wrap(txt, n=15):
    out, cur = [], ""
    for w in txt.split():
        if cur and len(cur) + 1 + len(w) > n: out.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    if cur: out.append(cur)
    return out


def A_preg2(txt, bgname, sub="TE LEO EN COMENTARIOS", logo=False):
    """tarjeta final: la pregunta sobre el escenario del propio vídeo difuminado; en los de app, logo pequeño (sin 'Gratis en Play Store')"""
    tr = MO.Track([K(0.0, "present", "happy", OR_), K(0.55, "point_up_r", "wink", PR)])
    lines = _wrap(txt)
    def draw(T, d, o):
        im = AN.bg(bgname + ":blur", T); size = 118 if len(lines) <= 2 else 100; y0 = 520
        for i, l in enumerate(lines):
            paste_c(im, big(l, size, YEL, (110, 40, 0)), W / 2, y0 + i * size * 1.08, pop(T, 0.08 + 0.1 * i, 0.3), rot=-3 + 2 * (i % 2))
        yb = y0 + len(lines) * size * 1.08 + 70
        paste_c(im, pill(sub, 56, path=MB), W / 2, yb, pop(T, 0.5, 0.3) * (1 + 0.04 * math.sin(T * 6)))
        if logo: paste_c(im, LOGO.resize((150, 150), Image.LANCZOS), W - 140, 1760, pop(T, 0.7, 0.3))
        put(im, T, o, tr, cx=W / 2 - 150, sc=0.7, foot=1900)
        return im
    return draw, lambda d, o: [(0.08, "pop", 0.7), (0.5, "pop2", 0.8)]


def A_app2(a, b, bgname, callout=None, mode="fit", pose_end="point_r"):
    """el móvil con la app sobre el escenario del vídeo (difuminado) y el personaje del vídeo señalándolo"""
    tr = MO.Track([K(0.0, "present", "proud", OR_), K(q(0, 0.5), pose_end, "wink", PR)])
    def draw(T, d, o):
        im = AN.bg(bgname + ":blur", T); clip = load_clip(a, b)
        fr = clip[min(len(clip) - 1, int(T / d * len(clip)))] if mode == "fit" else clip[0]; k = ease_out(T / 0.45); z = 0.9
        ph = PHONE.copy(); ph.paste(fr, (40 + BZ, 40 + BZ), MASK); top = 470 + (1 - k) * 1500; px = W / 2 + 150
        paste_c(im, ph, px, top + ph.height * z / 2, z)
        if callout:
            fx_, fy_, label, tc = callout; tc = at(tc, o); p = pop(T, tc, 0.32)
            if p > 0:
                sx = px - ph.width * z / 2 + (40 + BZ + fx_ * SCR_W) * z; sy = top + (40 + BZ + (fy_ - CROP) / (1 - CROP) * SCR_H) * z
                dr = ImageDraw.Draw(im); R = 95 * min(p, 1.2); dr.ellipse((sx - R * 1.3, sy - R * 0.75, sx + R * 1.3, sy + R * 0.75), outline=YEL, width=9)
                paste_c(im, pill(label, 62, fg=DARK, bg=YEL), clamp(sx + 60, 260, W - 230), sy + 150 if sy < 1500 else sy - 150, p, rot=5)
        put(im, T, o, tr, cx=200, sc=0.62, foot=1900)
        return im
    return draw, lambda d, o: [(0, "whoosh2", 0.8)] + ([(at(callout[3], o), "pop2", 1.2)] if callout else [])


def _ov(im):   # capa para dibujar con transparencia
    return Image.new("RGBA", im.size, (0, 0, 0, 0))


def glow(im, x, y, r, col, a=110, blur=40):
    g = _ov(im); ImageDraw.Draw(g).ellipse((x - r, y - r, x + r, y + r), fill=col + (a,)); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))


# ---------- props dibujados ----------
def camion(im, T, u, y=1560, dur=0.9, x_from=1500, x_to=-1300, s=1.0):
    """camión de reparto (genérico, sin marcas) que cruza a toda velocidad"""
    if s != 1.0:
        lay = _ov(im); camion(lay, T, u, y=1100, dur=dur, x_from=0, x_to=0); lay = lay.crop((0, 400, 1080, 1180))
        lay = lay.resize((int(lay.width * s), int(lay.height * s))); im.alpha_composite(lay, (int(x_from), int(y - lay.height))); return
    x = x_from + (x_to - x_from) * min(1, u / dur)
    if x < -1250: return
    d = ImageDraw.Draw(im)
    for k in range(6): d.line((x + 760 + k * 30, y - 300 + k * 60, x + 1000 + k * 60, y - 300 + k * 60), fill=(255, 255, 255), width=6)   # líneas de velocidad
    d.rounded_rectangle((x + 260, y - 460, x + 760, y - 40), radius=20, fill=(240, 240, 245)); d.rectangle((x + 260, y - 140, x + 760, y - 110), fill=(60, 140, 220))
    d.rounded_rectangle((x, y - 330, x + 280, y - 40), radius=40, fill=(60, 140, 220)); d.rounded_rectangle((x + 30, y - 300, x + 200, y - 190), radius=20, fill=(170, 220, 255))
    d.ellipse((x - 20, y - 150, x + 40, y - 90), fill=(255, 250, 200)); glow(im, x - 10, y - 120, 120, (255, 240, 180), 120, 40)
    d = ImageDraw.Draw(im)
    for wx in (x + 120, x + 420, x + 640):
        d.ellipse((wx - 70, y - 110, wx + 70, y + 30), fill=(30, 30, 36)); d.ellipse((wx - 30, y - 70, wx + 30, y - 10), fill=(170, 170, 180))


def portal(im, T, u, x=W / 2, y=1250, r=330):
    k = ease_out(min(1, u / 0.5)); R = r * k
    if R < 5: return
    glow(im, x, y, R * 1.1, (170, 110, 255), 120, 50)
    d = ImageDraw.Draw(im)
    for j in range(6):
        rr = R * (1 - j * 0.15); a0 = (T * (80 + j * 30) * (1 if j % 2 else -1)) % 360
        d.arc((x - rr, y - rr * 1.15, x + rr, y + rr * 1.15), a0, a0 + 250, fill=[(200, 160, 255), (120, 220, 255), (255, 255, 255)][j % 3], width=14)


def energia(im, T, u, x=W / 2 + 240, y=1180, r=170):
    k = ease_out(min(1, u / 0.7)); R = (40 + r * k) * (1 + 0.05 * math.sin(T * 5))
    glow(im, x, y, R * 1.9, (80, 170, 255), 120, 60); glow(im, x, y, R * 1.2, (150, 220, 255), 170, 25)
    d = ImageDraw.Draw(im); d.ellipse((x - R * 0.7, y - R * 0.7, x + R * 0.7, y + R * 0.7), fill=(235, 250, 255))
    for j in range(8):
        a = T * 1.5 + j * math.pi / 4; d.line((x + R * 0.9 * math.cos(a), y + R * 0.9 * math.sin(a), x + R * 1.5 * math.cos(a + 0.2), y + R * 1.5 * math.sin(a + 0.2)), fill=(190, 230, 255), width=8)


def corona(im, T, u, x=W / 2, y=700, s=1.0):
    yy = y - (1 - ease_out(min(1, u / 0.5))) * 700 + 10 * math.sin(T * 2.5)
    d = ImageDraw.Draw(im); w = 200 * s
    pts = [(x - w, yy + 90 * s), (x - w, yy - 40 * s), (x - w * 0.5, yy + 20 * s), (x, yy - 80 * s), (x + w * 0.5, yy + 20 * s), (x + w, yy - 40 * s), (x + w, yy + 90 * s)]
    d.polygon(pts, fill=GOLD2); d.rectangle((x - w, yy + 70 * s, x + w, yy + 110 * s), fill=(220, 160, 30))
    for j, c in enumerate([(230, 60, 80), (80, 160, 240), (230, 60, 80)]): d.ellipse((x - w * 0.55 + j * w * 0.55 - 18 * s, yy + 72 * s, x - w * 0.55 + j * w * 0.55 + 18 * s, yy + 108 * s), fill=c)


def bicho(d, x, y, s=1.0, col=(200, 60, 60), t=0.0):
    f = abs(math.sin(t * 14))
    d.ellipse((x - 46 * s * f - 10 * s, y - 40 * s, x - 4 * s, y + 6 * s), fill=(230, 240, 255)); d.ellipse((x + 4 * s, y - 40 * s, x + 46 * s * f + 10 * s, y + 6 * s), fill=(230, 240, 255))
    d.ellipse((x - 26 * s, y - 22 * s, x + 26 * s, y + 34 * s), fill=col); d.line((x, y - 20 * s, x, y + 34 * s), fill=INK2, width=max(2, int(4 * s)))
    d.ellipse((x - 16 * s, y - 40 * s, x + 16 * s, y - 14 * s), fill=INK2)
    for sg in (-1, 1): d.line((x + sg * 6 * s, y - 36 * s, x + sg * 22 * s, y - 60 * s), fill=INK2, width=max(2, int(4 * s)))


def red_caza(im, T, u, x0=W / 2 + 120, y0=1330):
    """cazamariposas que da un barrido y atrapa un bicho"""
    k = ease_out(min(1, u / 0.45)); a = math.radians(-150 + 120 * k)
    hx, hy = x0 + 430 * math.cos(a), y0 + 430 * math.sin(a)
    d = ImageDraw.Draw(im); d.line((x0, y0, hx, hy), fill=(150, 100, 60), width=16)
    d.ellipse((hx - 120, hy - 90, hx + 120, hy + 90), outline=(250, 250, 250), width=10)
    net = _ov(im); ImageDraw.Draw(net).ellipse((hx - 112, hy - 82, hx + 112, hy + 82), fill=(255, 255, 255, 70)); im.alpha_composite(net)
    d = ImageDraw.Draw(im)
    if k < 1: bicho(d, W / 2 + 160 - 260 * (1 - k), 640 + 60 * math.sin(T * 6), 1.2, t=T)
    else: bicho(d, hx, hy, 0.9, t=T)


def tarros(im, T, u):
    d = ImageDraw.Draw(im)
    for j in range(3):
        x = 240 + j * 150; y = 1560
        if u < j * 0.25: continue
        d.rounded_rectangle((x - 60, y - 160, x + 60, y), radius=24, fill=(210, 240, 255), outline=(150, 190, 220), width=6); d.rectangle((x - 50, y - 180, x + 50, y - 156), fill=(200, 80, 60))
        bicho(d, x + 14 * math.sin(T * 3 + j), y - 80, 0.7, [(200, 60, 60), (60, 150, 80), (70, 110, 220)][j], T + j)


def libro_magico(im, T, u, x=W / 2 - 220, y=1300):
    d = ImageDraw.Draw(im); k = ease_out(min(1, u / 0.35))
    glow(im, x, y - 60, 260 * k, (255, 230, 150), 140, 60); d = ImageDraw.Draw(im)
    w = 220 * k
    d.polygon([(x, y), (x - w, y - 40), (x - w, y + 160), (x, y + 190)], fill=(250, 246, 232)); d.polygon([(x, y), (x + w, y - 40), (x + w, y + 160), (x, y + 190)], fill=(240, 236, 220))
    d.line((x, y, x, y + 190), fill=(190, 180, 160), width=6)
    rnd = random.Random(3)
    for j in range(9):   # páginas que salen volando
        v = (u * 0.7 + j / 9) % 1; px = x + rnd.uniform(-1, 1) * 380 * v; py = y - 30 - 900 * v; a = rnd.uniform(-1, 1) * 200 * v
        pg = Image.new("RGBA", (90, 120), (255, 252, 240, int(255 * (1 - v)))); ImageDraw.Draw(pg).line((12, 30, 78, 30), fill=(180, 180, 190, int(255 * (1 - v))), width=5)
        paste_c(im, pg.rotate(a, expand=True), px, py)


def barras_vs(im, T, u, y=980):
    """ANIME (corta) vs NOVELA (larga)"""
    d = ImageDraw.Draw(im)
    for j, (lab, frac, col) in enumerate([("ANIME", 0.35, (120, 200, 255)), ("NOVELA", 0.95, (255, 200, 80))]):
        yy = y + j * 170; k = ease_out(min(1, max(0, u - j * 0.25) / 0.8)); x0 = 120
        d.rounded_rectangle((x0, yy, 700, yy + 90), radius=45, fill=(60, 50, 80))
        d.rounded_rectangle((x0, yy, x0 + max(90, (700 - x0) * frac * k), yy + 90), radius=45, fill=col)
        paste_c(im, text_img(lab, LG, 60, fill=DARK), x0 + 150, yy + 45)


def movil_scroll(im, T, u, x=W / 2 + 230, y=1180, s=0.9, color=True):
    """móvil con viñetas en vertical pasando hacia arriba (lectura tipo manhwa)"""
    w, h = 300 * s, 560 * s
    d = ImageDraw.Draw(im); d.rounded_rectangle((x - w / 2 - 16, y - h / 2 - 16, x + w / 2 + 16, y + h / 2 + 16), radius=40, fill=(20, 20, 26))
    scr = Image.new("RGBA", (int(w), int(h)), (250, 250, 250, 255)); sd = ImageDraw.Draw(scr)
    cols = [(255, 140, 170), (130, 200, 255), (255, 220, 100), (150, 230, 160), (200, 160, 255)] if color else [(60, 60, 60), (150, 150, 150), (220, 220, 220)]
    off = (T * 520) % 260
    for j in range(5):
        yy = j * 260 - off; sd.rounded_rectangle((16, yy + 10, w - 16, yy + 230), radius=10, fill=cols[j % len(cols)])
        sd.ellipse((w / 2 - 40, yy + 60, w / 2 + 40, yy + 140), fill=(255, 255, 255))
    im.alpha_composite(scr, (int(x - w / 2), int(y - h / 2)))


def pagina_manga(im, T, u, x=W / 2 - 230, y=1150):
    d = ImageDraw.Draw(im); w, h = 300, 420
    d.rectangle((x - w / 2, y - h / 2, x + w / 2, y + h / 2), fill=(250, 250, 248), outline=INK2, width=6)
    for (a, b, c, e) in [(0.05, 0.05, 0.95, 0.4), (0.05, 0.45, 0.48, 0.95), (0.52, 0.45, 0.95, 0.95)]:
        d.rectangle((x - w / 2 + a * w, y - h / 2 + b * h, x - w / 2 + c * w, y - h / 2 + e * h), outline=INK2, width=5)
    k = ease_out(min(1, u / 0.6)); y2 = y + h / 2 + 70
    d.line((x + w / 2, y2, x + w / 2 - w * k, y2), fill=YEL, width=20); d.polygon([(x + w / 2 - w * k - 40, y2), (x + w / 2 - w * k + 10, y2 - 34), (x + w / 2 - w * k + 10, y2 + 34)], fill=YEL)


def trofeo(im, T, u, x=W / 2 + 230, y=1150, s=1.0):
    """copa dorada genérica (no es la estatuilla real)"""
    yy = y + (1 - ease_out(min(1, u / 0.6))) * 900
    glow(im, x, yy - 80 * s, 230 * s, (255, 210, 90), 110, 50); d = ImageDraw.Draw(im)
    d.chord((x - 150 * s, yy - 320 * s, x + 150 * s, yy - 20 * s), 0, 180, fill=GOLD2); d.rectangle((x - 150 * s, yy - 330 * s, x + 150 * s, yy - 170 * s), fill=GOLD2)
    for sg in (-1, 1): d.arc((x + sg * 150 * s - 70 * s, yy - 300 * s, x + sg * 150 * s + 70 * s, yy - 160 * s), 270 if sg > 0 else 90, 90 if sg > 0 else 270, fill=(230, 170, 40), width=int(20 * s))
    d.rectangle((x - 24 * s, yy - 30 * s, x + 24 * s, yy + 90 * s), fill=(230, 170, 40)); d.rounded_rectangle((x - 110 * s, yy + 80 * s, x + 110 * s, yy + 150 * s), radius=int(12 * s), fill=(90, 60, 40))
    d.ellipse((x - 100 * s, yy - 290 * s, x - 40 * s, yy - 230 * s), fill=(255, 245, 190))


def podio_top3(im, T, u, y=1500):
    d = ImageDraw.Draw(im)
    for j, (x0, h, c, n) in enumerate([(60, 300, (190, 190, 205), "2"), (270, 440, GOLD2, "1"), (480, 220, (205, 130, 70), "3")]):
        k = ease_out(min(1, max(0, u - j * 0.12) / 0.4)); hh = h * k
        if hh < 4: continue
        d.rectangle((x0, y - hh, x0 + 200, y), fill=c); paste_c(im, text_img(n, LG, 120, fill=WHITE, stroke=8), x0 + 100, y - hh + 80)
        paste_c(im, text_img("?", LG, 130, fill=YEL, stroke=8), x0 + 100, y - hh - 90 + 8 * math.sin(T * 4 + j), pop(T, j * 0.12 + 0.3, 0.3)) if u > j * 0.12 + 0.3 else None


def micro(im, T, u, x=W / 2 + 260, y=1180):
    d = ImageDraw.Draw(im); d.line((x, y, x - 30, y + 320), fill=(50, 50, 60), width=26)
    d.ellipse((x - 70, y - 110, x + 70, y + 30), fill=(170, 170, 185));
    for j in range(5): d.line((x - 60, y - 90 + j * 25, x + 60, y - 90 + j * 25), fill=(120, 120, 135), width=4)


def flotar(T): return 40 * math.sin(T * 1.6)


V = {}
# 1) ISEKAI — Ren (oficinista), voz st5, APP
V["01_isekai_camion"] = ("ren", "st5", "lofi16", "app", [
    ("El *villano* del isekai… *un camión*.", "El villano del isekai… un camión."),
    ("Va el prota tan tranquilo… *¡pum!*… y despierta en *otro mundo*.", "Va el prota tan tranquilo… ¡pum!… y despierta en otro mundo."),
    ("Es tan típico del isekai que los fans le llaman *Truck-kun*.", "Es tan típico del isekai, que los fans le llaman Truck-kun."),
    ("Si te van, en *Manga Tracker* filtras por *Isekai* y salen todos.", "Si te van, en Manga Tracker filtras por isekai, y salen todos."),
    ("¿El mejor isekai? Dilo tú.", "¿Cuál es el mejor isekai? Dilo tú.")], [
    ([0], punch(A("carretera", [K(0.0, "phone_stand", "neutral"), K(0.35, "shock", "shock", O)], cx=430, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: camion(im, T, u, y=1720, dur=1.1, x_from=700, x_to=-1300), front=True, t=0.0),
                   dict(k="big", txt="EL VILLANO", y=600, size=150, t=-0.12), dict(k="pill", txt="¿UN CAMIÓN?", y=770, t=q(0, 0.55), rot=3)]),
          ), 0),
    ([1], A("isekai", [K(0.0, "phone_stand", "happy"), K(q(0, 0.42), "fall", "dizzy"), K(q(0, 0.72), "arms_up", "happy", O)], cx=W / 2, foot=1800, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: portal(im, T, u, x=W / 2, y=1350, r=380), t=q(0, 0.4)), dict(k="stamp", txt="¡PUM!", col=RED, t=q(0, 0.42), y=640, size=120),
                   dict(k="pill", txt="OTRO MUNDO", y=820, t=q(0, 0.75), rot=-3)], fx=[dict(k="notes", t=0.0, t_out=q(0, 0.42)), dict(k="sparkle", t=q(0, 0.75))]), 0),
    ([2], A("isekai", [K(0.0, "point_r", "smug", PR), K(q(0, 0.6), "shrug", "confused", O)], cx=330, sc=0.85,
            props=[dict(k="draw", fn=lambda im, T, u: camion(im, T, 9, y=1760, x_from=560, s=0.6), t=0.0), dict(k="pill", txt="TRUCK-KUN", x=740, y=1180, t=q(0, 0.55), rot=-4),
                   dict(k="stamp", txt="CULPABLE", col=RED, t=q(0, 0.75), y=760, size=110)]), 0),
    ([3], A_app2(*FILTROS, "isekai", callout=(0.31, 0.589, "ISEKAI", q(0, 0.55))), 0),
    ([4], A_preg2("¿EL MEJOR ISEKAI?", "isekai", sub="DILO TÚ", logo=True), 1.4)])

# 2) PLAYA DE HAWÁI — Leilani, voz st0, CONTENIDO
KAME = dict(lhx=150, lhy=60, rhx=175, rhy=30, lean=-6)
V["02_kamehameha_rey"] = ("leilani", "st0", "lofi17", "contenido", [
    ("*Kamehameha* era un *rey* de verdad.", "Kamehameha era un rey… de verdad."),
    ("*Kamehameha I* unificó las islas de *Hawái* en *1810*.", "Kamehameha primero unificó las islas de Hawái en mil ochocientos diez."),
    ("A *Toriyama* le costaba ponerle nombre al ataque… y su *mujer* le propuso *ese*.", "A Toriyama le costaba ponerle nombre al ataque… y su mujer le propuso ese."),
    ("Un rey hawaiano… convertido en *el ataque más famoso del anime*.", "Un rey hawaiano… convertido en el ataque más famoso del anime."),
    ("¿Kamehameha o Rasengan?", "¿Kamehameha o Rasengan? Solo puedes elegir uno.")], [
    ([0], punch(A("playa", [K(0.0, ("stand", KAME), "proud", O), K(q(0, 0.55), "shock", "shock", O)], cx=420, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: energia(im, T, u, x=720, y=1250, r=170), t=0.0, t_out=q(0, 0.55)),
                   dict(k="big", txt="KAMEHAMEHA", y=600, size=150, t=-0.12), dict(k="stamp", txt="¿UN REY?", col=RED, t=q(0, 0.55), y=800)])), 0),
    ([1], A("playa", [K(0.0, "present", "proud", OR_), K(q(0, 0.6), "finger_up", "smug", PR)], cx=780, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: corona(im, T, u, x=330, y=1180, s=1.0), front=True), dict(k="pill", txt="HAWÁI", x=320, y=640, t=q(0, 0.4), rot=-4),
                   dict(k="pill", txt="AÑO 1810", x=330, y=780, t=q(0, 0.75), bg=WHITE, rot=3)]), 0),
    ([2], A("playa_tarde", [K(0.0, "scratch", "confused"), K(q(0, 0.6), "finger_up", "happy", PR)], cx=W / 2, sc=0.95,
            props=[dict(k="pill", txt="TORIYAMA", y=540, t=0.05, rot=-3), dict(k="stamp", txt="IDEA DE SU MUJER", col=GREEN, t=q(0, 0.65), y=700, size=90)],
            fx=[dict(k="qmarks", t=0.1, t_out=q(0, 0.6)), dict(k="hearts", t=q(0, 0.7))]), 0),
    ([3], A("playa_tarde", [K(0.0, ("stand", KAME), "proud", O)], cx=400, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: energia(im, T, u, x=720, y=1250, r=230), t=0.0), dict(k="stamp", txt="LEYENDA", col=YEL, t=q(0, 0.6), y=700)]), 0),
    ([4], A_preg2("¿KAMEHAMEHA O RASENGAN?", "playa", sub="SOLO PUEDES ELEGIR UNO"), 1.4)])

# 3) METRO — Sora (estudiante), voz st4, APP
V["03_capitulo_metro"] = ("sora", "st4", "lofi18", "app", [
    ("¿Por qué capítulo ibas? *Ni idea*.", "¿Por qué capítulo ibas? Ni idea."),
    ("Lo dejaste a medias en el metro, pasan *dos semanas*… y dudas entre el *6* y el *9*.", "Lo dejaste a medias en el metro, pasan dos semanas… y dudas entre el seis y el nueve."),
    ("Y acabas viendo otra vez *veinte minutos* que ya habías visto.", "Y acabas viendo otra vez veinte minutos que ya habías visto."),
    ("En *Manga Tracker* apuntas el *episodio exacto*… y se acabó dudar.", "En Manga Tracker apuntas el episodio exacto… y se acabó dudar."),
    ("¿Cuántas veces te ha pasado?", "¿Cuántas veces te ha pasado? Di un número.")], [
    ([0], punch(A("anden", [K(0.0, "scratch", "confused"), K(q(0, 0.6), "shrug", "shock", O)], cx=W / 2, foot=1860,
            props=[dict(k="big", txt="¿POR QUÉ", y=560, size=150, t=-0.12), dict(k="big", txt="CAPÍTULO IBAS?", y=710, size=130, t=0.1)],
            fx=[dict(k="qmarks", t=q(0, 0.55))])), 0),
    ([1], A("metro", [K(0.0, "sit_phone", "happy", phone="r"), K(q(0, 0.6), "sit_wait", "confused")], foot=1530, cx=420, sc=0.9,
            props=[dict(k="calendar", seq=["DÍA 1", "DÍA 7", "DÍA 14"], x=820, y=760, s=1.0, t=q(0, 0.2), t_end=(0, 0, 0.55)),
                   dict(k="pill", txt="¿EP. 6?", x=740, y=1060, t=q(0, 0.72), rot=-5), dict(k="pill", txt="¿EP. 9?", x=880, y=1200, t=q(0, 0.86), rot=5)]), 0),
    ([2], A("metro", [K(0.0, "sit", "tired")], foot=1530, cx=420, sc=0.9,
            props=[dict(k="clock", x=800, y=820, r=170, speed=16), dict(k="stamp", txt="OTRA VEZ", col=RED, t=q(0, 0.55), y=620, size=110)],
            fx=[dict(k="zzz", t=q(0, 0.4))]), 0),
    ([3], A_app2(*EPIS, "metro", callout=(0.25, 0.455, "EPISODIO 7", q(0, 0.5))), 0),
    ([4], A_preg2("¿CUÁNTAS VECES TE HA PASADO?", "metro", sub="DI UN NÚMERO", logo=True), 1.4)])

# 4) PRADO — Kaito (explorador), voz st5, CONTENIDO
V["04_pokemon_bichos"] = ("kaito", "st5", "lofi19", "contenido", [
    ("*Pokémon* nació de *cazar bichos*.", "Pokémon nació… de cazar bichos."),
    ("De niño, *Satoshi Tajiri* coleccionaba insectos. Le llamaban *Doctor Bicho*.", "De niño, Satoshi Tajiri coleccionaba insectos. Le llamaban… Doctor Bicho."),
    ("Quería que los niños de ciudad vivieran lo mismo: *buscar*, *atrapar* y *coleccionar*.", "Quería que los niños de ciudad vivieran lo mismo: buscar, atrapar y coleccionar."),
    ("Por eso el lema era… *¡hazte con todos!*", "Por eso el lema era… ¡hazte con todos!"),
    ("¿Charmander, Squirtle o Bulbasaur?", "¿Cuál fue tu primero? ¿Charmander, Squirtle o Bulbasaur?")], [
    ([0], punch(A("prado", [K(0.0, "point_up_r", "proud", PR), K(0.5, "arms_up", "happy", O)], cx=420, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: red_caza(im, T, u, x0=520, y0=1330), front=True, t=0.0),
                   dict(k="big", txt="POKÉMON NACIÓ", y=560, size=130, t=-0.12), dict(k="pill", txt="¡CAZANDO BICHOS!", y=730, t=q(0, 0.6), rot=-3)])), 0),
    ([1], A("prado", [K(0.0, "present", "proud", OR_), K(q(0, 0.65), "finger_up", "smug", PR)], cx=760, sc=0.88,
            props=[dict(k="draw", fn=tarros, t=0.1), dict(k="pill", txt="SATOSHI TAJIRI", y=600, t=0.05, rot=-3),
                   dict(k="stamp", txt="DOCTOR BICHO", col=GREEN, t=q(0, 0.7), y=800, size=96)]), 0),
    ([2], A("prado_noche", [K(0.0, "run", "proud")], run_until=99, xmove=lambda T: 200 * math.sin(T * 0.9),
            props=[dict(k="stamp", txt="BUSCAR", col=GREEN, t=q(0, 0.55), y=660, size=100, t_out=q(0, 0.72)),
                   dict(k="stamp", txt="ATRAPAR", col=(230, 140, 30), t=q(0, 0.72), y=660, size=100, t_out=q(0, 0.86)),
                   dict(k="stamp", txt="COLECCIONAR", col=RED, t=q(0, 0.86), y=660, size=100)]), 0),
    ([3], A("prado", [K(0.0, "arms_up", "happy", O)], cx=W / 2,
            props=[dict(k="rain", kind="confetti", t=q(0, 0.4)), dict(k="big", txt="¡HAZTE CON TODOS!", y=640, size=120, t=q(0, 0.4))], fx=[dict(k="stars", t=0.1)]), 0),
    ([4], A_preg2("¿CHARMANDER, SQUIRTLE O BULBASAUR?", "prado", sub="¿CUÁL FUE TU PRIMERO?"), 1.4)])

# 5) CAFETERÍA-LIBRERÍA — Nora (barista), voz st0, APP
V["05_novelas_libro"] = ("nora", "st0", "lofi20", "app", [
    ("Tu anime favorito empezó *siendo un libro*.", "Tu anime favorito… empezó siendo un libro."),
    ("*Re:Zero*, *Sword Art Online*, *Konosuba*… todos nacieron como *novela ligera*.", "Re:Zero, Sword Art Online, Konosuba… todos nacieron como novela ligera."),
    ("Y la novela suele ir *muy por delante* del anime.", "Y la novela suele ir muy por delante del anime."),
    ("En *Manga Tracker* también buscas *novelas*, en su propia pestaña.", "En Manga Tracker también buscas novelas, en su propia pestaña."),
    ("¿Primero el anime o la novela?", "¿Tú qué haces primero? ¿El anime o la novela?")], [
    ([0], punch(A("cafe", [K(0.0, "shock", "shock", O), K(0.6, "present", "proud", OR_)], cx=760, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: libro_magico(im, T, u, x=330, y=1260), front=True, t=0.0),
                   dict(k="big", txt="ERA UN LIBRO", y=600, size=150, t=-0.12)])), 0),
    ([1], A("cafe_mesa", [K(0.0, "finger_up", "smug", PR), K(q(0, 0.75), "clap", "happy")], cx=820, sc=0.85, foot=1850,
            props=[dict(k="pill", txt="RE:ZERO", x=330, y=620, t=q(0, 0.02), rot=-4), dict(k="pill", txt="SWORD ART ONLINE", x=420, y=760, t=q(0, 0.18), bg=WHITE, rot=3),
                   dict(k="pill", txt="KONOSUBA", x=320, y=900, t=q(0, 0.42), rot=-2), dict(k="stamp", txt="NOVELA LIGERA", col=GREEN, t=q(0, 0.72), y=1100, x=420, size=90)]), 0),
    ([2], A("cafe_mesa", [K(0.0, "point_l", "proud", PL)], cx=860, sc=0.8, foot=1850,
            props=[dict(k="draw", fn=lambda im, T, u: barras_vs(im, T, u, y=1000), t=0.1), dict(k="pill", txt="LA NOVELA VA POR DELANTE", y=820, t=q(0, 0.5), rot=-3)]), 0),
    ([3], A_app2(*TABS, "cafe", callout=(0.86, 0.16, "NOVELAS", q(0, 0.5))), 0),
    ([4], A_preg2("¿PRIMERO EL ANIME O LA NOVELA?", "cafe", sub="TE LEO EN COMENTARIOS", logo=True), 1.4)])

# 6) BARCO — Hiro (marinero), voz st5, CONTENIDO
V["06_one_piece_dias"] = ("hiro", "st5", "lofi1", "contenido", [
    ("*One Piece* del tirón: *18 días*.", "One Piece del tirón… dieciocho días."),
    ("El anime ya supera los *1.100 episodios*.", "El anime ya supera los mil cien episodios."),
    ("A unos *24 minutos* cada uno, son más de *440 horas*.", "A unos veinticuatro minutos cada uno, son más de cuatrocientas cuarenta horas."),
    ("Más de *18 días seguidos*… sin dormir ni comer.", "Más de dieciocho días seguidos… sin dormir, ni comer."),
    ("¿Lo has visto entero? ¿Sí o no?", "¿Lo has visto entero? ¿Sí o no?")], [
    ([0], punch(A("barco", [K(0.0, "arms_up", "shock", O), K(0.7, "point_up_r", "smug", PR)], cx=W / 2 - 160, sc=0.9,
            props=[dict(k="counter", a=0, b=18, suf=" DÍAS", y=640, size=190, dur=0.9, t=-0.05), dict(k="clock", x=820, y=1080, r=130, speed=30, t=0.0)])), 0),
    ([1], A("barco", [K(0.0, "present", "proud", OR_), K(q(0, 0.65), "shock", "shock", O)], cx=760, sc=0.88,
            props=[dict(k="counter", a=0, b=1100, pre="+", y=640, size=180, dur=1.3, t=0.05), dict(k="pill", txt="EPISODIOS", y=820, t=q(0, 0.45), rot=-3),
                   dict(k="books", n=20, x=320, y=1700, dur=1.4, t=0.1)]), 0),
    ([2], A("barco_noche", [K(0.0, "finger_up", "smug", PR), K(q(0, 0.6), "scratch", "confused")], cx=W / 2,
            props=[dict(k="pill", txt="24 MIN × 1.100", y=600, t=0.05, rot=-3), dict(k="counter", a=0, b=440, pre="+", suf=" H", y=790, size=170, dur=1.2, t=q(0, 0.5))]), 0),
    ([3], A("barco_noche", [K(0.0, "dizzy", "dizzy")], cx=W / 2,
            props=[dict(k="calendar", seq=["DÍA 1", "DÍA 6", "DÍA 12", "DÍA 18"], x=W / 2, y=720, s=1.1, t=0.0, t_end=(0, 0, 0.7))], fx=[dict(k="zzz", t=q(0, 0.5))]), 0),
    ([4], A_preg2("¿LO HAS VISTO ENTERO?", "barco", sub="¿SÍ O NO?"), 1.4)])

# 7) AZOTEA DE NEÓN — Jin, voz st4, APP
V["07_manhwa_vertical"] = ("jin", "st4", "lofi2", "app", [
    ("Manga, manhwa, manhua: *¿la diferencia?*", "Manga, manhwa, manhua… ¿la diferencia?"),
    ("*Manga*: de Japón, en blanco y negro, de derecha a izquierda.", "Manga: de Japón, en blanco y negro, y de derecha a izquierda."),
    ("*Manhwa*: de Corea, casi siempre *a color* y *en vertical*. Y el *manhua*, de *China*.", "Manhwa: de Corea, casi siempre a color y en vertical. Y el manhua… de China."),
    ("En *Manga Tracker* tienes los tres, cada uno en su pestaña.", "En Manga Tracker tienes los tres, cada uno en su pestaña."),
    ("¿Manga o manhwa? Solo uno.", "¿Manga o manhwa? Solo puedes elegir uno.")], [
    ([0], punch(A("azotea", [K(0.0, "phone_stand", "smug"), K(q(0, 0.6), "shrug", "confused", O)], cx=360, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: movil_scroll(im, T, u, x=760, y=1150, s=1.0), front=True, t=0.0),
                   dict(k="big", txt="MANGA · MANHWA", y=560, size=120, t=-0.12), dict(k="big", txt="· MANHUA", y=690, size=120, t=0.15)])), 0),
    ([1], A("azotea", [K(0.0, "point_l", "proud", PL)], cx=800, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: pagina_manga(im, T, u, x=330, y=1150), t=0.05), dict(k="pill", txt="JAPÓN", x=330, y=640, t=0.05, rot=-4)]), 0),
    ([2], A("callejon", [K(0.0, "present", "happy", OR_), K(q(0, 0.75), "finger_up", "smug", PR)], cx=360, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: movil_scroll(im, T, u, x=760, y=1180, s=0.9), front=True, t=0.05),
                   dict(k="pill", txt="COREA", x=760, y=560, t=0.05, rot=-4), dict(k="pill", txt="A COLOR · VERTICAL", y=680, t=q(0, 0.3), bg=WHITE, rot=3),
                   dict(k="stamp", txt="MANHUA = CHINA", col=RED, t=q(0, 0.78), y=810, size=90)]), 0),
    ([3], A_app2(*TABS, "azotea", callout=(0.67, 0.16, "MANHWA", q(0, 0.5))), 0),
    ([4], A_preg2("¿MANGA O MANHWA?", "azotea", sub="SOLO PUEDES ELEGIR UNO", logo=True), 1.4)])

# 8) GALA — Mei, voz st4, CONTENIDO
V["08_ghibli_oscar"] = ("mei", "st4", "lofi3", "contenido", [
    ("Solo un estudio de anime tiene *dos Óscar*.", "Solo un estudio de anime… tiene dos Óscar."),
    ("*Studio Ghibli*: el primero, con *El viaje de Chihiro*, en *2003*.", "Studio Ghibli: el primero, con El viaje de Chihiro, en dos mil tres."),
    ("Y el segundo, *21 años después*, con *El chico y la garza*.", "Y el segundo, veintiún años después, con El chico y la garza."),
    ("Ninguna otra película de anime ha ganado *ese premio*.", "Ninguna otra película de anime ha ganado ese premio."),
    ("¿Chihiro o Totoro?", "¿Chihiro o Totoro? Solo puedes elegir una.")], [
    ([0], punch(A("gala", [K(0.0, "shock", "shock", O), K(0.6, "present", "proud", OR_)], cx=360, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: trofeo(im, T, u, x=790, y=1350, s=1.0), t=-0.15), dict(k="big", txt="DOS ÓSCAR", y=600, size=170, t=-0.12),
                   dict(k="rain", kind="confetti", t=q(0, 0.5))])), 0),
    ([1], A("gala", [K(0.0, "point_r", "proud", PR)], cx=330, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: trofeo(im, T, 9, x=790, y=1350, s=0.85), t=0.0), dict(k="pill", txt="EL VIAJE DE CHIHIRO", y=620, t=q(0, 0.35), rot=-3),
                   dict(k="pill", txt="2003", y=770, t=q(0, 0.8), bg=WHITE, rot=3)]), 0),
    ([2], A("gala_escenario", [K(0.0, "finger_up", "smug", PR), K(q(0, 0.6), "clap", "happy")], cx=330, sc=0.88, foot=1830,
            props=[dict(k="calendar", seq=["2003", "2010", "2017", "2024"], x=790, y=760, s=1.0, t=0.0, t_end=(0, 0, 0.45)),
                   dict(k="pill", txt="EL CHICO Y LA GARZA", y=1080, x=700, t=q(0, 0.6), rot=-3)]), 0),
    ([3], A("gala_escenario", [K(0.0, "arms_up", "happy", O)], cx=W / 2,
            props=[dict(k="stamp", txt="SOLO GHIBLI", col=GOLD2, t=q(0, 0.5), y=700), dict(k="rain", kind="confetti", t=q(0, 0.5))], fx=[dict(k="stars", t=0.1)]), 0),
    ([4], A_preg2("¿CHIHIRO O TOTORO?", "gala", sub="SOLO PUEDES ELEGIR UNA"), 1.4)])

# 9) OBSERVATORIO — Luna (astrónoma), voz st0, APP
V["09_horas_anime"] = ("luna", "st0", "lofi4", "app", [
    ("¿Cuántos días llevas *viendo anime*?", "¿Cuántos días llevas… viendo anime?"),
    ("Una temporada de *12 episodios* son casi *5 horas*.", "Una temporada de doce episodios son casi cinco horas."),
    ("Con *50 animes* vistos llevas unos *10 días*… enteros.", "Con cincuenta animes vistos, llevas unos diez días… enteros."),
    ("*Manga Tracker* lo cuenta por ti en tus *estadísticas*.", "Manga Tracker lo cuenta por ti, en tus estadísticas."),
    ("¿Cuántos animes has completado?", "¿Y tú cuántos animes has completado? Di tu número.")], [
    ([0], punch(A("observatorio", [K(0.0, "scratch", "confused"), K(0.6, "point_up_r", "smug", PR)], cx=780, sc=0.9,
            props=[dict(k="clock", x=300, y=1000, r=170, speed=26, t=0.0), dict(k="big", txt="¿CUÁNTOS DÍAS?", y=600, size=150, t=-0.12)],
            fx=[dict(k="qmarks", t=0.2, t_out=0.6)])), 0),
    ([1], A("observatorio", [K(0.0, "present", "proud", OR_)], cx=780, sc=0.88,
            props=[dict(k="pill", txt="12 EPISODIOS", x=320, y=640, t=q(0, 0.2), rot=-4), dict(k="big", txt="CASI 5 HORAS", y=820, size=140, t=q(0, 0.7))]), 0),
    ([2], A("espacio", [K(0.0, "arms_up", "shock", O), K(q(0, 0.7), "dizzy", "dizzy")], cx=W / 2, foot=1700, sc=0.9, xmove=lambda T: 60 * math.sin(T * 0.8),
            props=[dict(k="pill", txt="50 ANIMES", y=600, t=0.05, rot=-3), dict(k="counter", a=0, b=10, suf=" DÍAS", y=790, size=180, dur=1.0, t=q(0, 0.55))]), 0),
    ([3], A_app2(*PERFIL, "observatorio", mode="still", callout=(0.69, 0.487, "TUS CIFRAS", q(0, 0.55))), 0),
    ([4], A_preg2("¿CUÁNTOS ANIMES HAS COMPLETADO?", "observatorio", sub="DI TU NÚMERO", logo=True), 1.4)])

# 10) KARAOKE — Dai, voz st5, APP
V["10_top3_karaoke"] = ("dai", "st5", "lofi5", "app", [
    ("Tu *top 3* de anime. *Sin pensar*.", "Tu top tres de anime. Sin pensar."),
    ("*Tres segundos*: lo primero que te venga a la cabeza.", "Tres segundos… lo primero que te venga a la cabeza."),
    ("Yo cambio el mío *cada semana*… y acabo discutiendo *conmigo mismo*.", "Yo cambio el mío cada semana… y acabo discutiendo conmigo mismo."),
    ("Por eso lo guardo en mi lista *Top tier* de *Manga Tracker*.", "Por eso lo guardo en mi lista Top tier, de Manga Tracker."),
    ("¿Tu top 3? En comentarios.", "¿Tu top tres? En comentarios. Ya.")], [
    ([0], punch(A("karaoke_esc", [K(0.0, "arms_up", "proud", O), K(0.6, "point_l", "smug", PL)], cx=870, foot=1880, sc=0.72,
            props=[dict(k="draw", fn=lambda im, T, u: podio_top3(im, T, u, y=1440), t=-0.1), dict(k="big", txt="TU TOP 3", y=560, size=180, t=-0.12)])), 0),
    ([1], A("karaoke", [K(0.0, "scratch", "confused"), K(q(0, 0.7), "finger_up", "happy", PR)], cx=760, sc=0.9,
            props=[dict(k="big", txt="3", y=700, x=320, size=260, t=q(0, 0.0), t_out=q(0, 0.33)), dict(k="big", txt="2", y=700, size=260, t=q(0, 0.33), t_out=q(0, 0.66)),
                   dict(k="big", txt="1", y=700, size=260, t=q(0, 0.66))], fx=[dict(k="qmarks", t=0.1, t_out=q(0, 0.7)), dict(k="bulb", t=q(0, 0.7))]), 0),
    ([2], A("karaoke", [K(0.0, "phone_stand", "happy"), K(q(0, 0.55), "shrug", "confused", O)], cx=420, sc=0.9,
            props=[dict(k="calendar", seq=["LUNES", "LUNES", "LUNES"], x=820, y=860, s=0.9, t=0.0, t_end=(0, 0, 0.5)), dict(k="stamp", txt="¿OTRA VEZ?", col=RED, t=q(0, 0.7), y=640, size=110)]), 0),
    ([3], A_app2(*LISTAS, "karaoke", callout=(0.35, 0.21, "TOP TIER", q(0, 0.5))), 0),
    ([4], A_preg2("¿TU TOP 3?", "karaoke_esc", sub="EN COMENTARIOS. YA.", logo=True), 1.4)])

VOZ = lambda v: "chico" if v == "st5" else "chica"

if __name__ == "__main__":
    args = sys.argv[1:]; chk = "chk" in args
    names = [a for a in args if a != "chk"]
    for key, (look, voice, mus, tipo, lines, scenes) in V.items():
        tema = key[3:]
        if names and tema not in names and key not in names: continue
        MO.set_look(**LOOKS[look])
        n = f"{LOTE}_{tema}_{VOZ(voice)}"
        if chk:
            print(ES.render(n, voice, mus, lines, scenes, OUT, frames=[(si, T) for si in range(len(scenes)) for T in ((0.0, 0.25, 1.4) if si == 0 else (0.1, 1.5))]), flush=True); continue
        if os.path.exists(f"{OUT}/{n}.mp4"): continue
        print(ES.render(n, voice, mus, lines, scenes, OUT), flush=True)
