# Lote generado a partir de grabaciones/grabacion_2026-11-02.mp4
import os, sys, json
os.environ["SRC_VIDEO"]=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","grabaciones","grabacion_2026-11-02.mp4"))
sys.path.insert(0,os.path.dirname(__file__))
from make_video import make, S
FIN="Descárgala gratis en Play Store. ¡El enlace está en mi perfil!"
T={
"estrenos":("PRÓXIMOS|ESTRENOS",[
 (1.0,5.5,"¿Sabes qué animes se estrenan este invierno?"),
 (6.0,8.8,"Con Manga Tracker ves todos los próximos estrenos"),
 (13.0,17.6,"y los guardas en tu lista antes de que salgan.")],FIN,1),
"comedia":("¿QUÉ VEO HOY?",[
 (25.2,26.8,"¿Te apetece algo de comedia?"),
 (26.8,31.6,"Filtra por género en un toque"),
 (32.0,40.0,"y te salen todos los animes de comedia."),
 (52.0,53.9,"Con la sinopsis y la nota de cada uno.")],FIN,2),
"episodios":("MARCA CADA|EPISODIO",[
 (60.0,61.4,"¿Empiezas un anime nuevo?"),
 (61.4,63.2,"Añádelo a tu lista como viendo"),
 (63.2,66.6,"y marca cada episodio que ves, uno a uno."),
 (90.2,93.5,"Así nunca más te pierdes por dónde ibas.")],FIN,3),
"manhwa":("¿LEES|MANHWA?",[
 (76.2,78.2,"¿Lees manhwa?"),
 (78.2,81.6,"Manga Tracker no es solo para anime: también manga y manhwa."),
 (83.0,86.6,"Añade cualquier obra y guarda el capítulo exacto por el que vas.")],FIN,4),
"top_tier":("HAZ TU|TOP TIER",[
 (105.0,106.8,"¿Cuál es tu top tier?"),
 (97.4,100.6,"Añade cualquier obra a tus propias listas,"),
 (107.0,113.0,"públicas o privadas, con todas tus favoritas.")],"¿Cuál es tu top 1? Descarga Manga Tracker gratis en Play Store.",5),
"amigos":("¿QUIÉN HA VISTO|MÁS ANIME?",[
 (119.0,120.8,"¿Quién de tus amigos ha visto más anime?"),
 (121.0,123.2,"Entra en su perfil y mira sus estadísticas"),
 (123.5,125.8,"y los logros que ha desbloqueado."),
 (128.4,131.0,"Y después compáralos con los tuyos.")],FIN,6),
"cuanto_anime":("¿CUÁNTO ANIME|HAS VISTO?",[
 (128.2,129.4,"¿Cuánto anime has visto de verdad?"),
 (129.0,130.6,"Yo llevo 167 obras en mi lista"),
 (130.6,132.8,"y ya tengo diez medallas de doce.")],"¿Cuántas tienes tú? Descárgala gratis en Play Store.",7),
"resumen":("MANGA TRACKER|EN 30 SEGUNDOS",[
 (19.5,24.0,"Esta es Manga Tracker, la app para trackear todo lo que ves y lees."),
 (1.2,5.0,"Próximos estrenos,"),
 (26.8,31.6,"filtros por género,"),
 (61.4,66.6,"episodios uno a uno,"),
 (72.2,74.8,"manga"),(76.2,80.0,"y manhwa,"),
 (105.0,108.0,"tus propias listas,"),
 (119.0,121.0,"amigos"),
 (128.4,132.8,"y logros.")],FIN,8),
}
out=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","videos"))
only=sys.argv[1:] or list(T)
for k in only:
    title,sc,fin,mu=T[k]
    for voz in ("chico","chica"):
        n=f"2026-11-02_{k}_{voz}"
        if os.path.exists(f"{out}/{n}.mp4"): continue
        sc2=[(a,b,t.replace("167","ciento sesenta y siete") if False else t) for a,b,t in sc]
        d=make(n,title,sc2,fin,voz,f"{S}/music/n{mu}.wav",out)
        print(n,round(d,1),flush=True)
