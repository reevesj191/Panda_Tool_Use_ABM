from Model_definition import *
from mesa.batchrunner import BatchRunner, BatchRunnerMP

fixed_params = {"width": 500,
                "height": 500,
                "Na": 50
}


variable_params = {
    "Ns": (50, 75, 100, 125, 150),
    "Nn": (5, 10, 15, 20, 25, 30),
    "tool_acq": ("nearest","random"),
    "treesdie":(False, True),
    "max_ts": (1000,10000,100000,1000000)
}

batch_run = BatchRunner(PrimToolModel,
                        fixed_parameters=fixed_params,
                        variable_parameters=variable_params,
                        iterations=1,
                        max_steps=1000001)

batch_run.run_all()

# mp_batch_run = BatchRunnerMP(model_cls=PrimToolModel,
#                              nr_processes=4,
#                              variable_parameters=variable_params,
#                              fixed_parameters=fixed_params,
#                              iterations=30)
#
# mp_batch_run.run_all()

