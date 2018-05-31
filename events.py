

class PasarNivelEvent:
	def __init__(self):
		self.url = "images/fondos/pasar_nivel.png"

class SetEvent:
	def __init__(self, objeto, valor, tipo=None):
		self.objeto = objeto
		self.valor = valor
		self.tipo = tipo
class DeadEvent:
	def __init__(self, player):
		self.player = player

class StopEvent:
    def __init__(self, qtimer, timee= None):
        self.qtimer = qtimer
        self.time = timee

class HidePlayerEvent:
    def __init__(self, player):
        self.player = player

class ShowPlayerEvent:
    def __init__(self, player):
        self.player = player

class SoundEvent:
    def __init__(self, path):
        self.path = path

class MovePlayerEvent:
    def __init__(self, player):
        self.player = player

class MoveBarEvent:
    def __init__(self, progressBar, player):
        self.progressBar = progressBar
        self.player = player

class AttackEvent:
    def __init__(self, player, enemigo):
        self.player = player  
        self.enemigo = enemigo
        
class MoveImageEvent:
    def __init__(self, image, contador, x, y, imagenes, tipo, tamaño):
        self.image = image
        self.contador = contador
        self.x = x
        self.y = y
        self.imagenes = imagenes
        self.tipo = tipo
        self.tamaño = tamaño