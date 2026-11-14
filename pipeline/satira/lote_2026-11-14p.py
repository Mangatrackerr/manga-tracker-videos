# Lote "todo animado" del 14/11/2026 (reglas nuevas): 10 temas, UNA voz por tema, 5 "contenido" (sin app) + 5 "app" (integrada).
# Gancho ≤ 8 palabras en pantalla desde el segundo 0, pregunta final para comentarios (tarjeta A_preg). Música lo-fi distinta por vídeo.
# Uso: python3 pipeline/satira/lote_2026-11-14p.py [chk] [tema ...]
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["SRC_VIDEO"] = os.path.abspath(os.path.join(HERE, "..", "..", "procesadas", "grabacion_2026-11-02.mp4"))
sys.path.insert(0, HERE)
from animado import *
import voz_viva
voz_viva.patch(M)
M.SUBS += [("Sazae-san", "Sazáe san"), ("Guinness", "Guines"), ("Death Note", "Dez Nout"), ("Fullmetal Alchemist", "Fulmétal Álkemist"),
           ("Attack on Titan", "Atak on Táitan"), ("Solo Leveling", "Sólou Lévelin"), ("Konosuba", "Konosúba"), ("Pikachu", "Pikachú"),
           ("Pokémon", "Pokemon"), ("One Piece", "Uan Pis")]
ES.VOICE_CHAIN = "highpass=f=75,equalizer=f=3000:t=q:w=1.4:g=1.2,acompressor=threshold=0.15:ratio=2:attack=10:release=150,"
ES.MUSIC_VOL = 0.2
LOTE = "2026-11-14p"
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "videos"))
TABS = (76.0, 80.0); LISTAS = (105.0, 107.2); COMEDIA = (31.5, 31.6); FICHA_NOTA = (14.8, 14.9); ESTADOS = (129.5, 129.6)
O = ("open", "open"); PR = ("fist", "point"); PL = ("point", "fist"); OR_ = ("fist", "open")


def _wrap(txt, n=15):
    out, cur = [], ""
    for w in txt.split():
        if cur and len(cur) + 1 + len(w) > n: out.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    if cur: out.append(cur)
    return out


def A_preg(txt, sub="TE LEO EN COMENTARIOS", pal="purple", logo=False):
    """tarjeta final: la pregunta en grande + 'te leo en comentarios'; con logo pequeño solo en los vídeos 'app'"""
    tr = MO.Track([K(0.0, "present", "happy", OR_), K(0.55, "point_up_r", "wink", PR)])
    lines = _wrap(txt)
    def draw(T, d, o):
        im = rays(pal, T); size = 118 if len(lines) <= 2 else 100; y0 = 500
        for i, l in enumerate(lines):
            paste_c(im, big(l, size, YEL, (110, 40, 0)), W / 2, y0 + i * size * 1.08, pop(T, 0.08 + 0.1 * i, 0.3), rot=-3)
        yb = y0 + len(lines) * size * 1.08 + 70
        paste_c(im, pill(sub, 56, path=MB), W / 2, yb, pop(T, 0.5, 0.3) * (1 + 0.04 * math.sin(T * 6)))
        put(im, T, o, tr, cx=W / 2 - 170, sc=0.66, foot=1900)
        if logo:
            paste_c(im, LOGO.resize((170, 170), Image.LANCZOS), 830, 1560, pop(T, 0.7, 0.3))
            paste_c(im, text_img("MANGA TRACKER", LG, 50, stroke=5, shadow=(0, 0, 0)), 830, 1690, pop(T, 0.8, 0.3))
        return im
    return draw, lambda d, o: [(0.08, "pop", 0.7), (0.5, "pop2", 0.8)]


V = {}
# ---------------- CONTENIDO (sin app) ----------------
V["01_sazae_san_1969"] = ("st4", "lofi1", "contenido", [
    ("Este anime se emite desde *1969*.", "Este anime se emite desde mil novecientos sesenta y nueve."),
    ("Se llama *Sazae-san*… y todavía *no ha terminado*.", "Se llama Sazae-san… y todavía no ha terminado."),
    ("Tiene el *récord Guinness* al anime que más tiempo lleva en antena.", "Tiene el récord Guinness al anime que más tiempo lleva en antena."),
    ("Y tú abandonaste One Piece en el *episodio 200*.", "Y tú abandonaste One Piece en el episodio doscientos."),
    ("¿El anime más largo que has visto entero?", "¿Cuál es el anime más largo que has visto entero?")], [
    ([0], A("room", [K(0.0, "point_l", "neutral", PL), K(q(0, 0.6), "shock", "shock", O)], cx=800, sc=0.85,
            props=[dict(k="tv", mode="anime", label="1969"), dict(k="big", txt="DESDE 1969", y=560, size=160, t=0.0)]), 0),
    ([1], A("room", [K(0.0, "point_l", "proud", PL), K(q(0, 0.6), "arms_up", "shock", O)], cx=780, sc=0.85,
            props=[dict(k="calendar", seq=["1969", "1989", "2009", "2026"], x=320, y=820, s=1.2, t=0.05, t_end=(0, 0, 0.6)), dict(k="stamp", txt="Y SIGUE", col=GREEN, t=q(0, 0.65), x=760, y=640)]), 0),
    ([2], A("stage", [K(0.0, "clap", "happy")], cx=780, sc=0.85,
            props=[dict(k="icon", img=IC.trofeo("RÉCORD"), x=300, y=980, s=0.7, anim="rise"), dict(k="pill", txt="RÉCORD GUINNESS", y=560, t=q(0, 0.3))]), 0),
    ([3], A("room", [K(0.0, "sit_wait", "tired")], foot=1700,
            props=[dict(k="sofa"), dict(k="big", txt="EPISODIO 200", y=520, size=130, t=0.1), dict(k="stamp", txt="ABANDONADO", t=q(0, 0.6), y=790)]), 0),
    ([4], A_preg("¿EL ANIME MÁS LARGO QUE HAS VISTO ENTERO?", pal="blue"), 1.4)])

V["02_sub_o_doblaje"] = ("st0", "lofi2", "contenido", [
    ("Solo puedes elegir uno. *Para siempre*.", "Solo puedes elegir uno. Para siempre."),
    ("*Subtitulado*: voces originales… pero no apartas los ojos de las letras.", "Subtitulado: voces originales… pero no apartas los ojos de las letras."),
    ("*Doblaje*: lo ves tranquilo… pero a veces la voz *no le pega nada*.", "Doblaje: lo ves tranquilo… pero a veces la voz no le pega nada."),
    ("Y no vale decir *«depende del anime»*.", "Y no vale decir: depende del anime."),
    ("¿Sub o doblaje? Defiende tu respuesta.", "¿Sub o doblaje? Defiende tu respuesta.")], [
    ([0], A("rays:purple", [K(0.0, "shrug", "smug", O)], props=[dict(k="big", txt="ELIGE UNO", y=520, size=170, t=0.0), dict(k="pill", txt="PARA SIEMPRE", y=700, t=q(0, 0.55))]), 0),
    ([1], A("room", [K(0.0, "point_l", "neutral", PL), K(q(0, 0.6), "scratch", "tired")], cx=800, sc=0.85,
            props=[dict(k="tv", mode="anime", label="SUB"), dict(k="big", txt="SUBTITULADO", y=540, size=130, t=0.0)]), 0),
    ([2], A("room", [K(0.0, "point_l", "happy", PL), K(q(0, 0.55), "scratch", "confused")], cx=800, sc=0.85,
            props=[dict(k="tv", mode="anime", label="ES"), dict(k="big", txt="DOBLAJE", y=540, size=150, t=0.0), dict(k="stamp", txt="NO LE PEGA", t=q(0, 0.75), y=720)]), 0),
    ([3], A("stage", [K(0.0, "finger_up", "smug", PR)], props=[dict(k="big", txt="¿DEPENDE?", y=560, size=150, t=0.0), dict(k="stamp", txt="NO VALE", t=q(0, 0.55), y=760)]), 0),
    ([4], A_preg("¿SUB O DOBLAJE?", sub="DEFIENDE TU RESPUESTA", pal="purple"), 1.4)])

V["03_salvar_solo_uno"] = ("st5", "lofi3", "contenido", [
    ("Solo puedes salvar *uno* de estos tres.", "Solo puedes salvar uno de estos tres."),
    ("*Death Note*… *Fullmetal Alchemist*… o *Attack on Titan*.", "Death Note… Fullmetal Alchemist… o Attack on Titan."),
    ("Los otros dos desaparecen *para siempre*. Nadie los recuerda.", "Los otros dos desaparecen para siempre. Nadie los recuerda."),
    ("Mándaselo a tu amigo, a ver si *elegís el mismo*.", "Mándaselo a tu amigo, a ver si elegís el mismo."),
    ("¿Cuál salvas tú?", "¿Cuál salvas tú?")], [
    ([0], A("stage", [K(0.0, "stand", "neutral"), K(q(0, 0.5), "shock", "shock", O)], props=[dict(k="big", txt="SALVA SOLO 1", y=560, size=170, t=0.0)]), 0),
    ([1], A("rays:gold", [K(0.0, "present", "proud", OR_)], cx=W / 2, foot=1900, sc=0.8,
            props=[dict(k="pill", txt="DEATH NOTE", y=520, t=0.05, rot=-3), dict(k="pill", txt="FULLMETAL ALCHEMIST", y=680, t=q(0, 0.3), rot=2),
                   dict(k="pill", txt="ATTACK ON TITAN", y=840, t=q(0, 0.68), rot=-2)]), 0),
    ([2], A("street", [K(0.0, "bow", "cry")], props=[dict(k="stamp", txt="ADIÓS PARA SIEMPRE", t=q(0, 0.3), y=620, size=96)]), 0),
    ([3], A_send("blue"), 0),
    ([4], A_preg("¿CUÁL SALVAS TÚ?", pal="red"), 1.4)])

V["04_one_piece_500_millones"] = ("st0", "lofi4", "contenido", [
    ("One Piece: más de *500 millones* de copias.", "One Piece: más de quinientos millones de copias."),
    ("Es *récord Guinness*: la serie de cómic con más copias de un solo autor.", "Es récord Guinness: la serie de cómic con más copias de un solo autor."),
    ("Más de *100 tomos*… y todavía *no ha terminado*.", "Más de cien tomos… y todavía no ha terminado."),
    ("La pregunta es: ¿lo has leído entero… o te quedaste *por el camino*?", "La pregunta es: ¿lo has leído entero… o te quedaste por el camino?"),
    ("¿En qué arco te quedaste?", "¿En qué arco te quedaste?")], [
    ([0], A("rays:gold", [K(0.0, "arms_up", "happy", O)], props=[dict(k="rain", kind="cards", t=0.2), dict(k="big", txt="ONE PIECE", y=480, size=150, t=0.0, col=WHITE),
            dict(k="counter", a=0, b=500, pre="+", suf=" MILLONES", y=650, size=130, dur=1.4, t=0.1)]), 0),
    ([1], A("stage", [K(0.0, "clap", "happy")], cx=780, sc=0.85,
            props=[dict(k="icon", img=IC.trofeo("RÉCORD"), x=300, y=980, s=0.7, anim="rise"), dict(k="pill", txt="RÉCORD GUINNESS", y=560, t=q(0, 0.2))]), 0),
    ([2], A("room", [K(0.0, "point_l", "proud", PL), K(q(0, 0.6), "shock", "shock", O)], cx=820, sc=0.8,
            props=[dict(k="books", n=44, x=320, y=1780, dur=1.6), dict(k="big", txt="+100 TOMOS", y=520, size=140, t=0.1), dict(k="stamp", txt="Y SIGUE", col=GREEN, t=q(0, 0.6), x=760, y=760)]), 0),
    ([3], A("room", [K(0.0, "sit_wait", "tired")], foot=1700, props=[dict(k="sofa")], fx=[dict(k="qmarks", t=q(0, 0.4))]), 0),
    ([4], A_preg("¿EN QUÉ ARCO TE QUEDASTE?", pal="gold"), 1.4)])

V["05_pikachu_significa"] = ("st4", "lofi5", "contenido", [
    ("¿Sabes qué significa *Pikachu*?", "¿Sabes qué significa Pikachu?"),
    ("*Pika* es el sonido de una chispa eléctrica, en japonés.", "Pika es el sonido de una chispa eléctrica, en japonés."),
    ("Y *chu*… es el chillido de un *ratón*.", "Y chu… es el chillido de un ratón."),
    ("O sea: *chispa de ratón*. Así de simple.", "O sea: chispa de ratón. Así de simple."),
    ("¿Tu Pokémon favorito de pequeño?", "¿Cuál era tu Pokémon favorito de pequeño?")], [
    ([0], A("rays:gold", [K(0.0, "scratch", "confused")], props=[dict(k="big", txt="¿PIKACHU?", y=560, size=180, t=0.0)], fx=[dict(k="qmarks", t=0.3)]), 0),
    ([1], A("room", [K(0.0, "finger_up", "smug", PR)], props=[dict(k="pill", txt="PIKA = CHISPA", y=600, t=0.1, rot=-3)], fx=[dict(k="sparkle", t=q(0, 0.2))]), 0),
    ([2], A("room", [K(0.0, "point_l", "neutral", PL), K(q(0, 0.6), "shock", "shock", O)], props=[dict(k="pill", txt="CHU = CHILLIDO DE RATÓN", y=600, t=0.1, rot=2)]), 0),
    ([3], A("stage", [K(0.0, "clap", "happy")], props=[dict(k="big", txt="CHISPA + RATÓN", y=560, size=140, t=0.0), dict(k="stamp", txt="ASÍ DE SIMPLE", col=GREEN, t=q(0, 0.55), y=740)]), 0),
    ([4], A_preg("¿TU POKÉMON FAVORITO DE PEQUEÑO?", pal="gold"), 1.4)])

# ---------------- APP (integrada en la historia) ----------------
V["06_solo_leveling_novela"] = ("st5", "lofi6", "app", [
    ("*Solo Leveling* empezó siendo una *novela*.", "Solo Leveling empezó siendo una novela."),
    ("Una novela web coreana de *2016*. Luego fue *manhwa*… y luego *anime*.", "Una novela web coreana de dos mil dieciséis. Luego fue manhwa… y luego anime."),
    ("Unos lo han visto, otros lo han leído… y otros, *las tres cosas*.", "Unos lo han visto, otros lo han leído… y otros, las tres cosas."),
    ("Yo lo apunto todo en *Manga Tracker*: novelas, manhwas y anime, en la misma lista.", "Yo lo apunto todo en Manga Tracker: novelas, manhwas y anime, en la misma lista."),
    ("¿Novela, manhwa o anime?", "¿Tú lo conociste por la novela, el manhwa o el anime?")], [
    ([0], A("room", [K(0.0, "point_l", "neutral", PL), K(q(0, 0.55), "shock", "shock", O)], cx=800, sc=0.85,
            props=[dict(k="big", txt="SOLO LEVELING", y=520, size=150, t=0.0), dict(k="books", n=6, x=320, y=1780, dur=0.4), dict(k="pill", txt="EMPEZÓ COMO NOVELA", y=690, t=q(0, 0.55))]), 0),
    ([1], A("room", [K(0.0, "point_l", "proud", PL)], cx=780, sc=0.85,
            props=[dict(k="calendar", seq=["2016", "2018", "2024"], x=330, y=740, s=1.3, t=0.05, t_end=(0, 0, 0.85)),
                   dict(k="pill", txt="NOVELA", x=330, y=1000, t=0.05), dict(k="pill", txt="MANHWA", x=330, y=1110, t=q(0, 0.5)), dict(k="pill", txt="ANIME", x=330, y=1220, t=q(0, 0.8))]), 0),
    ([2], A("rays:blue", [K(0.0, "shrug", "smug", O), K(q(0, 0.6), "arms_up", "happy", O)], props=[dict(k="pill", txt="LO HA VISTO", x=300, y=720, t=0.1, rot=-4), dict(k="pill", txt="LO HA LEÍDO", x=780, y=860, t=q(0, 0.3), rot=4),
                   dict(k="stamp", txt="LAS TRES", col=YEL, t=q(0, 0.7), y=580)]), 0),
    ([3], A_app(*TABS, callout=(0.87, 0.165, "Y NOVELAS", q(0, 0.45))), 0),
    ([4], A_preg("¿NOVELA, MANHWA O ANIME?", pal="blue", logo=True), 1.4)])

V["07_anime_para_llorar"] = ("st0", "lofi7", "app", [
    ("Hay animes que te destrozan *sin avisar*.", "Hay animes que te destrozan sin avisar."),
    ("Empiezas tranquilo… y en el último episodio estás *llorando en el sofá*.", "Empiezas tranquilo… y en el último episodio estás llorando en el sofá."),
    ("Yo me hice una lista solo con esos, para recomendarlos *a quien se lo merezca*.", "Yo me hice una lista solo con esos, para recomendarlos a quien se lo merezca."),
    ("En *Manga Tracker* creas tus propias listas, *públicas o privadas*.", "En Manga Tracker creas tus propias listas, públicas o privadas."),
    ("¿Qué anime te hizo llorar más?", "¿Qué anime te hizo llorar más? Lo apunto.")], [
    ([0], A("bedroom", [K(0.0, "stand", "neutral"), K(q(0, 0.5), "shock", "shock", O)], props=[dict(k="big", txt="SIN AVISAR", y=560, size=170, t=0.0)]), 0),
    ([1], A("room", [K(0.0, "sit_happy", "happy"), K(q(0, 0.5), "sit", "cry")], foot=1700, props=[dict(k="sofa"), dict(k="pill", txt="ÚLTIMO EPISODIO", y=560, t=q(0, 0.45))]), 0),
    ([2], A("room", [K(0.0, "write", "proud")], foot=1760, props=[dict(k="desk"), dict(k="pill", txt="LISTA: PARA LLORAR", y=600, t=q(0, 0.3), rot=-3)], fx=[dict(k="hearts", t=q(0, 0.5))]), 0),
    ([3], A_app(*LISTAS, callout=(0.73, 0.17, "TUS LISTAS", q(0, 0.45))), 0),
    ([4], A_preg("¿QUÉ ANIME TE HIZO LLORAR MÁS?", pal="pink", logo=True), 1.4)])

V["08_comedia_konosuba"] = ("st4", "lofi8", "app", [
    ("Dime una comedia mejor que *Konosuba*.", "Dime una comedia mejor que Konosuba."),
    ("Te espero. Tranquilo. *No hay prisa*.", "Te espero. Tranquilo. No hay prisa."),
    ("¿Nada? *Ya me lo imaginaba*.", "¿Nada? Ya me lo imaginaba."),
    ("Si te quedas en blanco, en *Manga Tracker* filtras por *Comedia* y te salen todas.", "Si te quedas en blanco, en Manga Tracker filtras por comedia, y te salen todas."),
    ("Escríbela en comentarios. A ver quién gana.", "Escríbela en comentarios. A ver quién gana.")], [
    ([0], A("stage", [K(0.0, "finger_up", "smug", PR)], props=[dict(k="big", txt="¿MEJOR QUE", y=500, size=150, t=0.0), dict(k="big", txt="KONOSUBA?", y=660, size=170, t=0.0)]), 0),
    ([1], A("room", [K(0.0, "sit_wait", "tired")], foot=1700, props=[dict(k="sofa"), dict(k="clock", x=800, y=620, r=140, speed=14), dict(k="pill", txt="NO HAY PRISA", y=830, t=q(0, 0.6))]), 0),
    ([2], A("room", [K(0.0, "shrug", "smug", O)], props=[dict(k="stamp", txt="¿NADA?", t=0.1, y=600)]), 0),
    ([3], A_app(*COMEDIA, mode="still", callout=(0.75, 0.40, "COMEDIA", q(0, 0.5))), 0),
    ([4], A_preg("¿UNA COMEDIA MEJOR?", sub="ESCRÍBELA EN COMENTARIOS", pal="green", logo=True), 1.4)])

V["09_nota_a_naruto"] = ("st5", "lofi9", "app", [
    ("Ponle nota a *Naruto*. Del 1 al 10.", "Ponle nota a Naruto. Del uno al diez."),
    ("Sin pensar. La primera que se te venga *a la cabeza*.", "Sin pensar. La primera que se te venga a la cabeza."),
    ("Yo le pongo un *9*… y sé que alguien me va a sacar *el relleno*.", "Yo le pongo un nueve… y sé que alguien me va a sacar el relleno."),
    ("Mis notas las apunto en *Manga Tracker*: cada obra con su puntuación.", "Mis notas las apunto en Manga Tracker: cada obra con su puntuación."),
    ("¿Qué nota le pones?", "¿Qué nota le pones tú? Te leo.")], [
    ([0], A("rays:red", [K(0.0, "point_r", "smug", ("fist", "point"))], props=[dict(k="big", txt="NOTA A NARUTO", y=520, size=150, t=0.0), dict(k="pill", txt="DEL 1 AL 10", y=690, t=q(0, 0.5))]), 0),
    ([1], A("room", [K(0.0, "scratch", "confused"), K(q(0, 0.6), "finger_up", "happy", PR)], props=[dict(k="pill", txt="SIN PENSAR", y=600, t=0.1)], fx=[dict(k="bulb", t=q(0, 0.6))]), 0),
    ([2], A("stage", [K(0.0, "clap", "happy"), K(q(0, 0.55), "shrug", "smug", O)], props=[dict(k="counter", a=0, b=9, suf=" / 10", y=540, size=170, dur=0.8, t=0.0),
            dict(k="stamp", txt="¿Y EL RELLENO?", t=q(0, 0.7), y=760, size=96)]), 0),
    ([3], A_app(*FICHA_NOTA, mode="still", callout=(0.22, 0.565, "TU NOTA", q(0, 0.45))), 0),
    ([4], A_preg("¿QUÉ NOTA LE PONES?", pal="red", logo=True), 1.4)])

V["10_animes_para_luego"] = ("st0", "lofi10", "app", [
    ("Confiesa: ¿cuántos animes tienes *para luego*?", "Confiesa: ¿cuántos animes tienes para luego?"),
    ("Esos que guardas pensando: *«este finde lo empiezo»*…", "Esos que guardas pensando: este finde lo empiezo…"),
    ("…y llevan ahí *dos años*.", "…y llevan ahí dos años."),
    ("Yo lo miré en mi perfil de *Manga Tracker*: *26 planificados*. Ni uno empezado.", "Yo lo miré en mi perfil de Manga Tracker: veintiséis planificados. Ni uno empezado."),
    ("Di tu número. A ver quién gana.", "Di tu número. A ver quién gana.")], [
    ([0], A("room", [K(0.0, "finger_up", "smug", PR)], props=[dict(k="big", txt="¿PARA LUEGO?", y=560, size=170, t=0.0)]), 0),
    ([1], A("room", [K(0.0, "sit_phone", "happy", phone="r")], foot=1700, props=[dict(k="sofa"), dict(k="pill", txt="ESTE FINDE LO EMPIEZO", y=600, t=q(0, 0.4))]), 0),
    ([2], A("room", [K(0.0, "sit_wait", "tired")], foot=1700, props=[dict(k="sofa"), dict(k="calendar", seq=["2024", "2025", "2026"], x=840, y=860, s=1.0, t=0.0, t_end=(0, 0, 0.7)),
            dict(k="stamp", txt="2 AÑOS", t=q(0, 0.75), y=580)]), 0),
    ([3], A_app(*ESTADOS, mode="still", callout=(0.83, 0.566, "¡26 AQUÍ!", q(0, 0.55))), 0),
    ([4], A_preg("¿CUÁNTOS TIENES PARA LUEGO?", sub="DI TU NÚMERO", pal="purple", logo=True), 1.4)])

VOZ = lambda v: "chico" if v == "st5" else "chica"

if __name__ == "__main__":
    args = sys.argv[1:]; chk = "chk" in args
    names = [a for a in args if a != "chk"]
    for key, (voice, mus, tipo, lines, scenes) in V.items():
        tema = key[3:]
        if names and tema not in names and key not in names: continue
        n = f"{LOTE}_{tema}_{VOZ(voice)}"
        if chk:
            print(render(n, voice, mus, lines, scenes, OUT, frames=[(si, T) for si in range(len(scenes)) for T in (0.05, 1.5)]), flush=True); continue
        if os.path.exists(f"{OUT}/{n}.mp4"): continue
        print(render(n, voice, mus, lines, scenes, OUT), flush=True)
