from Model_definition import *
from mesa.batchrunner import BatchRunner, BatchRunnerMP

fixed_params = {"width": 100,
                "height": 100,
                "max_ts": 100000,
                "Na": 100,
                "treesdie": True,
}


variable_params = {
    "Ns": (10, 20,30,40),
    "Nn": (10, 20, 30, 40),
    "tool_acq": ("nearest","random")
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
