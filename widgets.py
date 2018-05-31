from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer, QSize, QUrl
from PyQt5.QtMultimedia import QSoundEffect, QSound
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QSizePolicy)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QToolBar)
from PyQt5.QtWidgets import (QPushButton, QLabel, QLineEdit, QAction)
from PyQt5.QtGui import QPainter, QColor, QPen,  QPalette, QBrush, QFont
from PyQt5.QtGui import QIcon, QImage, QDrag
from PyQt5.QtGui import QPixmap, QTransform, QFont
from math import sin, cos, radians
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, 
                            QLabel, QProgressBar,QToolButton,
                             QLineEdit, QHBoxLayout, QVBoxLayout)
from random import choice
from textos import *
from events import *
import funciones as f
import sys
import time

class Boton(QPushButton):
    def __init__(self, parent, text, style, method, size=None, tipo=None):
        super().__init__()
        self.tipo = tipo
        self.parent = parent
        self.style = style
        self.text = text
        if size is None:
            self.size_font = parent.size_font
        else:
            self.size_font = size
        self.setFont(MyFont(self.size_font))
        self.setText(self.text)
        self.setStyleSheet(self.style)
        self.clicked.connect(self.sound)
        self.clicked.connect(method)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setCursor(Qt.PointingHandCursor)
        pass

    def leaveEvent(self,event):
        pass


    def resize1(self, text_size):
        self.setFont(MyFont(text_size))

    def sound(self):
        QSound.play("sounds/button-28.wav")

class QHBoxSimetrica(QHBoxLayout):
    def __init__(self, *args):
        super().__init__()
        if args[-1] is not None:
            self.aux_label = QLabel("")
            for arg in args:
                self.addWidget(self.aux_label)
                if isinstance(arg, QVBoxSimetrica):
                    self.addLayout(arg)
                elif isinstance(arg, QHBoxLayout):
                    self.addLayout(arg)
                else:
                    self.addWidget(arg)
            self.addWidget(self.aux_label)
        else:
            for arg in args[:-1]:
                if type(arg) == int:
                    self.addStretch(arg)
                elif isinstance(arg, QVBoxSimetrica):
                    self.addLayout(arg)
                elif isinstance(arg, QHBoxLayout):
                    self.addLayout(arg)
                else:
                    self.addWidget(arg)


class QVBoxSimetrica(QVBoxLayout):
    def __init__(self, *args):
        super().__init__()
        if args[-1] is not None:
            self.aux_label = QLabel("")
            for arg in args:
                self.addWidget(self.aux_label)
                if isinstance(arg, QHBoxSimetrica):
                    self.addLayout(arg)
                else:
                    self.addWidget(arg)
            self.addWidget(self.aux_label)
        else:
            for arg in args[:-1]:
                if type(arg) == int or type(arg) == float:
                    self.addStretch(arg)
                elif isinstance(arg, QHBoxSimetrica):
                    self.addLayout(arg)
                elif isinstance(arg, QHBoxLayout):
                    self.addLayout(arg)
                else:
                    self.addWidget(arg)


class Music(QSoundEffect):
    def __init__(self, *args, path = None, loop = 0):
        super().__init__(*args)
        self.parent = args[0]
        self.path = path
        self.stop()
        self.setSource(QUrl.fromLocalFile(self.path))
        if loop == 1:
            self.timer = QTimer()
            self.timer.timeout.connect(self.play_music)
            self.timer.start(71*1000)

        if loop == 2:
            self.timer = QTimer()
            self.timer.timeout.connect(self.play_music)  
            self.timer.setSingleShot(True) 
            self.timer.start(0)


        self.play_music()

    def play_music(self):
        self.play()


class MouseLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("background-color: white")
        

    def leaveEvent(self,event):
        self.setStyleSheet("background-color: None")

class PuntajeLabel(QLabel):
    def __init__(self, parent, size):
        super().__init__(parent)
        self.setText("Puntaje: 0")
        self.setAlignment(Qt.AlignCenter)
        self.setFont(MyFont(size))

        self.setStyleSheet(puntaje_label)

    def set_valor(self, value):
        self.setText("Puntaje: {}".format(value))

    def resize1(self, text_size):
        self.setFont(MyFont(text_size))


class RankingLabel(QLabel):
    def __init__(self, parent, size, text):
        super().__init__(parent)

        self.setText(text)
        self.setFont(MyFont(size))
        self.setStyleSheet(ranking_label)
        if text == "No hay partidas hasta el momento.":
            self.setStyleSheet(ranking_label)

    def resize1(self, text_size):
        self.setFont(MyFont(text_size))


class MejoresLabel(QLabel):
    def __init__(self, parent, size, text):
        super().__init__(parent)

        self.setText(text)
        self.setFont(MyFont(size))
        self.setStyleSheet(mejores_label)

    def resize1(self, text_size):
        self.setFont(MyFont(text_size))


class ExpLabel(QLabel):
    def __init__(self, parent, size):
        super().__init__(parent)
        self.setText("Experiencia")
        self.setAlignment(Qt.AlignCenter)
        self.setFont(MyFont(size))
        self.setStyleSheet(exp_label)

    def resize1(self, text_size):
        self.setFont(MyFont(text_size))

class PuntajeEdit(QLineEdit):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.setGeometry(45, 15, 400, 50)
        self.setText(text)
        self.setFont(MyFont(parent.size_font))
        self.setStyleSheet("color:black; background-color: white;")

    def resize1(self, text_size):
        self.setFont(MyFont(text_size))


class MyFont(QFont):
    def __init__(self, size):
        super().__init__("Arial", weight=QFont.Bold)
        self.setPointSize(size)

class ExperienciaBar(QProgressBar):
    def __init__(self, parent, player, text_size):
        super().__init__(parent)
        self.player = player
        self.experiencia = player.experiencia
        self.experiencia_max = 1000
        self.setMinimum(0)
        self.setMaximum(self.experiencia_max)
        self.setValue(self.experiencia)
        self.setFormat("{} / 1000 ({} %)".format(
            f.decimales(self.experiencia,2), self.porciento
            ))
        self.setStyleSheet(stylesheet_expbar)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(MyFont(text_size))
        self.show()

    @property
    def porciento(self):
        return self.experiencia / self.experiencia_max * 100

    def set_valor(self, new_experiencia):
        self.experiencia = new_experiencia
        self.setValue(self.experiencia)
        self.setFormat("{} / 1000 ({} %)".format(
            f.decimales(self.experiencia,2), 
            f.decimales(self.porciento,0)
            ))

    def resize1(self, text_size):
        self.setFont(MyFont(text_size))

class CargandoBar(QProgressBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMaximum(100)
        self.setValue(0)
        self.setStyleSheet(style_cargando)
        self.setAlignment(Qt.AlignRight)

class MyQTimer(QTimer):
    def __init__(self, parent, method, time, aux = False):
        super().__init__(parent)
        if aux:
            self.setSingleShot(True)
        self.timeout.connect(method)
        self.start(time)  

class CargandoQLabel(QLabel):
    def __init__(self, parent, bool, text, aux = False):
        super().__init__(parent)
        self.setWordWrap(bool)
        self.setText(text)
        self.setFont(MyFont(parent.size_font))
        self.setStyleSheet("color:white;background-color:rgb( 54, 76, 100);")
        self.setAlignment(Qt.AlignCenter)        

class MyToolBar(QToolBar):
    def __init__(self, parent, *args):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setOrientation(Qt.Vertical)
        self.setMovable(False)
        for arg in args:
            self.addWidget(arg)
  



