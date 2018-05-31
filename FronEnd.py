from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget)
from PyQt5.QtWidgets import (QPushButton, QLabel, QShortcut)
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtGui import QPalette, QBrush
from PyQt5.QtGui import QIcon
from math import sin, cos, radians
from random import expovariate
from ctypes import windll
from jugadores import Jugador, Enemigo
from trampa import Trampa
from random import randint, choice
from textos import *
from events import *
from widgets import *
from tienda import *
from items import Item
import funciones as f
import sys
import time
import constantes


user32 = windll.user32
user32.SetProcessDPIAware()
ancho, alto = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


try:
    with open("ptjs.txt", "r", encoding="utf-8") as file:
        pass
except:
    with open("ptjs.txt", "w", encoding="utf-8") as file:
        pass   

class MenuPrincipal(QMainWindow):

    def __init__(self, x, y):
        super().__init__()
        self.setWindowIcon(QIcon('images/fondos/oso.png'))
        self.x = x
        self.y = y
        self.init_GUI()
        self.shortcut_paused = QShortcut(Qt.CTRL + Qt.Key_S, self)
        self.shortcut_paused.activated.connect(self.game_paused)
        self.shortcut_tienda = QShortcut(Qt.CTRL + Qt.Key_T, self)
        self.shortcut_tienda.activated.connect(self.abrir_tienda)
        self.shortcut_full_screen = QShortcut(Qt.CTRL + Qt.Key_F11, self)
        self.shortcut_full_screen.activated.connect(self.pantalla_completa)
        self.started = False
        self.alternar_paused = 0
        self.alternar_tienda = 0
        self.alternar_pantalla = 0
        self.factor_inicial_y = float(self.x)
        self.factor_inicial_x = float(self.y)
        self.etapa_jugador = 1

    def init_GUI(self):
        self.sounds_list = []
        self.sound1 = Music(self, path = "sounds/moonman.wav", loop=1)
        self.sounds_list.append(self.sound1)
        self.jugador = None
        self.velocidad_inicial_x = 0
        self.velocidad_inicial_y = 0
        self.menu_widget = QWidget() 
        self.setAutoFillBackground(True)
        self.setWindowTitle('Global Warning')
        self.setGeometry(ancho / 2 - self.x / 2, 
                         alto / 2 - self.y / 2, self.x, self.y)
        self.threads, self.deads = [], []
        self.aux_walk = True
        #historia
        self.contador_pag = 0
        #cargando
        self.value = 0
        self.label_cargando = 0
        #labels
        self.label1 = QLabel(self)
        self.label1.setText(bienvenida1)
        self.label1.setFont(MyFont(self.size_font))
        self.label1.setStyleSheet("color: black;")
        self.contador_picking = 0
        self.central_widget = QWidget()
        auxbox = QHBoxSimetrica(self.label1)
        self.central_widget.setLayout(auxbox)
        self.setCentralWidget(self.central_widget)
        #items
        self.coins_list, self.cuevas_list, self.botones = [], [], []
        self.trampas_list, self.food_list = [], []
        self.items = [self.coins_list, self.cuevas_list,
                      self.trampas_list, self.food_list]
        self.timer_list, self.cosas_menu = [], []
        self.contador_partida = 0
        self.ultimo_puntaje = 0
        self.nombre = "Anónimo"
        self.items_inv = []
        self.menu_inicio()
        self.aux_f = False

    def menu_inicio(self):
        a = QWidget()
        a.setLayout(self.central_widget.layout())
        self.imagen_actual = "images/fondos/bosque6.png"
        self.sImage = QPixmap(self.imagen_actual).scaled(self.x, self.y)
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(self.sImage))
        self.setPalette(self.palette)
        self.resize_background()
        style = btnFondoRadius + btnHover + btnPressed
        self.aux_label = QLabel("", self)
        self.btnInstrucciones = Boton(self, ' Instrucciones ', style,
                                  self.instrucciones)
        self.btnHistoria = Boton(self, ' Historia ', style,
                                  self.historia)
        self.btnIniciar = Boton(self, ' Comenzar Batalla ', style,
                                  self.escoger_modo)
        self.btnRanking = Boton(self, ' Ranking de Puntajes ', style,
                                  self.ranking_partidas)
        self.botones.extend([self.btnHistoria, self.btnIniciar, 
                             self.btnRanking, self.btnInstrucciones])
        #layouts
        self.hbox1 = QHBoxSimetrica(self.label1)
        self.hbox = QHBoxSimetrica(self.btnRanking)
        self.hbox2 = QHBoxSimetrica(self.btnIniciar)
        self.hbox3 = QHBoxSimetrica(self.btnHistoria)
        self.hbox4 = QHBoxSimetrica(self.btnInstrucciones)

        if self.contador_partida:
            self.label2 = QLabel(self)
            p = "Tu puntaje fue: {}".format(self.ultimo_puntaje)
            self.label2.setText(p)
            self.label2.setFont(MyFont(self.size_font))
            self.label2.setStyleSheet("color: black;")
            self.hbox5 = QHBoxSimetrica(self.label2) 

            self.vbox = QVBoxSimetrica(
                1, self.hbox1, 1, self.hbox5, 2, self.hbox4, 2, 
                self.hbox2, 2, self.hbox, 2, self.hbox3, 
                                4, None)
        else:
            self.vbox = QVBoxSimetrica(1, self.hbox1, 2, self.hbox4, 2, 
                                 self.hbox2, 2, self.hbox, 2, self.hbox3, 
                                 4, None)

        self.central_widget.setLayout(self.vbox)
        if self.contador_partida:
            a = QWidget()
            a.setLayout(self.menu_widget.layout())    

    @property
    def size_font(self):
        return self.h/40

    @property
    def ancho_menu(self):
        return self.w/7

    @property
    def factor_x(self):
        factor = self.w / self.factor_inicial_y
        return factor

    @property
    def factor_y(self):
        factor = self.h / self.factor_inicial_x
        return factor

    @property
    def w(self):
        return self.frameGeometry().width()

    @property
    def h(self):
        return self.frameGeometry().height()  

    def menuw(self):
        return self.toolbar.frameGeometry().width()

    def resizeEvent(self, event):
        self.resize_background()
        self.resize_jugador_ppal()
        self.resize_enemigos()
        self.resize_bar_menu()
        self.resize_botones()
        self.resize_items()
        
        self.factor_inicial_y = self.w
        self.factor_inicial_x = self.h
        try:
            self.tienda_widget.resize1()
        except:
            pass

    def resize_items(self):
        for tipo in self.items:
            for item in tipo:
                item. position = (item.position[0] * self.factor_x, 
                                item.position[1] * self.factor_y)
                item.resize1()

    def resize_bar_menu(self):
        if self.started:
            self.label_game.setStyleSheet( 
                "background-color:  rgb( 57, 101, 70);"\
                "border-radius: 10px;"\
                "min-width: {}px;".format(self.ancho_menu)+\
                "min-height: {} px;".format(self.ancho_menu)+\
                "padding: 1px;")
        for item in self.cosas_menu:
            if isinstance(item, InvetarioLabel):
                item.resize1()

            else:
                item.resize1(self.size_font/2)
   
    def resize_background(self):
        self.sImage = QPixmap(self.imagen_actual)
        self.sImage = self.sImage.scaled(self.w, self.h)
        self.palette.setBrush(QPalette.Window, QBrush(self.sImage))
        self.setPalette(self.palette)
        print(self.size())

    def resize_jugador_ppal(self):
        if self.started:
            self.jugador.factor_x = self.factor_x
            self.jugador.factor_y = self.factor_y
            self.jugador.resize1()

            self.jugador.position = (self.jugador.position[0] * self.factor_x,
                                    self.jugador.position[1] * self.factor_y)

    def resize_enemigos(self):    
        for oso in self.threads:
            oso.resize1()
            oso.factor_x = self.factor_x
            oso.factor_y = self.factor_y
            oso.position = (oso.position[0] * self.factor_x, 
                            oso.position[1] * self.factor_y)

    def resize_botones(self):
        
        for boton in self.botones:
            if type(boton) == list:
                for b in boton:
                    b.resize1(self.size_font)
            else:
                try:
                    boton.resize1(self.size_font)
                except:
                    pass

    def ranking_partidas(self):
        self.imagen_actual = "images/fondos/ranking.png"
        self.resize_background()
        self.setPalette(self.palette)
        self.menu_widget.setLayout(self.central_widget.layout())
        self.btnRetroceder = Boton(self, 'Retroceder',
                                     btnFondo2 + btnHover2 + \
                                     btnPressed2, self.retroceder_ranking)
        self.botones.append(self.btnRetroceder)
        mejores = MejoresLabel(self, self.size_font * 2, "Mejores Puntajes:")
        hbox_R = QHBoxSimetrica(mejores, 1, self.btnRetroceder, None)
        vbox_R = QVBoxSimetrica(hbox_R, None)
        with open("ptjs.txt", "r", encoding="utf-8") as file:
            lineas = file.read()
            lineas = f.ordenar_puntajes(lineas)
            if lineas:
                for i in range(0, min(3, len(lineas))):
                    p = f.puntajes_to_string(lineas[i])
                    l = RankingLabel(self, self.size_font, "Lugar nº{}: {}".format(i+1, p))
                    image = QLabel(self)
                    image.setGeometry(0,0, self.w / 20,self.w / 20)
                    pixmap = QPixmap(imagen_ranking[i]).scaled(self.w / 25, 
                                                               self.w / 25)
                    image.setAlignment(Qt.AlignCenter)
                    image.setPixmap(pixmap)
                    image.setVisible(True)
                    hbox_aux =  QHBoxSimetrica(image, l, 1, None)
                    vbox_R.addLayout(hbox_aux)
                if len(lineas) >= 3:
                    image = QLabel(self)
                    image.setGeometry(0,0, self.w / 20,self.w / 20)
                    pixmap = QPixmap("images/aux_invisible.png").scaled(self.w / 25, 
                                                                        self.w / 25)
                    image.setAlignment(Qt.AlignCenter)
                    image.setPixmap(pixmap)
                    image.setVisible(True)
                    text = [f.puntajes_to_string(i, 2) for i in lineas[3:10]]
                    for t in text:
                        l2 = RankingLabel(self, self.size_font, t)
                        hbox_aux =  QHBoxSimetrica(image, l2, 1, None)
                        vbox_R.addLayout(hbox_aux)             
            else:

                l = RankingLabel(self, self.size_font, "No hay partidas hasta el momento.")
                hbox_aux = QHBoxSimetrica(1, l, 1, None)
                vbox_R.addLayout(hbox_aux) 
            vbox_R.addStretch(1)              
        self.central_widget.setLayout(vbox_R)

    def escoger_modo(self):

        self.not_pickeado = True
        self.imagen_actual = "images/fondos/picking_background.png"
        self.resize_background()
        self.setPalette(self.palette)
        self.menu_widget.setLayout(self.central_widget.layout())
        self.btnRetroceder = Boton(self, 'Retroceder', btnFondo2 + btnHover2\
                                   + btnPressed2, self.retroceder_ranking)
        self.botones.append(self.btnRetroceder)
        self.label_pj1 = MouseLabel(self)
        self.label_pj2 = MouseLabel(self)
        pixmap1 = QPixmap("images/jugador1/sprite_j1.png")
        pixmap1 = pixmap1.scaled(self.w / 10, self.w / 10)
        pixmap2 = QPixmap("images/jugador2/sprite_jdos1.png")
        pixmap2 = pixmap2.scaled(self.w / 10, self.w / 10)
        self.label_pj1.setPixmap(pixmap1)
        self.label_pj1.mousePressEvent = self.pick_j1
        self.label_pj2.setPixmap(pixmap2)
        self.label_pj2.mousePressEvent = self.pick_j2

        self.timer_picking = QTimer()
        self.timer_picking.timeout.connect(self.mover_picking)
        self.timer_picking.start(200)
        hbox_R = QHBoxSimetrica(1, self.btnRetroceder, None)
        hbox_pjs = QHBoxSimetrica(6, self.label_pj2, 2, 
                                    self.label_pj1, 5, None)
        vbox_R = QVBoxSimetrica(hbox_R, 6, hbox_pjs, 1, None)
        self.central_widget.setLayout(vbox_R)

    def pick_j1(self, event):
        self.botones.pop(-1)
        self.not_pickeado = False
        self.tipo_player = "j1"
        layout_picking = QWidget()
        layout_picking.setLayout(self.central_widget.layout())
        self.cargando()

    def pick_j2(self, event):
        self.botones.pop(-1)
        self.not_pickeado = False
        self.tipo_player = "j2"
        layout_picking = QWidget()
        layout_picking.setLayout(self.central_widget.layout())
        self.cargando() 

    def mover_picking(self):
        if self.not_pickeado:
            pixmap1 = QPixmap(pj1_iniciales[self.contador_picking])
            pixmap1 = pixmap1.scaled(self.w / 10, self.w / 10)
            pixmap2 = QPixmap(pj2_iniciales[self.contador_picking])
            pixmap2 = pixmap2.scaled(self.w / 10, self.w / 10)
            self.label_pj1.setPixmap(pixmap1)
            self.label_pj2.setPixmap(pixmap2)
            self.contador_picking = (self.contador_picking + 1) % 4
        else:
            self.timer_picking.stop()

    def cargando(self):
        self.imagen_actual = "images/fondos/fondo_cargando2.png"
        self.resize_background()
        self.setPalette(self.palette)
        self.cargando_bar  = CargandoBar(self)
        self.timer_cargando = MyQTimer(self, self.cargar_bar, 300)
        self.label_cargando = CargandoQLabel(self, True, choice(datos))      
        vbox = QVBoxSimetrica(3, self.label_cargando, 2, 
                              self.cargando_bar, None)
        self.central_widget.setLayout(vbox)

    def cargar_bar(self):
        if self.value < 100:
            self.value = min(self.value + randint(10,30), 100)
            self.cargando_bar.setValue(self.value)
        else:
            self.timer_cargando.stop()
            cargado = QWidget()
            cargado.setLayout(self.central_widget.layout())
            self.timer_cargando.stop()
            self.value = 0
            self.iniciar_partida()

    def iniciar_partida(self):
        self.contador_partida = 1
        self.menu_herramientas = QPushButton()
        self.label_game = QLabel(self)
        self.label_game.setGeometry(0, 0, self.ancho_menu, self.h)
        self.label_game.setStyleSheet( 
            "background-color:  rgb( 46, 84, 57);"\
            "border-radius: 10px;"\
            "min-width: {} px;".format(self.ancho_menu)+\
            "min-height: {} px;".format(self.ancho_menu)+\
            "padding: 1px;")        
        self.imagen_actual = "images/fondos/bosque51.png"
        hbox_game = QHBoxSimetrica(1, self.label_game, None)
        vbox_game = QVBoxSimetrica(hbox_game, 1, None)
        self.central_widget.setLayout(vbox_game)
        self.jugador = Jugador(self, self.tipo_player)
        self.velocidad_inicial_x = self.jugador.velocidad_x
        self.velocidad_inicial_y = self.jugador.velocidad_y
        self.started = True
        self.jugador.start()
        T, M = True, 1000
        self.p = MyQTimer(self, self.suma_p, 1*M)
        first = MyQTimer(self, self.aparicion_enemigos, 0, T)#primer enemigo
        self.timer_list.append(self.p)
        self.timer_enemigo = MyQTimer(
            self, self.aparicion_enemigos, min(max(expovariate(
                alphas_level[self.etapa_jugador - 1]) * 1000, 5),2))
        self.timer_coins = MyQTimer(self, self.aparicion_coins, 1*M)
        self.timer_food = MyQTimer(self, self.aparicion_food, 1*M)
        self.timer_trampa = MyQTimer(self, self.aparicion_trampas, 1*M)
        self.timer_safe_zone = MyQTimer(self, self.aparicion_safe, 1*M)
        self.timer_list.extend(
            [self.timer_enemigo, self.timer_coins, self.timer_food, 
             self.timer_trampa])
        self.resize_background()
        self.q_aux = None
        self.btnSalir = Boton(self, '  Salir  ',btnFondoSalir, 
                              self.salir, self.size_font/2, "p")
        self.btnPausar = Boton(
            self, '  Pausar  ', btnFondoRadius6, self.game_paused, 
            self.size_font/2, "p"
            )
        self.btnTienda = Boton(
            self, '  Tienda  ', btnFondoTienda, self.abrir_tienda, 
            self.size_font/2, "p"
            )
        self.experiencia_bar = ExperienciaBar(
            self, self.jugador, self.size_font/2
            )
        self.label_puntaje = PuntajeLabel(self, self.size_font / 2)
        self.label_experiencia = ExpLabel(self, self.size_font / 2)
        self.jugador.experienciaBar = self.experiencia_bar
        self.jugador.puntaje_label = self.label_puntaje
        self.item1 = InvetarioLabel(self)
        self.item2 = InvetarioLabel(self)
        self.item3 = InvetarioLabel(self)
        self.item4 = InvetarioLabel(self)
        self.item5 = InvetarioLabel(self)
        self.items_inv.extend([self.item1, self.item2, self.item3, 
            self.item4, self.item5])
        self.toolbar = MyToolBar(
            self, self.label_game, self.item1, self.item2, self.item3, 
            self.item4, self.item5, self.btnTienda, self.btnPausar, 
            self.label_puntaje, self.label_experiencia, self.experiencia_bar,
            self.btnSalir
            )
        self.cosas_menu.extend(
            [self.btnSalir, self.btnPausar,self.btnTienda, self.item1,
            self.item2, self.item3, self.item4, self.item4, self.item5,
            self.experiencia_bar, self.label_puntaje, self.label_experiencia]
            )

        self.addToolBar(Qt.RightToolBarArea, self.toolbar)
        self.tienda_abierta, self.juego_pausado = False, False

    def suma_p(self):
        if self.jugador:
            self.jugador.puntaje += int(datos2[1][1])

    def pasar_nivel(self, PasarEvent):
        self.etapa_jugador += 1
        if self.etapa_jugador == 6:
            self.jugador.puntaje += 20000
            self.salir(False)
        if self.jugador:
           self.jugador.puntaje += int(datos2[3][1]) * self.etapa_jugador + 1500
        else:
            self.imagen_actual = "images/fondos/game_over.png"
            self.resize_background()
            self.setPalette(self.palette)
        self.imagen_actual = "images/fondos/bosque5{}.png".format(self.etapa_jugador)
        self.sImage = QPixmap(self.imagen_actual).scaled(self.w, self.h)
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(self.sImage))
        self.setPalette(self.palette)
        self.restaurar_valores(False)
        self.timer_enemigo.start(expovariate(
                alphas_level[self.etapa_jugador - 1]) * 1000)
        self.sound2 = Music(self, path = "sounds/win.wav", loop=2)

    def restaurar_valores(self, aux = True):
        if self.jugador:
            self.ultimo_puntaje = self.jugador.puntaje

        for dead in self.deads:
            dead.hide()
        for trampa in self.trampas_list:
            for player in trampa.players:
                if player.tipo == "enemigo":
                    player.hide()
            trampa.hide()
        for i in self.threads:
            try:
                i.hide()
            except:
                pass
        self.threads = []

        if self.jugador:
            self.jugador.threads = []
        if aux:
            for c in self.coins_list:
                c.hide()
            for f in self.food_list:
                f.hide()
            for threads in self.threads:
                threads.hide()
            for trampa in self.trampas_list:
                for player in trampa.players:
                    player.hide()
                trampa.hide()
            for tipo in self.items:
                for i in tipo:
                    i.hide()
            for c in self.cuevas_list:
                c.hide()
            for timer in self.timer_list:
                timer.stop()
            self.trampas_list = []
            self.timer_list = []
            self.deads = []
            self.items = []
            self.coins_list = []
            self.cuevas_list = []
            if self.jugador:
                self.jugador.hide()
            self.started = False
            self.tienda_abierta, self.juego_pausado = False, False
            self.cosas_menu = []
            self.jugador, self.q_aux = None, None
            self.pausar_juego()
            self.toolbar.setVisible(False)
            self.alternar_tienda, self.alternar_paused = 0, 0
            self.etapa_jugador = 1

    def salir(self, aux = True):
        if aux:
            soundend = QSound("sounds/game_over.wav", self)
        else:
            soundend = QSound("sounds/win.wav", self)
        soundend.play("sounds/game_over.wav")
        self.restaurar_valores()
        self.guardar_puntaje()

    def guardar_puntaje(self):
        self.imagen_actual = "images/fondos/game_over.png"
        self.resize_background()
        self.setPalette(self.palette)
        w = QWidget()
        w.setLayout(self.central_widget.layout())
        a = RankingLabel(self, self.size_font, "Ingrese su nombre de usuario:")
        self.edit = PuntajeEdit(self, 'Anónimo')
        boton = Boton(
            self, ' Enviar Puntaje ', btnFondo2 + btnHover2 + btnPressed2, 
            self.enviar_puntaje
            )
        hbox = QHBoxSimetrica(self.edit, boton, 1, None)
        vbox = QVBoxSimetrica(a, hbox, 1, None)
        self.botones.append(boton)
        self.central_widget.setLayout(vbox)

    def enviar_puntaje(self):
        self.nombre = self.edit.text()
        with open("ptjs.txt", "a", encoding="utf-8") as file:
            file.write("{};{}\n".format(self.nombre, self.ultimo_puntaje))
        self.menu_inicio()

    def game_paused(self):
        if self.started:
            if self.alternar_paused % 2 == 0:
                self.jugador.teclas_juego[Qt.Key_P] = True
                self.btnPausar.setText("Reanudar")
                if not self.juego_pausado and not self.tienda_abierta:
                    self.pausar_juego()
                    print("juego pausado")
                self.juego_pausado = True
                self.alternar_paused += 1
            else:
                self.jugador.teclas_juego[Qt.Key_P] = False
                self.btnPausar.setText("  Pausar  ")
                if self.juego_pausado and not self.tienda_abierta:
                    self.reanudar_juego()
                    print("juego reanudado")
                self.juego_pausado = False
                self.alternar_paused += 1

    def pausar_sounds(self):
        for sound in self.sounds_list:
            sound.setVolume(0)

    def reanudar_sounds(self):
        for sound in self.sounds_list:
            sound.setVolume(25)

    def pausar_timers(self):
        for timer in self.timer_list:
            timer.stop()

    def reanudar_timers(self):
        for timer in self.timer_list:
            timer.start()

    def pausar_items(self):
        for tipo in self.items:
            for item in tipo:
                item.stop()

    def reanudar_items(self):
        for tipo in self.items:
            for item in tipo:
                item.start()

    def pausar_enemigos(self):
        for oso in self.threads:
            oso.stop()

    def reanudar_enemigos(self):
        for oso in self.threads:
            oso.start()

    def retroceder_ranking(self):
        self.imagen_actual = "images/fondos/bosque6.png"
        self.resize_background()
        ranking_widget = QWidget()
        ranking_widget.setLayout(self.central_widget.layout())
        self.central_widget.setLayout(self.menu_widget.layout())
        self.contador_pag = 0
        self.not_pickeado = False
    
    def instrucciones(self):
        self.imagen_actual = "images/fondos/instrucciones.png"
        self.resize_background()
        self.setPalette(self.palette)
        self.menu_widget.setLayout(self.central_widget.layout())
        self.btnRetroceder = Boton(
            self, 'Retroceder', btnFondo2 + btnHover2 + btnPressed2, 
            self.retroceder_ranking
            )
        self.botones.append(self.btnRetroceder)
        hbox_R = QHBoxSimetrica(1, self.btnRetroceder, None)
        vbox_R = QVBoxSimetrica(hbox_R, 1, None)
        self.central_widget.setLayout(vbox_R)

    def historia(self):
        a = QWidget()
        self.imagen_actual = dict_images[self.contador_pag] 
        self.resize_background()
        self.setPalette(self.palette)

        self.btnRetroceder = Boton(
            self, '  ⇦  ', btnFondoRadius3 + btnHover3, 
            self.retroceder, self.size_font * 2
            )
        if self.contador_pag == 2:
            self.btnAvanzar = Boton(
                self, 'Volver', btnFondoRadius3 + btnHover3, 
                self.retroceder_ranking, self.size_font * 2
                )
        else:
            self.btnAvanzar = Boton(
                self, '  ⇨  ', btnFondoRadius3 + btnHover3, 
                self.avanzar, self.size_font * 2
                )
        hbox_R = QHBoxSimetrica(self.btnRetroceder,1000, self.btnAvanzar,None)
        vbox_R = QVBoxSimetrica(1, hbox_R, None)
        if not self.contador_pag:
            self.menu_widget.setLayout(self.central_widget.layout())
        else:
            a.setLayout(self.central_widget.layout())
        self.central_widget.setLayout(vbox_R)

    def retroceder(self):
        if not self.contador_pag:
            self.retroceder_ranking()
        else:
            self.contador_pag -= 1
            self.historia()

    def avanzar(self):
        self.contador_pag += 1
        self.historia()

    def pausar_juego(self):
        self.pausar_enemigos()
        self.pausar_items()
        self.pausar_timers()
        self.pausar_sounds()

    def reanudar_juego(self):
        self.reanudar_enemigos()
        self.reanudar_items()
        self.reanudar_timers()
        self.reanudar_sounds()

    def abrir_tienda(self):
        self.tienda_widget = MyTienda(
            ancho / 2 - self.x / 2, alto / 2 - self.y / 2, 
            self.w, self.h, self
            )
        if self.started:
            if self.alternar_tienda % 2 == 0:
                self.tienda_widget.show()
                
                self.jugador.teclas_juego[Qt.Key_T] = True
                if not self.tienda_abierta and not self.juego_pausado:
                    self.pausar_juego()
                    self.sound_tienda = Music(self, path = "sounds/tienda.wav")
                    self.sound_tienda.play()
                    print("tienda abierta")
                self.tienda_abierta = True
                self.alternar_tienda += 1
            else:
                self.tienda_widget.hide()
                self.jugador.teclas_juego[Qt.Key_T] = False
                if self.tienda_abierta and not self.juego_pausado:
                    self.sound_tienda.stop()
                    self.reanudar_juego()
                    print("tienda cerrada")

                self.tienda_abierta = False
                self.alternar_tienda += 1

    def pantalla_completa(self):
        if self.alternar_pantalla % 2 == 0:
            print("pantalla_completa")
            self.alternar_pantalla += 1
            self.showFullScreen()
            self.aux_f = True
        else:
            print("pantalla_chica")
            self.alternar_pantalla += 1
            self.showNormal()
            self.aux_f = False
    def keyPressEvent(self, event):
        if self.started:
            key = event.key()
            try:
                self.jugador.teclado_jugador1[key] = True
            except: 
                pass

    def keyReleaseEvent(self, event):
        if self.started:
            key = event.key()
            try:
                self.jugador.teclado_jugador1[key] = False

            except: 
                pass

    def aparicion_enemigos(self):
        if self.started:
            enemigo = Enemigo(
                self, "enemigo", self.jugador, min(f.triang(
                    matriz_level[self.etapa_jugador - 1]), 10))
            self.threads.append(enemigo)
            self.jugador.threads.append(enemigo)
            for trap in self.trampas_list:
                trap.players.append(enemigo)
            self.threads[-1].start(20)
        if len(self.threads) > 6:
            self.timer_enemigo.start(expovariate(
                    alphas_level[self.etapa_jugador - 1]) * 2000)
        else:
            self.timer_enemigo.start(expovariate(
                    alphas_level[self.etapa_jugador - 1]) * 1000)
    def aparicion_food(self):
        if self.started:
            if f.prob_uniforme(1/20):
                item = Item(self, 10, image_food[self.tipo_player], "food")
                self.food_list.append(item)
                self.jugador.items.append(item)
                self.food_list[-1].start(100)

    def aparicion_coins(self):
        if self.started:
            if f.prob_uniforme(1/30):
                item = Item(self, 18, image_coin, "coin")
                self.coins_list.append(item)
                self.jugador.items.append(item)
                self.coins_list[-1].start(100)


    def aparicion_trampas(self):
        if self.started:
            if f.prob_uniforme(1/25):
                item = Trampa(self)
                item.players.append(self.jugador)
                for thread in self.threads:
                    item.players.append(thread)
                self.trampas_list.append(item)
                self.trampas_list[-1].start(100)


    def aparicion_safe(self):
        if self.started:
            if f.prob_uniforme(1/30):
                if len(self.cuevas_list) < 4:
                    item = Item(self, 2, image_safe_zone, "safe_zone")
                    self.cuevas_list.append(item)
                    self.jugador.items.append(item)
                    self.cuevas_list[-1].start(1000)

    def atacar(self, MyAtackEvent):
        pl = MyAtackEvent.player
        enemigo = MyAtackEvent.enemigo
        pl.vida -= enemigo.ataque
        enemigo.vida -= pl.ataque

        if enemigo.vida <= 0 :
            pl.experiencia += 100 * max(enemigo.tamaño - pl.tamaño + 3, 1)
            pl.puntaje += 1000 + int(datos2[2][1]) * int(enemigo.tamaño - pl.tamaño) 

        if self.started:
            self.q_aux = QTimer()
            self.q_aux.timeout.connect(self.parar_ataque_real)
            self.q_aux.setSingleShot(True)
            self.q_aux.start(1000)
            j1 = QSound("sounds/bear1.wav", self)
            j1.play("sounds/bear1.wav")
            e1 = QSound("sounds/bear2.wav", self)
            e1.play("sounds/bear2.wav")
        
    def parar_ataque_real(self):
        if self.started:
            self.jugador.aux_ataque = False
            self.jugador.enemigo_atacado = None
            self.jugador.teclado_jugador1[Qt.Key_W] = False
            self.jugador.teclado_jugador1[Qt.Key_S] = False
            self.q_aux = QTimer()
            self.q_aux.timeout.connect(self.reanudar_ataque_real)
            self.q_aux.setSingleShot(True)
            self.q_aux.start(1000)

    def reanudar_ataque_real(self):
        if self.started:
            self.jugador.aux_ataque = True
            self.jugador.no_paso = True
            self.jugador.chequear_distancias()


    def actualizar_imagen(self, MyPlayerEvent):
        if self.started:
            for i in self.deads:
                i.is_dead = True
            pl = MyPlayerEvent.player
            d = pl.daño
            an = pl.pseudo_angulo
            tipo = pl.tipo
            ftipo = pl.first_tipo
            label = pl.image
            if pl.contador%20 == 0:
                self.sound_walk()
            if not pl.is_dead:
                c = pl.contador_game % 40 // 10 + 1
                pixmap = QPixmap(all_sprites_shits[tipo][d][c])
                l_pixmap = QPixmap(all_sprites_shits[ftipo][d][c])
            else:
                c = pl.contador_game % 60 // 10
                pixmap = QPixmap(entidad_muerta[tipo][c])
                l_pixmap = QPixmap(entidad_muerta[ftipo][c])
            
            pixmap = pixmap.scaled(self.w / 70 * pl.tamaño**0.8, 
                                   self.w / 70 * pl.tamaño**0.8)
            transform = QTransform().rotate(pl.angulo - 180 - an)
            pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
            label.move(pl.position[0], pl.position[1])  
            label.setPixmap(pixmap)
            label.raise_()
            l_pixmap = l_pixmap.scaled(self.w/10, self.w/10)
            l_pixmap = l_pixmap.transformed(transform, Qt.SmoothTransformation)
            self.label_game.setPixmap(l_pixmap) 
            self.label_game.setAlignment(Qt.AlignCenter)


    def actualizar_bar(self, MyPlayerEvent):
        if self.started:
            label = MyPlayerEvent.player.lifeBar

            pl = MyPlayerEvent.player
            label.resize1(self.w /15, self.h/ 40, self.h/100)
            if pl.is_dead:
                if pl.tipo == "enemigo":
                    if pl not in self.deads:
                        self.deads.append(pl)

                label.hide()
            else:
                label.move(pl.centro[0] - label.frameGeometry().width() / 2,
                           pl.centro[1] - pl.alto / 2 - self.h / 35)
            if pl.tipo == "j1" or "j2":
                label.raise_()

    def stop_qtimer(self, QtimerEvent):
        self.e = QtimerEvent
        if QtimerEvent.time:
            print("hel")
            QtimerEvent.qtimer.stop()
            q = QTimer(self)
            q.timeout.connect(self.playplay)
            q.setSingleShot(True)
            q.start(500)
        else:
            print("wtf")
            QtimerEvent.is_dead = True
            QtimerEvent.qtimer.stop()


    def playplay(self):
        for i in self.threads:
            self.e.qtimer.start(20)


    def sound_walk(self):
        if self.started:
            if self.aux_walk:
                a = QSound("sounds/walk2.wav", self)
                a.play("sounds/walk2.wav")
                q = QTimer(self)
                q.timeout.connect(self.aux_to_True)
                q.setSingleShot(True)

                q.start(1000)
                self.aux_walk = False

    def aux_to_True(self):
        if self.started:
            self.aux_walk = True

    def actualizar_imagen_enemigos(self, MyPlayerEvent):
        if self.started:
            pl = MyPlayerEvent.player
            d = pl.daño
            r = pl.rotacion
            tipo = pl.tipo
            label = pl.image
            if pl.is_dead:
                c = pl.contador_dead % 6
                pixmap = QPixmap(entidad_muerta[tipo][c])
            else:
                c = pl.contador_game % 40 // 10 + 1
                pixmap = QPixmap(all_sprites_shits[tipo][d][c])

            pixmap = pixmap.scaled(self.w / 70 * pl.tamaño**0.8, 
                                   self.w / 70 * pl.tamaño**0.8)
            transform = QTransform().rotate(pl.angulo - r)
            pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
            label.move(pl.position[0], pl.position[1])
            label.setPixmap(pixmap)

    def actualizar_item(self, MyImageEvent):
        if self.started:
            m = MyImageEvent
            label = m.image
            pixmap = QPixmap(m.imagenes[m.contador])
            pixmap = pixmap.scaled(self.w / m.tamaño, self.w / m.tamaño)
            label.move(m.x, m.y)
            label.setPixmap(pixmap)

    def sound_effect(self, MySoundEvent):
        if self.started:
            s = MySoundEvent
            aux_sound = QSound(s.path, self)
            aux_sound.play(s.path) 

    def dead_player(self, DeadEvent):
        pl = DeadEvent.player
        if pl.tipo == "enemigo":
            self.deads.append(pl)
        else:
            self.salir()

    def set_objeto(self, ObjetoEvent):
        if self.jugador:
            obj = ObjetoEvent
            obj.objeto.set_valor(obj.valor)
            if obj.tipo == "puntaje":
                self.item1.change_event(self.jugador.inventario[1])
                self.item2.change_event(self.jugador.inventario[2])
                self.item3.change_event(self.jugador.inventario[3])
                self.item4.change_event(self.jugador.inventario[4])
                self.item5.change_event(self.jugador.inventario[5])

if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    mi_juego = MenuPrincipal(1920/1.5, 1080/1.5)
    mi_juego.show()

    app.exec()

