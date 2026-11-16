# autores: 
# Carlos Leonardo Gonzalez Vilchis A01754553
# Maximiliano Arriaga Navarro A01753449

from modelo import ModeloLimpieza
from agentes import Robot

from mesa.visualization import (
	SolaraViz,
	SpaceRenderer,
)
from mesa.visualization.components import AgentPortrayalStyle


# proposito: define como se dibuja cada agente, las baldosas son cuadros (blancas si estan limpias, cafes si estan sucias) y los robots son circulos azules
# parametros: agente (baldosa o robot)
# retorno: el estilo de dibujo del agente
def retratarAgente(agente):
	if isinstance(agente, Robot):
		estilo = AgentPortrayalStyle(color = "tab:blue", marker = "o", size = 40, zorder = 2)
	else:
		colorBaldosa = "saddlebrown" if agente.estaSucia else "white"
		estilo = AgentPortrayalStyle(color = colorBaldosa, marker = "s", size = 60, zorder = 1)
	return estilo


# proposito: ajusta el aspecto de la grafica
# parametros: ejes
# retorno: ninguno.
def postProcesar(ejes):
	ejes.set_aspect("equal")
	ejes.set_xticks([])
	ejes.set_yticks([])


parametrosModelo = {
	"rng": {
		"type": "InputText",
		"value": 42,
		"label": "Semilla aleatoria",
	},
	"ancho": {
		"type": "SliderInt",
		"value": 20,
		"label": "Ancho",
		"min": 5,
		"max": 40,
		"step": 1,
	},
	"alto": {
		"type": "SliderInt",
		"value": 20,
		"label": "Alto",
		"min": 5,
		"max": 40,
		"step": 1,
	},
	"cantidadRobots": {
		"type": "SliderInt",
		"value": 5,
		"label": "Numero de robots",
		"min": 1,
		"max": 50,
		"step": 1,
	},
	"porcentajeSucio": {
		"type": "SliderFloat",
		"value": 0.3,
		"label": "Porcentaje de baldosas sucias",
		"min": 0.0,
		"max": 1.0,
		"step": 0.01,
	},
	"tiempoMaximo": {
		"type": "SliderInt",
		"value": 1000,
		"label": "Tiempo maximo",
		"min": 100,
		"max": 5000,
		"step": 100,
	},
}

# crea la instancia inicial del modelo con los valores por defecto
modeloInicial = ModeloLimpieza()

renderizador = SpaceRenderer(modeloInicial, backend = "matplotlib").setup_agents(retratarAgente)
renderizador.render()
renderizador.post_process = postProcesar

# crea la pagina de solara
page = SolaraViz(
	modeloInicial,
	renderizador,
	model_params = parametrosModelo,
	name = "Robot aspiradora",
)
page 