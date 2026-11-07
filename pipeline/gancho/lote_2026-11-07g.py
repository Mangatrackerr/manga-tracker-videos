# Lote "gancho" del 7/11/2026 — vídeos con motion graphics + promo indirecta (grabación del 2/11)
# Uso: python3 pipeline/gancho/lote_2026-11-07g.py [tema ...]   (renderiza chico y chica de cada tema; salta los que ya existen)
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["SRC_VIDEO"] = os.path.abspath(os.path.join(HERE, "..", "..", "procesadas", "grabacion_2026-11-02.mp4"))
sys.path.insert(0, HERE)
from engine import *
LOTE = "2026-11-07g"
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "videos"))
OR = (255, 120, 60); AM = (255, 170, 40); AZ = (90, 160, 255); MO = (190, 90, 255); RO = (230, 60, 90); VE = (40, 190, 120)
FIN = "Descárgala gratis en Play Store."
# clips de la grabación del 2/11
MI_LISTA = (90.1, 92.6); EPIS = (62.0, 66.0); PERFIL = (127.75, 127.85); ESTADOS = (129.5, 129.6); MEDALLAS = (131.0, 131.1)
FILTROS = (26.6, 28.8); ESTRENOS = (1.2, 5.5); GUARDAR = (13.5, 17.5); INICIO = (19.5, 24.0); TABS = (72.0, 80.0)
LISTAS = (105.0, 108.2); AMIGO = (121.3, 124.5); MANHWA = (76.0, 80.0)

V = {}
V["01_a_medias"] = ("chica", "n1", [
    ("Apuesto a que no sabes cuántos animes tienes a medias.", "Apuesto a que no sabes cuántos animes tienes a medias."),
    ("El que dejaste en el capítulo 6. El de 'mañana lo sigo'. El que te spoilearon.", "El que dejaste en el capítulo seis. El de, mañana lo sigo. El que te spoilearon."),
    ("Yo lo apunto todo en Manga Tracker,", "Yo lo apunto todo en Manga Tracker,"),
    ("y cuando lo vi, flipé: 11 abandonados y 28 en pausa.", "y cuando lo vi, flipé: once abandonados, y veintiocho en pausa."),
    ("¿Cuántos tienes tú a medias?", "¿Cuántos tienes tú a medias?"), (FIN, FIN)], [
    ([0], S_text([("¿CUÁNTOS ANIMES", 104, WHITE), ("TIENES", 104, WHITE), ("A MEDIAS?", 170, YEL)], y=820), 0),
    ([1], S_cards("TU CEMENTERIO DE ANIMES", [("EL DEL CAPÍTULO 6", OR, None, "?"), ("EL DE 'MAÑANA LO SIGO'", AM, None, "?"), ("EL QUE TE SPOILEARON", RO, None, "!")],
                  [(0, 0), (0, 0, 0.36), (0, 0, 0.68)], shake_at=(0, 0, 0.95)), 0),
    ([2], S_phone(*MI_LISTA, slide=True), 0),
    ([3], S_phone(*ESTADOS, mode="play", rate=0, callout=(0.80, 0.515, "11 ABANDONADOS", (0, 0, 0.45))), 0),
    ([4, 5], S_end("¿CUÁNTOS TIENES", "A MEDIAS?"), 1.3)])

V["02_regla_3_episodios"] = ("chico", "n2", [
    ("En el anime hay una regla no escrita: la regla de los 3 episodios.", "En el anime hay una regla no escrita: la regla de los tres episodios."),
    ("Si en el tercero no te ha enganchado, lo dejas. Sin culpa.", "Si en el tercero no te ha enganchado, lo dejas. Sin culpa."),
    ("El truco es saber siempre en qué episodio vas.", "El truco es saber siempre en qué episodio vas."),
    ("Yo marco cada episodio en Manga Tracker,", "Yo marco cada episodio en Manga Tracker,"),
    ("y si no me engancha, lo paso a abandonado y listo.", "y si no me engancha, lo paso a abandonado y listo."),
    ("¿Tú le das 3 episodios o solo 1?", "¿Tú le das tres episodios, o solo uno?"), (FIN, FIN)], [
    ([0], S_counter("REGLA OTAKU", "LA REGLA DE LOS", None, 3, "EPISODIOS", count_d=1.0), 0),
    ([1], S_cards("¿TE ENGANCHA?", [("EPISODIO 1", AZ, "PRESENTACIÓN", "1"), ("EPISODIO 2", MO, "SE PONE INTERESANTE...", "2"), ("EPISODIO 3", AM, "O TE ENGANCHA O FUERA", "3")],
                  [(0, 0), (0, 0, 0.25), (0, 0, 0.5)]), 0),
    ([2], S_text([("EL TRUCO:", 110, WHITE), ("SABER EN QUÉ", 120, WHITE), ("EPISODIO VAS", 150, YEL)], y=800), 0),
    ([3], S_phone(*EPIS, slide=True), 0),
    ([4], S_phone(62.0, 62.1, mode="play", rate=0, callout=(0.5, 0.27, "ESTADOS", (0, 0, 0.4))), 0),
    ([5, 6], S_end("¿3 EPISODIOS", "O SOLO 1?"), 1.3)])

V["03_manga_manhwa_manhua"] = ("chica", "n3", [
    ("Manga, manhwa y manhua no son lo mismo. Y casi nadie sabe la diferencia.", "Manga, manhwa y manhua no son lo mismo. Y casi nadie sabe la diferencia."),
    ("El manga es japonés y se lee de derecha a izquierda.", "El manga es japonés, y se lee de derecha a izquierda."),
    ("El manhwa es coreano y suele leerse en vertical y a todo color.", "El manhwa es coreano, y suele leerse en vertical, y a todo color."),
    ("Y el manhua es chino.", "Y el manhua es chino."),
    ("Yo los tengo todos en Manga Tracker, separados por tipo,", "Yo los tengo todos en Manga Tracker, separados por tipo,"),
    ("y me dice cuántos llevo de cada uno.", "y me dice cuántos llevo de cada uno."),
    ("¿Cuál lees tú más?", "¿Cuál lees tú más?"), (FIN, FIN)], [
    ([0], S_text([("MANGA", 150, YEL), ("MANHWA", 150, WHITE), ("MANHUA", 150, YEL), ("NO SON LO MISMO", 90, WHITE)], y=640), 0),
    ([1, 2, 3], S_cards("LA DIFERENCIA", [("MANGA", OR, "JAPÓN · DE DERECHA A IZQUIERDA", "1"), ("MANHWA", AZ, "COREA · VERTICAL Y A COLOR", "2"), ("MANHUA", RO, "CHINA", "3")],
                        [(0, 0), (1, 0), (2, 0)]), 0),
    ([4], S_phone(*TABS, slide=True), 0),
    ([5], S_phone(*PERFIL, mode="play", rate=0, callout=(0.5, 0.60, "38 MANHWAS", (0, 0, 0.3))), 0),
    ([6, 7], S_end("¿CUÁL LEES", "TÚ MÁS?"), 1.3)])

V["04_shonen_no_es_accion"] = ("chico", "n4", [
    ("Shonen no significa anime de acción.", "Shonen no significa anime de acción."),
    ("Significa 'chico joven': es el público al que va dirigido.", "Significa, chico joven. Es el público al que va dirigido."),
    ("Shojo es para chicas jóvenes, seinen para hombres adultos y josei para mujeres adultas.", "Shojo es para chicas jóvenes, seinen para hombres adultos, y josei para mujeres adultas."),
    ("Por eso en Manga Tracker puedes filtrar por género y también por demografía.", "Por eso en Manga Tracker puedes filtrar por género, y también por demografía."),
    ("¿Eres más de shonen o de seinen?", "¿Eres más de shonen o de seinen?"), (FIN, FIN)], [
    ([0, 1], S_strike("SHONEN", "ACCIÓN", "CHICO JOVEN"), 0),
    ([2], S_cards("DEMOGRAFÍAS", [("SHONEN", OR, "CHICOS JÓVENES", "S"), ("SHOJO", (240, 100, 170), "CHICAS JÓVENES", "S"), ("SEINEN", AZ, "HOMBRES ADULTOS", "S"), ("JOSEI", MO, "MUJERES ADULTAS", "J")],
                  [0.0, (0, 0, 0.05), (0, 0, 0.33), (0, 0, 0.66)]), 0),
    ([3], S_phone(*FILTROS, slide=True, callout=(0.59, 0.854, "DEMOGRAFÍA", (0, 0, 0.62))), 0),
    ([4, 5], S_end("¿SHONEN", "O SEINEN?"), 1.3)])

V["05_quiz_cuantos_animes"] = ("chica", "n5", [
    ("Responde rápido: ¿cuántos animes has visto en tu vida?", "Responde rápido: ¿cuántos animes has visto en tu vida?"),
    ("Si has dicho 'ni idea', tranqui, yo tampoco lo sabía.", "Si has dicho, ni idea, tranqui, yo tampoco lo sabía."),
    ("Hasta que empecé a apuntarlo todo en Manga Tracker.", "Hasta que empecé a apuntarlo todo en Manga Tracker."),
    ("Ahora lo sé: 120 animes y 167 obras en total.", "Ahora lo sé: ciento veinte animes, y ciento sesenta y siete obras en total."),
    ("Comenta tu respuesta 👇", "Comenta tu respuesta."), (FIN, FIN)], [
    ([0, 1], S_options("¿CUÁNTOS ANIMES", "HAS VISTO?", ["MENOS DE 20", "ENTRE 20 Y 50", "MÁS DE 50", "NI IDEA"], 3), 0),
    ([2], S_phone(*INICIO, slide=True), 0),
    ([3], S_phone(*PERFIL, mode="play", rate=0, callout=(0.13, 0.60, "120 ANIMES", (0, 0, 0.3))), 0),
    ([4, 5], S_end("COMENTA TU", "RESPUESTA"), 1.3)])

V["06_un_episodio_al_dia"] = ("chico", "n6", [
    ("Si ves un solo episodio de anime al día, en un año son 365 episodios.", "Si ves un solo episodio de anime al día, en un año son trescientos sesenta y cinco episodios."),
    ("Unas 146 horas. Seis días enteros de tu vida.", "Unas ciento cuarenta y seis horas. Seis días enteros de tu vida."),
    ("La pregunta es: ¿sabrías decir qué viste?", "La pregunta es: ¿sabrías decir qué viste?"),
    ("Yo sí, porque lo tengo todo en Manga Tracker: lo que veo, lo que he terminado y lo que tengo pendiente.", "Yo sí, porque lo tengo todo en Manga Tracker: lo que veo, lo que he terminado, y lo que tengo pendiente."),
    ("¿Cuántos episodios llevas este año?", "¿Cuántos episodios llevas este año?"), (FIN, FIN)], [
    ([0], S_grid(365, 20, "EPISODIOS EN 1 AÑO", fill_d=3.2, top=620), 0),
    ([1], S_counter(None, "1 EPISODIO AL DÍA =", None, 146, "HORAS", sub="6 DÍAS ENTEROS", sub_at=(0, 0, 0.55), count_d=1.3), 0),
    ([2], S_text([("¿SABRÍAS", 140, WHITE), ("DECIR QUÉ", 140, WHITE), ("VISTE?", 190, YEL)], y=760), 0),
    ([3], S_phone(*ESTADOS, mode="play", rate=0, slide=True, callout=(0.80, 0.388, "100 TERMINADOS", (0, 0, 0.6))), 0),
    ([4, 5], S_end("¿CUÁNTOS LLEVAS", "ESTE AÑO?"), 1.3)])

V["07_que_me_recomiendas"] = ("chica", "n7", [
    ("Cuando alguien te pregunta qué anime le recomiendas…", "Cuando alguien te pregunta qué anime le recomiendas…"),
    ("…y tu cerebro se queda en blanco.", "y tu cerebro se queda en blanco."),
    ("Ahora tengo mis listas en Manga Tracker: mi top tier, mis romances, todo.", "Ahora tengo mis listas en Manga Tracker: mi top tier, mis romances, todo."),
    ("Y encima puedo cotillear las estadísticas de mis amigos.", "Y encima puedo cotillear las estadísticas de mis amigos."),
    ("¿Qué anime recomendarías tú?", "¿Qué anime recomendarías tú?"), (FIN, FIN)], [
    ([0], S_chat([("in", "oye, ¿me recomiendas algún anime?", 0.3), ("in", "uno bueno porfa", (0, 0, 0.55)), ("out", "...", (0, 0, 0.9))], title="CUANDO TE PREGUNTAN..."), 0),
    ([1], S_text([("...", 100, WHITE)], [("TU CEREBRO:", 120, WHITE), ("EN BLANCO", 170, YEL)], switch=(0, -0.05),
                 bubbles=[("EH...", 230, 420, -8), ("ESE DE...", 820, 520, 7), ("¿CÓMO SE LLAMABA?", 520, 1320, 3)]), 0),
    ([2], S_phone(*LISTAS, slide=True), 0),
    ([3], S_phone(*AMIGO), 0),
    ([4, 5], S_end("¿QUÉ ANIME", "RECOMIENDAS TÚ?"), 1.3)])

V["08_temporadas_estrenos"] = ("chico", "n8", [
    ("Cada año hay cuatro temporadas de anime, y en cada una salen decenas de series nuevas.", "Cada año hay cuatro temporadas de anime, y en cada una salen decenas de series nuevas."),
    ("Y siempre te enteras tarde del que estaba bueno.", "Y siempre te enteras tarde del que estaba bueno."),
    ("Yo miro los próximos estrenos en Manga Tracker,", "Yo miro los próximos estrenos en Manga Tracker,"),
    ("y los guardo en mi lista antes de que salgan.", "y los guardo en mi lista antes de que salgan."),
    ("¿Qué estreno estás esperando?", "¿Qué estreno estás esperando?"), (FIN, FIN)], [
    ([0], S_quad("4 TEMPORADAS AL AÑO", [("INVIERNO", (60, 110, 220)), ("PRIMAVERA", (220, 90, 160)), ("VERANO", (240, 150, 30)), ("OTOÑO", (180, 70, 40))],
                 [0.1, 0.35, 0.6, 0.85]), 0),
    ([1], S_text([("Y TE ENTERAS", 120, WHITE), ("TARDE", 220, YEL)], bubbles=[("¿YA VA POR EL EP. 8?", 540, 420, -4), ("¡NO ME SPOILEES!", 300, 1330, 6), ("¿CUÁNDO SALIÓ?", 800, 1450, -6)],
                 after=[("Y TE ENTERAS", 120, WHITE), ("TARDE", 220, YEL)], switch=(0, -0.05), y=800), 0),
    ([2], S_phone(*ESTRENOS, slide=True), 0),
    ([3], S_phone(*GUARDAR), 0),
    ([4, 5], S_end("¿QUÉ ESTRENO", "ESPERAS?"), 1.3)])

V["09_logros"] = ("chica", "n2", [
    ("Ver anime ya da logros. Literal.", "Ver anime ya da logros. Literal."),
    ("Otaku iniciado, veterano, leyenda… cada medalla se desbloquea según lo que ves, lo que lees y tus amigos.", "Otaku iniciado, veterano, leyenda… cada medalla se desbloquea según lo que ves, lo que lees, y tus amigos."),
    ("Yo llevo 10 de 12. Me faltan Popular y Maestro Absoluto.", "Yo llevo diez de doce. Me faltan Popular, y Maestro Absoluto."),
    ("¿Cuántas sacarías tú?", "¿Cuántas sacarías tú?"), (FIN, FIN)], [
    ([0, 1], S_cards("LOGRO DESBLOQUEADO", [("OTAKU INICIADO", (205, 127, 50), "LOGRO DESBLOQUEADO", "1"), ("VETERANO", (230, 180, 40), "LOGRO DESBLOQUEADO", "2"),
                                            ("LEYENDA", MO, "LOGRO DESBLOQUEADO", "3"), ("MAESTRO ABSOLUTO", (90, 90, 110), "BLOQUEADO", "?")],
                     [0.2, (1, 0), (1, 0, 0.12), (1, 0, 0.3)], head_col=(205, 127, 50)), 0),
    ([2], S_phone(*MEDALLAS, mode="play", rate=0, slide=True, callout=(0.875, 0.182, "10 / 12", (0, 0, 0.25))), 0),
    ([3, 4], S_end("¿CUÁNTAS", "SACARÍAS TÚ?"), 1.3)])

V["10_dos_tipos"] = ("chico", "n1", [
    ("Hay dos tipos de personas que ven anime.", "Hay dos tipos de personas que ven anime."),
    ("Las que saben exactamente por qué episodio van…", "Las que saben exactamente por qué episodio van…"),
    ("…y las que empiezan la temporada otra vez porque no se acuerdan.", "y las que empiezan la temporada otra vez, porque no se acuerdan."),
    ("Yo era del segundo grupo. Hasta que me bajé Manga Tracker.", "Yo era del segundo grupo. Hasta que me bajé Manga Tracker."),
    ("Ahora cada serie me dice el episodio exacto en el que me quedé.", "Ahora cada serie me dice el episodio exacto en el que me quedé."),
    ("¿Tú de cuál eres, A o B?", "¿Tú de cuál eres? ¿A, o B?"), (FIN, FIN)], [
    ([0, 1, 2], S_versus("TIPO A", "TIPO B", ["SABE", "POR QUÉ", "EPISODIO VA"], ["EMPIEZA", "LA TEMPORADA", "OTRA VEZ"], (1, 0), (2, 0)), 0),
    ([3], S_phone(*MI_LISTA, slide=True), 0),
    ([4], S_phone(90.5, 90.6, mode="play", rate=0, callout=(0.09, 0.594, "VOY POR EL 7", (0, 0, 0.6))), 0),
    ([5, 6], S_end("¿TÚ ERES", "A O B?"), 1.3)])


# ---------------- segunda tanda (11–20) ----------------
FICHA = (97.3, 97.4); A_TOP = (98.0, 99.8); BUSCAR = (47.5, 47.6); COMEDIA = (32.0, 38.0); AMIGO_FIJO = (121.8, 121.9)

V["11_elegir_que_ver"] = ("chica", "n3", [
    ("Si tardas 15 minutos al día en elegir qué ver, al año son más de 90 horas.", "Si tardas quince minutos al día en elegir qué ver, al año son más de noventa horas."),
    ("Literalmente pasas más tiempo eligiendo que viendo.", "Literalmente pasas más tiempo eligiendo que viendo."),
    ("Yo ahora filtro por género en Manga Tracker,", "Yo ahora filtro por género en Manga Tracker,"),
    ("y en segundos tengo todos los animes de comedia, con su nota.", "y en segundos tengo todos los animes de comedia, con su nota."),
    ("¿Cuánto tardas tú en elegir?", "¿Cuánto tardas tú en elegir?"), (FIN, FIN)], [
    ([0], S_counter("15 MIN AL DÍA", "ELIGIENDO QUÉ VER =", None, 91, "HORAS AL AÑO", count_d=1.5), 0),
    ([1], S_text([("MÁS TIEMPO", 130, WHITE), ("ELIGIENDO", 170, YEL), ("QUE VIENDO", 130, WHITE)], [("MÁS TIEMPO", 130, WHITE), ("ELIGIENDO", 170, YEL), ("QUE VIENDO", 130, WHITE)],
                 switch=(0, -0.05), bubbles=[("¿Y ESTE?", 240, 430, -6), ("NAH...", 830, 520, 8), ("¿ESTE OTRO?", 300, 1350, 5), ("MEJOR MAÑANA", 780, 1470, -5)], y=820), 0),
    ([2], S_phone(*FILTROS, slide=True), 0),
    ([3], S_phone(*COMEDIA), 0),
    ([4, 5], S_end("¿CUÁNTO TARDAS", "EN ELEGIR?"), 1.3)])

V["12_red_flags"] = ("chico", "n4", [
    ("Red flags de un otaku.", "Red flags de un otaku."),
    ("Uno: dice que ha visto 'como 50' y no tiene ni idea. Dos: no sabe por qué episodio va. Tres: no tiene un top tier.", "Uno: dice que ha visto, como cincuenta, y no tiene ni idea. Dos: no sabe por qué episodio va. Tres: no tiene un top tier."),
    ("Si tienes las tres, tranquilo: tiene arreglo.", "Si tienes las tres, tranquilo: tiene arreglo."),
    ("En Manga Tracker sabes cuántas obras llevas exactas,", "En Manga Tracker sabes cuántas obras llevas exactas,"),
    ("y te haces tus propias listas, públicas o privadas.", "y te haces tus propias listas, públicas o privadas."),
    ("¿Cuál es tu red flag?", "¿Cuál es tu red flag?"), (FIN, FIN)], [
    ([0, 1], S_cards("RED FLAGS DE UN OTAKU", [("'HE VISTO COMO 50'", RO, "Y NO TIENE NI IDEA", "1"), ("NO SABE POR QUÉ EPISODIO VA", RO, "EMPIEZA OTRA VEZ", "2"), ("NO TIENE TOP TIER", RO, "NI LISTA NI NADA", "3")],
                     [(1, 0), (1, 0, 0.36), (1, 0, 0.7)], head_col=RO, bg="r"), 0),
    ([2], S_text([("TRANQUILO:", 120, WHITE), ("TIENE", 140, WHITE), ("ARREGLO", 200, YEL)], y=780), 0),
    ([3], S_phone(*PERFIL, mode="play", rate=0, slide=True, callout=(0.22, 0.487, "167 EXACTAS", (0, 0, 0.6))), 0),
    ([4], S_phone(*LISTAS), 0),
    ([5, 6], S_end("¿CUÁL ES TU", "RED FLAG?"), 1.3)])

V["13_isekai"] = ("chica", "n5", [
    ("Si un anime empieza con un camión, ya sabes lo que viene.", "Si un anime empieza con un camión, ya sabes lo que viene."),
    ("Reencarna en otro mundo, es el más fuerte, y tiene un menú como de videojuego.", "Reencarna en otro mundo, es el más fuerte, y tiene un menú como de videojuego."),
    ("Y lo peor es que te encanta.", "Y lo peor es que te encanta."),
    ("Si eres de isekai, en Manga Tracker los filtras todos de golpe.", "Si eres de isekai, en Manga Tracker los filtras todos de golpe."),
    ("¿Cuál es tu isekai favorito?", "¿Cuál es tu isekai favorito?"), (FIN, FIN)], [
    ([0], S_text([("SI EMPIEZA", 120, WHITE), ("CON UN", 120, WHITE), ("CAMIÓN...", 200, YEL)], y=760), 0),
    ([1], S_cards("ISEKAI EN 3 PASOS", [("REENCARNA EN OTRO MUNDO", AZ, None, "1"), ("ES EL MÁS FUERTE", MO, None, "2"), ("MENÚ DE VIDEOJUEGO", AM, None, "3")],
                  [(0, 0), (0, 0, 0.42), (0, 0, 0.7)]), 0),
    ([2], S_text([("Y LO PEOR:", 120, WHITE), ("TE ENCANTA", 190, YEL)], y=860), 0),
    ([3], S_phone(*FILTROS, slide=True, callout=(0.32, 0.589, "ISEKAI", (0, 0, 0.45))), 0),
    ([4, 5], S_end("¿TU ISEKAI", "FAVORITO?"), 1.3)])

V["14_top3_3_segundos"] = ("chico", "n6", [
    ("Tienes tres segundos. Dime tu top 3 de anime.", "Tienes tres segundos. Dime tu top tres de anime."),
    ("¿A que el tercero te ha costado?", "¿A que el tercero te ha costado?"),
    ("Por eso yo tengo mi top tier guardado en Manga Tracker,", "Por eso yo tengo mi top tier guardado en Manga Tracker,"),
    ("y cada vez que acabo uno bueno, lo añado en un toque.", "y cada vez que acabo uno bueno, lo añado en un toque."),
    ("Escribe tu top 3 👇", "Escribe tu top tres."), (FIN, FIN)], [
    ([0], S_countdown("TU TOP 3 DE ANIME EN..."), 0.9),
    ([1], S_text([("¿A QUE EL", 120, WHITE), ("TERCERO", 200, YEL), ("TE HA COSTADO?", 110, WHITE)], y=780), 0),
    ([2], S_phone(*LISTAS, slide=True), 0),
    ([3], S_phone(*A_TOP), 0),
    ([4, 5], S_end("ESCRIBE", "TU TOP 3"), 1.3)])

V["15_que_dice_tu_lista"] = ("chica", "n7", [
    ("Tu lista de anime dice mucho de ti.", "Tu lista de anime dice mucho de ti."),
    ("Muchos en pausa: te cuesta decidirte. Muchos abandonados: eres exigente. Muchos pendientes: eres un optimista.", "Muchos en pausa: te cuesta decidirte. Muchos abandonados: eres exigente. Muchos pendientes: eres un optimista."),
    ("La mía tiene 28 en pausa… sin comentarios.", "La mía tiene veintiocho en pausa… sin comentarios."),
    ("¿Y la tuya qué dice?", "¿Y la tuya qué dice?"), (FIN, FIN)], [
    ([0], S_text([("TU LISTA", 150, WHITE), ("DICE MUCHO", 130, YEL), ("DE TI", 150, WHITE)], y=760), 0),
    ([1], S_cards("¿QUÉ DICE DE TI?", [("MUCHOS EN PAUSA", AM, "TE CUESTA DECIDIRTE", "?"), ("MUCHOS ABANDONADOS", RO, "ERES EXIGENTE", "!"), ("MUCHOS PENDIENTES", AZ, "ERES UN OPTIMISTA", "+")],
                  [(0, 0), (0, 0, 0.34), (0, 0, 0.68)]), 0),
    ([2], S_phone(*ESTADOS, mode="play", rate=0, slide=True, callout=(0.80, 0.452, "28 EN PAUSA", (0, 0, 0.3))), 0),
    ([3, 4], S_end("¿Y LA TUYA", "QUÉ DICE?"), 1.3)])

V["16_novelas_ligeras"] = ("chico", "n8", [
    ("Muchos animes empiezan siendo una novela ligera.", "Muchos animes empiezan siendo una novela ligera."),
    ("Sword Art Online, Re:Zero o Konosuba, por ejemplo.", "Sord Art Online, Re Cero, o Konosuba, por ejemplo."),
    ("Y si lees la novela, puedes ir muy por delante del anime.", "Y si lees la novela, puedes ir muy por delante del anime."),
    ("En Manga Tracker también puedes llevar tus novelas, junto al anime, el manga y el manhwa.", "En Manga Tracker también puedes llevar tus novelas, junto al anime, el manga y el manhwa."),
    ("¿Lees novelas ligeras?", "¿Lees novelas ligeras?"), (FIN, FIN)], [
    ([0], S_text([("MUCHOS ANIMES", 110, WHITE), ("EMPIEZAN COMO", 110, WHITE), ("NOVELA LIGERA", 160, YEL)], y=760), 0),
    ([1], S_cards("EMPEZARON SIENDO NOVELA", [("SWORD ART ONLINE", AZ, None, "1"), ("RE:ZERO", MO, None, "2"), ("KONOSUBA", AM, None, "3")], [(0, 0), (0, 0, 0.42), (0, 0, 0.62)]), 0),
    ([2], S_text([("PUEDES IR", 130, WHITE), ("MUY POR DELANTE", 140, YEL), ("DEL ANIME", 130, WHITE)], y=780), 0),
    ([3], S_phone(*BUSCAR, mode="play", rate=0, slide=True, callout=(0.87, 0.165, "NOVELAS", (0, 0, 0.3))), 0),
    ([4, 5], S_end("¿LEES NOVELAS", "LIGERAS?"), 1.3)])

V["17_antes_ahora"] = ("chica", "n1", [
    ("Cómo llevaba mis animes antes y cómo los llevo ahora.", "Cómo llevaba mis animes antes, y cómo los llevo ahora."),
    ("Antes: notas del móvil, capturas de pantalla y mi memoria, que no sirve para nada.", "Antes: notas del móvil, capturas de pantalla, y mi memoria, que no sirve para nada."),
    ("Ahora: todo en Manga Tracker.", "Ahora: todo en Manga Tracker."),
    ("Lo que veo, lo que tengo pendiente y por qué episodio voy.", "Lo que veo, lo que tengo pendiente, y por qué episodio voy."),
    ("¿Tú cómo lo llevas?", "¿Tú cómo lo llevas?"), (FIN, FIN)], [
    ([0, 1, 2], S_versus("ANTES", "AHORA", ["NOTAS", "CAPTURAS", "MI MEMORIA"], ["MANGA", "TRACKER", "Y LISTO"], (1, 0), (2, 0)), 0),
    ([3], S_phone(*MI_LISTA, slide=True), 0),
    ([4, 5], S_end("¿TÚ CÓMO", "LO LLEVAS?"), 1.3)])

V["18_amigos_quien_mas"] = ("chico", "n2", [
    ("Todo grupo de amigos tiene esta discusión.", "Todo grupo de amigos tiene esta discusión."),
    ("Mi amigo decía que había visto más anime que yo.", "Mi amigo decía que había visto más anime que yo."),
    ("Así que le miré el perfil en Manga Tracker: 72 obras.", "Así que le miré el perfil en Manga Tracker: setenta y dos obras."),
    ("Yo, 167. Fin de la discusión.", "Yo, ciento sesenta y siete. Fin de la discusión."),
    ("Etiqueta a ese amigo 👇", "Etiqueta a ese amigo."), (FIN, FIN)], [
    ([0, 1], S_chat([("in", "yo he visto más anime que tú", 0.4), ("out", "jajaja ni de broma", (0, 0, 0.75)), ("in", "demuéstralo", (1, 0)), ("out", "...", (1, 0, 0.6))], title="EL GRUPO DE AMIGOS"), 0),
    ([2], S_phone(*AMIGO_FIJO, mode="play", rate=0, slide=True, callout=(0.18, 0.255, "72 OBRAS", (0, 0, 0.7))), 0),
    ([3], S_phone(*PERFIL, mode="play", rate=0, callout=(0.22, 0.487, "167", (0, 0.2))), 0),
    ([4, 5], S_end("ETIQUETA A", "ESE AMIGO"), 1.3)])

V["19_diez_mil_horas"] = ("chica", "n4", [
    ("Dicen que con 10.000 horas te vuelves experto en algo.", "Dicen que con diez mil horas te vuelves experto en algo."),
    ("En anime, eso son unos 25.000 episodios.", "En anime, eso son unos veinticinco mil episodios."),
    ("Yo voy por 120 animes… y aún me falta la medalla de Maestro Absoluto.", "Yo voy por ciento veinte animes… y aún me falta la medalla de Maestro Absoluto."),
    ("¿Cuánto te falta a ti?", "¿Cuánto te falta a ti?"), (FIN, FIN)], [
    ([0], S_counter("DICEN QUE...", "PARA SER EXPERTO", None, 10000, "HORAS", count_d=1.6), 0),
    ([1], S_counter(None, "EN ANIME SON", None, 25000, "EPISODIOS", count_d=1.2), 0),
    ([2], S_phone(*MEDALLAS, mode="play", rate=0, slide=True, callout=(0.83, 0.56, "ME FALTA", (0, 0, 0.6))), 0),
    ([3, 4], S_end("¿CUÁNTO TE", "FALTA A TI?"), 1.3)])

V["20_temporada_en_una_tarde"] = ("chico", "n7", [
    ("Una temporada de anime suele tener 12 episodios.", "Una temporada de anime suele tener doce episodios."),
    ("Unas cinco horas: te la ventilas en una tarde.", "Unas cinco horas: te la ventilas en una tarde."),
    ("Yo miro cuántos episodios tiene en Manga Tracker,", "Yo miro cuántos episodios tiene en Manga Tracker,"),
    ("y si me gusta, la meto directa en mi top tier.", "y si me gusta, la meto directa en mi top tier."),
    ("¿Cuál te viste en una tarde?", "¿Cuál te viste en una tarde?"), (FIN, FIN)], [
    ([0], S_grid(12, 4, "EPISODIOS POR TEMPORADA", fill_d=1.4, top=640, gap=30), 0),
    ([1], S_counter(None, "12 EPISODIOS =", None, 5, "HORAS", sub="UNA TARDE", sub_at=(0, 0, 0.6), count_d=1.0), 0),
    ([2], S_phone(*FICHA, mode="play", rate=0, slide=True, callout=(0.75, 0.316, "12 EP.", (0, 0, 0.55))), 0),
    ([3], S_phone(*A_TOP), 0),
    ([4, 5], S_end("¿CUÁL TE VISTE", "EN UNA TARDE?"), 1.3)])

if __name__ == "__main__":
    args = sys.argv[1:]; chk = "chk" in args; names = [a for a in args if a != "chk"]
    for key, (voz0, mus, lines, scenes) in V.items():
        tema = key[3:]
        if names and tema not in names and key not in names: continue
        for voz in (voz0, "chico" if voz0 == "chica" else "chica"):
            n = f"{LOTE}_{tema}_{voz}"
            if not chk and os.path.exists(f"{OUT}/{n}.mp4"): continue
            if chk:
                fr = [(si, 0.6) for si in range(len(scenes))] + [(si, 2.4) for si in range(len(scenes))]
                print(render(n, voz, mus, lines, scenes, OUT, frames=fr), flush=True); break
            print(render(n, voz, mus, lines, scenes, OUT), flush=True)
