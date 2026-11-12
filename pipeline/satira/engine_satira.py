# Motor estilo "explainer satírico" (trend nov-2026): narrador irónico "¿Sabías que...?", personaje plano,
# "invento" revelado en pedestal con rayos, insignias tipo HUD, medidores, sellos y subtítulos ARRIBA palabra a palabra.
import os, sys, math, random, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "gancho")); sys.path.insert(0, HERE)
from engine import (W, H, FPS, SR, LG, MB, YEL, PUR, WHITE, RED, GREEN, DARK, text_img, fit_text, paste_c, pop, ease_out, clamp,
                    pill, big, load_clip, PHONE, MASK, BZ, SCR_W, SCR_H, CROP, LOGO, SFX, M, Offs, at, _clips, P, GAP)
import personaje as PJ
GOLD = (255, 200, 70)

# ---------- fondos pre-renderizados (un poco más grandes para el movimiento de cámara) ----------
BW, BH = W + 160, H + 160
def _grad(c1, c2, h=BH, w=BW):
    t = np.linspace(0, 1, h)[:, None, None]
    return (np.array(c1) * (1 - t) + np.array(c2) * t).repeat(w, 1).astype(np.uint8)
def _room():
    im = Image.fromarray(_grad((28, 22, 58), (12, 8, 26)), "RGB").convert("RGBA"); d = ImageDraw.Draw(im)
    # ventana con ciudad de noche y luna
    wx, wy, ww, wh = 90, 330, 470, 560
    d.rounded_rectangle((wx - 18, wy - 18, wx + ww + 18, wy + wh + 18), radius=20, fill=(60, 46, 96))
    win = Image.fromarray(_grad((30, 40, 100), (90, 60, 130), wh, ww), "RGB"); wd = ImageDraw.Draw(win)
    wd.ellipse((ww - 170, 50, ww - 70, 150), fill=(255, 240, 200))
    rnd = random.Random(4)
    for _ in range(40):
        x = rnd.uniform(0, ww); y = rnd.uniform(0, wh * 0.5); wd.ellipse((x, y, x + 3, y + 3), fill=(255, 255, 255))
    x = 0
    while x < ww:
        bw = rnd.randint(50, 110); bh = rnd.randint(150, 380); col = (20 + rnd.randint(0, 15), 18, 45)
        wd.rectangle((x, wh - bh, x + bw, wh), fill=col)
        for yy in range(wh - bh + 14, wh - 10, 30):
            for xx in range(x + 10, x + bw - 14, 22):
                if rnd.random() < 0.45: wd.rectangle((xx, yy, xx + 10, yy + 14), fill=(255, 200, 110))
        x += bw + 4
    im.paste(win, (wx, wy)); d.line((wx + ww / 2, wy, wx + ww / 2, wy + wh), fill=(60, 46, 96), width=14)
    d.line((wx, wy + wh / 2, wx + ww, wy + wh / 2), fill=(60, 46, 96), width=14)
    # estantería con tomos (lomos de colores, sin títulos)
    sx = 700
    for k, sy in enumerate((420, 700, 980)):
        d.rectangle((sx - 20, sy + 200, BW, sy + 226), fill=(80, 56, 40))
        x = sx; r2 = random.Random(k + 9)
        while x < BW - 30:
            bw = r2.randint(30, 52); bh = r2.randint(150, 196)
            col = r2.choice([(230, 70, 90), (90, 160, 255), (255, 190, 60), (130, 90, 230), (60, 200, 150), (240, 240, 245), (250, 120, 60)])
            d.rounded_rectangle((x, sy + 200 - bh, x + bw, sy + 200), radius=5, fill=col)
            d.rectangle((x + 5, sy + 200 - bh + 22, x + bw - 5, sy + 200 - bh + 32), fill=(255, 255, 255, 150))
            x += bw + 3
    # lámpara cálida
    glow = Image.new("RGBA", (BW, BH), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.ellipse((-300, 900, 700, 1900), fill=(255, 150, 60, 70)); glow = glow.filter(ImageFilter.GaussianBlur(160))
    im.alpha_composite(glow)
    vig = Image.new("L", (BW, BH), 0); ImageDraw.Draw(vig).ellipse((-400, -200, BW + 400, BH + 300), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(200)); dark = Image.new("RGBA", (BW, BH), (0, 0, 0, 255)); dark.putalpha(vig.point(lambda v: int((255 - v) * 0.8)))
    im.alpha_composite(dark); return im
ROOM = _room()
ROOM_RED = Image.blend(ROOM, Image.new("RGBA", ROOM.size, (150, 10, 40, 255)), 0.42)
ROOM_BLUR = Image.blend(ROOM.filter(ImageFilter.GaussianBlur(18)), Image.new("RGBA", ROOM.size, (10, 6, 24, 255)), 0.45)

def _rays(col1=(120, 70, 20), col2=(40, 20, 10), n=18):
    S = 2600; im = Image.new("RGB", (S, S), col2); d = ImageDraw.Draw(im); c = S / 2
    for k in range(n):
        a0 = 2 * math.pi * k / n; a1 = a0 + math.pi / n
        d.polygon([(c, c), (c + S * math.cos(a0), c + S * math.sin(a0)), (c + S * math.cos(a1), c + S * math.sin(a1))], fill=col1)
    return im
_R = _rays(); RAYS = []
for i in range(36):  # un periodo (360/18 = 20º) en 36 pasos
    r = _R.rotate(i * 20 / 36, resample=Image.BILINEAR); c = r.width / 2
    fr = r.crop((int(c - W / 2), int(c - H * 0.38), int(c + W / 2), int(c + H * 0.62))).convert("RGBA")
    g = Image.new("L", (W, H), 0); ImageDraw.Draw(g).ellipse((-350, -400, W + 350, H * 0.85), fill=255); g = g.filter(ImageFilter.GaussianBlur(220))
    dk = Image.new("RGBA", (W, H), (12, 6, 4, 255)); dk.putalpha(g.point(lambda v: 255 - v)); fr.alpha_composite(dk); RAYS.append(fr)

def _pedestal():
    s = 2; w, h = 700, 520; im = Image.new("RGBA", (w * s, h * s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((60 * s, 90 * s, 640 * s, 440 * s), fill=(150, 20, 40))
    for k in range(9): d.line(((90 + k * 65) * s, 100 * s, (90 + k * 65) * s, 430 * s), fill=(170, 30, 52), width=10 * s)
    d.ellipse((60 * s, 380 * s, 640 * s, 500 * s), fill=(150, 20, 40))
    d.arc((60 * s, 380 * s, 640 * s, 500 * s), 0, 180, fill=GOLD, width=10 * s)
    d.ellipse((60 * s, 30 * s, 640 * s, 150 * s), fill=(185, 35, 60), outline=GOLD, width=10 * s)
    d.ellipse((140 * s, 60 * s, 560 * s, 120 * s), outline=(210, 60, 80), width=4 * s)
    return im.resize((w, h), Image.LANCZOS)
PEDESTAL = _pedestal()

def _brain():
    s = 2; w, h = 440, 340; im = Image.new("RGBA", (w * s, h * s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    base = (250, 150, 175); dk = (205, 90, 125)
    for (x, y, r) in [(120, 120, 95), (220, 90, 105), (320, 120, 95), (110, 210, 90), (220, 200, 110), (330, 210, 90), (220, 260, 80)]:
        d.ellipse(((x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s), fill=base)
    d.line((220 * s, 30 * s, 215 * s, 300 * s), fill=dk, width=8 * s)
    rnd = random.Random(2)
    for _ in range(14):
        x = rnd.uniform(60, 380); y = rnd.uniform(60, 270); a = rnd.uniform(0, math.pi)
        pts = [((x + 28 * math.cos(a + t / 3)) * s + 0, (y + 14 * math.sin(t * 1.4) + 6 * t) * s) for t in range(6)]
        d.line(pts, fill=dk, width=7 * s, joint="curve")
    d.ellipse((150 * s, 50 * s, 200 * s, 80 * s), fill=(255, 210, 225))
    out = im.resize((w, h), Image.LANCZOS)
    g = Image.new("RGBA", (w + 300, h + 300), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse((60, 60, w + 240, h + 240), fill=(255, 220, 120, 170)); g = g.filter(ImageFilter.GaussianBlur(60))
    g.alpha_composite(out, (150, 150)); return g
BRAIN = _brain()

# ---------- elementos ----------
def hud(l1, l2, dot=GREEN, w=760):
    im = Image.new("RGBA", (w, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, 149), radius=34, fill=(12, 14, 26, 215), outline=(255, 255, 255, 60), width=3)
    d.ellipse((38, 52, 78, 92), fill=dot)
    a = fit_text(l1, w - 140, 54, path=MB, fill=WHITE); b = fit_text(l2, w - 140, 40, path=MB, fill=dot)
    im.alpha_composite(a, (80, 4)); im.alpha_composite(b, (82, 62)); return im
def meter(label, k, pct_txt, w=820, col=None):
    im = Image.new("RGBA", (w, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    lab = text_img(label, MB, 50, fill=WHITE, stroke=5); im.alpha_composite(lab, (-14, -14))
    pt = text_img(pct_txt, MB, 50, fill=col or RED, stroke=5); im.alpha_composite(pt, (w - pt.width + 14, -14))
    d.rounded_rectangle((0, 82, w - 1, 138), radius=28, fill=(20, 16, 34), outline=WHITE, width=4)
    fw = int((w - 16) * clamp(k))
    if fw > 20:
        g = np.zeros((40, w - 16, 3), np.uint8); x = np.linspace(0, 1, w - 16)
        cols = np.array([(40, 200, 110), (255, 215, 60), (240, 60, 70)], float)
        c = np.where(x[:, None] < 0.5, cols[0] + (cols[1] - cols[0]) * (x[:, None] / 0.5), cols[1] + (cols[2] - cols[1]) * ((x[:, None] - 0.5) / 0.5))
        if col: c[:] = col
        g[:] = c.astype(np.uint8); gi = Image.fromarray(g[:, :fw]).convert("RGBA")
        mk = Image.new("L", (fw, 40), 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, fw - 1, 39), radius=20, fill=255)
        im.paste(gi, (8, 90), mk)
    return im
def stamp(txt, col=RED, size=96, sub=None):
    t = text_img(txt, LG, size, fill=col); w = t.width - 20; h = t.height - 20 + (60 if sub else 0)
    im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 20, w + 20, h + 20), radius=18, fill=(0, 0, 0, 120), outline=col, width=10)
    im.alpha_composite(t, (30, 26))
    if sub: s_ = text_img(sub, MB, 44, fill=col); im.alpha_composite(s_, (int((w + 40) / 2 - s_.width / 2), h - 54))
    return im
def tile(txt, col):
    im = Image.new("RGBA", (210, 130), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 10, 204, 128), radius=22, fill=(0, 0, 0, 110))
    d.rounded_rectangle((0, 0, 198, 118), radius=22, fill=col); d.rectangle((0, 0, 18, 118), fill=tuple(int(c * 0.7) for c in col))
    t = fit_text(txt, 160, 60, fill=WHITE, stroke=5, sfill=(0, 0, 0)); im.alpha_composite(t, (int(108 - t.width / 2), int(59 - t.height / 2)))
    return im
TILES = [tile(t, c) for t, c in [("EP 7", (230, 70, 90)), ("CAP 112", (90, 150, 255)), ("T2", (255, 170, 40)), ("VOL 5", (130, 90, 230)),
                                  ("EP 23", (50, 190, 140)), ("CAP 48", (240, 110, 60)), ("EP 3", (200, 80, 200)), ("CAP 210", (60, 170, 220))]]

def cam(bg, T, z0=1.07, dur=0.5, drift=(0, 0)):
    """movimiento de cámara: zoom de entrada + deriva lenta"""
    z = 1 + (z0 - 1) * (1 - ease_out(T / dur)) + 0.012 * T
    w, h = int(W / z), int(H / z); ox = (BW - w) / 2 + drift[0] * T; oy = (BH - h) / 2 + drift[1] * T
    return bg.crop((int(ox), int(oy), int(ox) + w, int(oy) + h)).resize((W, H), Image.BILINEAR)

def char(im, T, expr, x=W / 2, y=1350, sc=1.12, shake=0.0, **kw):
    blink = (T % 3.1) > 2.98 and not kw.get("glasses") and expr != "shock"
    c = PJ.draw(expr, blink=blink, **kw)
    bob = 7 * math.sin(T * 2.4); sh = shake * 10 * math.sin(T * 70)
    paste_c(im, c, x + sh, y + bob + 40 * (1 - ease_out(T / 0.35)), sc * (0.96 + 0.04 * ease_out(T / 0.35)))

# ---------- escenas: (dibujar(T,d,o), sfx(d,o)) ----------
def Sc_intro(tiles_at=(1, 0), count=30, label="SERIES A LA VEZ"):
    def draw(T, d, o):
        im = cam(ROOM, T); ta = at(tiles_at, o); smug = T >= ta
        char(im, T, "smug" if smug else "neutral")
        if T >= ta:
            u = T - ta
            for i, tl in enumerate(TILES):
                a = 2 * math.pi * i / len(TILES) + u * 0.6; r = 400 + 30 * math.sin(u * 2 + i)
                x = W / 2 + r * math.cos(a); y = 1000 + 300 * math.sin(a)
                if y > 1080 and abs(x - W / 2) < 260: continue  # no tapar la cara
                paste_c(im, tl, x, y, pop(u, 0.08 * i, 0.3), rot=8 * math.sin(u * 2 + i))
            n = int(round(count * ease_out(u / 1.4)))
            paste_c(im, pill(f"{n} {label}", 64, fg=DARK, bg=YEL), W / 2, 620, pop(u, 0.2, 0.3), rot=-3)
        return im
    def sfx(d, o):
        ta = at(tiles_at, o); return [(0, "whoosh2", 0.7), (ta, "boom", 0.5)] + [(ta + 0.08 * i, "pop", 0.6) for i in range(8)]
    return draw, sfx

def Sc_reveal(name1, name2, name_at=(0, 0, 0.45)):
    def draw(T, d, o):
        im = RAYS[int(T * 12) % 36].copy()
        paste_c(im, PEDESTAL, W / 2, 1530, pop(T, 0.0, 0.35))
        rise = ease_out((T - 0.15) / 0.6)
        if T > 0.15:
            paste_c(im, BRAIN, W / 2, 1180 + 160 * (1 - rise) + 14 * math.sin(T * 3), 0.6 + 0.4 * rise)
            rnd = random.Random(int(T * 6))
            dr = ImageDraw.Draw(im)
            for k in range(7):  # destellos
                x = W / 2 + rnd.uniform(-380, 380); y = rnd.uniform(950, 1450); r = rnd.uniform(6, 16)
                dr.polygon([(x, y - r * 2.2), (x + r * 0.5, y), (x, y + r * 2.2), (x - r * 0.5, y)], fill=(255, 240, 190))
                dr.polygon([(x - r * 2.2, y), (x, y - r * 0.5), (x + r * 2.2, y), (x, y + r * 0.5)], fill=(255, 240, 190))
        tn = at(name_at, o)
        paste_c(im, big(name1, 120, YEL, (110, 40, 0)), W / 2, 700, pop(T, tn, 0.32))
        paste_c(im, big(name2 + "™", 120, YEL, (110, 40, 0)), W / 2, 840, pop(T, tn + 0.12, 0.32))
        return im
    return draw, lambda d, o: [(0, "boom", 0.8), (0.2, "shine", 0.9), (at(name_at, o), "boom", 0.6)]

def Sc_hud(expr, l1, l2, hud_at=(0, 0, 0.5), arrow=True, glasses=False, meters=None, dot=GREEN):
    """meters: [(label, valor, texto, tiempo, color)]"""
    def draw(T, d, o):
        im = cam(ROOM, T, drift=(6, 0)); char(im, T, expr, glasses=glasses)
        if arrow and T > 0.3:
            dr = ImageDraw.Draw(im); k = ease_out((T - 0.3) / 0.3); bx = 900 + 10 * math.sin(T * 8)
            dr.line((bx, 820, bx - 120 * k, 900), fill=YEL, width=16)
            if k > 0.9: dr.polygon([(bx - 150, 915), (bx - 95, 870), (bx - 110, 935)], fill=YEL)
        if hud_at is not None: th = at(hud_at, o); paste_c(im, hud(l1, l2, dot), W / 2, 640, pop(T, th, 0.3))
        for i, (lab, val, txt, tm, col) in enumerate(meters or []):
            tm = at(tm, o); k = ease_out((T - tm) / 0.8) * val
            if T >= tm: paste_c(im, meter(lab, k, txt if k >= val * 0.98 else f"{int(k * 100)} %", col=col), W / 2, 590 + i * 170, pop(T, tm, 0.25))
        return im
    def sfx(d, o):
        ev = [(at(hud_at, o), "pop2", 1.0)] if hud_at is not None else []
        for (_, _, _, tm, _) in meters or []: ev += [(at(tm, o) + k * 0.05, "tick", 1) for k in range(16)]
        return ev
    return draw, sfx

def Sc_question(level, hud_l1, cycle, st_txt, st_at=(0, 0, 0.62), st_sub=None):
    """el personaje no recuerda: HUD que va cambiando valores sin acertar + sello"""
    def draw(T, d, o):
        im = cam(ROOM_RED, T, z0=1.1, dur=0.3); ts = at(st_at, o)
        ex = "confused" if level < 2 or T < ts else "shock"
        char(im, T, ex, sweat=min(2, level + (1 if T >= ts else 0)), shake=1 if T >= ts else 0.3, look=(math.sin(T * 5), 0))
        v = cycle[int(T * 7) % len(cycle)] if T < ts else "???"
        paste_c(im, hud(hud_l1, v, dot=RED if T >= ts else YEL), W / 2, 600, pop(T, 0.05, 0.25))
        if T >= ts:
            u = T - ts; sc = 1 + 1.2 * (1 - ease_out(u / 0.18))
            paste_c(im, stamp(st_txt, RED, 110, st_sub), W / 2, 830, sc, clamp(u / 0.08), rot=-8)
        return im
    def sfx(d, o): return [(0, "boom", 0.4)] + [(k / 7, "tick", 0.8) for k in range(int(at(st_at, o) * 7))] + [(at(st_at, o) + 0.12, "boom", 0.9)]
    return draw, sfx

def Sc_phone(a, b, callout=None, mode="fit"):
    def draw(T, d, o):
        im = cam(ROOM_BLUR, T, z0=1.0); clip = load_clip(a, b)
        idx = int(T / d * len(clip)) if mode == "fit" else 0
        fr = clip[min(len(clip) - 1, idx)]; k = ease_out(T / 0.45); z = 0.98 + 0.03 * ease_out(T / d)
        ph = PHONE.copy(); ph.paste(fr, (40 + BZ, 40 + BZ), MASK); top = 330 + (1 - k) * 1500
        paste_c(im, ph, W / 2, top + ph.height * z / 2, z)
        paste_c(im, char_small(T), 190, 1650, pop(T, 0.5, 0.3))
        if callout:
            fx, fy, label, tc = callout; tc = at(tc, o); p = pop(T, tc, 0.32)
            if p > 0:
                sx = W / 2 - ph.width * z / 2 + (40 + BZ + fx * SCR_W) * z; sy = top + (40 + BZ + (fy - CROP) / (1 - CROP) * SCR_H) * z
                dr = ImageDraw.Draw(im); R = 95 * min(p, 1.2)
                dr.ellipse((sx - R * 1.3, sy - R * 0.75, sx + R * 1.3, sy + R * 0.75), outline=YEL, width=9)
                paste_c(im, pill(label, 66, fg=DARK, bg=YEL), clamp(sx + 330, 260, W - 230), sy - 160, p, rot=5)
        return im
    return draw, lambda d, o: [(0, "whoosh2", 0.8)] + ([(at(callout[3], o), "pop2", 1.2)] if callout else [])
def char_small(T):
    return PJ.draw("shock", sweat=1).resize((PJ.CW * 2 // 5, PJ.CH * 2 // 5), Image.LANCZOS)

def Sc_ambassador(l1, l2, st_at=(0, 0, 0.55)):
    def draw(T, d, o):
        im = RAYS[int(T * 12) % 36].copy(); char(im, T, "proud", y=1330, sc=1.18, glasses=True, sash=True)
        ts = at(st_at, o)
        if T >= ts:
            u = T - ts; sc = 1 + 1.0 * (1 - ease_out(u / 0.18))
            paste_c(im, stamp(l1, YEL, 92), W / 2, 640, sc, clamp(u / 0.08), rot=-6)
            paste_c(im, big(l2, 104, YEL, (110, 40, 0)), W / 2, 800, pop(u, 0.15, 0.3), rot=-6)
        return im
    return draw, lambda d, o: [(0, "shine", 0.8), (at(st_at, o) + 0.12, "boom", 0.8)]

def Sc_end():
    def draw(T, d, o):
        im = cam(ROOM_BLUR, T, z0=1.0); t2 = o[-1] - 0.15
        paste_c(im, LOGO.resize((420, 420), Image.LANCZOS), W / 2, 700, pop(T, 0.1, 0.35))
        paste_c(im, text_img("MANGA TRACKER", LG, 128, stroke=9, shadow=(0, 0, 0)), W / 2, 1020, pop(T, 0.25))
        paste_c(im, text_img("GRATIS EN PLAY STORE", LG, 86, fill=YEL, stroke=8), W / 2, 1150, pop(T, max(0.45, t2 + 0.6)))
        paste_c(im, pill("ENLACE EN MI PERFIL", 58, path=MB), W / 2, 1290, pop(T, max(0.7, t2 + 0.9)) * (1 + 0.05 * math.sin(T * 6)))
        return im
    return draw, lambda d, o: [(0.1, "boom", 0.6)]

def _shine():
    t = np.arange(int(0.9 * SR)) / SR; y = np.zeros_like(t)
    for k, f in enumerate([1760, 2217, 2637, 3520]): y += np.sin(2 * np.pi * f * t) * np.exp(-((t - k * 0.08).clip(0)) * 7) * (t > k * 0.08)
    return 0.12 * y
SFX["shine"] = _shine()

# ---------- subtítulos ARRIBA, palabra a palabra (las palabras entre *asteriscos* en amarillo) ----------
CAP_HDR = M.HDR.split("[Events]")[0].replace("Style: Title", "Style: Cap,MTBlack,94,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,1,0,1,9,5,8,60,60,300,1\nStyle: Title") + "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
def cap_groups(show):
    words = show.split(); g = []; cur = []
    for w in words:
        if cur and (len(" ".join(x.strip("*") for x in cur + [w])) > 15 or len(cur) >= 3): g.append(cur); cur = []
        cur.append(w)
        if w.rstrip("*")[-1] in ",.!?:…": g.append(cur); cur = []
    if cur: g.append(cur)
    return g

def render(name, voice, music, lines, scenes, outdir, frames=None):
    wd = os.path.join(P, "build", "s_" + name); os.makedirs(wd, exist_ok=True)
    dur = [M.tts(say, voice, f"{wd}/v{i}.wav") for i, (show, say) in enumerate(lines)]
    starts = {}; plan = []; t = 0.0
    for si, (ls, prim, extra) in enumerate(scenes):
        s0 = t; tt = t + (0.12 if si == 0 else 0.05); offs = Offs([], [dur[l] for l in ls])
        for l in ls: starts[l] = tt; offs.append(tt - s0); tt += dur[l] + GAP
        d = tt - s0 + extra; plan.append((s0, d, offs, prim)); t += d
    total = t
    if frames:
        for si, T in frames:
            s0, d, offs, prim = plan[si]; prim[0](min(T, d - 0.01), d, offs).convert("RGB").save(f"{wd}/chk_{si}_{T}.jpg", quality=85)
        return wd
    lst = []
    for si, (s0, d, offs, prim) in enumerate(plan):
        nf = int(round(d * FPS)); tmp = f"{wd}/s{si}.tmp.mp4"
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
        for i in range(nf): p.stdin.write(prim[0](i / FPS, d, offs).convert("RGB").tobytes())
        p.stdin.close()
        if p.wait() != 0: raise RuntimeError("ffmpeg escena")
        os.replace(tmp, f"{wd}/s{si}.mp4"); lst.append(f"s{si}.mp4")
    _clips.clear()
    open(f"{wd}/list.txt", "w").write("".join(f"file '{x}'\n" for x in lst))
    ev = []
    for i, (show, _) in enumerate(lines[:-1]):
        st = starts[i]; ld = dur[i]; groups = cap_groups(show); allw = [w for g in groups for w in g]
        flags = {}; on = False; idx = 0
        for g in groups:
            for x in g:
                if x.startswith("*") or x.startswith("¿*"): on = True
                flags[idx] = on; idx += 1
                if x.rstrip(",.!?:…").endswith("*"): on = False
        tot = sum(M.weight(x.replace("*", "")) for x in allw); c = st; idx = 0
        for gi, g in enumerate(groups):
            gt = []
            for x in g: dw = ld * M.weight(x.replace("*", "")) / tot; gt.append((c, c + dw, x, flags[idx])); c += dw; idx += 1
            end_g = gt[-1][1] + (GAP if gi == len(groups) - 1 else 0)
            for k in range(len(gt)):
                ws = gt[k][0]; we = gt[k + 1][0] if k + 1 < len(gt) else end_g
                parts = [("{\\c&H004DE1FF&}" + y.replace("*", "").upper() + "{\\c&H00FFFFFF&}") if hl else y.replace("*", "").upper() for (_, _, y, hl) in gt[:k + 1]]
                pre = "{\\fscx112\\fscy112\\t(0,90,\\fscx100\\fscy100)}" if k == 0 else ""
                ev.append(f"Dialogue: 1,{M.ts(ws)},{M.ts(we)},Cap,,0,0,0,,{pre}{' '.join(parts)}")
    open(f"{wd}/s.ass", "w").write(CAP_HDR + "\n".join(ev) + "\n")
    N = int(total * SR) + SR; vo = np.zeros(N); fx = np.zeros(N)
    def add(buf, a, t_, g=1.0):
        i = int(max(0, t_) * SR); seg = a[:max(0, N - i)]; buf[i:i + len(seg)] += g * seg
    for i in range(len(lines)):
        a, sr = sf.read(f"{wd}/v{i}.wav")
        if sr != SR: a = np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a)
        add(vo, a, starts[i])
    for si, (s0, d, offs, prim) in enumerate(plan):
        if si > 0: add(fx, SFX["whoosh"], s0 - 0.18, 0.8)
        for t_, kind, g in prim[1](d, offs): add(fx, SFX[kind], s0 + t_, g)
    sf.write(f"{wd}/vo.wav", vo, SR); sf.write(f"{wd}/fx.wav", fx, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{wd}/list.txt", "-c", "copy", f"{wd}/allv.mp4"], check=True)
    fc = (f"[0:v]subtitles={wd}/s.ass:fontsdir={P}/fonts[v];[1:a]asplit[vo][sc];"
          f"[3:a]atrim=0:{total},afade=t=in:d=0.3,afade=t=out:st={total - 1.3}:d=1.3,volume=0.28[mu];"
          f"[mu][sc]sidechaincompress=threshold=0.02:ratio=5:attack=15:release=350[mud];"
          f"[vo][mud][2:a]amix=inputs=3:normalize=0,atrim=0:{total},loudnorm=I=-14:TP=-1.5:LRA=9,volume=2.2dB,alimiter=limit=0.85[au]")
    os.makedirs(outdir, exist_ok=True); out = f"{outdir}/{name}.mp4"; tmp = f"{outdir}/{name}.tmp.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{wd}/allv.mp4", "-i", f"{wd}/vo.wav", "-i", f"{wd}/fx.wav", "-stream_loop", "-1", "-i", f"{P}/music/{music}.wav",
                    "-filter_complex", fc, "-map", "[v]", "-map", "[au]", "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out); return out, total
