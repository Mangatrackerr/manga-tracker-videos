# Escenarios del lote 2026-11-27z: 8 sitios nuevos (uno por vídeo) + una variante de cada uno.
# Se registran en escenarios.SCEN con instalar4(). Todo dibujado aquí: sin imágenes, logos ni textos de marcas.
# Nada de destellos rápidos: lo que brilla lo hace con pulsos lentos.
import math, random
from PIL import Image, ImageDraw, ImageFilter
import escenarios as EC
from escenarios import BW2, BH2, _grad, _shade
from escenarios3 import _sky, _glow, _stars


# ---------------- 1. Aldea de tejados (relleno) ----------------
def _aldea(night=False):
    im = _sky(*(((16, 18, 50), (70, 50, 100)) if night else ((255, 190, 120), (255, 235, 200))), 1200)
    d = ImageDraw.Draw(im); rnd = random.Random(51)
    if night: _stars(d, rnd, 60, 600); d.ellipse((860, 150, 1010, 300), fill=(255, 246, 220))
    else: d.ellipse((780, 330, 1000, 550), fill=(255, 250, 220))
    m = (90, 70, 110) if night else (190, 130, 120)
    d.polygon([(0, 1000), (250, 640), (480, 900), (720, 560), (1000, 880), (BW2, 700), (BW2, 1100), (0, 1100)], fill=m)   # montañas
    for k in range(7):   # casas con tejado a dos aguas
        x = -60 + k * 190; y = 1080 + (k % 2) * 60; w = 200; h = 170
        wall = (230, 210, 180) if not night else (80, 74, 90)
        d.rectangle((x, y, x + w, y + h + 260), fill=_shade(wall, 0.92 + 0.04 * (k % 3)))
        d.polygon([(x - 30, y + 10), (x + w / 2, y - 110), (x + w + 30, y + 10)], fill=(170, 60, 50) if not night else (90, 40, 50))
        wy = y + 60; d.rectangle((x + 60, wy, x + 140, wy + 70), fill=(255, 210, 120) if night else (90, 70, 60))
    d.rectangle((0, 1500, BW2, BH2), fill=(180, 150, 110) if not night else (60, 54, 66))   # calle de tierra
    for k in range(0, BW2, 160): d.ellipse((k, 1640 + (k % 3) * 40, k + 60, 1660 + (k % 3) * 40), fill=_shade((180, 150, 110) if not night else (60, 54, 66), 0.85))
    for x in (120, 1080):   # farolillos
        d.line((x, 1500, x, 1240), fill=(70, 50, 40), width=12); d.ellipse((x - 45, 1180, x + 45, 1280), fill=(240, 90, 70))
        if night: _glow(im, x, 1230, 130, (255, 150, 90), 90, 40)
    return im


def _aldea_amb(im, T, ox, oy, night=False):
    d = ImageDraw.Draw(im); rnd = random.Random(5)
    for k in range(14):   # hojas que cruzan con el viento
        x = (rnd.uniform(0, BW2) + T * (120 + k * 9)) % (BW2 + 200) - 100 - ox; y = rnd.uniform(200, 1500) + 60 * math.sin(T * 1.5 + k) - oy
        f = abs(math.sin(T * 3 + k)); c = (120, 190, 90, 220) if not night else (150, 160, 200, 180)
        d.ellipse((x - 16, y - 7 * f - 2, x + 16, y + 7 * f + 2), fill=c)


# ---------------- 2. Tribunal (sobrevalorado) ----------------
def _tribunal(dark=False):
    im = _grad(*(((120, 70, 50), (160, 100, 70)) if not dark else ((40, 24, 30), (70, 40, 44)))); d = ImageDraw.Draw(im)
    for x in range(0, BW2, 150): d.rectangle((x, 0, x + 18, 1200), fill=_shade((120, 70, 50) if not dark else (40, 24, 30), 0.8))   # paneles
    d.rectangle((0, 120, BW2, 150), fill=(90, 50, 34) if not dark else (30, 18, 22))
    d.ellipse((470, 180, 730, 440), fill=(230, 190, 90)); d.ellipse((500, 210, 700, 410), fill=(200, 160, 60))   # escudo dorado genérico
    d.line((600, 230, 600, 390), fill=(110, 80, 30), width=10); d.line((520, 260, 680, 260), fill=(110, 80, 30), width=10)
    for sx in (520, 680): d.arc((sx - 40, 260, sx + 40, 340), 0, 180, fill=(110, 80, 30), width=8)
    d.rectangle((0, 1200, BW2, BH2), fill=(90, 54, 40) if not dark else (36, 22, 26))
    for y in range(1200, BH2, 70): d.line((0, y, BW2, y), fill=(76, 44, 32) if not dark else (28, 16, 20), width=4)
    d.rectangle((260, 900, 940, 1380), fill=(110, 64, 40) if not dark else (50, 30, 32)); d.rectangle((240, 880, 960, 920), fill=(140, 84, 54) if not dark else (64, 38, 40))   # estrado
    for x in range(300, 920, 120): d.rectangle((x, 960, x + 80, 1340), outline=(90, 52, 34) if not dark else (40, 24, 26), width=6)
    for x in (60, 1060):   # columnas
        d.rectangle((x - 50, 200, x + 50, 1200), fill=(220, 210, 190) if not dark else (90, 84, 80))
        for k in range(-30, 40, 30): d.line((x + k, 220, x + k, 1180), fill=(190, 180, 160) if not dark else (70, 64, 62), width=5)
    return im


def _tribunal_amb(im, T, ox, oy, dark=False):
    d = ImageDraw.Draw(im)
    if dark:   # un foco que barre despacio
        x = 600 + 300 * math.sin(T * 0.6) - ox
        d.polygon([(x - 30, -oy), (x + 30, -oy), (x + 260, 1950 - oy), (x - 260, 1950 - oy)], fill=(255, 245, 200, 30)); return
    for k in range(10):   # motas de polvo flotando en la luz
        x = 200 + (k * 97 + T * 20) % 800 - ox; y = 300 + (k * 131 + T * 15 * (1 + k % 3)) % 1100 - oy
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(255, 240, 200, 120))


# ---------------- 3. Planeta que se rompe (Namek) ----------------
def _planeta(red=False):
    im = _sky(*(((40, 120, 90), (150, 220, 160)) if not red else ((80, 20, 30), (230, 110, 60))), 1250)
    d = ImageDraw.Draw(im); rnd = random.Random(61)
    for (x, y, r) in ((200, 300, 90), (950, 220, 60), (700, 420, 40)):   # soles/lunas
        d.ellipse((x - r, y - r, x + r, y + r), fill=(250, 250, 220) if not red else (255, 200, 120))
    for k in range(5):   # islas-roca altas con copa redonda
        x = 80 + k * 260 + rnd.randint(-30, 30); h = rnd.randint(250, 480)
        c = (110, 130, 120) if not red else (90, 50, 50)
        d.polygon([(x - 50, 1250), (x + 50, 1250), (x + 30, 1250 - h), (x - 30, 1250 - h)], fill=c)
        d.ellipse((x - 90, 1250 - h - 70, x + 90, 1250 - h + 40), fill=(80, 170, 110) if not red else (130, 60, 40))
    d.rectangle((0, 1250, BW2, BH2), fill=(110, 170, 130) if not red else (110, 50, 40))
    for k in range(6):
        cx_ = rnd.uniform(0, BW2); d.ellipse((cx_ - 260, 1300 + k * 120, cx_ + 260, 1360 + k * 120), fill=_shade((110, 170, 130) if not red else (110, 50, 40), 0.9))
    lava = (255, 150, 60) if red else (60, 110, 90)
    for (pts) in ([(150, 1400), (320, 1520), (300, 1680), (480, 1800)], [(900, 1350), (780, 1500), (860, 1650), (720, 1900)]):   # grietas
        d.line(pts, fill=lava, width=16 if red else 10, joint="curve")
    return im


def _planeta_amb(im, T, ox, oy, red=False):
    d = ImageDraw.Draw(im); rnd = random.Random(8)
    for k in range(16):   # rocas que flotan hacia arriba despacio
        x = rnd.uniform(0, BW2) + 20 * math.sin(T + k) - ox; y = (rnd.uniform(0, 2000) - T * (60 + 10 * (k % 4))) % 2000 - oy; r = 8 + k % 4 * 6
        d.polygon([(x - r, y), (x, y - r), (x + r * 1.2, y + r * 0.3), (x, y + r)], fill=(120, 110, 100) if not red else (150, 70, 50))
    if red:
        a = int(40 + 30 * math.sin(T * 1.2)); g = Image.new("RGBA", im.size, (255, 120, 40, 0)); ImageDraw.Draw(g).rectangle((0, 1300 - oy, BW2, BH2), fill=(255, 120, 40, a)); im.alpha_composite(g)


# ---------------- 4. Desván lleno de cajas (planificado) ----------------
def _desvan(night=False):
    im = _grad(*(((150, 110, 80), (190, 150, 110)) if not night else ((40, 34, 50), (70, 56, 70)))); d = ImageDraw.Draw(im)
    d.polygon([(0, 0), (600, 0), (0, 700)], fill=(110, 76, 54) if not night else (30, 24, 36)); d.polygon([(BW2, 0), (600, 0), (BW2, 700)], fill=(110, 76, 54) if not night else (30, 24, 36))   # techo inclinado
    for k in range(6): d.line((k * 110, 0, 0, 700 - k * 115), fill=(90, 60, 42) if not night else (24, 20, 30), width=10); d.line((BW2 - k * 110, 0, BW2, 700 - k * 115), fill=(90, 60, 42) if not night else (24, 20, 30), width=10)
    d.polygon([(500, 200), (700, 200), (740, 460), (460, 460)], fill=(170, 220, 255) if not night else (40, 50, 110))   # ventanuco
    d.line((600, 200, 600, 460), fill=(90, 60, 42), width=10); d.line((480, 330, 720, 330), fill=(90, 60, 42), width=10)
    if night: d.ellipse((620, 230, 680, 290), fill=(255, 245, 220))
    d.rectangle((0, 1350, BW2, BH2), fill=(140, 100, 70) if not night else (56, 44, 50))
    for x in range(0, BW2, 150): d.line((x, 1350, x - 80, BH2), fill=(120, 84, 58) if not night else (46, 36, 42), width=5)
    rnd = random.Random(14)
    for (x, y, w, h) in ((20, 1150, 260, 210), (40, 950, 220, 200), (900, 1100, 280, 250), (940, 880, 230, 220), (960, 700, 180, 180), (300, 1230, 170, 130)):   # cajas
        c = _shade((205, 160, 100) if not night else (110, 86, 70), rnd.uniform(0.9, 1.05))
        d.rectangle((x, y, x + w, y + h), fill=c); d.rectangle((x, y, x + w, y + 22), fill=_shade(c, 0.85)); d.rectangle((x + w / 2 - 16, y, x + w / 2 + 16, y + h), fill=_shade(c, 1.1))
    return im


def _desvan_amb(im, T, ox, oy, night=False):
    d = ImageDraw.Draw(im)
    a = int(26 + 10 * math.sin(T * 0.8))   # rayo de luz del ventanuco con polvo
    d.polygon([(470 - ox, 460 - oy), (730 - ox, 460 - oy), (900 - ox, 1700 - oy), (300 - ox, 1700 - oy)], fill=(255, 245, 210, a) if not night else (180, 200, 255, a))
    for k in range(14):
        x = 380 + (k * 83 + T * 14) % 440 - ox; y = 520 + (k * 157 + T * 22) % 1100 - oy; d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(255, 250, 230, 150))


# ---------------- 5. Kiosco de calle (estrenos) ----------------
def _kiosco(night=False):
    im = _sky(*(((20, 26, 60), (60, 60, 110)) if night else ((140, 200, 255), (220, 240, 255))), 1100)
    d = ImageDraw.Draw(im); rnd = random.Random(71)
    if night: _stars(d, rnd, 40, 500)
    for k in range(6):   # edificios
        x = -40 + k * 220; h = rnd.randint(500, 800); c = (200, 180, 170) if not night else (60, 56, 80)
        d.rectangle((x, 1150 - h, x + 210, 1160), fill=_shade(c, 0.9 + 0.05 * (k % 3)))
        for yy in range(1150 - h + 50, 1100, 90):
            for xx in range(x + 25, x + 190, 60): d.rectangle((xx, yy, xx + 34, yy + 50), fill=(255, 220, 130) if night and rnd.random() < 0.6 else (130, 160, 200) if not night else (40, 40, 60))
    d.rectangle((0, 1160, BW2, 1260), fill=(190, 190, 195) if not night else (70, 70, 84))   # acera
    d.rectangle((0, 1260, BW2, BH2), fill=(120, 120, 130) if not night else (44, 44, 56))
    # kiosco verde a la derecha con revistas genéricas (sin títulos)
    kx = 760; d.rectangle((kx, 700, kx + 420, 1300), fill=(40, 120, 80) if not night else (24, 70, 50)); d.polygon([(kx - 40, 720), (kx + 460, 720), (kx + 420, 620), (kx, 620)], fill=(30, 90, 60))
    for j in range(3):
        for i in range(3):
            c = [(240, 90, 110), (90, 170, 250), (250, 210, 70), (160, 110, 240), (90, 210, 150), (255, 150, 80), (240, 240, 240), (230, 70, 70), (110, 200, 230)][j * 3 + i]
            d.rectangle((kx + 30 + i * 130, 760 + j * 170, kx + 140 + i * 130, 900 + j * 170), fill=c); d.rectangle((kx + 40 + i * 130, 775 + j * 170, kx + 130 + i * 130, 795 + j * 170), fill=(255, 255, 255))
    for x in range(0, BW2, 260): d.rectangle((x, 1580, x + 140, 1600), fill=(240, 240, 240) if not night else (120, 120, 130))   # marcas de la calzada
    return im


def _kiosco_amb(im, T, ox, oy, night=False):
    d = ImageDraw.Draw(im)
    for k in range(3):   # coches cruzando al fondo de la calle
        sp = 260 + k * 90; x = ((T * sp + k * 500) % (BW2 + 500)) - 250 - ox; y = 1330 + k * 30 - oy
        if k % 2: x = BW2 - x
        c = [(230, 70, 70), (70, 140, 230), (250, 200, 60)][k]
        d.rounded_rectangle((x - 110, y - 40, x + 110, y + 20), radius=18, fill=c); d.rounded_rectangle((x - 60, y - 80, x + 60, y - 30), radius=16, fill=_shade(c, 0.85))
        d.ellipse((x - 80, y, x - 40, y + 40), fill=(30, 30, 30)); d.ellipse((x + 40, y, x + 80, y + 40), fill=(30, 30, 30))
        if night: d.ellipse((x + 95 * (1 if not k % 2 else -1) - 14, y - 30, x + 95 * (1 if not k % 2 else -1) + 14, y - 6), fill=(255, 250, 200))


# ---------------- 6. Cumbre nevada (Ash) ----------------
def _nevada(dawn=False):
    im = _sky(*(((80, 140, 220), (200, 230, 255)) if not dawn else ((60, 40, 110), (255, 170, 120))), 1300)
    d = ImageDraw.Draw(im); rnd = random.Random(81)
    if dawn: d.ellipse((480, 900, 720, 1140), fill=(255, 220, 140))
    d.rectangle((0, 1250, BW2, BH2), fill=(225, 232, 248) if not dawn else (235, 205, 215))
    for (pts, c) in (([(0, 1200), (300, 700), (520, 1100), (800, 600), (BW2, 1150), (BW2, 1400), (0, 1400)], (150, 170, 210) if not dawn else (130, 100, 150)),):
        d.polygon(pts, fill=c)
    for (x, y) in ((300, 700), (800, 600)): d.polygon([(x - 80, y + 110), (x, y), (x + 80, y + 110), (x + 30, y + 90), (x - 20, y + 120)], fill=(250, 250, 255))
    # pico principal en primer plano (nieve) con banderín en la cima
    d.polygon([(-100, BH2), (600, 1150), (1300, BH2)], fill=(240, 245, 255) if not dawn else (250, 225, 225))
    d.polygon([(600, 1150), (700, 1400), (650, 1380), (600, 1500), (560, 1380), (520, 1420)], fill=(200, 210, 235) if not dawn else (220, 180, 200))
    d.line((600, 1150, 600, 960), fill=(80, 60, 50), width=10); d.polygon([(600, 960), (720, 995), (600, 1030)], fill=(230, 60, 60))
    d.rectangle((0, 1700, BW2, BH2), fill=(235, 240, 252) if not dawn else (245, 220, 225))
    return im


def _nevada_amb(im, T, ox, oy, dawn=False):
    d = ImageDraw.Draw(im); rnd = random.Random(3)
    for k in range(60):   # nieve que cae en diagonal
        x = (rnd.uniform(0, BW2) + T * 50 + 30 * math.sin(T + k)) % BW2 - ox; y = (rnd.uniform(0, 2000) + T * (90 + k % 5 * 20)) % 2000 - oy; r = 3 + k % 3 * 2
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, 220))
    x = 720 - ox; y = 995 - oy; w = 10 * math.sin(T * 5)   # el banderín ondea
    d.polygon([(600 - ox, 960 - oy), (x, y + w), (600 - ox, 1030 - oy)], fill=(230, 60, 60))


# ---------------- 7. Gimnasio de boxeo (One Punch Man) ----------------
def _gimnasio(night=False):
    im = _grad(*(((150, 160, 175), (190, 195, 205)) if not night else ((30, 32, 44), (54, 56, 70)))); d = ImageDraw.Draw(im)
    for y in range(0, 1300, 80): d.line((0, y, BW2, y), fill=_shade((150, 160, 175) if not night else (30, 32, 44), 0.92), width=3)   # ladrillo
    for x in range(160, BW2, 330): d.rectangle((x, 60, x + 200, 90), fill=(250, 250, 240) if not night else (80, 80, 90))
    # cuadrilátero al fondo
    d.rectangle((150, 1050, 1050, 1250), fill=(60, 90, 170) if not night else (30, 44, 90))
    for k, c in enumerate(((230, 60, 60), (250, 250, 250), (60, 120, 230))): d.line((150, 830 + k * 70, 1050, 830 + k * 70), fill=c, width=10)
    for x in (150, 1050): d.rectangle((x - 20, 780, x + 20, 1250), fill=(240, 240, 240) if not night else (120, 120, 130))
    d.rectangle((0, 1250, BW2, BH2), fill=(110, 110, 120) if not night else (40, 40, 50))
    for x in range(0, BW2, 200): d.rectangle((x, 1250, x + 196, BH2), outline=(95, 95, 105) if not night else (34, 34, 44), width=4)
    # pesas en el suelo
    for x in (90, 1100):
        d.rectangle((x - 60, 1720, x + 60, 1740), fill=(80, 80, 90)); d.ellipse((x - 90, 1680, x - 50, 1780), fill=(30, 30, 36)); d.ellipse((x + 50, 1680, x + 90, 1780), fill=(30, 30, 36))
    return im


def _gimnasio_amb(im, T, ox, oy, night=False):
    d = ImageDraw.Draw(im)
    for k, x in enumerate((140, 1060)):   # sacos que se balancean
        a = 0.12 * math.sin(T * 1.6 + k * 1.3); top = (x - ox, 100 - oy); L = 520
        bx = top[0] + L * math.sin(a); by = top[1] + L * math.cos(a)
        d.line((top, (bx, by - 260)), fill=(60, 60, 70), width=6)
        d.rounded_rectangle((bx - 70, by - 260, bx + 70, by + 60), radius=50, fill=(200, 50, 50) if k == 0 else (40, 40, 50))
    if night:
        a = int(24 + 10 * math.sin(T * 0.7)); d.polygon([(560 - ox, -oy), (640 - ox, -oy), (900 - ox, 1900 - oy), (300 - ox, 1900 - oy)], fill=(255, 250, 220, a))


# ---------------- 8. Aula (nota baja) ----------------
def _aula(evening=False):
    im = _grad(*(((230, 225, 205), (245, 240, 225)) if not evening else ((200, 150, 120), (230, 180, 140)))); d = ImageDraw.Draw(im)
    d.rectangle((120, 200, 1080, 760), fill=(40, 80, 60)); d.rectangle((100, 180, 1100, 200), fill=(150, 100, 60)); d.rectangle((100, 760, 1100, 790), fill=(150, 100, 60))   # pizarra
    rnd = random.Random(4)
    for k in range(4): d.line((180, 290 + k * 110, 180 + rnd.randint(250, 600), 290 + k * 110), fill=(220, 230, 220), width=8)   # tiza (garabatos sin texto)
    d.ellipse((860, 300, 1000, 440), outline=(220, 230, 220), width=8)
    for x in (30, 1170):   # ventanas
        d.rectangle((x - 30 if x < 600 else x - 60, 300, x + 60 if x < 600 else x + 30, 1100), fill=(170, 220, 255) if not evening else (255, 190, 130))
    d.rectangle((0, 1200, BW2, BH2), fill=(170, 130, 90) if not evening else (150, 100, 70))
    for y in range(1200, BH2, 60): d.line((0, y, BW2, y), fill=(150, 112, 76) if not evening else (130, 86, 60), width=3)
    for (x, y, s) in ((240, 1260, 0.8), (960, 1260, 0.8), (160, 1520, 1.1), (1040, 1520, 1.1)):   # pupitres
        d.rectangle((x - 140 * s, y, x + 140 * s, y + 30 * s), fill=(200, 160, 110)); d.rectangle((x - 120 * s, y + 30 * s, x - 100 * s, y + 200 * s), fill=(90, 90, 100)); d.rectangle((x + 100 * s, y + 30 * s, x + 120 * s, y + 200 * s), fill=(90, 90, 100))
    return im


def _aula_amb(im, T, ox, oy, evening=False):
    d = ImageDraw.Draw(im)
    for k in range(3):   # aviones de papel que planean
        v = (T * 0.18 + k / 3) % 1; x = -150 + (BW2 + 300) * v - ox; y = 880 + k * 90 + 60 * math.sin(v * 6 + k) - oy
        d.polygon([(x + 60, y), (x - 50, y - 26), (x - 20, y), (x - 50, y + 22)], fill=(255, 255, 255)); d.line((x + 60, y, x - 20, y), fill=(200, 200, 210), width=3)
    if evening:
        a = int(30 + 12 * math.sin(T * 0.6)); d.polygon([(1170 - ox, 300 - oy), (1170 - ox, 1100 - oy), (400 - ox, 1900 - oy), (200 - ox, 1500 - oy)], fill=(255, 210, 150, a))


NUEVOS4 = {
    "aldea": (lambda: _aldea(False), lambda im, T, ox, oy: _aldea_amb(im, T, ox, oy, False)),
    "aldea_noche": (lambda: _aldea(True), lambda im, T, ox, oy: _aldea_amb(im, T, ox, oy, True)),
    "tribunal": (lambda: _tribunal(False), lambda im, T, ox, oy: _tribunal_amb(im, T, ox, oy, False)),
    "tribunal_noche": (lambda: _tribunal(True), lambda im, T, ox, oy: _tribunal_amb(im, T, ox, oy, True)),
    "planeta": (lambda: _planeta(False), lambda im, T, ox, oy: _planeta_amb(im, T, ox, oy, False)),
    "planeta_rojo": (lambda: _planeta(True), lambda im, T, ox, oy: _planeta_amb(im, T, ox, oy, True)),
    "desvan": (lambda: _desvan(False), lambda im, T, ox, oy: _desvan_amb(im, T, ox, oy, False)),
    "desvan_noche": (lambda: _desvan(True), lambda im, T, ox, oy: _desvan_amb(im, T, ox, oy, True)),
    "kiosco": (lambda: _kiosco(False), lambda im, T, ox, oy: _kiosco_amb(im, T, ox, oy, False)),
    "kiosco_noche": (lambda: _kiosco(True), lambda im, T, ox, oy: _kiosco_amb(im, T, ox, oy, True)),
    "nevada": (lambda: _nevada(False), lambda im, T, ox, oy: _nevada_amb(im, T, ox, oy, False)),
    "nevada_alba": (lambda: _nevada(True), lambda im, T, ox, oy: _nevada_amb(im, T, ox, oy, True)),
    "gimnasio": (lambda: _gimnasio(False), lambda im, T, ox, oy: _gimnasio_amb(im, T, ox, oy, False)),
    "gimnasio_noche": (lambda: _gimnasio(True), lambda im, T, ox, oy: _gimnasio_amb(im, T, ox, oy, True)),
    "aula": (lambda: _aula(False), lambda im, T, ox, oy: _aula_amb(im, T, ox, oy, False)),
    "aula_tarde": (lambda: _aula(True), lambda im, T, ox, oy: _aula_amb(im, T, ox, oy, True)),
}


def instalar4():
    import escenarios3 as EC3
    EC.SCEN.update(EC3.NUEVOS3); EC.SCEN.update(NUEVOS4); EC.instalar()


if __name__ == "__main__":   # hoja de contacto: python3 escenarios4.py salida.jpg
    import sys
    instalar4(); names = list(NUEVOS4); cols = 4; tw, th = 216, 384
    sheet = Image.new("RGB", (cols * tw, ((len(names) + cols - 1) // cols) * th))
    for i, n in enumerate(names): sheet.paste(EC.bg(n, 1.0).convert("RGB").resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
    sheet.save(sys.argv[1])
