# Automatización diaria — vídeos de Manga Tracker

Instrucciones para la tarea programada (se ejecuta cada día a las 07:54 hora de Madrid). Xavi no revisa los vídeos: no le preguntes nada, decide tú.

## REGLAS VIGENTES (decididas por Xavi el 14/11/2026 — mandan sobre todo lo demás)
1. **2 publicaciones al día: 14:30 y 21:00** (Europe/Madrid), las dos en **TikTok + Instagram (Reel) + YouTube (Short)**. Se acabaron los huecos de 10:00, 19:00 y 22:00.
2. **Nunca se repite un vídeo ni un tema.** No hay resubidas. De cada tema se hace **UNA sola versión** con la voz que mejor le encaje:
   chico 1 = `st5`, chica 1 = `st0`, chica 5 = `st4` (las dos chicas que gustan a Xavi). Reparte las voces de forma variada a lo largo del lote.
3. **La mitad de los vídeos NO son publicidad**: contenido puro de anime/manga/manhwa (dato, ranking, polémica, pregunta) SIN demo de la app,
   SIN nombrar Manga Tracker en la voz y SIN "Gratis en Play Store" en el vídeo ni en el texto. Cierre: solo el logo pequeño 1 s, o nada.
   La otra mitad sí lleva la app, pero integrada en la historia (no como anuncio final). Alterna: un día el de 14:30 es "contenido" y el de 21:00 "app", al día siguiente al revés.
4. **Vídeos que inciten a comentar y compartir**: debates ("¿A o B?"), tops discutibles, "etiqueta a tu amigo que…", "di uno peor", preguntas con respuesta fácil.
   Termina siempre con una pregunta clara para comentarios. El texto del post también acaba con esa pregunta.
5. **Gancho corto**: la primera frase ≤ 8 palabras, en pantalla en el segundo 0, sin introducción ni saludo. Duración total 15–25 s.
6. **Revisión semanal (cada lunes)**: ver sección 4.
7. **ESTILO VARIADO (decidido por Xavi el 16/11/2026 — obligatorio desde ahora)**: en CADA vídeo cambian el **personaje**, el **escenario** y la **animación**.
   Nunca dos vídeos seguidos con el mismo personaje ni el mismo escenario. Se acabó el chico de la sudadera morada en la habitación para todo.
   - Personaje: `MO.set_look(**LOOKS[nombre])` (`pipeline/satira/looks.py`). Hay 5 (kenji, yuna, aiko, taro, mika); crea looks nuevos en cada lote
     combinando `hair_style` (short, spiky, curly, long, bob, ponytail, buns), `top` (hoodie, tee, tank, jacket, uniform, chef, sweater),
     `bottom` (jeans, skirt, shorts, track), colores de piel/pelo/ropa, `glasses`, `hat` (cap, bandana, headband, chef), `apron`, `lashes`. La voz debe cuadrar con el personaje (chico st5; chica st0/st4).
   - Escenario: `pipeline/satira/escenarios.py` (`EC.instalar()`; ramen, cocina, cine, cine_hall, biblio, biblio_mesa, montana, cielo, estadio, podio),
     cada uno con cámara a la deriva y animación ambiental propia. Dibuja escenarios NUEVOS en cada lote (función base + función `_amb`, añadir a `SCEN`):
     un escenario principal + una variante por vídeo, relacionados con el tema.
   - Animación: props dibujados propios del tema con `dict(k="draw", fn=..., front=bool)` (en `animado.A`), entradas corriendo (`run_until`/`xmove`), etc.
   - Cierre: `A_preg2(pregunta, escenario)` = la pregunta sobre el escenario del propio vídeo difuminado (no el fondo de rayos de siempre).
   - Lote de referencia: `pipeline/satira/lote_2026-11-20x.py` (el más completo: 10 personajes, 20 escenarios de `escenarios2.py`, gancho con `punch`).
8. **RETENCIÓN (pedido por Xavi el 20/11/2026)**: en el fotograma 0 ya tiene que estar pasando algo llamativo (un camión que cruza, un tren, una bola de energía,
   un contador disparado, un libro que explota en páginas...) y la primera escena entra con `punch(...)` (golpe de cámara). El texto grande del gancho
   aparece ya en el segundo 0 (`t=-0.12`). Temática distinta en cada vídeo (no repetir temas de lotes anteriores).
9. **VOZ HUMANA (20/11/2026)**: escribe la línea de voz con pausas naturales (comas y "…" donde una persona respiraría), números en letra y nombres
   extranjeros con su pronunciación en `M.SUBS` (p. ej. Kamehameha→"Kamejaméja", Ghibli→"Guíbli", hawaiano→"jawaiano").
   Comprueba SIEMPRE la voz transcribiendo el audio final con Whisper (modelo `sherpa-onnx-whisper-small` de los releases de k2-fsa en GitHub,
   Hugging Face está bloqueado) y corrige lo que se entienda mal antes de publicar.

## 0. Preparación
1. Clona el repo `Mangatrackerr/manga-tracker-videos` (si no está ya) y trabaja en él.
2. Lee `pipeline/README.md`: estilo, voces, música, subtítulos, cierre.
   Estilo preferido: **"TODO ANIMADO" VARIADO** (regla 7: personaje, escenario y animación distintos en cada vídeo; referencia `pipeline/satira/lote_2026-11-16v.py`). Base técnica: chico de cuerpo entero `pipeline/satira/monigote2.py`, kit `pipeline/satira/animado.py`: `A(...)`, `A_app`, `A_send`, `A_fin`).
   Lote de referencia: `pipeline/satira/lote_2026-11-16v.py` (el antiguo 13an ya no sirve de modelo visual). Voces Supertonic 3 (`pipeline/satira/voz_viva.py`, sin retoque de tono).
   Música lo-fi original (`pipeline/satira/lofi.py`), una distinta por vídeo, `MUSIC_VOL = 0.2`.
   Para los vídeos de "contenido" (sin app) no uses `A_app` ni `A_send` con la app; cierra con `A_fin` sin el texto "Gratis en Play Store" (o sin `A_fin`).

## 1. ¿Hace falta un lote nuevo?
Ejecuta `python3 pipeline/estado.py quedan` (nº de temas nuevos sin publicar). **Si quedan menos de 6**, crea un lote nuevo HOY
(haya o no grabaciones nuevas). Si hay grabaciones nuevas en `grabaciones/`, úsalas para las escenas de la app; si no, usa la más reciente de `procesadas/`.
1. Monta el entorno (sección "Montaje del entorno" del README). Fuentes: `pipeline/*.ttf` → `pipeline/fonts/`. Logo: `pipeline/logo.png`.
2. Grabación nueva: si pesa mucho o va a 60 fps, recomprímela a 30 fps sin audio (CRF 25). Analízala (fotogramas a 1/s) y haz un mapa segundo a segundo.
   Evita pantallas de carga y el final con la barra de notificaciones.
3. Copia `pipeline/satira/lote_2026-11-16v.py` a `pipeline/satira/lote_<fecha>X.py` (cambia `LOTE`, `SRC_VIDEO`, temas).
   **8–10 temas, la mitad "contenido" y la mitad "app"**, cumpliendo las reglas 3–5. Cada tema con UNA voz: genera solo esa versión
   (adapta el `__main__` para que cada tema tenga su voz fija y el archivo salga como `videos/<lote>_<tema>_<chico|chica>.mp4`).
   Usa SOLO funciones reales de la app y SOLO datos ciertos y comprobables. Nada de imágenes de anime ni logos de terceros. Nada de destellos rápidos.
   Fotogramas de prueba antes del render completo (`chk`).
4. `pipeline/textos_<lote>.json`: por tema (clave = nombre sin número) `titulo` (≤90 car.) y `texto`:
   - "contenido": texto + pregunta para comentarios + 4–6 hashtags (incluye #parati). SIN mención a la app.
   - "app": texto + pregunta + "Manga Tracker, gratis en Play Store, link en mi perfil 👆" + 4–6 hashtags.
   Añade también `"tipo": "contenido"` o `"tipo": "app"`.
5. Renderiza UNO A UNO (en paralelo da OOM). Revisa una tira de fotogramas de cada vídeo.
6. `python3 pipeline/estado.py registrar <lote> pipeline/textos_<lote>.json animado`.
7. Si usaste una grabación nueva, muévela a `procesadas/` (`git mv`). Borra los `.srt` sobrantes de `videos/`.
8. Commit y push (mensaje en español).

## 2. Programar publicaciones (siempre)
Mantén programados en Metricool los huecos de **hoy y mañana a las 14:30 y 21:00** (Europe/Madrid), saltando los que ya hayan pasado.
1. `getScheduledPosts` (blogId `7829643`, zona `Europe/Madrid`) para hoy y mañana. No dupliques huecos ocupados.
   Los posts en borrador (`draft: true`) no cuentan: son versiones repetidas que se desactivaron el 14/11.
2. Para cada hueco libre: `python3 pipeline/estado.py elegir <n>` (solo devuelve temas nunca publicados, una versión por tema).
   Respeta la alternancia contenido/app de la regla 3 cuando haya donde elegir.
   Si no hay vídeos suficientes, crea un lote (sección 1) antes de seguir; si eso falla, deja el hueco vacío y avísalo (NUNCA repitas un vídeo).
3. `createScheduledPost` (blogId `7829643`), un post por hueco:
   - `media`: [url del vídeo en raw.githubusercontent.com]
   - `providers`: tiktok, instagram, youtube
   - `text`: el `texto` del vídeo
   - `tiktokData`: {"title": titulo, "privacyOption": "PUBLIC_TO_EVERYONE", "isAigc": true, "autoAddMusic": false}
   - `instagramData`: {"type": "REEL", "showReelOnFeed": true, "isAiGenerated": true}
   - `youtubeData`: {"title": titulo, "type": "short", "privacy": "public", "madeForKids": false, "isAiGeneratedContent": false, "category": "ENTERTAINMENT", "tags": ["anime","manga","manhwa","mangatracker"]}
   - `autoPublish`: true, `draft`: false
   - `publicationDate`: {"dateTime": "YYYY-MM-DDTHH:MM:00", "timezone": "Europe/Madrid"}
4. Tras cada post correcto: `python3 pipeline/estado.py marcar <id> <YYYY-MM-DDTHH:MM>`.
5. Commit y push de `estado.json`.

## 3. Avisos
- Si algo falla (render, Metricool, GitHub), no lo dejes a medias: programa al menos los huecos de hoy con vídeos nuevos ya existentes y deja un resumen claro del problema.
- No borres vídeos de `videos/`. Si el repo pasa de ~2 GB, avisa a Xavi.
- Al final escribe un resumen corto en español: lote creado (si hay), publicaciones programadas (fecha, hora, tema, voz, contenido/app).

## 4. Revisión semanal (solo los lunes)
1. Saca de Metricool las métricas de TikTok de los últimos 7 días (`getAnalyticsDataByMetrics`, brandId `7829643`,
   métricas `TKPO02, TKPO05, TKPO07, TKPO08, TKPO09, TKPO10`; si `TKPO13`/`TKPO15` traen datos, inclúyelos). Si puedes, también Instagram y YouTube.
2. Compara: vídeos "contenido" vs "app", tipo de gancho, voz, hora. Saca 2–3 conclusiones concretas.
3. Escríbelo en `revisiones/<fecha>.md` (tabla + conclusiones + qué cambias en el próximo lote) y aplica esos cambios en esta guía si hace falta.
4. Envía a Xavi una notificación con el resumen (media de visitas de la semana vs la anterior, mejor y peor vídeo, qué vas a cambiar).

## Historial
- 13/11/2026: lote animado 2026-11-13an (10 temas × 2 voces).
- 14/11/2026: se pasa a 2 vídeos/día sin repeticiones. Las versiones repetidas ya programadas del 14 al 18/11 se pusieron en borrador en Metricool.
  Lote 2026-10-11 marcado como `descartado` (anuncio puro antiguo).
- 14/11/2026: lote 2026-11-14p (10 temas, 5 contenido + 5 app, una voz por tema) aprobado por Xavi y programado del 17/11 21:00 al 22/11 14:30.
  Quedan 8 temas sin publicar del lote satírico 2026-11-12i (todos "app"): úsalos intercalados con contenido nuevo cuando se cree el próximo lote.
- 16/11/2026: revisión semanal (`revisiones/2026-11-16.md`). Cambios para el próximo lote: mayoría "contenido" (6 + 3–4 app) porque lo que queda es todo "app";
  pregunta final cerrada y de una palabra ("¿A o B?", "di un número") en pantalla los últimos 3–4 s; nada de "¿Lo sabías?"; algún ranking incompleto adrede ("falta el nº 1, dilo tú").
- 16/11/2026: lote de prueba 2026-11-16v (5 temas de contenido, cada uno con personaje, escenario y animación distintos). A Xavi le gustan: es el estilo
  obligatorio desde ahora (regla 7). Programado intercalado con lo que había: los nuevos a las 14:30 del 17 al 21/11 y los antiguos corridos a las 21:00
  (y del 22 al 24/11). Programación cubierta hasta el 24/11 21:00.
- 20/11/2026: a petición de Xavi se vació la cola: los 8 vídeos antiguos programados (lote 14p, mismo personaje y escenario) pasaron a borrador en Metricool
  y se marcaron `descartado`, igual que los 8 sin publicar del lote satírico 12i. Se mantuvieron los 2 del lote variado 16v (20/11 y 21/11 a las 14:30).
  Lote nuevo 2026-11-20x: 10 temas (4 contenido + 6 app), cada uno con personaje, escenario, temática y animación distintos, gancho visual en el fotograma 0,
  voz mejorada (`voz_viva.py`: tomas de duración rara descartadas, finales sin cortar, pausas no idénticas, aire de habitación) y revisada con Whisper.
  Programado del 20/11 21:00 al 25/11 21:00.
- 21/11/2026 (tarea automática): lote 2026-11-21y, 8 temas (4 contenido + 4 app) ya ordenados para la alternancia (26/11 14:30 app → 29/11 21:00 app).
  Personajes nuevos en `looks.py` (momo, hana, rio, yui, takumi, iris, kuro, nami) y 8 escenarios nuevos + variante en `escenarios3.py`
  (futuro, campo, despacho/niebla, huerto, lavanderia, pizzeria, pabellon, sakura; `EC3.instalar3()`). Nota: `estado.py registrar` con estilo animado
  reordena los temas de una sola voz; tras registrar se dejó la cola en el orden del JSON de textos.
- 23/11/2026: revisión semanal (`revisiones/2026-11-23.md`). TikTok 458 visitas/vídeo (−44 %), Instagram 787 (+34 %). Cambios para el próximo lote:
  preguntas finales tipo "dilo tú" / "completa el top" / "di uno peor" (son las que traen comentarios), vídeos de "contenido" con opinión discutible
  (no solo dato curioso + "elige uno"), mantener gancho en el fotograma 0. Huecos 23–24/11 ya estaban cubiertos; quedan 8 temas (lote 21y) sin programar.

