# Automatización diaria — vídeos de Manga Tracker

Instrucciones para la tarea programada (se ejecuta cada día a las 08:00 hora de Madrid).
Objetivo: **publicidad de la app Manga Tracker**. Publicar 3 vídeos al día en TikTok, Instagram (Reels) y YouTube (Shorts)
a las **10:00, 14:30 y 19:00** (Europe/Madrid), sin revisión manual de Xavi. Xavi confía en la edición: no le preguntes nada, decide tú.

## 0. Preparación
1. Clona el repo `Mangatrackerr/manga-tracker-videos` (si no está ya) y trabaja en él.
2. Lee `pipeline/README.md`: estilo aprobado, voces, música, subtítulos, cierre.

## 1. ¿Hay grabaciones nuevas?
Mira `grabaciones/` (ignora `.gitkeep`). Si hay vídeos:
1. Monta el entorno (sección "Montaje del entorno" del README). Los modelos, fuentes y música van en `pipeline/` y están en `.gitignore`.
   - Las fuentes ya están en `pipeline/*.ttf`: cópialas a `pipeline/fonts/`. El logo es `pipeline/logo.png`.
   - Música: `cd pipeline/music && python3 ../synth_music.py` y normaliza a `n1..n8.wav` (-13.5 LUFS).
2. Si la grabación pesa mucho o va a 60 fps, recomprímela a 30 fps sin audio (CRF 25) antes de trabajar.
3. Analiza la grabación: fotogramas a 1/s (y 2/s en zonas con acciones). Haz un mapa segundo a segundo de qué pantalla sale.
   Evita empezar escenas en pantallas de carga (rejillas vacías, spinners). Corta el final si sale la barra de notificaciones o el aviso de grabación.
4. Escribe un lote nuevo copiando `pipeline/lote_2026-11-02.py` (cambia nombre de lote, archivo y temas). Entre 4 y 8 temas, cada uno con un gancho
   distinto, de 12–25 s, todos terminando con el cierre de descarga (lo pone `make()`). Música distinta por tema (n1..n8).
   Usa SOLO funciones reales de la app (lista en el README). Los textos de voz deben ser naturales y de tono TikTok.
5. Escribe `pipeline/textos_<lote>.json` con, por tema: `titulo` (para YouTube, ≤90 car.) y `texto` (descripción + 4–6 hashtags,
   incluyendo siempre #parati y el gancho "Gratis en Play Store / link en mi perfil").
6. Renderiza UNO A UNO (en paralelo da OOM): `python3 pipeline/lote_<lote>.py`. Genera versión chico y chica de cada tema en `videos/`.
7. Revisa una tira de fotogramas de cada vídeo (sin pantallas de carga, subtítulos legibles, cierre con logo oscurecido).
8. `python3 pipeline/estado.py registrar <lote> pipeline/textos_<lote>.json`
9. Mueve la grabación a `procesadas/` (`git mv`). Borra los `.srt` de `videos/` si no hacen falta.
10. Commit y push (mensaje en español).

## 2. Programar publicaciones (siempre, haya o no grabaciones nuevas)
Mantén programados en Metricool los huecos de **hoy y mañana** (10:00, 14:30, 19:00 Europe/Madrid), saltando los que ya hayan pasado.
1. Consulta `getScheduledPosts` (blogId `7829643`, zona `Europe/Madrid`) para hoy y mañana. No dupliques huecos ya ocupados.
2. Para cada hueco libre, elige vídeo con `python3 pipeline/estado.py elegir <n>`.
   Si no hay vídeos nuevos, el script devuelve los más antiguos para **resubirlos** (Xavi lo quiere así).
3. Programa con `createScheduledPost` (blogId `7829643`), un post por hueco con las 3 redes:
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
- Si algo falla (render, Metricool, GitHub), no lo dejes a medias: programa al menos los huecos de hoy con vídeos ya existentes y deja un resumen claro del problema.
- No borres vídeos de `videos/`: se usan para las resubidas.
- Si el repo pasa de ~2 GB, avisa a Xavi.
- Al final escribe un resumen corto en español: grabaciones procesadas, vídeos nuevos, publicaciones programadas (fecha, hora, tema, voz).
