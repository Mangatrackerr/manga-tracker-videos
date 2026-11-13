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

def _head(d, cx, cy, expr, blink, look, sweat):
    R = 150
    _E(d, cx - R + 4, cy + 20, 26, 34, fill=SK); _E(d, cx + R - 4, cy + 20, 26, 34, fill=SK)          # orejas
    _E(d, cx, cy, R, R * 1.02, fill=SK)
    # pelo: UNA sola forma lisa (cúpula + flequillo ondulado), un mechón arriba y un brillo
    dome = [(cx + (R + 12) * math.cos(a), cy - 14 + (R + 6) * math.sin(a)) for a in [math.pi * (1.0 + i / 40) for i in range(41)]]
    fr = []
    for i in range(41):
        u = i / 40; x = cx + R + 12 - u * (2 * R + 24)
        edge = abs(u - 0.5) * 2
        y = cy - 50 + 20 * (0.5 - 0.5 * math.cos(2 * math.pi * u * 4)) + 52 * edge ** 3
        fr.append((x, y))
    d.polygon([(x * S, y * S) for x, y in dome + fr], fill=HAIR)
    tuft = _bez((cx - 22, cy - R - 2), (cx - 4, cy - R - 70), (cx + 46, cy - R - 54), 14) + _bez((cx + 46, cy - R - 54), (cx + 14, cy - R - 30), (cx + 26, cy - R + 8), 14)
    d.polygon([(x * S, y * S) for x, y in tuft], fill=HAIR)
    _L(d, _arc(cx - 20, cy - 60, R - 40, R - 60, math.pi * 1.18, math.pi * 1.42), 10, HAIR_L)
    ey = cy + 18; ex = (cx - 56, cx + 56); lx, ly = look
    for i, x in enumerate(ex):
        if blink or (expr == "wink" and i == 0) or expr == "happy":
            _L(d, _arc(x, ey + 6, 26, 16, math.pi * 1.05, math.pi * 1.95), 9, INK); continue
        if expr == "cry":
            _L(d, _arc(x, ey - 4, 26, 12, math.pi * 0.05, math.pi * 0.95), 9, INK)
            d.polygon([(a * S, b * S) for a, b in [(x - 12, ey + 10), (x + 12, ey + 10), (x + 16, ey + 120), (x - 16, ey + 120)]], fill=(120, 190, 255)); continue
        rx, ry = (34, 40) if expr == "shock" else (27, 33)
        _E(d, x, ey, rx, ry, fill=WHITE, outline=INK, width=int(5 * S))
        if expr == "dizzy":
            sg = 1 if i else -1
            _L(d, [(x + (2 + 2.2 * a) * math.cos(sg * a), ey + (2 + 2.2 * a) * math.sin(sg * a)) for a in [k * 0.32 for k in range(40)]], 5, INK); continue
        pr = 9 if expr == "shock" else 15
        px = x + lx * 9; py = ey + 4 + ly * 9
        _E(d, px, py, pr, pr + 2, fill=INK); _E(d, px + 5, py - 6, 4.5, 4.5, fill=WHITE)
        if expr == "smug":  # párpado
            d.chord(((x - rx - 3) * S, (ey - ry - 3) * S, (x + rx + 3) * S, (ey + ry + 3) * S), 180, 360, fill=SK); _L(d, [(x - rx, ey), (x + rx, ey)], 6, INK)
    # cejas
    br = {"shock": (-62, -62), "confused": (-58, -44), "smug": (-46, -60), "cry": (-44, -44), "dizzy": (-50, -50)}.get(expr, (-52, -52))
    tilt = {"cry": 10, "confused": -8, "smug": 0}.get(expr, 0)
    _L(d, [(cx - 84, ey + br[0] + tilt), (cx - 30, ey + br[0] - tilt)], 11, HAIR); _L(d, [(cx + 30, ey + br[1] - tilt), (cx + 84, ey + br[1] + tilt)], 11, HAIR)
    for x in (cx - 92, cx + 92): _E(d, x, ey + 52, 22, 12, fill=(248, 160, 150))
    my = cy + 92
    if expr in ("shock",): _E(d, cx, my + 4, 24, 30, fill=INK); _E(d, cx, my + 20, 15, 9, fill=(225, 95, 105))
    elif expr in ("proud", "wink", "happy"):
        d.chord(((cx - 42) * S, (my - 26) * S, (cx + 42) * S, (my + 28) * S), 0, 180, fill=INK); d.chord(((cx - 32) * S, (my - 18) * S, (cx + 32) * S, (my + 2) * S), 0, 180, fill=WHITE)
    elif expr in ("confused", "dizzy"): _L(d, [(cx - 36 + i * 6, my + 6 * math.sin(i * 1.1)) for i in range(13)], 7, INK)
    elif expr == "smug": _L(d, [(cx - 36, my + 6), (cx, my + 10), (cx + 34, my - 6)], 8, INK)
    elif expr == "cry": d.chord(((cx - 36) * S, (my - 4) * S, (cx + 36) * S, (my + 40) * S), 180, 360, fill=INK)
    else: _L(d, _arc(cx, my - 12, 32, 18, 0.3, math.pi - 0.3), 8, INK)
    if sweat > 0: _E(d, cx + R - 20, cy - 50, 14, 20, fill=(140, 200, 255))

def draw(pose, expr="neutral", hands=("fist", "fist"), blink=False, look=(0, 0), sweat=0.0, phone=None):
    p = dict(BASE); p.update(pose)
    im = Image.new("RGBA", (CW * S, CH * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    hx, hy = HX, HY
    sq = p["squash"]; torso_h = 230 * (1 - 0.12 * sq); tw = 112 * (1 + 0.08 * sq)
    neck = (hx, hy - torso_h)
    sit = p["sit"]
    # piernas (de goma) — al sentarse se acortan
    legL = 290 * (1 - 0.35 * sit)
    for sgn, fx, fy in ((-1, p["lfx"], p["lfy"]), (1, p["rfx"], p["rfy"])):
        h0 = (hx + sgn * 46, hy - 6); f = (h0[0] + fx, h0[1] + fy * (1 - 0.35 * sit))
        _hose(d, h0, f, 56, JEANS, p["bend"], sgn, legL)
        _E(d, f[0] + sgn * 16, f[1] + 12, 46, 22, fill=SHOE, outline=SOLE, width=int(6 * S))
    # tronco: sudadera redondeada
    d.rounded_rectangle(((hx - tw) * S, (neck[1] - 10) * S, (hx + tw) * S, (hy + 30) * S), radius=int(70 * S), fill=HOOD)
    d.rounded_rectangle(((hx - tw) * S, (neck[1] - 10) * S, (hx - tw + 46) * S, (hy + 10) * S), radius=int(30 * S), fill=HOOD_L)
    d.rounded_rectangle(((hx - 62) * S, (hy - 90) * S, (hx + 62) * S, (hy - 30) * S), radius=int(22 * S), fill=HOOD_D)    # bolsillo
    d.rounded_rectangle(((hx - tw) * S, (hy + 4) * S, (hx + tw) * S, (hy + 30) * S), radius=int(14 * S), fill=HOOD_D)      # goma
    for o in (-24, 24): _L(d, [(hx + o, neck[1] + 20), (hx + o * 1.1, neck[1] + 92)], 7, (235, 235, 245))
    # brazos (de goma) desde los hombros
    for sgn, ax, ay, kind in ((-1, p["lhx"], p["lhy"], hands[0]), (1, p["rhx"], p["rhy"], hands[1])):
        sh = (hx + sgn * (tw - 16), neck[1] + 34); hnd = (sh[0] + ax, sh[1] + ay)
        _hose(d, sh, hnd, 44, HOOD, p["bend"], sgn, 225)
        if phone == ("l" if sgn < 0 else "r"):
            d.rounded_rectangle(((hnd[0] - 30) * S, (hnd[1] - 70) * S, (hnd[0] + 30) * S, (hnd[1] + 34) * S), radius=int(12 * S), fill=(25, 22, 40), outline=(150, 110, 255), width=int(4 * S))
            d.rounded_rectangle(((hnd[0] - 22) * S, (hnd[1] - 60) * S, (hnd[0] + 22) * S, (hnd[1] + 22) * S), radius=int(7 * S), fill=(95, 65, 210))
        r = 27
        if kind == "point":
            vx, vy = ax, ay; n = math.hypot(vx, vy) or 1; q = (hnd[0] + vx / n * 44, hnd[1] + vy / n * 44)
            _L(d, [hnd, q], 16, SK); _E(d, q[0], q[1], 8, 8, fill=SK)
        if kind == "open":
            for a in (-0.6, 0, 0.6):
                b = math.atan2(ay, ax) + a; q = (hnd[0] + math.cos(b) * 36, hnd[1] + math.sin(b) * 36)
                _L(d, [hnd, q], 13, SK); _E(d, q[0], q[1], 6.5, 6.5, fill=SK)
        _E(d, hnd[0], hnd[1], r, r, fill=SK)
    # cabeza (tapa el cuello: sin líneas raras)
    hcx = hx + 0; hcy = neck[1] - 118
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
