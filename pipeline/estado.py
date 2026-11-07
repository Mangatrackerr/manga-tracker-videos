"""Gestión de la cola de publicaciones (estado.json en la raíz del repo).

Uso:
  python3 pipeline/estado.py registrar <lote> <textos.json> [estilo]  # añade los vídeos videos/<lote>_*.mp4 a la cola (estilo: gancho|clasico, por defecto clasico)
  python3 pipeline/estado.py elegir <n>                         # muestra (JSON) los n siguientes vídeos a publicar
  python3 pipeline/estado.py marcar <id> <fecha_hora>           # registra que <id> se ha programado para <fecha_hora>
  python3 pipeline/estado.py desmarcar <id> <fecha_hora>        # deshace un marcar (si se sustituye un post)
  python3 pipeline/estado.py resumen
Reglas de elección:
  0. Los vídeos de estilo "gancho" (motion graphics, pipeline/gancho/) van SIEMPRE antes que los "clasico":
     nuevos gancho > resubida gancho > nuevos clasico > resubida clasico (los clásicos quedan de reserva).
  1. Primero vídeos nunca programados (por orden de alta, alternando temas).
  2. Si no quedan, se reutilizan los programados hace más tiempo (resubida),
     priorizando la versión de voz que menos veces se ha usado.
  3. Nunca dos vídeos del mismo tema en el mismo bloque de n.
"""
import json, os, sys, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EST = os.path.join(ROOT, "estado.json")
RAW = "https://raw.githubusercontent.com/Mangatrackerr/manga-tracker-videos/main/videos/"


def load():
    if os.path.exists(EST):
        return json.load(open(EST, encoding="utf-8"))
    return {"blogId": "7829643", "zona": "Europe/Madrid",
            "horarios": ["10:00", "14:30", "19:00"], "videos": []}


def save(e):
    json.dump(e, open(EST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def registrar(lote, textos_path, estilo="clasico"):
    e = load(); textos = json.load(open(textos_path, encoding="utf-8"))
    ids = {v["id"] for v in e["videos"]}
    # orden: primero todas las versiones "chico" de cada tema, luego las "chica"
    nuevos = []
    temas = list(textos.items())
    # clásico: primero todos los "chico" y luego los "chica".
    # gancho: primera pasada alternando voz por tema (chica, chico, chica…), segunda pasada con la otra voz.
    if estilo == "gancho":
        orden = [(v, tema, t) for pas in (0, 1) for i, (tema, t) in enumerate(temas) for v in [("chica", "chico")[(i + pas) % 2]]]
    else:
        orden = [(v, tema, t) for v in ("chico", "chica") for tema, t in temas]
    for voz, tema, t in orden:
        if True:
            vid = f"{lote}_{tema}_{voz}"
            if vid in ids or not os.path.exists(os.path.join(ROOT, "videos", vid + ".mp4")):
                continue
            nuevos.append({"id": vid, "lote": lote, "tema": f"{lote}_{tema}", "voz": voz,
                           "url": RAW + vid + ".mp4", "titulo": t["titulo"], "texto": t["texto"], "estilo": estilo,
                           "programado": []})
    e["videos"] += nuevos; save(e); print(f"registrados {len(nuevos)}")


def elegir(n):
    e = load(); vs = e["videos"]
    def pools(est):
        n = [v for v in vs if not v["programado"] and v.get("estilo", "clasico") == est]
        u = sorted([v for v in vs if v["programado"] and v.get("estilo", "clasico") == est], key=lambda v: (v["programado"][-1], len(v["programado"])))
        return n, u
    ng, ug = pools("gancho"); nc, uc = pools("clasico")
    nuevos, usados = ng + nc, ug + uc
    orden = (ng, ug, nc, uc)
    out, temas = [], set()
    for pool in orden:
        for v in pool:
            if len(out) >= n: break
            if v["tema"] in temas or v in out: continue
            out.append(v); temas.add(v["tema"])
    # si aún faltan (pocos temas), rellenar sin la restricción de tema
    for v in ng + ug + nc + uc:
        if len(out) >= n: break
        if v not in out: out.append(v)
    print(json.dumps(out, ensure_ascii=False, indent=1))


def desmarcar(vid, fecha):
    e = load()
    for v in e["videos"]:
        if v["id"] == vid and fecha in v["programado"]:
            v["programado"].remove(fecha); save(e); print("ok"); return
    sys.exit(f"no existe {vid} en {fecha}")


def marcar(vid, fecha):
    e = load()
    for v in e["videos"]:
        if v["id"] == vid:
            v["programado"].append(fecha); save(e); print("ok"); return
    sys.exit(f"no existe {vid}")


def resumen():
    e = load(); vs = e["videos"]
    print(f"{len(vs)} vídeos | sin programar: {sum(1 for v in vs if not v['programado'])}")
    fechas = sorted(f for v in vs for f in v["programado"])
    print("última programación:", fechas[-1] if fechas else "ninguna")


if __name__ == "__main__":
    c = sys.argv[1]
    {"registrar": lambda: registrar(sys.argv[2], sys.argv[3], *sys.argv[4:5]),
     "desmarcar": lambda: desmarcar(sys.argv[2], sys.argv[3]),
     "elegir": lambda: elegir(int(sys.argv[2])),
     "marcar": lambda: marcar(sys.argv[2], sys.argv[3]),
     "resumen": resumen}[c]()
