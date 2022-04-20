from Model_definition import *
from mesa.batchrunner import batch_run
from multiprocessing import freeze_support



#FxJj 50

params = {"width": 250,
                "height":  250,
                "Na": 100,
                "max_ts": 75000,
                "Nn": 2000,
                "treesdie": True,
                #"db_name": "FxJj50",
                "Ns": (10,100,500),
                "tool_size_mean": 125,
                "tool_size_min": 10,
                "tool_size_sd": 92,
                "frag_size_mean": 5.6,
                "frag_size_min": 1,
                "frag_size_sd": 8.7
                }

if __name__ == '__main__':
    freeze_support()

    batch_run(model_cls=PrimToolModel,  
    parameters= params, 
    number_processes= 40,
    iterations= 20,
    max_steps=75001,
    data_collection_period=1)

#FxJj20E
params = {"width": 250,
                "height":  250,
                "Na": 100,
                "max_ts": 75000,
                "Nn": 2000,
                "treesdie": True,
                #"db_name": "FxJj20",
                "Ns": (10,100,500),
                "tool_size_mean": 218,
                "tool_size_min": 34,
                "tool_size_sd": 197,
                "frag_size_mean": 10, 
                "frag_size_min": 1,
                "frag_size_sd": 15.9
                }

if __name__ == '__main__':
    freeze_support()

    batch_run(model_cls=PrimToolModel,  
    parameters= params, 
    number_processes= 40,
    iterations= 20,
    max_steps=75001,
    data_collection_period=1)

#FxJj16
params = {"width": 250,
                "height":  250,
                "Na": 100,
                "max_ts": 75000,
                "Nn": 2000,
                "treesdie": True,
                #"db_name": "FxJj16",
                "Ns": (10,100,500),
                "tool_size_mean": 535,
                "tool_size_min": 103,
                "tool_size_sd": 520, 
                "frag_size_mean": 150, 
                "frag_size_min": 26,
                "frag_size_sd": 146
}

if __name__ == '__main__':
    freeze_support()

    batch_run(model_cls=PrimToolModel,  
    parameters= params, 
    number_processes= 40,
    iterations= 20,
    max_steps=75001,
    data_collection_period=1)