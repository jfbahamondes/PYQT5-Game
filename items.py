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
from textos import *
from entidades import (Entidades, MyFont)
from events import *

class Item(QTimer):

    trigger_image = pyqtSignal(MoveImageEvent)
    trigger_sound = pyqtSignal(SoundEvent)
    trigger_stop = pyqtSignal(StopEvent)

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
        self.position = (randint(
            0, int(self.parent.w - self.parent.w/7 - 300)), 
                         randint(
            0, int(self.parent.h - self.parent.w/7 - 300)))
        self.image.setGeometry(
            self.position[0], self.position[1],
            self.parent.w / self.div1, self.parent.w / self.div2)
        self.contador = 0
        self.imagenes = imagenes
        pixmap = QPixmap(self.imagenes[self.contador])
        pixmap = pixmap.scaled(
            self.parent.w / self.tamaño, self.parent.w / self.tamaño)
        self.image.setPixmap(pixmap)
        self.image.show()
        self.image.setVisible(True)
        self.image.move(self.position[0], self.position[1])
        self.trigger_image.connect(self.parent.actualizar_item)
        self.trigger_sound.connect(self.parent.sound_effect)
        self.trigger_stop.connect(self.parent.stop_qtimer)
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
            return ((dist_final < (self.parent.w / 70 * player.tamaño)\
                    / 10 + self.parent.w / self.tamaño / 2), dist_x, dist_y)
        return ((dist_final < (self.parent.w / 70 * player.tamaño**0.3) \
                / 10 + self.parent.w / self.tamaño / 3), dist_x, dist_y)


    def resize1(self):
        self.image.setGeometry(
            0, 0, self.parent.w / self.div1, self.parent.w / self.div2
            )
        pixmap = QPixmap(self.imagenes[self.contador])
        pixmap = pixmap.scaled(
            self.parent.w / self.tamaño, self.parent.w / self.tamaño
            )
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
                jugador.comer()
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
        self.trigger_stop.emit(StopEvent(self))
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


