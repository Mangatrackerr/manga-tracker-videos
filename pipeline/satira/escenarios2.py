# Escenarios del lote 2026-11-20x: 10 sitios nuevos (uno por vídeo) + una variante de cada uno.
# Se registran en escenarios.SCEN con instalar2(). Todo dibujado aquí: sin imágenes, logos ni textos de marcas.
# Nada de destellos rápidos: todo lo que "brilla" lo hace despacio (pulsos lentos).
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import escenarios as EC
from escenarios import BW2, BH2, _grad, _shade
from engine_satira import W, H


def _glow(im, x, y, r, col, a=90, blur=60):
    g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((x - r, y - r, x + r, y + r), fill=col + (a,))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))


def _stars(d, rnd, n, y1, col=(255, 255, 255)):
    for _ in range(n):
        x, y = rnd.uniform(0, BW2), rnd.uniform(0, y1); r = rnd.choice((1.5, 2, 3)); d.ellipse((x - r, y - r, x + r, y + r), fill=col)


# ---------------- 1. Carretera al atardecer (isekai) ----------------
def _carretera():
    im = _grad((255, 150, 110), (120, 70, 150), h=1250); full = Image.new("RGBA", (BW2, BH2), (60, 56, 70, 255)); full.paste(im.crop((0, 0, BW2, 1250)), (0, 0)); im = full
    d = ImageDraw.Draw(im); rnd = random.Random(21)
    d.ellipse((760, 640, 1000, 880), fill=(255, 220, 150))
    x = -10
    while x < BW2:   # edificios de ciudad dormitorio
        bw = rnd.randint(110, 200); bh = rnd.randint(250, 620); c = (90 + rnd.randint(0, 20), 70, 110)
        d.rectangle((x, 1250 - bh, x + bw, 1250), fill=c)
        for yy in range(1250 - bh + 26, 1230, 52):
            for xx in range(x + 16, x + bw - 26, 40):
                if rnd.random() < 0.35: d.rectangle((xx, yy, xx + 18, yy + 26), fill=(255, 210, 130))
        x += bw + 8
    d.rectangle((0, 1250, BW2, 1330), fill=(150, 150, 160))   # acera
    for k in range(0, BW2, 80): d.line((k, 1250, k, 1330), fill=(130, 130, 140), width=3)
    d.rectangle((0, 1330, BW2, BH2), fill=(56, 54, 66))       # asfalto
    d.rectangle((0, 1340, BW2, 1352), fill=(240, 240, 240))
    # paso de cebra
    for k in range(7): d.rectangle((140 + k * 130, 1500, 220 + k * 130, 1900), fill=(230, 230, 230))
    # farola y señal genérica
    d.rectangle((60, 760, 76, 1250), fill=(70, 70, 80)); d.rectangle((60, 760, 200, 776), fill=(70, 70, 80)); d.ellipse((170, 760, 230, 800), fill=(255, 240, 180))
    d.rectangle((1040, 980, 1054, 1250), fill=(120, 120, 130)); d.polygon([(1047, 880), (1110, 980), (984, 980)], fill=(250, 200, 40)); d.polygon([(1047, 905), (1090, 970), (1004, 970)], fill=(40, 40, 40))
    return im


def _carretera_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    for k in range(4):   # pájaros lejanos
        x = (k * 300 + T * 60) % (BW2 + 200) - 100 - ox; y = 300 + k * 90 + 10 * math.sin(T * 3 + k) - oy; f = 12 * math.sin(T * 8 + k)
        d.line([(x - 26, y - f), (x, y), (x + 26, y - f)], fill=(70, 40, 80), width=5)


def _isekai():
    im = _grad((120, 200, 255), (210, 240, 255), h=1200); full = Image.new("RGBA", (BW2, BH2)); full.paste(im.crop((0, 0, BW2, 1200)), (0, 0)); im = full
    d = ImageDraw.Draw(im)
    d.rectangle((0, 1200, BW2, BH2), fill=(110, 200, 110))
    for layer, (col, base, amp) in enumerate([((150, 190, 230), 1000, 220), ((120, 180, 130), 1150, 120)]):
        pts = [(0, 1300)] + [(x, base - amp * abs(math.sin(x / (220 + 90 * layer) + 1 + layer))) for x in range(0, BW2 + 20, 20)] + [(BW2, 1300)]
        d.polygon(pts, fill=col)
    # castillo genérico en la colina
    c = (240, 236, 250); r = (110, 90, 200)
    d.rectangle((760, 780, 980, 1060), fill=c)
    for x in (740, 860, 960):
        d.rectangle((x, 700, x + 60, 1060), fill=c); d.polygon([(x - 10, 700), (x + 70, 700), (x + 30, 600)], fill=r)
    d.rounded_rectangle((850, 940, 890, 1060), radius=20, fill=(90, 70, 140))
    # flores en la hierba
    rnd = random.Random(8)
    for _ in range(90):
        x, y = rnd.uniform(0, BW2), rnd.uniform(1260, BH2); c2 = rnd.choice([(255, 120, 160), (255, 230, 90), (255, 255, 255), (180, 140, 255)])
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=c2); d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(255, 200, 60))
    return im


def _isekai_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    for k in range(2):   # islas flotantes que suben y bajan despacio
        x = 180 + k * 300 - ox; y = 420 + k * 160 + 20 * math.sin(T * 1.1 + k * 2) - oy
        d.polygon([(x - 120, y), (x + 120, y), (x + 40, y + 110), (x - 30, y + 140)], fill=(150, 110, 80)); d.ellipse((x - 130, y - 30, x + 130, y + 20), fill=(110, 200, 110))
        d.line((x + 30, y - 20, x + 30, y - 110), fill=(110, 80, 60), width=10); d.ellipse((x - 20, y - 170, x + 80, y - 80), fill=(90, 180, 100))
    rnd = random.Random(3)
    for k in range(18):  # chispitas mágicas flotando
        x = rnd.uniform(0, BW2) + 30 * math.sin(T + k) - ox; y = (rnd.uniform(0, BH2) - T * 60 * rnd.uniform(0.5, 1.4)) % BH2 - oy
        a = int(140 + 100 * math.sin(T * 1.5 + k)); d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(255, 250, 200, max(0, a)))


# ---------------- 2. Playa de Hawái ----------------
def _playa(sunset=False):
    sky = ((255, 170, 120), (255, 120, 140)) if sunset else ((80, 180, 250), (190, 235, 255))
    im = _grad(sky[0], sky[1], h=1100); full = Image.new("RGBA", (BW2, BH2)); full.paste(im.crop((0, 0, BW2, 1100)), (0, 0)); im = full
    d = ImageDraw.Draw(im)
    if sunset: d.ellipse((420, 840, 780, 1200), fill=(255, 210, 120))
    else: d.ellipse((860, 160, 1040, 340), fill=(255, 245, 190))
    # volcán al fondo
    d.polygon([(380, 1100), (640, 760), (720, 760), (1000, 1100)], fill=(120, 100, 130) if sunset else (90, 120, 110))
    d.polygon([(640, 760), (720, 760), (700, 800), (660, 800)], fill=(80, 60, 80))
    sea = ((240, 120, 120), (120, 70, 120)) if sunset else ((40, 150, 210), (20, 90, 170))
    d.rectangle((0, 1100, BW2, 1420), fill=sea[0]); d.rectangle((0, 1250, BW2, 1420), fill=sea[1])
    d.rectangle((0, 1420, BW2, BH2), fill=(250, 220, 160) if not sunset else (230, 180, 140))
    rnd = random.Random(5)
    for _ in range(140):
        x, y = rnd.uniform(0, BW2), rnd.uniform(1440, BH2); d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(220, 190, 130))
    for x0 in (40, 1080):   # troncos de palmera (las hojas se mueven en _amb)
        pts = [(x0 + 60 * math.sin(v * 1.2) * (1 if x0 < 600 else -1), 1700 - v * 900) for v in np.linspace(0, 1, 20)]
        for (a, b), (c, e) in zip(pts, pts[1:]): d.line((a, b, c, e), fill=(140, 96, 60), width=46)
        for (a, b) in pts[::2]: d.line((a - 22, b, a + 22, b - 8), fill=(110, 74, 46), width=6)
    return im


def _playa_amb(im, T, ox, oy, sunset=False):
    d = ImageDraw.Draw(im)
    for k in range(5):   # olas que van y vienen
        y = 1150 + k * 60 - oy; sh = 40 * math.sin(T * 1.2 + k)
        pts = [(x - ox + sh, y + 10 * math.sin(x / 70 + T * 2 + k)) for x in range(0, BW2 + 40, 40)]
        d.line(pts, fill=(255, 255, 255, 150), width=6)
    yfoam = 1420 - oy + 18 * math.sin(T * 1.3)
    d.rounded_rectangle((-40, yfoam - 14, BW2, yfoam + 14), radius=14, fill=(255, 255, 255, 200))
    for x0, sg in ((40, 1), (1080, -1)):   # hojas de palmera balanceándose
        tx = x0 + sg * 60 * math.sin(1.2) - ox; ty = 800 - oy
        for j in range(6):
            a = math.pi * (0.1 + j * 0.16) + 0.08 * math.sin(T * 1.7 + j); a = a if sg > 0 else math.pi - a
            pts = [(tx + 280 * v * math.cos(a), ty - 280 * v * math.sin(a) + 120 * v * v) for v in np.linspace(0, 1, 10)]
            d.line(pts, fill=(40, 140, 60) if not sunset else (50, 90, 60), width=34, joint="curve")
    for k in range(2):   # gaviotas
        x = (k * 500 + T * 90) % (BW2 + 300) - 150 - ox; y = 520 + k * 120 - oy; f = 16 * math.sin(T * 7 + k)
        d.line([(x - 34, y - f), (x, y), (x + 34, y - f)], fill=(255, 255, 255), width=6)


# ---------------- 3. Metro ----------------
def _metro():
    im = _grad((200, 210, 220), (170, 180, 195)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, BW2, 120), fill=(225, 228, 235))
    d.rectangle((0, 150, BW2, 170), fill=(160, 165, 175))                # barra del techo
    for k in range(3):   # ventanas
        x = 60 + k * 390; d.rounded_rectangle((x, 420, x + 330, 900), radius=40, fill=(40, 46, 70)); d.rounded_rectangle((x, 420, x + 330, 900), radius=40, outline=(150, 155, 165), width=14)
    d.rectangle((0, 1000, BW2, 1060), fill=(120, 130, 150))                 # respaldo
    d.rectangle((0, 1060, BW2, 1240), fill=(60, 110, 190)); d.rectangle((0, 1240, BW2, 1290), fill=(40, 80, 150))   # asientos
    for x in range(0, BW2, 200): d.line((x, 1060, x, 1240), fill=(50, 95, 170), width=6)
    d.rectangle((0, 1290, BW2, 1560), fill=(140, 145, 155))
    d.rectangle((0, 1560, BW2, BH2), fill=(110, 110, 118))
    for x in range(0, BW2, 60): d.line((x, 1560, x - 120, BH2), fill=(100, 100, 108), width=3)
    for x in (150, 1050): d.rectangle((x - 9, 170, x + 9, 1560), fill=(230, 200, 60))   # barras amarillas
    # mapa de línea genérico (puntos, sin nombres)
    d.rounded_rectangle((380, 230, 820, 330), radius=14, fill=(250, 250, 250)); d.line((420, 280, 780, 280), fill=(230, 60, 80), width=10)
    for k in range(7): d.ellipse((414 + k * 60, 270, 434 + k * 60, 290), fill=(255, 255, 255), outline=(230, 60, 80), width=5)
    return im


def _metro_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    for k in range(3):   # luces del túnel pasando por las ventanas
        x0 = 60 + k * 390 - ox; y0 = 420 - oy
        for j in range(3):
            v = (T * 1.6 + j / 3 + k * 0.13) % 1; x = x0 + 330 - v * 420
            if x0 < x < x0 + 300: d.rectangle((x, y0 + 40, x + 30, y0 + 440), fill=(255, 230, 160, 120))
    for k in range(6):   # asideros balanceándose
        x = 120 + k * 190 - ox; a = 0.12 * math.sin(T * 2.2 + k * 0.4); y0 = 160 - oy
        xe = x + 120 * math.sin(a); ye = y0 + 120 * math.cos(a)
        d.line((x, y0, xe, ye), fill=(90, 90, 100), width=6); d.ellipse((xe - 26, ye - 4, xe + 26, ye + 48), outline=(250, 250, 250), width=10)
    sway = 6 * math.sin(T * 9)   # traqueteo suave: una franja de sombra que se mueve
    d.rectangle((0, 1550 - oy + sway, BW2, 1570 - oy + sway), fill=(0, 0, 0, 30))


def _anden():
    im = _grad((40, 44, 60), (20, 22, 32)); d = ImageDraw.Draw(im)
    for y in range(0, 1300, 90):
        for x in range(0, BW2, 90): d.rectangle((x + 3, y + 3, x + 87, y + 87), fill=(235, 235, 240) if (x // 90 + y // 90) % 2 else (225, 228, 235))
    d.rectangle((0, 1180, BW2, 1300), fill=(200, 60, 70))
    d.rectangle((0, 1300, BW2, 1560), fill=(30, 30, 40))     # vía (el tren pasa en _amb)
    d.rectangle((0, 1560, BW2, 1600), fill=(250, 210, 50))   # línea amarilla
    d.rectangle((0, 1600, BW2, BH2), fill=(150, 150, 160))
    for x in range(0, BW2, 100): d.line((x, 1600, x, BH2), fill=(135, 135, 145), width=3)
    d.rounded_rectangle((380, 220, 820, 340), radius=16, fill=(20, 24, 30)); d.rectangle((410, 260, 790, 300), fill=(255, 170, 40))   # panel de horarios (sin texto)
    return im


def _anden_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    x0 = (T * 1500) % (BW2 + 2600) - 2600 - ox   # tren pasando (franjas, sin parpadeos)
    for k in range(3):
        x = x0 + k * 880; d.rounded_rectangle((x, 600 - oy, x + 860, 1520 - oy), radius=50, fill=(235, 240, 245))
        d.rectangle((x, 1180 - oy, x + 860, 1240 - oy), fill=(60, 120, 200))
        for j in range(3): d.rounded_rectangle((x + 60 + j * 270, 720 - oy, x + 260 + j * 270, 1000 - oy), radius=24, fill=(50, 60, 90))


# ---------------- 4. Prado con bosque (Pokémon / bichos) ----------------
def _prado(night=False):
    sky = ((20, 30, 70), (60, 60, 120)) if night else ((150, 215, 255), (220, 245, 255))
    im = _grad(sky[0], sky[1], h=1150); full = Image.new("RGBA", (BW2, BH2)); full.paste(im.crop((0, 0, BW2, 1150)), (0, 0)); im = full
    d = ImageDraw.Draw(im); rnd = random.Random(14)
    if night: _stars(d, rnd, 70, 900); d.ellipse((820, 200, 960, 340), fill=(255, 245, 210))
    g1 = (40, 90, 60) if night else (70, 160, 80); g2 = (30, 70, 50) if night else (90, 190, 90)
    for k in range(9):   # árboles del fondo
        x = -40 + k * 150 + rnd.randint(-20, 20); y = 1150; h = rnd.randint(300, 460)
        d.rectangle((x + 50, y - 160, x + 80, y), fill=(90, 60, 40))
        for j in range(3): d.ellipse((x - 10 + j * 30, y - h + j * 70, x + 140 - j * 20, y - h + 220 + j * 50), fill=_shade(g1, 1 + 0.08 * j))
    d.rectangle((0, 1150, BW2, BH2), fill=g2)
    for _ in range(260):   # briznas de hierba
        x, y = rnd.uniform(0, BW2), rnd.uniform(1160, BH2); d.line((x, y, x + rnd.uniform(-8, 8), y - rnd.uniform(16, 34)), fill=_shade(g2, 0.8), width=4)
    return im


def _prado_amb(im, T, ox, oy, night=False):
    d = ImageDraw.Draw(im); rnd = random.Random(2)
    if night:
        for k in range(22):   # luciérnagas que se encienden despacio
            x = rnd.uniform(0, BW2) + 50 * math.sin(T * 0.7 + k) - ox; y = rnd.uniform(900, 1800) + 30 * math.cos(T * 0.9 + k) - oy
            a = int(120 + 120 * math.sin(T * 1.2 + k * 1.3)); d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(230, 255, 120, max(0, a)))
        return
    for k in range(5):   # mariposas
        x = rnd.uniform(100, BW2 - 100) + 160 * math.sin(T * 0.6 + k * 1.7) - ox; y = rnd.uniform(900, 1500) + 60 * math.sin(T * 1.3 + k) - oy
        f = abs(math.sin(T * 9 + k)); c = [(255, 140, 60), (250, 230, 80), (140, 170, 255), (255, 120, 200), (255, 255, 255)][k]
        d.ellipse((x - 26 * f - 4, y - 18, x - 2, y + 4), fill=c); d.ellipse((x + 2, y - 18, x + 26 * f + 4, y + 4), fill=c); d.line((x, y - 14, x, y + 10), fill=(40, 30, 30), width=4)


# ---------------- 5. Cafetería-librería ----------------
def _cafe():
    im = _grad((110, 70, 50), (60, 36, 28)); d = ImageDraw.Draw(im); rnd = random.Random(31)
    EC._shelves(d, 40, BW2 - 40, 100, 760, rnd)
    d.rectangle((0, 760, BW2, 1300), fill=(150, 100, 70))
    for k in range(4):   # pizarra del menú (solo dibujitos)
        x = 90 + k * 270; d.rounded_rectangle((x, 830, x + 220, 1010), radius=12, fill=(40, 46, 44)); d.ellipse((x + 70, 870, x + 150, 950), outline=(240, 240, 230), width=6); d.arc((x + 140, 890, x + 180, 930), 270, 90, fill=(240, 240, 230), width=6)
    # barra con cafetera
    d.rectangle((0, 1300, BW2, 1380), fill=(90, 56, 40)); d.rectangle((0, 1380, BW2, 1560), fill=(120, 76, 52))
    d.rounded_rectangle((780, 1080, 1040, 1300), radius=20, fill=(190, 190, 200)); d.rectangle((830, 1200, 990, 1230), fill=(60, 60, 70)); d.ellipse((880, 1240, 940, 1290), fill=(250, 250, 250))
    d.rectangle((0, 1560, BW2, BH2), fill=(80, 50, 40))
    for x in range(0, BW2, 110): d.line((x, 1560, x + 60, BH2), fill=(70, 44, 34), width=4)
    return im


def _cafe_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    for k in range(6):   # vapor de la cafetera
        u = (T * 0.4 + k / 6) % 1; x = 910 - ox + 30 * math.sin(T * 1.6 + k * 2); y = 1060 - oy - u * 380; r = 18 + u * 40
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, int(110 * (1 - u))))
    for k in range(5):   # lámparas colgantes balanceándose
        x = 120 + k * 240 - ox; a = 0.05 * math.sin(T * 1.3 + k); cx = x + 200 * math.sin(a); cy = 200 * math.cos(a) - oy + 20
        d.line((x, -oy, cx, cy), fill=(30, 20, 16), width=4); d.chord((cx - 50, cy - 10, cx + 50, cy + 60), 180, 360, fill=(240, 180, 70))
        d.ellipse((cx - 70, cy + 10, cx + 70, cy + 90), fill=(255, 220, 140, 50))


def _cafe_mesa():
    im = _grad((70, 50, 60), (40, 28, 34)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((80, 200, 560, 900), radius=30, fill=(40, 60, 100))   # ventana con lluvia (lluvia en _amb)
    d.rounded_rectangle((80, 200, 560, 900), radius=30, outline=(110, 76, 52), width=20); d.line((320, 200, 320, 900), fill=(110, 76, 52), width=14)
    rnd = random.Random(7)
    for _ in range(40):
        x, y = rnd.uniform(100, 540), rnd.uniform(560, 880); d.rectangle((x, y, x + 10, y + 14), fill=(255, 200, 110))
    d.rounded_rectangle((40, 1360, BW2 - 40, 1440), radius=16, fill=(160, 104, 66)); d.rectangle((0, 1440, BW2, BH2), fill=(70, 48, 40))
    # taza y pila de novelas sobre la mesa
    d.rounded_rectangle((760, 1230, 900, 1360), radius=20, fill=(250, 250, 245)); d.arc((880, 1260, 950, 1330), 270, 90, fill=(250, 250, 245), width=14)
    for k in range(5): d.rounded_rectangle((150, 1336 - k * 34, 420, 1362 - k * 34), radius=6, fill=EC.BOOKC[k + 1])
    return im


def _cafe_mesa_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im); rnd = random.Random(4)
    for k in range(40):   # lluvia suave en la ventana
        x = rnd.uniform(100, 540) - ox; y = (rnd.uniform(220, 880) + T * 260) % 660 + 220 - oy
        d.line((x, y, x - 4, y + 26), fill=(180, 210, 255, 160), width=3)
    for k in range(4):
        u = (T * 0.45 + k / 4) % 1; x = 830 - ox + 20 * math.sin(T * 2 + k); y = 1210 - oy - u * 260; r = 14 + u * 30
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, int(100 * (1 - u))))


# ---------------- 6. Barco pirata genérico ----------------
def _barco(night=False):
    sky = ((20, 26, 60), (50, 60, 110)) if night else ((120, 190, 250), (200, 230, 255))
    im = _grad(sky[0], sky[1], h=1100); full = Image.new("RGBA", (BW2, BH2)); full.paste(im.crop((0, 0, BW2, 1100)), (0, 0)); im = full
    d = ImageDraw.Draw(im); rnd = random.Random(12)
    if night: _stars(d, rnd, 80, 900); d.ellipse((200, 180, 330, 310), fill=(255, 245, 210))
    d.rectangle((0, 1000, BW2, 1300), fill=(30, 70, 130) if not night else (20, 36, 70))
    # mástil y vela (lisa, sin símbolos)
    d.rectangle((560, 0, 600, 1350), fill=(110, 70, 40))
    d.polygon([(300, 140), (860, 140), (900, 700), (260, 700)], fill=(245, 236, 210) if not night else (200, 194, 176))
    d.line((300, 140, 860, 140), fill=(90, 56, 30), width=16); d.line((260, 700, 900, 700), fill=(90, 56, 30), width=16)
    for k in range(4): d.line((60 + k * 40, 1300, 560, 160), fill=(80, 56, 36), width=4)   # jarcias
    # barandilla y cubierta de madera
    d.rectangle((0, 1300, BW2, 1340), fill=(120, 76, 44))
    for x in range(0, BW2, 90): d.rectangle((x, 1340, x + 26, 1480), fill=(120, 76, 44))
    d.rectangle((0, 1480, BW2, 1520), fill=(100, 62, 36))
    d.rectangle((0, 1520, BW2, BH2), fill=(150, 100, 60))
    for y in range(1520, BH2, 70): d.line((0, y, BW2, y), fill=(120, 78, 46), width=5)
    # timón genérico
    cx, cy = 1000, 1380; d.ellipse((cx - 110, cy - 110, cx + 110, cy + 110), outline=(90, 56, 30), width=22)
    for k in range(8): a = k * math.pi / 4; d.line((cx, cy, cx + 150 * math.cos(a), cy + 150 * math.sin(a)), fill=(90, 56, 30), width=16)
    # barriles
    for x in (80, 230): d.rounded_rectangle((x, 1560, x + 130, 1760), radius=30, fill=(130, 84, 46)); d.rectangle((x, 1600, x + 130, 1614), fill=(70, 70, 80)); d.rectangle((x, 1700, x + 130, 1714), fill=(70, 70, 80))
    return im


def _barco_amb(im, T, ox, oy, night=False):
    d = ImageDraw.Draw(im)
    for k in range(4):   # olas del mar
        y = 1030 + k * 60 - oy
        pts = [(x - ox, y + 14 * math.sin(x / 90 + T * 1.8 + k)) for x in range(0, BW2 + 40, 40)]
        d.line(pts, fill=(255, 255, 255, 120), width=6)
    if not night:
        for k in range(3):
            x = (k * 420 + T * 70) % (BW2 + 300) - 150 - ox; y = 380 + k * 110 - oy; f = 18 * math.sin(T * 6 + k)
            d.line([(x - 36, y - f), (x, y), (x + 36, y - f)], fill=(255, 255, 255), width=6)


def bob_barco(T, amp=1.0):
    """balanceo del barco: se aplica girando el fondo un poco (lo usa la escena)"""
    return 1.6 * amp * math.sin(T * 1.1)


# ---------------- 7. Azotea con ciudad de neón ----------------
NEON = [(255, 80, 180), (80, 220, 255), (180, 110, 255), (255, 200, 80)]


def _azotea():
    im = _grad((20, 10, 50), (70, 20, 90), h=1300); full = Image.new("RGBA", (BW2, BH2), (40, 36, 50, 255)); full.paste(im.crop((0, 0, BW2, 1300)), (0, 0)); im = full
    d = ImageDraw.Draw(im); rnd = random.Random(41)
    _stars(d, rnd, 50, 600)
    x = -20
    while x < BW2:
        bw = rnd.randint(100, 190); bh = rnd.randint(400, 950); d.rectangle((x, 1300 - bh, x + bw, 1300), fill=(30 + rnd.randint(0, 20), 20, 60))
        for yy in range(1300 - bh + 30, 1280, 48):
            for xx in range(x + 14, x + bw - 22, 34):
                if rnd.random() < 0.3: d.rectangle((xx, yy, xx + 14, yy + 22), fill=rnd.choice([(255, 200, 120), (140, 220, 255)]))
        x += bw + 10
    d.rectangle((0, 1300, BW2, 1380), fill=(80, 76, 96))   # muro de la azotea
    d.rectangle((0, 1380, BW2, BH2), fill=(56, 54, 70))
    for x in range(0, BW2, 150): d.line((x, 1380, x - 40, BH2), fill=(50, 48, 62), width=4)
    d.rectangle((900, 1100, 1120, 1300), fill=(110, 110, 130)); d.ellipse((960, 1140, 1060, 1240), fill=(80, 80, 96))   # aire acondicionado
    return im


def _azotea_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    for k, (x, y, w, h) in enumerate([(120, 520, 160, 60), (480, 420, 90, 220), (760, 600, 200, 50), (300, 760, 120, 120)]):   # carteles de neón (sin letras) con pulso lento
        v = 0.65 + 0.35 * math.sin(T * 1.4 + k * 1.7); c = tuple(int(cc * v) for cc in NEON[k])
        d.rounded_rectangle((x - ox - 10, y - oy - 10, x + w - ox + 10, y + h - oy + 10), radius=18, fill=c + (60,))
        d.rounded_rectangle((x - ox, y - oy, x + w - ox, y + h - oy), radius=12, outline=c, width=8)
    v = (T * 140) % (BW2 + 400) - 200   # avión lejano con luz lenta
    d.ellipse((v - ox, 260 - oy, v + 10 - ox, 270 - oy), fill=(255, 120, 120, int(140 + 100 * math.sin(T * 2))))


def _callejon():
    im = _grad((30, 16, 50), (14, 8, 24)); d = ImageDraw.Draw(im)
    d.polygon([(0, 0), (380, 400), (380, 1500), (0, BH2)], fill=(50, 34, 70)); d.polygon([(BW2, 0), (820, 400), (820, 1500), (BW2, BH2)], fill=(44, 30, 64))
    d.rectangle((380, 400, 820, 1500), fill=(26, 16, 40))
    d.polygon([(0, BH2), (380, 1500), (820, 1500), (BW2, BH2)], fill=(36, 30, 46))
    for k in range(6): d.line((600, 1500, -200 + k * 320, BH2), fill=(46, 40, 58), width=4)
    for k in range(5):   # cables y farolillos
        y = 300 + k * 160; d.line((0, y, BW2, y + 60), fill=(20, 14, 26), width=4)
    return im


def _callejon_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    for k in range(6):
        sg = -1 if k % 2 else 1; x = (200 if sg > 0 else 1000) + sg * (k // 2) * 60 - ox; y = 420 + (k // 2) * 330 - oy
        v = 0.65 + 0.35 * math.sin(T * 1.2 + k); c = tuple(int(cc * v) for cc in NEON[k % 4])
        d.rounded_rectangle((x - 70, y, x + 70, y + 200), radius=14, fill=c + (70,)); d.rounded_rectangle((x - 60, y + 10, x + 60, y + 190), radius=10, outline=c, width=8)
    for k in range(4):   # charcos con reflejo
        x = 300 + k * 200 - ox; y = 1700 + (k % 2) * 140 - oy; c = NEON[k]
        d.ellipse((x - 90, y - 18, x + 90, y + 18), fill=c + (int(60 + 30 * math.sin(T * 1.5 + k)),))


# ---------------- 8. Alfombra roja / gala ----------------
def _gala():
    im = _grad((30, 10, 24), (10, 4, 10)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, BW2, 1150), fill=(24, 8, 22))
    for k in range(6):   # photocall genérico: estrellas doradas (sin logos)
        for j in range(4):
            x = 100 + k * 190 + (j % 2) * 95; y = 160 + j * 230; r = 34
            pts = [(x + (r if q % 2 == 0 else r * 0.45) * math.cos(-math.pi / 2 + q * math.pi / 5), y + (r if q % 2 == 0 else r * 0.45) * math.sin(-math.pi / 2 + q * math.pi / 5)) for q in range(10)]
            d.polygon(pts, fill=(200, 160, 70))
    d.rectangle((0, 1150, BW2, BH2), fill=(30, 20, 30))
    d.polygon([(380, 1150), (820, 1150), (1150, BH2), (50, BH2)], fill=(190, 20, 40))   # alfombra
    d.polygon([(380, 1150), (820, 1150), (830, 1170), (370, 1170)], fill=(150, 10, 30))
    for x0, sg in ((300, -1), (900, 1)):   # postes con cordón
        for k in range(4):
            x = x0 + sg * k * 90; y = 1250 + k * 200; d.rectangle((x - 10, y - 160, x + 10, y), fill=(230, 190, 80)); d.ellipse((x - 26, y - 186, x + 26, y - 134), fill=(240, 205, 100))
        pts = [(x0 + sg * k * 90, 1250 + k * 200 - 150 + 40 * math.sin(math.pi * (k % 1))) for k in range(4)]
        d.line(pts, fill=(160, 20, 40), width=16)
    return im


def _gala_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    for k in range(2):   # focos que barren despacio (nada de flashes)
        a = 0.35 * math.sin(T * 0.7 + k * 2.4); top = (300 + k * 600 - ox, -oy)
        d.polygon([top, (top[0] + 900 * math.sin(a) - 220, 1900 - oy), (top[0] + 900 * math.sin(a) + 220, 1900 - oy)], fill=(255, 240, 200, 30))
    rnd = random.Random(6)
    for k in range(20):   # purpurina cayendo despacio
        x = rnd.uniform(0, BW2) + 20 * math.sin(T + k) - ox; y = (rnd.uniform(0, 1200) + T * 50) % 1200 - oy
        d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 220, 120, int(150 + 80 * math.sin(T * 1.3 + k))))


def _gala_escenario():
    im = _grad((40, 14, 30), (14, 6, 12)); d = ImageDraw.Draw(im)
    for k in range(10): x = k * 125 - 20; d.rectangle((x, 0, x + 85, 1400), fill=(120, 20, 40)); d.rectangle((x + 85, 0, x + 125, 1400), fill=(90, 12, 30))
    d.rectangle((0, 0, BW2, 140), fill=(150, 110, 40))
    d.rectangle((0, 1400, BW2, BH2), fill=(60, 36, 30)); d.rectangle((0, 1400, BW2, 1440), fill=(220, 180, 80))
    d.polygon([(440, 1100), (760, 1100), (720, 1400), (480, 1400)], fill=(70, 50, 40)); d.rectangle((430, 1080, 770, 1110), fill=(200, 160, 70))   # atril
    return im


def _gala_escenario_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    d.polygon([(600 - ox, -oy), (250 - ox + 60 * math.sin(T * 0.6), 1500 - oy), (950 - ox + 60 * math.sin(T * 0.6), 1500 - oy)], fill=(255, 245, 210, 34))


# ---------------- 9. Observatorio de noche ----------------
def _observatorio():
    im = _grad((8, 10, 36), (30, 30, 80)); d = ImageDraw.Draw(im); rnd = random.Random(19)
    _stars(d, rnd, 160, 1300)
    d.ellipse((140, 160, 300, 320), fill=(240, 236, 220)); d.ellipse((190, 190, 230, 230), fill=(215, 210, 196)); d.ellipse((240, 250, 262, 272), fill=(215, 210, 196))
    pts = [(0, 1350)] + [(x, 1230 - 80 * abs(math.sin(x / 300 + 0.6))) for x in range(0, BW2 + 20, 20)] + [(BW2, 1350)]
    d.polygon(pts, fill=(26, 30, 60))
    d.chord((620, 900, 1060, 1340), 180, 360, fill=(200, 205, 220)); d.rectangle((620, 1120, 1060, 1400), fill=(180, 186, 200))   # cúpula
    d.polygon([(810, 905), (870, 905), (880, 1120), (800, 1120)], fill=(30, 30, 50))
    d.rectangle((0, 1400, BW2, BH2), fill=(40, 40, 64))
    for x in range(0, BW2, 120): d.line((x, 1400, x - 60, BH2), fill=(50, 50, 76), width=3)
    # telescopio en primer plano
    d.line((300, 1820, 380, 1500), fill=(80, 80, 96), width=14); d.line((460, 1820, 380, 1500), fill=(80, 80, 96), width=14)
    d.polygon([(330, 1480), (590, 1280), (620, 1330), (360, 1530)], fill=(230, 230, 240)); d.ellipse((580, 1270, 640, 1340), fill=(120, 170, 255))
    return im


def _observatorio_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im); rnd = random.Random(23)
    for k in range(40):   # estrellas que titilan despacio
        x, y = rnd.uniform(0, BW2) - ox, rnd.uniform(0, 1150) - oy; a = int(120 + 120 * math.sin(T * 1.1 + k * 0.9)); r = 3
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 230, max(0, a)))
    u = (T * 0.25) % 1   # estrella fugaz lenta
    x = 1100 - u * 900 - ox; y = 150 + u * 380 - oy
    if u < 0.6: d.line((x, y, x + 150, y - 64), fill=(255, 255, 255, int(200 * (1 - u / 0.6))), width=5)


def _espacio():
    im = _grad((6, 4, 20), (20, 8, 40)); d = ImageDraw.Draw(im); rnd = random.Random(29)
    _stars(d, rnd, 260, BH2)
    _glow(im, 300, 500, 300, (140, 60, 200), 70, 120); _glow(im, 900, 1300, 260, (40, 120, 220), 60, 120)
    d = ImageDraw.Draw(im)
    d.ellipse((620, 300, 1020, 700), fill=(240, 150, 90)); d.arc((520, 440, 1120, 560), 160, 380, fill=(250, 220, 170), width=14)
    for k in range(4): d.arc((640, 330 + k * 80, 1000, 420 + k * 80), 0, 180, fill=(220, 120, 70), width=10)
    return im


def _espacio_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im); rnd = random.Random(5)
    for k in range(12):
        x = (rnd.uniform(0, BW2) - T * 40 * rnd.uniform(0.5, 1.5)) % BW2 - ox; y = rnd.uniform(0, BH2) - oy
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(255, 255, 255, 200))


# ---------------- 10. Karaoke ----------------
def _karaoke():
    im = _grad((40, 14, 70), (16, 6, 30)); d = ImageDraw.Draw(im)
    for x in range(0, BW2, 60): d.line((x, 0, x, 1400), fill=(48, 18, 80), width=3)   # paneles acolchados
    d.rounded_rectangle((180, 260, 1020, 760), radius=20, fill=(20, 20, 30)); d.rounded_rectangle((210, 290, 990, 730), radius=10, fill=(30, 50, 120))   # pantalla
    d.rectangle((0, 1400, BW2, BH2), fill=(30, 20, 40))
    d.rounded_rectangle((-40, 1180, 560, 1460), radius=60, fill=(200, 40, 100)); d.rounded_rectangle((-40, 1300, 560, 1470), radius=40, fill=(230, 60, 120))   # sofá
    d.rounded_rectangle((640, 1380, 1080, 1440), radius=14, fill=(60, 50, 80)); d.rectangle((680, 1440, 710, 1700), fill=(50, 40, 70)); d.rectangle((1010, 1440, 1040, 1700), fill=(50, 40, 70))   # mesa
    for k in range(3): d.rounded_rectangle((690 + k * 120, 1290, 760 + k * 120, 1384), radius=14, fill=[(255, 200, 80), (120, 220, 255), (255, 120, 160)][k])   # vasos
    return im


def _karaoke_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    for k in range(4):   # barras de letra que se van llenando (sin texto)
        y = 380 + k * 90 - oy; x0 = 280 - ox; w = 640 - k * 60; fill = ((T * 0.5 - k * 0.25) % 1.4) / 1.0
        d.rounded_rectangle((x0, y, x0 + w, y + 40), radius=20, fill=(255, 255, 255, 120))
        d.rounded_rectangle((x0, y, x0 + int(w * min(1, max(0, fill))), y + 40), radius=20, fill=(255, 220, 80, 230))
    cx, cy = 600 - ox, 170 - oy   # bola de espejos girando y reflejos lentos
    d.line((cx, -oy, cx, cy - 60), fill=(200, 200, 210), width=4); d.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), fill=(200, 200, 215))
    for j in range(5):
        for i in range(6):
            a = i * math.pi / 3 + T * 1.2; x = cx + 60 * math.cos(a) * math.sin(math.pi * (j + 0.5) / 5); y = cy - 60 + j * 26
            if math.cos(a) > 0: d.rectangle((x - 8, y - 8, x + 8, y + 8), fill=(255, 255, 255))
    rnd = random.Random(9)
    for k in range(14):
        a = rnd.uniform(0, 6.28) + T * 0.6; r = rnd.uniform(300, 900); x = cx + r * math.cos(a); y = cy + 600 + 0.6 * r * math.sin(a)
        d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=NEON[k % 4] + (110,))


def _karaoke_esc():
    im = _grad((20, 6, 40), (6, 2, 14)); d = ImageDraw.Draw(im)
    d.rectangle((0, 1450, BW2, BH2), fill=(40, 26, 60)); d.rectangle((0, 1450, BW2, 1480), fill=(255, 80, 180))
    for k in range(8):   # altavoces
        x = 40 if k < 4 else BW2 - 220; y = 700 + (k % 4) * 180; d.rounded_rectangle((x, y, x + 180, y + 170), radius=14, fill=(30, 26, 40)); d.ellipse((x + 40, y + 30, x + 140, y + 130), fill=(60, 56, 80))
    return im


def _karaoke_esc_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    for k in range(4):
        a = 0.4 * math.sin(T * 0.8 + k * 1.6); top = (200 + k * 270 - ox, -oy)
        d.polygon([top, (top[0] + 1300 * math.sin(a) - 150, 1500 - oy), (top[0] + 1300 * math.sin(a) + 150, 1500 - oy)], fill=NEON[k] + (40,))
    for k in range(8):   # ecualizador del suelo (barras que suben y bajan suave)
        h = 60 + 50 * (1 + math.sin(T * 3 + k * 0.9)); x = 330 + k * 70 - ox
        d.rounded_rectangle((x, 1440 - h - oy, x + 46, 1440 - oy), radius=10, fill=NEON[k % 4] + (200,))


NUEVOS = {
    "carretera": (_carretera, _carretera_amb), "isekai": (_isekai, _isekai_amb),
    "playa": (lambda: _playa(False), lambda im, T, ox, oy: _playa_amb(im, T, ox, oy, False)),
    "playa_tarde": (lambda: _playa(True), lambda im, T, ox, oy: _playa_amb(im, T, ox, oy, True)),
    "metro": (_metro, _metro_amb), "anden": (_anden, _anden_amb),
    "prado": (lambda: _prado(False), lambda im, T, ox, oy: _prado_amb(im, T, ox, oy, False)),
    "prado_noche": (lambda: _prado(True), lambda im, T, ox, oy: _prado_amb(im, T, ox, oy, True)),
    "cafe": (_cafe, _cafe_amb), "cafe_mesa": (_cafe_mesa, _cafe_mesa_amb),
    "barco": (lambda: _barco(False), lambda im, T, ox, oy: _barco_amb(im, T, ox, oy, False)),
    "barco_noche": (lambda: _barco(True), lambda im, T, ox, oy: _barco_amb(im, T, ox, oy, True)),
    "azotea": (_azotea, _azotea_amb), "callejon": (_callejon, _callejon_amb),
    "gala": (_gala, _gala_amb), "gala_escenario": (_gala_escenario, _gala_escenario_amb),
    "observatorio": (_observatorio, _observatorio_amb), "espacio": (_espacio, _espacio_amb),
    "karaoke": (_karaoke, _karaoke_amb), "karaoke_esc": (_karaoke_esc, _karaoke_esc_amb),
}


def instalar2():
    EC.SCEN.update(NUEVOS); EC.instalar()


if __name__ == "__main__":   # hoja de contacto de todos los escenarios: python3 escenarios2.py salida.jpg
    import sys
    instalar2(); names = list(NUEVOS); cols = 5; tw, th = 216, 384
    sheet = Image.new("RGB", (cols * tw, ((len(names) + cols - 1) // cols) * th))
    for i, n in enumerate(names): sheet.paste(EC.bg(n, 1.0).convert("RGB").resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
    sheet.save(sys.argv[1])
