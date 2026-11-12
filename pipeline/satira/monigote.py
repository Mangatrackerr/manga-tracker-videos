# Muñeco de cuerpo entero (rig 2D) del chico de la sudadera: cabeza del personaje + tronco, brazos y piernas articulados.
# Ángulos en grados: 0 = hacia abajo; positivo = hacia fuera del cuerpo (para cada lado). ua/fa = brazo/antebrazo, th/sn = muslo/espinilla (absolutos).
import math
from PIL import Image, ImageDraw
import personaje as PJ

HOOD = PJ.HOOD; HOOD_D = PJ.HOOD_D; HOOD_L = PJ.HOOD_L; SK = PJ.SK; INK = PJ.INK
JEANS = (48, 70, 130); JEANS_D = (36, 52, 100); SHOE = (245, 245, 250); SOLE = (60, 60, 75)
CW, CH = 760, 1100; HX, HY = 380, 700  # lienzo y cadera (unidades 1x)
S = 2
BASE = dict(x=0, y=0, lean=0, head=0, l_ua=10, l_fa=6, r_ua=10, r_fa=6, l_th=6, l_sn=2, r_th=6, r_sn=2, sit=0.0, scale=1.0)
NUM = list(BASE)

_heads = {}
def head(expr, blink=False, look=(0, 0), sweat=0.0):
    k = (expr, blink, look, round(sweat, 1))
    if k not in _heads:
        im = PJ.draw(expr, blink=blink, look=look, sweat=sweat)
        _heads[k] = im.crop((150, 130, 610, 650)).resize((322, 364), Image.LANCZOS)  # cabeza ≈ 322 px de ancho (estilo chibi)
    return _heads[k]

def _v(a, sgn):  # vector unidad de un ángulo
    r = math.radians(a); return (sgn * math.sin(r), math.cos(r))
def _limb(d, p0, a, L, w, col, sgn):
    vx, vy = _v(a, sgn); p1 = (p0[0] + vx * L, p0[1] + vy * L)
    d.line([(p0[0] * S, p0[1] * S), (p1[0] * S, p1[1] * S)], fill=col, width=int(w * S))
    r = w / 2; d.ellipse(((p1[0] - r) * S, (p1[1] - r) * S, (p1[0] + r) * S, (p1[1] + r) * S), fill=col)
    d.ellipse(((p0[0] - r) * S, (p0[1] - r) * S, (p0[0] + r) * S, (p0[1] + r) * S), fill=col)
    return p1

def _hand(d, p, a, sgn, kind):
    r = 25; E = lambda cx, cy, rr, col: d.ellipse(((cx - rr) * S, (cy - rr) * S, (cx + rr) * S, (cy + rr) * S), fill=col)
    vx, vy = _v(a, sgn)
    if kind == "point":
        q = (p[0] + vx * 46, p[1] + vy * 46); d.line([(p[0] * S, p[1] * S), (q[0] * S, q[1] * S)], fill=SK, width=int(15 * S)); E(q[0], q[1], 7.5, SK)
    if kind == "open":
        for k in (-30, 0, 30):
            b = math.radians(a + k); q = (p[0] + sgn * math.sin(b) * 34, p[1] + math.cos(b) * 34)
            d.line([(p[0] * S, p[1] * S), (q[0] * S, q[1] * S)], fill=SK, width=int(12 * S)); E(q[0], q[1], 6, SK)
    E(p[0], p[1], r if kind != "fist" else 22, SK)

def draw(pose, expr="neutral", hands=("fist", "fist"), blink=False, look=(0, 0), sweat=0.0, phone=None):
    """devuelve RGBA CWxCH (1x). phone: 'l' o 'r' para llevar un móvil en esa mano"""
    p = dict(BASE); p.update(pose)
    im = Image.new("RGBA", (CW * S, CH * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    hx, hy = HX + p["x"], HY + p["y"]
    lean = math.radians(p["lean"]); up = (math.sin(lean), -math.cos(lean)); side = (math.cos(lean), math.sin(lean))
    # piernas (al sentarse se acortan: se ven en escorzo)
    ls = 1 - 0.5 * p["sit"]
    for sgn, th, sn in ((-1, p["l_th"], p["l_sn"]), (1, p["r_th"], p["r_sn"])):
        hp = (hx + sgn * 42 * side[0], hy + sgn * 42 * side[1])
        kn = _limb(d, hp, th, 135 * ls, 58, JEANS, sgn)
        ft = _limb(d, kn, sn, 130 * ls, 52, JEANS_D if p["sit"] > 0.5 else JEANS, sgn)
        d.ellipse(((ft[0] - 44 + sgn * 14) * S, (ft[1] - 8) * S, (ft[0] + 44 + sgn * 14) * S, (ft[1] + 34) * S), fill=SHOE, outline=SOLE, width=int(6 * S))
    # tronco (sudadera)
    nk = (hx + up[0] * 225, hy + up[1] * 225)
    def P(o_up, o_side): return ((hx + up[0] * o_up + side[0] * o_side) * S, (hy + up[1] * o_up + side[1] * o_side) * S)
    d.polygon([P(-30, -92), P(-30, 92), P(215, 108), P(235, 70), P(235, -70), P(215, -108)], fill=HOOD)
    d.polygon([P(-30, -92), P(-30, -40), P(215, -60), P(215, -108)], fill=HOOD_L)
    d.polygon([P(20, -60), P(20, 60), P(80, 50), P(80, -50)], fill=HOOD_D)  # bolsillo
    d.polygon([P(-30, -94), P(-30, 94), P(-5, 94), P(-5, -94)], fill=HOOD_D)  # goma
    for o in (-26, 26): d.line([P(220, o), P(150, o * 1.1)], fill=(235, 235, 245), width=int(7 * S))
    # brazos
    for sgn, ua, fa, kind in ((-1, p["l_ua"], p["l_fa"], hands[0]), (1, p["r_ua"], p["r_fa"], hands[1])):
        sh = (nk[0] + sgn * 96 * side[0] - up[0] * 22, nk[1] + sgn * 96 * side[1] - up[1] * 22)
        el = _limb(d, sh, ua + sgn * 0, 118, 50, HOOD, sgn)
        wr = _limb(d, el, fa, 112, 46, HOOD if kind != "none" else HOOD, sgn)
        wr2 = (wr[0] + _v(fa, sgn)[0] * 14, wr[1] + _v(fa, sgn)[1] * 14)
        _hand(d, wr2, fa, sgn, kind)
        if phone == ("l" if sgn < 0 else "r"):
            d.rounded_rectangle(((wr2[0] - 26) * S, (wr2[1] - 52) * S, (wr2[0] + 26) * S, (wr2[1] + 40) * S), radius=10 * S, fill=(25, 22, 40), outline=(150, 110, 255), width=int(4 * S))
            d.rounded_rectangle(((wr2[0] - 19) * S, (wr2[1] - 44) * S, (wr2[0] + 19) * S, (wr2[1] + 30) * S), radius=6 * S, fill=(90, 60, 200))
            _hand(d, (wr2[0], wr2[1] + 18), fa, sgn, "fist")
    out = im.resize((CW, CH), Image.LANCZOS)
    # cabeza (rotada con la inclinación)
    h = head(expr, blink, look, sweat)
    ang = -(p["lean"] + p["head"])
    if abs(ang) > 0.5: h = h.rotate(ang, resample=Image.BICUBIC, expand=True)
    hc = (nk[0] + up[0] * 140, nk[1] + up[1] * 140)
    out.alpha_composite(h, (int(hc[0] - h.width / 2), int(hc[1] - h.height / 2)))
    return out

def lerp_pose(a, b, k):
    return {n: a.get(n, BASE[n]) + (b.get(n, BASE[n]) - a.get(n, BASE[n])) * k for n in NUM}
def ease(k): k = max(0.0, min(1.0, k)); return k * k * (3 - 2 * k)

class Track:
    """keyframes: [(t, pose, expr, hands, extra)] — interpola poses; expr/hands cambian en cada keyframe"""
    def __init__(self, keys): self.keys = keys
    def at(self, T, times):
        ks = [(times(k[0]), *k[1:]) for k in self.keys]
        prev = ks[0]
        for k in ks[1:]:
            if T < k[0]:
                dur = min(0.35, max(0.12, (k[0] - prev[0])))
                kk = ease((T - (k[0] - dur)) / dur) if T > k[0] - dur else 0
                return lerp_pose(prev[1], k[1], kk), (prev[2] if kk < 0.5 else k[2]), (prev[3] if kk < 0.5 else k[3]), (prev[4] if len(prev) > 4 else {})
            prev = k
        return lerp_pose(prev[1], prev[1], 0), prev[2], prev[3], (prev[4] if len(prev) > 4 else {})

# poses útiles
P = {
 "stand": dict(), "relax": dict(l_ua=14, l_fa=8, r_ua=14, r_fa=8),
 "shock": dict(l_ua=120, l_fa=205, r_ua=120, r_fa=205, l_th=14, r_th=14, y=-10),         # manos a las mejillas
 "point_r": dict(r_ua=95, r_fa=95, l_ua=12, l_fa=8, lean=-4),                          # señala a su izquierda (derecha de la pantalla)
 "point_l": dict(l_ua=95, l_fa=95, r_ua=12, r_fa=8, lean=4),
 "wave": dict(r_ua=150, r_fa=170, lean=-3),
 "present": dict(r_ua=70, r_fa=110, l_ua=12, l_fa=8, lean=-3),                           # mano abierta presentando algo
 "scratch": dict(r_ua=125, r_fa=215, l_ua=14, l_fa=10, head=6),                           # rascarse la cabeza
 "facepalm": dict(r_ua=70, r_fa=200, l_ua=14, l_fa=10, head=-8, lean=-4),
 "arms_up": dict(l_ua=160, l_fa=170, r_ua=160, r_fa=170, y=-25),
 "shrug": dict(l_ua=60, l_fa=130, r_ua=60, r_fa=130, head=8),
 "sit": dict(sit=1, y=40, l_th=14, l_sn=10, r_th=14, r_sn=10),
 "sit_phone": dict(sit=1, y=40, l_th=14, l_sn=10, r_th=14, r_sn=10, r_ua=30, r_fa=160, l_ua=25, l_fa=150),
 "dizzy": dict(lean=8, head=12, l_ua=40, l_fa=20, r_ua=40, r_fa=20, l_th=12, r_th=4),
 "fall": dict(lean=-35, head=-10, l_ua=150, l_fa=170, r_ua=150, r_fa=170, l_th=60, l_sn=80, r_th=40, r_sn=60, y=60),
 "tap": dict(r_ua=40, r_fa=190, l_ua=12, l_fa=8),                                          # se toca la barbilla / espera
}

if __name__ == "__main__":
    import sys
    names = ["stand", "shock", "point_r", "wave", "scratch", "facepalm", "shrug", "sit_phone", "dizzy", "fall", "arms_up"]
    ex = {"shock": "shock", "scratch": "confused", "facepalm": "cry", "dizzy": "dizzy", "fall": "shock", "wave": "wink", "sit_phone": "smug"}
    hd = {"point_r": ("fist", "point"), "wave": ("fist", "open"), "shrug": ("open", "open"), "arms_up": ("open", "open"), "shock": ("open", "open")}
    sheet = Image.new("RGBA", (CW * 6, CH * 2), (40, 30, 60, 255))
    for i, n in enumerate(names):
        sheet.alpha_composite(draw(P[n], ex.get(n, "neutral"), hd.get(n, ("fist", "fist")), phone="r" if n == "sit_phone" else None), ((i % 6) * CW, (i // 6) * CH))
    sheet.convert("RGB").resize((CW * 3, CH)).save(sys.argv[1])
