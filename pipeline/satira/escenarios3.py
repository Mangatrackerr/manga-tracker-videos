# Escenarios del lote 2026-11-21y: 8 sitios nuevos (uno por vídeo) + una variante de cada uno.
# Se registran en escenarios.SCEN con instalar3(). Todo dibujado aquí: sin imágenes, logos ni textos de marcas.
# Nada de destellos rápidos: lo que brilla lo hace con pulsos lentos.
import math, random
from PIL import Image, ImageDraw, ImageFilter
import escenarios as EC
from escenarios import BW2, BH2, _grad, _shade


def _sky(c1, c2, h):
    im = _grad(c1, c2, h=h); full = Image.new("RGBA", (BW2, BH2), (0, 0, 0, 255)); full.paste(im.crop((0, 0, BW2, h)), (0, 0)); return full


def _glow(im, x, y, r, col, a=90, blur=50):
    g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((x - r, y - r, x + r, y + r), fill=col + (a,))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))


def _stars(d, rnd, n, y1):
    for _ in range(n):
        x, y = rnd.uniform(0, BW2), rnd.uniform(0, y1); r = rnd.choice((1.5, 2, 3)); d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255))


# ---------------- 1. Ciudad del futuro (Doraemon) ----------------
def _futuro(night=False):
    im = _sky(*(((20, 20, 70), (90, 50, 140)) if night else ((120, 220, 255), (230, 250, 255))), 1330)
    d = ImageDraw.Draw(im); rnd = random.Random(31)
    if night: _stars(d, rnd, 60, 700)
    else:
        for k in range(4): x = 100 + k * 300; d.ellipse((x, 220 + k * 40, x + 260, 300 + k * 40), fill=(255, 255, 255))
    for k in range(9):   # torres redondeadas
        x = -40 + k * 150 + rnd.randint(-15, 15); h = rnd.randint(500, 900); w = rnd.randint(100, 140)
        c = (70, 80, 150) if night else (200, 215, 240); d.rounded_rectangle((x, 1300 - h, x + w, 1320), radius=50, fill=c)
        d.ellipse((x - 20, 1300 - h - 30, x + w + 20, 1300 - h + 40), fill=_shade(c, 0.85))
        for yy in range(1300 - h + 70, 1280, 70):
            d.rounded_rectangle((x + 18, yy, x + w - 18, yy + 26), radius=13, fill=(255, 220, 120) if night else (150, 200, 240))
    for y, c in ((980, (240, 240, 250)), (1160, (220, 225, 240))):   # tubos elevados
        d.rounded_rectangle((-20, y, BW2 + 20, y + 50), radius=25, fill=c if not night else _shade(c, 0.5))
        for x in range(60, BW2, 260): d.rectangle((x, y + 50, x + 24, 1320), fill=(180, 185, 200) if not night else (60, 60, 90))
    d.rectangle((0, 1320, BW2, BH2), fill=(170, 180, 200) if not night else (40, 40, 70))
    for k in range(0, BW2, 120): d.line((k, 1320, k - 200, BH2), fill=(150, 160, 185) if not night else (55, 55, 90), width=4)
    d.ellipse((240, 1600, 960, 1760), fill=(200, 210, 230) if not night else (60, 60, 100))   # plataforma redonda
    return im


def _futuro_amb(im, T, ox, oy, night=False):
    d = ImageDraw.Draw(im)
    for k in range(5):   # coches voladores (cápsulas) cruzando
        sp = 140 + k * 40; y = 520 + k * 120 + 12 * math.sin(T * 2 + k) - oy
        x = ((T * sp + k * 330) % (BW2 + 400)) - 200 - ox
        if k % 2: x = BW2 - x - 200
        c = [(255, 110, 120), (255, 210, 80), (120, 230, 170), (180, 140, 255), (110, 190, 255)][k]
        d.rounded_rectangle((x - 70, y - 26, x + 70, y + 26), radius=26, fill=c); d.rounded_rectangle((x - 30, y - 44, x + 40, y - 10), radius=18, fill=(220, 245, 255))
        d.ellipse((x - 60, y + 22, x + 60, y + 40), fill=(255, 255, 255, 90))
    if night:
        for k in range(6):
            a = int(60 + 50 * math.sin(T * 1.1 + k)); x = 100 + k * 190 - ox
            d.rectangle((x, 1300 - oy, x + 120, 1312 - oy), fill=(120, 240, 255, a))


# ---------------- 2. Campo de fútbol infinito (Oliver y Benji) ----------------
def _campo(night=False):
    im = _sky(*(((10, 14, 40), (40, 40, 90)) if night else ((110, 190, 255), (210, 240, 255))), 900)
    d = ImageDraw.Draw(im); rnd = random.Random(42)
    if night: _stars(d, rnd, 40, 500)
    # grada lejana con público (puntitos)
    d.polygon([(0, 900), (BW2, 900), (BW2, 760), (0, 760)], fill=(70, 60, 90) if not night else (30, 26, 50))
    for _ in range(500):
        x, y = rnd.uniform(0, BW2), rnd.uniform(770, 895); d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=rnd.choice([(250, 90, 90), (255, 255, 255), (80, 140, 250), (250, 210, 70)]))
    # césped a rayas en perspectiva hasta el horizonte (el campo "que no se acaba")
    g1, g2 = ((50, 150, 60), (70, 175, 75)) if not night else ((30, 100, 45), (40, 120, 55))
    hz = 900
    for j in range(16):
        y0 = hz + (BH2 - hz) * (j / 16) ** 2; y1 = hz + (BH2 - hz) * ((j + 1) / 16) ** 2
        d.rectangle((0, y0, BW2, y1 + 1), fill=g1 if j % 2 else g2)
    cx = BW2 / 2
    for sx in (-1, 1): d.line((cx + sx * 40, hz, cx + sx * 900, BH2), fill=(245, 245, 245), width=8)   # bandas que convergen
    d.line((cx, hz, cx, BH2), fill=(245, 245, 245), width=6)
    d.ellipse((cx - 330, 1500, cx + 330, 1760), outline=(245, 245, 245), width=8)
    # portería lejana diminuta en el horizonte
    d.rectangle((cx - 30, hz - 22, cx + 30, hz), outline=(255, 255, 255), width=3)
    if night:
        for x in (120, BW2 - 120):
            d.rectangle((x - 8, 300, x + 8, 780), fill=(90, 90, 110)); d.rectangle((x - 70, 260, x + 70, 320), fill=(230, 230, 240))
    return im


def _campo_amb(im, T, ox, oy, night=False):
    d = ImageDraw.Draw(im)
    if night:
        for k, x in enumerate((120, BW2 - 120)):   # haces de los focos, oscilan despacio
            a = 0.18 * math.sin(T * 0.6 + k * 2); xs = x - ox; ys = 290 - oy
            d.polygon([(xs - 50, ys), (xs + 50, ys), (xs + 600 * math.sin(a) + (300 if k == 0 else -300), 1700 - oy), (xs + 600 * math.sin(a) + (-100 if k == 0 else 100), 1700 - oy)], fill=(255, 255, 220, 30))
    else:
        for k in range(3):
            x = (T * 25 + k * 420) % (BW2 + 300) - 150 - ox; y = 150 + k * 110 - oy
            d.ellipse((x, y, x + 240, y + 70), fill=(255, 255, 255, 200)); d.ellipse((x + 60, y - 30, x + 180, y + 50), fill=(255, 255, 255, 200))
    # banderín de córner ondeando
    x = 70 - ox; y = 1700 - oy; d.line((x, y, x, y - 220), fill=(240, 240, 240), width=7)
    w = 18 * math.sin(T * 5); d.polygon([(x, y - 220), (x + 90, y - 200 + w), (x, y - 160)], fill=(250, 220, 60))


# ---------------- 3. Despacho de detective + calle con niebla (Conan) ----------------
def _despacho():
    im = _grad((90, 60, 46), (60, 40, 32)); d = ImageDraw.Draw(im)
    for x in range(0, BW2, 90): d.line((x, 0, x, 1500), fill=(80, 52, 40), width=4)   # tablas de la pared
    d.rectangle((560, 260, 1080, 900), fill=(30, 40, 70)); d.rectangle((560, 260, 1080, 900), outline=(130, 90, 60), width=22)
    d.line((820, 260, 820, 900), fill=(130, 90, 60), width=14); d.line((560, 580, 1080, 580), fill=(130, 90, 60), width=14)
    rnd = random.Random(7)
    for k in range(6):   # edificios por la ventana
        x = 575 + k * 85; h = rnd.randint(140, 300); d.rectangle((x, 885 - h, x + 70, 885), fill=(50, 60, 95))
        for yy in range(900 - h, 870, 40):
            if rnd.random() < 0.5: d.rectangle((x + 15, yy, x + 30, yy + 18), fill=(255, 220, 140))
    # tablón de corcho con fotos y hilo rojo
    d.rectangle((70, 300, 470, 720), fill=(190, 140, 90)); d.rectangle((70, 300, 470, 720), outline=(110, 74, 50), width=14)
    pins = [(140, 380), (380, 360), (260, 520), (130, 640), (400, 640)]
    for (x, y) in pins: d.rectangle((x - 50, y - 36, x + 50, y + 50), fill=(245, 240, 225)); d.rectangle((x - 40, y - 26, x + 40, y + 30), fill=(150, 160, 175))
    for a, b in ((0, 2), (1, 2), (2, 3), (2, 4), (0, 1)): d.line((pins[a], pins[b]), fill=(210, 40, 40), width=5)
    for (x, y) in pins: d.ellipse((x - 9, y - 45, x + 9, y - 27), fill=(220, 50, 50))
    # perchero con sombrero
    d.rectangle((40, 760, 54, 1560), fill=(70, 44, 30)); d.ellipse((0, 740, 110, 790), fill=(90, 70, 50)); d.ellipse((-10, 715, 120, 760), fill=(110, 90, 66))
    d.rectangle((0, 1500, BW2, BH2), fill=(70, 44, 34))   # suelo
    for x in range(0, BW2, 140): d.line((x, 1500, x - 60, BH2), fill=(60, 38, 30), width=5)
    # escritorio con lámpara
    d.rectangle((640, 1240, 1120, 1300), fill=(120, 74, 44)); d.rectangle((670, 1300, 720, 1560), fill=(100, 60, 36)); d.rectangle((1040, 1300, 1090, 1560), fill=(100, 60, 36))
    d.rectangle((900, 1110, 914, 1240), fill=(40, 90, 60)); d.chord((830, 1060, 990, 1160), 180, 360, fill=(40, 120, 70)); d.rectangle((860, 1220, 960, 1240), fill=(40, 90, 60))
    d.rectangle((700, 1200, 820, 1240), fill=(240, 236, 220))   # papeles
    _glow(im, 910, 1200, 200, (255, 230, 150), 70, 60)
    return im


def _despacho_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im); rnd = random.Random(5)
    for k in range(40):   # lluvia en la ventana
        x = 575 + rnd.uniform(0, 490) - ox; y = (rnd.uniform(0, 640) + T * 700) % 640 + 260 - oy
        d.line((x, y, x - 6, y + 34), fill=(170, 190, 230, 150), width=3)
    a = T * 2.2; cx, cy = 300 - ox, 120 - oy   # ventilador de techo
    d.line((cx, -oy, cx, cy), fill=(60, 40, 30), width=8)
    for j in range(4):
        b = a + j * math.pi / 2; d.line((cx, cy, cx + 200 * math.cos(b), cy + 26 * math.sin(b)), fill=(90, 60, 40), width=22)
    d.ellipse((cx - 22, cy - 16, cx + 22, cy + 16), fill=(60, 40, 30))


def _niebla():
    im = _grad((26, 28, 46), (60, 64, 84)); d = ImageDraw.Draw(im); rnd = random.Random(19)
    d.ellipse((800, 180, 940, 320), fill=(235, 235, 220))
    x = -20
    while x < BW2:   # casas de ladrillo
        bw = rnd.randint(200, 280); bh = rnd.randint(700, 1000); c = (110 + rnd.randint(0, 20), 54, 44)
        d.rectangle((x, 1450 - bh, x + bw, 1450), fill=c)
        for yy in range(1450 - bh, 1450, 24): d.line((x, yy, x + bw, yy), fill=_shade(c, 0.85), width=2)
        for yy in range(1450 - bh + 60, 1350, 170):
            for xx in (x + 40, x + bw - 100):
                d.rectangle((xx, yy, xx + 60, yy + 100), fill=(255, 210, 130) if rnd.random() < 0.4 else (40, 40, 60)); d.rectangle((xx - 6, yy + 100, xx + 66, yy + 110), fill=(200, 200, 200))
        d.rectangle((x + bw / 2 - 20, 1450 - bh - 60, x + bw / 2 + 20, 1450 - bh), fill=_shade(c, 0.7))
        x += bw + 4
    d.rectangle((0, 1450, BW2, 1520), fill=(110, 110, 120)); d.rectangle((0, 1520, BW2, BH2), fill=(60, 60, 70))
    for yy in range(1540, BH2, 50):
        for xx in range((yy // 50) % 2 * 40, BW2, 80): d.rounded_rectangle((xx, yy, xx + 74, yy + 44), radius=8, fill=(72, 72, 82))
    d.rectangle((880, 900, 900, 1500), fill=(30, 30, 36)); d.polygon([(850, 860), (930, 860), (915, 920), (865, 920)], fill=(255, 230, 160))
    _glow(im, 890, 890, 180, (255, 220, 150), 90, 50)
    return im


def _niebla_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    for k in range(5):   # bancos de niebla que se deslizan
        x = (T * (30 + k * 8) + k * 300) % (BW2 + 800) - 600 - ox; y = 1000 + k * 170 - oy
        d.ellipse((x, y, x + 900, y + 260), fill=(220, 225, 235, 38))


# ---------------- 4. Huerto de manzanos (Ryuk) ----------------
def _huerto(night=False):
    im = _sky(*(((14, 12, 34), (50, 36, 80)) if night else ((255, 200, 140), (255, 235, 200))), 1150)
    d = ImageDraw.Draw(im); rnd = random.Random(55)
    if night: _stars(d, rnd, 50, 700); d.ellipse((160, 180, 330, 350), fill=(250, 245, 220))
    else: d.ellipse((780, 300, 960, 480), fill=(255, 245, 200))
    hill = (60, 110, 60) if not night else (26, 46, 36)
    d.polygon([(0, 1150)] + [(x, 1050 - 60 * math.sin(x / 260)) for x in range(0, BW2 + 20, 20)] + [(BW2, 1150)], fill=_shade(hill, 1.1))
    d.rectangle((0, 1150, BW2, BH2), fill=hill)
    for k, (x, y, s) in enumerate([(160, 1250, 1.0), (520, 1120, 0.7), (930, 1260, 1.05), (760, 1080, 0.55), (330, 1060, 0.5)]):
        tr = (100, 66, 40) if not night else (50, 34, 26); lf = (60, 140, 60) if not night else (30, 66, 44)
        d.rectangle((x - 22 * s, y - 260 * s, x + 22 * s, y), fill=tr)
        for j in range(5):
            a = j * 1.26; d.ellipse((x + 110 * s * math.cos(a) - 140 * s, y - 380 * s + 70 * s * math.sin(a) - 120 * s, x + 110 * s * math.cos(a) + 140 * s, y - 380 * s + 70 * s * math.sin(a) + 120 * s), fill=_shade(lf, 0.9 + 0.05 * j))
        for j in range(9):
            ax = x + rnd.uniform(-200, 200) * s; ay = y - 380 * s + rnd.uniform(-150, 120) * s; r = 18 * s
            d.ellipse((ax - r, ay - r, ax + r, ay + r), fill=(220, 40, 50) if not night else (140, 30, 40))
    for x in range(0, BW2, 110):   # valla
        d.rectangle((x, 1400, x + 24, 1560), fill=(200, 170, 120) if not night else (80, 70, 60))
    d.rectangle((0, 1440, BW2, 1460), fill=(190, 160, 110) if not night else (75, 65, 55)); d.rectangle((0, 1510, BW2, 1530), fill=(190, 160, 110) if not night else (75, 65, 55))
    return im


def _huerto_amb(im, T, ox, oy, night=False):
    d = ImageDraw.Draw(im); rnd = random.Random(8)
    if night:
        for k in range(4):   # cuervos volando despacio
            x = (T * (70 + k * 20) + k * 330) % (BW2 + 300) - 150 - ox; y = 400 + k * 90 + 20 * math.sin(T * 2 + k) - oy; f = 22 * math.sin(T * 7 + k)
            d.polygon([(x - 50, y - f), (x, y), (x + 50, y - f), (x, y + 14)], fill=(10, 8, 16))
    for k in range(10):   # hojas cayendo
        x = rnd.uniform(0, BW2) + 60 * math.sin(T * 1.2 + k) - ox; y = (rnd.uniform(0, 1800) + T * 90) % 1800 + 300 - oy
        d.ellipse((x - 12, y - 6, x + 12, y + 6), fill=(90, 160, 70) if not night else (60, 90, 60))


# ---------------- 5. Lavandería (en pausa / abandonado) ----------------
def _lavanderia(night=False):
    im = _grad((200, 225, 230), (170, 200, 210)) if not night else _grad((40, 50, 80), (24, 30, 54)); d = ImageDraw.Draw(im)
    for y in range(0, 1100, 80):   # azulejos
        for x in range(0, BW2, 80): d.rectangle((x, y, x + 78, y + 78), outline=(180, 205, 212) if not night else (34, 44, 70), width=2)
    if night:
        d.rounded_rectangle((420, 150, 780, 300), radius=30, outline=(255, 120, 200), width=12)
    else:
        d.rectangle((420, 150, 780, 300), fill=(250, 250, 250)); d.rectangle((420, 150, 780, 300), outline=(140, 160, 170), width=8)
    for k in range(4):   # lavadoras
        x = 30 + k * 290
        d.rounded_rectangle((x, 620, x + 270, 1200), radius=26, fill=(245, 248, 250) if not night else (190, 196, 210))
        d.rectangle((x, 620, x + 270, 700), fill=(220, 226, 232) if not night else (160, 166, 182))
        for j in range(3): d.ellipse((x + 30 + j * 50, 645, x + 60 + j * 50, 675), fill=(120, 130, 150))
        d.ellipse((x + 35, 780, x + 235, 980), fill=(120, 130, 150)); d.ellipse((x + 55, 800, x + 215, 960), fill=(150, 200, 230) if not night else (70, 100, 150))
    d.rectangle((0, 1200, BW2, 1260), fill=(120, 140, 150) if not night else (50, 56, 80))
    d.rectangle((0, 1260, BW2, BH2), fill=(230, 230, 225) if not night else (60, 60, 76))
    for y in range(1260, BH2, 90):
        for x in range((y // 90) % 2 * 90, BW2, 180): d.rectangle((x, y, x + 90, y + 90), fill=(200, 200, 195) if not night else (48, 48, 62))
    # cesta de ropa
    d.rounded_rectangle((850, 1420, 1080, 1600), radius=20, fill=(120, 170, 220)); d.ellipse((860, 1380, 1070, 1450), fill=(250, 120, 140)); d.ellipse((900, 1360, 1010, 1420), fill=(255, 220, 90))
    return im


def _lavanderia_amb(im, T, ox, oy, night=False):
    d = ImageDraw.Draw(im)
    for k in range(4):   # la ropa da vueltas dentro de cada tambor
        cx = 30 + k * 290 + 135 - ox; cy = 880 - oy; sp = 2.2 + 0.4 * k if k != 2 else 0.0   # una lavadora parada: "en pausa"
        for j in range(3):
            a = T * sp + j * 2.1; x = cx + 45 * math.cos(a); y = cy + 45 * math.sin(a)
            d.ellipse((x - 30, y - 22, x + 30, y + 22), fill=[(250, 110, 130, 220), (255, 220, 90, 220), (120, 210, 150, 220)][j])
        d.ellipse((cx - 80, cy - 80, cx - 20, cy - 40), fill=(255, 255, 255, 70))
    if night:
        a = int(90 + 60 * math.sin(T * 0.9)); d.rounded_rectangle((430 - ox, 160 - oy, 770 - ox, 290 - oy), radius=26, fill=(255, 120, 200, a // 3))


# ---------------- 6. Pizzería (lista para un amigo) ----------------
def _pizzeria(night=False):
    im = _grad((240, 220, 190), (220, 196, 160)) if not night else _grad((70, 46, 40), (44, 28, 26)); d = ImageDraw.Draw(im)
    br = (180, 90, 60) if not night else (110, 56, 40)
    for y in range(0, 1150, 46):   # pared de ladrillo
        for x in range(-((y // 46) % 2) * 60, BW2, 120): d.rectangle((x + 4, y + 4, x + 116, y + 42), fill=_shade(br, 0.9 + 0.1 * ((x + y) % 3) / 2))
    # horno de leña
    d.chord((560, 380, 1100, 1000), 180, 360, fill=(150, 150, 160) if not night else (90, 90, 100)); d.rectangle((560, 690, 1100, 1150), fill=(150, 150, 160) if not night else (90, 90, 100))
    d.chord((700, 560, 960, 900), 180, 360, fill=(40, 24, 20)); d.rectangle((700, 730, 960, 860), fill=(40, 24, 20))
    # pizarra de menú (dibujos, sin texto)
    d.rectangle((60, 300, 440, 700), fill=(40, 46, 44)); d.rectangle((60, 300, 440, 700), outline=(150, 100, 60), width=16)
    for j in range(3): d.ellipse((100, 350 + j * 110, 180, 430 + j * 110), outline=(250, 250, 240), width=5); d.line((210, 390 + j * 110, 400, 390 + j * 110), fill=(250, 250, 240), width=6)
    d.rectangle((0, 1150, BW2, 1180), fill=(120, 70, 40))
    d.rectangle((0, 1180, BW2, BH2), fill=(150, 100, 70) if not night else (80, 54, 40))
    for x in range(0, BW2, 130): d.line((x, 1180, x - 80, BH2), fill=_shade((150, 100, 70) if not night else (80, 54, 40), 0.85), width=5)
    # mesa con mantel de cuadros
    x0, x1, y0 = 80, 520, 1360
    d.rectangle((x0, y0, x1, y0 + 160), fill=(250, 250, 250))
    for j in range(0, x1 - x0, 44):
        for i in range(0, 160, 40):
            if (j // 44 + i // 40) % 2: d.rectangle((x0 + j, y0 + i, x0 + j + 44, y0 + i + 40), fill=(220, 50, 50))
    d.rectangle((140, y0 + 160, 170, 1640), fill=(90, 60, 40)); d.rectangle((430, y0 + 160, 460, 1640), fill=(90, 60, 40))
    d.ellipse((190, y0 - 30, 410, y0 + 40), fill=(240, 190, 90)); d.ellipse((205, y0 - 22, 395, y0 + 32), fill=(230, 90, 60))   # pizza
    for (px, py) in ((250, y0), (300, y0 - 10), (350, y0 + 6), (290, y0 + 14)): d.ellipse((px - 12, py - 8, px + 12, py + 8), fill=(170, 40, 40))
    if night:
        d.rectangle((0, 0, BW2, 260), fill=(30, 30, 60))
        for k in range(5): d.line((k * 260 + 130, 0, k * 260 + 130, 120), fill=(40, 40, 40), width=4); d.ellipse((k * 260 + 100, 110, k * 260 + 160, 170), fill=(255, 220, 140))
    return im


def _pizzeria_amb(im, T, ox, oy, night=False):
    d = ImageDraw.Draw(im)
    cx, cy = 830 - ox, 800 - oy   # fuego del horno, oscila despacio
    for j in range(5):
        h = 70 + 30 * math.sin(T * 3 + j * 1.3); x = cx - 90 + j * 45
        d.polygon([(x - 26, cy + 50), (x + 26, cy + 50), (x, cy + 50 - h)], fill=[(255, 150, 40, 230), (255, 210, 70, 230)][j % 2])
    for k in range(3):   # vapor de la pizza
        v = (T * 0.35 + k / 3) % 1; x = 300 + 30 * math.sin(T * 1.5 + k) + (k - 1) * 50 - ox; y = 1330 - 220 * v - oy
        d.ellipse((x - 20, y - 20, x + 20, y + 20), fill=(255, 255, 255, int(110 * (1 - v))))
    if night:
        for k in range(5): a = int(40 + 30 * math.sin(T * 0.8 + k)); x = k * 260 + 130 - ox; _ = d.ellipse((x - 70, 70 - oy, x + 70, 210 - oy), fill=(255, 220, 140, a))


# ---------------- 7. Pabellón de voleibol (deportes) ----------------
def _pabellon(empty=False):
    im = _grad((70, 80, 110), (110, 120, 150)) if not empty else _grad((20, 22, 36), (40, 42, 60)); d = ImageDraw.Draw(im)
    for k in range(4):   # gradas
        y = 560 + k * 90; d.rectangle((0, y, BW2, y + 80), fill=_shade((180, 60, 70) if not empty else (70, 30, 40), 1 - 0.08 * k))
    rnd = random.Random(3)
    if not empty:
        for _ in range(160):
            x, y = rnd.uniform(0, BW2), rnd.uniform(560, 900); d.ellipse((x - 9, y - 18, x + 9, y + 4), fill=rnd.choice([(250, 220, 190), (200, 150, 110), (120, 80, 60)]))
    for x in range(100, BW2, 330): d.rectangle((x, 80, x + 160, 110), fill=(250, 250, 240) if not empty else (90, 90, 100))   # focos del techo
    d.rectangle((0, 920, BW2, BH2), fill=(220, 160, 90) if not empty else (110, 80, 50))   # parqué
    for y in range(920, BH2, 60): d.line((0, y, BW2, y), fill=(200, 140, 75) if not empty else (95, 68, 42), width=3)
    d.line((0, 1400, BW2, 1400), fill=(250, 250, 250), width=10); d.line((BW2 / 2, 920, BW2 / 2, BH2), fill=(250, 250, 250), width=8)
    d.rectangle((0, 1700, BW2, 1720), fill=(60, 110, 200))
    # red en el centro (al fondo)
    nx = BW2 / 2
    d.rectangle((nx - 520, 920, nx - 500, 1100), fill=(200, 200, 210)); d.rectangle((nx + 500, 920, nx + 520, 1100), fill=(200, 200, 210))
    d.rectangle((nx - 500, 900, nx + 500, 990), fill=(30, 30, 40, 255))
    for x in range(int(nx - 500), int(nx + 500), 26): d.line((x, 900, x, 990), fill=(200, 200, 210), width=2)
    for y in range(900, 990, 22): d.line((nx - 500, y, nx + 500, y), fill=(200, 200, 210), width=2)
    d.rectangle((nx - 500, 896, nx + 500, 910), fill=(250, 250, 250))
    return im


def _pabellon_amb(im, T, ox, oy, empty=False):
    d = ImageDraw.Draw(im)
    if empty:   # un solo foco que se mueve despacio
        x = 600 + 260 * math.sin(T * 0.5) - ox
        d.polygon([(x - 40, -oy), (x + 40, -oy), (x + 300, 1900 - oy), (x - 300, 1900 - oy)], fill=(255, 250, 220, 28)); return
    v = (T * 0.55) % 1; x = 200 + 800 * v - ox; y = 820 - 420 * 4 * v * (1 - v) - oy   # pelota cruzando la red en parábola
    if (int(T * 0.55)) % 2: x = BW2 - x - 2 * ox
    d.ellipse((x - 34, y - 34, x + 34, y + 34), fill=(250, 250, 250)); d.arc((x - 34, y - 34, x + 34, y + 34), 200, 340, fill=(60, 110, 220), width=8)
    d.arc((x - 34, y - 34, x + 34, y + 34), 20, 160, fill=(250, 210, 60), width=8)


# ---------------- 8. Parque de cerezos (shojo) ----------------
def _sakura(night=False):
    im = _sky(*(((24, 20, 60), (80, 50, 110)) if night else ((170, 220, 255), (255, 230, 240))), 1150)
    d = ImageDraw.Draw(im); rnd = random.Random(77)
    if night: _stars(d, rnd, 50, 700); d.ellipse((820, 160, 960, 300), fill=(255, 245, 225))
    d.rectangle((0, 1150, BW2, BH2), fill=(120, 190, 110) if not night else (40, 70, 60))
    d.polygon([(500, 1150), (700, 1150), (1100, BH2), (100, BH2)], fill=(230, 210, 180) if not night else (90, 80, 90))   # camino
    pk = (255, 180, 205) if not night else (200, 130, 170)
    for (x, y, s) in [(140, 1350, 1.1), (1020, 1380, 1.15), (380, 1160, 0.6), (820, 1170, 0.65)]:
        d.polygon([(x - 26 * s, y), (x + 26 * s, y), (x + 12 * s, y - 330 * s), (x - 12 * s, y - 330 * s)], fill=(110, 70, 60) if not night else (60, 40, 40))
        for j in range(14):
            a = rnd.uniform(0, math.pi * 2); r = rnd.uniform(0, 210) * s; cx = x + r * math.cos(a); cy = y - 420 * s + r * 0.6 * math.sin(a)
            rr = rnd.uniform(90, 140) * s; d.ellipse((cx - rr, cy - rr * 0.8, cx + rr, cy + rr * 0.8), fill=_shade(pk, rnd.uniform(0.92, 1.05)))
    # banco
    d.rectangle((640, 1480, 1000, 1510), fill=(150, 100, 60)); d.rectangle((640, 1420, 1000, 1445), fill=(150, 100, 60)); d.rectangle((660, 1510, 680, 1600), fill=(60, 60, 70)); d.rectangle((960, 1510, 980, 1600), fill=(60, 60, 70))
    if night:
        for x in (300, 900):   # farolillos
            d.line((x, 1150, x, 900), fill=(60, 50, 60), width=10); d.ellipse((x - 40, 840, x + 40, 930), fill=(255, 150, 90)); _glow(im, x, 885, 120, (255, 170, 100), 90, 40)
    return im


def _sakura_amb(im, T, ox, oy, night=False):
    d = ImageDraw.Draw(im); rnd = random.Random(12)
    for k in range(34):   # pétalos que caen girando
        x = rnd.uniform(-100, BW2) + 80 * math.sin(T * 1.1 + k) + T * 40 % 200 - ox; y = (rnd.uniform(0, 2000) + T * (80 + k % 5 * 15)) % 2000 - oy
        f = abs(math.sin(T * 3 + k)); d.ellipse((x - 12, y - 7 * f - 2, x + 12, y + 7 * f + 2), fill=(255, 200, 220, 230) if not night else (230, 170, 210, 220))


NUEVOS3 = {
    "futuro": (lambda: _futuro(False), lambda im, T, ox, oy: _futuro_amb(im, T, ox, oy, False)),
    "futuro_noche": (lambda: _futuro(True), lambda im, T, ox, oy: _futuro_amb(im, T, ox, oy, True)),
    "campo": (lambda: _campo(False), lambda im, T, ox, oy: _campo_amb(im, T, ox, oy, False)),
    "campo_noche": (lambda: _campo(True), lambda im, T, ox, oy: _campo_amb(im, T, ox, oy, True)),
    "despacho": (_despacho, _despacho_amb), "niebla": (_niebla, _niebla_amb),
    "huerto": (lambda: _huerto(False), lambda im, T, ox, oy: _huerto_amb(im, T, ox, oy, False)),
    "huerto_noche": (lambda: _huerto(True), lambda im, T, ox, oy: _huerto_amb(im, T, ox, oy, True)),
    "lavanderia": (lambda: _lavanderia(False), lambda im, T, ox, oy: _lavanderia_amb(im, T, ox, oy, False)),
    "lavanderia_noche": (lambda: _lavanderia(True), lambda im, T, ox, oy: _lavanderia_amb(im, T, ox, oy, True)),
    "pizzeria": (lambda: _pizzeria(False), lambda im, T, ox, oy: _pizzeria_amb(im, T, ox, oy, False)),
    "pizzeria_noche": (lambda: _pizzeria(True), lambda im, T, ox, oy: _pizzeria_amb(im, T, ox, oy, True)),
    "pabellon": (lambda: _pabellon(False), lambda im, T, ox, oy: _pabellon_amb(im, T, ox, oy, False)),
    "pabellon_vacio": (lambda: _pabellon(True), lambda im, T, ox, oy: _pabellon_amb(im, T, ox, oy, True)),
    "sakura": (lambda: _sakura(False), lambda im, T, ox, oy: _sakura_amb(im, T, ox, oy, False)),
    "sakura_noche": (lambda: _sakura(True), lambda im, T, ox, oy: _sakura_amb(im, T, ox, oy, True)),
}


def instalar3():
    EC.SCEN.update(NUEVOS3); EC.instalar()


if __name__ == "__main__":   # hoja de contacto: python3 escenarios3.py salida.jpg
    import sys
    instalar3(); names = list(NUEVOS3); cols = 4; tw, th = 216, 384
    sheet = Image.new("RGB", (cols * tw, ((len(names) + cols - 1) // cols) * th))
    for i, n in enumerate(names): sheet.paste(EC.bg(n, 1.0).convert("RGB").resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
    sheet.save(sys.argv[1])
