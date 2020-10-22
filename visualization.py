from Model_definition import *

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


h = 25
w = 25

def agent_portrayal(agent):

    portrayal = {"Shape": "circle",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 1}

    if type(agent) is PrimAgent:

        portrayal["Color"] = "Brown"
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = "4"


    if type(agent) is StoneSource:

        portrayal["Color"] = "grey"
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = "2"

    if type(agent) is NutTree:

        portrayal["Color"] = "green"
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = "3"

    if type(agent) is PoundingTool:

        portrayal["Color"] = "black"
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = "1"
        portrayal["radius"] = ".25"

    return portrayal



grid = CanvasGrid(agent_portrayal, h, w, 750, 750)

server = ModularServer(PrimToolModel,
                       [grid],
                       "Primate Tool Model",
                       {"Na":5,
                        "Ns": 50,
                        "Nn": 25,
                        "width":h, "height":w})
server.port = 8521 # The default
server.launch()