# Lote del 21/11/2026 (tarea diaria automática): 8 vídeos, cada uno con personaje, escenario, temática y animación distintos.
# Algo llamativo moviéndose desde el fotograma 0 + "punch" de cámara, gancho ≤ 8 palabras, pregunta cerrada al final.
# 4 de contenido + 4 con la app integrada, ya ordenados para alternar (26/11 14:30 app, 21:00 contenido; 27/11 al revés...).
# Escenarios nuevos: escenarios3.py. Personajes nuevos: looks.py (momo, hana, rio, yui, takumi, iris, kuro, nami).
# Uso: python3 pipeline/satira/lote_2026-11-21y.py [chk] [tema ...]
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["SRC_VIDEO"] = os.path.abspath(os.path.join(HERE, "..", "..", "procesadas", "grabacion_2026-11-02.mp4"))
sys.path.insert(0, HERE)
from animado import *
import animado as AN, escenarios as EC, escenarios3 as EC3, voz_viva
from looks import LOOKS
EC3.instalar3(); voz_viva.patch(M)
M.SUBS += [("Doraemon", "Doraemón"), ("Shin-chan", "Shin chan"), ("Captain Tsubasa", "Képtan Tsubása"), ("Oliver", "Óliver"), ("Benji", "Bényi"),
           ("Fernando Torres", "Fernando Torres"), ("Fruits Basket", "Fruts Básket"), ("Sailor Moon", "Séilor Mun"),
           ("Arthur Conan Doyle", "Ártur Conan Dóil"), ("Sherlock Holmes", "Shérlok Jólms"), ("Sherlock", "Shérlok"), ("Edogawa Ranpo", "Edogáwa Ránpo"),
           ("Edogawa", "Edogáwa"), ("Edgar Allan Poe", "Édgar Álan Póu"), ("Ryuk", "Riúk"), ("shinigami", "shinigámi"),
           ("Light", "Láit"), ("Haikyuu", "Jaikiú"), ("Kuroko no Basket", "Kuróko no Básket"), ("Kuroko", "Kuróko")]
ES.VOICE_CHAIN = "highpass=f=75,equalizer=f=3000:t=q:w=1.4:g=1.2,acompressor=threshold=0.15:ratio=2:attack=10:release=150,"
ES.MUSIC_VOL = 0.2
LOTE = "2026-11-21y"
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "videos"))
O = ("open", "open"); PR = ("fist", "point"); PL = ("point", "fist"); OR_ = ("fist", "open")
INK2 = (22, 16, 30); GOLD2 = (250, 200, 60)
# clips de la grabación 2026-11-02 (ver README)
FILTROS = (27.4, 28.8); ESTADOS = (129.45, 129.55); LISTAS = (105.0, 107.2)


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



# ---------- props dibujados (lote 21y) ----------
def ropa_volando(im, T, u, x0=520, y0=1050):
    """prendas que salen disparadas de la lavadora y cruzan la pantalla girando"""
    rnd = random.Random(4)
    for j in range(7):
        v = (u * 0.75 + j / 7) % 1; a = rnd.uniform(-0.9, 0.9); sp = rnd.uniform(900, 1300)
        x = x0 + math.sin(a) * sp * v; y = y0 - math.cos(a) * sp * v * 0.9 + 900 * v * v; rot = (u * 300 + j * 50) % 360
        c = [(250, 110, 130), (255, 220, 90), (120, 210, 150), (110, 170, 250), (250, 250, 250), (190, 140, 250), (255, 160, 80)][j]
        pz = Image.new("RGBA", (150, 150), (0, 0, 0, 0)); dz = ImageDraw.Draw(pz)
        if j % 3 == 0: dz.polygon([(20, 30), (55, 15), (95, 15), (130, 30), (120, 60), (105, 55), (105, 130), (45, 130), (45, 55), (30, 60)], fill=c)   # camiseta
        elif j % 3 == 1: dz.rounded_rectangle((55, 10, 90, 100), radius=14, fill=c); dz.rounded_rectangle((55, 80, 130, 115), radius=16, fill=c)   # calcetín
        else: dz.polygon([(30, 20), (120, 20), (130, 130), (85, 130), (75, 60), (65, 130), (20, 130)], fill=c)   # pantalón
        paste_c(im, pz.rotate(rot, expand=True), x, y, 1.1)


def pintura(im, T, u, x=W / 2 + 230, y=1150, r=170, t_change=0.6):
    """mancha de pintura que pasa de amarillo a azul (con gotas)"""
    k = clamp((u - t_change) / 0.8); c = tuple(int(a + (b - a) * k) for a, b in zip((255, 215, 40), (40, 150, 240)))
    s = ease_out(min(1, u / 0.35)); R = r * s * (1 + 0.03 * math.sin(T * 4))
    if R < 4: return
    d = ImageDraw.Draw(im); d.ellipse((x - R, y - R * 0.9, x + R, y + R * 0.9), fill=c)
    for j in range(5):
        a = j * 1.25 + 0.4; d.ellipse((x + R * 1.05 * math.cos(a) - R * 0.28, y + R * 0.95 * math.sin(a) - R * 0.28, x + R * 1.05 * math.cos(a) + R * 0.28, y + R * 0.95 * math.sin(a) + R * 0.28), fill=c)
    for j in range(3):   # gotas que caen despacio
        v = (u * 0.5 + j / 3) % 1; gx = x - R * 0.5 + j * R * 0.5; gy = y + R * 0.8 + 260 * v
        d.ellipse((gx - 18, gy - 26, gx + 18, gy + 18), fill=c)


def raton_robot(im, T, u, y=1720, dur=1.6, x_from=1250, x_to=-200):
    """ratón robot genérico (gris, antena, ruedas) que cruza corriendo"""
    x = x_from + (x_to - x_from) * min(1, u / dur)
    if x < -180: return
    d = ImageDraw.Draw(im); b = 6 * abs(math.sin(T * 18))
    d.ellipse((x - 110, y - 120 - b, x + 90, y - b), fill=(170, 175, 190)); d.ellipse((x - 150, y - 110 - b, x - 60, y - 40 - b), fill=(170, 175, 190))
    d.ellipse((x - 150, y - 170 - b, x - 90, y - 110 - b), fill=(150, 155, 170)); d.ellipse((x - 135, y - 155 - b, x - 105, y - 125 - b), fill=(240, 170, 190))
    d.ellipse((x - 135, y - 95 - b, x - 115, y - 75 - b), fill=(220, 40, 40)); d.line((x + 90, y - 60 - b, x + 190, y - 100 - b + 20 * math.sin(T * 10)), fill=(120, 120, 135), width=8)
    d.line((x - 40, y - 120 - b, x - 20, y - 190 - b), fill=(90, 90, 100), width=6); d.ellipse((x - 32, y - 205 - b, x - 8, y - 181 - b), fill=(250, 80, 80))
    for wx in (x - 70, x + 40): d.ellipse((wx - 26, y - 30, wx + 26, y + 22), fill=(50, 50, 60))
    for k in range(4): d.line((x + 110 + k * 26, y - 100 + k * 26, x + 200 + k * 40, y - 100 + k * 26), fill=(255, 255, 255), width=5)


def lagrimas(im, T, u, x=W / 2, y=980):
    d = ImageDraw.Draw(im)
    for j in range(6):
        v = (u * 1.3 + j / 6) % 1; sg = -1 if j % 2 else 1; gx = x + sg * (60 + 160 * v); gy = y + 380 * v * v - 60 * v
        d.ellipse((gx - 16, gy - 24, gx + 16, gy + 16), fill=(120, 200, 255))


def balon(im, T, u, x0=900, y0=1750, x1=W / 2, y1=930, dur=1.0, s0=1.6, s1=0.12):
    """balón (genérico) chutado que se aleja hacia la portería del horizonte"""
    k = ease_out(min(1, u / dur)); x = x0 + (x1 - x0) * k; y = y0 + (y1 - y0) * k - 300 * math.sin(math.pi * k); r = 70 * (s0 + (s1 - s0) * k)
    d = ImageDraw.Draw(im)
    for j in range(5):   # estela
        kk = max(0, k - 0.04 * (j + 1)); xx = x0 + (x1 - x0) * kk; yy = y0 + (y1 - y0) * kk - 300 * math.sin(math.pi * kk); rr = 70 * (s0 + (s1 - s0) * kk)
        d.ellipse((xx - rr * 0.7, yy - rr * 0.7, xx + rr * 0.7, yy + rr * 0.7), fill=(255, 255, 255, 60))
    d.ellipse((x - r, y - r, x + r, y + r), fill=(250, 250, 250), outline=(30, 30, 36), width=max(2, int(r * 0.08)))
    for j in range(5):
        a = T * 6 + j * 2 * math.pi / 5; d.ellipse((x + r * 0.55 * math.cos(a) - r * 0.22, y + r * 0.55 * math.sin(a) - r * 0.22, x + r * 0.55 * math.cos(a) + r * 0.22, y + r * 0.55 * math.sin(a) + r * 0.22), fill=(30, 30, 36))


def porteria_lejos(im, T, u, x=W / 2, y=980):
    """la portería, diminuta, alejándose todavía más"""
    s = max(0.15, 1 - 0.8 * ease_out(min(1, u / 2.0))); d = ImageDraw.Draw(im); w, h = 260 * s, 110 * s
    d.rectangle((x - w, y - h, x + w, y), outline=(255, 255, 255), width=max(3, int(10 * s)))
    for k in range(1, 6): d.line((x - w + k * w / 3, y - h, x - w + k * w / 3, y), fill=(255, 255, 255, 120), width=2)


def burbujas(im, T, u, n=6):
    """burbujas de chat que no paran de llegar: «¿QUÉ VEO?»"""
    txts = ["¿QUÉ VEO?", "RECOMIÉNDAME ALGO", "¿QUÉ VEO HOY?", "¿ALGUNA SERIE?", "¿QUÉ VEO?", "PÁSAME UNA"]
    for j in range(n):
        t0 = j * 0.32
        if u < t0: continue
        x = [640, 820, 650, 830, 660, 820][j]; y = 900 + j * 150 - min(1, (u - t0) * 0.6) * 80 - max(0, u - 1.8) * 60
        paste_c(im, pill(txts[j], 50, fg=DARK, bg=WHITE if j % 2 else (150, 230, 160)), x, y, pop(T, T - (u - t0), 0.25), rot=[-4, 3, -2, 4, -3, 2][j])


def pergamino(im, T, u, x=820, y0=560):
    """lista eterna: un papel que se desenrolla hasta el suelo"""
    L = min(1250, 1250 * ease_out(min(1, u / 2.2))); d = ImageDraw.Draw(im); w = 240
    d.rectangle((x - w / 2, y0, x + w / 2, y0 + L), fill=(252, 248, 232)); rnd = random.Random(2)
    for yy in range(int(y0 + 30), int(y0 + L - 10), 44):
        d.line((x - w / 2 + 26, yy, x - w / 2 + 26 + rnd.randint(110, 190), yy), fill=(120, 120, 140), width=7)
    d.rounded_rectangle((x - w / 2 - 20, y0 + L - 22, x + w / 2 + 20, y0 + L + 22), radius=22, fill=(220, 200, 160))
    d.rounded_rectangle((x - w / 2 - 20, y0 - 22, x + w / 2 + 20, y0 + 22), radius=22, fill=(220, 200, 160))


def remolino_petalos(im, T, u, x=W / 2, y=1150):
    """remolino de pétalos de cerezo que explota hacia fuera"""
    d = ImageDraw.Draw(im); rnd = random.Random(9)
    for j in range(60):
        a = rnd.uniform(0, 2 * math.pi) + u * 2.5; r = (80 + rnd.uniform(0, 600)) * min(1, 0.25 + u * 0.9); px = x + r * math.cos(a); py = y + r * 0.8 * math.sin(a) - 120 * u
        f = abs(math.sin(T * 4 + j)); d.ellipse((px - 18, py - 10 * f - 3, px + 18, py + 10 * f + 3), fill=rnd.choice([(255, 190, 210), (255, 160, 190), (255, 225, 235)]))


def revista(im, T, u, x=820, y=1150):
    """revista genérica (sin título real) con un corazón en la portada"""
    yy = y + (1 - ease_out(min(1, u / 0.5))) * 900; d = ImageDraw.Draw(im); w, h = 230, 320
    d.rectangle((x - w / 2, yy - h / 2, x + w / 2, yy + h / 2), fill=(255, 170, 200)); d.rectangle((x - w / 2, yy - h / 2, x + w / 2, yy - h / 2 + 70), fill=(230, 60, 120))
    heart(d, x, yy + 30, 70, (255, 255, 255))


def lupa(im, T, u, x0=700, y0=1150):
    """lupa que barre la escena"""
    x = x0 + 180 * math.sin(u * 2.2); y = y0 + 90 * math.sin(u * 3.1); d = ImageDraw.Draw(im)
    lens = _ov(im); ImageDraw.Draw(lens).ellipse((x - 130, y - 130, x + 130, y + 130), fill=(200, 230, 255, 80)); im.alpha_composite(lens)
    d = ImageDraw.Draw(im); d.ellipse((x - 140, y - 140, x + 140, y + 140), outline=(90, 60, 40), width=22)
    d.line((x + 100, y + 100, x + 260, y + 260), fill=(90, 60, 40), width=34); d.arc((x - 100, y - 100, x + 40, y + 40), 190, 250, fill=(255, 255, 255), width=10)


def libro_nombre(im, T, u, x, y, col):
    d = ImageDraw.Draw(im); yy = y + (1 - ease_out(min(1, u / 0.45))) * 800 + 8 * math.sin(T * 2 + x) - 60
    d.rectangle((x - 130, yy - 180, x + 130, yy + 180), fill=col); d.rectangle((x - 130, yy - 180, x - 98, yy + 180), fill=_sh(col)); d.rectangle((x - 70, yy - 100, x + 100, yy - 66), fill=(250, 240, 200))
    d.rectangle((x - 70, yy - 40, x + 60, yy - 22), fill=(250, 240, 200))


def _sh(c): return tuple(int(v * 0.75) for v in c)


def manzanas(im, T, u, n=7):
    """manzanas que caen y botan"""
    d = ImageDraw.Draw(im); rnd = random.Random(6)
    for j in range(n):
        t0 = j * 0.13; v = u - t0
        if v < 0: continue
        x = rnd.uniform(140, W - 140); yf = rnd.uniform(1650, 1820); y = min(yf, -100 + 2600 * v * v)
        if y >= yf: y = yf - abs(math.sin((v - math.sqrt((yf + 100) / 2600)) * 7)) * 90 * math.exp(-3 * v)
        r = 48; d.ellipse((x - r, y - r, x + r, y + r), fill=(220, 40, 50)); d.ellipse((x - r * 0.55, y - r * 0.6, x - r * 0.1, y - r * 0.2), fill=(255, 140, 140))
        d.line((x, y - r, x + 8, y - r - 26), fill=(90, 60, 40), width=7); d.ellipse((x + 6, y - r - 30, x + 40, y - r - 12), fill=(70, 160, 70))


def manzana_grande(im, T, u, x=W / 2 + 250, y=1150, r=150):
    yy = y + (1 - ease_out(min(1, u / 0.5))) * -900 + 12 * math.sin(T * 2.4)
    glow(im, x, yy, r * 1.4, (255, 120, 120), 90, 40); d = ImageDraw.Draw(im)
    d.ellipse((x - r, yy - r, x + r, yy + r), fill=(215, 35, 45)); d.ellipse((x - r * 0.6, yy - r * 0.6, x - r * 0.1, yy - r * 0.15), fill=(255, 140, 140))
    d.line((x, yy - r, x + 15, yy - r - 60), fill=(90, 60, 40), width=14); d.ellipse((x + 10, yy - r - 70, x + 90, yy - r - 30), fill=(70, 160, 70))


def cuaderno(im, T, u, x=W / 2 + 240, y=1150):
    """cuaderno negro genérico (sin título)"""
    yy = y + 10 * math.sin(T * 2); d = ImageDraw.Draw(im)
    glow(im, x, yy, 220, (120, 40, 60), 80, 50); d = ImageDraw.Draw(im)
    d.rounded_rectangle((x - 130, yy - 175, x + 130, yy + 175), radius=10, fill=(20, 18, 24)); d.rectangle((x - 130, yy - 175, x - 105, yy + 175), fill=(40, 36, 46))


def remate(im, T, u, x0=900, y0=500, x1=520, y1=1640, dur=0.45):
    """remate de voleibol: el balón baja a toda velocidad y al botar suelta ondas"""
    k = min(1, u / dur); x = x0 + (x1 - x0) * k; y = y0 + (y1 - y0) * k * k; d = ImageDraw.Draw(im)
    if k < 1:
        for j in range(6): d.line((x + 30 + j * 18, y - 60 - j * 50, x + 60 + j * 22, y - 160 - j * 60), fill=(255, 255, 255), width=8)
    else:
        v = u - dur
        for j in range(3):
            R = 80 + (v * 700 + j * 90) % 400; a = max(0, int(200 - R * 0.45))
            ov = _ov(im); ImageDraw.Draw(ov).ellipse((x1 - R, y1 - R * 0.3, x1 + R, y1 + R * 0.3), outline=(255, 240, 160, a), width=12); im.alpha_composite(ov)
        y = y1 - abs(math.sin(v * 5)) * 260 * math.exp(-1.6 * v); x = x1 - 140 * v
    d = ImageDraw.Draw(im); r = 62
    d.ellipse((x - r, y - r, x + r, y + r), fill=(250, 250, 250)); d.arc((x - r, y - r, x + r, y + r), 200, 340, fill=(60, 110, 220), width=12); d.arc((x - r, y - r, x + r, y + r), 20, 160, fill=(250, 200, 50), width=12)


def marcador(im, T, u, x=W / 2, y=760):
    """marcador de sets que no para"""
    a = min(25, int(u * 9)); b = min(24, int(u * 8.6))
    d = ImageDraw.Draw(im); d.rounded_rectangle((x - 260, y - 90, x + 260, y + 90), radius=22, fill=(20, 22, 30)); d.rounded_rectangle((x - 260, y - 90, x + 260, y + 90), radius=22, outline=(250, 200, 60), width=8)
    paste_c(im, text_img(f"{a:02d} - {b:02d}", LG, 120, fill=YEL, stroke=6), x, y + 6)


V = {}
# 1) LAVANDERÍA — Momo, voz st4, APP
V["01_en_pausa"] = ("momo", "st4", "lofi6", "app", [
    ("Ese anime *no está en pausa*.", "Ese anime… no está en pausa."),
    ("Lo pusiste en pausa *hace un año*… y no lo has vuelto a tocar.", "Lo pusiste en pausa hace un año… y no lo has vuelto a tocar."),
    ("Eso tiene otro nombre: *abandonado*. Y no pasa nada.", "Eso tiene otro nombre: abandonado. Y no pasa nada."),
    ("En *Manga Tracker* tienes los dos estados… y tú decides dónde va.", "En Manga Tracker tienes los dos estados… y tú decides dónde va."),
    ("¿Cuál tienes en pausa desde hace siglos?", "¿Cuál tienes en pausa… desde hace siglos? Confiesa.")], [
    ([0], punch(A("lavanderia", [K(0.0, "shock", "shock", O), K(0.7, "point_l", "smug", PL)], cx=760, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: ropa_volando(im, T, u, x0=420, y0=980), front=True, t=0.0),
                   dict(k="big", txt="¿EN PAUSA?", y=560, size=150, t=-0.12), dict(k="pill", txt="NO, NO LO ESTÁ", y=740, t=q(0, 0.6), rot=3)])), 0),
    ([1], A("lavanderia", [K(0.0, "scratch", "confused"), K(q(0, 0.65), "shrug", "tired", O)], cx=330, sc=0.9,
            props=[dict(k="calendar", seq=["HACE 1 MES", "HACE 6 MESES", "HACE 1 AÑO"], x=800, y=760, s=1.0, t=q(0, 0.15), t_end=(0, 0, 0.75))],
            fx=[dict(k="zzz", t=q(0, 0.65))]), 0),
    ([2], A("lavanderia_noche", [K(0.0, "finger_up", "smug", PR), K(q(0, 0.6), "shrug", "happy", O)], cx=W / 2, sc=0.95,
            props=[dict(k="stamp", txt="ABANDONADO", col=RED, t=q(0, 0.3), y=600, size=120), dict(k="pill", txt="Y NO PASA NADA", y=800, t=q(0, 0.65), bg=WHITE, rot=-3)],
            fx=[dict(k="sparkle", t=q(0, 0.65))]), 0),
    ([3], A_app2(*ESTADOS, "lavanderia", mode="still", callout=(0.80, 0.452, "EN PAUSA", q(0, 0.45))), 0),
    ([4], A_preg2("¿CUÁL TIENES EN PAUSA?", "lavanderia", sub="CONFIESA", logo=True), 1.4)])

# 2) CIUDAD DEL FUTURO — Hana, voz st0, CONTENIDO
V["02_doraemon_amarillo"] = ("hana", "st0", "lofi7", "contenido", [
    ("*Doraemon* no siempre fue *azul*.", "Doraemon… no siempre fue azul."),
    ("Según su historia, es un *gato robot* del siglo XXII: fabricado en el año *2112*.", "Según su historia, es un gato robot del siglo veintidós: fabricado en el año dos mil ciento doce."),
    ("Era *amarillo*… hasta que un *ratón robot* le comió las orejas.", "Era amarillo… hasta que un ratón robot le comió las orejas."),
    ("Lloró tanto que *perdió el color*. Y por eso *odia los ratones*.", "Lloró tanto, que perdió el color. Y por eso… odia los ratones."),
    ("¿Doraemon o Shin-chan?", "¿Doraemon o Shin-chan? Solo puedes elegir uno.")], [
    ([0], punch(A("futuro", [K(0.0, "shock", "shock", O), K(0.6, "point_r", "smug", PR)], cx=330, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: pintura(im, T, u + 0.25, x=790, y=1220, r=180, t_change=0.5), t=0.0),
                   dict(k="big", txt="NO SIEMPRE", y=540, size=150, t=-0.12), dict(k="big", txt="FUE AZUL", y=690, size=150, t=0.05)])), 0),
    ([1], A("futuro", [K(0.0, "present", "proud", OR_), K(q(0, 0.6), "finger_up", "happy", PR)], cx=760, sc=0.88,
            props=[dict(k="pill", txt="GATO ROBOT", x=330, y=600, t=q(0, 0.2), rot=-4),
                   dict(k="counter", a=1970, b=2112, pre="AÑO ", fmt="{:.0f}", y=800, size=150, dur=1.1, t=q(0, 0.55))]), 0),
    ([2], A("futuro_noche", [K(0.0, "point_r", "happy", PR), K(q(0, 0.55), "shock", "shock", O)], cx=330, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: pintura(im, T, 0.3, x=790, y=1150, r=150, t_change=9), t=0.0),
                   dict(k="draw", fn=lambda im, T, u: raton_robot(im, T, u, y=1760), front=True, t=q(0, 0.45)),
                   dict(k="pill", txt="AMARILLO", x=790, y=620, t=0.05, rot=4), dict(k="stamp", txt="¡SIN OREJAS!", col=RED, t=q(0, 0.7), y=820, size=100)]), 0),
    ([3], A("futuro_noche", [K(0.0, "stand", "cry"), K(q(0, 0.7), "shock", "shock", O)], cx=330, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: pintura(im, T, u, x=790, y=1150, r=150, t_change=0.2), t=0.0),
                   dict(k="draw", fn=lambda im, T, u: lagrimas(im, T, u, x=330, y=1000), front=True, t=0.0, t_out=q(0, 0.6)),
                   dict(k="pill", txt="DE AMARILLO A AZUL", y=600, t=q(0, 0.3), rot=-3), dict(k="stamp", txt="ODIA LOS RATONES", col=RED, t=q(0, 0.72), y=780, size=90)]), 0),
    ([4], A_preg2("¿DORAEMON O SHIN-CHAN?", "futuro", sub="SOLO PUEDES ELEGIR UNO"), 1.4)])

# 3) CAMPO INFINITO — Rio, voz st5, CONTENIDO
V["03_oliver_campo_infinito"] = ("rio", "st5", "lofi8", "contenido", [
    ("El campo de *Oliver y Benji* no se acaba.", "El campo de Oliver y Benji… no se acaba."),
    ("Un pase, *cinco minutos* corriendo… y la portería sigue *lejísimos*.", "Un pase, cinco minutos corriendo… y la portería sigue lejísimos."),
    ("En Japón se llama *Captain Tsubasa*. Su autor lo empezó en *1981*.", "En Japón se llama Captain Tsubasa. Su autor lo empezó en mil novecientos ochenta y uno."),
    ("Y *Fernando Torres* ha contado que *le enganchó al fútbol*.", "Y Fernando Torres ha contado… que le enganchó al fútbol."),
    ("¿Oliver o Benji?", "¿Oliver o Benji? Solo puedes elegir uno.")], [
    ([0], punch(A("campo", [K(0.0, "run", "proud"), K(0.5, "arms_up", "shock", O)], cx=300, sc=0.85,
            props=[dict(k="draw", fn=lambda im, T, u: balon(im, T, u, x0=420, y0=1760, dur=1.1), front=True, t=0.0),
                   dict(k="big", txt="NO SE ACABA", y=600, size=160, t=-0.12)])), 0),
    ([1], A("campo", [K(0.0, "run", "proud")], run_until=99, xmove=lambda T: 160 * math.sin(T * 0.9), cx=W / 2, sc=0.85,
            props=[dict(k="draw", fn=lambda im, T, u: porteria_lejos(im, T, u), t=0.0), dict(k="timer", b=300, dur=2.0, y=620, t=q(0, 0.15)),
                   dict(k="stamp", txt="¿Y LA PORTERÍA?", col=RED, t=q(0, 0.72), y=820, size=90)]), 0),
    ([2], A("campo", [K(0.0, "present", "proud", OR_), K(q(0, 0.6), "finger_up", "smug", PR)], cx=760, sc=0.88,
            props=[dict(k="pill", txt="JAPÓN", x=320, y=600, t=0.05, rot=-4), dict(k="pill", txt="CAPTAIN TSUBASA", x=360, y=740, t=q(0, 0.25), bg=WHITE, rot=3),
                   dict(k="counter", a=1950, b=1981, pre="DESDE ", fmt="{:.0f}", y=920, size=120, dur=0.8, t=q(0, 0.6))]), 0),
    ([3], A("campo_noche", [K(0.0, "point_up_r", "proud", PR), K(q(0, 0.55), "arms_up", "happy", O)], cx=W / 2, sc=0.9,
            props=[dict(k="pill", txt="FERNANDO TORRES", y=600, t=0.05, rot=-3), dict(k="stamp", txt="ENGANCHADO", col=GREEN, t=q(0, 0.6), y=800, size=110),
                   dict(k="rain", kind="confetti", t=q(0, 0.6))], fx=[dict(k="stars", t=q(0, 0.6))]), 0),
    ([4], A_preg2("¿OLIVER O BENJI?", "campo", sub="SOLO PUEDES ELEGIR UNO"), 1.4)])

# 4) PIZZERÍA — Yui, voz st0, APP
V["04_lista_amigo"] = ("yui", "st0", "lofi9", "app", [
    ("Ese amigo que siempre pregunta: *¿qué veo?*", "Ese amigo… que siempre pregunta: ¿qué veo?"),
    ("Cada semana igual… y tú escribiéndole una *lista eterna*.", "Cada semana igual… y tú, escribiéndole una lista eterna."),
    ("Y a la semana siguiente… *te lo vuelve a preguntar*.", "Y a la semana siguiente… te lo vuelve a preguntar."),
    ("En *Manga Tracker* haces una lista *pública*… y se la pasas. Fin.", "En Manga Tracker haces una lista pública… y se la pasas. Fin."),
    ("¿Quién es? Etiquétalo.", "¿Quién es ese amigo? Etiquétalo.")], [
    ([0], punch(A("pizzeria", [K(0.0, "phone_stand", "confused"), K(0.8, "shrug", "tired", O)], cx=300, sc=0.85, foot=1860,
            props=[dict(k="draw", fn=lambda im, T, u: burbujas(im, T, u + 0.7), front=True, t=0.0),
                   dict(k="big", txt="¿QUÉ VEO?", y=560, size=170, t=-0.12)])), 0),
    ([1], A("pizzeria", [K(0.0, "write", "happy"), K(q(0, 0.6), "write", "tired")], foot=1560, cx=330, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: pergamino(im, T, u, x=820, y0=420), t=q(0, 0.1)),
                   dict(k="pill", txt="LISTA ETERNA", x=360, y=660, t=q(0, 0.55), rot=-4)]), 0),
    ([2], A("pizzeria_noche", [K(0.0, "phone_stand", "neutral"), K(q(0, 0.5), "shock", "shock", O)], cx=W / 2, sc=0.92,
            props=[dict(k="draw", fn=lambda im, T, u: burbujas(im, T, u, n=3), front=True, t=q(0, 0.4)),
                   dict(k="stamp", txt="¡OTRA VEZ NO!", col=RED, t=q(0, 0.55), y=640, size=110)]), 0),
    ([3], A_app2(*LISTAS, "pizzeria", callout=(0.74, 0.226, "PÚBLICA", q(0, 0.5))), 0),
    ([4], A_preg2("¿QUIÉN ES? ETIQUÉTALO", "pizzeria", sub="YA SABES QUIÉN ES", logo=True), 1.4)])

# 5) PARQUE DE CEREZOS — Takumi, voz st5, APP
V["05_shojo_chicos"] = ("takumi", "st5", "lofi10", "app", [
    ("¿El *shojo* es solo *para chicas*?", "¿El shojo… es solo para chicas?"),
    ("*Shojo* significa *chica joven*: es el público al que apunta la revista.", "Shojo significa chica joven: es el público al que apunta la revista."),
    ("Pero *Fruits Basket* o *Sailor Moon*… los ha visto *todo el mundo*.", "Pero Fruits Basket, o Sailor Moon… los ha visto todo el mundo."),
    ("En *Manga Tracker* filtras por *Shojo* en Demografía y lo pruebas.", "En Manga Tracker filtras por shojo, en demografía… y lo pruebas."),
    ("¿Has visto algún shojo?", "¿Has visto algún shojo? Sé sincero.")], [
    ([0], punch(A("sakura", [K(0.0, "arms_up", "shock", O), K(0.6, "scratch", "confused")], cx=W / 2, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: remolino_petalos(im, T, u, x=W / 2, y=1150), front=True, t=0.0),
                   dict(k="big", txt="¿SOLO PARA", y=540, size=150, t=-0.12), dict(k="big", txt="CHICAS?", y=690, size=170, t=0.05)])), 0),
    ([1], A("sakura", [K(0.0, "point_r", "proud", PR), K(q(0, 0.6), "finger_up", "smug", PR)], cx=320, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: revista(im, T, u, x=800, y=1250), t=0.05), dict(k="pill", txt="SHOJO = CHICA JOVEN", y=620, t=q(0, 0.2), rot=-3),
                   dict(k="pill", txt="EL PÚBLICO DE LA REVISTA", y=760, t=q(0, 0.6), bg=WHITE, rot=3)]), 0),
    ([2], A("sakura_noche", [K(0.0, "present", "happy", OR_), K(q(0, 0.6), "clap", "happy")], cx=760, sc=0.88,
            props=[dict(k="pill", txt="FRUITS BASKET", x=330, y=620, t=0.05, rot=-4), dict(k="pill", txt="SAILOR MOON", x=330, y=760, t=q(0, 0.3), bg=WHITE, rot=3),
                   dict(k="stamp", txt="TODO EL MUNDO", col=GREEN, t=q(0, 0.65), y=950, x=360, size=90)], fx=[dict(k="hearts", t=q(0, 0.65))]), 0),
    ([3], A_app2(*FILTROS, "sakura", callout=(0.504, 0.854, "SHOJO", q(0, 0.5))), 0),
    ([4], A_preg2("¿HAS VISTO ALGÚN SHOJO?", "sakura", sub="SÉ SINCERO", logo=True), 1.4)])

# 6) DESPACHO DE DETECTIVE — Iris, voz st4, CONTENIDO
V["06_conan_nombre"] = ("iris", "st4", "lofi11", "contenido", [
    ("El nombre de *Conan* esconde *dos escritores*.", "El nombre de Conan… esconde a dos escritores."),
    ("*Conan*, por *Arthur Conan Doyle*, el creador de *Sherlock Holmes*.", "Conan, por Arthur Conan Doyle… el creador de Sherlock Holmes."),
    ("Y *Edogawa*, por *Edogawa Ranpo*, maestro japonés del misterio.", "Y Edogawa, por Edogawa Ranpo… maestro japonés del misterio."),
    ("Y ojo: *Edogawa Ranpo* suena a… *Edgar Allan Poe*.", "Y ojo… Edogawa Ranpo suena a… Edgar Allan Poe."),
    ("¿Conan o Sherlock?", "¿Conan o Sherlock? ¿Quién es mejor detective?")], [
    ([0], punch(A("despacho", [K(0.0, "point_r", "smug", PR), K(0.7, "finger_up", "proud", PR)], cx=300, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: lupa(im, T, u + 0.4, x0=760, y0=1180), front=True, t=0.0),
                   dict(k="big", txt="DOS ESCRITORES", y=600, size=125, t=-0.12)])), 0),
    ([1], A("despacho", [K(0.0, "present", "proud", OR_), K(q(0, 0.6), "point_r", "smug", PR)], cx=330, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: libro_nombre(im, T, u, 790, 1250, (60, 90, 160)), t=0.05),
                   dict(k="pill", txt="CONAN = CONAN DOYLE", y=600, t=q(0, 0.2), rot=-3), dict(k="pill", txt="SHERLOCK HOLMES", y=740, t=q(0, 0.65), bg=WHITE, rot=3)]), 0),
    ([2], A("niebla", [K(0.0, "point_l", "proud", PL), K(q(0, 0.6), "finger_up", "smug", PR)], cx=760, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: libro_nombre(im, T, u, 320, 1250, (150, 40, 50)), t=0.05),
                   dict(k="pill", txt="EDOGAWA = EDOGAWA RANPO", y=600, t=q(0, 0.25), rot=-3), dict(k="pill", txt="MISTERIO JAPONÉS", y=740, t=q(0, 0.65), bg=WHITE, rot=3)]), 0),
    ([3], A("niebla", [K(0.0, "scratch", "confused"), K(q(0, 0.6), "shock", "shock", O)], cx=W / 2, sc=0.92,
            props=[dict(k="pill", txt="EDOGAWA RANPO", y=560, t=0.05, rot=-3), dict(k="big", txt="EDGAR ALLAN POE", y=740, size=120, t=q(0, 0.6)),
                   dict(k="stamp", txt="CASO RESUELTO", col=GREEN, t=q(0, 0.85), y=920, size=90)], fx=[dict(k="qmarks", t=0.1, t_out=q(0, 0.6)), dict(k="bulb", t=q(0, 0.6))]), 0),
    ([4], A_preg2("¿CONAN O SHERLOCK?", "despacho", sub="¿QUIÉN ES MEJOR DETECTIVE?"), 1.4)])

# 7) HUERTO DE MANZANOS — Kuro, voz st5, CONTENIDO
V["07_ryuk_manzanas"] = ("kuro", "st5", "lofi12", "contenido", [
    ("*Ryuk* haría *cualquier cosa* por una manzana.", "Ryuk haría cualquier cosa… por una manzana."),
    ("Para el shinigami de *Death Note*, las manzanas humanas son *adictivas*.", "Para el shinigami de Death Note, las manzanas humanas son adictivas."),
    ("Sin ellas le da *el mono*… y se retuerce como un *contorsionista*.", "Sin ellas le da el mono… y se retuerce como un contorsionista."),
    ("Y *Light* lo aprovecha: *manzanas* a cambio de *ayuda*.", "Y Light lo aprovecha: manzanas… a cambio de ayuda."),
    ("¿Light o L?", "¿Light o Ele? Solo puedes elegir uno.")], [
    ([0], punch(A("huerto", [K(0.0, "shock", "shock", O), K(0.7, "arms_up", "happy", O)], cx=W / 2, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: manzanas(im, T, u + 0.25), front=True, t=0.0),
                   dict(k="big", txt="POR UNA MANZANA", y=600, size=130, t=-0.12)])), 0),
    ([1], A("huerto", [K(0.0, "present", "proud", OR_), K(q(0, 0.6), "finger_up", "smug", PR)], cx=330, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: manzana_grande(im, T, u, x=790, y=1200), t=0.0), dict(k="pill", txt="DEATH NOTE", x=780, y=600, t=0.05, rot=4),
                   dict(k="stamp", txt="ADICTIVAS", col=RED, t=q(0, 0.7), y=800, x=700, size=110)]), 0),
    ([2], A("huerto_noche", [K(0.0, "dizzy", "dizzy"), K(q(0, 0.35), "fall", "shock"), K(q(0, 0.7), "dizzy", "dizzy")], cx=W / 2, sc=0.9,
            props=[dict(k="stamp", txt="EL MONO", col=RED, t=q(0, 0.3), y=620, size=120)], fx=[dict(k="sparkle", t=0.1)]), 0),
    ([3], A("huerto_noche", [K(0.0, "phone_stand", "smug"), K(q(0, 0.5), "present", "proud", OR_)], cx=330, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: cuaderno(im, T, u, x=800, y=1220), t=0.0),
                   dict(k="pill", txt="MANZANAS", x=780, y=600, t=q(0, 0.35), rot=4), dict(k="pill", txt="A CAMBIO DE AYUDA", y=760, t=q(0, 0.7), bg=WHITE, rot=-3)]), 0),
    ([4], A_preg2("¿LIGHT O L?", "huerto", sub="SOLO PUEDES ELEGIR UNO"), 1.4)])

# 8) PABELLÓN — Nami, voz st4, APP
V["08_deportes_haikyuu"] = ("nami", "st4", "lofi13", "app", [
    ("Odias el deporte… pero *lloraste con Haikyuu*.", "Odias el deporte… pero lloraste con Haikyuu."),
    ("Nunca has pisado una cancha… y te sabes *todas las jugadas*.", "Nunca has pisado una cancha… y te sabes todas las jugadas."),
    ("Un solo partido dura *varios episodios*… y no te aburres *ni un segundo*.", "Un solo partido dura varios episodios… y no te aburres ni un segundo."),
    ("En *Manga Tracker* filtras por *Deportes*… y sale tu próxima obsesión.", "En Manga Tracker filtras por deportes… y sale tu próxima obsesión."),
    ("¿Haikyuu o Kuroko?", "¿Haikyuu… o Kuroko? Solo uno.")], [
    ([0], punch(A("pabellon", [K(0.0, "arms_up", "shock", O), K(0.6, "shrug", "cry", O)], cx=330, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: remate(im, T, u + 0.12, x0=980, y0=380, x1=760, y1=1660), front=True, t=0.0),
                   dict(k="big", txt="¿ODIAS EL DEPORTE?", y=600, size=105, t=-0.12)])), 0),
    ([1], A("pabellon", [K(0.0, "phone_stand", "happy"), K(q(0, 0.6), "point_up_r", "proud", PR)], cx=760, sc=0.88,
            props=[dict(k="pill", txt="CERO PARTIDOS", x=330, y=600, t=0.05, rot=-4), dict(k="stamp", txt="TODAS LAS JUGADAS", col=GREEN, t=q(0, 0.6), y=800, x=420, size=80)]), 0),
    ([2], A("pabellon_vacio", [K(0.0, "phone_stand", "happy"), K(q(0, 0.6), "shock", "shock", O)], cx=330, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: marcador(im, T, u, y=620), t=0.0),
                   dict(k="calendar", seq=["EP. 1", "EP. 2", "EP. 3", "EP. 4"], x=800, y=1000, s=0.9, t=q(0, 0.2), t_end=(0, 0, 0.85))]), 0),
    ([3], A_app2(*FILTROS, "pabellon", callout=(0.62, 0.452, "DEPORTES", q(0, 0.45))), 0),
    ([4], A_preg2("¿HAIKYUU O KUROKO?", "pabellon", sub="SOLO UNO", logo=True), 1.4)])

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
