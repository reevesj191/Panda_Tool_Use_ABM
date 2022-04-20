from Model_definition import *
from mesa.visualization.modules import CanvasGrid, ChartModule
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
        portrayal["Layer"] = "1"
        portrayal["r"] = 1


    if type(agent) is StoneSource:

        portrayal["Color"] = "grey"
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = "2"
        portrayal["r"] = 1

    if type(agent) is NutTree:

        portrayal["Color"] = "green"
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = "4"
        portrayal["r"] = 1

    if type(agent) is PoundingTool:

        portrayal["Color"] = "red"
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = "3"
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
                       "Reeves et. al. (2021) Modeling a Primate Technological Niche",
                       {"Na": 100,
                        "search_rad": 2,
                        "Ns": 10,
                        "Nn": 200,
                        "tool_acq": "nearest",
                        "max_ts": 500,
                        "width": h, "height": w,
                        "treesdie": True,
                        "mem_safe": True, # This must be kept false in order for the visualization to work properly
                        "db_name": "Flaker_Model/Visualization"})

server.port = 1234 # The default

server.launch()
