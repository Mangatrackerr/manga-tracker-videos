# Voz "con vida" (prueba 12/11/2026): Supertonic 3 + trucos para que suene menos a IA.
#  1) se genera frase a frase (cortando en . ! ? …) con velocidad según el tipo de frase
#  2) varias tomas por frase y se elige la de entonación más viva (más variación de tono; en preguntas, la que más sube al final)
#  3) retoque de entonación con WORLD: se amplían los altibajos de tono y se sube el final de las preguntas
#  4) pausas con intención (… = pausa dramática) y cadena de "micro de creador" (EQ + compresión) en el montaje
# Voces: "st0".."st9" (0–4 chicas, 5–9 chicos). Aprobadas por Xavi para probar: chico 1 = st5; chica 1, 2, 5 = st0, st1, st4.
import os, re, numpy as np, soundfile as sf, pyworld as pw
import sherpa_onnx as so
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "..", "supertonic")
_tts = None
def _engine():
    global _tts
    if _tts is None:
        m = so.OfflineTtsSupertonicModelConfig(duration_predictor=f"{D}/duration_predictor.int8.onnx", text_encoder=f"{D}/text_encoder.int8.onnx",
            vector_estimator=f"{D}/vector_estimator.int8.onnx", vocoder=f"{D}/vocoder.int8.onnx", tts_json=f"{D}/tts.json",
            unicode_indexer=f"{D}/unicode_indexer.bin", voice_style=f"{D}/voice.bin")
        _tts = so.OfflineTts(so.OfflineTtsConfig(model=so.OfflineTtsModelConfig(supertonic=m, num_threads=2)))
    return _tts

def _gen(text, sid, speed):
    g = so.GenerationConfig(); g.sid = sid; g.speed = speed; g.extra = {"lang": "es"}
    a = _engine().generate(text, g); x = np.array(a.samples, dtype=np.float64)
    thr = 0.02 * np.abs(x).max(); idx = np.where(np.abs(x) > thr)[0]
    return x[max(0, idx[0] - 600):idx[-1] + 1800], a.sample_rate

def _f0(x, sr):
    f0, t = pw.dio(x, sr, frame_period=5.0); return pw.stonemask(x, f0, t, sr), t

def _score(x, sr, kind):
    f0, _ = _f0(x, sr); v = f0[f0 > 0]
    if len(v) < 20: return -9
    lf = np.log(v); s = np.std(lf)
    if kind == "?":  # que suba al final
        n = len(v); s += 2.0 * (np.median(lf[int(n * 0.8):]) - np.median(lf[:int(n * 0.6)]))
    return s

def _intonate(x, sr, kind):
    f0, t = pw.harvest(x, sr, frame_period=5.0); sp = pw.cheaptrick(x, f0, t, sr); ap = pw.d4c(x, f0, t, sr)
    vo = f0 > 0
    if vo.sum() < 10: return x
    lf = np.log(np.where(vo, f0, 1.0)); mu = np.median(lf[vo])
    k = {"!": 1.3, "?": 1.22, "…": 1.12}.get(kind, 1.18)
    lf2 = np.where(vo, mu + (lf - mu) * k, 0)
    if kind == "!": lf2 = np.where(vo, lf2 + 1.2 / 12 * np.log(2), 0)  # algo más agudo = más energía
    if kind == "?":  # subida final de hasta +4 semitonos en los últimos ~0.45 s con voz
        vi = np.where(vo)[0]; end = vi[-1]; st = max(vi[0], end - 90)
        ramp = np.clip((np.arange(len(f0)) - st) / max(1, end - st), 0, 1) ** 1.6
        lf2 = np.where(vo, lf2 + ramp * 3.2 / 12 * np.log(2), 0)
    lf2 = np.clip(lf2, mu - 7 / 12 * np.log(2), mu + 10 / 12 * np.log(2))  # sin pasarse: de -7 a +10 semitonos
    f2 = np.where(vo, np.exp(lf2), 0.0)
    y = pw.synthesize(f2, sp, ap, sr, 5.0)
    return y[:len(x)] if len(y) >= len(x) else np.pad(y, (0, len(x) - len(y)))

SPEED = {"!": 1.13, "?": 1.06, "…": 0.98, ".": 1.05}
PAUSE = {"!": 0.16, "?": 0.2, "…": 0.42, ".": 0.24}
def tts_viva(text, voice, fn, takes=4):
    sid = int(voice[2:])
    parts = [p for p in re.split(r"(?<=[.!?…])\s+", text.strip()) if p]
    sr = 44100; out = []
    for i, p in enumerate(parts):
        kind = p[-1] if p[-1] in "!?…" else "."
        txt = p.replace("…", "...")
        best, bs = None, -1e9
        for k in range(takes):
            x, sr = _gen(txt, sid, SPEED[kind] * (1 + 0.03 * (k - 1.5)))
            sc = _score(x, sr, kind)
            if sc > bs: best, bs = x, sc
        y = _intonate(best, sr, kind)
        out.append(y)
        if i < len(parts) - 1: out.append(np.zeros(int(PAUSE[kind] * sr)))
    a = np.concatenate(out); a = a / (np.abs(a).max() + 1e-9) * 0.9
    sf.write(fn, a, sr); return len(a) / sr

def patch(M):
    """sustituye M.tts para las voces 'stN' (las demás siguen con Kokoro)"""
    orig = M.tts
    def tts(text, voice, fn):
        if voice.startswith("st"): return tts_viva(M.to_say(text), voice, fn)
        return orig(text, voice, fn)
    M.tts = tts
