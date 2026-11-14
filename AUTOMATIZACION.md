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

## 0. Preparación
1. Clona el repo `Mangatrackerr/manga-tracker-videos` (si no está ya) y trabaja en él.
2. Lee `pipeline/README.md`: estilo, voces, música, subtítulos, cierre.
   Estilo preferido: **"TODO ANIMADO"** (chico de cuerpo entero `pipeline/satira/monigote2.py`, kit `pipeline/satira/animado.py`: `A(...)`, `A_app`, `A_send`, `A_fin`).
   Lote de referencia: `pipeline/satira/lote_2026-11-13an.py`. Voces Supertonic 3 (`pipeline/satira/voz_viva.py`, sin retoque de tono).
   Música lo-fi original (`pipeline/satira/lofi.py`), una distinta por vídeo, `MUSIC_VOL = 0.2`.
   Para los vídeos de "contenido" (sin app) no uses `A_app` ni `A_send` con la app; cierra con `A_fin` sin el texto "Gratis en Play Store" (o sin `A_fin`).

## 1. ¿Hace falta un lote nuevo?
Ejecuta `python3 pipeline/estado.py quedan` (nº de temas nuevos sin publicar). **Si quedan menos de 6**, crea un lote nuevo HOY
(haya o no grabaciones nuevas). Si hay grabaciones nuevas en `grabaciones/`, úsalas para las escenas de la app; si no, usa la más reciente de `procesadas/`.
1. Monta el entorno (sección "Montaje del entorno" del README). Fuentes: `pipeline/*.ttf` → `pipeline/fonts/`. Logo: `pipeline/logo.png`.
2. Grabación nueva: si pesa mucho o va a 60 fps, recomprímela a 30 fps sin audio (CRF 25). Analízala (fotogramas a 1/s) y haz un mapa segundo a segundo.
   Evita pantallas de carga y el final con la barra de notificaciones.
3. Copia `pipeline/satira/lote_2026-11-13an.py` a `pipeline/satira/lote_<fecha>X.py` (cambia `LOTE`, `SRC_VIDEO`, temas).
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
