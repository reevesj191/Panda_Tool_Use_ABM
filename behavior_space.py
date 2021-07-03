from Model_definition import *
from mesa.batchrunner import BatchRunnerMP
from multiprocessing import freeze_support

# fixed_params = {"width": 250,
#                 "height":  250,
#                 "Na": 100,
#                 "Ns": 100,
#                 "Nn": 2000,
#                 "max_ts": 75000,
#                 "tool_acq": "nearest",
#                 "recycle_priority": False,
#                 "db_name": "Experiment_PNAS"
# }


fixed_params = {"width": 250,
                "height":  250,
                "Na": 100,
                "max_ts": 75000,
                "tool_acq": "nearest",
                "db_name": "Experiment_PNAS"
}

variable_params = {
    "Nn": (100,500,1000,2000),
     "Ns": (10,100,500),
    "treesdie":(True, False),
}


# ## Single Run
#
# fixed_params = {"width": 100,
#                 "height": 100,
#                 "Na": 50,
#                 "Nn": 100,
#                 "Ns": 30,
#                 "max_ts": 1000000,
#                 "tool_acq": "nearest",
#                 "db_name": "Single_Run"
# }
#


# batch_run = BatchRunner(PrimToolModel,
#                         fixed_parameters=fixed_params,
#                         variable_parameters=variable_params,
#                         iterations=1,
#                         max_steps=1000000001)
#
# batch_run.run_all()

if __name__ == '__main__':
    freeze_support()

    mp_batch_run = BatchRunnerMP(model_cls=PrimToolModel,
                             nr_processes=60,
                             variable_parameters=variable_params,
                             fixed_parameters=fixed_params,
                             iterations=30,
                             max_steps=10000000000)

    mp_batch_run.run_all()

