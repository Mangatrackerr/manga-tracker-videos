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
 # ---- lote 2026-11-21y (uno por vídeo) ----
 # chica de la lavandería: moños dobles verde menta, sudadera lila con capucha, pantalón de chándal gris
 "momo": dict(skin=(246, 212, 186), hair=(110, 200, 170), hair_l=(160, 230, 205), hair_style="buns", lashes=True, iris=(50, 110, 90),
              top="hoodie", top_c=(190, 160, 230), top_d=(160, 128, 205), top_l=(215, 190, 245), inner=(250, 250, 255),
              bottom="track", bottom_c=(130, 130, 145), stripe_b=(250, 250, 250), shoe=(250, 250, 250), sole=(150, 150, 170), blush=(255, 160, 170)),
 # chica del futuro: media melena azul eléctrico, chaqueta blanca con interior amarillo, falda azul marino
 "hana": dict(skin=(250, 224, 202), hair=(50, 120, 230), hair_l=(110, 170, 250), hair_style="bob", lashes=True, iris=(40, 80, 170),
              top="jacket", top_c=(245, 246, 250), top_d=(210, 214, 225), top_l=(255, 255, 255), inner=(255, 210, 60),
              bottom="skirt", bottom_c=(30, 50, 110), socks=(255, 255, 255), shoe=(230, 60, 60), sole=(150, 30, 30), blush=(255, 160, 170)),
 # futbolista: pelo de punta negro, cinta blanca, camiseta blanca con raya azul, pantalón corto azul
 "rio": dict(skin=(214, 166, 126), hair=(28, 22, 20), hair_l=(70, 60, 56), hair_style="spiky", hat="headband", hat_c=(250, 250, 250),
             top="tee", top_c=(250, 250, 252), top_d=(215, 218, 228), top_l=(255, 255, 255), stripe=(40, 90, 220),
             bottom="shorts", bottom_c=(40, 90, 220), socks=(250, 250, 250), shoe=(30, 30, 36), sole=(250, 250, 250), blush=(220, 130, 110)),
 # chica de la pizzería: coleta pelirroja, pañuelo rojo, camiseta verde con raya blanca, vaqueros
 "yui": dict(skin=(252, 222, 200), hair=(200, 80, 40), hair_l=(240, 130, 80), hair_style="ponytail", lashes=True, iris=(60, 110, 60), hat="bandana", hat_c=(210, 40, 40),
             top="tee", top_c=(40, 150, 80), top_d=(28, 116, 60), top_l=(80, 185, 115), stripe=(250, 250, 250),
             bottom="jeans", bottom_c=(60, 80, 130), shoe=(250, 250, 250), sole=(210, 40, 40), blush=(250, 150, 140)),
 # chico del parque de cerezos: pelo rizado castaño claro, gafas redondas, jersey rosa palo, pantalón beige
 "takumi": dict(skin=(244, 208, 176), hair=(150, 100, 60), hair_l=(200, 150, 100), hair_style="curly", glasses=(70, 50, 40),
                top="sweater", top_c=(240, 170, 190), top_d=(215, 140, 162), top_l=(250, 200, 215), inner=(250, 250, 250),
                bottom="jeans", bottom_c=(200, 180, 140), shoe=(110, 70, 50), sole=(60, 40, 26)),
 # detective: pelo largo castaño oscuro, gafas, gabardina beige, falda marrón
 "iris": dict(skin=(240, 204, 176), hair=(70, 40, 30), hair_l=(120, 80, 60), hair_style="long", lashes=True, glasses=(30, 30, 30), iris=(90, 60, 40),
              top="jacket", top_c=(200, 170, 120), top_d=(170, 140, 96), top_l=(225, 200, 150), inner=(250, 250, 250),
              bottom="skirt", bottom_c=(100, 64, 44), socks=(40, 36, 40), shoe=(60, 40, 30), sole=(30, 20, 14)),
 # chico gótico del huerto: pelo de punta blanco, chaqueta negra con interior rojo, vaqueros negros
 "kuro": dict(skin=(232, 214, 210), hair=(235, 235, 240), hair_l=(255, 255, 255), hair_style="spiky", iris=(170, 40, 60),
              top="jacket", top_c=(30, 28, 36), top_d=(18, 16, 22), top_l=(64, 60, 74), inner=(190, 30, 50),
              bottom="jeans", bottom_c=(26, 26, 32), shoe=(60, 20, 30), sole=(20, 10, 14)),
 # jugadora de voleibol: coleta negra, cinta naranja, camiseta de tirantes naranja con raya negra, pantalón corto negro
 "nami": dict(skin=(226, 180, 140), hair=(26, 22, 24), hair_l=(70, 62, 66), hair_style="ponytail", lashes=True, iris=(80, 50, 30), hat="headband", hat_c=(255, 140, 30),
              top="tank", top_c=(255, 140, 30), top_d=(225, 110, 20), top_l=(255, 175, 90), stripe=(30, 30, 36), inner=(255, 140, 30),
              bottom="shorts", bottom_c=(30, 30, 36), socks=(250, 250, 250), shoe=(250, 250, 250), sole=(255, 140, 30), blush=(240, 140, 110)),
 # ---- lote 2026-11-27z (uno por vídeo) ----
 # chico de la aldea: pelo corto negro, cinta verde, chaqueta verde oliva, chándal gris
 "goro": dict(skin=(226, 182, 146), hair=(24, 20, 22), hair_l=(66, 60, 64), hair_style="short", hat="headband", hat_c=(60, 140, 80),
              top="jacket", top_c=(100, 120, 70), top_d=(76, 94, 50), top_l=(130, 150, 96), inner=(40, 40, 50),
              bottom="track", bottom_c=(110, 110, 124), stripe_b=(40, 40, 50), shoe=(40, 40, 46), sole=(20, 20, 24)),
 # jueza: media melena granate, chaqueta negra, camisa blanca, falda gris
 "rina": dict(skin=(244, 210, 184), hair=(130, 30, 50), hair_l=(180, 70, 90), hair_style="bob", lashes=True, iris=(90, 40, 50),
              top="jacket", top_c=(30, 28, 36), top_d=(18, 16, 22), top_l=(64, 60, 74), inner=(250, 250, 255),
              bottom="skirt", bottom_c=(110, 110, 124), socks=(30, 30, 36), shoe=(30, 26, 30), sole=(14, 12, 14)),
 # chico del planeta: pelo rizado castaño oscuro, sudadera roja, chándal negro
 "kenta": dict(skin=(200, 150, 112), hair=(70, 44, 30), hair_l=(120, 84, 60), hair_style="curly",
               top="hoodie", top_c=(210, 50, 56), top_d=(170, 34, 40), top_l=(240, 96, 100), inner=(250, 250, 250),
               bottom="track", bottom_c=(30, 30, 38), stripe_b=(250, 250, 250), shoe=(250, 250, 250), sole=(210, 50, 56), blush=(220, 120, 100)),
 # chica del desván: coleta castaña clara, jersey mostaza, vaqueros
 "chiho": dict(skin=(250, 220, 196), hair=(170, 120, 70), hair_l=(210, 165, 110), hair_style="ponytail", lashes=True, iris=(90, 70, 40),
               top="sweater", top_c=(230, 180, 50), top_d=(200, 150, 30), top_l=(245, 205, 100), inner=(250, 250, 250),
               bottom="jeans", bottom_c=(70, 90, 140), shoe=(200, 70, 60), sole=(120, 40, 30), blush=(255, 160, 150)),
 # chica del kiosco: moños negros, chaqueta turquesa, falda blanca
 "aya": dict(skin=(238, 196, 164), hair=(30, 24, 30), hair_l=(76, 66, 80), hair_style="buns", lashes=True, iris=(40, 90, 110),
             top="jacket", top_c=(40, 170, 180), top_d=(28, 130, 140), top_l=(90, 205, 210), inner=(250, 240, 120),
             bottom="skirt", bottom_c=(245, 245, 250), socks=(40, 40, 50), shoe=(40, 40, 50), sole=(20, 20, 24)),
 # montañero: pelo de punta castaño, pañuelo verde, chaqueta naranja, chándal azul
 "sho": dict(skin=(236, 196, 160), hair=(110, 70, 40), hair_l=(160, 110, 70), hair_style="spiky", hat="bandana", hat_c=(40, 150, 90),
             top="jacket", top_c=(250, 130, 40), top_d=(220, 100, 20), top_l=(255, 170, 90), inner=(250, 250, 250),
             bottom="track", bottom_c=(40, 70, 150), stripe_b=(250, 250, 250), shoe=(120, 80, 50), sole=(60, 40, 24), blush=(240, 140, 120)),
 # chica del gimnasio: pelo corto blanco, cinta roja, camiseta de tirantes gris, chándal negro
 "kana": dict(skin=(214, 168, 130), hair=(240, 240, 245), hair_l=(255, 255, 255), hair_style="short", lashes=True, iris=(150, 60, 50), hat="headband", hat_c=(220, 40, 50),
              top="tank", top_c=(130, 134, 146), top_d=(104, 108, 120), top_l=(160, 164, 176), inner=(130, 134, 146),
              bottom="track", bottom_c=(26, 26, 32), stripe_b=(220, 40, 50), shoe=(250, 250, 250), sole=(220, 40, 50), blush=(230, 130, 110)),
 # estudiante del aula: pelo corto azul marino, gafas, uniforme con lazo, pantalón gris
 "yuto": dict(skin=(246, 212, 182), hair=(30, 40, 90), hair_l=(70, 84, 140), hair_style="short", glasses=(40, 40, 50),
              top="uniform", top_c=(60, 64, 76), top_d=(44, 48, 58), top_l=(90, 94, 108), inner=(250, 250, 255),
              bottom="jeans", bottom_c=(110, 112, 124), shoe=(50, 36, 30), sole=(24, 18, 14)),
}
