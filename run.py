from Model_definition import *
import pandas as pd

print("Running Model....")

model = PrimToolModel(Na=100,
                      Ns=100,
                      Nn=50,
                      height=100,
                      width=100,
                      treesdie=True,
                      max_ts= 100)


model.step()