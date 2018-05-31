from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer, QSize, QUrl, QPoint
from PyQt5.QtMultimedia import QSoundEffect, QSound
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QSizePolicy)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QToolBar)
from PyQt5.QtWidgets import (QPushButton, QLabel, QLineEdit, QAction)
from PyQt5.QtGui import QPainter, QColor, QPen,  QPalette, QBrush, QFont
from PyQt5.QtGui import QIcon, QImage, QDrag

from PyQt5.QtGui import QPixmap, QTransform, QFont
import sys
import time
from math import sin, cos, radians
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, 
                            QLabel, QProgressBar,QToolButton,
                             QLineEdit, QHBoxLayout, QVBoxLayout)
from random import choice
from textos import *
from events import *
from widgets import *
import funciones as f


class MyTienda(QWidget):
    def __init__(self, x, y, parent_w, parent_h, fake_parent,*args, parent = None):
        super().__init__(parent)
        self.url_aux = None
        self.fake_parent = fake_parent
        self.jugador = fake_parent.jugador
        self.w = parent_w
        self.h = parent_h
        self.setGeometry(x, y, parent_w, parent_h)
        self.imagen_actual = "images/fondos/bosque4_2.png"
        self.sImage = QPixmap(self.imagen_actual).scaled(parent_w, parent_h)
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(self.sImage))
        self.setPalette(self.palette)
        self.setWindowTitle('Tienda')
        self.setWindowIcon(QIcon('images/items/tienda_icon.png'))
        self.number = 0
        self.lista_label_tienda = []
        self.lista_label_tienda.append(TiendaLabel(self, url="images/tienda/armor.png"))
        self.lista_label_tienda.append(TiendaLabel(self, url="images/tienda/botas.png"))
        self.lista_label_tienda.append(TiendaLabel(self, url="images/tienda/garras.png"))
        v1 = QVBoxSimetrica(self.lista_label_tienda[1-1], LabelNombre(self, armadura))
        v2 = QVBoxSimetrica(self.lista_label_tienda[2-1], LabelNombre(self, botas))
        v3 = QVBoxSimetrica(self.lista_label_tienda[3-1], LabelNombre(self, garras))
        hbox0 = QHBoxSimetrica(LabelTitulo(
            self, "Arrastre un objeto en un espacio para comprar:"
            ),1, None)
        hbox1 = QHBoxSimetrica(1, v1, v2, v3, 1, None)
        for arg in args:
            arg.setParent(self)
        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        self.lista_label = []
        if self.fake_parent.aux_f:
            self.showFullScreen()




        for key in self.jugador.inventario:
            a = InvetarioLabel(self, 5, self.jugador.inventario[key], 1)
            self.lista_label.append(a)
            hbox2.addWidget(a)
            hbox2.addStretch(1)
        self.puntaje_gastar = LabelTitulo(
            self, "Puntaje para gastar: {}".format(self.jugador.puntaje)
            )
        hbox3 = QHBoxSimetrica(1,self.puntaje_gastar , None)
        vbox = QVBoxSimetrica(hbox0,1, hbox1, 1, hbox2, 2, hbox3, None)

        self.setLayout(vbox)

    def closeEvent(self, event):
        self.fake_parent.abrir_tienda()

    def resizeEvent(self, event):
        self.sImage = QPixmap(self.imagen_actual)
        self.sImage = self.sImage.scaled(self.frameGeometry().width(), self.frameGeometry().height())
        self.palette.setBrush(QPalette.Window, QBrush(self.sImage))
        self.setPalette(self.palette)
        print(self.size())

    def resize1(self):
        self.sImage = QPixmap(self.imagen_actual)
        self.sImage = self.sImage.scaled(self.w, self.h)
        self.palette.setBrush(QPalette.Window, QBrush(self.sImage))
        self.setPalette(self.palette)
        print(self.size())

    def actualizar_tienda(self, numero, url):
        for i in self.lista_label_tienda:
            i.aux_leave = True
        if self.jugador.puntaje >= costo[url]:
            QSound.play("sounds/money.wav")
            self.jugador.inventario[numero] = url
            self.jugador.puntaje -= costo[url]
            self.lista_label[numero-1].change_event(url)

            self.puntaje_gastar.setText(
                "Puntaje para gastar: {}".format(self.jugador.puntaje)
                )
            self.jugador.vida += 0
        else:
            QSound.play("sounds/no_comprar.wav")
            print(" no alcanza")

    def mouseMoveEvent(self, event):
        for i in self.lista_label:
            i.enterEvent(event)  
            if i.auxx:
                i.auxx = False
                break 


class InvetarioLabel(QLabel):

    id = 1

    def __init__(self, parent, size = 25, url =  None, asd = None):
        super().__init__(parent)
        self.id = InvetarioLabel.id
        InvetarioLabel.id = InvetarioLabel.id%5 + 1
        self.parent = parent
        self.jugador = parent.jugador
        if url is None:
            url = "images/tienda/inventorio_vacio3.png"


        self.url = url
        self.size = size
        self.setMouseTracking(True)
        self.setGeometry(0, 0, self.parent.w / self.size, self.parent.w / self.size )
        pixmap = QPixmap(self.url).scaled(
            self.parent.w / self.size, self.parent.w / self.size
            )
        self.setAlignment(Qt.AlignCenter)
        self.setPixmap(pixmap)
        self.setVisible(True)
        self.setAcceptDrops(True)
        self.setStyleSheet(item_label)
        self.asd = asd
        if asd:
            self.setStyleSheet("background-color: None")
        self.auxx = False
        self.raise_()

    def enterEvent(self,event):
        if not self.asd:
            self.setStyleSheet("background-color: white")
        if event.pos():
            self.auxx = True
            try:
                if self.parent.url_aux:
                    print("asd")
                    self.parent.actualizar_tienda(self.id, self.parent.url_aux)
                    self.parent.url_aux = None
            except:
                pass



    def leaveEvent(self,event):
        if not self.asd:
            self.setStyleSheet("background-color: None")

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.accept() 
        



    def change_event(self, url):
        self.url = url
        if url is None:
            self.url = "images/tienda/inventorio_vacio.png"
        self.setPixmap(QPixmap(self.url).scaled(
            self.parent.w / self.size, self.parent.w / self.size
            )) 
        if url and self.asd:
            self.setStyleSheet("background-color: black")        


    def resize1(self):
        pixmap = QPixmap(self.url).scaled(
            self.parent.w / self.size, self.parent.w / self.size
            )
        self.setPixmap(pixmap)

    def __repr__(self):
        return self.url

class TiendaLabel(QLabel):
    def __init__(self, parent, size = 8, url =  "images/tienda/armor.png"):
        super().__init__(parent)
        self.parent = parent
        self.url = url
        self.size = size
        self.setText(url)
        self.setMouseTracking(True)
        self.setGeometry(
            0, 0, self.parent.w / self.size, self.parent.w / self.size 
            )
        pixmap = QPixmap(self.url).scaled(
            self.parent.w / self.size, self.parent.w / self.size
            )
        self.setAlignment(Qt.AlignCenter)
        self.setPixmap(pixmap)
        self.setVisible(True)
        self.setStyleSheet(tienda_label)
        self.aux_leave = True
        # self.raise_()


    def enterEvent(self,event):
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("background-color: white")
        

    def leaveEvent(self,event):
        self.setStyleSheet("background-color: black")


    def mousePressEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)
        self.__mousePressPos = None
        self.__mouseMovePos = None
        self.setCursor(Qt.ClosedHandCursor)
        # self.raise_()
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()
        super(TiendaLabel, self).mousePressEvent(event)


    def mouseMoveEvent(self, event):
        self.parent.url_aux = None
        if event.buttons() == Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = (globalPos - self.__mouseMovePos)
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)
            print(event.x(), event.y())

            self.__mouseMovePos = globalPos
        # super(TiendaLabel, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        print(1123123, self.url, self.parent.url_aux)
        self.parent.url_aux = self.url
        # if self.parent.number == 1:
        #     self.parent.actualizar_tienda(1, self.url)
        # elif self.parent.number == 2:
        #     self.parent.actualizar_tienda(2, self.url)
        # elif self.parent.number == 3:
        #     self.parent.actualizar_tienda(3, self.url)
        # elif self.parent.number == 4:
        #     self.parent.actualizar_tienda(4, self.url)
        # elif self.parent.number == 5:
        #     self.parent.actualizar_tienda(5, self.url)
        # self.parent.number = 0
    #     pass
        print(self.parent.url_aux)
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3 or False:
                event.ignore()
        # super(TiendaLabel, self).mouseReleaseEvent(event)

    def resize1(self):
        pixmap = QPixmap(self.url).scaled(
            self.parent.w / self.size, self.parent.w / self.size
            )
        self.setPixmap(pixmap)


class LabelTitulo(QLabel):
    def __init__(self, parent, text):
        super().__init__(parent=parent)
        self.setText(text)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(MyFont(20))
        self.setStyleSheet(label_titulo)

class LabelNombre(QLabel):
    def __init__(self, parent, text):
        super().__init__(parent=parent)
        self.setText(text)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(MyFont(10))
        self.setStyleSheet(label_nombre)