# autores: 
# Carlos Leonardo Gonzalez Vilchis A01754553
# Maximiliano Arriaga Navarro A01753449

from mesa.discrete_space import CellAgent, FixedAgent


class Baldosa(FixedAgent):
	LIMPIA = 0
	SUCIA = 1

	# proposito: crea una baldosa del piso en la celda indicada
	# parametros: modelo (modelo al que pertenece), celda (donde se coloca),
	#             estadoInicial (limpia o sucia)
	# retorno: ninguno
	def __init__(self, modelo, celda, estadoInicial = LIMPIA):
		super().__init__(modelo)
		self.cell = celda
		self.estado = estadoInicial

	# proposito: indica si la baldosa esta sucia
	# retorno: verdadero si esta sucia, falso si esta limpia
	@property
	def estaSucia(self):
		return self.estado == self.SUCIA

	# proposito: deja la baldosa limpia
	# retorno: ninguno
	def limpiar(self):
		self.estado = self.LIMPIA


class Robot(CellAgent):

	# proposito: crea la aspiradora en la celda indicada
	# parametros: modelo (modelo al que pertenece), celda (donde inicia)
	# retorno: ninguno
	def __init__(self, modelo, celda):
		super().__init__(modelo)
		self.cell = celda
		self.cantidadMovimientos = 0

	# proposito: busca la baldosa del piso que esta debajo del robot
	# retorno: la baldosa de la celda actual
	def obtenerBaldosa(self):
		baldosa = None
		for agente in self.cell.agents:
			if isinstance(agente, Baldosa):
				baldosa = agente
		return baldosa

	# proposito: revisa si ya hay un robot en la celda indicada
	# parametros: celda que se va a revisar
	# retorno: verdadero si hay un robot en la celda, falso si no
	def hayRobot(self, celda):
		ocupada = False
		for agente in celda.agents:
			if isinstance(agente, Robot):
				ocupada = True
		return ocupada

	# proposito: elige al azar una celda vecina para moverse
	# retorno: la celda elegida, o ninguna si esta ocupada por otro robot
	def elegirDestino(self):
		destino = self.cell.neighborhood.select_random_cell()
		if self.hayRobot(destino):
			destino = None
		return destino

	# proposito: ejecuta un paso del robot. si la celda esta sucia aspira y si esta limpia intenta moverse a una celda vecina
	# retorno: ninguno.
	def step(self):
		baldosa = self.obtenerBaldosa()
		if baldosa.estaSucia:
			baldosa.limpiar()
		else:
			destino = self.elegirDestino()
			if destino is not None:
				self.cell = destino
				self.cantidadMovimientos += 1