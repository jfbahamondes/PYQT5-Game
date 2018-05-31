from textos import (btnFondoRadius, btnHover, btnPressed, bar_styles, 
                    image_jugador, image_trap)
from PyQt5.QtCore import Qt, QThread, QSize
from PyQt5.QtMultimedia import QSoundEffect, QSound
from PyQt5.QtWidgets import QLabel,QProgressBar
from PyQt5.QtGui import QPixmap, QFont
from random import randint
from events import *
from widgets import MyFont
import funciones as f
import time

class Entidades(QThread):
    def __init__(self, parent, tipo, aux = None, tamaño = 2):
        super().__init__()    
        self.vida_inicial = 500
        self.parent = parent
        self.tipo = tipo
        self.contador = 10
        self.rotacion = 180
        self.pseudo_angulo = 0
        self.inventario = {i: None for i in range(1,6)}
        self.image_jugador = image_jugador
        self.__angulo = 0
        self.__tamaño = tamaño
        self.factor_x = 1
        self.factor_y = 1
        self.velocidad_inicial_x = self.velocidad_x
        self.velocidad_inicial_y = self.velocidad_y        
        self.__position = (
            randint(0, int(self.parent.w - self.parent.w/7 - 200)), 
            randint(0, int(self.parent.h - self.parent.w/7 - 200))
            )
        self.image = QLabel(self.parent)
        self.image.setGeometry(
            self.position[0], self.position[1], 
            self.parent.w / 6,self.parent.w / 6
            )
        pixmap = QPixmap(self.image_jugador["j1"]).scaled(
            self.parent.w / 70 * self.tamaño**0.8, self.parent.w / 70 * self.tamaño**0.8
            )

        self.image.setAlignment(Qt.AlignCenter)
        self.image.setPixmap(pixmap)
        self.image.setVisible(True)
        self.items = []
        self.center = (
            self.image.frameGeometry().width() / 2, 
            self.image.frameGeometry().height() / 2
            )
        self.teclas_juego = {Qt.Key_P: False, Qt.Key_T: False}
        self.peleando = False
        self.enemigo_atacado = None
        self.trigger.emit(MovePlayerEvent(self))
        self.is_dead = False
        self.contador_dead = 0
        self.__vida = self.vida_maxima
        self.lifeBar = LifeBar(self.parent, self)
        self.no_paso = True
        self.enemigo_atacado = None
        self.time = 1000   
    
    @property
    def tamaño(self):
        return self.__tamaño

    @tamaño.setter
    def tamaño(self, value):
        self.__tamaño = min(value, 10)

    @property
    def objeto_vida(self):
        c = 0
        if self.tipo != "enemigo":
            for key in self.inventario:
                if self.inventario[key] is not None and\
                "armor" in self.inventario[key]:
                    c+=1
        return c

    @property
    def objeto_vel(self):
        c = 0
        if self.tipo != "enemigo":
            for key in self.inventario:
                if self.inventario[key] is not None and\
                "botas" in self.inventario[key]:
                    c+=1
        return c

    @property
    def objeto_daño(self):
        c = 0
        if self.tipo != "enemigo":
            for key in self.inventario:
                if self.inventario[key] is not None and\
                "garras" in self.inventario[key]:
                    c+=1
        return c

    @property
    def vida_maxima(self):
        a = (self.tamaño * 20 + 100) * (1 + self.objeto_vida * 0.3)
        return a

    @property
    def ataque(self):
        return round(self.tamaño * 1/10 * self.vida_maxima, 0) *\
               (1 + self.objeto_daño * 0.5)

    @property
    def daño(self):
        if self.vida == 0:
            return 3
        if self.vida < 25:
            return 3
        if self.vida < 50:
            return 2
        if self.vida < 75:
            return 1
        else:
            return 0
        return int(self.vida_maxima / self.vida % 4)

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, value):
        self.__vida = value
        self.trigger_set.emit(SetEvent(self.lifeBar, self.vida))
        self.trigger_bar.emit(MoveBarEvent(
            self.lifeBar, self
        )) 
        if self.vida <= 0:
            self.morirse()   

    @property
    def ancho_medio(self):
        return self.image.frameGeometry().width() / 2

    @property
    def alto_medio(self):
        return self.image.frameGeometry().height() / 2

    @property
    def ancho(self):
        return self.parent.w / 70 * self.tamaño**0.8

    @property
    def alto(self):
        return self.parent.w / 70 * self.tamaño**0.8

    @property
    def contador_game(self):
        return self.contador 

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
        self.trigger.emit(MovePlayerEvent(self))
        self.trigger_bar.emit(MoveBarEvent(
            self.lifeBar, self
        ))

    @property
    def angulo(self):
        return self.__angulo

    @angulo.setter
    def angulo(self, value):
        self.__angulo = value
        self.trigger.emit(MovePlayerEvent(self))

    @property
    def velocidad_x(self):
        if self.tipo == "enemigo":
            return (5 / self.tamaño ** 0.5 * self.factor_x / 1.493) \
                * (1 + self.objeto_vel * 0.1)
        return (4 / self.tamaño ** 0.5 * self.factor_y / 1.366) * \
               (1 + self.objeto_vel * 0.5)

    @property
    def velocidad_y(self):
        if self.tipo == "enemigo":
            return (5 / self.tamaño ** 0.5 * self.factor_y / 1.366) * \
               (1 + self.objeto_vel * 0.1)
        return (4 / self.tamaño ** 0.5 * self.factor_y / 1.366) * \
               (1 + self.objeto_vel * 0.5)

    def run(self):
        pass

    def resize1(self):
        self.image.setGeometry(0, 0, self.parent.w / 6, self.parent.w / 6)
        pixmap = QPixmap(self.image_jugador[self.tipo]).scaled(
            self.parent.w / 70 * self.tamaño**0.8, self.parent.w / 70 * self.tamaño**0.8
            )
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setPixmap(pixmap)

    @property
    def centro(self):
        return (self.position[0] + \
                self.image.frameGeometry().width() / 2, 
                self.position[1] + \
                self.image.frameGeometry().height() / 2)

    @centro.setter
    def centro(self, value):
        return value

    def atacar(self):
        time.sleep(0.02)
        self.contador += 10
        self.position = self.position

    def morirse(self):
        self.trigger_dead.emit(DeadEvent(self))
        self.trigger.emit(MovePlayerEvent(self))
        self.is_dead = True
        self.contador = 0
        self.trigger_set.emit(SetEvent(self.lifeBar, 0))
        QSound.play("sounds/bear_diying.wav")

    def hide(self):
        self.position = (10000,10000)
        if self.tipo == "enemigo":
            self.trigger_stop.emit(StopEvent(self))
        else:
            self.stoped = True

class LifeBar(QProgressBar):
    def __init__(self, parent, player):
        super().__init__(parent = parent)
        self.text_size = parent.h / 100 
        self.player = player
        self.vida = self.player.vida_maxima
        self.tipo = player.tipo
        self.setMinimum(0)
        self.setMaximum(self.vida)
        self.setValue(self.vida)
        self.setFormat("{}HP {}".format(self.vida, f.decimales(
                self.player.ataque, 1
                )))
        if self.tipo == "enemigo":
            self.setFormat("{}% {}".format(
                self.vida/ self.player.vida_maxima * 100
                , f.decimales(
                self.player.ataque, 1
                )))

        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(bar_styles[self.tipo])
        self.setFont(MyFont(self.text_size))
        self.move(player.position[0], player.position[1])
        self.resize(QSize(self.player.ancho, self.player.ancho/4))
        self.show()

    def set_valor(self, new_vida):
        self.vida = new_vida
        self.setMaximum(self.player.vida_maxima)
        self.setValue(min(self.vida, self.player.vida_maxima))
        self.setFormat("{} HP".format(f.decimales(self.vida, 3)))
        if self.tipo == "enemigo":
            self.setFormat("{}% {}".format(f.decimales(
                self.vida/ self.player.vida_maxima * 100, 1
                ), f.decimales(
                self.player.ataque, 1
                )))

    def resize1(self, x, y, text_size):
        self.setFont(MyFont(text_size))
        self.resize(QSize(x, y))

    def hide(self):
        self.resize(QSize(0,0))
        self.move(100000, 100000)

