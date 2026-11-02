# Pipeline de vídeos promocionales — Manga Tracker

Receta para convertir una grabación de pantalla de la app en varios vídeos verticales (TikTok / Reels / Shorts) con voz en off, subtítulos karaoke, música de fondo y cierre con logo. Todo es offline y gratuito.

## Archivos (en este proyecto, carpeta claude/pipeline-videos/)
- `make_video.py` — motor de render. Función `make(name, title, scenes, end_show, voice, music, outdir)`.
- `synth_music.py` — genera 8 pistas de música originales (m1..m8.wav) con semillas fijas. Normalizar después a -13.5 LUFS.
- `logo_png_base64.txt` — logo redondo con aro morado (460x460 PNG) en base64 → decodificar a `logo.png`.

## Montaje del entorno (cada sesión empieza de cero)
```bash
mkdir -p work && cd work   # copiar aquí make_video.py, synth_music.py
base64 -d logo_png_base64.txt > logo.png
pip install --break-system-packages kokoro-onnx soundfile scipy fonttools brotli
mkdir kokoro && cd kokoro
curl -sSLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -sSLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
cd ..
# Fuentes (raw.githubusercontent está bloqueado; usar npm)
mkdir fonts && cd fonts && npm pack @fontsource/luckiest-guy @fontsource/montserrat && for t in *.tgz; do mkdir -p ${t%.tgz}; tar xzf $t -C ${t%.tgz}; done && cd ..
python3 - <<'EOF'
from fontTools.ttLib import TTFont; import glob
f=TTFont(glob.glob("fonts/*luckiest*/package/files/luckiest-guy-latin-400-normal.woff2")[0]); f.flavor=None; f.save("fonts/LuckiestGuy.ttf")
f=TTFont(glob.glob("fonts/*montserrat*/package/files/montserrat-latin-900-normal.woff2")[0]); f.flavor=None
for r in f["name"].names:
    if r.nameID in (1,4,16): r.string="MTBlack"
    if r.nameID in (2,17): r.string="Regular"
    if r.nameID==6: r.string="MTBlack-Regular"
f["OS/2"].usWeightClass=400; f.save("fonts/Montserrat-Black.ttf")
EOF
mkdir music && cd music && python3 ../synth_music.py && for i in 1 2 3 4 5 6 7 8; do ffmpeg -v error -y -i m$i.wav -af loudnorm=I=-13.5:TP=-1.5 -ar 44100 n$i.wav; done && cd ..
```
Copiar la grabación como `in.mp4` (o exportar `SRC_VIDEO=/ruta/video.mp4`).

## Proceso por grabación
1. Extraer fotogramas (1/s, y a 2/s en las zonas con acciones) y mapear qué pantalla sale en cada segundo. Las grabaciones son VFR: elegir inicios de escena cuando la pantalla ya ha cargado (no en el "Populares ahora" vacío).
2. Cortar el final si sale la barra de notificaciones / overlay de grabación.
3. Escribir 6–8 temas distintos. Cada escena = `(inicio_seg, fin_seg, "frase")`; la voz marca la duración y el vídeo se acelera (máx 2.2x) o ralentiza (máx 1.35x + congelado) para encajar.
4. Llamar `make()` dos veces por tema: voz "chico" y voz "chica". Música distinta por tema (n1..n8).
5. Renderizar UNO A UNO (en paralelo da OOM con ~3 GB por ffmpeg).
6. Revisar con una tira de fotogramas: cierre oscurecido, subtítulos legibles, sin pantallas de carga.

## Estilo fijado (aprobado por Xavi)
- 1080x1920, 30 fps, H.264 CRF 18, AAC 192k, -14 LUFS.
- Fondo: el propio vídeo difuminado y oscurecido a los lados; se recorta la barra de estado (34 px arriba del original 386x850).
- Título gancho arriba (Luckiest Guy 84, caja morada #7B3FE4), hasta el cierre.
- Subtítulos karaoke: Montserrat Black 112, blanco, contorno negro 10, sombra morada, palabra activa amarilla (#FFE14D) con "pop"; grupos de ≤12 caracteres.
- Música a volumen 0.32 con sidechain (baja cuando habla la voz), fade in 0.4 s / out 1.3 s.
- Cierre ~4.5 s: último fotograma congelado, difuminado y oscurecido + logo + "MANGA TRACKER" + "GRATIS EN PLAY STORE" (amarillo) + "ENLACE EN MI PERFIL".
- Voces Kokoro, speed 1.0: chico = `em_santa`; chica = 0.5·`ef_dora` + 0.5·`af_heart`.
- Pronunciación: Manga Tracker→"Manga Tráker", trackear→"trakear", manhwa→"manjua", manhua→"manjúa", top tier→"top táier", Play Store→"Plei Stor".

## Ejemplo de escenas (grabación del 11-oct, 101 s)
```python
make("02_que_veo_hoy_chico","¿QUÉ VEO HOY?",[
 (31.8,33.6,"¿No sabes qué ver hoy?"),
 (33.6,37.2,"Filtra por género: misterio, deportes,"),
 (37.2,41.0,"isekai, reencarnación, romance… lo que te apetezca."),
 (41.8,47.5,"Y Manga Tracker te enseña justo lo que buscas.")],
 "Descárgala gratis en Play Store. ¡El enlace está en mi perfil!","chico","music/n2.wav","out")
```
Temas que funcionaron: Todo en una app · ¿Qué veo hoy? (filtros) · ¿Por qué capítulo ibas? · Añade cualquier serie · Haz tu top tier · ¿Cuánto anime has visto? · ¿No sabes qué leer? · Manga Tracker en 30 s.

Funciones reales de la app (no inventar otras): buscar anime/manga/manhwa/manhua/novelas, filtros por género y demografía, Mi Lista con estados (viendo, completado, en pausa, abandonado, planificado) y episodio exacto, listas personalizadas públicas/privadas, ficha con sinopsis/valoración/géneros, recomendaciones para ti, nuevos capítulos, amigos, estadísticas, medallas/logros, 6 idiomas.

Enlace Play Store: https://play.google.com/store/apps/details?id=com.mangatracker.app
