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
from random import randint
from textos import *
from entidades import (Entidades, MyFont)
from events import *


class Trampa(QTimer):

    trigger_image = pyqtSignal(MoveImageEvent)
    trigger_sound = pyqtSignal(SoundEvent)
    trigger_stop = pyqtSignal(StopEvent)

    def __init__(
        self, parent, contador_limite = 7, 
        imagenes = ["images/items/trap1.png"], tipo = "trampa"
                ):
        super().__init__()
        self.activated = False
        self.contador_run = 0
        self.players = []
        self.parent = parent
        self.tipo = tipo
        self.contador_limite = contador_limite
        self.tomado = False
        self.timeout.connect(self.run)
        self.image = QLabel(self.parent)
        self.tamaño = 15
        self.image.setGeometry(
            0, 0, self.parent.w / self.tamaño, self.parent.w / self.tamaño
            )
        self.contador = 0
        self.imagenes = imagenes
        pixmap = QPixmap(self.imagenes[self.contador])
        pixmap = pixmap.scaled(
            self.parent.w / self.tamaño, self.parent.w / self.tamaño
            )
        self.image.setPixmap(pixmap)
        self.image.show()
        self.image.setVisible(True)
        self.position = (randint(0, int(self.parent.w - self.parent.w/7-300)), 
                         randint(0, int(self.parent.h - self.parent.w/7-300)))
        self.image.move(self.position[0], self.position[1])
        self.trigger_image.connect(self.parent.actualizar_item)
        self.trigger_sound.connect(self.parent.sound_effect)
        self.trigger_stop.connect(self.parent.stop_qtimer)
        self._centro = 0
        self.tomado = False
        self.dead = []
        self.image.setAlignment(Qt.AlignCenter)

    @property
    def centro(self):
        self._centro = (self.position[0] + \
                       self.image.frameGeometry().width() / 2, 
                       self.position[1] + \
                       self.image.frameGeometry().height() / 2)
        return self._centro
        
    @centro.setter
    def centro(self, value):
        self._centro = value
        return self._centro

    def distance_to_player(self):
        for player in self.players:
            if player.tipo != "invisible" and player not in self.dead:
                dist_x = player.centro[0] - self.centro[0]
                dist_y = player.centro[1] - self.centro[1]
                dist_final = (dist_x ** 2 + dist_y ** 2) ** 0.5
                if dist_final < (self.parent.w / 70 * player.tamaño) / 2 +\
                 self.parent.w / self.tamaño / 2 and not self.activated:
                    self.tomar()
                    return

    def kill_players(self):
        for player in self.players:
            dist_x = player.centro[0] - self.centro[0]
            dist_y = player.centro[1] - self.centro[1]
            dist_final = (dist_x ** 2 + dist_y ** 2) ** 0.5
            if dist_final < self.parent.w/15:
                if player.tipo != "invisible" and not player.is_dead and\
                   player not in self.dead:
                    player.vida = 0
                    self.dead.append(player)
                    print("murio uno {}".format(player.id))

    def resize1(self):
        pixmap = QPixmap(self.imagenes[self.contador])
        pixmap = pixmap.scaled(
            self.parent.w / self.tamaño, self.parent.w / self.tamaño
            )
        self.image.setPixmap(pixmap) 
        self.trigger_image.emit(MoveImageEvent(
            self.image, self.contador, self.position[0],
            self.position[1], self.imagenes, self.tipo, self.tamaño
        ))

    def tomar(self):
        if not self.activated:
            self.activarse()
            self.start(1000)
            self.activated = True
        
    def activarse(self):
        self.imagenes = image_trap_activated
        self.sound()

    def sound(self):
        self.trigger_sound.emit(SoundEvent(
            sound[self.tipo]
            ))
        
    def hide(self):
        self.image.move(10000,10000)
        self.centro = (10000, 10000)
        self.position = (10000,10000)
        self.trigger_stop.emit(StopEvent(self))
        del(self)


    def run(self):
        if not self.activated:
            self.distance_to_player()
        if self.activated and self.contador_run <= 3 and\
           self.contador_run != -1:
            self.trigger_image.emit(MoveImageEvent(
                self.image, self.contador, self.position[0],
                self.position[1], self.imagenes, self.tipo, self.tamaño
            ))
            self.contador_run += 1
            self.contador = (self.contador + 1)

        if self.contador_run == 4:
            self.contador = 0
            self.kill_players()

        if self.contador_run > 3:
            self.start(200)
            self.imagenes = image_trap
            self.trigger_image.emit(MoveImageEvent(
                self.image, self.contador, self.position[0],
                self.position[1], self.imagenes, self.tipo, self.tamaño
            ))
            self.contador_run += 1
            self.contador = (self.contador + 1) % 4

        if self.contador == 0 and self.contador_run > 5:
            self.hide() 
            self.contador_run = -1


