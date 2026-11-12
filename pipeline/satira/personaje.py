# Personaje plano estilo "explainer satírico" (trend nov-2026): el amigo otaku.
# Se dibuja a 2x y se reduce para suavizar bordes. Todo vectorial con PIL, sin imágenes externas.
import math
from PIL import Image, ImageDraw, ImageFilter

SK = (238, 190, 152); SK_D = (205, 150, 115); HAIR = (34, 28, 44); HAIR_L = (62, 52, 80)
HOOD = (92, 52, 178); HOOD_D = (64, 34, 130); HOOD_L = (120, 80, 210)
PH = (40, 40, 52); PH_L = (150, 110, 255); WHITE = (255, 255, 255); INK = (22, 16, 30)
CW, CH = 760, 980  # lienzo final
_cache = {}

def _poly(d, pts, s, **kw): d.polygon([(x * s, y * s) for x, y in pts], **kw)
def _ell(d, cx, cy, rx, ry, s, **kw): d.ellipse(((cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s), **kw)
def _line(d, pts, s, w, **kw): d.line([(x * s, y * s) for x, y in pts], width=int(w * s), joint="curve", **kw)
def _curve(cx, cy, w, h, n=16, a0=0, a1=math.pi):
    return [(cx + w * math.cos(a0 + (a1 - a0) * i / n), cy + h * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]

def draw(expr="neutral", blink=False, look=(0, 0), glasses=False, sash=None, sweat=0.0, s=2):
    """expr: neutral | smug | confused | shock | proud. Devuelve RGBA CWxCH."""
    key = (expr, blink, look, glasses, sash, round(sweat, 1))
    if key in _cache: return _cache[key]
    im = Image.new("RGBA", (CW * s, CH * s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, hy = 380, 410  # centro de la cabeza
    # --- cuerpo / sudadera ---
    _poly(d, [(110, 980), (150, 760), (230, 690), (530, 690), (610, 760), (650, 980)], s, fill=HOOD)
    _poly(d, [(150, 760), (230, 690), (260, 700), (205, 980), (110, 980)], s, fill=HOOD_L)
    _ell(d, cx, 700, 150, 55, s, fill=HOOD_D)  # capucha caída
    # cordones
    _line(d, [(345, 715), (338, 840)], s, 9, fill=(235, 235, 245)); _line(d, [(415, 715), (422, 840)], s, 9, fill=(235, 235, 245))
    _ell(d, 338, 846, 9, 12, s, fill=(235, 235, 245)); _ell(d, 422, 846, 9, 12, s, fill=(235, 235, 245))
    if sash:  # banda de embajador
        _poly(d, [(205, 700), (265, 690), (640, 980), (560, 980)], s, fill=(200, 30, 50))
        _poly(d, [(215, 700), (240, 696), (605, 980), (585, 980)], s, fill=(250, 200, 70))
        _ell(d, 470, 860, 34, 34, s, fill=(250, 200, 70)); _ell(d, 470, 860, 22, 22, s, fill=(225, 160, 40))
    # cuello
    _poly(d, [(335, 560), (425, 560), (450, 700), (310, 700)], s, fill=SK_D); _ell(d, cx, 640, 70, 26, s, fill=(185, 130, 100))
    # cascos al cuello
    _line(d, _curve(cx, 690, 165, 60, 20, math.pi, 2 * math.pi)[::-1], s, 22, fill=PH)
    for sx in (-1, 1):
        _ell(d, cx + sx * 168, 690, 46, 58, s, fill=PH); _ell(d, cx + sx * 168, 690, 30, 40, s, fill=PH_L)
    # orejas
    for sx in (-1, 1):
        _ell(d, cx + sx * 178, hy + 30, 34, 46, s, fill=SK); _ell(d, cx + sx * 180, hy + 30, 16, 26, s, fill=SK_D)
    # cabeza
    _ell(d, cx, hy, 182, 200, s, fill=SK)
    _ell(d, cx, hy + 150, 120, 50, s, fill=SK)  # mandíbula
    # pelo: casquete + flequillo en picos
    _ell(d, cx, hy - 95, 196, 128, s, fill=HAIR)
    spikes = [(186, 360), (215, 300), (240, 365), (275, 290), (305, 350), (345, 280), (375, 345), (420, 278), (448, 345),
              (490, 290), (515, 360), (545, 305), (575, 375), (585, 250), (380, 200), (175, 250)]
    _poly(d, spikes, s, fill=HAIR)
    _poly(d, [(330, 230), (360, 150), (395, 225)], s, fill=HAIR); _poly(d, [(400, 225), (450, 160), (450, 240)], s, fill=HAIR)
    _line(d, [(260, 250), (300, 215)], s, 10, fill=HAIR_L); _line(d, [(440, 215), (480, 245)], s, 10, fill=HAIR_L)
    # --- cara ---
    ex = (310, 450); ey = 440; lx, ly = look
    if glasses:
        for x in ex: d.rounded_rectangle(((x - 62) * s, (ey - 38) * s, (x + 62) * s, (ey + 40) * s), radius=30 * s, fill=INK)
        _line(d, [(372, ey - 22), (388, ey - 22)], s, 12, fill=INK)
        for x in ex: _line(d, [(x - 36, ey - 18), (x - 10, ey - 26)], s, 7, fill=(110, 110, 140))
        _line(d, [(cx - 128, ey - 60), (cx - 30, ey - 70)], s, 14, fill=HAIR); _line(d, [(cx + 30, ey - 76), (cx + 128, ey - 66)], s, 14, fill=HAIR)
    else:
        for i, x in enumerate(ex):
            if blink or expr == "cry":
                if expr == "cry":
                    _line(d, _curve(x, ey - 6, 36, 14, 10, math.pi, 2 * math.pi), s, 10, fill=INK)
                    _poly(d, [(x - 14, ey + 8), (x + 14, ey + 8), (x + 20, ey + 210), (x - 20, ey + 210)], s, fill=(120, 190, 255))
                    continue
                _line(d, _curve(x, ey + 4, 36, 10, 10, 0, math.pi), s, 9, fill=INK); continue
            if expr == "wink" and i == 0:
                _line(d, _curve(x, ey + 4, 36, -14, 10, 0, math.pi), s, 10, fill=INK); continue
            ry = 50 if expr != "shock" else 60; rx = 42 if expr != "shock" else 50
            _ell(d, x, ey, rx, ry, s, fill=WHITE, outline=INK, width=int(4 * s))
            if expr == "dizzy":  # ojos en espiral
                pts = [(x + (3 + 2.6 * a) * math.cos(a * (1 if i else -1)), ey + (3 + 2.6 * a) * math.sin(a * (1 if i else -1))) for a in [k * 0.3 for k in range(48)]]
                _line(d, pts, s, 6, fill=INK); continue
            pr = 21 if expr != "shock" else 12
            px = x + lx * 12 + (6 if (expr == "confused" and i == 0) else -6 if expr == "confused" else 0); py = ey + 6 + ly * 12
            _ell(d, px, py, pr, pr + 2, s, fill=INK); _ell(d, px + 6, py - 7, 5, 5, s, fill=WHITE)
            if expr in ("smug", "proud"):  # párpado caído
                d.chord(((x - rx - 3) * s, (ey - ry - 3) * s, (x + rx + 3) * s, (ey + ry + 3) * s), 180, 360, fill=SK)
                _line(d, [(x - rx, ey), (x + rx, ey)], s, 7, fill=INK)
        # cejas
        if expr == "smug":
            _line(d, [(cx - 120, ey - 58), (cx - 30, ey - 50)], s, 14, fill=HAIR); _line(d, [(cx + 30, ey - 72), (cx + 120, ey - 92)], s, 14, fill=HAIR)
        elif expr == "cry":
            _line(d, [(cx - 120, ey - 58), (cx - 30, ey - 78)], s, 14, fill=HAIR); _line(d, [(cx + 30, ey - 78), (cx + 120, ey - 58)], s, 14, fill=HAIR)
        elif expr == "confused":
            _line(d, [(cx - 120, ey - 70), (cx - 30, ey - 58)], s, 14, fill=HAIR); _line(d, [(cx + 30, ey - 50), (cx + 120, ey - 78)], s, 14, fill=HAIR)
        elif expr == "shock":
            _line(d, [(cx - 120, ey - 82), (cx - 30, ey - 92)], s, 14, fill=HAIR); _line(d, [(cx + 30, ey - 92), (cx + 120, ey - 82)], s, 14, fill=HAIR)
        elif expr == "proud":
            _line(d, [(cx - 120, ey - 70), (cx - 30, ey - 66)], s, 14, fill=HAIR); _line(d, [(cx + 30, ey - 66), (cx + 120, ey - 70)], s, 14, fill=HAIR)
        else:
            _line(d, [(cx - 120, ey - 66), (cx - 30, ey - 62)], s, 14, fill=HAIR); _line(d, [(cx + 30, ey - 62), (cx + 120, ey - 66)], s, 14, fill=HAIR)
    # nariz
    _line(d, [(cx + 4, 480), (cx - 8, 520), (cx + 10, 524)], s, 7, fill=SK_D)
    # mejillas
    for x in (270, 490): _ell(d, x, 530, 30, 16, s, fill=(245, 160, 150))
    # boca
    my = 575
    if expr == "wink":
        d.chord(((cx - 55) * s, (my - 35) * s, (cx + 55) * s, (my + 30) * s), 10, 170, fill=INK)
        d.chord(((cx - 42) * s, (my - 26) * s, (cx + 42) * s, (my + 6) * s), 20, 160, fill=WHITE)
    elif expr == "dizzy":
        pts = [(cx - 60 + i * 8, my + 9 * math.sin(i * 0.9)) for i in range(16)]; _line(d, pts, s, 9, fill=INK)
    elif expr in ("smug", "proud") or glasses:
        _line(d, [(cx - 60, my + 5), (cx - 10, my + 12), (cx + 40, my + 2), (cx + 72, my - 22)], s, 10, fill=INK)
        if expr == "proud" or glasses:
            d.chord(((cx - 50) * s, (my - 30) * s, (cx + 60) * s, (my + 30) * s), 10, 170, fill=INK)
            d.chord(((cx - 38) * s, (my - 22) * s, (cx + 48) * s, (my + 8) * s), 20, 160, fill=WHITE)
    elif expr == "cry":
        d.chord(((cx - 55) * s, (my - 10) * s, (cx + 55) * s, (my + 60) * s), 180, 360, fill=INK)
    elif expr == "confused":
        pts = [(cx - 60 + i * 8, my + 6 * math.sin(i * 1.2)) for i in range(16)]; _line(d, pts, s, 9, fill=INK)
    elif expr == "shock":
        _ell(d, cx, my + 5, 34, 44, s, fill=INK); _ell(d, cx, my + 30, 22, 14, s, fill=(220, 90, 100))
    else:
        _line(d, _curve(cx, my - 18, 48, 24, 12, 0.25, math.pi - 0.25), s, 10, fill=INK)
    # sudor
    if sweat > 0:
        for k in range(int(sweat * 2 + 0.5)):
            x0, y0 = (570, 330) if k == 0 else (195, 360)
            _poly(d, [(x0, y0), (x0 - 20, y0 + 42), (x0 + 20, y0 + 42)], s, fill=(140, 200, 255))
            _ell(d, x0, y0 + 46, 21, 21, s, fill=(140, 200, 255)); _ell(d, x0 - 6, y0 + 40, 6, 8, s, fill=WHITE)
    out = im.resize((CW, CH), Image.LANCZOS)
    # sombra suave de contorno para separarlo del fondo
    a = out.getchannel("A").filter(ImageFilter.GaussianBlur(14))
    glow = Image.new("RGBA", out.size, (0, 0, 0, 0)); glow.putalpha(a.point(lambda v: int(v * 0.55)))
    res = Image.new("RGBA", out.size, (0, 0, 0, 0)); res.alpha_composite(glow, (6, 14)); res.alpha_composite(out)
    _cache[key] = res; return res

if __name__ == "__main__":
    import sys
    row = Image.new("RGBA", (CW * 6, CH), (40, 30, 60, 255))
    for i, (e, kw) in enumerate([("neutral", {}), ("smug", {}), ("confused", {"sweat": 1}), ("shock", {"sweat": 2}), ("proud", {"glasses": True, "sash": True}), ("neutral", {"blink": True})]):
        row.alpha_composite(draw(e, **kw), (i * CW, 0))
    row.convert("RGB").resize((CW * 3, CH // 2)).save(sys.argv[1])
