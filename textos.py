datos2 = []
with open("constantes.py", "r", encoding="utf-8") as file:
	for linea in file:
		datos2.append(linea[:-1].split(' = '))


bienvenida1 = "Bienvenidos a Global Warming"

btnFondoRadius = "QPushButton{background-color:  rgb( 18, 144, 56);"\
				 "border-style: inset;"\
				 "border-width: 10px;"\
				 "border-radius: 10px;"\
				 "border-color:  rgb( 11, 100, 39);"\
				 "padding: 10px;}"

btnHover = "QPushButton:hover { background-color: rgb( 43, 165, 80) }" 
btnPressed = "QPushButton:pressed { background-color: rgb( 116, 243, 151) }"

btnFondo2 = "QPushButton{color:white; background-color: rgb( 91, 86, 86) ;"\
				 "border-style: inset;"\
				 "border-width: 10 px;"\
				 "border-radius: 10px;"\
				 "border-color:  rgb( 0, 0, 0);"\
				 "padding: 10 px;}"

btnHover2 = "QPushButton:hover {color:white;  "\
			"background-color: rgb( 115, 109, 109) }" 
btnPressed2 = "QPushButton:pressed {color:white;"  \
			"background-color: rgb( 89, 74, 188) }"

btnFondoRadius3 = "QPushButton{color:white; "\
				 "background-color:  rgb( 21, 71, 121);"\
				 "border-style: inset;"\
				 "border-width: 10 px;"\
				 "border-radius: 10px;"\
				 "border-color:  rgb( 11, 49, 87);"\
				 "padding: 10 px;}"

btnFondoRadius6 = "QPushButton{color:white; "\
				 "background-color:  rgb( 21, 71, 121);"\
				 "border-style: inset;"\
				 "border-width: 10 px;"\
				 "border-radius: 10px;"\
				 "border-color:  rgb( 11, 49, 87);}"

btnHover3 = "QPushButton:hover {color:white;  "\
						"background-color: rgb( 69, 122, 176) }" 

btnFondoRadius4 = "QPushButton{color:white; "\
				 "background-color:  rgb( 21, 71, 121);"\
				 "border-style: inset;"\
				 "border-width: 10 px;"\
				 "border-radius: 10px;"\
				 "border-color:  rgb( 11, 49, 87);"\
				 "padding: 10 px;}"


btnFondoSalir = "QPushButton{color:white; "\
				 "background-color:  rgb( 144, 43, 43);"\
				 "border-style: inset;"\
				 "border-width: 10 px;"\
				 "border-radius: 10px;"\
				 "border-color:  rgb( 131, 5, 5);}"

btnFondoTienda = "QPushButton{color:white;"\
				 "background-color:  rgb( 103, 31, 135);"\
				 "border-style: inset;"\
				 "border-width: 10 px;"\
				 "border-radius: 10px;"\
				 "border-color:  rgb( 72, 5, 131);}"


puntaje_label =  "color:black; background-color:  rgb( 199, 194, 38);"\
				 "border-style: inset;"\
				 "border-width: 5 px;"\
				 "border-radius: 5 px;"\
				 "border-color:  white;"


label_nombre =   "color: white; background-color: black;"\
				 "border-style: inset;"\
				 "border-width: 5 px;"\
				 "border-radius: 5 px;"\
				 "border-color:  white;"

label_titulo =   "color:black; background-color:  rgb( 199, 194, 38);"\
				 "border-style: inset;"\
				 "border-width: 5 px;"\
				 "border-radius: 5 px;"\
				 "border-color:  white;"

item_label = 	 "color:white; background-color:  None;"\
				 "border-color:  white;"


tienda_label = 	 "color:white; background-color:  black;"\
				 "border-color:  white;"


ranking_label =  "color:white; background-color: None;"

mejores_label =  "color: rgb( 138, 24, 24);"

exp_label =  "color:white; background-color:  black;"\
			 "border-style: inset;"\
			 "border-width: 10 px;"\
			 "border-radius: 10 px;"\
			 "border-color:  grey;"\
			 "padding: 10 px;"

stylesheet_expbar = """QProgressBar{color:black; 
					   background-color: white;
					   border: 2px solid grey; 
					   border-radius: 5px}
		               QProgressBar::chunk{
		               background-color: rgb( 2, 108, 116);}"""
		               

spritesheetj1_daño0 = {1: "images/jugador1/sprite_j1.png", 
					   2: "images/jugador1/sprite_j2.png", 
					   3: "images/jugador1/sprite_j3.png", 
					   4: "images/jugador1/sprite_j4.png"}

spritesheetj1_daño1 = {1: "images/jugador1/sprite_j1d1.png", 
					   2: "images/jugador1/sprite_j2d1.png", 
					   3: "images/jugador1/sprite_j3d1.png", 
					   4: "images/jugador1/sprite_j4d1.png"}

spritesheetj1_daño2 = {1: "images/jugador1/sprite_j1d2.png", 
					   2: "images/jugador1/sprite_j2d2.png", 
					   3: "images/jugador1/sprite_j3d2.png", 
					   4: "images/jugador1/sprite_j4d2.png"}

spritesheetj1_daño3 = {1: "images/jugador1/sprite_j1d3.png", 
					   2: "images/jugador1/sprite_j2d3.png", 
					   3: "images/jugador1/sprite_j3d3.png", 
					   4: "images/jugador1/sprite_j4d3.png"}

spritesheetj1 = {0: spritesheetj1_daño0, 
				 1: spritesheetj1_daño1, 
				 2: spritesheetj1_daño2, 
				 3: spritesheetj1_daño3}

spritesheetj2_daño0 = {1: "images/jugador2/sprite_jdos1.png", 
					   2: "images/jugador2/sprite_jdos2.png", 
					   3: "images/jugador2/sprite_jdos3.png", 
					   4: "images/jugador2/sprite_jdos4.png"}

spritesheetj2_daño1 = {1: "images/jugador2/sprite_jdos1d1.png", 
					   2: "images/jugador2/sprite_jdos2d1.png", 
					   3: "images/jugador2/sprite_jdos3d1.png", 
					   4: "images/jugador2/sprite_jdos4d1.png"}

spritesheetj2_daño2 = {1: "images/jugador2/sprite_jdos1d2.png", 
					   2: "images/jugador2/sprite_jdos2d2.png", 
					   3: "images/jugador2/sprite_jdos3d2.png", 
					   4: "images/jugador2/sprite_jdos4d2.png"}

spritesheetj2_daño3 = {1: "images/jugador2/sprite_jdos1d3.png", 
					   2: "images/jugador2/sprite_jdos2d3.png", 
					   3: "images/jugador2/sprite_jdos3d3.png", 
					   4: "images/jugador2/sprite_jdos4d3.png"}

spritesheetj2 = {0: spritesheetj2_daño0, 
				 1: spritesheetj2_daño1, 
				 2: spritesheetj2_daño2, 
				 3: spritesheetj2_daño3}

spritesheet_enemigo1 = {1: "images/enemigo/sprite_e1.png", 
						2: "images/enemigo/sprite_e2.png", 
						3: "images/enemigo/sprite_e3.png", 
						4: "images/enemigo/sprite_e4.png"}

spritesheet_enemigo2 = {1: "images/enemigo/sprite_e1d1.png", 
						2: "images/enemigo/sprite_e2d1.png", 
						3: "images/enemigo/sprite_e3d1.png", 
						4: "images/enemigo/sprite_e4d1.png"}

spritesheet_enemigo3 = {1: "images/enemigo/sprite_e1d2.png", 
						2: "images/enemigo/sprite_e2d2.png", 
						3: "images/enemigo/sprite_e3d2.png", 
						4: "images/enemigo/sprite_e4d2.png"}

spritesheet_enemigo4 = {1: "images/enemigo/sprite_e1d3.png", 
						2: "images/enemigo/sprite_e2d3.png", 
						3: "images/enemigo/sprite_e3d3.png", 
						4: "images/enemigo/sprite_e4d3.png"}
spritesheet_enemigo = {0: spritesheet_enemigo1, 
					   1: spritesheet_enemigo2, 
					   2: spritesheet_enemigo3, 
					   3: spritesheet_enemigo4}

spritesheet_invisible = {1: "images/aux_invisible.png", 
						2: "images/aux_invisible.png", 
						3: "images/aux_invisible.png", 
						4: "images/aux_invisible.png"}


spritesheet_invisible_all = {0: spritesheet_invisible, 
							 1: spritesheet_invisible, 
							 2: spritesheet_invisible, 
							 3: spritesheet_invisible}

# all_sprites_shits = {"j1": spritesheetj1, 
# 					 "j2": spritesheetj2, 
# 					 "enemigo": spritesheet_enemigo, 
# 					 "invisible": spritesheet_invisible_all}


all_sprites_shits = {"enemigo": spritesheet_enemigo, 
					 "j2": spritesheetj2, 
					 "j1": spritesheetj1, 
					 "invisible": spritesheet_invisible_all}

spriteauxiliar = {1: "images/auxliar/sprite_j1.png", 
				  2: "images/auxliar/sprite_j2.png", 
				  3: "images/auxliar/sprite_j3.png", 
				  4: "images/auxliar/sprite_j4.png", 
				  5: "images/auxliar/sprite_j5.png", 
				  6: "images/auxliar/sprite_j6.png", 
				  7: "images/auxliar/sprite_j7.png", 
				  8: "images/auxliar/sprite_j8.png"}

dict_images = {0: "images/fondos/instrucciones0.png", 
			   1: "images/fondos/instrucciones2.png",
			   2: "images/fondos/instrucciones3.png"}

bar_style_j = """QProgressBar{color:black; 
				 background-color: red;
				 border: 2px solid grey; 
				 border-radius: 5px}
                 QProgressBar::chunk{
                 background-color: green;
                 width: 10px;
                 margin: 0px}"""

bar_style_e = """QProgressBar{color:black; 
				 background-color:  None;
				 border: 2px solid grey; 
				 border-radius: 5px}
                 QProgressBar::chunk{
                 color: red;
                 background-color: red;
                 width: 10px;
                 margin: 0px}"""
style_cargando = """QProgressBar::chunk{
	                background-color: rgb( 54, 76, 100);
	                width: 10px;
	                margin: 1px}"""
bar_styles = {"j1": bar_style_j, "enemigo": bar_style_e, "j2": bar_style_j}

image_jugador = {"j1": "images/jugador1/sprite_j1.png", 
				 "enemigo": "images/jugador1/sprite_e1.png", 
				 "j2": "images/jugador1/sprite_j2.png",
				 "invisible": "images/aux_invisible.png"}

s = "Sabías que "

pseudo_datos = ["en el mundo existen ocho principales especies de osos.",
	"los osos polares son los más carnívoros entre los osos.",
	"los osos polares pueden nadar entre 30 y 100 kms sin parar.",
	"los osos polares comen 30 kg de comida diario.",
	"el deshielo está disminuyendo la tasa de natalidad de los osos polares.",
	"un panda hembra es fértil solo tres días al año.",
	"para estudiar mejor a los pandas los científicos se disfrazan de ellos.",
	"un panda puede defecar hasta 40 veces al día",
	"el bambú es la mayor parte de la alimentación de un panda.",
	"el panda es el logo de la World Wildlife Foundation.",
	"el oso pardo puede llegar a pesar más de 600 kgs.",
	"los osos son muy inteligentes.",
				"los koalas no son osos. :P"]
datos = [s + i for i in pseudo_datos]
pj1_iniciales = {0: "images/jugador1/sprite_j1.png", 
				 1: "images/jugador1/sprite_j2.png", 
				 2: "images/jugador1/sprite_j3.png", 
				 3: "images/jugador1/sprite_j4.png"}
pj2_iniciales = {0: "images/jugador2/sprite_jdos1.png", 
				 1: "images/jugador2/sprite_jdos2.png", 
				 2: "images/jugador2/sprite_jdos3.png", 
				 3: "images/jugador2/sprite_jdos4.png"}


image_coin = ["images/items/coin1.png", "images/items/coin1.png",
			  "images/items/coin1.png", "images/items/coin2.png",
			  "images/items/coin3.png", "images/items/coin4.png",
			  "images/items/coin5.png", "images/items/coin6.png",
			  "images/items/coin7.png", "images/items/coin8.png",
			  "images/items/coin8.png", "images/items/coin8.png",
			  "images/items/coin7.png", "images/items/coin6.png",
			  "images/items/coin5.png", "images/items/coin4.png",
			  "images/items/coin3.png", "images/items/coin2.png"]

# image_coin = ["images/items/coinaux.png", "images/items/coinaux.png",
# 			  "images/items/coinaux.png", "images/items/coinaux.png",
# 			  "images/items/coinaux.png", "images/items/coinaux.png",
# 			  "images/items/coinaux.png", "images/items/coinaux.png",
# 			  "images/items/coinaux.png", "images/items/coinaux.png",
# 			  "images/items/coinaux.png", "images/items/coinaux.png",
# 			  "images/items/coinaux.png", "images/items/coinaux.png",
# 			  "images/items/coinaux.png", "images/items/coinaux.png",
# 			  "images/items/coinaux.png", "images/items/coinaux.png"]

# image_food_pardo = ["images/items/meataux.png", "images/items/meataux.png",
# 				    "images/items/meataux.png", "images/items/meataux.png",
# 				    "images/items/meataux.png", "images/items/meataux.png",
# 				    "images/items/meataux.png", "images/items/meataux.png",
# 				    "images/items/meataux.png", "images/items/meataux.png"]

# image_food_panda = ["images/items/fishaux.png", "images/items/fishaux.png",
# 				    "images/items/fishaux.png", "images/items/fishaux.png",
# 				    "images/items/fishaux.png", "images/items/fishaux.png",
# 				    "images/items/fishaux.png", "images/items/fishaux.png",
# 				    "images/items/fishaux.png", "images/items/fishaux.png"]

image_food_pardo = ["images/items/meat1.png", "images/items/meat2.png",
				    "images/items/meat3.png", "images/items/meat4.png",
				    "images/items/meat5.png", "images/items/meat6.png",
				    "images/items/meat7.png", "images/items/meat8.png",
				    "images/items/meat9.png", "images/items/meat10.png"]

image_food_panda = ["images/items/bambu1.png", "images/items/bambu2.png",
				    "images/items/bambu3.png", "images/items/bambu4.png",
				    "images/items/bambu5.png", "images/items/bambu6.png",
				    "images/items/bambu7.png", "images/items/bambu8.png",
				    "images/items/bambu9.png", "images/items/bambu10.png"]

image_trap_activated = ["images/items/trap_activada3.png",
						"images/items/trap_activada2.png",
						"images/items/trap_activada1.png",
						"images/items/trap1.png" ]
image_trap = ["images/items/trap1.png", "images/items/trap2.png",
			  "images/items/trap3.png", "images/items/trap4.png",
			  "images/items/trap4.png"]


image_food = {"j1": image_food_pardo, "j2": image_food_panda}
sound = {"coin": "sounds/coin.wav", "food": "sounds/eating.wav",
		 "trampa": "sounds/timer.wav", "safe_zone": None}

image_safe_zone = ["images/items/safe_zone.png",
				   "images/items/safe_zone2.png"]

jugador1_muerto =  ["images/jugador1/oso_dead1.png", 
					"images/jugador1/oso_dead2.png",
				    "images/jugador1/oso_dead3.png", 
				    "images/jugador1/oso_dead4.png",
				    "images/jugador1/oso_dead5.png", 
				    "images/jugador1/oso_dead6.png"]

jugador2_muerto =  ["images/jugador2/polar_dead1.png",
					"images/jugador2/polar_dead2.png",
				    "images/jugador2/polar_dead3.png", 
				    "images/jugador2/polar_dead4.png",
				    "images/jugador2/polar_dead5.png", 
				    "images/jugador2/polar_dead6.png"]

enemigo_muerto =  ["images/enemigo/polar_dead1.png", 
				   "images/enemigo/polar_dead2.png",
				   "images/enemigo/polar_dead3.png", 
				   	"images/enemigo/polar_dead4.png",
				   "images/enemigo/polar_dead5.png", 
				   	"images/enemigo/polar_dead6.png"]

entidad_muerta = {"j1": jugador1_muerto, 
				  "j2": jugador2_muerto, 
				  "enemigo": enemigo_muerto}

imagen_ranking = ["images/ranking/coin1.png",
				  "images/ranking/coin2.png",
				  "images/ranking/coin3.png"]

armadura = "Armadura\nPrecio: 1200 ptos\n+30% vida máxima"

garras = "Garras\nPrecio: 1200 ptos\n+50% poder de ataque"

botas = "Alas\nPrecio: 800 ptos\n+30% vel. de movimiento"

costo = {"images/tienda/armor.png": 1200, 
		 "images/tienda/garras.png":1200, 
		 "images/tienda/botas.png": 800}

alphas_level = [1 / 10, 1 / 8, 1 / 6, 1 / 4, 1 / 2]
matriz_level = [[1, 5, 1], [1, 6, 3], [3, 7, 5], 
				[5, 9, 7], [7, 10, 9]]

# from random import triangular
# from funciones import *

# for i in range(100):
# 	print(triang(
#                     matriz_level[0]))