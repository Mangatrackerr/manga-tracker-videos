# Revisión de la voz (20/11/2026): transcribe con Whisper small (sherpa-onnx) para detectar palabras mal pronunciadas.
# Modelo (Hugging Face está bloqueado; GitHub sí funciona):
#   mkdir -p pipeline/whisper && cd pipeline/whisper && curl -sSL https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2 | tar xj
# Uso: python3 pipeline/satira/revisar_voz.py videos/<vídeo>.mp4 [más vídeos o .wav]
import sys, os, glob, subprocess, numpy as np, soundfile as sf, sherpa_onnx as so
HERE = os.path.dirname(os.path.abspath(__file__))
D = glob.glob(os.path.join(HERE, "..", "whisper", "*whisper-small*", ""))[0]
rec = so.OfflineRecognizer.from_whisper(encoder=D + "small-encoder.int8.onnx", decoder=D + "small-decoder.int8.onnx", tokens=D + "small-tokens.txt",
                                        language="es", task="transcribe", num_threads=2)
for f in sys.argv[1:]:
    if not f.endswith(".wav"):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
        a, sr = np.frombuffer(raw, np.float32), 16000
    else:
        a, sr = sf.read(f); a = a if a.ndim == 1 else a.mean(1)
        if sr != 16000: a = np.interp(np.arange(0, len(a), sr / 16000), np.arange(len(a)), a); sr = 16000
    a = np.concatenate([a, np.zeros(int(2.5 * sr))]).astype(np.float32)   # margen para que no corte el final
    s = rec.create_stream(); s.accept_waveform(sr, a); rec.decode_stream(s)
    print(os.path.basename(f), "|", s.result.text.strip(), flush=True)
