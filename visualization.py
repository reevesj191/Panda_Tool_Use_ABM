from Model_definition import *
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

h = 250
w = 250

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

chart = ChartModule([{"Label": "Trees Available",
                     "Color": "Black"}],
                    data_collector_name= 'tree_datacollector')

chart2 = ChartModule([{"Label": "Trees Near Sources",
                     "Color": "Grey"}],
                    data_collector_name= 'tree_datacollector')

chart3 = ChartModule([{"Label": "Trees Near Pounding Tools",
                     "Color": "Grey"}],
                    data_collector_name= 'tree_datacollector')





server = ModularServer(PrimToolModel,
                       [chart, chart2, chart3],
                       "Primate Tool Model",
                       {"Na": 200,
                        "search_rad": 2,
                        "Ns": 10,
                        "Nn": 2000,
                        "tool_acq": "nearest",
                        "max_ts": 1000000000,
                        "width": h, "height": w,
                        "treesdie": True,
                        "db_name": "delete.db"})

server.port = 1234 # The default

server.launch()