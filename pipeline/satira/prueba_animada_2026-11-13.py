# PROTOTIPO "todo animado" (13/11/2026): el chico de cuerpo entero representa cada frase. Tema: 685 niños al hospital. Voz chico 1.
# Uso: python3 pipeline/satira/prueba_animada_2026-11-13.py [chk]
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["SRC_VIDEO"] = os.path.abspath(os.path.join(HERE, "..", "..", "procesadas", "grabacion_2026-11-02.mp4"))
sys.path.insert(0, HERE)
import numpy as np
from engine_satira import *
import engine_satira as ES, iconos as IC, voz_viva, monigote2 as MO
from PIL import Image, ImageDraw, ImageFilter
voz_viva.patch(M)
ES.VOICE_CHAIN = "highpass=f=75,equalizer=f=3000:t=q:w=1.4:g=1.2,acompressor=threshold=0.15:ratio=2:attack=10:release=150,"
ES.MUSIC_VOL = 0.2
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "videos"))
NAME = "2026-11-13c_685_ninos_animado_chico"
q = lambda k, f=0.0: (k, 0, f)
FOOT = 1830  # altura de los pies del muñeco

# ---------- utilidades ----------
def put(im, T, o, track, cx=W / 2, foot=FOOT, sc=1.0, dx=0, dy=0, bob=True, **kw):
    pose, expr, hands, extra = track.at(T, lambda s_: at(s_, o))
    pose = dict(pose)
    if bob: pose["y"] = pose.get("y", 0) + 4 * math.sin(T * 2.6)
    blink = (T % 3.3) > 3.18 and expr not in ("dizzy", "cry", "wink")
    c = MO.draw(pose, expr, hands, blink=blink, **{**extra, **kw})
    if sc != 1.0: c = c.resize((int(c.width * sc), int(c.height * sc)), Image.BILINEAR)
    x0 = cx + dx - MO.HX * sc; y0 = foot + dy - MO.FOOT_Y * sc
    im.alpha_composite(c, (int(x0), int(y0)))
    # posición aproximada de la cabeza (para estrellas, interrogaciones…)
    return (cx + dx + pose.get("x", 0) * sc, y0 + (MO.HY + pose.get("y", 0) - 348) * sc)

def star(d, x, y, r, col=YEL):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    d.polygon(pts, fill=col)

def label(im, txt, y, t, T, size=110, col=YEL):
    paste_c(im, big(txt, size, col, (110, 40, 0) if col == YEL else (0, 0, 0)), W / 2, y, pop(T, t, 0.25))

# ---------- fondos ----------
def _street():
    im = Image.fromarray(np.concatenate([np.linspace([18, 20, 60], [60, 40, 110], 1300)[:, None, :].repeat(W, 1),
                                         np.full((620, W, 3), (34, 30, 48))], 0).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(im); rnd = random.Random(5)
    for _ in range(60):
        x, y = rnd.uniform(0, W), rnd.uniform(0, 700); d.ellipse((x, y, x + 3, y + 3), fill=(255, 255, 255))
    d.ellipse((760, 170, 900, 310), fill=(255, 245, 210))
    x = -20
    while x < W:
        bw = rnd.randint(120, 220); bh = rnd.randint(380, 760); col = (28 + rnd.randint(0, 14), 24, 56)
        d.rectangle((x, 1300 - bh, x + bw, 1300), fill=col)
        for yy in range(1300 - bh + 30, 1280, 56):
            for xx in range(x + 18, x + bw - 30, 42):
                if rnd.random() < 0.4: d.rectangle((xx, yy, xx + 20, yy + 30), fill=(255, 200, 110))
        x += bw + 6
    d.rectangle((0, 1300, W, 1360), fill=(70, 66, 84))  # acera
    return im
STREET = _street()
def street(T, scroll=0):
    im = STREET.copy(); d = ImageDraw.Draw(im)
    off = (scroll * T * 900) % 240
    for k in range(-1, 6):
        x = k * 240 - off; d.rectangle((x, 1600, x + 130, 1622), fill=(230, 220, 120))
    return im

def _room_tv():
    im = cam(ROOM, 0.0, z0=1.0).copy(); d = ImageDraw.Draw(im)
    d.rectangle((0, 1560, W, H), fill=(70, 48, 40)); d.rectangle((0, 1560, W, 1580), fill=(95, 66, 52))  # suelo
    d.rounded_rectangle((60, 1380, 520, 1600), radius=16, fill=(110, 76, 56))  # mueble
    return im
ROOM_TV = _room_tv()
def crt(im, T, mode="anime", rays=0.0):
    """tele de tubo sobre el mueble; mode: anime | off"""
    d = ImageDraw.Draw(im); x0, y0, x1, y1 = 80, 1010, 500, 1390
    d.rounded_rectangle((x0, y0, x1, y1), radius=40, fill=(70, 66, 80)); d.rounded_rectangle((x0 + 30, y0 + 30, x1 - 90, y1 - 40), radius=30, fill=(20, 26, 50))
    for k in range(3): d.ellipse((x1 - 66, y0 + 70 + k * 70, x1 - 30, y0 + 106 + k * 70), fill=(40, 38, 50))
    d.line((x0 + 130, y0, x0 + 60, y0 - 90), fill=(160, 160, 180), width=8); d.line((x0 + 200, y0, x0 + 290, y0 - 100), fill=(160, 160, 180), width=8)
    sx0, sy0, sx1, sy1 = x0 + 40, y0 + 40, x1 - 100, y1 - 50
    if mode == "anime":  # dibujos abstractos que se mueven (sin destellos)
        for k in range(5):
            cx = sx0 + (sx1 - sx0) * (0.5 + 0.35 * math.sin(T * 1.3 + k * 1.7)); cy = sy0 + (sy1 - sy0) * (0.5 + 0.3 * math.cos(T * 1.1 + k))
            col = [(255, 120, 160), (120, 200, 255), (255, 220, 90), (140, 255, 170), (200, 140, 255)][k]
            d.ellipse((cx - 28, cy - 28, cx + 28, cy + 28), fill=col)
    else:
        txt = text_img("SIN EMISIÓN", MB, 34, fill=(200, 200, 220)); im.alpha_composite(txt, (int((sx0 + sx1) / 2 - txt.width / 2), int((sy0 + sy1) / 2 - txt.height / 2)))
    if rays > 0:  # rayos de colores girando despacio (no parpadea)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov); cx, cy = (sx0 + sx1) / 2, (sy0 + sy1) / 2
        for k in range(12):
            a = T * 0.8 + k * math.pi / 6; col = [(255, 90, 120), (90, 160, 255)][k % 2]
            od.polygon([(cx, cy), (cx + 1500 * math.cos(a - 0.06), cy + 1500 * math.sin(a - 0.06)), (cx + 1500 * math.cos(a + 0.06), cy + 1500 * math.sin(a + 0.06))], fill=col + (int(70 * rays),))
        im.alpha_composite(ov)

def calendar(im, x, y, txt, flip=0.0, sc=1.0):
    d = ImageDraw.Draw(im); w, h = 220 * sc, 240 * sc
    d.rounded_rectangle((x - w / 2, y - h / 2, x + w / 2, y + h / 2), radius=18, fill=(250, 250, 245)); d.rounded_rectangle((x - w / 2, y - h / 2, x + w / 2, y - h / 2 + 64 * sc), radius=18, fill=RED)
    paste_c(im, text_img(txt, LG, int(76 * sc), fill=INK_), x, y + 26 * sc)
    if flip > 0:  # hoja que se levanta
        k = min(1, flip); d.polygon([(x - w / 2, y - h / 2 + 64 * sc), (x + w / 2, y - h / 2 + 64 * sc), (x + w / 2, y - h / 2 + 64 * sc + (h - 64 * sc) * (1 - k)), (x - w / 2, y - h / 2 + 64 * sc + (h - 64 * sc) * (1 - k) * 0.7)], fill=(225, 225, 220))
INK_ = (22, 16, 30)

def sofa(im):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 1340, 990, 1720), radius=60, fill=(200, 70, 90)); d.rounded_rectangle((40, 1460, 220, 1760), radius=50, fill=(175, 55, 75)); d.rounded_rectangle((860, 1460, 1040, 1760), radius=50, fill=(175, 55, 75))
    d.rounded_rectangle((150, 1560, 930, 1720), radius=40, fill=(220, 90, 110))

def kid(d, x, y, t, hair, shirt, sway):
    a = 0.25 * math.sin(t * 3 + sway); hx = x + 30 * math.sin(a);
    d.rounded_rectangle((x - 34, y + 20, x + 34, y + 110), radius=18, fill=shirt)
    d.ellipse((hx - 42, y - 64, hx + 42, y + 22), fill=PJ_SK); d.chord((hx - 46, y - 74, hx + 46, y + 4), 180, 360, fill=hair)
    for ex_ in (-16, 16):
        pts = [(hx + ex_ + (1 + 1.6 * a2) * math.cos(a2 + t * 4), y - 22 + (1 + 1.6 * a2) * math.sin(a2 + t * 4)) for a2 in [k * 0.35 for k in range(26)]]
        d.line(pts, fill=INK_, width=3)
    d.arc((hx - 14, y - 4, hx + 14, y + 12), 200, 340, fill=INK_, width=3)
PJ_SK = MO.SK

# ---------- escenas ----------
def S_ambulance():
    amb = IC.ambulancia()
    tr = MO.Track([(0.0, dict(MO.P["run"], x=700), "neutral", ("fist", "fist")), (0.55, dict(MO.P["run"], x=40), "neutral", ("fist", "fist")),
                   (0.85, MO.P["shock"], "shock", ("open", "open")), (q(0, 0.75), MO.P["point_l"], "shock", ("point", "fist"))])
    def draw(T, d, o):
        im = street(T, scroll=max(0, 1 - T / 0.8)); k = ease_out(T / 0.8)
        ax = -420 + (420 + 330) * k; ay = 1430 + 8 * math.sin(T * 30) * (1 - k)
        paste_c(im, amb, ax, ay, 0.95)
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl); a = 0.5 + 0.2 * math.sin(T * 6)
        gd.ellipse((ax - 160, ay - 420, ax + 140, ay - 120), fill=(255, 60, 70, int(80 * a))); im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(40)))
        run = T < 0.55
        if run:
            ph_ = math.sin(T * 22); tr.keys[0][1].update(lfx=-80 * ph_, rfx=80 * ph_, lhx=-120 * ph_, rhx=110 * ph_); tr.keys[1][1].update(lfx=-80 * ph_, rfx=80 * ph_, lhx=-120 * ph_, rhx=110 * ph_)
        put(im, T, o, tr, cx=800, dy=(-abs(math.sin(T * 18)) * 30 if run else 0))
        if T > 0.85:
            tc = 0.85; n = int(round(685 * ease_out((T - tc) / 1.1)))
            paste_c(im, big(f"{n} NIÑOS", 150, YEL, (110, 40, 0)), W / 2, 640, pop(T, tc, 0.25))
            paste_c(im, big("AL HOSPITAL", 100), W / 2, 790, pop(T, tc + 0.15, 0.25))
        return im
    return draw, lambda d, o: [(0, "siren", 0.9), (0.85, "boom", 0.9)] + [(0.85 + 1.1 * (k / 12) ** 1.5, "tick", 1) for k in range(12)]

def S_night():
    tr = MO.Track([(0.0, MO.P["shock"], "shock", ("open", "open")), (q(0, 0.4), MO.P["arms_up"], "shock", ("open", "open"))])
    def draw(T, d, o):
        im = street(T); dr = ImageDraw.Draw(im); cx, cy, R = W / 2, 620, 170
        dr.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(250, 248, 235), outline=RED, width=18)
        a = T * 9; dr.line((cx, cy, cx + 120 * math.sin(a), cy - 120 * math.cos(a)), fill=INK_, width=12); dr.line((cx, cy, cx + 80 * math.sin(a / 12), cy - 80 * math.cos(a / 12)), fill=INK_, width=16)
        paste_c(im, big("EN UNA NOCHE", 110, YEL, (110, 40, 0)), W / 2, 870, pop(T, 0.1, 0.25))
        put(im, T, o, tr, cx=W / 2, dy=-abs(math.sin(T * 9)) * 18)
        return im
    return draw, lambda d, o: [(0, "pop", 0.8)] + [(k * 0.25, "tick", 1.2) for k in range(int(d / 0.25))]

def S_tv(mode="watch"):
    """watch: ve la tele feliz; flash: rayos y se marea"""
    if mode == "watch":
        tr = MO.Track([(0.0, MO.P["sit"], "neutral", ("fist", "fist"), {"look": (-1, 0)}), (q(0, 0.5), MO.P["sit_happy"], "proud", ("open", "fist"), {"look": (-1, 0)})])
    else:
        tr = MO.Track([(0.0, MO.P["sit"], "shock", ("fist", "fist")), (q(0, 0.35), MO.P["sit_dizzy"], "dizzy", ("open", "open"))])
    def draw(T, d, o):
        im = ROOM_TV.copy(); calendar(im, 860, 640, "1997")
        crt(im, T, "anime", rays=(ease_out((T - at(q(0, 0.3), o)) / 0.5) if mode == "flash" and T > at(q(0, 0.3), o) else 0))
        hp = put(im, T, o, tr, cx=800, dx=(10 * math.sin(T * 2) if mode == "flash" else 0))
        if mode == "flash" and T > at(q(0, 0.4), o):
            dr = ImageDraw.Draw(im)
            for k in range(5):
                a = T * 3 + k * 2 * math.pi / 5; star(dr, hp[0] + 190 * math.cos(a), hp[1] - 150 + 50 * math.sin(a), 26)
        if mode == "watch": paste_c(im, pill("JAPÓN · 1997", 64, fg=DARK, bg=YEL), W / 2, 820, pop(T, 0.1, 0.3))
        return im
    return draw, lambda d, o: ([(0, "pop", 0.8)] if mode == "watch" else [(at(q(0, 0.3), o), "boom", 0.7), (at(q(0, 0.4), o), "shine", 0.8)])

def S_building():
    def draw(T, d, o):
        im = street(T); dr = ImageDraw.Draw(im)
        dr.rectangle((90, 860, 990, 1560), fill=(70, 60, 110)); rnd = random.Random(3)
        for r in range(3):
            for c in range(3):
                x0 = 150 + c * 290; y0 = 920 + r * 210; t0 = 0.15 + (r * 3 + c) * 0.08
                dr.rectangle((x0, y0, x0 + 200, y0 + 170), fill=(255, 210, 120) if T > t0 else (40, 34, 70))
                if T > t0:
                    hair = rnd.choice([(40, 30, 40), (120, 70, 30), (230, 160, 60), (30, 30, 60)]); shirt = rnd.choice([(230, 70, 90), (90, 160, 255), (60, 190, 140), (255, 170, 40)])
                    kid(dr, x0 + 100, y0 + 90, T, hair, shirt, r * 3 + c)
        tc = 0.1; n = int(round(12000 * ease_out((T - tc) / 1.3)))
        paste_c(im, big(f"+{n:,}".replace(",", "."), 170, YEL, (110, 40, 0)), W / 2, 590, pop(T, tc, 0.25))
        paste_c(im, big("CON SÍNTOMAS", 100), W / 2, 750, pop(T, tc + 0.2, 0.25))
        return im
    return draw, lambda d, o: [(0, "boom", 0.7)] + [(0.15 + k * 0.08, "pop", 0.5) for k in range(9)] + [(0.1 + 1.3 * (k / 12) ** 1.5, "tick", 1) for k in range(12)]

def S_hiatus():
    tr = MO.Track([(0.0, MO.P["sit"], "confused", ("fist", "fist")), (q(0, 0.3), MO.P["sit_wait"], "confused", ("fist", "fist"))])
    months = ["DIC", "ENE", "FEB", "MAR", "ABR"]
    def draw(T, d, o):
        im = ROOM_TV.copy(); crt(im, T, "off")
        t0 = at(q(0, 0.15), o); dur = max(0.3, d - t0 - 0.6); k = (T - t0) / dur * 4
        i = int(max(0, min(4, k))); calendar(im, 860, 640, months[i], flip=(k - i) if 0 < k < 4 else 0)
        put(im, T, o, tr, cx=800, dy=0)
        if k >= 4: paste_c(im, stamp("4 MESES", RED, 110, "SIN SERIE"), W / 2, 860, 1 + 1.2 * (1 - ease_out((T - t0 - dur) / 0.18)), rot=-8)
        return im
    return draw, lambda d, o: [(at(q(0, 0.15), o) + j * max(0.3, d - at(q(0, 0.15), o) - 0.6) / 4, "whoosh", 0.6) for j in range(4)] + [(d - 0.45, "boom", 0.8)]

def S_sofa(beat):
    if beat == "relax":
        tr = MO.Track([(0.0, MO.P["sit_phone"], "smug", ("fist", "fist"), {"phone": "r"}), (q(0, 0.75), MO.P["sit_phone"], "neutral", ("fist", "fist"), {"phone": "r"})])
    else:
        tr = MO.Track([(0.0, dict(MO.P["sit"], rhx=-10, rhy=-215, head=6), "confused", ("fist", "fist")), (q(1, 0.0), dict(MO.P["fall"], y=40), "shock", ("open", "open"))])
    def draw(T, d, o):
        im = cam(ROOM, T, z0=1.0); sofa(im)
        zoom = beat == "relax" and T > at(q(0, 0.6), o)
        hp = put(im, T, o, tr, cx=W / 2, foot=1700)
        if beat == "lost":
            dr = ImageDraw.Draw(im)
            for k, (dx_, t_) in enumerate([(-230, 0.15), (0, 0.35), (230, 0.55)]):
                tt = at(q(0, t_), o)
                if T > tt and T < at(q(1), o): paste_c(im, big("?", 150, YEL, (110, 40, 0)), hp[0] + dx_, hp[1] - 260 - 20 * math.sin(T * 4 + k), pop(T, tt, 0.25), rot=10 * math.sin(T * 3 + k))
            if T >= at(q(1), o):
                u = T - at(q(1), o); paste_c(im, stamp("NI IDEA", RED, 130), W / 2, 760, 1 + 1.3 * (1 - ease_out(u / 0.18)), clamp(u / 0.08), rot=-8)
        if zoom:  # zoom dramático a la cara
            k = ease_out((T - at(q(0, 0.6), o)) / 0.4); z = 1 + 0.25 * k
            w_, h_ = int(W / z), int(H / z); cx_, cy_ = W / 2, 1150
            im = im.crop((int(cx_ - w_ / 2), int(cy_ - h_ / 2), int(cx_ + w_ / 2), int(cy_ + h_ / 2))).resize((W, H), Image.BILINEAR)
        return im
    if beat == "relax": return draw, lambda d, o: [(0, "pop", 0.6), (at(q(0, 0.6), o), "boom", 0.5)]
    return draw, lambda d, o: [(at(q(0, t_), o), "pop", 0.8) for t_ in (0.15, 0.35, 0.55)] + [(at(q(1), o) + 0.1, "boom", 1.0)]

def S_app():
    tr = MO.Track([(0.0, MO.P["present"], "proud", ("fist", "open")), (q(0, 0.5), MO.P["point_r"], "wink", ("fist", "point"))])
    def draw(T, d, o):
        im = cam(ROOM_BLUR, T, z0=1.0); clip = load_clip(62.0, 66.0)
        fr = clip[min(len(clip) - 1, int(T / d * len(clip)))]; k = ease_out(T / 0.45); z = 0.9
        ph = PHONE.copy(); ph.paste(fr, (40 + BZ, 40 + BZ), MASK); top = 470 + (1 - k) * 1500
        px = W / 2 + 150; paste_c(im, ph, px, top + ph.height * z / 2, z)
        tc = at(q(0, 0.55), o); p = pop(T, tc, 0.32)
        if p > 0:
            sx = px - ph.width * z / 2 + (40 + BZ + 0.25 * SCR_W) * z; sy = top + (40 + BZ + (0.455 - CROP) / (1 - CROP) * SCR_H) * z
            dr = ImageDraw.Draw(im); R = 95 * min(p, 1.2); dr.ellipse((sx - R * 1.3, sy - R * 0.75, sx + R * 1.3, sy + R * 0.75), outline=YEL, width=9)
            paste_c(im, pill("EPISODIO 7", 66, fg=DARK, bg=YEL), sx + 120, sy + 150, p, rot=5)
        put(im, T, o, tr, cx=200, sc=0.62, foot=1900)
        return im
    return draw, lambda d, o: [(0, "whoosh2", 0.8), (at(q(0, 0.55), o), "pop2", 1.2)]

def S_send():
    tr = MO.Track([(0.0, MO.P["wave"], "wink", ("fist", "open")), (q(0, 0.45), MO.P["point_up_r"], "proud", ("fist", "point"))])
    def draw(T, d, o):
        im = rays("purple", T); hp = put(im, T, o, tr, cx=W / 2 - 80)
        t0 = at(q(0, 0.45), o)
        if T > t0:  # avión de papel con estela
            u = min(1, (T - t0) / 1.2); dr = ImageDraw.Draw(im)
            pts = [(hp[0] + 200 + 600 * v, hp[1] + 60 - 700 * v + 120 * math.sin(v * 6)) for v in np.linspace(0, u, 30)]
            for a, b in zip(pts[::2], pts[1::2]): dr.line((a, b), fill=(255, 255, 255, 180), width=6)
            x, y = pts[-1]; dr.polygon([(x + 60, y - 30), (x - 50, y - 10), (x - 10, y + 30)], fill=WHITE); dr.polygon([(x + 60, y - 30), (x - 10, y + 30), (x - 5, y)], fill=(200, 200, 220))
        paste_c(im, big("MÁNDASELO", 130, YEL, (110, 40, 0)), W / 2, 640, pop(T, 0.15, 0.3), rot=-4)
        return im
    return draw, lambda d, o: [(0, "pop", 0.7), (at(q(0, 0.45), o), "whoosh2", 0.9)]

def S_fin():
    tr = MO.Track([(0.0, MO.P["wave"], "proud", ("fist", "open"))])
    def draw(T, d, o):
        im = cam(ROOM_BLUR, T, z0=1.0)
        paste_c(im, LOGO.resize((360, 360), Image.LANCZOS), W / 2, 560, pop(T, 0.1, 0.35))
        paste_c(im, text_img("MANGA TRACKER", LG, 120, stroke=9, shadow=(0, 0, 0)), W / 2, 830, pop(T, 0.25))
        paste_c(im, text_img("GRATIS EN PLAY STORE", LG, 82, fill=YEL, stroke=8), W / 2, 950, pop(T, 0.5))
        paste_c(im, pill("ENLACE EN MI PERFIL", 56, path=MB), W / 2, 1075, pop(T, 0.75) * (1 + 0.05 * math.sin(T * 6)))
        tr.keys[0][1]["rhx"] = 95 + 35 * math.sin(T * 9)  # saluda
        put(im, T, o, tr, cx=W / 2, sc=0.62, foot=1900)
        return im
    return draw, lambda d, o: [(0.1, "boom", 0.6)]

def _siren():
    t = np.arange(int(1.6 * SR)) / SR; f = np.where((t // 0.32) % 2 == 0, 760, 980)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR); y = np.sign(y) * np.abs(y) ** 0.5
    return 0.13 * y * np.minimum(1, t / 0.05) * np.minimum(1, (1.6 - t) / 0.4)
SFX["siren"] = _siren()

FIN = "Manga Tracker. ¡Gratis en Play Store!"
LINES = [
    ("¡Un episodio de anime mandó a *685 niños* al hospital!", "¡Un episodio de anime mandó a seiscientos ochenta y cinco niños al hospital!"),
    ("En *una sola noche*.", "En una sola noche."),
    ("Japón, 1997. Millones de niños viendo la tele…", "Japón, mil novecientos noventa y siete. Millones de niños viendo la tele…"),
    ("Y de repente… unos *destellos de luz* en la pantalla.", "Y de repente… unos destellos de luz en la pantalla."),
    ("¡Y otros *12.000* niños tuvieron síntomas en casa!", "¡Y otros doce mil niños tuvieron síntomas en casa!"),
    ("La serie desapareció de la tele… *4 meses*.", "La serie desapareció de la tele… cuatro meses."),
    ("Hoy, por suerte, lo más peligroso de ver anime es otra cosa…", "Hoy, por suerte, lo más peligroso de ver anime es otra cosa…"),
    ("¿Por qué capítulo iba yo?", "¿Por qué capítulo iba yo?"),
    ("¡*Ni idea*!", "¡Ni idea!"),
    ("Para eso está *Manga Tracker*: marcas el episodio, y listo.", "Para eso está Manga Tracker: marcas el episodio, y listo."),
    ("Mándaselo a ese amigo que *siempre se pierde*.", "Mándaselo a ese amigo que siempre se pierde."), (FIN, FIN)]
SCENES = [([0], S_ambulance(), 0), ([1], S_night(), 0), ([2], S_tv("watch"), 0), ([3], S_tv("flash"), 0), ([4], S_building(), 0),
          ([5], S_hiatus(), 0.5), ([6], S_sofa("relax"), 0), ([7, 8], S_sofa("lost"), 0.3), ([9], S_app(), 0), ([10], S_send(), 0), ([11], S_fin(), 1.4)]

if __name__ == "__main__":
    if "chk" in sys.argv:
        print(render(NAME, "st5", "lofi12", LINES, SCENES, OUT, frames=[(si, T) for si in range(len(SCENES)) for T in (0.3, 1.2, 2.4)]))
    else:
        print(render(NAME, "st5", "lofi12", LINES, SCENES, OUT))
