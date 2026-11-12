# Vídeo de PRUEBA estilo trend "explainer satírico" (12/11/2026): "La Memoria Prodigiosa™" del amigo otaku.
# Uso: python3 pipeline/satira/prueba_2026-11-12.py [chk] [chico|chica]
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["SRC_VIDEO"] = os.path.abspath(os.path.join(HERE, "..", "..", "procesadas", "grabacion_2026-11-02.mp4"))
sys.path.insert(0, HERE)
from engine_satira import *
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "videos"))
NAME = "2026-11-12s_memoria_prodigiosa"
FIN = "Manga Tracker. Gratis en Play Store."
LINES = [
    ("¿Sabías que tu amigo *otaku* tiene un *superpoder*", "¿Sabías que tu amigo otaku tiene un superpoder"),
    ("que le permite seguir *30 series* a la vez… sin apuntar *nada*?", "que le permite seguir treinta series a la vez... sin apuntar nada?"),
    ("Se llama… la *Memoria Prodigiosa*.", "Se llama... la Memoria Prodigiosa."),
    ("Él no necesita apps. Lo lleva todo *aquí*.", "Él no necesita apps. Lo lleva todo aquí."),
    ("¿En qué capítulo iba? *Ni idea*.", "¿En qué capítulo iba? Ni idea."),
    ("¿Lo terminó o lo dejó? *Quién sabe*.", "¿Lo terminó, o lo dejó? Quién sabe."),
    ("¿Que ya salió la segunda temporada? Se enteró por un *spoiler*.", "¿Que ya salió la segunda temporada? Se enteró por un spoiler."),
    ("Pero tranquilo, que él *se acuerda de todo*.", "Pero tranquilo, que él se acuerda de todo."),
    ("Los demás usamos *Manga Tracker*: marcas el capítulo y *listo*.", "Los demás usamos Manga Tracker: marcas el capítulo, y listo."),
    ("Así que mándaselo a ese amigo que dice que *se acuerda de todo*.", "Así que mándaselo a ese amigo que dice que se acuerda de todo."),
    (FIN, FIN)]
SCENES = [
    ([0, 1], Sc_intro(tiles_at=(1, 0)), 0),
    ([2], Sc_reveal("MEMORIA", "PRODIGIOSA"), 0.2),
    ([3], Sc_hud("smug", "MODO 'YO ME ACUERDO'", "ACTIVADO", hud_at=(0, 0, 0.35)), 0),
    ([4], Sc_question(0, "CAPÍTULO ACTUAL", ["¿EP 7?", "¿EP 9?", "¿EP 12?", "¿EP 4?"], "NI IDEA"), 0),
    ([5], Sc_question(1, "ESTADO", ["¿TERMINADO?", "¿ABANDONADO?", "¿EN PAUSA?"], "QUIÉN SABE", st_at=(0, 0, 0.6)), 0),
    ([6], Sc_question(2, "TEMPORADA 2", ["¿EN 2027?", "¿CANCELADA?", "¿ESTE AÑO?"], "SPOILER", st_at=(0, 0, 0.72), st_sub="RECIBIDO"), 0),
    ([7], Sc_hud("smug", "MEMORIA PRODIGIOSA™", "FUNCIONANDO (SEGÚN ÉL)", hud_at=None, arrow=False, glasses=True,
                 meters=[("CONFIANZA", 1.0, "100 %", (0, 0, 0.2), GREEN), ("MEMORIA REAL", 0.03, "3 %", (0, 0, 0.55), RED)]), 0),
    ([8], Sc_phone(90.1, 92.6, callout=(0.09, 0.594, "EP. 7", (0, 0, 0.6))), 0),
    ([9], Sc_ambassador("EMBAJADOR DEL", "\"YO ME ACUERDO\"", st_at=(0, 0, 0.62)), 0),
    ([10], Sc_end(), 1.4)]

if __name__ == "__main__":
    a = sys.argv[1:]; voz = "chica" if "chica" in a else "chico"
    if "chk" in a:
        fr = [(si, T) for si in range(len(SCENES)) for T in (0.25, 1.4, 3.0)]
        print(render(f"{NAME}_{voz}", voz, "n6", LINES, SCENES, OUT, frames=fr))
    else:
        print(render(f"{NAME}_{voz}", voz, "n6", LINES, SCENES, OUT))
