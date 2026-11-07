# Motor de vídeos "gancho + promo indirecta" (Manga Tracker)
import os, sys, json, math, random, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
P = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ROOT = os.path.dirname(P)
# grabación de la que salen las escenas del móvil (cada lote la fija con SRC_VIDEO antes de importar)
SRC = os.environ.setdefault("SRC_VIDEO", os.path.join(ROOT, "procesadas", "grabacion_2026-11-02.mp4"))
sys.path.insert(0, P)
import make_video as M
M.SUBS += [("One Piece", "Uan Pis"), ("Bleach", "Blich"), ("shonen", "chónen"), ("shojo", "chóyo"), ("seinen", "séinen"),
           ("josei", "yósei"), ("webtoon", "uebtun"), ("spoilearon", "espoilearon"), ("spoiler", "espóiler")]
W, H, FPS = 1080, 1920, 30
LG = f"{P}/fonts/LuckiestGuy.ttf"; MB = f"{P}/fonts/Montserrat-Black.ttf"
YEL = (255, 225, 77); PUR = (123, 63, 228); WHITE = (255, 255, 255); RED = (230, 50, 80); GREEN = (40, 200, 130)
DARK = (20, 10, 40); SH_P = (60, 20, 140); SH_Y = (120, 40, 10); SH_R = (120, 10, 40)
GAP = 0.22

# ---------- utilidades de dibujo ----------
_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]
_tc = {}
def text_img(txt, path=LG, size=100, fill=WHITE, stroke=0, sfill=(0, 0, 0), shadow=None):
    k = (txt, path, size, fill, stroke, sfill, shadow)
    if k in _tc: return _tc[k]
    f = font(path, size); bb = f.getbbox(txt, stroke_width=stroke)
    pad = 30; w = bb[2] - bb[0] + pad * 2; h = bb[3] - bb[1] + pad * 2
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if shadow: d.text((pad - bb[0] + 8, pad - bb[1] + 10), txt, font=f, fill=shadow, stroke_width=stroke, stroke_fill=shadow)
    d.text((pad - bb[0], pad - bb[1]), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)
    _tc[k] = im; return im
def fit_text(txt, maxw, size, **kw):
    while size > 30:
        im = text_img(txt, size=size, **kw)
        if im.width - 60 <= maxw: return im
        size -= 6
    return text_img(txt, size=size, **kw)
def paste_c(base, im, cx, cy, scale=1.0, alpha=1.0, rot=0):
    if scale <= 0.01 or alpha <= 0.01: return
    if abs(scale - 1) > 0.005:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot: im = im.rotate(rot, resample=Image.BILINEAR, expand=True)
    if alpha < 0.999:
        a = im.getchannel("A").point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def back_out(x, s=1.9):
    x = clamp(x); x -= 1; return x * x * ((s + 1) * x + s) + 1
def pop(t, t0, d=0.28): return back_out((t - t0) / d) if t >= t0 else 0
_pc = {}
def pill(txt, size, fg=WHITE, bg=PUR, padx=34, pady=18, path=LG):
    k = (txt, size, fg, bg, path)
    if k in _pc: return _pc[k]
    ti = text_img(txt, path, size, fill=fg); w = ti.width - 60 + padx * 2; h = ti.height - 60 + pady * 2
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=bg)
    im.alpha_composite(ti, (padx - 30, pady - 30)); _pc[k] = im; return im
def big(txt, size=110, col=WHITE, sh=SH_P, maxw=980):
    return fit_text(txt, maxw, size, fill=col, stroke=max(6, size // 12), shadow=sh)

# ---------- fondos ----------
yy, xx = np.mgrid[0:H + 200, 0:W + 200].astype(np.float32)
def make_bg(c1, c2):
    r = np.sqrt(((xx - (W + 200) / 2) / 900) ** 2 + ((yy - (H + 200) * 0.42) / 1300) ** 2)
    r = np.clip(r, 0, 1)[..., None]
    return Image.fromarray((np.array(c1) * (1 - r) + np.array(c2) * r).astype(np.uint8), "RGB")
BGS = {"p": make_bg((58, 22, 120), (10, 6, 24)), "r": make_bg((90, 18, 48), (12, 4, 12)),
       "b": make_bg((20, 50, 120), (4, 8, 24)), "g": make_bg((14, 80, 70), (4, 14, 14))}
random.seed(7)
PART = [(random.uniform(0, W), random.uniform(0, H), random.uniform(2, 7), random.uniform(20, 70), random.uniform(0.2, 1)) for _ in range(70)]
def background(T, bg="p"):
    ox = 100 + 60 * math.sin(T * 0.35); oy = 100 + 70 * math.cos(T * 0.27)
    im = BGS[bg].crop((int(ox), int(oy), int(ox) + W, int(oy) + H)).convert("RGBA")
    d = ImageDraw.Draw(im)
    for (x, y, r, sp, b) in PART:
        py = (y - sp * T) % H; px = x + 18 * math.sin(T * 0.8 + y)
        c = int(90 + 120 * b); d.ellipse((px - r, py - r, px + r, py + r), fill=(c, int(c * 0.75), 255, int(90 + 120 * b)))
    return im
def glitch(im):
    a = np.array(im); a[..., 0] = np.roll(a[..., 0], 14, axis=1); a[..., 2] = np.roll(a[..., 2], -14, axis=1); return Image.fromarray(a)

# ---------- móvil ----------
SCR_W, SCR_H = 560, 1170; BZ = 22; CROP = 0.055
_clips = {}
def load_clip(a, b):
    if (a, b) in _clips: return _clips[(a, b)]
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{a}", "-t", f"{b - a}", "-i", SRC, "-vf",
           f"fps=30,crop=iw:ih*{1 - CROP}:0:ih*{CROP},scale={SCR_W}:{SCR_H}:flags=lanczos", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout; fs = SCR_W * SCR_H * 3
    _clips[(a, b)] = [Image.frombuffer("RGB", (SCR_W, SCR_H), raw[i * fs:(i + 1) * fs]) for i in range(len(raw) // fs)]
    return _clips[(a, b)]
def _phone():
    w, h = SCR_W + BZ * 2, SCR_H + BZ * 2
    im = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 50, 40 + w, 50 + h), radius=78, fill=(0, 0, 0, 150))
    im = im.filter(ImageFilter.GaussianBlur(22)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 40, 40 + w, 40 + h), radius=78, fill=(18, 14, 30), outline=(150, 110, 255), width=4)
    return im
PHONE = _phone()
MASK = Image.new("L", (SCR_W, SCR_H), 0); ImageDraw.Draw(MASK).rounded_rectangle((0, 0, SCR_W - 1, SCR_H - 1), radius=58, fill=255)
LOGO = Image.open(f"{P}/logo.png").convert("RGBA"); LOGO120 = LOGO.resize((120, 120), Image.LANCZOS); LOGO420 = LOGO.resize((420, 420), Image.LANCZOS)
PH_TOP = 230
def header(im, p=1.0):
    ti = text_img("MANGA TRACKER", LG, 76, stroke=7, shadow=SH_P); w = 120 + 20 + ti.width - 60
    paste_c(im, LOGO120, W / 2 - w / 2 + 60, 130, p); paste_c(im, ti, W / 2 - w / 2 + 140 + ti.width / 2 - 30, 130, p)

# ---------- referencias de tiempo ----------
def at(spec, offs):
    """float = segundos desde inicio de escena; (k, dt) = inicio de la línea k de la escena + dt"""
    if isinstance(spec, tuple):
        return offs[spec[0]] + spec[1] + (offs.d[spec[0]] * spec[2] if len(spec) > 2 else 0)
    return spec
class Offs(list):
    def __init__(self, s, d): super().__init__(s); self.d = d

# ---------- primitivas de escena: devuelven (dibujar(T,d,offs), sfx(d,offs)->[(t,tipo,gain)]) ----------
def S_counter(tag, l1, l2, target, label, sub=None, sub_at=(0, 1.9), bg="p", prefix="", count_d=1.6):
    def draw(T, d, o):
        im = background(T, bg); y = 250
        if tag: paste_c(im, pill(tag, 62, fg=DARK, bg=YEL), W / 2, 250, pop(T, 0)); y = 400
        if l1: paste_c(im, big(l1, 92), W / 2, y, pop(T, 0.08))
        if l2: paste_c(im, big(l2, 92), W / 2, y + 100, pop(T, 0.16))
        k = ease_out((T - 0.2) / count_d); n = int(round(target * k)); cx, cy, R = W / 2, 960, 300
        dr = ImageDraw.Draw(im); dr.ellipse((cx - R, cy - R, cx + R, cy + R), outline=(70, 40, 130), width=34)
        if k > 0: dr.arc((cx - R, cy - R, cx + R, cy + R), -90, -90 + 360 * k, fill=YEL, width=34)
        te = 0.2 + count_d; bump = 1 + 0.12 * max(0, 1 - abs(T - te) / 0.18)
        sh = 10 * math.sin(T * 90) if te - 0.05 < T < te + 0.25 else 0
        s = prefix + f"{n:,}".replace(",", ".")
        paste_c(im, fit_text(s, 470, 380 if len(s) <= 2 else 300, fill=YEL, stroke=14, shadow=SH_Y), cx + sh, cy + 20, bump * min(1, pop(T, 0.15)))
        paste_c(im, big(label, 118), W / 2, 1360, pop(T, 0.5, 0.32))
        if sub: paste_c(im, pill(sub, 66, fg=DARK, bg=YEL), W / 2, 1500, pop(T, at(sub_at, o), 0.32))
        return im
    def sfx(d, o):
        ev = [(0, "boom", 0.9), (0.2 + count_d, "boom", 0.6)] + [(0.2 + count_d * (k / 16) ** 2, "tick", 1) for k in range(16)]
        if sub: ev.append((at(sub_at, o), "pop", 1))
        return ev
    return draw, sfx

def S_grid(n, cols, label, prefix="", bg="p", fill_d=1.9, top=600, s=None, gap=4):
    rows = math.ceil(n / cols); s = s or int((960 - (cols - 1) * gap) / cols)
    def draw(T, d, o):
        im = background(T + 6, bg); k = ease_out((T - 0.05) / fill_d); m = int(round(n * k))
        paste_c(im, fit_text(prefix + f"{m:,}".replace(",", "."), 900, 230, fill=YEL, stroke=12, shadow=SH_Y), W / 2, 330, pop(T, 0))
        paste_c(im, big(label, 104), W / 2, 500, pop(T, 0.1))
        dr = ImageDraw.Draw(im); x0 = (W - cols * (s + gap) + gap) / 2
        for i in range(rows * cols):
            r, c = divmod(i, cols); x = x0 + c * (s + gap); y = top + r * (s + gap)
            if i >= n: continue
            if i < m:
                f = i / n; col = (int(123 + 132 * f), int(63 + 162 * f), int(228 - 150 * f))
                if m - i < max(3, n // 45): col = WHITE
            else: col = (40, 28, 70)
            dr.rounded_rectangle((x, y, x + s, y + s), radius=max(2, s // 5), fill=col)
        return im
    return draw, lambda d, o: [(0.05 + fill_d * (k / 24) ** 1.6, "tick", 0.8) for k in range(24)] + [(0, "boom", 0.7)]

def _card(txt, col, sub=None, icon="+", w=860):
    h = 200 if sub else 180
    im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((26, 30, w + 26, h + 30), radius=36, fill=(0, 0, 0, 120))
    im = im.filter(ImageFilter.GaussianBlur(10)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 20, w + 20, h + 20), radius=36, fill=(30, 22, 54), outline=col, width=5)
    d.rounded_rectangle((20, 20, 60, h + 20), radius=20, fill=col)
    maxw = w - 220
    if sub:
        ti = fit_text(txt, maxw, 76); im.alpha_composite(ti, (95, int(20 + h * 0.36 - ti.height / 2)))
        si = fit_text(sub, maxw, 40, path=MB, fill=(210, 200, 240)); im.alpha_composite(si, (97, int(20 + h * 0.74 - si.height / 2)))
    else:
        ti = fit_text(txt, maxw, 78); im.alpha_composite(ti, (95, int(20 + h / 2 - ti.height / 2)))
    if icon:
        cx, cy = w - 50, 20 + h / 2
        d.ellipse((cx - 50, cy - 50, cx + 50, cy + 50), fill=col)
        ic = text_img(icon, LG, 70, fill=DARK); im.alpha_composite(ic, (int(cx - ic.width / 2), int(cy - ic.height / 2 + 4)))
    return im
def S_cards(head, items, times, bg="p", shake_at=None, head_col=PUR, spacing=None, y0=None):
    """items: (texto, color, sub, icono)"""
    ims = [_card(*it) for it in items]; n = len(ims)
    sp = spacing or (235 if n <= 4 else 200); y0 = y0 or (470 if n <= 4 else 430)
    def draw(T, d, o):
        im = background(T + 12, bg)
        if head: paste_c(im, pill(head, 64, bg=head_col), W / 2, 260, pop(T, 0))
        for i, c in enumerate(ims):
            tt = T - at(times[i], o)
            if tt < 0: continue
            sh = 6 * math.sin(T * 60) if shake_at is not None and T > at(shake_at, o) else 0
            paste_c(im, c, W / 2 + sh, y0 + i * sp - 140 * (1 - ease_out(tt / 0.3)), 1.0, clamp(tt / 0.15), rot=(i % 2 * 2 - 1) * 2 * (1 - ease_out(tt / 0.4)))
        return im
    return draw, lambda d, o: [(at(t, o) + 0.1, "pop", 1) for t in times]

def S_text(before, after=None, switch=(1, 0), bubbles=(), bg1="p", bg2="r", strike=None, y=760):
    """before/after: listas de (texto, tamaño, color). strike: índice de la línea de 'before' a tachar en el cambio"""
    def lines(im, L, t0, T, sh):
        yy_ = y
        for i, (tx, sz, col) in enumerate(L):
            paste_c(im, big(tx, sz, col, sh), W / 2, yy_, pop(T, t0 + 0.12 * i)); yy_ += sz * 1.1 + 10
    def draw(T, d, o):
        ts = at(switch, o) if after else 1e9
        if T < ts:
            im = background(T + 18, bg1); lines(im, before, 0, T, SH_P if bg1 == "p" else SH_R)
            if strike is not None and T > ts - 0.01: pass
            return im
        u = T - ts; im = background(T + 18, bg2)
        for i, (q, x, yb, r) in enumerate(bubbles):
            paste_c(im, pill(q, 62, bg=(200, 40, 70) if bg2 == "r" else PUR), x + 8 * math.sin(T * 13 + i), yb + 8 * math.cos(T * 11 + i * 2), pop(u, 0.25 + i * 0.12), rot=r)
        lines(im, after, 0, u, SH_R if bg2 == "r" else SH_P)
        return glitch(im) if u < 0.12 and bg2 == "r" else im
    def sfx(d, o):
        ev = [(0, "pop", 0.8)]
        if after: ev += [(at(switch, o), "boom", 0.6)] + [(at(switch, o) + 0.25 + i * 0.12, "pop", 0.5) for i in range(len(bubbles))]
        return ev
    return draw, sfx

def S_strike(word, wrong, right, sw=(1, 0), bg="p"):
    """WORD grande; debajo 'wrong' que se tacha y se cambia por 'right'"""
    def draw(T, d, o):
        im = background(T + 3, bg); ts = at(sw, o)
        paste_c(im, big(word, 200, YEL, SH_Y), W / 2, 700, pop(T, 0))
        if T < ts:
            paste_c(im, big("NO ES", 90), W / 2, 900, pop(T, 0.2))
            wi = big(wrong, 130); paste_c(im, wi, W / 2, 1050, pop(T, 0.35))
            k = clamp((T - 0.9) / 0.25)
            if k > 0:
                dr = ImageDraw.Draw(im); x0 = W / 2 - (wi.width - 60) / 2 - 20
                dr.line((x0, 1060, x0 + (wi.width - 20) * k, 1040), fill=RED, width=18)
        else:
            u = T - ts
            paste_c(im, big("SIGNIFICA", 90), W / 2, 900, pop(u, 0))
            paste_c(im, big(right, 130, WHITE), W / 2, 1050, pop(u, 0.15))
        return im
    return draw, lambda d, o: [(0, "boom", 0.8), (0.9, "pop", 1), (at(sw, o), "boom", 0.5)]

def S_options(q1, q2, opts, hi, hi_at=(1, 0), countdown=True, bg="p"):
    def draw(T, d, o):
        im = background(T + 9, bg)
        paste_c(im, big(q1, 96), W / 2, 300, pop(T, 0)); paste_c(im, big(q2, 96, YEL, SH_Y), W / 2, 410, pop(T, 0.1))
        th = at(hi_at, o)
        for i, tx in enumerate(opts):
            sel = T >= th and i == hi
            col = YEL if sel else (40, 30, 70)
            w, h = 860, 150; card = Image.new("RGBA", (w, h), (0, 0, 0, 0)); dr = ImageDraw.Draw(card)
            dr.rounded_rectangle((0, 0, w - 1, h - 1), radius=40, fill=col, outline=(150, 110, 255), width=4)
            dr.ellipse((25, 25, 125, 125), fill=PUR if not sel else DARK)
            L = text_img("ABCD"[i], LG, 64); card.alpha_composite(L, (int(75 - L.width / 2), int(75 - L.height / 2 + 4)))
            t2 = fit_text(tx, 650, 66, fill=DARK if sel else WHITE); card.alpha_composite(t2, (160, int(75 - t2.height / 2)))
            sc = pop(T, 0.3 + 0.12 * i) * ((1.06 + 0.03 * math.sin((T - th) * 8)) if sel else 1)
            paste_c(im, card, W / 2, 640 + i * 185, sc)
        if countdown and T < th:
            n = 3 - int(T / max(0.6, th / 3)); n = max(1, n)
            paste_c(im, pill(str(n), 90, fg=DARK, bg=YEL), W / 2, 1420, 1 + 0.15 * (1 - ((T / max(0.6, th / 3)) % 1)))
        return im
    def sfx(d, o):
        th = at(hi_at, o); step = max(0.6, th / 3)
        return [(0, "boom", 0.7)] + [(k * step, "tick", 1.4) for k in range(3) if k * step < th] + [(0.3 + 0.12 * i, "pop", 0.5) for i in range(4)] + [(th, "boom", 0.6)]
    return draw, sfx

def S_chat(msgs, title=None, bg="p"):
    """msgs: (lado 'in'/'out', texto o '...', tiempo)"""
    def bubble(tx, side):
        f = font(MB, 52); words = tx.split(); lines_ = []; cur = ""
        for w_ in words:
            if f.getlength(cur + " " + w_) > 620 and cur: lines_.append(cur); cur = w_
            else: cur = (cur + " " + w_).strip()
        lines_.append(cur)
        w = int(max(f.getlength(l) for l in lines_)) + 70; h = 70 * len(lines_) + 50
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
        dr.rounded_rectangle((0, 0, w - 1, h - 1), radius=40, fill=(245, 245, 250) if side == "in" else PUR)
        for i, l in enumerate(lines_): dr.text((35, 22 + 70 * i), l, font=f, fill=DARK if side == "in" else WHITE)
        return im
    def draw(T, d, o):
        im = background(T + 15, bg)
        if title: paste_c(im, pill(title, 60, fg=DARK, bg=YEL), W / 2, 230, pop(T, 0))
        y = 420
        for side, tx, t0 in msgs:
            t0 = at(t0, o)
            if T < t0: break
            if tx == "...":
                b = bubble("     ", side); dr = ImageDraw.Draw(b)
                for k in range(3):
                    a = 0.5 + 0.5 * math.sin(T * 9 - k * 0.9); c = int(150 + 100 * a)
                    dr.ellipse((40 + k * 50, 35, 70 + k * 50, 65), fill=(c, c, 255))
            else: b = bubble(tx, side)
            x = 80 + b.width / 2 if side == "in" else W - 80 - b.width / 2
            paste_c(im, b, x, y + b.height / 2, pop(T, t0, 0.25)); y += b.height + 40
        return im
    return draw, lambda d, o: [(at(t, o), "pop", 0.9) for _, _, t in msgs]

def S_versus(lt, rt, lsub, rsub, l_at, r_at, bg="p"):
    def draw(T, d, o):
        im = background(T + 21, bg); dr = ImageDraw.Draw(im)
        dr.rectangle((0, 0, W / 2 - 4, H), fill=(20, 60, 50, 140)); dr.rectangle((W / 2 + 4, 0, W, H), fill=(70, 15, 35, 140))
        paste_c(im, big(lt, 110, WHITE, (10, 60, 40)), W / 4, 520, pop(T, 0.05))
        paste_c(im, big(rt, 110, WHITE, (90, 10, 30)), 3 * W / 4, 520, pop(T, 0.15))
        paste_c(im, pill("VS", 90, fg=DARK, bg=YEL), W / 2, 820, pop(T, 0.3) * (1 + 0.05 * math.sin(T * 6)))
        for side, subs, t0, cx, col in ((0, lsub, l_at, W / 4, GREEN), (1, rsub, r_at, 3 * W / 4, RED)):
            t0 = at(t0, o)
            for i, s in enumerate(subs):
                paste_c(im, fit_text(s, 470, 76, fill=col if i == 0 else WHITE, stroke=7, shadow=(0, 0, 0)), cx, 1050 + i * 100, pop(T, t0 + 0.12 * i))
        return im
    return draw, lambda d, o: [(0, "boom", 0.7), (at(l_at, o), "pop", 1), (at(r_at, o), "pop", 1)]

def S_quad(head, items, times, bg="p"):
    """2x2 bloques: (texto, color)"""
    def draw(T, d, o):
        im = background(T + 27, bg)
        if head: paste_c(im, pill(head, 62), W / 2, 270, pop(T, 0))
        for i, (tx, col) in enumerate(items):
            r, c = divmod(i, 2); cx = W / 2 + (c - 0.5) * 470; cy = 640 + r * 470
            t0 = at(times[i], o); p = pop(T, t0, 0.3)
            if p <= 0: continue
            b = Image.new("RGBA", (430, 430), (0, 0, 0, 0)); dr = ImageDraw.Draw(b)
            dr.rounded_rectangle((0, 0, 429, 429), radius=60, fill=col)
            ti = fit_text(tx, 380, 84, stroke=6, shadow=(0, 0, 0)); b.alpha_composite(ti, (int(215 - ti.width / 2), int(215 - ti.height / 2)))
            paste_c(im, b, cx, cy, p, rot=4 * math.sin(T * 2 + i))
        return im
    return draw, lambda d, o: [(at(t, o), "pop", 1) for t in times]

def S_phone(a, b, mode="fit", rate=1.0, callout=None, slide=False, bg="p", zoom=0.04):
    """mode: fit (todo el clip en la escena), play (a velocidad rate), callout=(fx, fy, texto, tiempo)"""
    def draw(T, d, o):
        im = background(T + 30, bg); clip = load_clip(a, b)
        header(im, pop(T, 0.05) if slide else 1)
        if mode == "fit": idx = int(T / d * len(clip))
        else: idx = int(T * 30 * rate)
        fr = clip[min(len(clip) - 1, idx)]
        k = ease_out(T / 0.45) if slide else 1
        z = (0.94 + 0.06 * k) * (1 + zoom * ease_out(T / d)); top = PH_TOP + (1 - k) * 1500 - 20 * zoom * ease_out(T / d) / 0.04
        ph = PHONE.copy(); ph.paste(fr, (40 + BZ, 40 + BZ), MASK)
        paste_c(im, ph, W / 2, top + ph.height * z / 2, z)
        if callout:
            fx, fy, label, tc = callout; tc = at(tc, o); p = pop(T, tc, 0.32)
            if p > 0:
                sx = W / 2 - ph.width * z / 2 + (40 + BZ + fx * SCR_W) * z
                sy = top + (40 + BZ + (fy - CROP) / (1 - CROP) * SCR_H) * z
                dr = ImageDraw.Draw(im); R = 95 * min(p, 1.2)
                dr.ellipse((sx - R * 1.3, sy - R * 0.75, sx + R * 1.3, sy + R * 0.75), outline=YEL, width=9)
                lx = clamp(sx + (300 if sx < W / 2 + 60 else -300), 260, W - 260)
                paste_c(im, pill(label, 66, fg=DARK, bg=YEL), lx, sy - 170, p, rot=5)
        return im
    def sfx(d, o):
        ev = [(0, "whoosh2", 0.8)] if slide else []
        if callout: ev.append((at(callout[3], o), "pop2", 1.2))
        return ev
    return draw, sfx

def S_countdown(head, n=3, step=None, bg="p"):
    """cuenta atrás grande n..1 con anillo que se vacía"""
    def draw(T, d, o):
        st = step or min(1.0, (d - 0.3) / n)
        im = background(T + 33, bg)
        if head: paste_c(im, big(head, 96), W / 2, 330, pop(T, 0))
        k = int(T / st); cx, cy, R = W / 2, 960, 320
        dr = ImageDraw.Draw(im); dr.ellipse((cx - R, cy - R, cx + R, cy + R), outline=(70, 40, 130), width=34)
        if k < n:
            f = (T % st) / st; dr.arc((cx - R, cy - R, cx + R, cy + R), -90 + 360 * f, 270, fill=YEL, width=34)
            paste_c(im, text_img(str(n - k), LG, 420, fill=YEL, stroke=14, shadow=SH_Y), cx, cy + 20, 1 + 0.25 * (1 - ease_out(f / 0.25)))
        else:
            paste_c(im, big("¡YA!", 260, YEL, SH_Y), cx, cy, pop(T, n * st))
        return im
    def sfx(d, o):
        st = step or min(1.0, (d - 0.3) / n)
        return [(k * st, "tick", 2) for k in range(n)] + [(n * st, "boom", 0.7)]
    return draw, sfx

def S_end(q1, q2):
    def draw(T, d, o):
        im = background(T + 42); a = np.array(im.convert("RGB")).astype(np.float32) * 0.85
        im = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
        paste_c(im, big(q1, 100), W / 2, 230, pop(T, 0.0)); paste_c(im, big(q2, 100, YEL), W / 2, 345, pop(T, 0.12))
        t2 = o[-1] - 0.15
        paste_c(im, LOGO420, W / 2, 760, pop(T, 0.3, 0.35))
        paste_c(im, text_img("MANGA TRACKER", LG, 128, stroke=9, shadow=(0, 0, 0)), W / 2, 1080, pop(T, t2))
        paste_c(im, text_img("GRATIS EN PLAY STORE", LG, 86, fill=YEL, stroke=8), W / 2, 1210, pop(T, t2 + 0.25))
        paste_c(im, pill("ENLACE EN MI PERFIL", 58, path=MB), W / 2, 1350, pop(T, t2 + 0.5) * (1 + 0.05 * math.sin(max(0, T - t2 - 0.5) * 6)))
        return im
    return draw, lambda d, o: [(o[-1] - 0.15, "boom", 0.6)]

# ---------- sonido ----------
SR = 44100; rng = np.random.default_rng(3)
def _whoosh(d=0.38, f1=300, f2=5000):
    n = int(d * SR); x = rng.standard_normal(n); t = np.linspace(0, 1, n)
    f = np.exp(np.log(f1) + (np.log(f2) - np.log(f1)) * t); y = np.zeros(n); lp = 0
    for k in range(n):
        a_ = min(1, 2 * np.pi * f[k] / SR); lp += a_ * (x[k] - lp); y[k] = lp
    return 0.5 * y * np.sin(np.pi * t) ** 2 / (np.abs(y).max() + 1e-9)
def _boom(d=0.9):
    t = np.arange(int(d * SR)) / SR; f = 90 * np.exp(-t * 4) + 38
    return 0.9 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5)
def _pop(d=0.09, f0=900):
    t = np.arange(int(d * SR)) / SR; return 0.35 * np.sin(2 * np.pi * (f0 + 1600 * t / d) * t) * np.exp(-t * 40)
def _tick():
    t = np.arange(int(0.03 * SR)) / SR; return 0.18 * np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 180)
SFX = {"whoosh": _whoosh(), "whoosh2": _whoosh(0.5, 200, 3000), "boom": _boom(), "pop": _pop(), "pop2": _pop(0.12, 600), "tick": _tick()}

# ---------- render de un vídeo ----------
def render(name, voice, music, lines, scenes, outdir, frames=None, wdir=None):
    """lines: [(texto_pantalla, texto_voz)]; scenes: [([índices de línea], (draw, sfx), cola_extra)]"""
    wd = os.path.join(wdir or os.path.join(P, "build"), "g_" + name); os.makedirs(wd, exist_ok=True)
    dur = []
    for i, (show, say) in enumerate(lines):
        fn = f"{wd}/v{i}.wav"
        dur.append(M.tts(say, voice, fn))
    starts = {}; plan = []; t = 0.0
    for si, (ls, prim, extra) in enumerate(scenes):
        s0 = t; tt = t + (0.12 if si == 0 else 0.05); offs = Offs([], [dur[l] for l in ls])
        for l in ls: starts[l] = tt; offs.append(tt - s0); tt += dur[l] + GAP
        d = tt - s0 + extra; plan.append((s0, d, offs, prim)); t += d
    total = t
    if frames:  # comprobación rápida: [(escena, T)]
        for si, T in frames:
            s0, d, offs, prim = plan[si]; prim[0](T, d, offs).convert("RGB").save(f"{wd}/chk_{si}_{T}.jpg", quality=85)
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
    # subtítulos karaoke (sin la última línea, que va con el cierre)
    hdr = M.HDR.replace("Style: Sub,MTBlack,112", "Style: Sub,MTBlack,100").replace(",2,40,40,600,1\nStyle: Title", ",2,40,40,250,1\nStyle: Title")
    ev = []
    for i, (show, _) in enumerate(lines[:-1]):
        st = starts[i]; ld = dur[i]; groups = M.word_groups(show); allw = [w for g in groups for w in g]
        tot = sum(M.weight(x) for x in allw); c = st
        for g in groups:
            gt = []
            for x in g: dw = ld * M.weight(x) / tot; gt.append((c, c + dw, x)); c += dw
            for k, (ws, we, x) in enumerate(gt):
                parts = [("{\\c&H004DE1FF&\\t(0,90,\\fscx116\\fscy116)\\t(90,180,\\fscx108\\fscy108)}" + y.upper() + "{\\c&H00FFFFFF&\\fscx100\\fscy100}") if j == k else y.upper() for j, (_, _, y) in enumerate(gt)]
                ev.append(f"Dialogue: 1,{M.ts(ws)},{M.ts(we)},Sub,,0,0,0,,{' '.join(parts)}")
    open(f"{wd}/s.ass", "w").write(hdr + "\n".join(ev) + "\n")
    N = int(total * SR) + SR; vo = np.zeros(N); fx = np.zeros(N)
    def add(buf, a, t_, g=1.0):
        i = int(max(0, t_) * SR); seg = a[:max(0, N - i)]; buf[i:i + len(seg)] += g * seg
    for i in range(len(lines)):
        a, sr = sf.read(f"{wd}/v{i}.wav")
        if sr != SR: a = np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a)
        add(vo, a, starts[i])
    for si, (s0, d, offs, prim) in enumerate(plan):
        if si > 0: add(fx, SFX["whoosh"], s0 - 0.18)
        for t_, kind, g in prim[1](d, offs): add(fx, SFX[kind], s0 + t_, g)
    sf.write(f"{wd}/vo.wav", vo, SR); sf.write(f"{wd}/fx.wav", fx, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{wd}/list.txt", "-c", "copy", f"{wd}/allv.mp4"], check=True)
    fc = (f"[0:v]subtitles={wd}/s.ass:fontsdir={P}/fonts[v];[1:a]asplit[vo][sc];"
          f"[3:a]atrim=0:{total},afade=t=in:d=0.3,afade=t=out:st={total - 1.3}:d=1.3,volume=0.30[mu];"
          f"[mu][sc]sidechaincompress=threshold=0.02:ratio=5:attack=15:release=350[mud];"
          f"[vo][mud][2:a]amix=inputs=3:normalize=0,atrim=0:{total},loudnorm=I=-14:TP=-1.5:LRA=9,volume=2.2dB,alimiter=limit=0.85[au]")
    out = f"{outdir}/{name}.mp4"; tmp = f"{outdir}/{name}.tmp.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{wd}/allv.mp4", "-i", f"{wd}/vo.wav", "-i", f"{wd}/fx.wav", "-stream_loop", "-1", "-i", f"{P}/music/{music}.wav",
                    "-filter_complex", fc, "-map", "[v]", "-map", "[au]", "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out); return out, total
