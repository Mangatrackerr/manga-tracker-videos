# Lote del 27/11/2026 (tarea diaria automática): 8 vídeos, cada uno con personaje, escenario, temática y animación distintos.
# Algo llamativo moviéndose desde el fotograma 0 + "punch" de cámara, gancho ≤ 8 palabras, pregunta final tipo "dilo tú" (revisión del 23/11).
# 4 de contenido + 4 con la app integrada, ya ordenados para alternar (30/11 14:30 app, 21:00 contenido; 01/12 al revés...).
# Escenarios nuevos: escenarios4.py. Personajes nuevos: looks.py (goro, rina, kenta, chiho, aya, sho, kana, yuto).
# Uso: python3 pipeline/satira/lote_2026-11-27z.py [chk] [tema ...]
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["SRC_VIDEO"] = os.path.abspath(os.path.join(HERE, "..", "..", "procesadas", "grabacion_2026-11-02.mp4"))
sys.path.insert(0, HERE)
from animado import *
import animado as AN, escenarios as EC, escenarios4 as EC4, voz_viva
from looks import LOOKS
EC4.instalar4(); voz_viva.patch(M)
M.SUBS += [("Naruto", "Narúto"), ("Freezer", "Fríser"), ("Namek", "Námek"), ("Saitama", "Saitáma"), ("spoiler", "espóiler"), ("hype", "jáip")]
ES.VOICE_CHAIN = "highpass=f=75,equalizer=f=3000:t=q:w=1.4:g=1.2,acompressor=threshold=0.15:ratio=2:attack=10:release=150,"
ES.MUSIC_VOL = 0.2
LOTE = "2026-11-27z"
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "videos"))
O = ("open", "open"); PR = ("fist", "point"); PL = ("point", "fist"); OR_ = ("fist", "open")
# clips de la grabación 2026-11-02 (ver README)
MILISTA = (90.1, 92.6); PERFIL = (129.45, 129.55); ESTRENOS = (1.2, 5.5); FICHA = (97.25, 97.35)

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



def _sh(c, k=0.75): return tuple(int(v * k) for v in c)


# ---------- props dibujados (lote 27z) ----------
def tira_pelicula(im, T, u, y=1180, sp=900, marcar=True):
    """tira de película que cruza a toda velocidad; los fotogramas de relleno van tachados en rojo"""
    d = ImageDraw.Draw(im); fw = 230; off = -(u * sp) % fw
    d.rectangle((0, y - 150, W, y + 150), fill=(28, 26, 32))
    for j in range(-1, W // fw + 2):
        x = j * fw + off; n = int((u * sp - off) // fw) + j
        for yy in (y - 135, y + 112):
            for k in range(5): d.rectangle((x + 14 + k * 44, yy, x + 40 + k * 44, yy + 22), fill=(240, 240, 235))
        relleno = marcar and (n * 7) % 5 in (1, 3)
        c = (90, 150, 220) if (n % 3) else (240, 180, 90)
        d.rectangle((x + 16, y - 100, x + fw - 16, y + 100), fill=(200, 70, 70) if relleno else c)
        d.ellipse((x + fw / 2 - 40, y - 60, x + fw / 2 + 40, y + 20), fill=(255, 255, 255, 200)); d.rectangle((x + fw / 2 - 60, y + 30, x + fw / 2 + 60, y + 80), fill=(255, 255, 255, 200))
        if relleno:
            d.line((x + 30, y - 85, x + fw - 30, y + 85), fill=(255, 255, 255), width=14); d.line((x + fw - 30, y - 85, x + 30, y + 85), fill=(255, 255, 255), width=14)


def tijeras(im, T, u, x=W / 2 + 200, y=1180):
    """tijeras que cortan la tira (se abren y cierran despacio)"""
    a = 0.35 * abs(math.sin(u * 3)); d = ImageDraw.Draw(im)
    for s in (-1, 1):
        ang = math.pi + s * a; ex = x + 260 * math.cos(ang); ey = y + 260 * math.sin(ang)
        d.line((x, y, ex, ey), fill=(210, 215, 225), width=26)
        hx = x + 120 * math.cos(ang + math.pi); hy = y + 120 * math.sin(ang + math.pi)
        d.ellipse((hx - 55, hy - 40 + s * 30, hx + 55, hy + 40 + s * 30), outline=(230, 60, 70), width=20)
    d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=(90, 90, 100))


def mazo(im, T, u, x=W / 2 + 230, y=1260):
    """mazo de juez que golpea (cada 1 s) y suelta ondas"""
    ph = (u * 1.0) % 1; up = ph > 0.18; ang = (-55 if up else 0) * (1 if ph < 0.18 else min(1, (ph - 0.18) / 0.3))
    d = ImageDraw.Draw(im); d.rounded_rectangle((x - 150, y + 40, x + 150, y + 90), radius=14, fill=(120, 70, 40))   # base
    r = math.radians(ang); hx, hy = x + 40, y - 10
    ex = hx + 220 * math.cos(math.pi + r); ey = hy + 220 * math.sin(math.pi + r)
    hd = Image.new("RGBA", (220, 120), (0, 0, 0, 0)); ImageDraw.Draw(hd).rounded_rectangle((0, 0, 220, 120), radius=24, fill=(150, 90, 50)); ImageDraw.Draw(hd).rectangle((40, 0, 60, 120), fill=(230, 190, 90)); ImageDraw.Draw(hd).rectangle((160, 0, 180, 120), fill=(230, 190, 90))
    d.line((hx, hy, ex + 300 * math.cos(math.pi + r) * 0 + 0, ey), fill=(110, 64, 34), width=22)
    paste_c(im, hd.rotate(-ang, expand=True), hx, hy - 10)
    if ph < 0.45:
        v = ph / 0.45
        for j in range(2):
            R = 60 + (v + j * 0.3) * 320; a_ = max(0, int(190 * (1 - v)))
            ov = _ov(im); ImageDraw.Draw(ov).ellipse((x - R, y + 60 - R * 0.28, x + R, y + 60 + R * 0.28), outline=(255, 240, 170, a_), width=10); im.alpha_composite(ov)


def hype_bar(im, T, u, x=840, y=1500, h=700):
    """medidor de HYPE que se dispara y se sale"""
    k = min(1.15, ease_out(min(1, u / 1.2)) * 1.15); d = ImageDraw.Draw(im)
    d.rounded_rectangle((x - 70, y - h, x + 70, y), radius=30, fill=(30, 26, 40), outline=(255, 255, 255), width=8)
    top = min(y - 17, y - h * min(1, k)); c = (80, 210, 120) if k < 0.6 else (250, 200, 50) if k < 0.95 else (240, 60, 70)
    d.rounded_rectangle((x - 54, top, x + 54, y - 16), radius=24, fill=c)
    if k >= 1: 
        for j in range(3): R = 40 + j * 30 + 8 * math.sin(T * 4 + j); d.ellipse((x - R, y - h - 40 - R * 0.5 - j * 30, x + R, y - h - 40 + R * 0.5 - j * 30), fill=(240, 60, 70))
    paste_c(im, text_img("HYPE", LG, 64, fill=WHITE, stroke=5), x, y + 50)


def cuenta_atras(im, T, u, x=W / 2, y=760, rate=0.08):
    """reloj de 5:00 que casi no avanza (los cinco minutos eternos)"""
    s = max(0, 300 - u * rate * 10); mm, ss = divmod(int(math.ceil(s)), 60)
    d = ImageDraw.Draw(im); d.rounded_rectangle((x - 300, y - 120, x + 300, y + 120), radius=26, fill=(20, 16, 22)); d.rounded_rectangle((x - 300, y - 120, x + 300, y + 120), radius=26, outline=(240, 60, 60), width=10)
    paste_c(im, text_img(f"{mm}:{ss:02d}", LG, 190, fill=(255, 80, 80), stroke=6), x, y + 10)


def aura(im, T, u, x=W / 2, y=1450, col=(255, 220, 90)):
    """aura de energía que late despacio alrededor del personaje"""
    s = 1 + 0.06 * math.sin(T * 3); glow(im, x, y, 360 * s, col, 90, 50)
    d = ImageDraw.Draw(im); rnd = random.Random(2)
    for j in range(16):
        a = rnd.uniform(0, 2 * math.pi); v = (u * 0.8 + j / 16) % 1; r = 200 + rnd.uniform(0, 140)
        px = x + r * math.cos(a); py = y + r * 1.3 * math.sin(a) - 500 * v
        d.line((px, py, px, py - 60), fill=col + (int(220 * (1 - v)),), width=8)


def planeta_grietas(im, T, u, x=W / 2, y=1700):
    """grietas que se abren en el suelo, con brillo lento"""
    d = ImageDraw.Draw(im); k = ease_out(min(1, u / 1.5)); a = int(160 + 60 * math.sin(T * 1.5))
    for s, (dx, dy) in enumerate(((-1, -0.3), (1, -0.2), (-0.6, 0.4), (0.7, 0.5))):
        pts = [(x, y)]; px, py = x, y
        for j in range(5):
            px += dx * 90 * k + (25 if j % 2 else -25); py += dy * 60 * k + (12 if j % 2 else -12); pts.append((px, py))
        d.line(pts, fill=(255, 150, 60, a), width=14, joint="curve")


def cajas(im, T, u, x=820, base=1800, n=6):
    """cajas de PENDIENTE que caen y se apilan"""
    d = ImageDraw.Draw(im)
    for j in range(n):
        t0 = j * 0.35; v = u - t0
        if v < 0: continue
        yf = base - j * 150; y = min(yf, -200 + 3000 * v * v); xx = x + (25 if j % 2 else -25)
        c = [(210, 165, 105), (195, 150, 95), (220, 175, 115)][j % 3]
        d.rectangle((xx - 130, y - 140, xx + 130, y), fill=c); d.rectangle((xx - 130, y - 140, xx + 130, y - 118), fill=_sh(c, 0.85)); d.rectangle((xx - 18, y - 140, xx + 18, y), fill=_sh(c, 1.12))
        paste_c(im, text_img("PENDIENTE", LG, 34, fill=(150, 40, 40)), xx, y - 60, rot=-6 if j % 2 else 5)


def folletos(im, T, u, n=8):
    """hojas de periódico/folletos genéricos que cruzan volando"""
    rnd = random.Random(11)
    for j in range(n):
        v = (u * 0.45 + j / n) % 1; y0 = rnd.uniform(500, 1600); x = -200 + (W + 400) * v; y = y0 + 120 * math.sin(v * 7 + j); rot = (u * 200 + j * 47) % 360
        pz = Image.new("RGBA", (170, 220), (0, 0, 0, 0)); dz = ImageDraw.Draw(pz); dz.rectangle((0, 0, 170, 220), fill=(248, 246, 236))
        dz.rectangle((14, 14, 156, 60), fill=[(230, 70, 80), (70, 140, 230), (250, 190, 50)][j % 3])
        for k in range(5): dz.line((14, 80 + k * 26, 156 - (k % 2) * 40, 80 + k * 26), fill=(150, 150, 160), width=6)
        paste_c(im, pz.rotate(rot, expand=True), x, y, 1.0)


def avisos(im, T, u):
    """burbujas de comentario con SPOILER que llegan"""
    txts = ["¡QUÉ FINAL!", "NO ME LO ESPERABA", "SPOILER:", "¿YA LO HABÉIS VISTO?"]
    for j, tx in enumerate(txts):
        t0 = j * 0.4
        if u < t0: continue
        paste_c(im, pill(tx, 50, fg=DARK, bg=WHITE if j != 2 else (255, 120, 120)), [700, 760, 690, 740][j], 900 + j * 160 - min(1, (u - t0)) * 40, pop(T, T - (u - t0), 0.25), rot=[-3, 3, -2, 2][j])


def trofeo(im, T, u, x=W / 2 + 230, y=1150):
    """copa dorada genérica que sube con brillo"""
    yy = y + (1 - ease_out(min(1, u / 0.6))) * 900 + 10 * math.sin(T * 2)
    glow(im, x, yy, 230, (255, 220, 110), 90, 45); d = ImageDraw.Draw(im); g = (250, 200, 60); g2 = (210, 160, 30)
    d.pieslice((x - 150, yy - 230, x + 150, yy + 70), 0, 180, fill=g); d.rectangle((x - 150, yy - 160, x + 150, yy - 80), fill=g)
    for s in (-1, 1): d.arc((x + s * 150 - 70, yy - 150, x + s * 150 + 70, yy - 10), 270 if s > 0 else 90, 90 if s > 0 else 270, fill=g2, width=22)
    d.rectangle((x - 25, yy + 70, x + 25, yy + 150), fill=g2); d.rounded_rectangle((x - 110, yy + 150, x + 110, yy + 200), radius=12, fill=g2)
    star(d, x, yy - 100, 40, (255, 255, 230))


def saco_volando(im, T, u, x0=W / 2 + 200, y0=1100):
    """saco de boxeo que sale disparado hacia el cielo tras un puñetazo"""
    k = min(1, u / 1.2); x = x0 + 500 * k; y = y0 - 1500 * ease_out(k); rot = -40 * k; d = ImageDraw.Draw(im)
    for j in range(7): d.line((x - 120 - j * 30, y + 200 + j * 40, x - 220 - j * 50, y + 380 + j * 60), fill=(255, 255, 255, 200), width=8)
    pz = Image.new("RGBA", (180, 380), (0, 0, 0, 0)); ImageDraw.Draw(pz).rounded_rectangle((10, 30, 170, 370), radius=60, fill=(200, 50, 50)); ImageDraw.Draw(pz).rectangle((60, 0, 120, 40), fill=(60, 60, 70))
    paste_c(im, pz.rotate(rot, expand=True), x, y, 1.0 - 0.5 * k)
    if u < 0.5:
        v = u / 0.5; R = 80 + 300 * v; ov = _ov(im); ImageDraw.Draw(ov).ellipse((x0 - R, y0 - R, x0 + R, y0 + R), outline=(255, 240, 160, int(220 * (1 - v))), width=14); im.alpha_composite(ov)


def bocetos(im, T, u, x=820, y=1160, pro=False):
    """hoja de dibujo: garabato sencillo o dibujo trabajado (personaje genérico, inventado)"""
    yy = y + (1 - ease_out(min(1, u / 0.45))) * 900 + 8 * math.sin(T * 2); d = ImageDraw.Draw(im)
    d.rectangle((x - 190, yy - 260, x + 190, yy + 260), fill=(252, 250, 244)); d.rectangle((x - 190, yy - 260, x + 190, yy + 260), outline=(190, 190, 200), width=4)
    if not pro:   # monigote de palos
        c = (60, 60, 70); d.ellipse((x - 50, yy - 190, x + 50, yy - 90), outline=c, width=7); d.line((x, yy - 90, x, yy + 80), fill=c, width=7)
        d.line((x - 90, yy - 30, x + 90, yy - 50), fill=c, width=7); d.line((x, yy + 80, x - 70, yy + 200), fill=c, width=7); d.line((x, yy + 80, x + 60, yy + 200), fill=c, width=7)
        d.ellipse((x - 25, yy - 155, x - 12, yy - 142), fill=c); d.ellipse((x + 12, yy - 155, x + 25, yy - 142), fill=c)
    else:         # figura sombreada con capa y líneas de acción
        d.polygon([(x - 40, yy - 80), (x + 40, yy - 80), (x + 150, yy + 220), (x - 150, yy + 220)], fill=(240, 240, 245), outline=(60, 60, 70), width=6)
        d.rounded_rectangle((x - 75, yy - 90, x + 75, yy + 120), radius=30, fill=(250, 210, 70), outline=(60, 60, 70), width=6)
        d.ellipse((x - 65, yy - 230, x + 65, yy - 90), fill=(250, 220, 190), outline=(60, 60, 70), width=6)
        d.rounded_rectangle((x - 70, yy - 20, x + 70, yy + 10), radius=10, fill=(60, 60, 70))
        d.ellipse((x + 80, yy - 160, x + 170, yy - 70), fill=(220, 60, 60), outline=(60, 60, 70), width=6)   # puño
        for j in range(5): d.line((x + 180, yy - 150 + j * 20, x + 185 + 0, yy - 150 + j * 20), fill=(60, 60, 70), width=4)
        for j in range(6): d.line((x - 180 + j * 20, yy + 240, x - 120 + j * 20, yy + 180), fill=(150, 150, 170), width=4)


def examen(im, T, u, x=820, y=1180, nota="6,8"):
    """hoja de examen con la nota en rojo"""
    yy = y + (1 - ease_out(min(1, u / 0.45))) * 900 + 8 * math.sin(T * 2); d = ImageDraw.Draw(im)
    d.rectangle((x - 200, yy - 270, x + 200, yy + 270), fill=(252, 252, 248))
    for k in range(8): d.line((x - 160, yy - 130 + k * 45, x + 160 - (k % 3) * 50, yy - 130 + k * 45), fill=(170, 180, 210), width=5)
    k = ease_out(clamp((u - 0.35) / 0.3))
    if k > 0:
        paste_c(im, text_img(nota, LG, 150, fill=(220, 40, 40)), x + 40, yy - 180, 0.5 + 0.5 * k, rot=-8)
        d = ImageDraw.Draw(im); d.ellipse((x - 120, yy - 290, x + 200, yy - 70), outline=(220, 40, 40), width=10)


def estrellas(im, T, u, x=W / 2, y=760, val=3.4):
    """cinco estrellas que se rellenan hasta val"""
    d = ImageDraw.Draw(im); f = val * ease_out(min(1, u / 1.0))
    for j in range(5):
        cx = x + (j - 2) * 150; star(d, cx, y, 62, (80, 70, 100))
        if f > j:
            fr = min(1, f - j); s = Image.new("RGBA", (140, 140), (0, 0, 0, 0)); star(ImageDraw.Draw(s), 70, 70, 62, YEL)
            s = s.crop((0, 0, int(8 + 124 * fr), 140)); im.alpha_composite(s, (int(cx - 70), int(y - 70)))


V = {}
# 1) ALDEA — Goro, voz st5, APP
V["01_relleno_naruto"] = ("goro", "st5", "lofi14", "app", [
    ("Te tragaste *noventa episodios* de relleno.", "Te tragaste… noventa episodios de relleno."),
    ("En *Naruto* clásico, unos *cuatro de cada diez* episodios son relleno.", "En Naruto clásico, unos cuatro de cada diez episodios… son relleno."),
    ("Historias que *no salen en el manga*… y tú, viéndolas *todas*.", "Historias que no salen en el manga… y tú, viéndolas todas."),
    ("En *Manga Tracker* apuntas el *episodio exacto*… y te lo saltas sin perderte.", "En Manga Tracker apuntas el episodio exacto… y te lo saltas sin perderte."),
    ("¿El peor relleno? Dilo tú.", "¿Cuál es el peor relleno que has visto? Dilo tú.")], [
    ([0], punch(A("aldea", [K(0.0, "shock", "shock", O), K(0.7, "point_r", "tired", PR)], cx=W / 2, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: tira_pelicula(im, T, u + 0.3, y=1240), t=0.0),
                   dict(k="big", txt="90 EPISODIOS", y=540, size=150, t=-0.12), dict(k="big", txt="DE RELLENO", y=690, size=140, t=0.05)])), 0),
    ([1], A("aldea", [K(0.0, "present", "proud", OR_), K(q(0, 0.6), "finger_up", "smug", PR)], cx=300, sc=0.88,
            props=[dict(k="grid", n=10, cols=5, y=690, dur=0.1, t=0.05), dict(k="draw", fn=lambda im, T, u: [ImageDraw.Draw(im).rounded_rectangle((W / 2 - 185 + c * 74, 690 + r * 74, W / 2 - 185 + c * 74 + 64, 690 + r * 74 + 64), radius=12, fill=RED) for j in range(min(4, int(u * 4))) for r, c in [divmod(j, 5)]], front=True, t=q(0, 0.35)),
                   dict(k="pill", txt="NARUTO CLÁSICO", y=570, t=0.05, rot=-3), dict(k="big", txt="4 DE CADA 10", y=940, size=120, t=q(0, 0.5))]), 0),
    ([2], A("aldea_noche", [K(0.0, "sit_phone", "tired"), K(q(0, 0.6), "sit_dizzy", "dizzy")], cx=330, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: tira_pelicula(im, T, u, y=1080, sp=300), t=0.0),
                   dict(k="stamp", txt="NO SALE EN EL MANGA", col=RED, t=q(0, 0.3), y=620, size=80)], fx=[dict(k="zzz", t=q(0, 0.6))]), 0),
    ([3], A_app2(*MILISTA, "aldea", callout=(0.09, 0.594, "EP. EXACTO", q(0, 0.45))), 0),
    ([4], A_preg2("¿EL PEOR RELLENO? DILO TÚ", "aldea", sub="TE LEO", logo=True), 1.4)])

# 2) TRIBUNAL — Rina, voz st4, CONTENIDO
V["02_anime_sobrevalorado"] = ("rina", "st4", "lofi15", "contenido", [
    ("Tu anime favorito está *sobrevalorado*.", "Tu anime favorito… está sobrevalorado."),
    ("Sí, ese… el que todo el mundo pone *por las nubes*.", "Sí, ese… el que todo el mundo pone por las nubes."),
    ("Lo empezaste por el *hype*… y a mitad *te aburriste*. Pero no lo dijiste.", "Lo empezaste por el hype… y a mitad, te aburriste. Pero no lo dijiste."),
    ("Hoy se abre el juicio: aquí se dice *sin miedo*.", "Hoy se abre el juicio… y aquí se dice sin miedo."),
    ("¿El más sobrevalorado? Dilo tú.", "¿Cuál es el anime más sobrevalorado? Dilo tú… sin miedo.")], [
    ([0], punch(A("tribunal", [K(0.0, "point_r", "smug", PR), K(0.8, "finger_up", "smug", PR)], cx=300, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: mazo(im, T, u + 0.82, x=800, y=1300), front=True, t=0.0),
                   dict(k="big", txt="SOBREVALORADO", y=600, size=130, t=-0.12)])), 0),
    ([1], A("tribunal", [K(0.0, "shrug", "smug", O), K(q(0, 0.5), "point_up_r", "happy", PR)], cx=330, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: hype_bar(im, T, u, x=830, y=1600), t=q(0, 0.1)),
                   dict(k="pill", txt="POR LAS NUBES", x=560, y=620, t=q(0, 0.4), rot=-3)], fx=[dict(k="stars", t=q(0, 0.5))]), 0),
    ([2], A("tribunal_noche", [K(0.0, "sit_phone", "happy"), K(q(0, 0.45), "sit_wait", "tired"), K(q(0, 0.8), "shrug", "confused", O)], cx=W / 2, sc=0.9,
            props=[dict(k="pill", txt="HYPE", y=580, t=0.05, rot=-4), dict(k="stamp", txt="ME ABURRÍ", col=RED, t=q(0, 0.45), y=760, size=110),
                   dict(k="pill", txt="(PERO NO LO DIJISTE)", y=920, bg=WHITE, t=q(0, 0.8), rot=3)], fx=[dict(k="zzz", t=q(0, 0.45))]), 0),
    ([3], A("tribunal", [K(0.0, "arms_up", "shock", O), K(q(0, 0.5), "point_r", "proud", PR)], cx=330, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: mazo(im, T, u + 0.82, x=820, y=1300), front=True, t=0.0),
                   dict(k="stamp", txt="SIN MIEDO", col=GREEN, t=q(0, 0.6), y=700, size=120)]), 0),
    ([4], A_preg2("¿EL MÁS SOBREVALORADO? DILO TÚ", "tribunal", sub="SIN MIEDO"), 1.4)])

# 3) PLANETA — Kenta, voz st5, CONTENIDO
V["03_namek_cinco_minutos"] = ("kenta", "st5", "lofi16", "contenido", [
    ("Cinco minutos que duraron *varios episodios*.", "Cinco minutos… que duraron varios episodios."),
    ("En *Dragon Ball Z*, *Freezer* avisa: *Namek* explota en *cinco minutos*.", "En Dragon Bol Zeta, Freezer avisa: Namek explota… en cinco minutos."),
    ("Y empieza la pelea: *gritos*, *transformaciones*, recuerdos…", "Y empieza la pelea: gritos, transformaciones, recuerdos…"),
    ("Y el planeta, *aguantando*… semana tras semana.", "Y el planeta, aguantando… semana tras semana."),
    ("¿Otra escena eterna? Dila tú.", "¿Qué otra escena se hizo eterna? Dila tú.")], [
    ([0], punch(A("planeta_rojo", [K(0.0, "shock", "shock", O), K(0.7, "point_up_r", "confused", PR)], cx=W / 2, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: planeta_grietas(im, T, u + 1.0, y=1760), t=0.0), dict(k="draw", fn=lambda im, T, u: cuenta_atras(im, T, u, y=820), t=0.0),
                   dict(k="big", txt="5 MINUTOS ETERNOS", y=560, size=115, t=-0.12)])), 0),
    ([1], A("planeta", [K(0.0, "present", "proud", OR_), K(q(0, 0.6), "finger_up", "smug", PR)], cx=300, sc=0.88,
            props=[dict(k="pill", txt="DRAGON BALL Z", x=760, y=600, t=0.05, rot=4), dict(k="pill", txt="NAMEK", x=760, y=740, bg=WHITE, t=q(0, 0.35), rot=-3),
                   dict(k="draw", fn=lambda im, T, u: cuenta_atras(im, T, 0, x=760, y=980), t=q(0, 0.6))]), 0),
    ([2], A("planeta_rojo", [K(0.0, "arms_up", "shock", O), K(q(0, 0.4), "stand", "smug"), K(q(0, 0.75), "arms_up", "proud", O)], cx=W / 2, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: aura(im, T, u, x=W / 2, y=1450), t=q(0, 0.3))], fx=[dict(k="sparkle", t=q(0, 0.3))]), 0),
    ([3], A("planeta_rojo", [K(0.0, "sit_wait", "tired"), K(q(0, 0.6), "shrug", "tired", O)], cx=330, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: cuenta_atras(im, T, u + 30, x=W / 2, y=620, rate=0.05), t=0.0),
                   dict(k="calendar", seq=["SEMANA 1", "SEMANA 2", "SEMANA 3"], x=800, y=1050, s=0.9, t=q(0, 0.15), t_end=(0, 0, 0.85))]), 0),
    ([4], A_preg2("¿OTRA ESCENA ETERNA? DILA TÚ", "planeta", sub="TE LEO"), 1.4)])

# 4) DESVÁN — Chiho, voz st0, APP
V["04_lista_pendientes"] = ("chiho", "st0", "lofi17", "app", [
    ("Tu lista de *pendientes* no tiene fondo.", "Tu lista de pendientes… no tiene fondo."),
    ("Cada vez que alguien te recomienda algo… *otra más*.", "Cada vez que alguien te recomienda algo… otra más."),
    ("Ya van *ochenta*… y sigues viendo *lo mismo de siempre*.", "Ya van ochenta… y sigues viendo lo mismo de siempre."),
    ("En *Manga Tracker* las tienes en *Planificado*… y eliges la siguiente en un segundo.", "En Manga Tracker las tienes en planificado… y eliges la siguiente, en un segundo."),
    ("¿Cuántas tienes? Di un número.", "¿Cuántas tienes pendientes? Di un número.")], [
    ([0], punch(A("desvan", [K(0.0, "shock", "shock", O), K(0.7, "scratch", "confused")], cx=300, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: cajas(im, T, u + 0.9, x=830), front=True, t=0.0),
                   dict(k="big", txt="NO TIENE FONDO", y=600, size=135, t=-0.12)])), 0),
    ([1], A("desvan", [K(0.0, "phone_stand", "happy"), K(q(0, 0.55), "phone_stand", "tired")], cx=330, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: cajas(im, T, u, x=830, n=4), t=0.0), dict(k="pill", txt="¡TIENES QUE VERLA!", x=560, y=620, bg=WHITE, t=0.05, rot=3),
                   dict(k="pill", txt="+1", x=560, y=760, t=q(0, 0.55), rot=-4)]), 0),
    ([2], A("desvan_noche", [K(0.0, "sit_phone", "tired"), K(q(0, 0.6), "sit_wait", "tired")], cx=W / 2, sc=0.9,
            props=[dict(k="counter", a=12, b=80, y=620, size=170, dur=1.0, t=0.05), dict(k="stamp", txt="LO DE SIEMPRE", col=RED, t=q(0, 0.6), y=820, size=100)]), 0),
    ([3], A_app2(*PERFIL, "desvan", mode="still", callout=(0.80, 0.577, "PLANIFICADO", q(0, 0.45))), 0),
    ([4], A_preg2("¿CUÁNTAS TIENES? DI UN NÚMERO", "desvan", sub="SÉ SINCERO", logo=True), 1.4)])

# 5) KIOSCO — Aya, voz st4, APP
V["05_estreno_no_te_enteraste"] = ("aya", "st4", "lofi18", "app", [
    ("Se estrenó tu anime… y *no te enteraste*.", "Se estrenó tu anime… y no te enteraste."),
    ("Tres semanas después… alguien te hace *spoiler* en los comentarios.", "Tres semanas después… alguien te hace spoiler en los comentarios."),
    ("Y tú: *¿cómo que ya ha salido?*", "Y tú: ¿cómo que ya ha salido?"),
    ("En *Manga Tracker* tienes los *próximos estrenos* de cada temporada.", "En Manga Tracker tienes los próximos estrenos… de cada temporada."),
    ("¿Qué estreno esperas? Dilo tú.", "¿Qué estreno estás esperando? Dilo tú.")], [
    ([0], punch(A("kiosco", [K(0.0, "phone_stand", "neutral"), K(0.6, "shock", "shock", O)], cx=300, sc=0.86,
            props=[dict(k="draw", fn=lambda im, T, u: folletos(im, T, u + 0.4), front=True, t=0.0),
                   dict(k="big", txt="¿NO TE ENTERASTE?", y=600, size=115, t=-0.12)])), 0),
    ([1], A("kiosco", [K(0.0, "phone_stand", "happy"), K(q(0, 0.55), "shock", "shock", O)], cx=300, sc=0.86,
            props=[dict(k="calendar", seq=["SEMANA 1", "SEMANA 2", "SEMANA 3"], x=780, y=640, s=0.8, t=0.05, t_end=(0, 0, 0.4)),
                   dict(k="draw", fn=lambda im, T, u: avisos(im, T, u), front=True, t=q(0, 0.45))]), 0),
    ([2], A("kiosco_noche", [K(0.0, "arms_up", "shock", O), K(q(0, 0.5), "scratch", "confused")], cx=W / 2, sc=0.9,
            props=[dict(k="big", txt="¿YA HA SALIDO?", y=620, size=130, t=0.05)], fx=[dict(k="qmarks", t=q(0, 0.4))]), 0),
    ([3], A_app2(*ESTRENOS, "kiosco", callout=(0.42, 0.082, "ESTRENOS", q(0, 0.4))), 0),
    ([4], A_preg2("¿QUÉ ESTRENO ESPERAS? DILO TÚ", "kiosco", sub="TE LEO", logo=True), 1.4)])

# 6) CUMBRE NEVADA — Sho, voz st5, CONTENIDO
V["06_ash_25_anos"] = ("sho", "st5", "lofi19", "contenido", [
    ("*Ash Ketchum* tardó *25 años* en ser campeón.", "Ash Kétchum tardó veinticinco años… en ser campeón."),
    ("Empezó en *1997* con diez años… y siguió teniendo *diez años*.", "Empezó en mil novecientos noventa y siete, con diez años… y siguió teniendo diez años."),
    ("Liga tras liga… *casi*, pero no.", "Liga tras liga… casi, pero no."),
    ("Hasta *2022*: por fin, *campeón mundial*. Y poco después… *se despidió*.", "Hasta dos mil veintidós: por fin, campeón mundial. Y poco después… se despidió."),
    ("¿Quién tarda más en ganar? Dilo tú.", "¿Qué protagonista tarda una eternidad en ganar? Dilo tú.")], [
    ([0], punch(A("nevada", [K(0.0, "run", "proud")], run_until=99, xmove=lambda T: -120 + 60 * T, cx=W / 2, sc=0.85,
            props=[dict(k="draw", fn=lambda im, T, u: trofeo(im, T, u, x=860, y=1150), front=False, t=0.0),
                   dict(k="big", txt="25 AÑOS", y=560, size=190, t=-0.12), dict(k="big", txt="PARA GANAR", y=720, size=130, t=0.05)])), 0),
    ([1], A("nevada", [K(0.0, "present", "proud", OR_), K(q(0, 0.6), "finger_up", "smug", PR)], cx=300, sc=0.88,
            props=[dict(k="counter", a=1990, b=1997, pre="", fmt="{:.0f}", y=600, size=150, dur=0.7, t=0.05),
                   dict(k="pill", txt="10 AÑOS", x=780, y=820, t=q(0, 0.3), rot=-3), dict(k="stamp", txt="SIEMPRE 10", col=RED, t=q(0, 0.7), y=1000, x=760, size=90)]), 0),
    ([2], A("nevada_alba", [K(0.0, "run", "proud"), K(q(0, 0.5), "fall", "cry"), K(q(0, 0.8), "dizzy", "dizzy")], cx=W / 2, sc=0.9,
            props=[dict(k="calendar", seq=["LIGA 1", "LIGA 2", "LIGA 3", "LIGA 4"], x=W / 2, y=640, s=0.85, t=0.05, t_end=(0, 0, 0.7)),
                   dict(k="stamp", txt="CASI", col=RED, t=q(0, 0.55), y=900, x=W / 2 + 220, size=120)]), 0),
    ([3], A("nevada_alba", [K(0.0, "arms_up", "happy", O), K(q(0, 0.65), "wave", "cry")], cx=330, sc=0.9, wave=True,
            props=[dict(k="draw", fn=lambda im, T, u: trofeo(im, T, u, x=820, y=1180), t=0.0), dict(k="counter", a=1997, b=2022, fmt="{:.0f}", y=600, size=160, dur=0.9, t=0.05),
                   dict(k="rain", kind="confetti", t=q(0, 0.3)), dict(k="pill", txt="SE DESPIDIÓ", x=560, y=800, bg=WHITE, t=q(0, 0.72), rot=3)]), 0),
    ([4], A_preg2("¿QUIÉN TARDA MÁS EN GANAR? DILO TÚ", "nevada", sub="TE LEO"), 1.4)])

# 7) GIMNASIO — Kana, voz st0, CONTENIDO
V["07_one_punch_webcomic"] = ("kana", "st0", "lofi20", "contenido", [
    ("El manga *One Punch Man* empezó siendo *casero*.", "El manga Wan Panch Man… empezó siendo casero."),
    ("Lo dibujaba su propio autor en internet… con trazos *muy sencillos*.", "Lo dibujaba su propio autor en internet… con trazos muy sencillos."),
    ("Se hizo tan viral que *Yusuke Murata* lo redibujó… y quedó *espectacular*.", "Se hizo tan viral, que Yusuke Muráta lo redibujó… y quedó espectacular."),
    ("Y aun así, hay quien dice que el original *tiene más gracia*.", "Y aun así… hay quien dice que el original tiene más gracia."),
    ("¿Quién gana a Saitama? Dilo tú.", "¿Quién podría ganar a Saitama? Dilo tú.")], [
    ([0], punch(A("gimnasio", [K(0.0, "point_r", "proud", PR), K(0.6, "arms_up", "happy", O)], cx=330, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: saco_volando(im, T, u + 0.15, x0=760, y0=1180), front=True, t=0.0),
                   dict(k="big", txt="EMPEZÓ CASERO", y=600, size=135, t=-0.12)])), 0),
    ([1], A("gimnasio", [K(0.0, "write", "happy"), K(q(0, 0.6), "present", "proud", OR_)], cx=300, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: bocetos(im, T, u, x=800, y=1200), t=0.05), dict(k="pill", txt="WEBCÓMIC", x=780, y=640, t=q(0, 0.3), rot=4),
                   dict(k="pill", txt="TRAZOS SENCILLOS", y=800, x=560, bg=WHITE, t=q(0, 0.7), rot=-3)]), 0),
    ([2], A("gimnasio_noche", [K(0.0, "point_r", "smug", PR), K(q(0, 0.6), "clap", "happy")], cx=280, sc=0.86,
            props=[dict(k="draw", fn=lambda im, T, u: bocetos(im, T, u, x=800, y=1200, pro=True), t=q(0, 0.3)), dict(k="pill", txt="YUSUKE MURATA", x=760, y=620, t=0.05, rot=4),
                   dict(k="stamp", txt="ESPECTACULAR", col=GREEN, t=q(0, 0.75), y=820, x=640, size=90)], fx=[dict(k="stars", t=q(0, 0.75))]), 0),
    ([3], A("gimnasio", [K(0.0, "shrug", "smug", O), K(q(0, 0.6), "finger_up", "wink", PR)], cx=W / 2, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: bocetos(im, T, u, x=250, y=1200), t=0.0), dict(k="draw", fn=lambda im, T, u: bocetos(im, T, u, x=850, y=1200, pro=True), t=0.0),
                   dict(k="big", txt="¿MÁS GRACIA?", y=640, size=130, t=q(0, 0.5))]), 0),
    ([4], A_preg2("¿QUIÉN GANA A SAITAMA? DILO TÚ", "gimnasio", sub="TE LEO"), 1.4)])

# 8) AULA — Yuto, voz st5, APP
V["08_nota_baja"] = ("yuto", "st5", "lofi5", "app", [
    ("Ese anime con *nota baja*… es *buenísimo*.", "Ese anime con nota baja… es buenísimo."),
    ("Lo dejaste pasar por un *seis y pico*… y te lo perdiste.", "Lo dejaste pasar por un seis y pico… y te lo perdiste."),
    ("La nota es la media de *miles de opiniones*… no *la tuya*.", "La nota es la media de miles de opiniones… no la tuya."),
    ("En *Manga Tracker* ves la *valoración*… y le pones *tu propia nota*.", "En Manga Tracker ves la valoración… y le pones tu propia nota."),
    ("¿Uno con nota baja que te encante?", "¿Qué anime con nota baja te encanta? Dilo tú.")], [
    ([0], punch(A("aula", [K(0.0, "shock", "shock", O), K(0.7, "point_r", "happy", PR)], cx=300, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: examen(im, T, u + 0.5, x=800, y=1200), front=True, t=0.0),
                   dict(k="big", txt="NOTA BAJA", y=540, size=160, t=-0.12), dict(k="big", txt="¿Y BUENÍSIMO?", y=700, size=120, t=0.05)])), 0),
    ([1], A("aula", [K(0.0, "phone_stand", "neutral"), K(q(0, 0.6), "shrug", "cry", O)], cx=330, sc=0.88,
            props=[dict(k="draw", fn=lambda im, T, u: estrellas(im, T, u, y=640, val=3.4), t=0.05),
                   dict(k="stamp", txt="TE LO PERDISTE", col=RED, t=q(0, 0.65), y=860, size=95)]), 0),
    ([2], A("aula_tarde", [K(0.0, "present", "proud", OR_), K(q(0, 0.6), "point_up_r", "smug", PR)], cx=W / 2, sc=0.9,
            props=[dict(k="draw", fn=lambda im, T, u: estrellas(im, T, u, y=960, val=3.4), t=0.05), dict(k="pill", txt="MILES DE OPINIONES", y=600, t=0.05, rot=-3),
                   dict(k="pill", txt="NO LA TUYA", y=760, bg=WHITE, t=q(0, 0.65), rot=3)]), 0),
    ([3], A_app2(*FICHA, "aula", mode="still", callout=(0.47, 0.316, "VALORACIÓN", q(0, 0.4))), 0),
    ([4], A_preg2("¿UNO CON NOTA BAJA QUE TE ENCANTE?", "aula", sub="DILO TÚ", logo=True), 1.4)])

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
