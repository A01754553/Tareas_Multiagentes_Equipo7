# autores: 
# Carlos Leonardo Gonzalez Vilchis A01754553
# Maximiliano Arriaga Navarro A01753449

from mesa import Model
from mesa.discrete_space import OrthogonalMooreGrid
from agentes import Baldosa, Robot


class ModeloLimpieza(Model):

	# proposito: crea la habitacion con sus baldosas, su suciedad y sus robots.
	# parametros: ancho, alto, cantidad de robots, porcentaje de suciedad, tiempo maximo en pasos, y el rng
	# retorno: ninguno
	def __init__(self, ancho = 20, alto = 20, cantidadRobots = 5, porcentajeSucio = 0.3, tiempoMaximo = 1000, rng = None):
		super().__init__(rng = rng)
		self.tiempoMaximo = tiempoMaximo
		self.pasosEjecutados = 0

		# los bordes son paredes y cada celda admite varios agentes
		self.grid = OrthogonalMooreGrid((ancho, alto), torus = False, random = self.random)

		for celda in self.grid.all_cells:
			Baldosa(self, celda)

		self.ensuciarBaldosas(porcentajeSucio)

		celdaInicial = self.grid[(0, 0)]
		for numeroRobot in range(cantidadRobots):
			Robot(self, celdaInicial)

		self.running = True

	# proposito: ensucia al azar la cantidad de baldosas que indica el porcentaje
	# parametros: porcentaje de suciedad
	# retorno: ninguno
	def ensuciarBaldosas(self, porcentajeSucio):
		baldosas = self.agents_by_type[Baldosa]
		cantidadSucias = round(len(baldosas) * porcentajeSucio)
		for baldosa in self.random.sample(baldosas.to_list(), cantidadSucias):
			baldosa.estado = Baldosa.SUCIA

	# proposito: cuenta las baldosas que siguen sucias
	# retorno: numero de baldosas sucias
	def contarSucias(self):
		sucias = self.agents_by_type[Baldosa].select(lambda baldosa: baldosa.estaSucia)
		return len(sucias)

	# proposito: calcula el porcentaje de baldosas limpias
	# retorno: porcentaje de baldosas limpias entre 0.0 y 100.0
	def calcularPorcentajeLimpias(self):
		total = len(self.agents_by_type[Baldosa])
		return (total - self.contarSucias()) / total * 100.0

	# proposito: suma los movimientos realizados por todos los robots
	# retorno: total de movimientos de todos los robots
	def contarMovimientos(self):
		return sum(self.agents_by_type[Robot].get("cantidadMovimientos"))

	# proposito: avanza un paso y todos los robots actuan en orden aleatorio y despues se revisa si la simulacion debe terminar.
	# retorno: ninguno
	def step(self):
		self.agents_by_type[Robot].shuffle_do("step")
		self.pasosEjecutados += 1
		if self.contarSucias() == 0 or self.pasosEjecutados >= self.tiempoMaximo:
			self.running = False