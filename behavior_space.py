from Model_definition import *
from mesa.batchrunner import BatchRunnerMP
from multiprocessing import freeze_support


fixed_params = {"width": 250,
                "height":  250,
                "Na": 100,
                "max_ts": 75000,
                "tool_acq": "nearest",
                "db_name": "Param_Sweep"
}

variable_params = {
    "Nn": (100,500,1000,2000),
     "Ns": (10,100,500),
    "treesdie":(True, False),
}


if __name__ == '__main__':
    freeze_support()

    mp_batch_run = BatchRunnerMP(model_cls=PrimToolModel,
                             nr_processes=60,
                             variable_parameters=variable_params,
                             fixed_parameters=fixed_params,
                             iterations=30,
                             max_steps=750001)

    mp_batch_run.run_all()

