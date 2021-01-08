from Model_definition import *
from mesa.batchrunner import BatchRunner, BatchRunnerMP

fixed_params = {"width": 250,
                "height":  250,
                "Na": 100,
                "max_ts": 100000,
                "tool_acq": "nearest",
                "db_name": "Experiment_3"
}

variable_params = {
    "Nn": (100, 500, 1000, 2000),
    "Ns": (10, 100, 500, 1000),
    "max_ts": (25000, 50000, 75000),
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
# variable_params = {
#
#     "treesdie":(True, False),
# }


# batch_run = BatchRunner(PrimToolModel,
#                         fixed_parameters=fixed_params,
#                         variable_parameters=variable_params,
#                         iterations=1,
#                         max_steps=1000000001)
#
# batch_run.run_all()

mp_batch_run = BatchRunnerMP(model_cls=PrimToolModel,
                              nr_processes=70,
                              variable_parameters=variable_params,
                              fixed_parameters=fixed_params,
                              iterations=1,
                              max_steps=1000000000001)

mp_batch_run.run_all()

