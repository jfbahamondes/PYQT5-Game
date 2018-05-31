from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer, QSize, QUrl
from PyQt5.QtMultimedia import QSoundEffect, QSound
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QSizePolicy)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout)
from PyQt5.QtWidgets import (QPushButton, QLabel, QLineEdit, QAction)
from PyQt5.QtGui import QPixmap, QTransform, QFont
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, 
                            QLabel, QProgressBar,QToolButton,
                             QLineEdit, QHBoxLayout, QVBoxLayout)
import sys
import time
from math import sin, cos, radians
from random import choice, random
from textos import *
from entidades import Entidades
from events import *
import funciones as f


class Jugador(Entidades):

    trigger = pyqtSignal(MovePlayerEvent)
    trigger_bar = pyqtSignal(MoveBarEvent)
    trigger_attack = pyqtSignal(AttackEvent)
    trigger_dead = pyqtSignal(DeadEvent)
    trigger_set = pyqtSignal(SetEvent)
    trigger_nivel = pyqtSignal(PasarNivelEvent)

    id_ = 1

    def __init__(self, *args):
        super().__init__(*args)
        self.teclado_jugador1 = {Qt.Key_A: False, Qt.Key_S: False,
                                 Qt.Key_D: False, Qt.Key_W: False,
                                 }
        self.trigger.connect(self.parent.actualizar_imagen)
        self.trigger_bar.connect(self.parent.actualizar_bar)
        self.trigger_attack.connect(self.parent.atacar)
        self.trigger_dead.connect(self.parent.dead_player)
        self.trigger_set.connect(self.parent.set_objeto)
        self.trigger_nivel.connect(self.parent.pasar_nivel)
        self.ataque_w = False
        self.ataque_s = False
        self.threads = []
        self.__experiencia = 0
        self.paso_quina = False
        self.__puntaje = int(datos2[0][1]) + 10000
        self.id = "Jugador {}".format(Jugador.id_)
        Jugador.id_ += 1
        self.cueva = None
        self.aux_tipo = self.tipo
        self.experienciaBar = None
        self.puntaje_label = None
        self.stoped = False
        self.first_tipo = self.tipo

    @property
    def experiencia(self):
        return self.__experiencia

    @experiencia.setter
    def experiencia(self, value):

        if value > 500 and not self.paso_quina:
            self.tamaño = min(self.tamaño + 1, 10)
            self.paso_quina = True

        if value >= 1000:
            self.__experiencia = 0
            self.trigger_set.emit(SetEvent(
                self.experienciaBar, self.experiencia
                ))
            self.tamaño = min(self.tamaño + 1, 10)
            self.paso_quina = False
            self.pasar_nivel()

        else:
            self.__experiencia = value
            self.trigger_set.emit(SetEvent(
                self.experienciaBar, self.experiencia
                ))

    @property
    def puntaje(self):
        return self.__puntaje

    @puntaje.setter
    def puntaje(self, value):
        self.__puntaje = value
        self.trigger_set.emit(SetEvent(
            self.puntaje_label, self.puntaje, "puntaje")
        )

    def chequear_ataque(self):
        if self.enemigo_atacado is not None:
            if self.tipo != "invisible":
                self.enemigo_atacado.atacar()
                self.atacar()
                if self.no_paso:
                    self.trigger_attack.emit(AttackEvent(
                        self, self.enemigo_atacado
                        ))
                    self.no_paso = False


    def chequear_distancias_items(self):
        for i in self.items:
            aux = i.distance_to_player(self)
            if i == self.cueva:
                if not aux[0]:
                    self.mostrarse()
                    self.cueva = None
            if aux[0]:
                if i.tipo == "safe_zone":
                    self.esconderse()
                    self.cueva = i

                else:
                    i.tomar(self)
                    i.tomado = True

    def chequear_distancias(self):
        a = radians(self.angulo)
        seno = sin(a) * self.velocidad_x
        coseno = cos(a) * self.velocidad_y
        enemigos_cerca = False

        for j, i in enumerate(self.threads):
            if i.is_dead:
                self.threads.pop(j)
            else:
                aux = i.distance_to_player()
                if aux[0]:
                    if self.tipo != "invisible":

                        enemigos_cerca = True
                        # if self.teclado_jugador1[Qt.Key_W] and not self.ataque_w and not self.ataque_s:
                        #     self.ataque_w = True

                        # elif self.teclado_jugador1[Qt.Key_S] and not self.ataque_w and not self.ataque_s:
                        #     self.ataque_s = True 
                        # if aux[2] > 0: #estoy abajo de el
                        #     if self.angulo > 0 and self.angulo < 90 or self.angulo > 270 and self.angulo < 360:
                        #         self.ataque_w = True
                        #         self.ataque_s = False
                        #         self.pseudo_angulo = 0
                        #     else:
                        #         self.ataque_s = True
                        #         self.ataque_w = False
                        #         self.pseudo_angulo = 180
                        # else:#estoy arriba
                        #     if self.angulo > 0 and self.angulo < 90 or self.angulo > 270 and self.angulo < 360:
                        #         self.ataque_s = True
                        #         self.ataque_w = False
                        #         self.pseudo_angulo = 180

                        #     else:
                        #         self.ataque_w = True
                        #         self.ataque_s = False
                        #         self.pseudo_angulo = 0

                        i.contacto_player = True
                        i.angulo = self.angulo - i.rotacion - self.pseudo_angulo
                        self.enemigo_atacado = i
                elif not aux[0] or self.tipo == "insivible":
                    i.contacto_player = False

        if not enemigos_cerca:
            self.ataque_w = False
            self.ataque_s = False
            self.enemigo_atacado = None
             
        return seno, coseno

    def pasar_nivel(self):
        self.trigger_nivel.emit(PasarNivelEvent())
        print("he pasado de nivel")

    def esconderse(self):
        self.tipo = "invisible"

    def mostrarse(self):
        print("ya no me escondo")
        self.tipo = self.aux_tipo

    def comer(self):
        self.vida = self.vida_maxima

    def run(self):
        while True and not self.stoped:
            if not self.teclas_juego[Qt.Key_P] and \
               not self.teclas_juego[Qt.Key_T]:
                time.sleep(0.01)
                self.chequear_distancias_items()
                if self.teclado_jugador1[Qt.Key_W]:
                    self.pseudo_angulo = 0
                    seno, coseno = self.chequear_distancias()
                    if self.ataque_w:
                        seno, coseno = 0, 0
                    x = min(
            max(
                self.position[0] + seno, - self.ancho_medio + self.ancho/2), 
                    self.parent.w - (
                        self.parent.menuw() + self.ancho_medio + self.ancho
                                    )
                )

                    y = min(
                            max(
            self.position[1] - coseno, - self.alto_medio + self.alto/2), 
            self.parent.h - self.alto_medio - self.alto - 30 
                            )
                    self.rotacion = 180
                    self.contador += 1
                    self.position = (x, y)

                if self.teclado_jugador1[Qt.Key_S]:
                    self.pseudo_angulo = 0
                    seno,coseno = self.chequear_distancias()
                    if self.ataque_s:
                        seno, coseno = 0, 0
                    
                    x = min(
            max(self.position[0] - seno, - self.ancho_medio + self.ancho/2), 
                self.parent.w - (
                    self.parent.menuw() + self.ancho_medio + self.ancho
                    )
                )
                    y = min(
            max(self.position[1] + coseno, - self.alto_medio + self.alto/2),  
                self.parent.h - self.alto_medio - self.alto - 30 
                )
                    self.rotacion = 0
                    self.contador += 1

                    self.position = (x, y)

                if self.teclado_jugador1[Qt.Key_A]:
                    self.chequear_distancias()
                    self.angulo = (self.angulo - 3 + 360) % 360
                    self.contador += 1


                if self.teclado_jugador1[Qt.Key_D]:
                    self.chequear_distancias()
                    self.angulo = (self.angulo + 3 + 360) % 360
                    self.contador += 1

                self.chequear_distancias()
                self.chequear_ataque()
                self.position = (self.position[0], self.position[1])


class Enemigo(QTimer, Entidades):

    trigger = pyqtSignal(MovePlayerEvent)
    trigger_bar = pyqtSignal(MoveBarEvent)
    trigger_stop = pyqtSignal(StopEvent)
    trigger_dead = pyqtSignal(DeadEvent)
    trigger_set = pyqtSignal(SetEvent)
    trigger_attack = pyqtSignal(AttackEvent)
    id_ = 1

    def __init__(self, *args):
        super().__init__(*args)
        self.jugador = args[2]
        self.contador_bucles = 0
        self.paso = False
        self.contacto_player = False
        self.azar = choice([1,2, 3, 4])
        self.timeout.connect(self.run)
        self.trigger.connect(self.parent.actualizar_imagen_enemigos)
        self.trigger_bar.connect(self.parent.actualizar_bar)
        self.trigger_stop.connect(self.parent.stop_qtimer)
        self.trigger_set.connect(self.parent.set_objeto)
        self.trigger_attack.connect(self.parent.atacar)
        self.id = "Enemigo {}".format(Enemigo.id_)
        self.en_alerta = False
        Enemigo.id_ += 1
        self.enemigo_atacado = self.jugador

    @property
    def rango_vision(self):
        return self.tamaño * 25 + 70

    @property
    def rango_escape(self):
        return self.rango_vision * 1.5

    @property
    def tiempo_reaccion(self):
        return random()

    @property
    def dist_x(self):
        return self.jugador.centro[0] - self.centro[0]

    @property
    def dist_y(self):
        return self.jugador.centro[1] - self.centro[1]

    @property
    def distancia(self):
        distancia_final = (self.dist_x ** 2 + self.dist_y ** 2) ** 0.5
        if self.en_alerta:
            if distancia_final > self.rango_escape:
                self.en_alerta = False
            else:
                self.en_alerta = True
        if not self.en_alerta:
            if distancia_final < self.rango_vision:
                self.en_alerta = True
            else:
                self.en_alerta = False
        if self.jugador.tipo == "invisible":
            self.en_alerta = False
        return distancia_final

    @property
    def escapar(self):
        if self.jugador.tamaño < self.tamaño or self.jugador.vida < self.jugador.vida_maxima / 2.5:
            return False
        else:
            return True

    def distance_to_player(self):

        if self.paso:
            self.paso = False
            return ((
                self.distancia < (self.parent.w / 70 * self.jugador.tamaño)/5\
                 +  (self.parent.w / 70 * self.tamaño)/2), 
                 self.dist_x, 
                 self.dist_y
                 )
        return ((
            self.distancia < (self.parent.w / 80 * self.jugador.tamaño)/5\
            + (self.parent.w / 80 * self.tamaño)/2),
            self.dist_x,
            self.dist_y)

    def run(self):
        if self not in self.parent.threads or self.parent is None:
            self.stoped = True
            self.hide()
        if self.is_dead:
            if self.contador_dead <= 5:
                self.contador += 1
                self.trigger.emit(MovePlayerEvent(self))
                if self.contador // 10 > self.contador_dead:
                    self.contador_dead += 1

            if self.contador_dead == 6:
                self.trigger_bar.emit(MoveBarEvent(
                    self.lifeBar, self
                ))
                self.trigger_stop.emit(StopEvent(self))
            return

        if self.contacto_player:
            self.trigger_stop.emit(StopEvent(self, 1))

        if (self.teclas_juego[Qt.Key_P] or\
           self.teclas_juego[Qt.Key_T]):   
            return
        if self.en_alerta:
            if self.contador_bucles < 10:
                angulo = f.angulo_entre_player(
                    self.jugador.position, self.position
                    )
                a = radians(angulo)
                if self.escapar:
                    a = - a
                self.rotacion = 180
                self.angulo = angulo 
                seno = sin(a) * self.velocidad_x
                coseno = cos(a) * self.velocidad_y
                x = min(
                        max(
            self.position[0] + seno, - self.ancho_medio + self.ancho / 2), 
            self.parent.w - (
            self.parent.menuw() + self.ancho_medio + self.ancho
                            )
                        )
                y = min(
                        max(
            self.position[1] - coseno, - self.alto_medio + self.alto/2
                            ),  
            self.parent.h - self.alto_medio - self.alto - 30 
                        ) 
                self.contador += 1
                self.position = (x, y)
                self.contador_bucles += 1 
                return

        if self.contador_bucles < 10:
            if self.azar == 1:
                a = radians(self.angulo)
                if self.escapar:
                    a = - a
                seno = sin(a) * self.velocidad_x
                coseno = cos(a) * self.velocidad_y
                x = min(
                        max(self.position[0] + seno, - self.ancho_medio + self.ancho/2), 
                        self.parent.w - (
                        self.parent.menuw() + self.ancho_medio + self.ancho
                                         )
                            )
                y = min(
                        max(
                self.position[1] - coseno, - self.alto_medio + self.alto/2
                            ), 
                self.parent.h - self.alto_medio - self.alto - 30 
                        )
                self.rotacion = 180
                self.contador += 1
                self.position = (x, y)
                self.contador_bucles += 1

            elif self.azar == 2:
                a = radians(self.angulo)
                seno = sin(a) * self.velocidad_x
                
                coseno = cos(a) * self.velocidad_y
                if self.escapar:
                    a = - a
                x = min(
                        max(self.position[0] - seno, - self.ancho_medio + self.ancho / 2), 
                        self.parent.w - (
                           self.parent.menuw() + self.ancho_medio + self.ancho
                                        )
                           )
                y = min(
                        max(self.position[1] + coseno, - self.alto_medio + self.alto / 2), 
                        self.parent.h - self.alto_medio - self.alto - 30 )
                self.rotacion = 0
                self.contador += 1

                self.position = (x, y)
                self.contador_bucles += 1

            elif self.azar == 3:
                self.position = self.position
                self.angulo = (self.angulo - 4) % 360
                self.contador += 1
                self.contador_bucles += 1
            else:
                self.position = self.position
                self.angulo = (self.angulo + 4) % 360
                self.contador += 1
                self.contador_bucles += 1
        else:
            self.contador_bucles = 0
            self.azar = choice([1, 2, 3, 4])





if __name__ == '__main__':
    # def hook(type, value, traceback):
    #     print(type)
    #     print(traceback)
    # sys.__excepthook__ = hook

    # app = QApplication([])

    # music.show()
    # app.exec()
    pass
