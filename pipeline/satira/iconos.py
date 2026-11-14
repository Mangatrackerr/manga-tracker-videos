# Iconos planos para los ganchos (dibujados con PIL a 2x, sin imágenes externas)
import math, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE)
LG = f"{P}/fonts/LuckiestGuy.ttf"; MB = f"{P}/fonts/Montserrat-Black.ttf"
S = 2; N = 640
INK = (22, 16, 30); WHITE = (255, 255, 255); YEL = (255, 225, 77); RED = (230, 50, 80)

def _new(): im = Image.new("RGBA", (N * S, N * S), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
def E(d, cx, cy, rx, ry, **kw): d.ellipse(((cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S), **kw)
def R(d, x0, y0, x1, y1, r=0, **kw): d.rounded_rectangle((x0 * S, y0 * S, x1 * S, y1 * S), radius=r * S, **kw)
def PO(d, pts, **kw): d.polygon([(x * S, y * S) for x, y in pts], **kw)
def L(d, pts, w, **kw): d.line([(x * S, y * S) for x, y in pts], width=int(w * S), joint="curve", **kw)
def T(d, cx, cy, txt, size, fill=WHITE, path=LG, stroke=0, sfill=INK):
    f = ImageFont.truetype(path, size * S); bb = f.getbbox(txt, stroke_width=stroke * S)
    d.text((cx * S - (bb[0] + bb[2]) / 2, cy * S - (bb[1] + bb[3]) / 2), txt, font=f, fill=fill, stroke_width=stroke * S, stroke_fill=sfill)
def heart(d, cx, cy, r, col=RED):
    E(d, cx - r * 0.5, cy - r * 0.2, r * 0.55, r * 0.55, fill=col); E(d, cx + r * 0.5, cy - r * 0.2, r * 0.55, r * 0.55, fill=col)
    PO(d, [(cx - r * 1.03, cy), (cx + r * 1.03, cy), (cx, cy + r * 1.05)], fill=col)
def _fin(im):
    out = im.resize((N, N), Image.LANCZOS)
    a = out.getchannel("A").filter(ImageFilter.GaussianBlur(12)); sh = Image.new("RGBA", out.size, (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: int(v * 0.5)))
    res = Image.new("RGBA", out.size, (0, 0, 0, 0)); res.alpha_composite(sh, (8, 16)); res.alpha_composite(out); return res

def pecera():
    im, d = _new()
    E(d, 320, 350, 250, 240, fill=(170, 220, 255, 90), outline=(220, 240, 255), width=10 * S)
    d.chord(((320 - 244) * S, (350 - 234) * S, (320 + 244) * S, (350 + 234) * S), -12, 192, fill=(60, 150, 230, 200))
    R(d, 170, 95, 470, 125, 15, fill=(220, 240, 255))
    E(d, 320, 545, 170, 30, fill=(240, 210, 140))
    # pez
    PO(d, [(400, 360), (480, 300), (470, 360), (480, 420)], fill=(255, 120, 30))
    E(d, 320, 360, 105, 70, fill=(255, 150, 40)); E(d, 300, 380, 60, 30, fill=(255, 190, 90))
    PO(d, [(300, 300), (350, 255), (370, 300)], fill=(255, 120, 30))
    E(d, 260, 345, 20, 22, fill=WHITE); E(d, 255, 348, 11, 12, fill=INK); E(d, 252, 343, 4, 4, fill=WHITE)
    L(d, [(225, 385), (240, 392)], 6, fill=INK)
    for (x, y, r) in [(200, 250, 14), (180, 200, 10), (205, 160, 7)]: E(d, x, y, r, r, outline=WHITE, width=4 * S)
    return _fin(im)

def tarta(num="10"):
    im, d = _new()
    E(d, 320, 560, 260, 40, fill=(230, 230, 240))
    R(d, 110, 380, 530, 550, 30, fill=(250, 150, 190)); R(d, 110, 380, 530, 420, 20, fill=(255, 245, 250))
    for x in range(140, 520, 60): E(d, x, 420, 26, 30, fill=(255, 245, 250))
    R(d, 170, 260, 470, 390, 26, fill=(255, 190, 215)); R(d, 170, 260, 470, 290, 18, fill=(255, 245, 250))
    for x in range(195, 460, 55): E(d, x, 292, 22, 24, fill=(255, 245, 250))
    for x, y in [(160, 480), (250, 500), (350, 480), (450, 500), (220, 340), (400, 345)]: E(d, x, y, 9, 9, fill=(200, 60, 120))
    T(d, 320, 190, num, 150, fill=YEL, stroke=8)
    for x in (270, 375):
        E(d, x, 95, 16, 28, fill=(255, 170, 40)); E(d, x, 102, 8, 15, fill=(255, 240, 150))
    return _fin(im)

def tele(txt="EP 1.100", sub="SIN PARAR"):
    im, d = _new()
    L(d, [(320, 160), (230, 60)], 8, fill=(180, 180, 200)); L(d, [(320, 160), (420, 70)], 8, fill=(180, 180, 200))
    E(d, 230, 60, 14, 14, fill=RED); E(d, 420, 70, 14, 14, fill=RED)
    R(d, 60, 150, 580, 520, 50, fill=(60, 50, 90)); R(d, 95, 185, 545, 470, 30, fill=(30, 40, 90))
    d.rectangle((95 * S, 185 * S, 545 * S, 470 * S), fill=None)
    for k in range(9): L(d, [(110, 200 + k * 32), (530, 200 + k * 32)], 3, fill=(50, 70, 140))
    T(d, 320, 300, txt, 92, fill=YEL, stroke=6)
    if sub: T(d, 320, 405, sub, 52, fill=WHITE, path=MB)
    R(d, 150, 520, 220, 570, 10, fill=(60, 50, 90)); R(d, 420, 520, 490, 570, 10, fill=(60, 50, 90))
    return _fin(im)

def estudio():
    im, d = _new()
    R(d, 110, 80, 530, 590, 30, fill=(150, 100, 60)); R(d, 140, 120, 500, 570, 14, fill=(250, 250, 245))
    R(d, 240, 60, 400, 130, 20, fill=(120, 120, 140))
    T(d, 320, 175, "ESTUDIO", 64, fill=INK)
    for i, h in enumerate([90, 150, 230, 320]):
        x = 180 + i * 75; R(d, x, 520 - h, x + 55, 520, 8, fill=[(90, 160, 255), (60, 200, 150), (255, 190, 60), (230, 70, 90)][i])
    L(d, [(180, 470), (260, 420), (340, 340), (440, 230)], 10, fill=INK)
    PO(d, [(450, 210), (455, 262), (412, 240)], fill=INK)
    return _fin(im)

def curva():
    im, d = _new()
    R(d, 60, 70, 580, 570, 40, fill=(250, 250, 245))
    L(d, [(130, 120), (130, 500), (540, 500)], 10, fill=INK)
    pts = [(130 + x, 140 + 330 * (1 - math.exp(-x / 70)) * 0.95) for x in range(0, 401, 10)]
    L(d, pts, 14, fill=RED)
    T(d, 330, 545, "TIEMPO", 40, fill=INK, path=MB); T(d, 330, 105, "MEMORIA", 40, fill=INK, path=MB)
    E(d, 200, 375, 34, 34, fill=YEL, outline=INK, width=5 * S); T(d, 200, 378, "1h", 34, fill=INK, path=MB)
    return _fin(im)

def calendario(txt="1969", head="DESDE"):
    im, d = _new()
    R(d, 80, 90, 560, 570, 40, fill=(250, 250, 245)); R(d, 80, 90, 560, 220, 40, fill=RED); d.rectangle((80 * S, 180 * S, 560 * S, 220 * S), fill=RED)
    for x in (190, 450): R(d, x - 18, 50, x + 18, 140, 14, fill=(80, 80, 100))
    T(d, 320, 160, head, 70, fill=WHITE)
    T(d, 320, 400, txt, 190 if len(txt) <= 4 else 120, fill=INK)
    return _fin(im)

def pulpo():
    im, d = _new()
    col = (190, 90, 230); dk = (150, 60, 190)
    for k in range(8):
        a = math.pi * (0.1 + 0.8 * k / 7); pts = []
        for t in range(14):
            r = 60 + t * 17; ang = a + 0.35 * math.sin(t * 0.6 + k)
            pts.append((320 + r * math.cos(ang) * 1.35, 380 + r * math.sin(ang) * 0.75 + t * 6))
        L(d, pts, 46 - 2.4 * len(pts) * 0.5, fill=dk if k % 2 else col)
    E(d, 320, 300, 170, 170, fill=col); E(d, 260, 240, 40, 30, fill=(215, 140, 245))
    for x in (260, 380): E(d, x, 320, 30, 34, fill=WHITE); E(d, x + 4, 326, 15, 17, fill=INK)
    L(d, [(290, 385), (320, 400), (350, 385)], 8, fill=INK)
    for i, x in enumerate((170, 320, 470)): heart(d, x, 85 + (20 if i != 1 else 0), 48)
    return _fin(im)

def estaciones():
    im, d = _new()
    cols = [(120, 190, 255), (255, 150, 200), (255, 200, 60), (240, 120, 50)]
    for i in range(4):
        r, c = divmod(i, 2); x0 = 70 + c * 260; y0 = 70 + r * 260
        R(d, x0, y0, x0 + 240, y0 + 240, 40, fill=cols[i]); cx, cy = x0 + 120, y0 + 120
        if i == 0:
            for k in range(3):
                a = k * math.pi / 3; L(d, [(cx - 70 * math.cos(a), cy - 70 * math.sin(a)), (cx + 70 * math.cos(a), cy + 70 * math.sin(a))], 12, fill=WHITE)
        elif i == 1:
            for k in range(5): a = k * 2 * math.pi / 5; E(d, cx + 42 * math.cos(a), cy + 42 * math.sin(a), 32, 32, fill=WHITE)
            E(d, cx, cy, 26, 26, fill=YEL)
        elif i == 2:
            for k in range(8): a = k * math.pi / 4; L(d, [(cx + 55 * math.cos(a), cy + 55 * math.sin(a)), (cx + 85 * math.cos(a), cy + 85 * math.sin(a))], 12, fill=WHITE)
            E(d, cx, cy, 45, 45, fill=WHITE)
        else:
            PO(d, [(cx, cy - 80), (cx + 60, cy), (cx, cy + 70), (cx - 60, cy)], fill=(160, 60, 20)); L(d, [(cx, cy - 70), (cx, cy + 90)], 8, fill=(120, 40, 10))
    return _fin(im)

def ojo():
    im, d = _new()
    PO(d, [(40, 320)] + [(40 + 560 * t / 20, 320 - 200 * math.sin(math.pi * t / 20)) for t in range(21)] + [(600, 320)], fill=(80, 40, 60))
    pts_top = [(60 + 520 * t / 20, 320 - 170 * math.sin(math.pi * t / 20)) for t in range(21)]
    pts_bot = [(60 + 520 * t / 20, 320 + 170 * math.sin(math.pi * t / 20)) for t in range(21)][::-1]
    PO(d, pts_top + pts_bot, fill=(255, 240, 240))
    for (a, b) in [((90, 310), (190, 280)), ((100, 350), (200, 360)), ((550, 300), (450, 270)), ((540, 350), (440, 370)), ((150, 250), (220, 270))]:
        L(d, [a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 12), b], 5, fill=(230, 60, 70))
    E(d, 320, 320, 120, 120, fill=(110, 70, 200)); E(d, 320, 320, 60, 60, fill=INK); E(d, 290, 285, 22, 22, fill=WHITE)
    L(d, pts_top, 14, fill=INK)
    return _fin(im)

def vacas():
    im, d = _new()
    def cara(cx, cy, flip):
        for sx in (-1, 1): PO(d, [(cx + sx * 80, cy - 90), (cx + sx * 110, cy - 160), (cx + sx * 120, cy - 80)], fill=(240, 220, 180))
        for sx in (-1, 1): E(d, cx + sx * 140, cy - 50, 55, 25, fill=(250, 250, 250), outline=INK, width=4 * S)
        E(d, cx, cy, 120, 135, fill=(250, 250, 250), outline=INK, width=5 * S)
        E(d, cx + flip * 50, cy - 70, 45, 35, fill=INK); E(d, cx - flip * 70, cy + 10, 25, 30, fill=INK)
        E(d, cx, cy + 85, 95, 60, fill=(255, 175, 185), outline=INK, width=4 * S)
        E(d, cx - 35, cy + 85, 12, 16, fill=(200, 90, 110)); E(d, cx + 35, cy + 85, 12, 16, fill=(200, 90, 110))
        for x in (cx - 45, cx + 45): E(d, x, cy - 20, 17, 20, fill=INK); E(d, x + 5, cy - 26, 6, 6, fill=WHITE)
    cara(175, 370, 1); cara(465, 370, -1)
    heart(d, 320, 130, 70)
    return _fin(im)

def reloj(hora="4:00"):
    im, d = _new()
    for x in (180, 460): E(d, x, 130, 70, 55, fill=(240, 60, 80)); L(d, [(x, 175), (x + (40 if x < 320 else -40), 220)], 14, fill=INK)
    E(d, 320, 360, 230, 230, fill=(240, 60, 80)); E(d, 320, 360, 190, 190, fill=(255, 250, 240))
    for k in range(12):
        a = k * math.pi / 6; L(d, [(320 + 160 * math.cos(a), 360 + 160 * math.sin(a)), (320 + 180 * math.cos(a), 360 + 180 * math.sin(a))], 8, fill=INK)
    L(d, [(320, 360), (320, 210)], 12, fill=INK); L(d, [(320, 360), (320 + 105 * 0.866, 360 + 105 * 0.5)], 16, fill=INK)  # 4:00
    T(d, 320, 470, hora, 60, fill=RED, path=MB)
    E(d, 320, 360, 16, 16, fill=INK)
    for x in (200, 440): L(d, [(x, 580), (x - (30 if x < 320 else -30), 620)], 16, fill=INK)
    return _fin(im)

def reloj_arena():
    im, d = _new()
    R(d, 140, 50, 500, 100, 20, fill=(150, 100, 60)); R(d, 140, 560, 500, 610, 20, fill=(150, 100, 60))
    PO(d, [(180, 100), (460, 100), (340, 330), (300, 330)], fill=(210, 235, 255)); PO(d, [(180, 560), (460, 560), (340, 330), (300, 330)], fill=(210, 235, 255))
    PO(d, [(250, 200), (390, 200), (330, 320), (310, 320)], fill=(255, 200, 80)); PO(d, [(200, 560), (440, 560), (320, 440)], fill=(255, 200, 80))
    L(d, [(320, 330), (320, 470)], 6, fill=(255, 200, 80))
    for x in (160, 480): L(d, [(x, 100), (x, 560)], 14, fill=(150, 100, 60))
    return _fin(im)

def pergamino():
    im, d = _new()
    R(d, 160, 30, 480, 610, 20, fill=(250, 240, 210))
    for y in range(90, 590, 42):
        L(d, [(200, y), (200 + 16, y)], 10, fill=(60, 200, 130)); L(d, [(235, y), (430 - (y * 37) % 90, y)], 10, fill=(150, 140, 120))
    R(d, 140, 10, 500, 60, 25, fill=(200, 160, 100)); R(d, 140, 590, 500, 640, 25, fill=(200, 160, 100))
    return _fin(im)

def ambulancia():
    im, d = _new()
    R(d, 40, 200, 470, 500, 40, fill=(250, 250, 250)); R(d, 440, 280, 610, 500, 40, fill=(250, 250, 250))
    R(d, 470, 300, 590, 390, 20, fill=(120, 190, 240))
    d.rectangle((40 * S, 400 * S, 610 * S, 430 * S), fill=RED)
    R(d, 190, 250, 330, 390, 10, fill=WHITE); d.rectangle((235 * S, 265 * S, 285 * S, 375 * S), fill=RED); d.rectangle((205 * S, 295 * S, 315 * S, 345 * S), fill=RED)
    R(d, 200, 160, 300, 205, 14, fill=(80, 140, 255)); R(d, 300, 160, 380, 205, 14, fill=RED)
    for x in (150, 500): E(d, x, 510, 62, 62, fill=INK); E(d, x, 510, 28, 28, fill=(180, 180, 190))
    return _fin(im)

def web_caida():
    im, d = _new()
    R(d, 40, 90, 600, 540, 36, fill=(245, 245, 250)); R(d, 40, 90, 600, 170, 36, fill=(60, 60, 80)); d.rectangle((40 * S, 140 * S, 600 * S, 170 * S), fill=(60, 60, 80))
    for i, c in enumerate([(240, 80, 80), (250, 190, 60), (80, 200, 120)]): E(d, 90 + i * 45, 130, 14, 14, fill=c)
    # calavera pirata
    E(d, 320, 320, 105, 95, fill=INK); R(d, 260, 360, 380, 440, 20, fill=INK)
    E(d, 280, 315, 28, 30, fill=WHITE); E(d, 360, 315, 28, 30, fill=WHITE); PO(d, [(320, 345), (305, 375), (335, 375)], fill=WHITE)
    for x in (285, 310, 335, 360): L(d, [(x, 405), (x, 440)], 6, fill=WHITE)
    L(d, [(180, 470), (460, 200)], 18, fill=INK); L(d, [(180, 200), (460, 470)], 18, fill=INK)
    T(d, 320, 500, "ERROR 404", 44, fill=RED, path=MB)
    return _fin(im)

def ticket():
    im, d = _new()
    pts = [(150, 60), (490, 60), (490, 560)] + [(490 - k * 34, 560 + (18 if k % 2 else 0)) for k in range(11)] + [(150, 560)]
    PO(d, pts, fill=(255, 252, 240))
    T(d, 320, 120, "PEDIDO", 60, fill=INK)
    for k, (a, b) in enumerate([("2 CAFÉS", "3,00"), ("1 TOSTADA", "2,50"), ("1 ZUMO", "2,20"), ("1 TARTA", "3,80")]):
        y = 210 + k * 60; T(d, 260, y, a, 29, fill=INK, path=MB); T(d, 435, y, b, 29, fill=INK, path=MB)
    L(d, [(180, 455), (460, 455)], 4, fill=INK); T(d, 255, 500, "TOTAL", 40, fill=INK, path=MB); T(d, 430, 500, "11,50", 40, fill=INK, path=MB)
    return _fin(im)

def saco_yen():
    im, d = _new()
    E(d, 320, 400, 210, 190, fill=(200, 150, 70)); PO(d, [(250, 230), (390, 230), (430, 170), (210, 170)], fill=(200, 150, 70))
    R(d, 230, 205, 410, 245, 18, fill=(150, 100, 40)); E(d, 260, 330, 50, 70, fill=(225, 180, 100))
    T(d, 320, 420, "¥", 220, fill=YEL, stroke=8, sfill=(120, 70, 20))
    for (x, y) in [(120, 560), (190, 590), (470, 575), (540, 550)]: E(d, x, y, 48, 20, fill=(255, 210, 70), outline=(180, 130, 30), width=4 * S)
    return _fin(im)

def quesito(pct=0.52, txt="1 DE CADA 2"):
    im, d = _new()
    E(d, 320, 310, 250, 250, fill=(70, 70, 100))
    d.pieslice(((320 - 250) * S, (310 - 250) * S, (320 + 250) * S, (310 + 250) * S), -90, -90 + 360 * pct, fill=(230, 50, 80))
    E(d, 320, 310, 110, 110, fill=(30, 22, 54)); T(d, 320, 312, "+50%", 64, fill=WHITE)
    return _fin(im)

def trofeo(txt="TOP 20"):
    im, d = _new()
    PO(d, [(170, 90), (470, 90), (430, 330), (210, 330)], fill=(255, 200, 60)); E(d, 320, 330, 110, 60, fill=(255, 200, 60))
    for sx in (-1, 1): d.arc(((320 + sx * 160 - 70) * S, 120 * S, (320 + sx * 160 + 70) * S, 280 * S), 90 if sx > 0 else -90, 270 if sx > 0 else 90, fill=(255, 200, 60), width=22 * S)
    R(d, 290, 380, 350, 470, 10, fill=(230, 170, 40)); R(d, 200, 470, 440, 560, 20, fill=(120, 80, 50)); R(d, 230, 490, 410, 540, 12, fill=(255, 220, 120))
    T(d, 320, 515, txt, 40, fill=INK, path=MB)
    PO(d, [(320, 140), (338, 190), (390, 190), (348, 222), (364, 272), (320, 242), (276, 272), (292, 222), (250, 190), (302, 190)], fill=WHITE)
    return _fin(im)

def lapiz_moneda():
    im, d = _new()
    PO(d, [(110, 470), (420, 160), (500, 240), (190, 550)], fill=(255, 200, 60)); PO(d, [(110, 470), (190, 550), (80, 580)], fill=(240, 210, 170))
    PO(d, [(80, 580), (95, 535), (125, 565)], fill=INK); PO(d, [(420, 160), (460, 120), (540, 200), (500, 240)], fill=(240, 120, 140))
    L(d, [(150, 510), (460, 200)], 6, fill=(220, 160, 40))
    E(d, 470, 470, 110, 110, fill=(255, 210, 70), outline=(180, 130, 30), width=8 * S); T(d, 470, 474, "¥", 120, fill=(180, 130, 30))
    return _fin(im)

def globo():
    im, d = _new()
    E(d, 300, 330, 230, 230, fill=(70, 150, 240))
    for blob in [[(200, 200), (290, 160), (330, 230), (270, 300), (190, 280)], [(330, 330), (420, 300), (460, 380), (400, 470), (340, 430)], [(150, 360), (220, 380), (230, 460), (170, 470)]]:
        PO(d, blob, fill=(80, 200, 120))
    L(d, [(380, 560), (480, 440), (540, 470), (620, 330)], 22, fill=YEL); PO(d, [(625, 290), (635, 365), (580, 340)], fill=YEL)
    return _fin(im)

ICONS = {"pecera": pecera, "tarta": tarta, "tele": tele, "estudio": estudio, "curva": curva, "calendario": calendario, "pulpo": pulpo,
         "estaciones": estaciones, "ojo": ojo, "vacas": vacas, "reloj": reloj, "reloj_arena": reloj_arena, "pergamino": pergamino, "ambulancia": ambulancia, "web_caida": web_caida, "ticket": ticket, "saco_yen": saco_yen,
         "quesito": quesito, "trofeo": trofeo, "lapiz_moneda": lapiz_moneda, "globo": globo}
if __name__ == "__main__":
    ks = list(ICONS)[-8:]; sheet = Image.new("RGBA", (N * 5, N * 3), (40, 30, 60, 255))
    for i, k in enumerate(ks): sheet.alpha_composite(ICONS[k](), ((i % 5) * N, (i // 5) * N))
    sheet.convert("RGB").resize((N * 5 // 2, N * 3 // 2)).save(sys.argv[1])
