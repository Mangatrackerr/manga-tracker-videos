# Lote "satírico" del 12/11/2026 — trend explainer irónico con GANCHO random (dato cierto) en los primeros 5 s,
# después la sátira del amigo otaku y la app como solución. Uso: python3 pipeline/satira/lote_2026-11-12s.py [chk] [tema ...]
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["SRC_VIDEO"] = os.path.abspath(os.path.join(HERE, "..", "..", "procesadas", "grabacion_2026-11-02.mp4"))
sys.path.insert(0, HERE)
from engine_satira import *
import iconos as IC
M.SUBS += [("Pokémon", "Pokemon"), ("Ash", "Ash")]
LOTE = "2026-11-12s"
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "videos"))
FIN = "Manga Tracker. Gratis en Play Store."
# clips de la grabación del 2/11 (callouts en fracciones del fotograma original)
MI_LISTA = (90.1, 92.6); EPIS = (62.0, 66.0); PERFIL = (127.75, 127.85); LISTAS = (105.0, 108.2); AMIGO = (121.3, 124.5); ESTRENOS = (1.2, 5.5)
Y1, Y2 = 1450, 1630  # filas de texto bajo el icono del gancho
q = lambda k, f=0.0: (k, 0, f)  # tiempo: inicio de la línea k de la escena + f·duración

V = {}
V["01_memoria_de_pez"] = ("chico", "n1", [
    ("¿Sabías que un *pez de colores* puede recordar cosas durante *meses*?", "¿Sabías que un pez de colores puede recordar cosas durante meses?"),
    ("Lo de los *3 segundos* es un *mito*.", "Lo de los tres segundos, es un mito."),
    ("O sea, tiene más memoria que tu amigo, que no sabe ni *en qué capítulo iba*.", "O sea, tiene más memoria que tu amigo, que no sabe ni en qué capítulo iba."),
    ("¿Episodio 7? ¿El 9? *Ni idea*.", "¿Episodio siete? ¿El nueve? Ni idea."),
    ("Los demás usamos *Manga Tracker*: marcas el episodio y *listo*.", "Los demás usamos Manga Tracker: marcas el episodio, y listo."),
    ("Así que mándaselo a ese amigo con *memoria de pez*.", "Así que mándaselo a ese amigo con memoria de pez."), (FIN, FIN)], [
    ([0, 1], Sc_hook(IC.pecera(), [("MEMORIA DE PEZ:", 96, WHITE, 0.15, None, Y1), ("MESES", 190, YEL, 0.45, q(1), Y2),
                                    ("NO 3 SEGUNDOS", 130, YEL, q(1), None, Y2)], pal="blue", stamp_=("MITO", q(1, 0.55), RED, None)), 0),
    ([2], Sc_hud("smug", "", "", hud_at=None, arrow=False, meters=[("PEZ DE COLORES", 0.92, "MESES", q(0, 0.2), GREEN), ("TU AMIGO", 0.04, "3 SEG", q(0, 0.6), RED)]), 0),
    ([3], Sc_question(1, "CAPÍTULO ACTUAL", ["¿EP 7?", "¿EP 9?", "¿EP 12?", "¿EP 4?"], "NI IDEA", st_at=q(0, 0.7)), 0),
    ([4], Sc_phone(*EPIS, callout=(0.25, 0.455, "EPISODIO 7", q(0, 0.6))), 0),
    ([5], Sc_ambassador("CAMPEÓN MUNDIAL DE", "\"MEMORIA DE PEZ\"", pal="blue"), 0),
    ([6], Sc_end(), 1.4)])

V["02_diez_anos_eternos"] = ("chica", "n2", [
    ("¿Sabías que *Ash*, el de *Pokémon*, tuvo *10 años*… durante *26 años*?", "¿Sabías que Ash, el de Pokémon, tuvo diez años... durante veintiséis años?"),
    ("Del *1997* al *2023*. Sin cumplir *ni uno*.", "Del mil novecientos noventa y siete, al dos mil veintitrés. Sin cumplir ni uno."),
    ("Pues tu amigo lleva *3 años* diciendo: *este finde lo empiezo*.", "Pues tu amigo lleva tres años diciendo: este finde lo empiezo."),
    ("Tiene un nombre: el *Finde Eterno*.", "Tiene un nombre: el Finde Eterno."),
    ("Apúntalo como *Planificado* en *Manga Tracker*, y empiézalo *de verdad*.", "Apúntalo como planificado en Manga Tracker, y empiézalo de verdad."),
    ("Y mándaselo a ese que *siempre lo empieza el finde*.", "Y mándaselo a ese que siempre lo empieza el finde."), (FIN, FIN)], [
    ([0, 1], Sc_hook(IC.tarta(), [("EDAD:", 110, WHITE, 0.15, q(1), Y1), ("10 AÑOS", 190, YEL, 0.45, q(1), Y2), ("AÑO", 110, WHITE, q(1), None, Y1)],
                     pal="pink", counter=(1997, 2023, "", q(1), 1.6, Y2, YEL), stamp_=("NI UNO", q(1, 0.75), RED, "CUMPLIDO")), 0),
    ([2], Sc_question(0, "LO EMPIEZA...", ["ESTE FINDE", "EL OTRO", "EN VERANO", "EN NAVIDAD"], "3 AÑOS", st_at=q(0, 0.75), st_sub="ESPERANDO"), 0),
    ([3], Sc_reveal("EL FINDE", "ETERNO", obj=IC.calendario("FINDE", "ESTE"), pal="pink"), 0.2),
    ([4], Sc_phone(*MI_LISTA, callout=(0.12, 0.88, "PLANIFICADO", q(0, 0.4))), 0),
    ([5], Sc_ambassador("PRESIDENTE DEL", "\"ESTE FINDE LO EMPIEZO\"", pal="pink"), 0),
    ([6], Sc_end(), 1.4)])

V["03_casi_entero"] = ("chico", "n3", [
    ("Ver *One Piece* entero, del tirón, te llevaría *más de 2 semanas*… sin dormir.", "Ver One Piece entero, del tirón, te llevaría más de dos semanas... sin dormir."),
    ("Son *más de 1.100* episodios.", "Son más de mil cien episodios."),
    ("Y tu amigo dice que se lo ha visto *casi entero*.", "Y tu amigo dice que se lo ha visto casi entero."),
    ("Casi entero. Va por el *61*.", "Casi entero. Va por el sesenta y uno."),
    ("Con *Manga Tracker* sabes en qué episodio vas *de verdad*.", "Con Manga Tracker sabes en qué episodio vas, de verdad."),
    ("Mándaselo a ese que se lo ha visto *casi entero*.", "Mándaselo a ese que se lo ha visto casi entero."), (FIN, FIN)], [
    ([0, 1], Sc_hook(IC.tele(), [("DEL TIRÓN:", 100, WHITE, 0.15, q(1), Y1), ("+2 SEMANAS", 170, YEL, 0.45, q(1), Y2), ("EPISODIOS", 110, WHITE, q(1), None, Y1)],
                     pal="red", counter=(0, 1100, "+", q(1), 1.2, Y2, YEL)), 0),
    ([2, 3], Sc_hud("smug", "", "", hud_at=None, arrow=False, glasses=True, meters=[("LO QUE DICE", 0.97, "CASI ENTERO", q(0, 0.5), GREEN), ("LO QUE LLEVA", 0.055, "61 / 1.100", q(1, 0.4), RED)],
                    st=("PILLADO", q(1, 0.85), RED, None)), 0),
    ([4], Sc_phone(*EPIS, callout=(0.25, 0.455, "EPISODIO EXACTO", q(0, 0.55))), 0),
    ([5], Sc_ambassador("CAMPEÓN DEL", "\"CASI ENTERO\"", pal="red"), 0),
    ([6], Sc_end(), 1.4)])

V["04_spoilers_ciencia"] = ("chica", "n4", [
    ("Un estudio de la *Universidad de California* dice que los *spoilers* hacen que disfrutes *más* una historia.", "Un estudio de la Universidad de California dice que los spoilers hacen que disfrutes más una historia."),
    ("Sí, *más*.", "Sí. Más."),
    ("Entonces el amigo que te *spoileó* el final… ¿era un *genio*?", "Entonces, el amigo que te spoileó el final... ¿era un genio?"),
    ("*No*. Sigue siendo un *monstruo*.", "No. Sigue siendo un monstruo."),
    ("Marca tus episodios en *Manga Tracker* y ponte al día *antes* de que te lo cuenten.", "Marca tus episodios en Manga Tracker, y ponte al día antes de que te lo cuenten."),
    ("Y mándaselo a ese amigo que *spoilea*.", "Y mándaselo a ese amigo que spoilea."), (FIN, FIN)], [
    ([0, 1], Sc_hook(IC.estudio(), [("SPOILERS =", 110, WHITE, 0.15, None, Y1), ("+ DISFRUTE", 170, YEL, 0.45, None, Y2)], pal="green",
                     stamp_=("CIENCIA", q(1, 0.1), GREEN, "DE VERDAD")), 0),
    ([2, 3], Sc_hud("smug", "MODO SPOILER", "ACTIVADO", hud_at=q(0, 0.2), arrow=False, glasses=True, dot=RED, expr2=("shock", q(1), False),
                    st=("MONSTRUO", q(1, 0.45), RED, "CERTIFICADO")), 0),
    ([4], Sc_phone(*EPIS, callout=(0.25, 0.455, "PONTE AL DÍA", q(0, 0.5))), 0),
    ([5], Sc_ambassador("PRESIDENTE DEL", "CLUB DEL SPOILER", pal="green"), 0),
    ([6], Sc_end(), 1.4)])

V["05_curva_del_olvido"] = ("chico", "n5", [
    ("Según la *curva del olvido*, en *una hora* olvidas *más de la mitad* de lo que acabas de aprender.", "Según la curva del olvido, en una hora olvidas más de la mitad de lo que acabas de aprender."),
    ("Por eso nunca te acuerdas de cómo se llamaba *ese anime*.", "Por eso nunca te acuerdas de cómo se llamaba ese anime."),
    ("Ya sabes cuál: *el de la espada*… el del chico que… *ese*.", "Ya sabes cuál: el de la espada... el del chico que... ese."),
    ("Yo lo tengo todo en *Manga Tracker*: *167 obras*, y no se me olvida *ninguna*.", "Yo lo tengo todo en Manga Tracker: ciento sesenta y siete obras, y no se me olvida ninguna."),
    ("Mándaselo a ese que siempre dice: *el anime ese, el de la espada*.", "Mándaselo a ese que siempre dice: el anime ese, el de la espada."), (FIN, FIN)], [
    ([0], Sc_hook(IC.curva(), [("EN 1 HORA OLVIDAS", 92, WHITE, 0.15, None, Y1), ("+ DE LA MITAD", 160, YEL, 0.45, None, Y2)], pal="purple"), 0),
    ([1, 2], Sc_question(1, "¿CÓMO SE LLAMABA?", ["EL DE LA ESPADA", "EL DEL CHICO", "EL DE LA ESCUELA", "ESE..."], "NI IDEA", st_at=q(1, 0.8)), 0),
    ([3], Sc_phone(*PERFIL, mode="still", callout=(0.22, 0.487, "167 OBRAS", q(0, 0.5))), 0),
    ([4], Sc_ambassador("REY DEL", "\"EL ANIME ESE\"", pal="purple"), 0),
    ([5], Sc_end(), 1.4)])

V["06_desde_1969"] = ("chica", "n6", [
    ("El anime *más largo de la historia* se emite desde *1969*.", "El anime más largo de la historia se emite desde mil novecientos sesenta y nueve."),
    ("*Más de 50 años* en antena. Y sigue.", "Más de cincuenta años en antena. Y sigue."),
    ("Y aun así, tu lista de *pendientes* es más larga.", "Y aun así, tu lista de pendientes es más larga."),
    ("Tiene un nombre: la *Lista Infinita*.", "Tiene un nombre: la Lista Infinita."),
    ("En *Manga Tracker* la tienes ordenada y ves *cuántos te quedan*.", "En Manga Tracker la tienes ordenada, y ves cuántos te quedan."),
    ("Mándaselo a ese que tiene *200 pendientes* y empieza *otro*.", "Mándaselo a ese que tiene doscientos pendientes, y empieza otro."), (FIN, FIN)], [
    ([0, 1], Sc_hook(IC.calendario("1969"), [("EN ANTENA", 110, WHITE, 0.15, None, Y1), ("AÑOS", 100, WHITE, q(1), None, 1780)], pal="gold",
                     counter=(0, 50, "+", q(1), 1.0, Y2, YEL)), 0),
    ([2], Sc_hud("smug", "", "", hud_at=None, arrow=False, meters=[("ANIME + LARGO", 0.55, "+50 AÑOS", q(0, 0.2), GREEN), ("TUS PENDIENTES", 1.0, "INFINITO", q(0, 0.55), RED)]), 0),
    ([3], Sc_reveal("LA LISTA", "INFINITA", obj=IC.pergamino(), pal="gold"), 0.2),
    ([4], Sc_phone(*MI_LISTA, callout=(0.9, 0.675, "26 PENDIENTES", q(0, 0.55))), 0),
    ([5], Sc_ambassador("COLECCIONISTA DE", "PENDIENTES", pal="gold"), 0),
    ([6], Sc_end(), 1.4)])

V["07_tres_corazones"] = ("chico", "n7", [
    ("¿Sabías que los *pulpos* tienen *3 corazones*?", "¿Sabías que los pulpos tienen tres corazones?"),
    ("Y aun así no les llegarían para todos los animes que *te han roto el tuyo*.", "Y aun así no les llegarían para todos los animes que te han roto el tuyo."),
    ("Tú dices que el anime *no te hace llorar*…", "Tú dices que el anime no te hace llorar..."),
    ("Pero los pañuelos dicen *otra cosa*.", "Pero los pañuelos dicen otra cosa."),
    ("Yo los guardo todos en una lista en *Manga Tracker*: *los que me hicieron llorar*.", "Yo los guardo todos en una lista en Manga Tracker: los que me hicieron llorar."),
    ("Mándaselo a ese que dice que *el anime no le hace llorar*.", "Mándaselo a ese que dice que el anime no le hace llorar."), (FIN, FIN)], [
    ([0, 1], Sc_hook(IC.pulpo(), [("PULPO", 120, WHITE, 0.1, None, Y1), ("3 CORAZONES", 170, YEL, 0.45, None, Y2)], pal="purple",
                     stamp_=("NO LLEGAN", q(1, 0.6), RED, None)), 0),
    ([2, 3], Sc_hud("smug", "", "", hud_at=None, arrow=False, glasses=True, expr2=("cry", q(1), False),
                    meters=[("LO QUE DICE", 0.02, "0 LÁGRIMAS", q(0, 0.3), GREEN), ("PAÑUELOS USADOS", 1.0, "TODOS", q(1, 0.2), RED)]), 0),
    ([4], Sc_phone(*LISTAS, callout=(0.35, 0.215, "TUS LISTAS", q(0, 0.5))), 0),
    ([5], Sc_ambassador("EL QUE NUNCA LLORA", "(MENTIRA)", pal="purple"), 0),
    ([6], Sc_end(), 1.4)])

V["08_llego_tarde"] = ("chica", "n8", [
    ("Cada *3 meses* empieza una *temporada nueva* de anime.", "Cada tres meses empieza una temporada nueva de anime."),
    ("*Invierno, primavera, verano y otoño*. Con *decenas de estrenos* cada una.", "Invierno, primavera, verano y otoño. Con decenas de estrenos cada una."),
    ("Y tu amigo se entera del bueno… *cuando ya ha terminado*.", "Y tu amigo se entera del bueno... cuando ya ha terminado."),
    ("Tiene un nombre: el *Llego Tarde*.", "Tiene un nombre: el Llego Tarde."),
    ("En *Manga Tracker* ves los *próximos estrenos* antes que nadie.", "En Manga Tracker ves los próximos estrenos antes que nadie."),
    ("Mándaselo a ese que *siempre llega tarde*.", "Mándaselo a ese que siempre llega tarde."), (FIN, FIN)], [
    ([0, 1], Sc_hook(IC.estaciones(), [("CADA", 110, WHITE, 0.1, None, Y1), ("3 MESES", 190, YEL, 0.45, None, Y2)], pal="blue",
                     stamp_=("DECENAS", q(1, 0.62), YEL, "DE ESTRENOS")), 0),
    ([2], Sc_question(1, "SE ENTERA DEL ESTRENO", ["¿HOY?", "¿AYER?", "¿HACE 1 MES?"], "TARDE", st_at=q(0, 0.72), st_sub="COMO SIEMPRE"), 0),
    ([3], Sc_reveal("EL", "\"LLEGO TARDE\"", obj=IC.reloj_arena(), pal="blue"), 0.2),
    ([4], Sc_phone(*ESTRENOS, callout=(0.3, 0.152, "PRÓXIMOS ESTRENOS", q(0, 0.5))), 0),
    ([5], Sc_ambassador("MIEMBRO VIP DEL", "\"LLEGO TARDE\"", pal="blue"), 0),
    ([6], Sc_end(), 1.4)])

V["09_solo_uno_mas"] = ("chico", "n2", [
    ("Cuando miras una pantalla, *parpadeas muchísimo menos* de lo normal.", "Cuando miras una pantalla, parpadeas muchísimo menos de lo normal."),
    ("Tus ojos lo saben. *Tú no*.", "Tus ojos lo saben. Tú no."),
    ("Sobre todo a las *4 de la mañana*, en el capítulo *solo uno más*.", "Sobre todo a las cuatro de la mañana, en el capítulo, solo uno más."),
    ("Tiene un nombre: el *Solo Uno Más*.", "Tiene un nombre: el Solo Uno Más."),
    ("Al menos con *Manga Tracker* sabes en qué episodio *te dormiste*.", "Al menos con Manga Tracker sabes en qué episodio te dormiste."),
    ("Mándaselo a ese que dice *solo uno más* a las 4 de la mañana.", "Mándaselo a ese que dice, solo uno más, a las cuatro de la mañana."), (FIN, FIN)], [
    ([0, 1], Sc_hook(IC.ojo(), [("PARPADEAS", 120, WHITE, 0.1, None, Y1), ("MUCHO MENOS", 160, YEL, 0.45, None, Y2)], pal="red",
                     stamp_=("OJOS SECOS", q(1, 0.5), RED, None)), 0),
    ([2], Sc_question(1, "HORA", ["01:12", "02:30", "03:47", "04:00"], "SOLO UNO MÁS", st_at=q(0, 0.7)), 0),
    ([3], Sc_reveal("EL \"SOLO", "UNO MÁS\"", obj=IC.reloj(), pal="red"), 0.2),
    ([4], Sc_phone(*EPIS, callout=(0.25, 0.455, "AQUÍ TE DORMISTE", q(0, 0.55))), 0),
    ([5], Sc_ambassador("CAMPEÓN DEL", "\"SOLO UNO MÁS\"", pal="red"), 0),
    ([6], Sc_end(), 1.4)])

V["10_vacas_amigas"] = ("chica", "n4", [
    ("¿Sabías que las *vacas* tienen *mejores amigas*?", "¿Sabías que las vacas tienen mejores amigas?"),
    ("Y cuando están juntas, *se estresan menos*. Es ciencia.", "Y cuando están juntas, se estresan menos. Es ciencia."),
    ("Mientras tanto tú, *sin nadie* con quien comentar el capítulo de ayer.", "Mientras tanto tú, sin nadie con quien comentar el capítulo de ayer."),
    ("Nivel de soledad otaku: *100 %*.", "Nivel de soledad otaku: cien por cien."),
    ("En *Manga Tracker* agregas a tus amigos y ves *qué están viendo*.", "En Manga Tracker agregas a tus amigos, y ves qué están viendo."),
    ("Mándaselo a tu *mejor amigo otaku*. No seas menos que una vaca.", "Mándaselo a tu mejor amigo otaku. No seas menos que una vaca."), (FIN, FIN)], [
    ([0, 1], Sc_hook(IC.vacas(), [("VACAS CON", 110, WHITE, 0.1, None, Y1), ("MEJORES AMIGAS", 140, YEL, 0.45, None, Y2)], pal="green",
                     stamp_=("CIENCIA", q(1, 0.6), GREEN, None)), 0),
    ([2, 3], Sc_hud("confused", "AMIGOS OTAKU", "0 CONECTADOS", hud_at=q(0, 0.3), arrow=False, dot=RED,
                    meters=[("SOLEDAD OTAKU", 1.0, "100 %", q(1, 0.1), RED)]), 0),
    ([4], Sc_phone(*AMIGO, callout=(0.5, 0.075, "TU AMIGO", q(0, 0.5))), 0),
    ([5], Sc_ambassador("MEJORES AMIGOS", "(COMO LAS VACAS)", pal="green"), 0),
    ([6], Sc_end(), 1.4)])

if __name__ == "__main__":
    args = sys.argv[1:]; chk = "chk" in args; names = [a for a in args if a != "chk"]
    for key, (voz, mus, lines, scenes) in V.items():
        tema = key[3:]
        if names and tema not in names and key not in names: continue
        n = f"{LOTE}_{tema}_{voz}"
        if chk:
            fr = [(0, T) for T in (0.1, 0.4, 1.5, 3.0, 4.5)] + [(si, T) for si in range(1, len(scenes)) for T in (0.6, 2.5)]
            print(render(n, voz, mus, lines, scenes, OUT, frames=fr), flush=True); continue
        if os.path.exists(f"{OUT}/{n}.mp4"): continue
        print(render(n, voz, mus, lines, scenes, OUT), flush=True)
