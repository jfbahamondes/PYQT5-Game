from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer, QSize, QUrl
from PyQt5.QtMultimedia import QSoundEffect, QSound
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QSizePolicy)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout)
from PyQt5.QtWidgets import (QPushButton, QLabel, QLineEdit, QAction)
from PyQt5.QtGui import QPixmap, QTransform, QFont
import sys
import time
from math import sin, cos, radians
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, 
                            QLabel, QProgressBar,QToolButton,
                             QLineEdit, QHBoxLayout, QVBoxLayout)
from random import randint, choice
from textos import (btnFondoRadius,btnFondoRadius2, btnHover,btnHover2, 
                    btnPressed,btnPressed2, all_sprites_shits, bar_styles, 
                    image_jugador, image_coin, sound, image_trap, 
                    image_trap_activated)
from entidades import (Entidades, MyFont, MovePlayerEvent, MoveBarEvent,
                      AttackEvent)



class HidePlayerEvent:
    def __init__(self, player):
        self.player = player

class ShowPlayerEvent:
    def __init__(self, player):
        self.player = player

class SoundEvent:
    def __init__(self, path):
        self.path = path


class MoveImageEvent:
    def __init__(self, image, contador, x, y, imagenes, tipo, tamaño):
        self.image = image
        self.contador = contador
        self.x = x
        self.y = y
        self.imagenes = imagenes
        self.tipo = tipo
        self.tamaño = tamaño

class Jugador(Entidades):
    trigger = pyqtSignal(MovePlayerEvent)
    trigger_bar = pyqtSignal(MoveBarEvent)
    trigger_attack = pyqtSignal(AttackEvent)
    id_ = 1

    def __init__(self, *args):
        super().__init__(*args)

        self.teclado_jugador1 = {Qt.Key_A: False, Qt.Key_S: False,
                                 Qt.Key_D: False, Qt.Key_W: False,
                                 }
        self.trigger.connect(self.parent.actualizar_imagen)
        self.trigger_bar.connect(self.parent.actualizar_bar)
        self.trigger_attack.connect(self.parent.atacar)
        self.aux_ataque = True
        self.no_paso = True
        self.ataque_w = False
        self.ataque_s = False
        self.threads = []
        self.puntaje = 0
        self.id = "Jugador {}".format(Jugador.id_)
        Jugador.id_ += 1
        self.cueva = None
        self.aux_tipo = self.tipo

    def chequear_ataque(self):
        if self.enemigo_atacado is not None:
            if self.aux_ataque:
                if self.tipo != "invisible":
                    self.enemigo_atacado.atacar()
                    self.atacar()
                    if self.no_paso:
                        self.trigger_attack.emit(AttackEvent(self))
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
                aux = i.distance_to_player(self)
                if aux[0]:
                    enemigos_cerca = True
                    if aux[2] > 0: #estoy abajo de el
                        if self.angulo < 90 or self.angulo > 270:
                            self.ataque_w = True
                            self.ataque_s = False
                            self.pseudo_angulo = 0
                        else:
                            self.ataque_s = True
                            self.ataque_w = False
                            self.pseudo_angulo = 180
                    else:#estoy arriba
                        if self.angulo < 90 or self.angulo > 270:
                            self.ataque_s = True
                            self.ataque_w = False
                            self.pseudo_angulo = 180

                        else:
                            self.ataque_w = True
                            self.ataque_s = False
                            self.pseudo_angulo = 0


                    i.contacto_player = True
                    i.angulo = self.angulo - i.rotacion - self.pseudo_angulo
                    self.enemigo_atacado = i
                else:
                    i.contacto_player = False
        if not enemigos_cerca:
            self.ataque_w = False
            self.ataque_s = False
            self.enemigo_atacado = None
             
        return seno, coseno

    def esconderse(self):
        self.tipo = "invisible"

    def mostrarse(self):
        print("ya no me escondo")
        self.tipo = self.aux_tipo

    def run(self):
        self.position = (randint(0, self.parent.w - 200), 
                         randint(0, self.parent.h - 200))
        while True:
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
                            max(self.position[0] + seno, 0), 
                            self.parent.menuw(self))

                    y = min(
                            max(self.position[1] - coseno, 0), 
                            self.parent.h - self.alto * 2 )
                    self.rotacion = 180
                    self.contador += 1
                    self.position = (x, y)

                if self.teclado_jugador1[Qt.Key_S]:
                    self.pseudo_angulo = 0
                    seno,coseno = self.chequear_distancias()
                    if self.ataque_s:
                        seno, coseno = 0, 0
                    
                    x = min(
                            max(self.position[0] - seno, 0), 
                            self.parent.menuw(self))
                    y = min(
                            max(self.position[1] + coseno, 0), 
                            self.parent.h - self.alto * 2 )
                    self.rotacion = 0
                    self.contador += 1

                    self.position = (x, y)

                if self.teclado_jugador1[Qt.Key_A]:
                    self.chequear_distancias()
                    self.angulo = (self.angulo - 3) % 360
                    self.contador += 1


                if self.teclado_jugador1[Qt.Key_D]:
                    self.chequear_distancias()
                    self.angulo = (self.angulo + 3) % 360
                    self.contador += 1

                self.chequear_distancias()
                self.chequear_ataque()
                self.position = (self.position[0], self.position[1])


class Enemigo(QTimer, Entidades):
    trigger = pyqtSignal(MovePlayerEvent)
    trigger_bar = pyqtSignal(MoveBarEvent)
    id_ = 1

    def __init__(self, *args):
        super().__init__(*args)
        self.contador_bucles = 0
        self.paso = False
        self.contacto_player = False
        self.azar = choice([1,2, 3, 4])
        self.timeout.connect(self.run)
        self.trigger.connect(self.parent.actualizar_imagen_enemigos)
        self.trigger_bar.connect(self.parent.actualizar_bar)
        self.id = "Enemigo {}".format(Enemigo.id_)
        Enemigo.id_ += 1

    def distance_to_player(self, player):
        dist_x = player.centro[0] - self.centro[0]
        dist_y = player.centro[1] - self.centro[1]
        dist_final = (dist_x ** 2 + dist_y ** 2) ** 0.5
        if self.paso:
            self.paso = False
            return ((dist_final < self.parent.w/15), dist_x, dist_y)
        return ((dist_final < self.parent.w/25), dist_x, dist_y)

    def run(self):
        if not self.is_dead:
            if not self.contacto_player:
                if not (self.teclas_juego[Qt.Key_P] or\
                   self.teclas_juego[Qt.Key_T]):   

                    if self.contador_bucles < 10:
                        if self.azar == 1:
                            a = radians(self.angulo)
                            seno = sin(a) * self.velocidad_x
                            
                            coseno = cos(a) * self.velocidad_y
                            

                            x = min(
                                    max(self.position[0] + seno, 0), 
                                    self.parent.menuw(self))

                            y = min(
                                    max(self.position[1] - coseno, 0), 
                                    self.parent.h - self.alto * 2)
                            self.rotacion = 180
                            self.contador += 1
                            self.position = (x, y)
                            self.contador_bucles += 1

                        elif self.azar == 2:
                            a = radians(self.angulo)
                            seno = sin(a) * self.velocidad_x
                            
                            coseno = cos(a) * self.velocidad_y
                            
                            x = min(
                                    max(self.position[0] - seno, 0),
                                    self.parent.menuw(self))
                            y = min(
                                    max(self.position[1] + coseno, 0),
                                    self.parent.h - self.alto * 2)
                            self.rotacion = 0
                            self.contador += 1

                            self.position = (x, y)
                            self.contador_bucles += 1


                        elif self.azar == 3:
                            self.angulo = (self.angulo - 2) % 360
                            self.contador += 1
                            self.contador_bucles += 2


                        else:
                            self.angulo = (self.angulo + 2) % 360
                            self.contador += 1
                            self.contador_bucles += 2
                    else:
                        self.contador_bucles = 0
                        self.azar = choice([1, 2, 3, 4])
        else:

            self.trigger.connect(self.parent.actualizar_imagen_enemigos)
            if self.contador_dead <= 5:
                self.contador += 1
                self.trigger.emit(MovePlayerEvent(self))
                if self.contador // 10 > self.contador_dead:
                    self.contador_dead += 1

            if self.contador_dead == 6:
                self.trigger_bar.emit(MoveBarEvent(
                    self.progressBar, self
                ))
                self.stop()


    def hide(self):
        self.position = (10000,10000)
        self.trigger.emit(MovePlayerEvent(self))
        self.stop()
        del(self)

class Item(QTimer):

    trigger_image = pyqtSignal(MoveImageEvent)
    trigger_sound = pyqtSignal(SoundEvent)

    def __init__(self, parent, contador_limite, imagenes, tipo):
        super().__init__()
        self.parent = parent
        self.tipo = tipo
        self.contador_limite = contador_limite
        self.tomado = False
        self.timeout.connect(self.run)
        self.image = QLabel(self.parent)
        self.image.setAlignment(Qt.AlignCenter)
        if self.tipo != "safe_zone":
            self.div1 = 20
            self.div2 = 20
            self.tamaño = 25
        else:
            self.div2 = 12
            self.div1 = 12
            self.tamaño = 15
        self.position = (randint(0, int(self.parent.w) - 300),
                        randint(0, int(self.parent.h) - 200))
        self.image.setGeometry(self.position[0], self.position[1],
                               self.parent.w / self.div1, self.parent.w / self.div2)
        self.contador = 0
        self.imagenes = imagenes
        pixmap = QPixmap(self.imagenes[self.contador])
        pixmap = pixmap.scaled(self.parent.w / self.tamaño, self.parent.w / self.tamaño)

        self.image.setPixmap(pixmap)
        self.image.show()
        self.image.setVisible(True)

        self.image.move(self.position[0], self.position[1])
        self.trigger_image.connect(self.parent.actualizar_coin)
        self.trigger_sound.connect(self.parent.sound_effect)
        self.tomado = False

    @property
    def centro(self):
        return (self.position[0] + \
                self.image.frameGeometry().width() / 2, 
                self.position[1] + \
                self.image.frameGeometry().height() / 2)
        
    @centro.setter
    def centro(self, value):
        return value

    def distance_to_player(self, player):
        dist_x = player.centro[0] - self.centro[0]
        dist_y = player.centro[1] - self.centro[1]
        dist_final = (dist_x ** 2 + dist_y ** 2) ** 0.5
        if self.tipo != "safe_zone":
            return ((dist_final < self.parent.w/25), dist_x, dist_y)
        else:
            return ((dist_final < self.parent.w/30), dist_x, dist_y)


    def resize1(self):
        self.image.setGeometry(0, 0, self.parent.w / self.div1, self.parent.w / self.div2)
        pixmap = QPixmap(self.imagenes[self.contador])
        pixmap = pixmap.scaled(self.parent.w / self.tamaño, self.parent.w / self.tamaño)
        self.image.setPixmap(pixmap) 
        self.trigger_image.emit(MoveImageEvent(
            self.image, self.contador, self.position[0],
            self.position[1], self.imagenes, self.tipo, self.tamaño
        ))


    def tomar(self, jugador):
        if not self.tomado:
            if self.tipo == "coin":
                jugador.puntaje += 1000
                self.tomado = True
                jugador.items.pop(jugador.items.index(self))
                self.sound()
                self.hide()
                self.tomado = True
            elif self.tipo == "food":
                print("he comido")
                jugador.items.pop(jugador.items.index(self))
                self.sound()
                self.hide()
                self.tomado = True
                pass #rellenar
            elif self.tipo == "safe_zone":
                pass


    def hide(self):
        self.image.move(10000,10000)
        self.centro = (10000, 10000)
        self.position = (10000,10000)
        del(self)

    def sound(self):
        if sound[self.tipo]:
            self.trigger_sound.emit(SoundEvent(
                sound[self.tipo]
            ))
        

    def run(self):

        self.contador = (self.contador + 1) % self.contador_limite
        self.trigger_image.emit(MoveImageEvent(
            self.image, self.contador, self.position[0],
            self.position[1], self.imagenes, self.tipo, self.tamaño
        ))



class MouseLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("background-color: white")
        

    def leaveEvent(self,event):
        self.setStyleSheet("background-color: None")

if __name__ == '__main__':
    # def hook(type, value, traceback):
    #     print(type)
    #     print(traceback)
    # sys.__excepthook__ = hook

    # app = QApplication([])

    # music.show()
    # app.exec()
    pass
