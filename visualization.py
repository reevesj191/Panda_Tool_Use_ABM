from Model_definition import *

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

server = ModularServer(PrimToolModel,
                       [grid],
                       "Primate Tool Model",
                       {"N":10, "width":100, "height":100})
server.port = 8521 # The default
server.launch()