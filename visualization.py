from Model_definition import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


h = 100
w = 100

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
        portrayal["r"] = 1


    if type(agent) is StoneSource:

        portrayal["Color"] = "grey"
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = "3"
        portrayal["r"] = 1

    if type(agent) is NutTree:

        portrayal["Color"] = "green"
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = "3"
        portrayal["r"] = 1

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



grid = CanvasGrid(agent_portrayal, h, w)

server = ModularServer(PrimToolModel,
                       [grid],
                       "Primate Tool Model",
                       {"Na": 100,
                        "search_rad": 1,
                        "Ns": 50,
                        "Nn": 500,
                        "max_ts": 10,
                        "width": h, "height": w,
                        "treesdie": True,
                        "db_name": "test2.db"})

server.port = 1234 # The default

server.launch()