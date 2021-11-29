from Model_definition import *
from mesa.batchrunner import BatchRunnerMP
from multiprocessing import freeze_support



# PARAMTERS THAT WILL REMAIN THE SAME IN ALL RUNS

fixed_params = {"width": 250,
                "height":  250,
                "Na": 100,
                "max_ts": 75000,
                "db_name": "Param_Sweep"
}

# PARAMETERS TO BE VARIED

variable_params = {
    "Nn": (100,500,1000,2000),
     "Ns": (10,100,500),
    "treesdie":(True, False),
}

if __name__ == '__main__':
    freeze_support()

    mp_batch_run = BatchRunnerMP(model_cls=PrimToolModel,
                             nr_processes=2, # Number of cores to use
                             variable_parameters=variable_params, # See line 18 
                             fixed_parameters=fixed_params, # See line 9
                             iterations=30, # The number of interations for each combination of parameters
                             max_steps=750001) # Make sure this number if greater than "max_ts" on line 12

    mp_batch_run.run_all()

