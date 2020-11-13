from Model_definition import *
from mesa.batchrunner import BatchRunner, BatchRunnerMP

fixed_params = {"width": 500,
                "height": 500,
                "Na": 50,
                "tool_acq": "nearest",
                "db_name": "11_13_2020_wide_variation_agents"
}


variable_params = {
    "Nn": (50, 100, 150, 300, 400, 500),
    "Ns": (10, 30, 50, 100, 200, 300),
    "max_ts": (100000,1000000, 1000000),
    "treesdie":(True, False),
}


batch_run = BatchRunner(PrimToolModel,
                        fixed_parameters=fixed_params,
                        variable_parameters=variable_params,
                        iterations=10,
                        max_steps=1000000001)

batch_run.run_all()

# mp_batch_run = BatchRunnerMP(model_cls=PrimToolModel,
#                              nr_processes=4,
#                              variable_parameters=variable_params,
#                              fixed_parameters=fixed_params,
#                              iterations=30)
#
# mp_batch_run.run_all()

