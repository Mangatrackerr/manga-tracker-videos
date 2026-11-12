# Lote "industria" del 12/11/2026 — estilo satírico animado, GANCHO de industria/curiosidad/noticia en los primeros 5 s.
# Voces (Supertonic 3, sin retoque): chico 1 = st5 en todos; chica alterna chica 1 (st0) y chica 5 (st4). Música lo-fi original distinta por vídeo.
# Uso: python3 pipeline/satira/lote_2026-11-12i.py [chk] [tema ...] [chico|chica]
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["SRC_VIDEO"] = os.path.abspath(os.path.join(HERE, "..", "..", "procesadas", "grabacion_2026-11-02.mp4"))
sys.path.insert(0, HERE)
from engine_satira import *
import engine_satira as ES, iconos as IC, voz_viva
voz_viva.patch(M)
M.SUBS += [("Netflix", "Nétflix"), ("IMDb", "I eme de be"), ("Demon Slayer", "Démon Sléyer"), ("Infinity Castle", "Infíniti Cásel"), ("Astro Boy", "Ástro Boi")]
ES.VOICE_CHAIN = "highpass=f=75,equalizer=f=3000:t=q:w=1.4:g=1.2,acompressor=threshold=0.15:ratio=2:attack=10:release=150,"
ES.MUSIC_VOL = 0.2
LOTE = "2026-11-12i"
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "videos"))
FIN = "Manga Tracker. ¡Gratis en Play Store!"
MI_LISTA = (90.1, 92.6); EPIS = (62.0, 66.0); PERFIL = (127.75, 127.85); INICIO = (19.5, 24.0); ESTADOS = (129.5, 129.6); FICHA_NOTA = (14.8, 14.9)
Y1, Y2 = 1450, 1630
q = lambda k, f=0.0: (k, 0, f)

V = {}  # clave: (voz chica, música chico, música chica, líneas, escenas)
V["01_685_ninos_hospital"] = ("st0", "lofi4", "lofi10", [
    ("Un episodio de anime mandó a *685 niños* al hospital. En *una sola noche*.", "Un episodio de anime mandó a seiscientos ochenta y cinco niños al hospital. En una sola noche."),
    ("Japón, 1997: unos destellos de luz… ¡y otros *12.000 niños* tuvieron síntomas en casa!", "Japón, mil novecientos noventa y siete: unos destellos de luz… ¡y otros doce mil niños tuvieron síntomas en casa!"),
    ("La serie desapareció de la tele *4 meses*.", "La serie desapareció de la tele cuatro meses."),
    ("Hoy, por suerte, lo más peligroso de ver anime es otra cosa…", "Hoy, por suerte, lo más peligroso de ver anime es otra cosa…"),
    ("¿Por qué capítulo iba? *Ni idea*.", "¿Por qué capítulo iba? Ni idea."),
    ("Para eso está *Manga Tracker*: marcas el episodio y *listo*.", "Para eso está Manga Tracker: marcas el episodio, y listo."),
    ("Mándaselo a ese amigo que *siempre se pierde*.", "Mándaselo a ese amigo que siempre se pierde."), (FIN, FIN)], [
    ([0], Sc_hook(IC.ambulancia(), [("EN UNA NOCHE", 100, WHITE, 0.15, None, Y1)], pal="red", counter=(0, 685, " NIÑOS", 0.35, 1.3, Y2, YEL)), 0),
    ([1, 2], Sc_hook(IC.calendario("1997", "DICIEMBRE"), [("+12.000", 150, YEL, q(0, 0.55), None, Y1), ("CON SÍNTOMAS", 100, WHITE, q(0, 0.6), None, Y2)], pal="purple",
                     stamp_=("4 MESES", q(1, 0.1), YEL, "FUERA DE LA TELE")), 0),
    ([3, 4], Sc_question(1, "CAPÍTULO ACTUAL", ["¿EP 7?", "¿EP 9?", "¿EP 12?", "¿EP 4?"], "NI IDEA", st_at=q(1, 0.6)), 0),
    ([5], Sc_phone(*EPIS, callout=(0.25, 0.455, "EPISODIO 7", q(0, 0.5))), 0),
    ([6], Sc_ambassador("CAMPEÓN DEL", "\"¿POR DÓNDE IBA?\"", pal="red"), 0),
    ([7], Sc_end(), 1.4)])

V["02_cae_web_pirata"] = ("st4", "lofi7", "lofi11", [
    ("¡Ha caído la web pirata de anime *más grande del mundo*! *7 detenidos*.", "¡Ha caído la web pirata de anime más grande del mundo! Siete detenidos."),
    ("Tenía más de *150 millones* de visitas al mes.", "Tenía más de ciento cincuenta millones de visitas al mes."),
    ("Y de un día para otro, millones de personas perdieron *todo su historial*.", "Y de un día para otro, millones de personas perdieron todo su historial."),
    ("¿Qué estaba viendo? ¿Por dónde iba? *Ni idea*.", "¿Qué estaba viendo? ¿Por dónde iba? Ni idea."),
    ("Ve anime *legal*, y lleva tu lista en *Manga Tracker*. Es tuya, veas donde veas.", "Ve anime legal, y lleva tu lista en Manga Tracker. Es tuya, veas donde veas."),
    ("Mándaselo a ese amigo que *perdió su historial*.", "Mándaselo a ese amigo que perdió su historial."), (FIN, FIN)], [
    ([0, 1], Sc_hook(IC.web_caida(), [("WEB PIRATA", 110, WHITE, 0.1, q(1), Y1), ("CERRADA", 180, YEL, 0.4, q(1), Y2), ("VISITAS AL MES", 100, WHITE, q(1), None, Y1)],
                     pal="red", stamp_=("7 DETENIDOS", q(0, 0.72), RED, None), counter=(0, 150, " MILLONES", q(1, 0.2), 1.0, Y2, YEL)), 0),
    ([2, 3], Sc_question(1, "TU HISTORIAL", ["CARGANDO...", "ERROR 404", "¿?", "CARGANDO..."], "BORRADO", st_at=q(0, 0.8)), 0),
    ([4], Sc_phone(*MI_LISTA, callout=(0.13, 0.334, "TU LISTA", q(0, 0.6))), 0),
    ([5], Sc_ambassador("SUPERVIVIENTE DEL", "HISTORIAL BORRADO", pal="red"), 0),
    ([6], Sc_end(), 1.4)])

V["03_camareros_1927"] = ("st0", "lofi2", "lofi8", [
    ("En 1927, una psicóloga notó algo raro: los camareros recordaban *todos los pedidos*…", "En mil novecientos veintisiete, una psicóloga notó algo raro: los camareros recordaban todos los pedidos…"),
    ("¡Hasta que los cobraban! Entonces… los *olvidaban*.", "¡Hasta que los cobraban! Entonces… los olvidaban."),
    ("Lo que dejamos a medias se nos queda *dando vueltas*.", "Lo que dejamos a medias se nos queda dando vueltas."),
    ("Como ese anime que dejaste en el capítulo 6… y *sigue en tu cabeza*.", "Como ese anime que dejaste en el capítulo seis… y sigue en tu cabeza."),
    ("En *Manga Tracker* lo dejas en pausa, en su episodio, y lo *retomas* cuando quieras.", "En Manga Tracker lo dejas en pausa, en su episodio, y lo retomas cuando quieras."),
    ("Mándaselo a ese que tiene *mil animes a medias*.", "Mándaselo a ese que tiene mil animes a medias."), (FIN, FIN)], [
    ([0, 1], Sc_hook(IC.ticket(), [("CAMAREROS", 120, WHITE, 0.1, None, Y1), ("LO RECUERDAN TODO", 120, YEL, 0.45, q(1), Y2), ("HASTA COBRAR", 150, YEL, q(1), None, Y2)],
                     pal="gold", stamp_=("OLVIDADO", q(1, 0.62), RED, None)), 0),
    ([2, 3], Sc_hud("confused", "ANIME A MEDIAS", "CAPÍTULO 6 · DANDO VUELTAS", hud_at=q(0, 0.3), arrow=False, dot=YEL,
                    meters=[("LO PIENSAS", 1.0, "DEMASIADO", q(1, 0.3), RED)]), 0),
    ([4], Sc_phone(*ESTADOS, mode="still", callout=(0.80, 0.44, "EN PAUSA", q(0, 0.45))), 0),
    ([5], Sc_ambassador("COLECCIONISTA DE", "ANIMES A MEDIAS", pal="gold"), 0),
    ([6], Sc_end(), 1.4)])

V["04_100000_millones"] = ("st4", "lofi6", "lofi12", [
    ("¡Una película de anime ha recaudado más de *100.000 millones de yenes*!", "¡Una película de anime ha recaudado más de cien mil millones de yenes!"),
    ("*Demon Slayer: Infinity Castle*. La primera película japonesa de la historia en conseguirlo.", "Demon Slayer, Infinity Castle. La primera película japonesa de la historia en conseguirlo."),
    ("Y tu tío sigue diciendo que el anime es *de frikis*.", "Y tu tío sigue diciendo que el anime es de frikis."),
    ("Pues los frikis somos *millones*.", "Pues los frikis somos millones."),
    ("Únete a ellos: lleva todo lo que ves en *Manga Tracker*.", "Únete a ellos: lleva todo lo que ves en Manga Tracker."),
    ("Mándaselo a ese tío que dice que el anime es *para niños*.", "Mándaselo a ese tío que dice que el anime es para niños."), (FIN, FIN)], [
    ([0, 1], Sc_hook(IC.saco_yen(), [("TAQUILLA", 110, WHITE, 0.1, None, Y1), ("+100.000 M ¥", 150, YEL, 0.45, None, Y2)], pal="gold",
                     stamp_=("RÉCORD", q(1, 0.55), YEL, "HISTÓRICO")), 0),
    ([2, 3], Sc_hud("smug", "OPINIÓN DE TU TÍO", "\"EL ANIME ES DE FRIKIS\"", hud_at=q(0, 0.2), arrow=False, dot=RED, expr2=("proud", q(1), True),
                    st=("SOMOS MILLONES", q(1, 0.35), GREEN, None)), 0),
    ([4], Sc_phone(*INICIO, callout=(0.3, 0.15, "TODO LO QUE VES", q(0, 0.5))), 0),
    ([5], Sc_ambassador("FRIKI", "Y ORGULLOSO", pal="gold"), 0),
    ([6], Sc_end(), 1.4)])

V["05_decision_de_1963"] = ("st0", "lofi9", "lofi13", [
    ("Hay una decisión de *1963* que explica por qué el anime se hace con *tan poco dinero*.", "Hay una decisión de mil novecientos sesenta y tres que explica por qué el anime se hace con tan poco dinero."),
    ("*Astro Boy* se vendió a la tele tan barato… que el estudio *perdía dinero*.", "Astro Boy se vendió a la tele tan barato… que el estudio perdía dinero."),
    ("¿La solución? *Menos dibujos*… y vender *juguetes*.", "¿La solución? Menos dibujos… y vender juguetes."),
    ("Y ese modelo, barato y con muñecos, se quedó en la industria *hasta hoy*.", "Y ese modelo, barato y con muñecos, se quedó en la industria hasta hoy."),
    ("El anime vive de fans como tú. Lleva todo lo que ves en *Manga Tracker*.", "El anime vive de fans como tú. Lleva todo lo que ves en Manga Tracker."),
    ("Mándaselo a ese que se lo ve todo… *sin saber cómo se hace*.", "Mándaselo a ese que se lo ve todo… sin saber cómo se hace."), (FIN, FIN)], [
    ([0], Sc_hook(IC.calendario("1963", "AÑO"), [("UNA DECISIÓN", 110, WHITE, 0.1, None, Y1), ("ANIME LOW COST", 140, YEL, 0.45, None, Y2)], pal="blue"), 0),
    ([1], Sc_hook(IC.tele("TV 1963", "ASTRO BOY"), [("VENDIDO A LA TELE", 100, WHITE, 0.1, None, Y1), ("EL ESTUDIO PERDÍA", 120, YEL, q(0, 0.6), None, Y2)], pal="red",
                  stamp_=("BARATO", q(0, 0.45), YEL, None)), 0),
    ([2, 3], Sc_hud("shock", "", "", hud_at=None, arrow=False, meters=[("DIBUJOS", 0.25, "MENOS", q(0, 0.25), RED), ("JUGUETES", 1.0, "MÁS", q(0, 0.7), GREEN)],
                    st=("HASTA HOY", q(1, 0.55), YEL, None)), 0),
    ([4], Sc_phone(13.5, 17.5, callout=None), 0),
    ([5], Sc_ambassador("SABELOTODO", "DEL ANIME", pal="blue"), 0),
    ([6], Sc_end(), 1.4)])

V["06_maraton_olvido"] = ("st4", "lofi5", "lofi14", [
    ("Un estudio dice que ver series del tirón hace que las *olvides antes*.", "Un estudio dice que ver series del tirón hace que las olvides antes."),
    ("Al día siguiente te acuerdas de todo… pero *meses después*, mucho menos que quien las vio poco a poco.", "Al día siguiente te acuerdas de todo… pero meses después, mucho menos que quien las vio poco a poco."),
    ("¡Y encima las *disfrutas menos*!", "¡Y encima las disfrutas menos!"),
    ("Tú, después de una maratón de 24 episodios: ¿de qué iba? *Ni idea*.", "Tú, después de una maratón de veinticuatro episodios: ¿de qué iba? Ni idea."),
    ("Por eso yo lo apunto todo en *Manga Tracker*. Y no se me olvida *nada*.", "Por eso yo lo apunto todo en Manga Tracker. Y no se me olvida nada."),
    ("Mándaselo a ese que se ve una temporada *en una noche*.", "Mándaselo a ese que se ve una temporada en una noche."), (FIN, FIN)], [
    ([0, 1], Sc_hook(IC.curva(), [("MARATÓN", 120, WHITE, 0.1, None, Y1), ("= OLVIDO", 170, YEL, 0.45, None, Y2)], pal="purple",
                     stamp_=("ESTUDIO", q(1, 0.45), GREEN, "REAL")), 0),
    ([2, 3], Sc_hud("smug", "", "", hud_at=None, arrow=False, glasses=True, expr2=("confused", q(1), False),
                    meters=[("DISFRUTE", 0.35, "MENOS", q(0, 0.15), RED)], st=("NI IDEA", q(1, 0.78), RED, None)), 0),
    ([4], Sc_phone(*PERFIL, mode="still", callout=(0.22, 0.487, "167 OBRAS", q(0, 0.5))), 0),
    ([5], Sc_ambassador("REY DE LA", "MARATÓN", pal="purple"), 0),
    ([6], Sc_end(), 1.4)])

V["07_mitad_netflix"] = ("st0", "lofi3", "lofi15", [
    ("Más de la *mitad* de los usuarios de Netflix ven anime.", "Más de la mitad de los usuarios de Netflix ven anime."),
    ("Lo dijo la propia Netflix. Sí: *1 de cada 2*.", "Lo dijo la propia Netflix. Sí: uno de cada dos."),
    ("Así que tu vecino, tu profe… y probablemente *tu madre*, ven anime.", "Así que tu vecino, tu profe… y probablemente tu madre, ven anime."),
    ("El anime ya *no es de nicho*.", "El anime ya no es de nicho."),
    ("Y si ves tanto, organízalo en *Manga Tracker*: viendo, pendientes, completados.", "Y si ves tanto, organízalo en Manga Tracker: viendo, pendientes, completados."),
    ("Mándaselo a tu madre. *Por si acaso*.", "Mándaselo a tu madre. Por si acaso."), (FIN, FIN)], [
    ([0, 1], Sc_hook(IC.quesito(), [("USUARIOS DE NETFLIX", 92, WHITE, 0.1, None, Y1), ("1 DE CADA 2", 170, YEL, 0.45, None, Y2)], pal="red",
                     stamp_=("VEN ANIME", q(1, 0.35), GREEN, None)), 0),
    ([2, 3], Sc_hud("proud", "ANIME DETECTADO EN", "TU VECINO · TU PROFE · TU MADRE", hud_at=q(0, 0.15), arrow=False, dot=GREEN,
                    st=("YA NO ES NICHO", q(1, 0.25), YEL, None)), 0),
    ([4], Sc_phone(*MI_LISTA, callout=(0.13, 0.334, "VIENDO", q(0, 0.55))), 0),
    ([5], Sc_ambassador("MADRE OTAKU", "CERTIFICADA", pal="red"), 0),
    ([6], Sc_end(), 1.4)])

V["08_imdb_1_de_cada_3"] = ("st4", "lofi16", "lofi17", [
    ("*1 de cada 3* de las series más votadas de IMDb… es anime.", "Una de cada tres de las series más votadas de IMDb… es anime."),
    ("100 de las 300. ¡Y *9 de las 20* primeras!", "Cien de las trescientas. ¡Y nueve de las veinte primeras!"),
    ("Y tu amigo sigue diciendo: *yo no veo dibujos*.", "Y tu amigo sigue diciendo: yo no veo dibujos."),
    ("*Él se lo pierde*.", "Él se lo pierde."),
    ("En *Manga Tracker* tienes recomendaciones para ti. Empieza por ahí.", "En Manga Tracker tienes recomendaciones para ti. Empieza por ahí."),
    ("Mándaselo a ese amigo que *no ve dibujos*.", "Mándaselo a ese amigo que no ve dibujos."), (FIN, FIN)], [
    ([0, 1], Sc_hook(IC.trofeo(), [("SERIES MÁS VOTADAS", 92, WHITE, 0.1, None, Y1), ("1 DE CADA 3", 170, YEL, 0.45, None, Y2)], pal="gold",
                     stamp_=("9 DEL TOP 20", q(1, 0.5), YEL, None)), 0),
    ([2, 3], Sc_hud("smug", "MODO 'YO NO VEO DIBUJOS'", "ACTIVADO", hud_at=q(0, 0.2), arrow=False, glasses=True, dot=RED,
                    st=("SE LO PIERDE", q(1, 0.15), RED, None)), 0),
    ([4], Sc_phone(*INICIO, callout=(0.3, 0.79, "PARA TI", q(0, 0.5))), 0),
    ([5], Sc_ambassador("PRESIDENTE DEL CLUB", "\"YO NO VEO DIBUJOS\"", pal="gold"), 0),
    ([6], Sc_end(), 1.4)])

V["09_animadores_pocos_euros"] = ("st0", "lofi1", "lofi18", [
    ("Quien dibuja tu anime favorito puede cobrar *unos cientos de yenes* por dibujo.", "Quien dibuja tu anime favorito puede cobrar unos cientos de yenes por dibujo."),
    ("O sea, *unos pocos euros*. Un estudio calculó que los principiantes ganaban unos *9.000 dólares al año*.", "O sea, unos pocos euros. Un estudio calculó que los principiantes ganaban unos nueve mil dólares al año."),
    ("Dibujando *a mano*. Uno a uno.", "Dibujando a mano. Uno a uno."),
    ("Y tú no te acuerdas ni de *cómo se llamaba* el anime.", "Y tú no te acuerdas ni de cómo se llamaba el anime."),
    ("Lo mínimo: apúntalo en *Manga Tracker* y dale *tu nota*.", "Lo mínimo: apúntalo en Manga Tracker, y dale tu nota."),
    ("Mándaselo a quien *respeta a los animadores*.", "Mándaselo a quien respeta a los animadores."), (FIN, FIN)], [
    ([0, 1, 2], Sc_hook(IC.lapiz_moneda(), [("POR DIBUJO", 110, WHITE, 0.1, None, Y1), ("UNOS POCOS EUROS", 130, YEL, 0.45, None, Y2)], pal="blue",
                        stamp_=("9.000 $ AL AÑO", q(1, 0.62), RED, "PRINCIPIANTES")), 0),
    ([3], Sc_question(1, "¿CÓMO SE LLAMABA?", ["EL DE LA ESPADA", "EL DEL CHICO", "ESE..."], "NI IDEA", st_at=q(0, 0.7)), 0),
    ([4], Sc_phone(*FICHA_NOTA, mode="still", callout=(0.22, 0.565, "TU NOTA", q(0, 0.45))), 0),
    ([5], Sc_ambassador("MÁXIMO RESPETO", "A LOS ANIMADORES", pal="blue"), 0),
    ([6], Sc_end(), 1.4)])

V["10_28000_millones"] = ("st4", "lofi19", "lofi20", [
    ("El anime mueve más de *28.000 millones de dólares* al año.", "El anime mueve más de veintiocho mil millones de dólares al año."),
    ("¡Récord histórico! Y más de la *mitad* ya se gasta fuera de Japón.", "¡Récord histórico! Y más de la mitad ya se gasta fuera de Japón."),
    ("O sea: *tú* también estás en esa cifra.", "O sea: tú también estás en esa cifra."),
    ("Cada capítulo que ves… *cuenta*.", "Cada capítulo que ves… cuenta."),
    ("Y en *Manga Tracker* ves todo lo que llevas: *167 obras*, en mi caso.", "Y en Manga Tracker ves todo lo que llevas: ciento sesenta y siete obras, en mi caso."),
    ("Mándaselo a ese que dice que el anime *no da dinero*.", "Mándaselo a ese que dice que el anime no da dinero."), (FIN, FIN)], [
    ([0, 1], Sc_hook(IC.globo(), [("AL AÑO", 110, WHITE, 0.1, None, Y1), ("+28.000 M $", 160, YEL, 0.45, None, Y2)], pal="green",
                     stamp_=("RÉCORD", q(1, 0.15), YEL, None)), 0),
    ([2, 3], Sc_hud("proud", "57 % FUERA DE JAPÓN", "INCLUIDO TÚ", hud_at=q(0, 0.2), arrow=False, glasses=True, dot=GREEN,
                    meters=[("TU APORTACIÓN", 1.0, "CUENTA", q(1, 0.2), GREEN)]), 0),
    ([4], Sc_phone(*PERFIL, mode="still", callout=(0.22, 0.487, "167 OBRAS", q(0, 0.6))), 0),
    ([5], Sc_ambassador("ACCIONISTA", "DEL ANIME", pal="green"), 0),
    ([6], Sc_end(), 1.4)])

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
                fr = [(0, T) for T in (0.1, 0.5, 2.0, 4.0)] + [(si, T) for si in range(1, len(scenes)) for T in (0.7, 2.6)]
                print(render(n, vid, mus, lines, scenes, OUT, frames=fr), flush=True); break
            if os.path.exists(f"{OUT}/{n}.mp4"): continue
            print(render(n, vid, mus, lines, scenes, OUT), flush=True)
