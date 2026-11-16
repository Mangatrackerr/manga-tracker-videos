# Escenarios nuevos (16/11/2026): cada vídeo con su sitio propio + animación ambiental + cámara que se mueve despacio.
# Se enganchan al kit animado con escenarios.instalar(): A("ramen", ...), A("cine_hall", ...), etc.
# Todo dibujado aquí (sin imágenes ni logos de terceros, sin textos de marcas).
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import animado as AN
from engine_satira import W, H, WHITE, YEL

MG = 120; BW2, BH2 = W + MG, H + MG


def _grad(c1, c2, h=BH2, w=BW2):
    return Image.fromarray(np.linspace(c1, c2, h)[:, None, :].repeat(w, 1).astype(np.uint8)).convert("RGBA")


def _shade(c, k): return tuple(int(max(0, min(255, v * k))) for v in c)


# ---------------- 1. Tienda de ramen ----------------
def _ramen():
    im = _grad((120, 60, 34), (70, 34, 20)); d = ImageDraw.Draw(im)
    for x in range(0, BW2, 90): d.rectangle((x, 0, x + 6, 1420), fill=(96, 46, 26))           # listones de madera
    # noren (cortinilla) arriba
    for k in range(6):
        x = 40 + k * 175; d.rectangle((x, 60, x + 160, 380), fill=(30, 40, 90)); d.ellipse((x + 50, 170, x + 110, 230), fill=(240, 240, 240))
    d.rectangle((0, 40, BW2, 70), fill=(60, 40, 30))
    # tablillas de menú con cuencos dibujados
    for k in range(5):
        x = 70 + k * 210; d.rounded_rectangle((x, 470, x + 170, 700), radius=10, fill=(245, 230, 200))
        d.chord((x + 30, 560, x + 140, 660), 0, 180, fill=(210, 60, 50)); d.rectangle((x + 30, 600, x + 140, 610), fill=(250, 210, 120))
    # estantería con cuencos
    d.rectangle((60, 860, BW2 - 60, 880), fill=(60, 30, 18))
    for k in range(8): x = 110 + k * 125; d.chord((x, 790, x + 90, 870), 0, 180, fill=[(230, 230, 235), (210, 60, 50)][k % 2])
    # barra al fondo y suelo
    d.rectangle((0, 1420, BW2, 1460), fill=(150, 96, 60)); d.rectangle((0, 1460, BW2, 1600), fill=(110, 66, 40))
    d.rectangle((0, 1600, BW2, BH2), fill=(64, 52, 48))
    for x in range(0, BW2, 140):
        for y in range(1600, BH2, 140): d.rectangle((x + 4, y + 4, x + 136, y + 136), outline=(80, 66, 60), width=4)
    return im


def _ramen_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    for k in range(4):   # farolillos que se balancean
        x = 160 + k * 260 - ox; a = 0.08 * math.sin(T * 1.6 + k); top = 0 - oy
        cx = x + 260 * math.sin(a); cy = top + 300
        d.line((x, top, cx, cy - 70), fill=(40, 20, 10), width=5)
        d.ellipse((cx - 60, cy - 80, cx + 60, cy + 80), fill=(225, 60, 50)); d.rectangle((cx - 40, cy - 90, cx + 40, cy - 70), fill=(40, 26, 20)); d.rectangle((cx - 40, cy + 70, cx + 40, cy + 90), fill=(40, 26, 20))
        for j in (-30, 0, 30): d.line((cx - 58, cy + j, cx + 58, cy + j), fill=(190, 40, 34), width=3)


def _cocina():
    im = _grad((230, 236, 240), (190, 200, 210)); d = ImageDraw.Draw(im)
    for x in range(0, BW2, 100):
        for y in range(0, 1450, 100): d.rectangle((x + 3, y + 3, x + 97, y + 97), outline=(205, 214, 222), width=5)
    d.rectangle((0, 300, BW2, 330), fill=(140, 140, 150))
    for k in range(6):   # cazos colgados
        x = 120 + k * 170; d.line((x, 330, x, 420), fill=(100, 100, 110), width=6); d.ellipse((x - 50, 420, x + 50, 500), fill=(170, 170, 185))
    d.rectangle((0, 1400, BW2, 1460), fill=(120, 120, 130)); d.rectangle((0, 1460, BW2, BH2), fill=(70, 72, 82))
    # olla grande
    d.rounded_rectangle((90, 1080, 470, 1400), radius=30, fill=(150, 150, 165)); d.rectangle((70, 1070, 490, 1110), fill=(120, 120, 135))
    return im


def _cocina_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    for k in range(7):   # vapor de la olla
        u = (T * 0.35 + k / 7) % 1; x = 280 - ox + 60 * math.sin(T * 1.4 + k * 2) ; y = 1060 - oy - u * 600; r = 30 + u * 70
        a = int(110 * (1 - u)); d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, a))


# ---------------- 2. Cine ----------------
def _cine():
    im = _grad((26, 12, 30), (8, 4, 12)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 70, BH2), fill=(110, 16, 36)); d.rectangle((BW2 - 70, 0, BW2, BH2), fill=(110, 16, 36))
    d.rounded_rectangle((110, 120, BW2 - 110, 760), radius=14, fill=(40, 40, 56))
    d.rectangle((0, 1560, BW2, BH2), fill=(60, 14, 30))
    for k in range(12): d.ellipse((60 + k * 95, 1600, 80 + k * 95, 1620), fill=(230, 200, 90))   # luces de pasillo
    return im


def _cine_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 130 - ox, 140 - oy, BW2 - 130 - ox, 740 - oy
    d.rectangle((x0, y0, x1, y1), fill=(230, 235, 255))
    for k in range(4):   # formas abstractas en la pantalla (nada de personajes)
        cx = x0 + (x1 - x0) * (0.5 + 0.38 * math.sin(T * 0.9 + k * 1.6)); cy = y0 + (y1 - y0) * (0.5 + 0.3 * math.cos(T * 0.7 + k))
        r = 70 + 20 * math.sin(T * 2 + k); d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=[(255, 120, 160), (120, 190, 255), (255, 210, 90), (150, 240, 170)][k])
    # haz del proyector
    d.polygon([((x0 + x1) / 2 - 30, BH2 - oy), (x0 + 40, y1), (x1 - 40, y1)], fill=(255, 255, 230, 18 + int(6 * math.sin(T * 7))))


def cine_butacas(im, T, u=0):
    """fila de butacas delante (prop 'draw' con front=True)"""
    d = ImageDraw.Draw(im)
    for k in range(7):
        x = -40 + k * 175; d.rounded_rectangle((x, 1640, x + 160, 1940), radius=40, fill=(170, 26, 46)); d.rounded_rectangle((x + 12, 1660, x + 148, 1720), radius=26, fill=(200, 40, 62))


def _hall():
    im = _grad((70, 26, 60), (34, 12, 30)); d = ImageDraw.Draw(im)
    cols = [(240, 90, 120), (90, 170, 255), (255, 200, 70), (130, 230, 160)]
    for k in range(4):   # carteles abstractos (sin marcas)
        x = 70 + k * 260; d.rounded_rectangle((x, 280, x + 210, 620), radius=10, fill=(250, 220, 120)); d.rectangle((x + 16, 296, x + 194, 604), fill=cols[k])
        d.ellipse((x + 60, 360, x + 150, 450), fill=(255, 255, 255)); d.polygon([(x + 30, 590), (x + 105, 470), (x + 180, 590)], fill=_shade(cols[k], 0.6))
    d.rectangle((0, 1500, BW2, BH2), fill=(150, 30, 50))
    for k in range(20):
        x = (k * 97) % BW2; y = 1530 + (k * 53) % 380; d.ellipse((x, y, x + 26, y + 26), fill=(120, 20, 40))
    # máquina de palomitas
    d.rounded_rectangle((760, 900, 1060, 1500), radius=20, fill=(210, 40, 50)); d.rectangle((790, 940, 1030, 1200), fill=(255, 240, 200))
    for k in range(40): d.ellipse((800 + (k * 37) % 220, 1100 + (k * 23) % 90, 824 + (k * 37) % 220, 1124 + (k * 23) % 90), fill=(255, 250, 230))
    return im


def _hall_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    for k in range(30):   # bombillas de marquesina que se encienden en ola (suave, sin parpadeo)
        x = 40 + k * 36 - ox; v = 0.5 + 0.5 * math.sin(T * 2.4 - k * 0.5); c = (int(150 + 105 * v), int(120 + 100 * v), 60)
        d.ellipse((x - 10, 200 - oy, x + 10, 220 - oy), fill=c)
    for k in range(6):   # palomitas saltando
        u = (T * 0.9 + k / 6) % 1; x = 820 + k * 36 - ox; y = 1060 - oy - 90 * math.sin(math.pi * u); d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=(255, 250, 225))


# ---------------- 3. Biblioteca ----------------
BOOKC = [(200, 60, 70), (60, 120, 200), (240, 180, 60), (90, 170, 110), (150, 90, 200), (230, 120, 60), (60, 160, 170), (240, 240, 230)]


def _shelves(d, x0, x1, y0, y1, rnd):
    d.rectangle((x0 - 20, y0 - 20, x1 + 20, y1), fill=(90, 56, 34))
    y = y0
    while y < y1 - 200:
        x = x0
        while x < x1 - 20:
            w = rnd.randint(26, 46); h = rnd.randint(130, 175); c = rnd.choice(BOOKC)
            d.rectangle((x, y + 190 - h, x + w, y + 190), fill=c); d.rectangle((x + 4, y + 190 - h + 20, x + w - 4, y + 190 - h + 28), fill=_shade(c, 0.7)); x += w + 3
        d.rectangle((x0 - 20, y + 190, x1 + 20, y + 210), fill=(70, 42, 26)); y += 230


def _biblio():
    im = _grad((70, 52, 46), (40, 30, 28)); d = ImageDraw.Draw(im); rnd = random.Random(3)
    _shelves(d, 40, 470, 120, 1500, rnd); _shelves(d, 730, BW2 - 40, 120, 1500, rnd)
    d.rounded_rectangle((520, 200, 680, 760), radius=80, fill=(60, 80, 130)); d.line((600, 200, 600, 760), fill=(90, 60, 40), width=10)  # ventana
    d.rectangle((0, 1500, BW2, BH2), fill=(110, 70, 46))
    for x in range(0, BW2, 120): d.line((x, 1500, x - 60, BH2), fill=(90, 56, 36), width=4)
    return im


def _biblio_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im); rnd = random.Random(9)
    d.polygon([(520 - ox, 200 - oy), (680 - ox, 200 - oy), (900 - ox, 1500 - oy), (380 - ox, 1500 - oy)], fill=(255, 240, 190, 26))   # rayo de luz
    for k in range(26):   # motas de polvo flotando
        x = rnd.uniform(380, 900) + 40 * math.sin(T * 0.5 + k) - ox; y = (rnd.uniform(200, 1500) - T * 25 * rnd.uniform(0.5, 1.5)) % 1300 + 200 - oy
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(255, 245, 200, 150))


def _mesa():
    im = _grad((52, 70, 60), (30, 40, 34)); d = ImageDraw.Draw(im); rnd = random.Random(4)
    _shelves(d, 40, BW2 - 40, 80, 900, rnd)
    d.rectangle((0, 900, BW2, 1500), fill=(48, 64, 54))
    d.rounded_rectangle((60, 1360, BW2 - 60, 1430), radius=14, fill=(150, 100, 62)); d.rectangle((110, 1430, 150, BH2), fill=(110, 72, 44)); d.rectangle((BW2 - 150, 1430, BW2 - 110, BH2), fill=(110, 72, 44))
    for k in range(7): d.rounded_rectangle((120, 1340 - k * 34, 340, 1366 - k * 34), radius=5, fill=BOOKC[k])                         # pila de libros
    d.rectangle((BW2 - 260, 1100, BW2 - 244, 1360), fill=(60, 60, 60)); d.polygon([(BW2 - 340, 1110), (BW2 - 160, 1110), (BW2 - 210, 1010), (BW2 - 290, 1010)], fill=(70, 140, 90))  # flexo
    d.rectangle((0, 1500, BW2, BH2), fill=(100, 64, 42))
    return im


def _mesa_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    d.polygon([(BW2 - 340 - ox, 1110 - oy), (BW2 - 160 - ox, 1110 - oy), (BW2 - 60 - ox, 1360 - oy), (BW2 - 460 - ox, 1360 - oy)], fill=(255, 240, 170, 40 + int(8 * math.sin(T * 3))))


# ---------------- 4. Montaña con templo ----------------
def _montana():
    im = _grad((250, 150, 90), (120, 60, 120), h=1300).crop((0, 0, BW2, 1300)); full = Image.new("RGBA", (BW2, BH2)); full.paste(im, (0, 0)); im = full
    d = ImageDraw.Draw(im)
    d.rectangle((0, 1300, BW2, BH2), fill=(70, 50, 70))
    d.ellipse((620, 380, 900, 660), fill=(255, 220, 140))
    for layer, (col, base, amp) in enumerate([((150, 80, 120), 900, 300), ((110, 60, 100), 1080, 220), ((70, 40, 70), 1250, 160)]):
        pts = [(0, BH2)] + [(x, base - amp * abs(math.sin(x / (260 + 80 * layer) + layer))) for x in range(0, BW2 + 20, 20)] + [(BW2, BH2)]
        d.polygon(pts, fill=col)
    # torii genérico
    c = (210, 50, 40)
    d.rectangle((150, 1000, 190, 1560), fill=c); d.rectangle((470, 1000, 510, 1560), fill=c)
    d.polygon([(90, 960), (570, 960), (590, 920), (70, 920)], fill=(40, 26, 30)); d.rectangle((110, 960, 550, 995), fill=c); d.rectangle((130, 1060, 530, 1085), fill=c)
    # escalones de piedra
    for k in range(6): d.rectangle((60 + k * 30, 1560 + k * 60, BW2 - 60 - k * 30, 1610 + k * 60), fill=_shade((150, 140, 150), 1 - k * 0.07))
    return im


def _montana_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im); rnd = random.Random(11)
    for k in range(3):   # nubes que pasan
        x = (k * 420 + T * 30) % (BW2 + 500) - 300 - ox; y = 260 + k * 150 - oy
        for j, (dx, r) in enumerate([(0, 60), (70, 80), (150, 60)]): d.ellipse((x + dx - r, y - r * 0.7, x + dx + r, y + r * 0.7), fill=(255, 235, 230, 200))
    for k in range(14):  # hojas cayendo
        x0 = rnd.uniform(0, BW2); sp = rnd.uniform(70, 140); y = (rnd.uniform(0, BH2) + T * sp) % BH2 - oy; x = x0 + 50 * math.sin(T * 1.3 + k) - ox
        a = T * 2 + k; d.polygon([(x + 16 * math.cos(a), y + 16 * math.sin(a)), (x - 16 * math.cos(a), y - 16 * math.sin(a)), (x + 6 * math.sin(a), y - 6 * math.cos(a))], fill=(240, 110, 60, 230))


def _cielo():
    im = _grad((90, 160, 240), (190, 220, 255)); return im


def _cielo_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    for k in range(6):   # nubes grandes que pasan rápido (sensación de volar)
        x = (k * 300 - T * 260) % (BW2 + 600) - 300 - ox; y = 200 + (k * 330) % 1500 - oy; s = 1 + (k % 3) * 0.4
        for dx, r in [(0, 70), (90, 100), (190, 70), (100, 60)]: d.ellipse((x + dx * s - r * s, y - r * 0.6 * s, x + dx * s + r * s, y + r * 0.6 * s), fill=(255, 255, 255, 220))
    for k in range(10):  # líneas de velocidad
        y = (k * 197) % BH2 - oy; x = (BW2 - (T * 900 + k * 233) % (BW2 + 400)) - ox; d.line((x, y, x + 180, y), fill=(255, 255, 255, 120), width=5)


def nube(im, T, u=0, x=W / 2, y=1820):
    """nube bajo los pies (prop 'draw')"""
    d = ImageDraw.Draw(im); y = y + 10 * math.sin(T * 3)
    for dx, r in [(-200, 70), (-90, 95), (40, 105), (170, 80), (-20, 60)]: d.ellipse((x + dx - r, y - r * 0.55, x + dx + r, y + r * 0.55), fill=(255, 236, 140))


# ---------------- 5. Estadio ----------------
def _estadio():
    im = _grad((110, 180, 250), (200, 230, 255)); d = ImageDraw.Draw(im); rnd = random.Random(6)
    d.rectangle((0, 520, BW2, 1180), fill=(70, 70, 96))   # gradas
    for r in range(11):
        y = 540 + r * 58
        for k in range(28): d.ellipse((10 + k * 42 + (r % 2) * 20, y, 40 + k * 42 + (r % 2) * 20, y + 30), fill=rnd.choice([(240, 90, 90), (90, 150, 240), (250, 220, 90), (240, 240, 240), (120, 220, 140)]))
    d.rectangle((0, 1180, BW2, 1230), fill=(250, 250, 250))
    d.rectangle((0, 1230, BW2, BH2), fill=(210, 90, 70))   # pista
    for k in range(5): d.line((0, 1330 + k * 130, BW2, 1330 + k * 130 + 40 * k), fill=(255, 255, 255), width=8)
    d.rectangle((380, 160, 820, 440), fill=(40, 40, 50)); d.rectangle((400, 180, 800, 420), fill=(20, 24, 30))   # marcador
    return im


def _estadio_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    for k in range(3):   # banderines ondeando
        x = 120 + k * 400 - ox; d.line((x, 520 - oy, x, 300 - oy), fill=(240, 240, 240), width=8)
        pts = [(x, 300 - oy)] + [(x + j * 20, 300 - oy + 10 * math.sin(T * 5 + j * 0.8 + k)) for j in range(1, 9)] + [(x + 160, 380 - oy + 10 * math.sin(T * 5 + 6.4 + k))] + [(x, 400 - oy)]
        d.polygon(pts, fill=[(240, 70, 70), (250, 210, 60), (70, 140, 240)][k])
    for k in range(3):   # puntos del marcador
        v = 0.5 + 0.5 * math.sin(T * 2 + k); d.ellipse((470 + k * 120 - ox, 270 - oy, 530 + k * 120 - ox, 330 - oy), fill=(int(120 + 135 * v), int(220 * v), 60))


def _podio():
    im = _grad((40, 30, 80), (14, 10, 30)); d = ImageDraw.Draw(im)
    d.rectangle((0, 1560, BW2, BH2), fill=(30, 26, 50))
    for x0, h, c in [(130, 300, (190, 190, 205)), (420, 440, (250, 200, 60)), (710, 220, (205, 130, 70))]:
        d.rectangle((x0, 1560 - h, x0 + 290, 1560), fill=c); d.rectangle((x0, 1560 - h, x0 + 290, 1560 - h + 24), fill=_shade(c, 1.15))
    return im


def _podio_amb(im, T, ox, oy):
    d = ImageDraw.Draw(im)
    for k, x in enumerate((275, 565, 855)):   # focos que barren despacio
        a = 0.25 * math.sin(T * 0.8 + k * 2); top = (x + 600 * math.sin(a) - ox, -oy)
        d.polygon([top, (x - 170 - ox, 1560 - oy), (x + 170 - ox, 1560 - oy)], fill=(255, 250, 220, 34))


SCEN = {"ramen": (_ramen, _ramen_amb), "cocina": (_cocina, _cocina_amb), "cine": (_cine, _cine_amb), "cine_hall": (_hall, _hall_amb),
        "biblio": (_biblio, _biblio_amb), "biblio_mesa": (_mesa, _mesa_amb), "montana": (_montana, _montana_amb), "cielo": (_cielo, _cielo_amb),
        "estadio": (_estadio, _estadio_amb), "podio": (_podio, _podio_amb)}
_cache = {}


def base(name):
    if name not in _cache: _cache[name] = SCEN[name][0]()
    return _cache[name]


def bg(name, T, blur=False):
    b = base(name)
    ox = MG / 2 + MG / 2 * 0.8 * math.sin(T * 0.33); oy = MG / 2 + MG / 2 * 0.6 * math.cos(T * 0.27)   # cámara a la deriva
    im = b.crop((int(ox), int(oy), int(ox) + W, int(oy) + H)).copy()
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); SCEN[name][1](ov, T, int(ox), int(oy)); im.alpha_composite(ov)
    if blur: im = Image.blend(im.filter(ImageFilter.GaussianBlur(16)), Image.new("RGBA", im.size, (10, 6, 24, 255)), 0.45)
    return im


_old_bg = AN.bg


def _bg(name, T):
    if name.endswith(":blur") and name[:-5] in SCEN: return bg(name[:-5], T, blur=True)
    if name in SCEN: return bg(name, T)
    return _old_bg(name, T)


def instalar():
    AN.bg = _bg
