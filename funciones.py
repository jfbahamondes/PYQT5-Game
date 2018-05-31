from random import random, triangular, expovariate
from math import degrees, atan2


def prob_uniforme(p):
	return random() < p

def decimales(number, d):
	return int(number * (10 ** d))/ (10 ** d)


def puntajes_to_string(linea, aux = None):
	text = "{} alcanzó {} puntos.".format(linea[0], linea[1])
	return text

def ordenar_puntajes(lineas):
	lineas = lineas.split("\n")
	if lineas[-1] == "":
		lineas = lineas[:-1]

	lineas = [i.split(";") for i in lineas]
	lineas.sort(key=lambda linea: int(linea[1]), reverse=True)
	return lineas

def angulo_entre_player(pos_pl, pos_enemigo):
    x_atacante = pos_enemigo[0]
    y_atacante = pos_enemigo[1]

    x_target = pos_pl[0]
    y_target = pos_pl[1]
    ang = degrees(atan2(y_target - y_atacante, x_target - x_atacante)) + 90
    return ang

def entre(valor1, valor2, valor3):
	return (valor1 > valor2 and valor1 < valor3)

def triang(lista):
	return triangular(lista[0], lista[1], lista[2])

if __name__ == "__main__":
	print(puntajes_to_string(ordenar_puntajes("2;4\n1;3\n")[0]))