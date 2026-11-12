# PRUEBA de "voz con vida" (12/11/2026): tema "Casi entero" con Supertonic 3 + entonación retocada.
# Uso: python3 pipeline/satira/prueba_viva_2026-11-12.py [chk] [chico1|chica1|chica2|chica5 ...]
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["SRC_VIDEO"] = os.path.abspath(os.path.join(HERE, "..", "..", "procesadas", "grabacion_2026-11-02.mp4"))
sys.path.insert(0, HERE)
from engine_satira import *
import engine_satira as ES, iconos as IC, voz_viva
voz_viva.patch(M)
ES.VOICE_CHAIN = "highpass=f=75,equalizer=f=3000:t=q:w=1.4:g=1.2,acompressor=threshold=0.15:ratio=2:attack=10:release=150,"
ES.MUSIC_VOL = 0.16
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "videos"))
VOCES = {"chico1": "st5", "chica1": "st0", "chica5": "st4"}
MUSICA = {"chico1": "lofi1", "chica1": "lofi2", "chica5": "lofi3"}
EPIS = (62.0, 66.0); Y1, Y2 = 1450, 1630
q = lambda k, f=0.0: (k, 0, f)
FIN = "Manga Tracker. ¡Gratis en Play Store!"
LINES = [
    ("¿Sabías que ver *One Piece* entero, del tirón… te llevaría *más de 2 semanas*?", "¿Sabías que ver One Piece entero, del tirón… te llevaría más de dos semanas?"),
    ("¡Sin dormir! ¡*Más de 1.100* episodios!", "¡Sin dormir! ¡Más de mil cien episodios!"),
    ("Y tu amigo dice que se lo ha visto… *casi entero*.", "Y tu amigo dice que se lo ha visto… casi entero."),
    ("¿Casi entero? ¡Va por el *61*!", "¿Casi entero? ¡Va por el sesenta y uno!"),
    ("Con *Manga Tracker* sabes en qué episodio vas. *De verdad*.", "Con Manga Tracker sabes en qué episodio vas. De verdad."),
    ("Mándaselo a ese que se lo ha visto… ¡*casi entero*!", "Mándaselo a ese que se lo ha visto… ¡casi entero!"), (FIN, FIN)]
SCENES = [
    ([0, 1], Sc_hook(IC.tele(), [("DEL TIRÓN:", 100, WHITE, 0.15, q(1), Y1), ("+2 SEMANAS", 170, YEL, 0.45, q(1), Y2), ("EPISODIOS", 110, WHITE, q(1), None, Y1)],
                     pal="red", counter=(0, 1100, "+", q(1, 0.25), 1.0, Y2, YEL), stamp_=("SIN DORMIR", q(1, 0.02), RED, None)), 0),
    ([2, 3], Sc_hud("smug", "", "", hud_at=None, arrow=False, glasses=True, meters=[("LO QUE DICE", 0.97, "CASI ENTERO", q(0, 0.5), GREEN), ("LO QUE LLEVA", 0.055, "61 / 1.100", q(1, 0.35), RED)],
                    st=("PILLADO", q(1, 0.8), RED, None), expr2=("shock", q(1, 0.3), False)), 0),
    ([4], Sc_phone(*EPIS, callout=(0.25, 0.455, "EPISODIO EXACTO", q(0, 0.5))), 0),
    ([5], Sc_ambassador("CAMPEÓN DEL", "\"CASI ENTERO\"", pal="red"), 0),
    ([6], Sc_end(), 1.4)]

if __name__ == "__main__":
    a = sys.argv[1:]; chk = "chk" in a; sel = [x for x in a if x in VOCES] or list(VOCES)
    for v in sel:
        n = f"2026-11-12v_casi_entero_{v}"
        if chk: print(render(n, VOCES[v], MUSICA[v], LINES, SCENES, OUT, frames=[(0, 0.3), (0, 4.0), (1, 1.0), (1, 3.5), (3, 1.0)])); continue
        print(render(n, VOCES[v], MUSICA[v], LINES, SCENES, OUT), flush=True)
