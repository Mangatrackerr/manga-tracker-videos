# Kit de escenas "todo animado" (13/11/2026): el chico de cuerpo entero (monigote2) actúa cada frase.
# Una escena = A(fondo, pista de poses, props, fx). Tiempos: float (s desde el inicio de la escena) o (k, dt, f) = línea k + dt + f·duración.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from engine_satira import *
import engine_satira as ES, iconos as IC, monigote2 as MO
INK_ = (22, 16, 30)
q = lambda k, f=0.0: (k, 0, f)
def tt(spec, o): return at(spec, o) if spec is not None else None

# ---------- fondos ----------
def _street():
    im = Image.fromarray(np.concatenate([np.linspace([18, 20, 60], [60, 40, 110], 1300)[:, None, :].repeat(W, 1), np.full((620, W, 3), (34, 30, 48))], 0).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(im); rnd = random.Random(5)
    for _ in range(60):
        x, y = rnd.uniform(0, W), rnd.uniform(0, 700); d.ellipse((x, y, x + 3, y + 3), fill=(255, 255, 255))
    d.ellipse((760, 170, 900, 310), fill=(255, 245, 210)); x = -20
    while x < W:
        bw = rnd.randint(120, 220); bh = rnd.randint(380, 760); d.rectangle((x, 1300 - bh, x + bw, 1300), fill=(28 + rnd.randint(0, 14), 24, 56))
        for yy in range(1300 - bh + 30, 1280, 56):
            for xx in range(x + 18, x + bw - 30, 42):
                if rnd.random() < 0.4: d.rectangle((xx, yy, xx + 20, yy + 30), fill=(255, 200, 110))
        x += bw + 6
    d.rectangle((0, 1300, W, 1360), fill=(70, 66, 84))
    for k in range(5): d.rectangle((k * 240, 1600, k * 240 + 130, 1622), fill=(230, 220, 120))
    return im
def _room():
    im = cam(ROOM, 0.0, z0=1.0).copy(); d = ImageDraw.Draw(im)
    d.rectangle((0, 1560, W, H), fill=(70, 48, 40)); d.rectangle((0, 1560, W, 1580), fill=(95, 66, 52)); return im
def _stage():
    im = Image.fromarray(np.linspace([40, 8, 18], [10, 2, 6], H)[:, None, :].repeat(W, 1).astype(np.uint8)).convert("RGBA"); d = ImageDraw.Draw(im)
    for k in range(9):  # telón
        x = k * 130 - 20; d.rectangle((x, 0, x + 90, 1500), fill=(150, 20, 40)); d.rectangle((x + 90, 0, x + 130, 1500), fill=(110, 12, 30))
    d.rectangle((0, 0, W, 120), fill=(120, 14, 34)); d.rectangle((0, 1500, W, H), fill=(60, 36, 30)); d.rectangle((0, 1500, W, 1530), fill=(200, 160, 60))
    sp = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sp); sd.polygon([(440, 0), (640, 0), (900, 1700), (180, 1700)], fill=(255, 240, 200, 70))
    im.alpha_composite(sp.filter(ImageFilter.GaussianBlur(30))); return im
def _bedroom():
    im = Image.fromarray(np.linspace([16, 14, 40], [8, 6, 20], H)[:, None, :].repeat(W, 1).astype(np.uint8)).convert("RGBA"); d = ImageDraw.Draw(im)
    d.rounded_rectangle((120, 300, 520, 760), radius=14, fill=(40, 46, 100)); d.ellipse((380, 360, 470, 450), fill=(255, 245, 210))
    for x, y in [(170, 360), (250, 500), (330, 420), (200, 640), (450, 600)]: d.ellipse((x, y, x + 4, y + 4), fill=WHITE)
    d.line((320, 300, 320, 760), fill=(60, 50, 90), width=12); d.line((120, 530, 520, 530), fill=(60, 50, 90), width=12)
    d.rectangle((0, 1560, W, H), fill=(44, 34, 40)); return im
BGS_ = {}
def bg(name, T):
    if name.startswith("rays:"): return rays(name[5:], T)
    if name == "blur": return cam(ROOM_BLUR, T, z0=1.0)
    if name not in BGS_: BGS_[name] = {"street": _street, "room": _room, "stage": _stage, "bedroom": _bedroom}[name]()
    return BGS_[name].copy()

# ---------- props ----------
def crt(im, T, mode="anime", rays_k=0.0, label=None, x0=80, y0=1010):
    d = ImageDraw.Draw(im); x1, y1 = x0 + 420, y0 + 380
    d.rounded_rectangle((x0 - 20, y0 + 370, x1 + 20, y0 + 590), radius=16, fill=(110, 76, 56))
    d.rounded_rectangle((x0, y0, x1, y1), radius=40, fill=(70, 66, 80)); d.rounded_rectangle((x0 + 30, y0 + 30, x1 - 90, y1 - 40), radius=30, fill=(20, 26, 50))
    for k in range(3): d.ellipse((x1 - 66, y0 + 70 + k * 70, x1 - 30, y0 + 106 + k * 70), fill=(40, 38, 50))
    d.line((x0 + 130, y0, x0 + 60, y0 - 90), fill=(160, 160, 180), width=8); d.line((x0 + 200, y0, x0 + 290, y0 - 100), fill=(160, 160, 180), width=8)
    sx0, sy0, sx1, sy1 = x0 + 40, y0 + 40, x1 - 100, y1 - 50
    if mode == "anime":
        for k in range(5):
            cx = sx0 + (sx1 - sx0) * (0.5 + 0.35 * math.sin(T * 1.3 + k * 1.7)); cy = sy0 + (sy1 - sy0) * (0.5 + 0.3 * math.cos(T * 1.1 + k))
            d.ellipse((cx - 28, cy - 28, cx + 28, cy + 28), fill=[(255, 120, 160), (120, 200, 255), (255, 220, 90), (140, 255, 170), (200, 140, 255)][k])
    if label: t = text_img(label, LG, 64, fill=YEL, stroke=5); im.alpha_composite(t, (int((sx0 + sx1) / 2 - t.width / 2), int((sy0 + sy1) / 2 - t.height / 2)))
def calendar(im, x, y, txt, flip=0.0, sc=1.0):
    d = ImageDraw.Draw(im); w, h = 240 * sc, 260 * sc
    d.rounded_rectangle((x - w / 2, y - h / 2, x + w / 2, y + h / 2), radius=18, fill=(250, 250, 245)); d.rounded_rectangle((x - w / 2, y - h / 2, x + w / 2, y - h / 2 + 66 * sc), radius=18, fill=RED)
    paste_c(im, fit_text(txt, w - 30, int(84 * sc), fill=INK_), x, y + 28 * sc)
    if flip > 0:
        k = min(1, flip); top = y - h / 2 + 66 * sc
        d.polygon([(x - w / 2, top), (x + w / 2, top), (x + w / 2, top + (h - 66 * sc) * (1 - k)), (x - w / 2, top + (h - 66 * sc) * (1 - k) * 0.7)], fill=(225, 225, 220))
def sofa(im, y=1340):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, y, 990, y + 380), radius=60, fill=(200, 70, 90)); d.rounded_rectangle((40, y + 120, 220, y + 420), radius=50, fill=(175, 55, 75)); d.rounded_rectangle((860, y + 120, 1040, y + 420), radius=50, fill=(175, 55, 75))
    d.rounded_rectangle((150, y + 220, 930, y + 380), radius=40, fill=(220, 90, 110))
def desk(im, y=1430):
    d = ImageDraw.Draw(im); d.rounded_rectangle((120, y, 960, y + 50), radius=12, fill=(150, 104, 70)); d.rectangle((160, y + 50, 200, 1900), fill=(120, 80, 54)); d.rectangle((880, y + 50, 920, 1900), fill=(120, 80, 54))
    d.polygon([(560, y), (820, y), (790, y - 30), (590, y - 30)], fill=(250, 250, 245))
def bed(im, y=1450):
    d = ImageDraw.Draw(im); d.rounded_rectangle((60, y - 120, 140, 1880), radius=20, fill=(120, 80, 60)); d.rounded_rectangle((60, y, 1020, y + 260), radius=40, fill=(90, 110, 200)); d.rounded_rectangle((60, y + 200, 1020, y + 330), radius=30, fill=(120, 80, 60))
    d.rounded_rectangle((90, y - 40, 330, y + 60), radius=40, fill=(245, 245, 250))
def books(im, x, y, n, sc=1.0):
    d = ImageDraw.Draw(im); cols = [(230, 70, 90), (90, 160, 255), (255, 190, 60), (130, 90, 230), (60, 200, 150), (250, 120, 60)]
    for k in range(n):
        yy = y - k * 26 * sc; xo = 6 * math.sin(k * 1.7) * sc
        d.rounded_rectangle((x - 110 * sc + xo, yy - 24 * sc, x + 110 * sc + xo, yy), radius=int(5 * sc), fill=cols[k % 6]); d.rectangle((x - 100 * sc + xo, yy - 16 * sc, x + 100 * sc + xo, yy - 10 * sc), fill=(255, 255, 255))
def casa():
    im = Image.new("RGBA", (640, 640), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(320, 60), (600, 300), (40, 300)], fill=(230, 80, 80)); d.rectangle((100, 290, 540, 600), fill=(250, 235, 210))
    d.rectangle((270, 420, 370, 600), fill=(150, 100, 70)); d.rectangle((140, 350, 230, 440), fill=(140, 200, 255)); d.rectangle((410, 350, 500, 440), fill=(140, 200, 255))
    d.rectangle((440, 110, 500, 220), fill=(120, 60, 60)); return im
def star(d, x, y, r, col=YEL):
    pts = [(x + (r if k % 2 == 0 else r * 0.45) * math.cos(-math.pi / 2 + k * math.pi / 5), y + (r if k % 2 == 0 else r * 0.45) * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)]
    d.polygon(pts, fill=col)
def heart(d, x, y, r, col=(240, 70, 110)):
    d.ellipse((x - r, y - r * 0.6, x, y + r * 0.4), fill=col); d.ellipse((x, y - r * 0.6, x + r, y + r * 0.4), fill=col); d.polygon([(x - r, y), (x + r, y), (x, y + r * 1.1)], fill=col)
def note(d, x, y, col=WHITE):
    d.ellipse((x - 22, y + 20, x + 10, y + 44), fill=col); d.line((x + 8, y + 32, x + 8, y - 40), fill=col, width=7); d.line((x + 8, y - 40, x + 40, y - 26), fill=col, width=9)
def bulb(d, x, y):
    d.ellipse((x - 46, y - 60, x + 46, y + 30), fill=(255, 230, 90)); d.rectangle((x - 22, y + 24, x + 22, y + 56), fill=(170, 170, 190))
    for k in range(8):
        a = k * math.pi / 4; d.line((x + 70 * math.cos(a), y - 15 + 70 * math.sin(a), x + 95 * math.cos(a), y - 15 + 95 * math.sin(a)), fill=(255, 230, 90), width=8)

# ---------- personaje ----------
def put(im, T, o, track, cx=W / 2, foot=1830, sc=1.0, dx=0, dy=0, wave=False, run=False):
    pose, expr, hands, extra = track.at(T, lambda s_: at(s_, o)); pose = dict(pose)
    pose["y"] = pose.get("y", 0) + 4 * math.sin(T * 2.6)
    if wave: pose["rhx"] = pose.get("rhx", 95) + 35 * math.sin(T * 9)
    if run:
        ph = math.sin(T * 22); pose.update(lfx=-80 * ph, rfx=80 * ph, lhx=-120 * ph, rhx=110 * ph); dy -= abs(math.sin(T * 11)) * 30
    blink = (T % 3.3) > 3.18 and expr not in ("dizzy", "cry", "wink", "happy")
    c = MO.draw(pose, expr, hands, blink=blink, **extra)
    if sc != 1.0: c = c.resize((int(c.width * sc), int(c.height * sc)), Image.BILINEAR)
    x0 = cx + dx - MO.HX * sc; y0 = foot + dy - MO.FOOT_Y * sc
    im.alpha_composite(c, (int(x0), int(y0)))
    return (cx + dx + pose.get("x", 0) * sc, y0 + (MO.HY + pose.get("y", 0) - 348) * sc)

def K(t, pose, expr="neutral", hands=("fist", "fist"), **extra):
    """keyframe cómodo: pose = nombre de MO.P o dict (se puede sumar: ('sit', dict(...)))"""
    if isinstance(pose, str): pose = MO.P[pose]
    elif isinstance(pose, tuple): pose = dict(MO.P[pose[0]], **pose[1])
    return (t, pose, expr, hands, extra)

# ---------- escena genérica ----------
def A(bgname, keys, props=(), fx=(), cx=W / 2, foot=1830, sc=1.0, run_until=None, xmove=None, wave=False, zoom=None):
    """props: dicts con 'k' (tipo) y 't' (aparición). fx: efectos alrededor de la cabeza."""
    tr = MO.Track(keys)
    def draw(T, d, o):
        im = bg(bgname, T); dr = ImageDraw.Draw(im)
        late = []
        for p in props:
            t0 = tt(p.get("t", 0.0), o); t1 = tt(p.get("t_out"), o)
            if T < t0 or (t1 is not None and T >= t1): continue
            u = T - t0; k = p["k"]
            if k == "sofa": sofa(im)
            elif k == "desk": desk(im)
            elif k == "bed": bed(im)
            elif k == "tv": crt(im, T, p.get("mode", "anime"), label=p.get("label"))
            elif k == "calendar":
                seq = p["seq"]; dur = max(0.3, tt(p.get("t_end", (0, 0, 0.9)), o) - t0) if len(seq) > 1 else 1
                kk = min(len(seq) - 1, u / dur * (len(seq) - 1)); i = int(kk)
                calendar(im, p.get("x", W / 2), p.get("y", 700), seq[i], flip=max(0.0, ((kk - i) - 0.75) / 0.25) if len(seq) > 1 and i < len(seq) - 1 else 0, sc=p.get("s", 1.0))  # se mantiene y pasa la hoja al final
            elif k == "books":
                n = int(round(p["n"] * ease_out(u / p.get("dur", 1.2)))); books(im, p.get("x", W / 2), p.get("y", 1500), n, p.get("s", 1.0))
            elif k == "clock":
                cx_, cy_, R = p.get("x", W / 2), p.get("y", 700), p.get("r", 160); dr.ellipse((cx_ - R, cy_ - R, cx_ + R, cy_ + R), fill=(250, 248, 235), outline=RED, width=16)
                a = T * p.get("speed", 9); dr.line((cx_, cy_, cx_ + R * 0.7 * math.sin(a), cy_ - R * 0.7 * math.cos(a)), fill=INK_, width=11); dr.line((cx_, cy_, cx_ + R * 0.45 * math.sin(a / 12), cy_ - R * 0.45 * math.cos(a / 12)), fill=INK_, width=15)
            elif k == "icon":
                an = p.get("anim", "pop"); x, y, s = p.get("x", W / 2), p.get("y", 760), p.get("s", 0.8); rot = 0
                if an == "slide_r": x = x + (1 - ease_out(u / 0.5)) * 900
                if an == "slide_l": x = x - (1 - ease_out(u / 0.5)) * 900
                if an == "rise": y = y + (1 - ease_out(u / 0.6)) * 600
                sc_ = s * (pop(T, t0, 0.3) if an == "pop" else 1); y += 10 * math.sin(T * 2.4 + x); rot = 3 * math.sin(T * 2)
                late.append(lambda im_, img=p["img"], x=x, y=y, sc_=sc_, rot=rot: paste_c(im_, img, x, y, sc_, rot=rot))
            elif k == "big":
                late.append(lambda im_, p=p, t0=t0: paste_c(im_, big(p["txt"], p.get("size", 120), p.get("col", YEL), (110, 40, 0) if p.get("col", YEL) == YEL else (0, 0, 0)), W / 2, p.get("y", 640), pop(T, t0, 0.25), rot=p.get("rot", 0)))
            elif k == "pill":
                late.append(lambda im_, p=p, t0=t0: paste_c(im_, pill(p["txt"], p.get("size", 64), fg=DARK, bg=p.get("bg", YEL)), p.get("x", W / 2), p.get("y", 640), pop(T, t0, 0.3), rot=p.get("rot", -3)))
            elif k == "counter":
                n = p["a"] + (p["b"] - p["a"]) * ease_out(u / p.get("dur", 1.2)); fmt = p.get("fmt", "{:,.0f}")
                s_ = p.get("pre", "") + fmt.format(n).replace(",", ".") + p.get("suf", "")
                late.append(lambda im_, s_=s_, p=p, t0=t0: paste_c(im_, big(s_, p.get("size", 160), YEL, (110, 40, 0)), W / 2, p.get("y", 620), pop(T, t0, 0.25)))
            elif k == "stamp":
                late.append(lambda im_, p=p, u=u: paste_c(im_, stamp(p["txt"], p.get("col", RED), p.get("size", 110), p.get("sub")), p.get("x", W / 2), p.get("y", 820), 1 + 1.2 * (1 - ease_out(u / 0.18)), clamp(u / 0.08), rot=p.get("rot", -8)))
            elif k == "rain":
                rnd = random.Random(p.get("seed", 1)); kind = p.get("kind", "confetti")
                def _r(im_, u=u, rnd=rnd, kind=kind):
                    d_ = ImageDraw.Draw(im_)
                    for j in range(40):
                        x = rnd.uniform(0, W); sp = rnd.uniform(500, 900); y = (rnd.uniform(-600, 0) + sp * u) % (H + 200) - 100; a = u * 4 + j
                        if kind == "money":
                            pts = [(x + 60 * math.cos(a) - 30 * math.sin(a) * 0.4, y + 60 * math.sin(a) * 0.3), (x - 60 * math.cos(a), y - 60 * math.sin(a) * 0.3), (x - 60 * math.cos(a), y - 60 * math.sin(a) * 0.3 + 34), (x + 60 * math.cos(a), y + 60 * math.sin(a) * 0.3 + 34)]
                            d_.polygon(pts, fill=(90, 190, 110)); d_.ellipse((x - 10, y + 4, x + 10, y + 26), fill=(60, 140, 80))
                        elif kind == "cards":
                            d_.rounded_rectangle((x - 40, y - 56, x + 40, y + 56), radius=10, fill=[(230, 70, 90), (90, 160, 255), (255, 190, 60), (130, 90, 230), (60, 200, 150)][j % 5])
                        else:
                            d_.rectangle((x, y, x + 18, y + 30), fill=[(255, 90, 120), (90, 200, 255), (255, 220, 70), (140, 255, 160)][j % 4])
                late.append(_r)
            elif k == "phone_tiles":
                late.append(lambda im_, u=u: [paste_c(im_, TILES[j % len(TILES)], W / 2 + 380 * math.cos(u * 1.2 + j * 0.8), 1050 + 300 * math.sin(u * 1.2 + j * 0.8), 0.9, rot=10 * math.sin(u * 3 + j)) for j in range(8)])
            elif k == "grid":
                n = p["n"]; cols = p.get("cols", 11); m = int(round(n * ease_out(u / p.get("dur", 1.4)))); s = 64; g = 10; x0 = W / 2 - (cols * (s + g) - g) / 2; y0 = p.get("y", 760)
                for j in range(n):
                    r, c = divmod(j, cols); dr.rounded_rectangle((x0 + c * (s + g), y0 + r * (s + g), x0 + c * (s + g) + s, y0 + r * (s + g) + s), radius=12, fill=(GREEN if j < m else (60, 50, 90)))
            elif k == "timer":
                n = min(p.get("b", 90), p.get("b", 90) * ease_out(u / p.get("dur", 1.6))); mm, ss = divmod(int(n), 60)
                late.append(lambda im_, s_=f"{mm}:{ss:02d}", p=p, t0=t0: paste_c(im_, big(s_, 230, YEL, (110, 40, 0)), W / 2, p.get("y", 680), pop(T, t0, 0.25)))
        hp = put(im, T, o, tr, cx=cx + (xmove(T) if xmove else 0), foot=foot, sc=sc, wave=wave, run=(run_until is not None and T < run_until))
        for f in fx:
            t0 = tt(f.get("t", 0.0), o); t1 = tt(f.get("t_out"), o)
            if T < t0 or (t1 is not None and T >= t1): continue
            u = T - t0; k = f["k"]; dr = ImageDraw.Draw(im)
            if k == "qmarks":
                for j, ddx in enumerate((-220, 0, 220)):
                    if u > j * 0.18: paste_c(im, big("?", 150, YEL, (110, 40, 0)), hp[0] + ddx, hp[1] - 270 - 20 * math.sin(T * 4 + j), pop(T, t0 + j * 0.18, 0.25), rot=10 * math.sin(T * 3 + j))
            elif k == "stars":
                for j in range(5): a = T * 3 + j * 2 * math.pi / 5; star(dr, hp[0] + 190 * math.cos(a), hp[1] - 160 + 50 * math.sin(a), 26)
            elif k == "hearts":
                for j in range(4): heart(dr, hp[0] - 200 + j * 130, hp[1] - 220 - ((u * 160 + j * 60) % 260), 34)
            elif k == "notes":
                for j in range(4): note(dr, hp[0] - 260 + j * 170, hp[1] - 200 - ((u * 180 + j * 70) % 300) + 20 * math.sin(T * 5 + j))
            elif k == "zzz":
                for j in range(3): paste_c(im, big("Z", 70 + 25 * j, WHITE), hp[0] + 160 + j * 60, hp[1] - 200 - j * 80 - (u * 40) % 40, pop(T, t0 + j * 0.2, 0.3))
            elif k == "bulb": bulb(dr, hp[0], hp[1] - 300 + 6 * math.sin(T * 4))
            elif k == "sparkle":
                rnd = random.Random(int(T * 6))
                for j in range(6): star(dr, hp[0] + rnd.uniform(-300, 300), hp[1] + rnd.uniform(-300, 200), rnd.uniform(10, 22), (255, 245, 200))
        for fn in late: fn(im)
        if zoom is not None:
            zt = tt(zoom, o)
            if T > zt:
                k = ease_out((T - zt) / 0.4); z = 1 + 0.22 * k; w_, h_ = int(W / z), int(H / z); cy_ = min(H - h_ / 2, max(h_ / 2, hp[1] + 150))
                im = im.crop((int(W / 2 - w_ / 2), int(cy_ - h_ / 2), int(W / 2 + w_ / 2), int(cy_ + h_ / 2))).resize((W, H), Image.BILINEAR)
        return im
    def sfx(d, o):
        ev = [(0, "pop", 0.5)]
        for p in props:
            t0 = tt(p.get("t", 0.0), o)
            if p["k"] in ("stamp",): ev.append((t0 + 0.12, "boom", 0.9))
            elif p["k"] in ("big", "pill", "icon"): ev.append((t0, "pop", 0.7))
            elif p["k"] in ("counter", "timer", "grid", "books"): ev += [(t0 + p.get("dur", 1.2) * (j / 12) ** 1.5, "tick", 1) for j in range(12)]
            elif p["k"] == "rain": ev.append((t0, "shine", 0.8))
            elif p["k"] == "calendar" and len(p["seq"]) > 1: ev += [(t0 + j * 0.3, "whoosh", 0.4) for j in range(len(p["seq"]) - 1)]
        for f in fx:
            if f["k"] == "qmarks": ev += [(tt(f.get("t", 0.0), o) + j * 0.18, "pop", 0.7) for j in range(3)]
            elif f["k"] in ("bulb", "sparkle"): ev.append((tt(f.get("t", 0.0), o), "shine", 0.7))
        return ev
    return draw, sfx

# ---------- escenas finales comunes ----------
def A_app(a, b, callout=None, mode="fit", pose_end="point_r"):
    tr = MO.Track([K(0.0, "present", "proud", ("fist", "open")), K(q(0, 0.5), pose_end, "wink", ("fist", "point"))])
    def draw(T, d, o):
        im = cam(ROOM_BLUR, T, z0=1.0); clip = load_clip(a, b)
        fr = clip[min(len(clip) - 1, int(T / d * len(clip)))] if mode == "fit" else clip[0]; k = ease_out(T / 0.45); z = 0.9
        ph = PHONE.copy(); ph.paste(fr, (40 + BZ, 40 + BZ), MASK); top = 470 + (1 - k) * 1500; px = W / 2 + 150
        paste_c(im, ph, px, top + ph.height * z / 2, z)
        if callout:
            fx_, fy_, label, tc = callout; tc = at(tc, o); p = pop(T, tc, 0.32)
            if p > 0:
                sx = px - ph.width * z / 2 + (40 + BZ + fx_ * SCR_W) * z; sy = top + (40 + BZ + (fy_ - CROP) / (1 - CROP) * SCR_H) * z
                dr = ImageDraw.Draw(im); R = 95 * min(p, 1.2); dr.ellipse((sx - R * 1.3, sy - R * 0.75, sx + R * 1.3, sy + R * 0.75), outline=YEL, width=9)
                paste_c(im, pill(label, 62, fg=DARK, bg=YEL), clamp(sx + 60, 260, W - 230), sy + 150 if sy < 1500 else sy - 150, p, rot=5)
        put(im, T, o, tr, cx=200, sc=0.62, foot=1900)
        return im
    return draw, lambda d, o: [(0, "whoosh2", 0.8)] + ([(at(callout[3], o), "pop2", 1.2)] if callout else [])
def A_send(pal="purple"):
    tr = MO.Track([K(0.0, "wave", "wink", ("fist", "open")), K(q(0, 0.45), "point_up_r", "proud", ("fist", "point"))])
    def draw(T, d, o):
        im = rays(pal, T); hp = put(im, T, o, tr, cx=W / 2 - 80); t0 = at(q(0, 0.45), o)
        if T > t0:
            u = min(1, (T - t0) / 1.2); dr = ImageDraw.Draw(im)
            pts = [(hp[0] + 200 + 600 * v, hp[1] + 60 - 700 * v + 120 * math.sin(v * 6)) for v in np.linspace(0, u, 30)]
            for a_, b_ in zip(pts[::2], pts[1::2]): dr.line((a_, b_), fill=(255, 255, 255), width=6)
            x, y = pts[-1]; dr.polygon([(x + 60, y - 30), (x - 50, y - 10), (x - 10, y + 30)], fill=WHITE); dr.polygon([(x + 60, y - 30), (x - 10, y + 30), (x - 5, y)], fill=(200, 200, 220))
        paste_c(im, big("MÁNDASELO", 130, YEL, (110, 40, 0)), W / 2, 640, pop(T, 0.15, 0.3), rot=-4)
        return im
    return draw, lambda d, o: [(0, "pop", 0.7), (at(q(0, 0.45), o), "whoosh2", 0.9)]
def A_fin():
    tr = MO.Track([K(0.0, "wave", "proud", ("fist", "open"))])
    def draw(T, d, o):
        im = cam(ROOM_BLUR, T, z0=1.0)
        paste_c(im, LOGO.resize((360, 360), Image.LANCZOS), W / 2, 560, pop(T, 0.1, 0.35))
        paste_c(im, text_img("MANGA TRACKER", LG, 120, stroke=9, shadow=(0, 0, 0)), W / 2, 830, pop(T, 0.25))
        paste_c(im, text_img("GRATIS EN PLAY STORE", LG, 82, fill=YEL, stroke=8), W / 2, 950, pop(T, 0.5))
        paste_c(im, pill("ENLACE EN MI PERFIL", 56, path=MB), W / 2, 1075, pop(T, 0.75) * (1 + 0.05 * math.sin(T * 6)))
        put(im, T, o, tr, cx=W / 2, sc=0.62, foot=1900, wave=True)
        return im
    return draw, lambda d, o: [(0.1, "boom", 0.6)]
