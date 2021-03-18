from Model_definition import *
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

h = 5
w = 5

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
                       [grid, chart3],
                       "Primate Tool Model",
                       {"Na": 1,
                        "search_rad": 2,
                        "Ns": 1,
                        "Nn": 2,
                        "tool_acq": "nearest",
                        "recycle_priority": True,
                        "max_ts": 2000,
                        "width": h, "height": w,
                        "treesdie": False,
                        "mem_safe": False,
                        "db_name": "delete.db"})

server.port = 1234 # The default

server.launch()