from Model_definition import *
import pandas as pd

print("Running Model....")

model = PrimToolModel(Na=100,
                      Ns=100,
                      Nn=100,
                      height=100,
                      width=100,
                      treesdie=False)

for i in range(100000):
    model.step()

mesa_id = []
pos = []
x = []
y = []
size = []


print("Writing Stone Data")
for agent in model.schedule.agents:

    if type(agent) is PoundingTool:

        mesa_id.append(agent.unique_id)
        pos.append(agent.pos)
        x.append(agent.pos[0])
        y.append(agent.pos[1])
        size.append(agent.Tool_size)




df = pd.DataFrame(list(zip(mesa_id, pos, x, y, size)),
                           columns= ['Mesa_ID', 'Coords','X', 'Y', 'size'])

df.to_csv("/Users/jonathanreeves/Documents/GitHub/Primate_Tool_Use_ABM/Test_Results_Stones.csv")



mesa_id = []
pos = []
x = []
y = []

for agent in model.schedule.agents:

    if type(agent) is StoneSource:

        mesa_id.append(agent.unique_id)
        pos.append(agent.pos)
        x.append(agent.pos[0])
        y.append(agent.pos[1])


df = pd.DataFrame(list(zip(mesa_id, pos, x, y)),
                           columns= ['Mesa_ID', 'Coords','X', 'Y'])

df.to_csv("/Users/jonathanreeves/Documents/GitHub/Primate_Tool_Use_ABM/Test_Results_Sources.csv")


mesa_id = []
pos = []
x = []
y = []

for agent in model.schedule.agents:

    if type(agent) is NutTree:
        mesa_id.append(agent.unique_id)
        pos.append(agent.pos)
        x.append(agent.pos[0])
        y.append(agent.pos[1])

df = pd.DataFrame(list(zip(mesa_id, pos, x, y)),
                  columns=['Mesa_ID', 'Coords', 'X', 'Y'])

df.to_csv("/Users/jonathanreeves/Documents/GitHub/Primate_Tool_Use_ABM/Test_Results_Trees.csv")