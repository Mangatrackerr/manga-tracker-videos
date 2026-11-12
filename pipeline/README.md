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


## Estilo gancho (aprobado por Xavi el 7/11/2026 — PREFERIDO)
Vídeos tipo "anuncio indirecto": empiezan con algo interesante y la app aparece como solución. Motor: `pipeline/gancho/engine.py`.
Lote de ejemplo (20 temas): `pipeline/gancho/lote_2026-11-07g.py`. Necesita el mismo entorno (kokoro, fuentes, música n1..n8).
- Estructura: **gancho** (dato cierto / pregunta / test, 0–3 s) → **escalada** → **giro** (problema con el que te identificas) → **demo** de la app en un móvil
  (con círculo amarillo + etiqueta sobre el dato, `callout=(x, y, texto, tiempo)` en fracciones del fotograma ORIGINAL de la grabación) → **cierre** con pregunta para comentar + logo + "Gratis en Play Store".
- Fondo morado animado con partículas (rojo para los giros), tipografía Luckiest Guy con sombra, efectos de sonido (boom, whoosh, pop, ticks), música 0.30 con sidechain, karaoke abajo.
- Primitivas: `S_counter` (número con anillo), `S_grid` (rejilla que se llena), `S_cards` (tarjetas que caen), `S_text` (texto grande, con cambio a rojo + burbujas),
  `S_strike` (tachar y corregir), `S_options` (test A/B/C/D), `S_chat` (burbujas de chat), `S_versus` (A vs B), `S_quad` (2x2), `S_countdown` (3-2-1),
  `S_phone(a, b, mode="fit"|"play", rate, callout, slide)` (la grabación entre a y b s dentro del móvil; `mode="play", rate=0` = imagen fija), `S_end`.
- Cada escena: `([índices de líneas de voz], primitiva, cola_extra)`. Tiempos: float = segundos desde el inicio de la escena; `(k, dt)` = inicio de la línea k + dt; `(k, dt, f)` = + f·duración de la línea k.
- Líneas: `(texto en pantalla, texto para la voz)` — en la voz los números van en letra. Pronunciación extra en `engine.py` (`M.SUBS`).
- Sin imágenes de anime ni logos de terceros. Solo datos ciertos o cuentas sencillas (p. ej. 365 × 24 min ≈ 146 h).
- Clips útiles de `procesadas/grabacion_2026-11-02.mp4` (s): estrenos 1.2–5.5 · ficha+añadir 13.5–17.5 · inicio 19.5–24 · filtros 26.6–28.8 (demografía y=0.854, isekai 0.32/0.589) ·
  comedia 32–38 · buscar con pestañas 47.5 (Novelas 0.87/0.165) · episodios 62–66 · manga/manhwa 72–80 · Mi Lista 90.1–92.6 (Ep. 7 0.09/0.594) · ficha 12 ep. 97.3 ·
  añadir a top tier 98–99.8 · mis listas 105–108.2 · amigo 121.3–124.5 · perfil fijo 127.75 (167 0.22/0.487, 120 0.13/0.60, 38 0.5/0.60) · estados fijo 129.5 (completado 0.80/0.388, en pausa 0.80/0.452, abandonado 0.80/0.515) · medallas fijo 131.0 (10/12 0.875/0.182).


## Estilo satírico (aprobado por Xavi el 13/11/2026 — PREFERIDO)
Basado en el trend de explainers satíricos animados ("¿Sabías que…?" con tono irónico). Motor: `pipeline/satira/engine_satira.py`.
- Estructura: **GANCHO potente 0–5 s** (`Sc_hook`: icono grande + cifra/contador + sello; dato de industria, noticia reciente o curiosidad,
  aunque no sea del nicho) → **sátira** con el personaje plano (`Sc_hud` con medidores/sellos, `Sc_question` con HUD que no acierta, `Sc_reveal` "invento™" en pedestal)
  → **app en el móvil** (`Sc_phone` con callout) → **"Mándaselo a…"** (`Sc_ambassador`) → cierre `Sc_end`.
- Subtítulos ARRIBA palabra a palabra; las palabras entre *asteriscos* salen en amarillo. Fondos de rayos (`pal`: gold/blue/pink/green/red/purple).
- Personaje: `personaje.py` (expresiones neutral/smug/confused/shock/proud/cry, gafas, banda). Iconos: `iconos.py` (todo dibujado, sin imágenes de terceros).
- Voz: Supertonic 3 (modelo en `pipeline/supertonic/`, se descarga de
  https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/sherpa-onnx-supertonic-3-tts-int8-2026-05-11.tar.bz2; `pip install sherpa-onnx pyworld`).
  `voz_viva.patch(M)`: frase a frase, 4 tomas y se elige la más expresiva; texto con ¡! ¿? y "…" para dar vida. El retoque de tono (WORLD) está DESACTIVADO porque sonaba robótico.
- Música: `python3 pipeline/satira/lofi.py` genera lofi1..lofi20 (originales). Una distinta por vídeo, volumen 0.2.
- Nada de destellos/parpadeos rápidos (vídeo del episodio de Porygon). Solo datos comprobados; nada de tragedias reales (p. ej. Kyoto Animation) como gancho.
