This is repository where the code for the agent-based model published in "Modeling a primate technological niche" is kept and actively maintained.

# Using This Code

Running this code is a simple as downloading the folder and running either the behavior_space.py or visualization.py from your terminal or prefered IDE. Ensure that all of the files associated with the respository remain in the same folder in order to ensure that the code runs properly. 

## Requirements and Dependencies

This model was developed using python 3.8.10 using the python agent-based modeling framework mesa. Be sure to  install the python library mesa prior to running this model. All other dependencies come with python 3.8 when it is installed or will be installed when you install mesa. 

Alternatively, you can set up python to use the virtual environment panda_venv. "panda_venv" is a virtual environment that contains the version of python and libraries that were used to develop the model.

## Running a single instance of the model

### Visualization.py

## Running parameter sweeps

To run the model on multiple different settings use behavior_space.py. This will allow you to define both fixed and variable parameters for the model to iterate through. The setttings currently provided in this code are those which were presented in the paper. This will allow you to reproduce the results. 

### Parallel Processing

There is an option for taking advantage of the parallel prcoessing. However, the code necessary for this to work is operating system dependent. You will need to comment out the blocks of code that do not match your operating system. 

## Output

The raw data of the model is bundled into an individual SQLite database. Each iteration is given its own database. Use the compile.py script to aggregate all of the runs into a single database. SQL is preferred over excel or csv files as the output of the models can be very large in size. This is paricularly the case when all iterations are bundled together. This allows the user to query the database for the specific data they need so that they do not have to load the entire dataset directly into memory during analysis.   

# Bugs, Errors, and Feedback

Feel free to message me with any issues you have using this code. I will do my best to rectify any issues that may arise. 




 
