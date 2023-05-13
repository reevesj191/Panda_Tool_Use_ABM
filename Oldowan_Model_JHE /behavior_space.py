from Model_definition import *
from mesa.batchrunner import BatchRunnerMP, batch_run
from multiprocessing import freeze_support


MAX_TS = 75000
ITERATIONS = 30
N_CORE = 60

# FxJj50

params = {"width": 250,
                "height":  250,
                "Na": 100,
                "max_ts": MAX_TS,
                "scenario": ("FxJj50"),
                "search_rad": (2, 10),
                "Nn": (100,2000),
                "treesdie": True,
                "Ns": 100,
                "max_uses": (5, 20, 40), 
                "mem_safe": True
                }

if __name__ == '__main__':
    freeze_support()

    batch_run(model_cls=PrimToolModel,  
    parameters= params, 
    number_processes= N_CORE,
    iterations= ITERATIONS,
    max_steps=75001,
    data_collection_period=1)

# FxJj20E

params = {"width": 250,
                "height":  250,
                "Na": 100,
                "max_ts": MAX_TS,
                "scenario": ("FxJj20E"),
                "search_rad": (2, 10),
                "Nn": (100,2000),
                "treesdie": True,
                "Ns": 100,
                "max_uses": (5, 20, 40), 
                "mem_safe": True
                }

if __name__ == '__main__':
    freeze_support()

    batch_run(model_cls=PrimToolModel,  
    parameters= params, 
    number_processes= N_CORE,
    iterations= ITERATIONS,
    max_steps=75001,
    data_collection_period=1)

# Panda

params = {"width": 250,
                "height":  250,
                "Na": 100,
                "max_ts": MAX_TS,
                "scenario": ("Panda"),
                "search_rad": (2,10),
                "Nn": 2000,
                "treesdie": True,
                "Ns": 100,
                "max_uses": (5, 20, 40), 
                "mem_safe": True
                }

if __name__ == '__main__':
    freeze_support()

    batch_run(model_cls=PrimToolModel,  
    parameters= params, 
    number_processes= N_CORE,
    iterations= ITERATIONS,
    max_steps=75001,
    data_collection_period=1)

# Reduced

    params = {"width": 250,
                "height":  250,
                "Na": 100,
                "max_ts": MAX_TS,
                "scenario": ("Reduced"),
                "search_rad": (2,10),
                "Nn": 2000,
                "treesdie": True,
                "Ns": 100,
                "max_uses": (5, 20, 40), 
                "mem_safe": True
                }

if __name__ == '__main__':
    freeze_support()

    batch_run(model_cls=PrimToolModel,  
    parameters= params, 
    number_processes= N_CORE,
    iterations= ITERATIONS,
    max_steps=75001,
    data_collection_period=1)

