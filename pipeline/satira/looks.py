# Personajes distintos para cada vídeo (16/11/2026). Uso: MO.set_look(**LOOKS["nombre"]).
LOOKS = {
 # chico cocinero de ramen: pañuelo rojo, chaqueta blanca, delantal azul marino
 "kenji": dict(skin=(236, 190, 150), hair=(30, 24, 22), hair_l=(70, 58, 52), hair_style="short", hat="bandana", hat_c=(215, 50, 50),
               top="chef", top_c=(248, 248, 250), top_d=(220, 220, 228), top_l=(255, 255, 255), inner=(215, 50, 50), apron=(40, 52, 96),
               bottom="jeans", bottom_c=(40, 40, 52), shoe=(40, 40, 46), sole=(20, 20, 24)),
 # chica de cine: dos moños rosas, chaqueta amarilla, falda vaquera
 "yuna": dict(skin=(250, 214, 190), hair=(240, 120, 170), hair_l=(255, 170, 205), hair_style="buns", lashes=True, iris=(90, 60, 160),
              top="jacket", top_c=(250, 196, 50), top_d=(210, 150, 20), top_l=(255, 220, 110), inner=(40, 36, 60),
              bottom="skirt", bottom_c=(70, 100, 170), socks=(255, 255, 255), shoe=(230, 60, 90), sole=(150, 30, 60), blush=(255, 150, 170)),
 # chica de biblioteca: pelo largo granate, gafas, jersey verde, falda de cuadros
 "aiko": dict(skin=(244, 206, 176), hair=(120, 34, 44), hair_l=(170, 70, 80), hair_style="long", lashes=True, glasses=(40, 30, 40), iris=(60, 120, 80),
              top="sweater", top_c=(70, 140, 100), top_d=(50, 110, 78), top_l=(100, 170, 130), inner=(250, 250, 250),
              bottom="skirt", bottom_c=(110, 70, 60), socks=(40, 36, 50), shoe=(80, 50, 40), sole=(40, 26, 20)),
 # chico de montaña: piel morena, pelo de punta castaño, gorra hacia atrás verde, camiseta naranja con raya
 "taro": dict(skin=(176, 120, 84), hair=(90, 56, 30), hair_l=(130, 90, 54), hair_style="spiky", hat=None,
              top="tee", top_c=(40, 160, 150), top_d=(28, 120, 112), top_l=(70, 190, 180), stripe=(250, 250, 250),
              bottom="shorts", bottom_c=(60, 60, 80), socks=(250, 250, 250), shoe=(250, 200, 40), sole=(150, 110, 20), blush=(200, 110, 90)),
 # chica deportista: pelo corto azul en coleta, chándal rojo con raya blanca
 "mika": dict(skin=(232, 180, 140), hair=(40, 60, 130), hair_l=(80, 110, 190), hair_style="ponytail", lashes=True, hat="headband", hat_c=(255, 255, 255),
              top="jacket", top_c=(220, 50, 60), top_d=(170, 30, 40), top_l=(245, 100, 100), inner=(255, 255, 255),
              bottom="track", bottom_c=(200, 40, 52), stripe=(255, 255, 255), shoe=(255, 255, 255), sole=(60, 60, 80)),
}
