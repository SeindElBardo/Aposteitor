import random
import math
import text

class Jugador(): # Llamado apostador en la mayoría de las variables
	def __init__(self, nombre, dineros):
		self.nombre = nombre
		self.dineros = self.dinerosIniciales = dineros

	def moverDineros(self, cantidad):
		if (self.dineros + cantidad) >= 0:
			self.dineros = self.dineros + cantidad

	def apostar(self, cantidad):
		#Gestionar que no tenga pasta
		self.moverDineros(-cantidad)
		return Apuesta(self, cantidad)

	def resultados(self):
		return self.dineros - self.dinerosIniciales

class Pnj(Jugador): # Para que no explote
	def __init__(self, nombre, media, varianza, dineros = float("inf")):
		super(Pnj, self).__init__(nombre, dineros)
		self.media = media
		self.varianza = varianza

	def generarCantidad(self):
		return math.ceil(random.normalvariate(self.media, self.varianza))

class Participante():
	def __init__(self, nombre):
		self.nombre = nombre
		self.apuestas = []
						
class Apuesta():
	def __init__(self, apostador, cantidad):
		self.apostador = apostador
		self.cantidad = cantidad

class Ronda():
	def __init__(self):
		self.apostadores = []
		self.pnjs = []
		self.participantes = []
		self.bote = 0.0
		self.boteGanador = 0.0 # Es necesario para que se haga la proporción con el dinero ganado
		self.ganadores = []
		# Podría mejorar añadiendole un nivel de dramatismo que condicione las apuestas de pnjs

	def addParticipante(self,participante):
		#No puede haber uno con el mismo nombre
		if not [x for x in self.participantes if x.nombre == participante.nombre] and participante not in self.participantes:
			self.participantes.append(participante)
			return 0
		return -1

	def getApostador(self, nombre):
		aux = [x for x in self.participantes if x.nombre == participante.nombre]
		if h:
			return h.pop()
		return None

	def crearApuesta(self, apostador, cantidad, participante):
		"""Deben llegar objetos"""
		apuesta = apostador.apostar(cantidad)
		participante.apuestas.append(apuesta)
		self.bote += cantidad
		return text.bet(apostador.nombre, str(cantidad), participante.nombre)

	def proclamarGanador(self, ganadores):
		for ganador in ganadores:
			for apuesta in ganador.apuestas:
				self.boteGanador += apuesta.cantidad

	def repartirPremio(self, ganadores):
		report = "" # Se genera un report con los resultados de las apuestas
		proporcion = self.bote/self.boteGanador;
		report += text.rpTotal
		for ganador in ganadores:
			report += text.rpBetOf(ganador.nombre)
			for apuesta in ganador.apuestas:
				premio = math.floor(apuesta.cantidad*proporcion*100)/100
				apuesta.apostador.moverDineros(premio)
				report += text.rpBetResults(apuesta.apostador.nombre, str(premio))

		return report

	def loadPNJs(self):
		try:
			fileHandle = open("pnjs.txt", "r")
		except:     
			fileHandle = open("pnjs.txt", "w")
			fileHandle.close()
			return
		pnjsList = fileHandle.readlines()
		index = 0
		for pnj in pnjsList:
			pnj = pnj[:-1]#Quitamos el salto de línea    
			pnjAtr = pnj.split(';')#Creamos una lista con los datos del pnj
			self.pnjs.append(Pnj(pnjAtr[0], int(pnjAtr[1]), float(pnjAtr[2])))
			fileHandle.close()


	def generarApuestasDeRelleno(self, cantidad):
		"""Con este metodo creamos apuestas hechas por personajes no jugadores."""
		for x in range(1,cantidad):
			pnj = random.choice(self.pnjs)
			self.crearApuesta(pnj, pnj.generarCantidad(), random.choice(self.participantes))