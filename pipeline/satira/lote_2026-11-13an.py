# Lote "todo animado" del 13/11/2026: 10 temas nuevos, el chico de cuerpo entero actúa cada frase.
# Voces: chico 1 (st5) en todos; chica alterna chica 1 (st0) / chica 5 (st4). Música lo-fi original distinta por vídeo.
# Uso: python3 pipeline/satira/lote_2026-11-13an.py [chk] [tema ...] [chico|chica]
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["SRC_VIDEO"] = os.path.abspath(os.path.join(HERE, "..", "..", "procesadas", "grabacion_2026-11-02.mp4"))
sys.path.insert(0, HERE)
from animado import *
import voz_viva
voz_viva.patch(M)
M.SUBS += [("Golgo 13", "Gólgo trece"), ("Guinness", "Guines"), ("Star Wars", "Estar Guors"), ("Marvel", "Márvel"), ("Harry Potter", "Jari Póter"),
           ("Pokémon", "Pokemon"), ("Ghibli", "Guibli"), ("Hayao Miyazaki", "Jayao Miyazaki"), ("mangaka", "mangaka"), ("openings", "ópenings"), ("opening", "ópening")]
ES.VOICE_CHAIN = "highpass=f=75,equalizer=f=3000:t=q:w=1.4:g=1.2,acompressor=threshold=0.15:ratio=2:attack=10:release=150,"
ES.MUSIC_VOL = 0.2
LOTE = "2026-11-13an"
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "videos"))
FIN = "Manga Tracker. ¡Gratis en Play Store!"
MI_LISTA = (90.1, 92.6); EPIS = (62.0, 66.0); PERFIL = (127.75, 127.85); LISTAS = (105.0, 108.2); MEDALLAS = (131.0, 131.1)
O = ("open", "open"); PR = ("fist", "point"); PL = ("point", "fist"); OR_ = ("fist", "open")

V = {}
V["01_dos_oscar_mismo_senor"] = ("st0", "lofi7", "lofi8", [
    ("Solo *2* películas de anime han ganado el *Óscar* de animación.", "Solo dos películas de anime han ganado el Óscar a mejor película de animación."),
    ("¿Y sabes qué? ¡Las dos son del *mismo señor*!", "¿Y sabes qué? ¡Las dos son del mismo señor!"),
    ("*Hayao Miyazaki*: en 2003… y otra vez en 2024.", "Hayao Miyazaki: en dos mil tres… y otra vez en dos mil veinticuatro."),
    ("¡Con *83 años*!", "¡Con ochenta y tres años!"),
    ("Y tú, con veinte, no te acuerdas de qué viste *el mes pasado*.", "Y tú, con veinte, no te acuerdas de qué viste el mes pasado."),
    ("Apúntalo todo en *Manga Tracker* y monta tu *top* de favoritos.", "Apúntalo todo en Manga Tracker, y monta tu top de favoritos."),
    ("Mándaselo a ese amigo que *aún no ha visto nada de Ghibli*.", "Mándaselo a ese amigo que aún no ha visto nada de Ghibli."), (FIN, FIN)], [
    ([0], A("stage", [K(0.0, "stand", "neutral"), K(q(0, 0.5), "shock", "shock", O)], cx=830, sc=0.8,
            props=[dict(k="icon", img=IC.trofeo(), x=420, y=900, s=0.9, anim="rise"), dict(k="big", txt="SOLO 2", y=560, size=170, t=0.2), dict(k="pill", txt="ÓSCAR DE ANIMACIÓN", y=720, t=q(0, 0.6))]), 0),
    ([1], A("stage", [K(0.0, "point_l", "neutral", PL), K(q(0, 0.6), "shrug", "shock", O)], cx=830, sc=0.8,
            props=[dict(k="icon", img=IC.trofeo(), x=230, y=930, s=0.6), dict(k="icon", img=IC.trofeo(), x=520, y=930, s=0.6, t=0.25), dict(k="stamp", txt="MISMO SEÑOR", t=q(0, 0.62), y=620)]), 0),
    ([2, 3], A("stage", [K(0.0, "present", "proud", OR_), K(q(1), "arms_up", "happy", O)],
               props=[dict(k="calendar", seq=["2003", "2024"], x=540, y=680, t=0.1, t_end=(0, 0, 0.75), t_out=q(1)), dict(k="big", txt="83 AÑOS", y=640, size=190, t=q(1)), dict(k="rain", kind="confetti", t=q(1))]), 0),
    ([4], A("room", [K(0.0, "scratch", "confused")], props=[dict(k="calendar", seq=["¿MES PASADO?"], x=540, y=640, s=1.2, t=0.1)], fx=[dict(k="qmarks", t=q(0, 0.35))]), 0),
    ([5], A_app(*LISTAS, callout=(0.35, 0.215, "TU TOP", q(0, 0.5))), 0),
    ([6], A_send("gold"), 0), ([7], A_fin(), 1.4)])

V["02_manga_desde_1968"] = ("st4", "lofi9", "lofi10", [
    ("Hay un manga que se publica desde *1968*…", "Hay un manga que se publica desde mil novecientos sesenta y ocho…"),
    ("Su autor falleció en 2021… ¡y el manga *sigue saliendo*!", "Su autor falleció en dos mil veintiuno… ¡y el manga sigue saliendo!"),
    ("Lo continúa su equipo. Ya va por más de *220 tomos*.", "Lo continúa su equipo. Ya va por más de doscientos veinte tomos."),
    ("*Récord Guinness* incluido. Se llama Golgo 13.", "Récord Guinness incluido. Se llama Golgo 13."),
    ("Y tú no eres capaz de terminar *un manga de 10 tomos*.", "Y tú no eres capaz de terminar un manga de diez tomos."),
    ("Con *Manga Tracker* sabes por dónde vas… y lo terminas *de una vez*.", "Con Manga Tracker sabes por dónde vas… y lo terminas de una vez."),
    ("Mándaselo a ese que deja *todos los mangas a medias*.", "Mándaselo a ese que deja todos los mangas a medias."), (FIN, FIN)], [
    ([0], A("room", [K(0.0, "stand"), K(q(0, 0.45), "shock", "shock", O)], cx=780, sc=0.85,
            props=[dict(k="calendar", seq=["1968"], x=330, y=760, s=1.3, t=0.05), dict(k="big", txt="DESDE 1968", y=530, size=150, t=q(0, 0.4))]), 0),
    ([1], A("room", [K(0.0, "bow", "neutral"), K(q(0, 0.6), "point_l", "shock", PL)], cx=780, sc=0.85,
            props=[dict(k="calendar", seq=["2021"], x=330, y=760, s=1.3), dict(k="stamp", txt="SIGUE SALIENDO", col=GREEN, t=q(0, 0.62), y=560)]), 0),
    ([2, 3], A("room", [K(0.0, "point_l", "proud", PL), K(q(1), "clap", "happy")], cx=820, sc=0.8,
               props=[dict(k="books", n=44, x=330, y=1780, dur=2.0, t=0.0), dict(k="counter", a=0, b=220, pre="+", suf=" TOMOS", y=520, dur=1.6), dict(k="icon", img=IC.trofeo(), x=820, y=760, s=0.45, t=q(1))]), 0),
    ([4], A("room", [K(0.0, "sit", "confused"), K(q(0, 0.6), "sit_wait", "tired")], cx=760,
            props=[dict(k="books", n=10, x=290, y=1780, dur=0.5), dict(k="stamp", txt="A MEDIAS", t=q(0, 0.65), y=700)], fx=[dict(k="qmarks", t=q(0, 0.2), t_out=q(0, 0.65))]), 0),
    ([5], A_app(*MI_LISTA, callout=(0.13, 0.334, "POR DÓNDE VAS", q(0, 0.5))), 0),
    ([6], A_send("red"), 0), ([7], A_fin(), 1.4)])

V["03_franquicia_mas_rica"] = ("st0", "lofi11", "lofi12", [
    ("La franquicia que *más dinero* ha generado en la historia… no es Star Wars.", "La franquicia que más dinero ha generado en la historia… no es Star Wars."),
    ("Ni Marvel. Ni Harry Potter.", "Ni Marvel. Ni Harry Potter."),
    ("¡Es *Pokémon*! Se calcula que más de *90.000 millones de dólares*.", "¡Es Pokémon! Se calcula que más de noventa mil millones de dólares."),
    ("Y todo empezó en 1996… con un *videojuego*.", "Y todo empezó en mil novecientos noventa y seis… con un videojuego."),
    ("Mientras tanto tú no sabes ni *cuántos animes* has visto este año.", "Mientras tanto tú no sabes ni cuántos animes has visto este año."),
    ("En *Manga Tracker* lo ves en tus estadísticas, *al momento*.", "En Manga Tracker lo ves en tus estadísticas, al momento."),
    ("Mándaselo al que dice que Pokémon es *para niños*.", "Mándaselo al que dice que Pokémon es para niños."), (FIN, FIN)], [
    ([0], A("stage", [K(0.0, "finger_up", "smug", PR), K(q(0, 0.7), "shrug", "neutral", O)],
            props=[dict(k="big", txt="¿STAR WARS?", y=600, size=130, t=0.3), dict(k="stamp", txt="NO", t=q(0, 0.78), y=600)]), 0),
    ([1], A("stage", [K(0.0, ("shrug", dict(head=-10)), "smug", O), K(q(0, 0.5), ("shrug", dict(head=10)), "smug", O)],
            props=[dict(k="big", txt="¿MARVEL?", y=520, size=110, t=0.0), dict(k="big", txt="¿HARRY POTTER?", y=680, size=110, t=q(0, 0.45)), dict(k="stamp", txt="TAMPOCO", t=q(0, 0.8), y=860)]), 0),
    ([2], A("rays:gold", [K(0.0, "arms_up", "happy", O)], props=[dict(k="rain", kind="money", t=0.1), dict(k="counter", a=0, b=90000, pre="+", suf=" M $", y=600, dur=1.6, t=q(0, 0.35))]), 0),
    ([3], A("room", [K(0.0, "point_l", "proud", PL)], cx=800, sc=0.85, props=[dict(k="icon", img=IC.tele("1996", "VIDEOJUEGO"), x=330, y=900, s=0.8, anim="slide_l")]), 0),
    ([4], A("room", [K(0.0, "scratch", "confused")], props=[dict(k="big", txt="¿CUÁNTOS ESTE AÑO?", y=640, size=100, t=0.2)], fx=[dict(k="qmarks", t=q(0, 0.4))]), 0),
    ([5], A_app(*PERFIL, mode="still", callout=(0.22, 0.487, "TUS ESTADÍSTICAS", q(0, 0.5))), 0),
    ([6], A_send("gold"), 0), ([7], A_fin(), 1.4)])

V["04_otaku_tu_casa"] = ("st4", "lofi13", "lofi14", [
    ("La palabra *otaku* significa, literalmente… *tu casa*.", "La palabra otaku significa, literalmente… tu casa."),
    ("Era una forma *muy educada* de decir «usted» en japonés.", "Era una forma muy educada de decir, usted, en japonés."),
    ("Y acabó siendo el nombre de los fans que *no salen de casa*.", "Y acabó siendo el nombre de los fans que no salen de casa."),
    ("Que, siendo sinceros… *tiene sentido*.", "Que, siendo sinceros… tiene sentido."),
    ("Si te quedas en casa viendo anime, al menos organízalo en *Manga Tracker*.", "Si te quedas en casa viendo anime, al menos organízalo en Manga Tracker."),
    ("Mándaselo a tu amigo más *otaku*. Ya sabes cuál.", "Mándaselo a tu amigo más otaku. Ya sabes cuál."), (FIN, FIN)], [
    ([0], A("street", [K(0.0, "stand", "neutral"), K(q(0, 0.55), "point_l", "shock", PL)], cx=800, sc=0.85,
            props=[dict(k="icon", img=casa(), x=320, y=1100, s=0.8, anim="pop", t=q(0, 0.5)), dict(k="big", txt="OTAKU =", y=500, size=140, t=0.1, col=WHITE), dict(k="big", txt="TU CASA", y=660, size=170, t=q(0, 0.6))]), 0),
    ([1], A("room", [K(0.0, "bow", "happy")], props=[dict(k="pill", txt="«USTED», MUY EDUCADO", y=620, t=0.2)], fx=[dict(k="sparkle", t=0.2)]), 0),
    ([2], A("room", [K(0.0, "sit_phone", "smug", phone="r")], foot=1700, props=[dict(k="sofa"), dict(k="stamp", txt="SIN SALIR", t=q(0, 0.6), y=640)]), 0),
    ([3], A("room", [K(0.0, "shrug", "happy", O)], props=[dict(k="stamp", txt="TIENE SENTIDO", col=GREEN, t=q(0, 0.4), y=640)]), 0),
    ([4], A_app(*MI_LISTA, callout=(0.13, 0.334, "VIENDO", q(0, 0.5))), 0),
    ([5], A_send("pink"), 0), ([6], A_fin(), 1.4)])

V["05_primer_anime_1917"] = ("st0", "lofi15", "lofi16", [
    ("El primer anime de la historia tiene *más de 100 años*.", "El primer anime de la historia tiene más de cien años."),
    ("Es de *1917*. Seguramente ni tus abuelos habían nacido.", "Es de mil novecientos diecisiete. Seguramente ni tus abuelos habían nacido."),
    ("Duraba unos *pocos minutos*… y se dibujaba *a mano*, dibujo a dibujo.", "Duraba unos pocos minutos… y se dibujaba a mano, dibujo a dibujo."),
    ("Hoy hay *miles* de animes.", "Hoy hay miles de animes."),
    ("Imposible acordarte de *todos los que has visto*… si no los apuntas.", "Imposible acordarte de todos los que has visto… si no los apuntas."),
    ("Para eso está *Manga Tracker*.", "Para eso está Manga Tracker."),
    ("Mándaselo a ese que dice que el anime *es una moda*.", "Mándaselo a ese que dice que el anime es una moda."), (FIN, FIN)], [
    ([0], A("room", [K(0.0, "stand"), K(q(0, 0.5), "shock", "shock", O)], cx=780, sc=0.85,
            props=[dict(k="counter", a=0, b=100, pre="+", suf=" AÑOS", y=520, dur=1.2, t=0.1), dict(k="icon", img=IC.reloj_arena(), x=300, y=980, s=0.6)]), 0),
    ([1], A("room", [K(0.0, "point_l", "proud", PL)], cx=780, sc=0.85, props=[dict(k="calendar", seq=["1917"], x=320, y=820, s=1.3), dict(k="stamp", txt="NI TUS ABUELOS", t=q(0, 0.55), y=560)]), 0),
    ([2], A("room", [K(0.0, "write", "neutral")], foot=1760, props=[dict(k="desk"), dict(k="icon", img=IC.lapiz_moneda(), x=840, y=820, s=0.4), dict(k="pill", txt="DIBUJO A DIBUJO", y=600, t=q(0, 0.5))]), 0),
    ([3], A("room", [K(0.0, "shock", "shock", O)], props=[dict(k="rain", kind="cards", t=0.0), dict(k="big", txt="MILES", y=620, size=200, t=0.1)]), 0),
    ([4], A("room", [K(0.0, "scratch", "confused")], fx=[dict(k="qmarks", t=q(0, 0.3))]), 0),
    ([5], A_app(*PERFIL, mode="still", callout=(0.22, 0.487, "167 OBRAS", q(0, 0.4))), 0),
    ([6], A_send("blue"), 0), ([7], A_fin(), 1.4)])

V["06_revista_6_millones"] = ("st4", "lofi17", "lofi18", [
    ("Una revista de manga llegó a vender *6,5 millones* de copias… en *una semana*.", "Una revista de manga llegó a vender seis millones y medio de copias… en una semana."),
    ("Fue en 1995. ¡*Récord absoluto*!", "Fue en mil novecientos noventa y cinco. ¡Récord absoluto!"),
    ("Hoy casi todo el mundo lee manga *en el móvil*.", "Hoy casi todo el mundo lee manga en el móvil."),
    ("Y se pierde entre mil capítulos… en *mil webs distintas*.", "Y se pierde entre mil capítulos… en mil webs distintas."),
    ("Con *Manga Tracker* tienes todos tus mangas en *una sola lista*.", "Con Manga Tracker tienes todos tus mangas en una sola lista."),
    ("Mándaselo a ese que lee manga en *cinco apps distintas*.", "Mándaselo a ese que lee manga en cinco apps distintas."), (FIN, FIN)], [
    ([0], A("room", [K(0.0, "point_l", "neutral", PL), K(q(0, 0.6), "shock", "shock", O)], cx=790, sc=0.85,
            props=[dict(k="books", n=40, x=320, y=1780, dur=2.2), dict(k="counter", a=0, b=6.5, fmt="{:.1f}", suf=" MILLONES", y=520, dur=1.6, t=0.2)]), 0),
    ([1], A("stage", [K(0.0, "clap", "happy")], cx=780, sc=0.85, props=[dict(k="calendar", seq=["1995"], x=300, y=800, s=1.2), dict(k="icon", img=IC.trofeo(), x=300, y=1250, s=0.45, t=0.2), dict(k="stamp", txt="RÉCORD", col=YEL, t=q(0, 0.5), y=560)]), 0),
    ([2], A("street", [K(0.0, "phone_stand", "smug", phone="r")]), 0),
    ([3], A("room", [K(0.0, "dizzy", "dizzy", O)], props=[dict(k="phone_tiles")], fx=[dict(k="stars", t=0.3)]), 0),
    ([4], A_app(*MI_LISTA, callout=(0.13, 0.334, "UNA SOLA LISTA", q(0, 0.5))), 0),
    ([5], A_send("purple"), 0), ([6], A_fin(), 1.4)])

V["07_mangaka_20_paginas"] = ("st0", "lofi19", "lofi20", [
    ("Un mangaka de revista semanal dibuja unas *20 páginas*… *cada semana*.", "Un mangaka de revista semanal dibuja unas veinte páginas… cada semana."),
    ("Durante años. A veces durmiendo *muy poco*.", "Durante años. A veces durmiendo muy poco."),
    ("Mientras tanto tú, que solo tienes que *leerlas*…", "Mientras tanto tú, que solo tienes que leerlas…"),
    ("¿Vas al día? ¿Te has quedado atrás? *Ni idea*.", "¿Vas al día? ¿Te has quedado atrás? Ni idea."),
    ("En *Manga Tracker* ves los *capítulos nuevos* y por cuál vas.", "En Manga Tracker ves los capítulos nuevos, y por cuál vas."),
    ("Mándaselo a ese que va *diez capítulos por detrás*.", "Mándaselo a ese que va diez capítulos por detrás."), (FIN, FIN)], [
    ([0], A("room", [K(0.0, "write", "neutral")], foot=1760, props=[dict(k="desk"), dict(k="books", n=20, x=260, y=1420, s=0.7, dur=1.6), dict(k="counter", a=0, b=20, suf=" PÁGINAS", y=520, dur=1.4), dict(k="pill", txt="CADA SEMANA", y=680, t=q(0, 0.6))]), 0),
    ([1], A("bedroom", [K(0.0, "write", "tired")], foot=1760, props=[dict(k="desk"), dict(k="clock", x=820, y=560, r=130, speed=12)], fx=[dict(k="zzz", t=0.3)]), 0),
    ([2], A("room", [K(0.0, "sit_phone", "smug", phone="r")], foot=1700, props=[dict(k="sofa")]), 0),
    ([3], A("room", [K(0.0, ("sit", dict(rhx=-10, rhy=-215, head=6)), "confused")], foot=1700, props=[dict(k="sofa"), dict(k="stamp", txt="NI IDEA", t=q(0, 0.75), y=700)], fx=[dict(k="qmarks", t=0.2, t_out=q(0, 0.75))]), 0),
    ([4], A_app(*EPIS, callout=(0.25, 0.455, "POR CUÁL VAS", q(0, 0.5))), 0),
    ([5], A_send("blue"), 0), ([6], A_fin(), 1.4)])

V["08_openings_90_segundos"] = ("st4", "lofi1", "lofi2", [
    ("Casi todos los openings de anime duran lo mismo: *1 minuto y 30 segundos*.", "Casi todos los openings de anime duran lo mismo: un minuto y treinta segundos."),
    ("Por cómo se reparte el tiempo de cada episodio en la tele japonesa.", "Por cómo se reparte el tiempo de cada episodio en la tele japonesa."),
    ("Y tú te los sabes *todos de memoria*…", "Y tú te los sabes todos de memoria…"),
    ("…pero no te acuerdas de *en qué capítulo ibas*.", "…pero no te acuerdas de en qué capítulo ibas."),
    ("Para eso está *Manga Tracker*: marcas el episodio, y listo.", "Para eso está Manga Tracker: marcas el episodio, y listo."),
    ("Mándaselo a ese que *canta todos los openings*.", "Mándaselo a ese que canta todos los openings."), (FIN, FIN)], [
    ([0], A("room", [K(0.0, "stand"), K(q(0, 0.6), "shock", "shock", O)], props=[dict(k="timer", b=90, y=640, dur=1.8, t=0.1)]), 0),
    ([1], A("room", [K(0.0, "point_l", "proud", PL)], cx=800, sc=0.85, props=[dict(k="tv", mode="anime", label="OP 1:30")]), 0),
    ([2], A("rays:pink", [K(0.0, "arms_up", "happy", O), K(q(0, 0.5), "wave", "happy", OR_)], fx=[dict(k="notes", t=0.0)]), 0),
    ([3], A("room", [K(0.0, "scratch", "confused")], props=[dict(k="stamp", txt="NI IDEA", t=q(0, 0.7), y=640)], fx=[dict(k="qmarks", t=0.1, t_out=q(0, 0.7))]), 0),
    ([4], A_app(*EPIS, callout=(0.25, 0.455, "EPISODIO 7", q(0, 0.5))), 0),
    ([5], A_send("pink"), 0), ([6], A_fin(), 1.4)])

V["09_habito_66_dias"] = ("st0", "lofi3", "lofi4", [
    ("Crear un hábito nuevo tarda, de media, *66 días*.", "Crear un hábito nuevo tarda, de media, sesenta y seis días."),
    ("Lo dice un estudio del *University College de Londres*.", "Lo dice un estudio del University College de Londres."),
    ("Ni 21, como dicen por ahí. *66*.", "Ni veintiuno, como dicen por ahí. Sesenta y seis."),
    ("¿Quieres leer o ver anime cada día? Necesitas *constancia*.", "¿Quieres leer o ver anime cada día? Necesitas constancia."),
    ("En *Manga Tracker* ves tu progreso y ganas *medallas* por el camino.", "En Manga Tracker ves tu progreso, y ganas medallas por el camino."),
    ("Mándaselo a ese que empieza algo *y lo deja a los tres días*.", "Mándaselo a ese que empieza algo, y lo deja a los tres días."), (FIN, FIN)], [
    ([0], A("room", [K(0.0, "present", "proud", OR_)], cx=540, props=[dict(k="grid", n=66, cols=11, y=620, dur=1.8), dict(k="counter", a=0, b=66, suf=" DÍAS", y=520, size=130, dur=1.8)], foot=1880, sc=0.75), 0),
    ([1], A("room", [K(0.0, "point_l", "neutral", PL)], cx=800, sc=0.85, props=[dict(k="icon", img=IC.estudio(), x=320, y=900, s=0.75, anim="pop")]), 0),
    ([2], A("room", [K(0.0, "finger_up", "smug", PR)], props=[dict(k="big", txt="21", y=640, size=200, t=0.0, t_out=q(0, 0.45), col=WHITE), dict(k="stamp", txt="66", col=GREEN, t=q(0, 0.45), y=640, size=180)]), 0),
    ([3], A("room", [K(0.0, "sit_phone", "happy", phone="r")], foot=1700, props=[dict(k="sofa"), dict(k="pill", txt="CADA DÍA", y=640, t=q(0, 0.5))], fx=[dict(k="sparkle", t=q(0, 0.5))]), 0),
    ([4], A_app(*MEDALLAS, mode="still", callout=(0.875, 0.182, "MEDALLAS", q(0, 0.6))), 0),
    ([5], A_send("green"), 0), ([6], A_fin(), 1.4)])

V["10_dormir_6_horas"] = ("st4", "lofi5", "lofi6", [
    ("Si duermes *6 horas* cada noche durante *2 semanas*…", "Si duermes seis horas cada noche durante dos semanas…"),
    ("…tu cerebro rinde como si llevaras *una noche entera sin dormir*.", "…tu cerebro rinde como si llevaras una noche entera sin dormir."),
    ("Lo comprobó un estudio de la *Universidad de Pensilvania*.", "Lo comprobó un estudio de la Universidad de Pensilvania."),
    ("Y tú, a las 3 de la mañana: *solo un capítulo más*.", "Y tú, a las tres de la mañana: solo un capítulo más."),
    ("Al menos con *Manga Tracker* sabes dónde lo dejaste… y te puedes ir a dormir.", "Al menos con Manga Tracker sabes dónde lo dejaste… y te puedes ir a dormir."),
    ("Mándaselo a ese que *nunca se va a dormir*.", "Mándaselo a ese que nunca se va a dormir."), (FIN, FIN)], [
    ([0], A("bedroom", [K(0.0, "stand", "tired")], cx=760, sc=0.85, props=[dict(k="clock", x=300, y=1000, r=150, speed=6), dict(k="big", txt="6 H × 14 DÍAS", y=520, size=130, t=0.2)], fx=[dict(k="zzz", t=0.4)]), 0),
    ([1], A("bedroom", [K(0.0, "dizzy", "dizzy", O)], props=[dict(k="stamp", txt="1 NOCHE SIN DORMIR", t=q(0, 0.6), y=600, size=90)], fx=[dict(k="stars", t=0.2)]), 0),
    ([2], A("room", [K(0.0, "point_l", "neutral", PL)], cx=800, sc=0.85, props=[dict(k="icon", img=IC.estudio(), x=320, y=900, s=0.75)]), 0),
    ([3], A("bedroom", [K(0.0, "sit_bed", "tired", phone="r")], foot=1700, props=[dict(k="bed"), dict(k="icon", img=IC.reloj("3:00"), x=830, y=650, s=0.5), dict(k="pill", txt="SOLO UNO MÁS", y=480, t=q(0, 0.5))]), 0),
    ([4], A_app(*EPIS, callout=(0.25, 0.455, "AQUÍ LO DEJASTE", q(0, 0.5))), 0),
    ([5], A_send("blue"), 0), ([6], A_fin(), 1.4)])

if __name__ == "__main__":
    args = sys.argv[1:]; chk = "chk" in args
    voces = [v for v in ("chico", "chica") if v in args] or ["chico", "chica"]
    names = [a for a in args if a not in ("chk", "chico", "chica")]
    for key, (vchica, mus_o, mus_a, lines, scenes) in V.items():
        tema = key[3:]
        if names and tema not in names and key not in names: continue
        for voz in voces:
            vid, mus = ("st5", mus_o) if voz == "chico" else (vchica, mus_a)
            n = f"{LOTE}_{tema}_{voz}"
            if chk:
                print(render(n, vid, mus, lines, scenes, OUT, frames=[(si, T) for si in range(len(scenes)) for T in (0.4, 2.2)]), flush=True); break
            if os.path.exists(f"{OUT}/{n}.mp4"): continue
            print(render(n, vid, mus, lines, scenes, OUT), flush=True)
