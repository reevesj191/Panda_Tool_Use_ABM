from Model_definition import *

print("Running Model....")

model = PrimToolModel(Na=100, # Number of agents
                      Ns=100, # Number of sources
                      Nn=50,  # Number of Trees  
                      db_name="output", # Name of the folder where the output is saved
                      height=100, # Height of the grid space
                      width=100, # Width of the grid space
                      treesdie=True, # Whether or not the Trees will change location 
                      max_ts= 100) # Number of time steps the model will run for


model.run_model()

print("Model_Completed")