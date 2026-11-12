# Música lo-fi original y tranquila (sin copyright: se sintetiza aquí desde cero).
# Uso: python3 pipeline/satira/lofi.py  → crea pipeline/music/lofi1..lofi6.wav (-17 LUFS aprox.)
import os, subprocess, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__)); OUTD = os.path.join(HERE, "..", "music")
def mf(n): return 440 * 2 ** ((n - 69) / 12)
def lp(x, f): return sosfilt(butter(2, f, "lp", fs=SR, output="sos"), x)
def hp(x, f): return sosfilt(butter(2, f, "hp", fs=SR, output="sos"), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], "bp", fs=SR, output="sos"), x)

def ep(f, d, vel=1.0):  # piano eléctrico suave
    t = np.arange(int(d * SR)) / SR; env = np.minimum(1, t / 0.012) * np.exp(-t * 2.2)
    y = sum((1 / h ** 1.7) * np.sin(2 * np.pi * h * f * t + 0.3 * h) for h in range(1, 6))
    y += 0.25 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 9)                       # "campana" del ataque
    y *= 1 + 0.12 * np.sin(2 * np.pi * 4.5 * t)                                      # trémolo
    return vel * env * y
def pad(f, d):
    t = np.arange(int(d * SR)) / SR; env = np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.6)
    y = sum(np.sin(2 * np.pi * f * (1 + dt) * t) for dt in (-0.004, 0, 0.004)) / 3
    return env * lp(y + 0.3 * np.sin(2 * np.pi * 2 * f * t), 1800)
def kalimba(f, d=1.2):
    t = np.arange(int(d * SR)) / SR
    return (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 5.4 * f * t) * np.exp(-t * 18)) * np.exp(-t * 5) * np.minimum(1, t / 0.004)
def marimba(f, d=0.9):
    t = np.arange(int(d * SR)) / SR
    return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t * 30)) * np.exp(-t * 7) * np.minimum(1, t / 0.003)
def pluck(f, d=1.4):  # guitarra suave (Karplus-Strong)
    n = int(d * SR); p = int(SR / f); buf = np.random.default_rng(int(f)).uniform(-1, 1, p); y = np.zeros(n)
    for i in range(n): y[i] = buf[i % p]; buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    return lp(y, 3000)
def bass(f, d):
    t = np.arange(int(d * SR)) / SR; env = np.minimum(1, t / 0.02) * np.exp(-t * 1.5) * np.minimum(1, (d - t) / 0.05)
    return env * (np.sin(2 * np.pi * f * t) + 0.15 * np.sin(2 * np.pi * 2 * f * t))
def kick():
    t = np.arange(int(0.35 * SR)) / SR; return np.sin(2 * np.pi * np.cumsum(50 + 70 * np.exp(-t * 30)) / SR) * np.exp(-t * 9)
def snare(rng):
    t = np.arange(int(0.25 * SR)) / SR; return bp(rng.standard_normal(len(t)), 1200, 5000) * np.exp(-t * 16) * 0.6 + 0.2 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25)
def hat(rng):
    t = np.arange(int(0.06 * SR)) / SR; return hp(rng.standard_normal(len(t)), 7000) * np.exp(-t * 60)

def track(name, bpm, chords, lead="kalimba", seed=1, bars=16, swing=0.58, mel_density=0.45, drums=True):
    rng = np.random.default_rng(seed); beat = 60 / bpm; bar = 4 * beat; N = int(bars * bar * SR) + SR * 2
    mix = {k: np.zeros(N) for k in ("keys", "bass", "lead", "drums")}
    def add(k, y, t, g=1.0):
        i = int(t * SR); y = y[:max(0, N - i)]; mix[k][i:i + len(y)] += g * y
    scale = sorted({n % 12 for c in chords for n in c})
    for b in range(bars):
        c = chords[b % len(chords)]; t0 = b * bar
        for j, n in enumerate(c[1:]):  # acorde arpegiado ligeramente
            add("keys", ep(mf(n), bar * 1.05, 0.55) if lead != "pad" else pad(mf(n), bar), t0 + j * 0.018, 0.5)
        add("bass", bass(mf(c[0] - 12), beat * 1.8), t0); add("bass", bass(mf(c[0] - 12), beat * 1.4), t0 + beat * 2.5, 0.8)
        if drums:
            for k_ in range(8):
                tt = t0 + k_ * beat / 2 + (beat / 2 * (swing - 0.5) * 2 if k_ % 2 else 0)
                add("drums", hat(rng), tt, 0.16 + 0.05 * (k_ % 2 == 0))
            add("drums", kick(), t0, 0.9); add("drums", kick(), t0 + beat * 2.5, 0.7)
            add("drums", snare(rng), t0 + beat, 0.45); add("drums", snare(rng), t0 + beat * 3, 0.45)
        if b >= 2:  # melodía tranquila sobre la escala del acorde
            for k_ in range(8):
                if rng.random() < mel_density:
                    n = 72 + rng.choice([x for x in scale]) + (12 if rng.random() < 0.15 else 0)
                    tt = t0 + k_ * beat / 2 + (beat / 2 * (swing - 0.5) * 2 if k_ % 2 else 0)
                    v = {"kalimba": kalimba, "marimba": marimba, "pluck": pluck, "pad": kalimba}[lead](mf(n))
                    add("lead", v, tt, 0.28)
    y = 0.9 * lp(mix["keys"], 2600) + 0.8 * mix["bass"] + lp(mix["lead"], 4200) + 0.55 * lp(mix["drums"], 6500)
    t = np.arange(N) / SR
    y = y * (1 + 0.004 * np.sin(2 * np.pi * 0.5 * t))                                # wow de cinta
    crack = np.zeros(N); idx = rng.integers(0, N, int(N / SR * 9)); crack[idx] = rng.uniform(-1, 1, len(idx))
    y += 0.04 * lp(crack, 3000) + 0.006 * lp(rng.standard_normal(N), 1200)            # vinilo
    y = lp(hp(y, 40), 7000); y = y[:int(bars * bar * SR)]
    tmp = f"{OUTD}/_{name}.wav"; sf.write(tmp, y / np.abs(y).max() * 0.8, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", "loudnorm=I=-17:TP=-2", "-ar", "44100", f"{OUTD}/{name}.wav"], check=True); os.remove(tmp)
    print(name, round(len(y) / SR, 1), "s")

# progresiones (nota grave primero = bajo); todo original
TRACKS = {
    "lofi1": dict(bpm=84, chords=[[50, 62, 65, 69, 72], [55, 59, 65, 69, 71], [48, 64, 67, 71, 74], [57, 60, 64, 67, 71]], lead="kalimba", seed=3),   # Dm9 G13 Cmaj9 Am9
    "lofi2": dict(bpm=78, chords=[[53, 64, 67, 69, 72], [52, 62, 67, 71, 74], [57, 60, 64, 67, 72], [55, 62, 65, 69, 71]], lead="pluck", seed=5),     # Fmaj7 Em7 Am7 G
    "lofi3": dict(bpm=88, chords=[[51, 62, 67, 70, 74], [48, 63, 67, 70, 74], [56, 63, 67, 72, 75], [58, 62, 65, 70, 74]], lead="marimba", seed=8),   # Ebmaj7 Cm9 Abmaj7 Bb
    "lofi4": dict(bpm=74, chords=[[45, 60, 64, 67, 71], [50, 60, 65, 69, 72], [43, 59, 62, 65, 69], [48, 59, 64, 67, 71]], lead="pad", seed=11, mel_density=0.3),  # Am9 Dm9 G9 Cmaj7
    "lofi5": dict(bpm=82, chords=[[52, 62, 66, 69, 73], [57, 61, 64, 68, 71], [54, 61, 64, 68, 69], [59, 63, 66, 69, 73]], lead="kalimba", seed=13),  # Emaj9-ish A F#m B
    "lofi6": dict(bpm=90, chords=[[48, 64, 67, 71, 74], [45, 64, 67, 72, 76], [53, 64, 69, 72, 76], [55, 62, 65, 71, 74]], lead="marimba", seed=17, drums=True),  # Cmaj9 Am7 Fmaj9 G7
}
if __name__ == "__main__":
    os.makedirs(OUTD, exist_ok=True)
    for k, v in TRACKS.items(): track(k, **v)
