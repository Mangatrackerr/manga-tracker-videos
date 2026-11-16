# Muñeco v2 (13/11/2026): más simple y sin fallos. Cabeza dibujada aquí (sin cascos ni cuello recortado)
# y brazos/piernas "de goma" (curvas suaves): cada pose solo dice DÓNDE están manos y pies, y la curva se calcula sola.
# Coordenadas de la pose relativas: manos respecto al hombro, pies respecto a la cadera (px a escala 1, y hacia abajo).
import math
from PIL import Image, ImageDraw

SK = (240, 196, 160); SK_D = (214, 160, 125); HAIR = (34, 28, 44); HAIR_L = (70, 60, 92); INK = (22, 16, 30); WHITE = (255, 255, 255)
HOOD = (112, 66, 210); HOOD_D = (84, 46, 165); HOOD_L = (140, 98, 232); JEANS = (52, 78, 140); SHOE = (248, 248, 252); SOLE = (70, 70, 90)
CW, CH = 820, 1180; HX, HY = 410, 760          # lienzo y cadera
FOOT_Y = HY + 300                                # los pies quedan aquí (para colocar el muñeco)
S = 2
# ---- aspecto configurable (16/11/2026): set_look(...) cambia pelo, ropa, piel y accesorios. Por defecto = el chico de siempre ----
DEFAULT_LOOK = dict(skin=SK, skin_d=SK_D, hair=HAIR, hair_l=HAIR_L, hair_style="short", top="hoodie", top_c=HOOD, top_d=HOOD_D, top_l=HOOD_L,
                    inner=(235, 235, 245), bottom="jeans", bottom_c=JEANS, socks=(250, 250, 250), shoe=SHOE, sole=SOLE, iris=INK,
                    lashes=False, glasses=None, hat=None, hat_c=(220, 60, 60), apron=None, blush=(248, 160, 150), stripe=None)
LOOK = dict(DEFAULT_LOOK)
def set_look(**kw):
    LOOK.clear(); LOOK.update(DEFAULT_LOOK); LOOK.update(kw)
BASE = dict(x=0, y=0, lean=0, head=0, lhx=-28, lhy=205, rhx=28, rhy=205, lfx=-14, lfy=280, rfx=14, rfy=280, sit=0.0, bend=1.0, squash=0.0)
NUM = list(BASE)

def _bez(p0, c, p1, n=18):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1]) for t in [i / n for i in range(n + 1)]]

def _hose(d, p0, p1, w, col, bend, out_sgn, length):
    """miembro de goma: si la distancia es menor que su longitud se curva hacia fuera"""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; dist = math.hypot(dx, dy) or 1
    slack = max(0.0, length - dist); k = min(1.0, slack / length) * 0.9 * bend
    nx, ny = -dy / dist, dx / dist                       # normal
    if nx * out_sgn < 0: nx, ny = -nx, -ny               # que el codo/rodilla salga hacia fuera
    c = ((p0[0] + p1[0]) / 2 + nx * length * 0.5 * k, (p0[1] + p1[1]) / 2 + ny * length * 0.5 * k)
    pts = _bez(p0, c, p1, 24)
    # una sola forma rellena (sin costuras): bordes desplazados a ambos lados de la curva
    L, Rr = [], []
    for i, (x, y) in enumerate(pts):
        a = pts[max(0, i - 1)]; b = pts[min(len(pts) - 1, i + 1)]; tx, ty = b[0] - a[0], b[1] - a[1]; n = math.hypot(tx, ty) or 1
        ox, oy = -ty / n * w / 2, tx / n * w / 2; L.append(((x + ox) * S, (y + oy) * S)); Rr.append(((x - ox) * S, (y - oy) * S))
    d.polygon(L + Rr[::-1], fill=col)
    for x, y in (pts[0], pts[-1]): d.ellipse(((x - w / 2) * S, (y - w / 2) * S, (x + w / 2) * S, (y + w / 2) * S), fill=col)
    return pts

def _E(d, cx, cy, rx, ry, **kw): d.ellipse(((cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S), **kw)
def _L(d, pts, w, col): d.line([(x * S, y * S) for x, y in pts], fill=col, width=int(w * S), joint="curve")
def _arc(cx, cy, rx, ry, a0, a1, n=14): return [(cx + rx * math.cos(a0 + (a1 - a0) * i / n), cy + ry * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]

def _hair_front(d, cx, cy, R, st, HC, HL):
    """pelo delante de la cara (cúpula + flequillo) según el estilo"""
    dome = [(cx + (R + 12) * math.cos(a), cy - 14 + (R + 6) * math.sin(a)) for a in [math.pi * (1.0 + i / 40) for i in range(41)]]
    P_ = lambda pts: d.polygon([(x * S, y * S) for x, y in pts], fill=HC)
    if st in ("short", "spiky", "curly"):
        fr = []
        for i in range(41):
            u = i / 40; x = cx + R + 12 - u * (2 * R + 24); edge = abs(u - 0.5) * 2
            y = cy - 50 + 20 * (0.5 - 0.5 * math.cos(2 * math.pi * u * 4)) + 52 * edge ** 3
            fr.append((x, y))
        P_(dome + fr)
        if st == "short":
            P_(_bez((cx - 22, cy - R - 2), (cx - 4, cy - R - 70), (cx + 46, cy - R - 54), 14) + _bez((cx + 46, cy - R - 54), (cx + 14, cy - R - 30), (cx + 26, cy - R + 8), 14))
        elif st == "spiky":
            for k in range(7):
                a = math.pi * (1.08 + k * 0.84 / 6); ln = 95 if k in (2, 3, 4) else 70
                b0 = (cx + (R + 6) * math.cos(a - 0.16), cy - 14 + (R + 2) * math.sin(a - 0.16)); b1 = (cx + (R + 6) * math.cos(a + 0.16), cy - 14 + (R + 2) * math.sin(a + 0.16))
                tip = (cx + (R + ln) * math.cos(a + 0.05), cy - 14 + (R + ln) * math.sin(a + 0.05)); P_([b0, tip, b1])
        else:
            for k in range(13):
                a = math.pi * (0.96 + k * 1.08 / 12); _E(d, cx + (R + 6) * math.cos(a), cy - 20 + (R + 2) * math.sin(a), 42, 42, fill=HC)
        _L(d, _arc(cx - 20, cy - 60, R - 40, R - 60, math.pi * 1.18, math.pi * 1.42), 10, HL)
        return
    # estilos con flequillo recto / de lado (chicas, pelo largo)
    if st == "ponytail":   # flequillo de lado
        fr = [(cx + R + 12, cy - 30), (cx + R - 10, cy + 10)] + _bez((cx + R - 10, cy + 10), (cx + 20, cy - 10), (cx - R + 10, cy - 70), 16) + [(cx - R - 12, cy - 14)]
        P_(dome + fr)
    else:                  # flequillo recto con mechones
        fr = []
        for i in range(41):
            u = i / 40; x = cx + R + 12 - u * (2 * R + 24); edge = abs(u - 0.5) * 2
            y = cy - 36 + 12 * abs(math.sin(math.pi * u * 5)) + 40 * edge ** 4
            fr.append((x, y))
        P_(dome + fr)
    # mechones laterales hasta la mandíbula (tapan las orejas)
    if st in ("long", "bob", "buns"):
        for sg in (-1, 1):
            x0 = cx + sg * (R - 6); ln = 150 if st == "bob" else 175
            P_([(x0 - sg * 30, cy - 40), (x0 + sg * 26, cy - 40), (x0 + sg * 30, cy + ln), (x0 - sg * 12, cy + ln - 30)])
    if st == "buns":
        for sg in (-1, 1): _E(d, cx + sg * 105, cy - R + 5, 58, 58, fill=HC); _L(d, _arc(cx + sg * 105, cy - R + 5, 40, 40, math.pi * 1.1, math.pi * 1.5), 8, HL)
    _L(d, _arc(cx - 20, cy - 70, R - 40, R - 70, math.pi * 1.18, math.pi * 1.42), 10, HL)

def _hair_back(d, cx, cy, R, st, HC):
    """pelo por detrás de la cabeza/hombros (se pinta antes que el cuerpo)"""
    if st == "long":
        d.rounded_rectangle(((cx - R - 22) * S, (cy - 40) * S, (cx + R + 22) * S, (cy + 330) * S), radius=int(60 * S), fill=HC)
    elif st == "bob":
        d.rounded_rectangle(((cx - R - 20) * S, (cy - 40) * S, (cx + R + 20) * S, (cy + 160) * S), radius=int(50 * S), fill=HC)
    elif st == "ponytail":
        pts = _bez((cx + R - 30, cy - R + 30), (cx + R + 110, cy - 80), (cx + R + 50, cy + 130), 16)
        for i, (x, y) in enumerate(pts):
            w = 52 - i * 1.6; _E(d, x, y, w, w, fill=HC)

def _hat(d, cx, cy, R, hat, col):
    if hat == "cap":   # gorra hacia atrás
        d.chord(((cx - R - 8) * S, (cy - R - 30) * S, (cx + R + 8) * S, (cy + 40) * S), 180, 360, fill=col)
        d.rounded_rectangle(((cx - R - 10) * S, (cy - 26) * S, (cx + R + 10) * S, (cy - 4) * S), radius=int(10 * S), fill=tuple(max(0, c - 40) for c in col))
        d.rounded_rectangle(((cx + R - 40) * S, (cy - 40) * S, (cx + R + 60) * S, (cy - 10) * S), radius=int(14 * S), fill=tuple(max(0, c - 40) for c in col))
        _E(d, cx, cy - R - 26, 12, 9, fill=tuple(max(0, c - 40) for c in col))
    elif hat in ("bandana", "headband"):
        h = 40 if hat == "bandana" else 26
        d.rounded_rectangle(((cx - R - 6) * S, (cy - 78) * S, (cx + R + 6) * S, (cy - 78 + h) * S), radius=int(12 * S), fill=col)
        if hat == "bandana":
            d.polygon([(a * S, b * S) for a, b in [(cx + R, cy - 64), (cx + R + 70, cy - 100), (cx + R + 60, cy - 50)]], fill=col)
            d.polygon([(a * S, b * S) for a, b in [(cx + R, cy - 56), (cx + R + 64, cy - 20), (cx + R + 30, cy - 4)]], fill=col)
    elif hat == "chef":
        d.rounded_rectangle(((cx - R + 10) * S, (cy - R - 20) * S, (cx + R - 10) * S, (cy - 60) * S), radius=int(10 * S), fill=(250, 250, 250), outline=(210, 210, 220), width=int(4 * S))
        for k in (-70, 0, 70): _E(d, cx + k, cy - R - 60, 70, 60, fill=(250, 250, 250))

def _head(d, cx, cy, expr, blink, look, sweat):
    R = 150; L_ = LOOK; SKc = L_["skin"]; HC = L_["hair"]; HL = L_["hair_l"]; st = L_["hair_style"]
    _E(d, cx - R + 4, cy + 20, 26, 34, fill=SKc); _E(d, cx + R - 4, cy + 20, 26, 34, fill=SKc)          # orejas
    _E(d, cx, cy, R, R * 1.02, fill=SKc)
    _hair_front(d, cx, cy, R, st, HC, HL)
    if L_["hat"]: _hat(d, cx, cy, R, L_["hat"], L_["hat_c"])
    ey = cy + 18; ex = (cx - 56, cx + 56); lx, ly = look
    for i, x in enumerate(ex):
        if blink or (expr == "wink" and i == 0) or expr == "happy":
            _L(d, _arc(x, ey + 6, 26, 16, math.pi * 1.05, math.pi * 1.95), 9, INK); continue
        if expr == "cry":
            _L(d, _arc(x, ey - 4, 26, 12, math.pi * 0.05, math.pi * 0.95), 9, INK)
            d.polygon([(a * S, b * S) for a, b in [(x - 12, ey + 10), (x + 12, ey + 10), (x + 16, ey + 120), (x - 16, ey + 120)]], fill=(120, 190, 255)); continue
        rx, ry = (34, 40) if expr == "shock" else (27, 33)
        _E(d, x, ey, rx, ry, fill=WHITE, outline=INK, width=int(5 * S))
        if L_["lashes"]:
            sg = -1 if i == 0 else 1
            for k in range(2): _L(d, [(x + sg * (rx - 4), ey - ry + 10 + k * 12), (x + sg * (rx + 14), ey - ry + 2 + k * 14)], 6, INK)
        if expr == "dizzy":
            sg = 1 if i else -1
            _L(d, [(x + (2 + 2.2 * a) * math.cos(sg * a), ey + (2 + 2.2 * a) * math.sin(sg * a)) for a in [k * 0.32 for k in range(40)]], 5, INK); continue
        pr = 9 if expr == "shock" else 15
        px = x + lx * 9; py = ey + 4 + ly * 9
        if L_["iris"] != INK and expr != "shock": _E(d, px, py, pr + 5, pr + 7, fill=L_["iris"])
        _E(d, px, py, pr if L_["iris"] == INK else pr - 5, (pr + 2) if L_["iris"] == INK else pr - 3, fill=INK); _E(d, px + 5, py - 6, 4.5, 4.5, fill=WHITE)
        if expr in ("smug", "tired"):  # párpado
            d.chord(((x - rx - 3) * S, (ey - ry - 3) * S, (x + rx + 3) * S, (ey + ry + 3) * S), 180, 360, fill=SKc); _L(d, [(x - rx, ey), (x + rx, ey)], 6, INK)
    if L_["glasses"]:
        for x in ex: _E(d, x, ey + 2, 44, 40, outline=L_["glasses"], width=int(8 * S))
        _L(d, [(cx - 14, ey - 2), (cx + 14, ey - 2)], 7, L_["glasses"])
    br = {"shock": (-62, -62), "confused": (-58, -44), "smug": (-46, -60), "cry": (-44, -44), "dizzy": (-50, -50)}.get(expr, (-52, -52))
    tilt = {"cry": 10, "confused": -8, "smug": 0}.get(expr, 0)
    bw = 8 if L_["lashes"] else 11
    if st not in ("long", "bob", "buns", "ponytail") or True:
        _L(d, [(cx - 84, ey + br[0] + tilt), (cx - 30, ey + br[0] - tilt)], bw, HC); _L(d, [(cx + 30, ey + br[1] - tilt), (cx + 84, ey + br[1] + tilt)], bw, HC)
    for x in (cx - 92, cx + 92): _E(d, x, ey + 52, 22, 12, fill=L_["blush"])
    my = cy + 92
    if expr in ("shock",): _E(d, cx, my + 4, 24, 30, fill=INK); _E(d, cx, my + 20, 15, 9, fill=(225, 95, 105))
    elif expr in ("proud", "wink", "happy"):
        d.chord(((cx - 42) * S, (my - 26) * S, (cx + 42) * S, (my + 28) * S), 0, 180, fill=INK); d.chord(((cx - 32) * S, (my - 18) * S, (cx + 32) * S, (my + 2) * S), 0, 180, fill=WHITE)
    elif expr in ("confused", "dizzy"): _L(d, [(cx - 36 + i * 6, my + 6 * math.sin(i * 1.1)) for i in range(13)], 7, INK)
    elif expr == "smug": _L(d, [(cx - 36, my + 6), (cx, my + 10), (cx + 34, my - 6)], 8, INK)
    elif expr == "tired": _L(d, [(cx - 26, my + 6), (cx + 26, my + 6)], 8, INK); _E(d, cx - 56, cy + 60, 22, 7, fill=(190, 150, 170)); _E(d, cx + 56, cy + 60, 22, 7, fill=(190, 150, 170))
    elif expr == "cry": d.chord(((cx - 36) * S, (my - 4) * S, (cx + 36) * S, (my + 40) * S), 180, 360, fill=INK)
    else: _L(d, _arc(cx, my - 12, 32, 18, 0.3, math.pi - 0.3), 8, INK)
    if sweat > 0: _E(d, cx + R - 20, cy - 50, 14, 20, fill=(140, 200, 255))

def _sub(pts, f):
    n = max(2, int(len(pts) * f)); return pts[:n]

def draw(pose, expr="neutral", hands=("fist", "fist"), blink=False, look=(0, 0), sweat=0.0, phone=None):
    p = dict(BASE); p.update(pose); L_ = LOOK; SKc = L_["skin"]
    TOP, TOP_D, TOP_L = L_["top_c"], L_["top_d"], L_["top_l"]
    im = Image.new("RGBA", (CW * S, CH * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    hx, hy = HX, HY
    sq = p["squash"]; torso_h = 230 * (1 - 0.12 * sq); tw = (112 if L_["top"] not in ("tank", "tee") else 104) * (1 + 0.08 * sq)
    neck = (hx, hy - torso_h); hcx = hx; hcy = neck[1] - 118
    _hair_back(d, hcx, hcy, 150, L_["hair_style"], L_["hair"])
    sit = p["sit"]; bt = L_["bottom"]
    legL = 290 * (1 - 0.35 * sit)
    leg_col = SKc if bt in ("skirt", "shorts") else L_["bottom_c"]
    for sgn, fx, fy in ((-1, p["lfx"], p["lfy"]), (1, p["rfx"], p["rfy"])):
        h0 = (hx + sgn * 46, hy - 6); f = (h0[0] + fx, h0[1] + fy * (1 - 0.35 * sit))
        pts = _hose(d, h0, f, 56 if bt not in ("skirt", "shorts") else 46, leg_col, p["bend"], sgn, legL)
        if bt in ("skirt", "shorts"): _L(d, pts[-8:], 50, L_["socks"])
        if bt == "shorts": _L(d, _sub(pts, 0.4), 62, L_["bottom_c"])
        if bt == "track" and L_["stripe"]: _L(d, [(x + sgn * 20, y) for x, y in pts[2:-2]], 8, L_["stripe"])
        _E(d, f[0] + sgn * 16, f[1] + 12, 46, 22, fill=L_["shoe"], outline=L_["sole"], width=int(6 * S))
    if bt == "skirt":
        d.polygon([(a * S, b * S) for a, b in [(hx - tw + 6, hy - 10), (hx + tw - 6, hy - 10), (hx + tw + 40, hy + 110 - 40 * sit), (hx - tw - 40, hy + 110 - 40 * sit)]], fill=L_["bottom_c"])
        for k in (-60, -20, 20, 60): _L(d, [(hx + k * 0.8, hy), (hx + k * 1.15, hy + 100 - 40 * sit)], 5, tuple(max(0, c - 35) for c in L_["bottom_c"]))
    # tronco
    tp = L_["top"]
    d.rounded_rectangle(((hx - tw) * S, (neck[1] - 10) * S, (hx + tw) * S, (hy + 30) * S), radius=int((70 if tp != "tank" else 50) * S), fill=TOP)
    if tp == "hoodie":
        d.rounded_rectangle(((hx - tw) * S, (neck[1] - 10) * S, (hx - tw + 46) * S, (hy + 10) * S), radius=int(30 * S), fill=TOP_L)
        d.rounded_rectangle(((hx - 62) * S, (hy - 90) * S, (hx + 62) * S, (hy - 30) * S), radius=int(22 * S), fill=TOP_D)
        d.rounded_rectangle(((hx - tw) * S, (hy + 4) * S, (hx + tw) * S, (hy + 30) * S), radius=int(14 * S), fill=TOP_D)
        for o in (-24, 24): _L(d, [(hx + o, neck[1] + 20), (hx + o * 1.1, neck[1] + 92)], 7, L_["inner"])
    elif tp == "jacket":
        d.polygon([(a * S, b * S) for a, b in [(hx - 40, neck[1] - 6), (hx + 40, neck[1] - 6), (hx + 30, hy + 28), (hx - 30, hy + 28)]], fill=L_["inner"])
        _L(d, [(hx - 40, neck[1]), (hx - 30, hy + 26)], 8, TOP_D); _L(d, [(hx + 40, neck[1]), (hx + 30, hy + 26)], 8, TOP_D)
        d.polygon([(a * S, b * S) for a, b in [(hx - 40, neck[1] - 6), (hx - 80, neck[1] + 4), (hx - 36, neck[1] + 80)]], fill=TOP_L)
        d.polygon([(a * S, b * S) for a, b in [(hx + 40, neck[1] - 6), (hx + 80, neck[1] + 4), (hx + 36, neck[1] + 80)]], fill=TOP_L)
    elif tp == "uniform":
        d.polygon([(a * S, b * S) for a, b in [(hx - 42, neck[1] - 6), (hx + 42, neck[1] - 6), (hx, neck[1] + 110)]], fill=L_["inner"])
        d.polygon([(a * S, b * S) for a, b in [(hx - 26, neck[1] + 22), (hx + 26, neck[1] + 22), (hx + 12, neck[1] + 42), (hx - 12, neck[1] + 42)]], fill=(220, 50, 60))
        d.polygon([(a * S, b * S) for a, b in [(hx - 4, neck[1] + 30), (hx - 36, neck[1] + 90), (hx - 12, neck[1] + 96)]], fill=(220, 50, 60))
        d.polygon([(a * S, b * S) for a, b in [(hx + 4, neck[1] + 30), (hx + 36, neck[1] + 90), (hx + 12, neck[1] + 96)]], fill=(220, 50, 60))
        for k in (0, 1): _E(d, hx + 60, hy - 70 + k * 50, 8, 8, fill=(240, 210, 90))
    elif tp == "chef":
        for k in range(3):
            for sg in (-1, 1): _E(d, hx + sg * 34, neck[1] + 50 + k * 52, 9, 9, fill=(170, 170, 185))
        d.rounded_rectangle(((hx - 46) * S, (neck[1] - 14) * S, (hx + 46) * S, (neck[1] + 14) * S), radius=int(12 * S), fill=L_["inner"])
    elif tp in ("tee", "tank"):
        d.chord(((hx - 44) * S, (neck[1] - 34) * S, (hx + 44) * S, (neck[1] + 22) * S), 0, 180, fill=SKc)
        if L_["stripe"]: d.rectangle(((hx - tw) * S, (hy - 120) * S, (hx + tw) * S, (hy - 96) * S), fill=L_["stripe"])
    elif tp == "sweater":
        d.polygon([(a * S, b * S) for a, b in [(hx - 50, neck[1] - 8), (hx + 50, neck[1] - 8), (hx + 22, neck[1] + 36), (hx - 22, neck[1] + 36)]], fill=L_["inner"])
        d.rounded_rectangle(((hx - tw) * S, (hy + 4) * S, (hx + tw) * S, (hy + 30) * S), radius=int(14 * S), fill=TOP_D)
    if L_["apron"]:
        d.rounded_rectangle(((hx - tw + 18) * S, (neck[1] + 60) * S, (hx + tw - 18) * S, (hy + 150) * S), radius=int(20 * S), fill=L_["apron"])
        _L(d, [(hx - tw + 18, neck[1] + 70), (hx - 40, neck[1] - 4)], 8, L_["apron"]); _L(d, [(hx + tw - 18, neck[1] + 70), (hx + 40, neck[1] - 4)], 8, L_["apron"])
    # brazos
    for sgn, ax, ay, kind in ((-1, p["lhx"], p["lhy"], hands[0]), (1, p["rhx"], p["rhy"], hands[1])):
        sh = (hx + sgn * (tw - 16), neck[1] + 34); hnd = (sh[0] + ax, sh[1] + ay)
        arm_col = SKc if tp in ("tee", "tank") else TOP
        pts = _hose(d, sh, hnd, 44 if tp != "tank" else 38, arm_col, p["bend"], sgn, 225)
        if tp == "tee": _L(d, _sub(pts, 0.36), 52, TOP)
        if tp == "jacket": _L(d, pts[-3:], 50, TOP_D)
        if phone == ("l" if sgn < 0 else "r"):
            d.rounded_rectangle(((hnd[0] - 30) * S, (hnd[1] - 70) * S, (hnd[0] + 30) * S, (hnd[1] + 34) * S), radius=int(12 * S), fill=(25, 22, 40), outline=(150, 110, 255), width=int(4 * S))
            d.rounded_rectangle(((hnd[0] - 22) * S, (hnd[1] - 60) * S, (hnd[0] + 22) * S, (hnd[1] + 22) * S), radius=int(7 * S), fill=(95, 65, 210))
        r = 27
        if kind == "point":
            vx, vy = ax, ay; n = math.hypot(vx, vy) or 1; q = (hnd[0] + vx / n * 44, hnd[1] + vy / n * 44)
            _L(d, [hnd, q], 16, SKc); _E(d, q[0], q[1], 8, 8, fill=SKc)
        if kind == "open":
            for a in (-0.6, 0, 0.6):
                b = math.atan2(ay, ax) + a; q = (hnd[0] + math.cos(b) * 36, hnd[1] + math.sin(b) * 36)
                _L(d, [hnd, q], 13, SKc); _E(d, q[0], q[1], 6.5, 6.5, fill=SKc)
        _E(d, hnd[0], hnd[1], r, r, fill=SKc)
    hd = Image.new("RGBA", (CW * S, CH * S), (0, 0, 0, 0)); _head(ImageDraw.Draw(hd), hcx, hcy, expr, blink, look, sweat)
    if abs(p["head"]) > 0.3: hd = hd.rotate(-p["head"], resample=Image.BICUBIC, center=(hcx * S, (hcy + 120) * S))
    im.alpha_composite(hd)
    out = im.resize((CW, CH), Image.LANCZOS)
    if abs(p["lean"]) > 0.3: out = out.rotate(-p["lean"], resample=Image.BICUBIC, center=(HX, HY))
    if p["x"] or p["y"]:
        o2 = Image.new("RGBA", out.size, (0, 0, 0, 0)); o2.alpha_composite(out, (int(p["x"]), int(p["y"]))); out = o2
    return out

def lerp_pose(a, b, k): return {n: a.get(n, BASE[n]) + (b.get(n, BASE[n]) - a.get(n, BASE[n])) * k for n in NUM}
def ease(k): k = max(0.0, min(1.0, k)); return k * k * (3 - 2 * k)

class Track:
    """keyframes: [(t, pose, expr, hands, extra)] — transición suave de 0.12–0.3 s antes de cada keyframe"""
    def __init__(self, keys): self.keys = keys
    def at(self, T, times):
        ks = [(times(k[0]), *k[1:]) for k in self.keys]
        prev = ks[0]
        for k in ks[1:]:
            if T < k[0]:
                dur = min(0.3, max(0.12, k[0] - prev[0]))
                kk = ease((T - (k[0] - dur)) / dur) if T > k[0] - dur else 0
                return lerp_pose(prev[1], k[1], kk), (prev[2] if kk < 0.5 else k[2]), (prev[3] if kk < 0.5 else k[3]), (prev[4] if len(prev) > 4 else {})
            prev = k
        return lerp_pose(prev[1], prev[1], 0), prev[2], prev[3], (prev[4] if len(prev) > 4 else {})

P = {
 "stand": dict(),
 "shock": dict(lhx=-40, lhy=-150, rhx=40, rhy=-150, squash=0.3),                 # manos a la cabeza
 "arms_up": dict(lhx=-90, lhy=-210, rhx=90, rhy=-210, y=-20),
 "point_r": dict(rhx=225, rhy=-10, lhx=-26, lhy=205, lean=-3),
 "point_l": dict(lhx=-225, lhy=-10, rhx=26, rhy=205, lean=3),
 "point_up_r": dict(rhx=170, rhy=-150, lhx=-26, lhy=205),
 "wave": dict(rhx=95, rhy=-200, lean=-2),
 "scratch": dict(rhx=-10, rhy=-215, head=6),
 "present": dict(rhx=190, rhy=40, lean=-3),
 "shrug": dict(lhx=-120, lhy=-40, rhx=120, rhy=-40, head=8),
 "sit": dict(sit=1, y=60, lfx=-60, lfy=250, rfx=60, rfy=250, lhx=10, lhy=180, rhx=-10, rhy=180),
 "sit_phone": dict(sit=1, y=60, lfx=-60, lfy=250, rfx=60, rfy=250, lhx=60, lhy=150, rhx=-30, rhy=120),
 "sit_happy": dict(sit=1, y=60, lfx=-60, lfy=250, rfx=60, rfy=250, lhx=-100, lhy=-60, rhx=-10, rhy=180),
 "sit_wait": dict(sit=1, y=60, lfx=-60, lfy=250, rfx=60, rfy=250, lhx=10, lhy=180, rhx=-50, rhy=-60),   # mano en la barbilla
 "dizzy": dict(lean=7, head=10, lhx=-80, lhy=180, rhx=80, rhy=190, lfx=-40, rfx=34),
 "sit_dizzy": dict(sit=1, y=60, lfx=-60, lfy=250, rfx=60, rfy=250, lhx=-90, lhy=150, rhx=90, rhy=160, lean=8, head=10),
 "fall": dict(lean=-30, head=-8, lhx=-140, lhy=-150, rhx=140, rhy=-170, lfx=-150, lfy=60, rfx=160, rfy=20, y=50),
 "write": dict(sit=1, y=60, lfx=-60, lfy=250, rfx=60, rfy=250, lhx=40, lhy=95, rhx=-40, rhy=95),
 "phone_stand": dict(rhx=-60, rhy=95, lhx=40, lhy=120),
 "bow": dict(y=30, squash=0.5, head=0, lhx=70, lhy=150, rhx=-70, rhy=150),
 "finger_up": dict(rhx=150, rhy=-150, lhx=-26, lhy=205),
 "clap": dict(lhx=82, lhy=50, rhx=-82, rhy=50),
 "sit_bed": dict(sit=1, y=60, lfx=-60, lfy=250, rfx=60, rfy=250, rhx=-60, rhy=95, lhx=40, lhy=120),
 "run": dict(lhx=-120, lhy=60, rhx=110, rhy=120, lfx=-80, lfy=240, rfx=70, rfy=200, lean=-6),
}

if __name__ == "__main__":
    import sys
    names = ["stand", "shock", "arms_up", "point_r", "wave", "scratch", "present", "sit_phone", "sit_wait", "sit_dizzy", "fall", "run"]
    ex = {"shock": "shock", "arms_up": "shock", "scratch": "confused", "wave": "wink", "present": "proud", "sit_phone": "smug", "sit_wait": "confused", "sit_dizzy": "dizzy", "fall": "shock"}
    hd = {"point_r": ("fist", "point"), "wave": ("fist", "open"), "present": ("fist", "open"), "shock": ("open", "open"), "arms_up": ("open", "open")}
    sheet = Image.new("RGBA", (CW * 6, CH * 2), (40, 30, 60, 255))
    for i, n in enumerate(names):
        sheet.alpha_composite(draw(P[n], ex.get(n, "neutral"), hd.get(n, ("fist", "fist")), phone="r" if n == "sit_phone" else None), ((i % 6) * CW, (i // 6) * CH))
    sheet.convert("RGB").resize((CW * 3, CH)).save(sys.argv[1])
