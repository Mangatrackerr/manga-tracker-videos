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
 # ---- lote 2026-11-20x (uno por vídeo) ----
 # oficinista (isekai): pelo rizado negro, gafas, chaqueta gris de traje, camisa blanca, pantalón oscuro
 "ren": dict(skin=(240, 200, 166), hair=(26, 22, 30), hair_l=(66, 60, 80), hair_style="curly", glasses=(30, 30, 40),
             top="jacket", top_c=(110, 116, 130), top_d=(84, 90, 104), top_l=(140, 146, 160), inner=(250, 250, 255),
             bottom="jeans", bottom_c=(46, 48, 60), shoe=(30, 26, 26), sole=(14, 12, 12)),
 # chica de playa (Hawái): pelo largo negro, camiseta de tirantes coral, shorts vaqueros, chanclas amarillas
 "leilani": dict(skin=(196, 140, 100), hair=(24, 18, 20), hair_l=(70, 50, 50), hair_style="long", lashes=True, iris=(70, 40, 20),
                 top="tank", top_c=(255, 120, 100), top_d=(220, 90, 76), top_l=(255, 160, 140), inner=(255, 120, 100),
                 bottom="shorts", bottom_c=(80, 130, 200), socks=(196, 140, 100), shoe=(250, 210, 60), sole=(200, 160, 30), blush=(230, 120, 100)),
 # estudiante del metro: media melena lila, uniforme azul marino con lazo, falda gris
 "sora": dict(skin=(250, 220, 196), hair=(150, 120, 220), hair_l=(190, 165, 245), hair_style="bob", lashes=True, iris=(80, 60, 160),
              top="uniform", top_c=(40, 52, 100), top_d=(28, 38, 76), top_l=(70, 84, 140), inner=(250, 250, 255),
              bottom="skirt", bottom_c=(120, 120, 140), socks=(30, 30, 40), shoe=(60, 40, 30), sole=(30, 20, 14)),
 # chico explorador de bichos: pelo rizado naranja, camiseta verde oliva con raya, pantalón corto beige
 "kaito": dict(skin=(246, 206, 170), hair=(220, 110, 40), hair_l=(250, 160, 90), hair_style="curly",
               top="tee", top_c=(110, 130, 60), top_d=(84, 100, 44), top_l=(140, 160, 84), stripe=(250, 230, 120),
               bottom="shorts", bottom_c=(190, 160, 110), socks=(250, 250, 250), shoe=(120, 80, 50), sole=(60, 40, 24), blush=(250, 150, 120)),
 # barista de la cafetería-librería: coleta castaña, jersey crema, delantal verde
 "nora": dict(skin=(236, 192, 160), hair=(110, 64, 36), hair_l=(160, 104, 66), hair_style="ponytail", lashes=True, iris=(90, 60, 30),
              top="sweater", top_c=(240, 226, 200), top_d=(214, 198, 170), top_l=(252, 242, 222), inner=(240, 226, 200), apron=(50, 110, 80),
              bottom="jeans", bottom_c=(50, 60, 90), shoe=(140, 90, 60), sole=(70, 44, 30)),
 # marinero: pañuelo azul, camiseta de tirantes blanca con raya roja, pantalón de chándal azul
 "hiro": dict(skin=(214, 160, 120), hair=(40, 30, 26), hair_l=(90, 70, 60), hair_style="spiky", hat="bandana", hat_c=(40, 90, 200),
              top="tank", top_c=(250, 250, 250), top_d=(220, 220, 228), top_l=(255, 255, 255), stripe=(220, 50, 60), inner=(250, 250, 250),
              bottom="track", bottom_c=(40, 60, 120), stripe_b=(250, 250, 250), shoe=(250, 250, 250), sole=(80, 80, 96), blush=(220, 130, 110)),
 # chica urbana de neón: pelo corto rosa chicle, chaqueta negra, vaqueros, zapatillas moradas
 "jin": dict(skin=(248, 216, 190), hair=(255, 110, 180), hair_l=(255, 170, 215), hair_style="short", lashes=True, iris=(60, 40, 90),
             top="jacket", top_c=(36, 34, 44), top_d=(24, 22, 30), top_l=(70, 68, 84), inner=(120, 220, 255),
             bottom="jeans", bottom_c=(60, 70, 110), shoe=(150, 90, 230), sole=(80, 40, 140)),
 # chica de gala: pelo largo rubio, chaqueta roja elegante, falda negra
 "mei": dict(skin=(250, 222, 200), hair=(240, 200, 100), hair_l=(255, 230, 160), hair_style="long", lashes=True, iris=(40, 90, 150),
             top="jacket", top_c=(190, 30, 50), top_d=(150, 20, 36), top_l=(225, 70, 84), inner=(30, 26, 34),
             bottom="skirt", bottom_c=(30, 26, 34), socks=(30, 26, 34), shoe=(230, 190, 80), sole=(150, 110, 30)),
 # astrónoma: media melena plateada, gafas, sudadera turquesa, falda azul noche
 "luna": dict(skin=(232, 196, 170), hair=(200, 206, 222), hair_l=(240, 244, 255), hair_style="bob", lashes=True, glasses=(60, 50, 90), iris=(60, 110, 160),
              top="hoodie", top_c=(40, 170, 170), top_d=(28, 130, 130), top_l=(80, 205, 200), inner=(240, 250, 250),
              bottom="skirt", bottom_c=(40, 46, 100), socks=(250, 250, 250), shoe=(40, 40, 60), sole=(20, 20, 30)),
 # chico de karaoke: pelo corto turquesa, cinta roja, camiseta de tirantes amarilla, vaqueros negros
 "dai": dict(skin=(226, 176, 136), hair=(40, 170, 180), hair_l=(110, 215, 220), hair_style="short", hat="headband", hat_c=(230, 40, 60),
             top="tank", top_c=(255, 210, 50), top_d=(220, 170, 20), top_l=(255, 230, 120), inner=(255, 210, 50),
             bottom="jeans", bottom_c=(34, 34, 44), shoe=(250, 250, 250), sole=(230, 40, 60), blush=(240, 140, 110)),
}
