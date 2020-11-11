from Model_definition import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


h = 50
w = 50

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
        portrayal["r"] = .5


    if type(agent) is StoneSource:

        portrayal["Color"] = "grey"
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = "3"
        portrayal["r"] = .75

    if type(agent) is NutTree:

        portrayal["Color"] = "green"
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = "3"

    if type(agent) is PoundingTool:

        portrayal["Color"] = "red"
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = "4"
        portrayal["r"] = ".5"

    if agent.active is False:

        portrayal["Color"] = "black"
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = "5"
        portrayal["r"] = ".25"

    else:
        pass

    return portrayal



grid = CanvasGrid(agent_portrayal, h, w, 750, 750)

server = ModularServer(PrimToolModel,
                       [grid],
                       "Primate Tool Model",
                       {"Na": 50,
                        "search_rad": 1,
                        "Ns": 200,
                        "Nn": 200,
                        "max_ts": 1000000,
                        "width": h, "height": w,
                        "treesdie": False})
server.port = 3456 # The default

server.launch()