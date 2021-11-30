This is repository where the code for the agent-based model published in "Modeling a primate technological niche" is kept and actively maintained.

# Using This Code

Running this code is a simple as downloading the folder and running either the run.py, behavior_space.py or visualization.py from your terminal or prefered IDE. Ensure that all of the files associated with the respository remain in the same folder in order to ensure that the code runs properly. 

## Requirements and Dependencies

This model was developed using python 3.8.10 using the python agent-based modeling framework mesa. Be sure to  install the python library mesa prior to running this model. All other dependencies come with python 3.8 when it is installed or will be installed when you install mesa. 

# Using This Code

Running this code is a simple as downloading the folder and running either the run.py, behavior_space.py or visualization.py from your terminal or prefered IDE. Ensure that all of the files associated with the respository remain in the same folder in order to ensure that the code runs properly. 

## Running a single instance of the model

You can use the following scripts to run model depending on your interests and needs.

### Visualization.py

This is the easiest way to run a single instance of the model. It also provides a nice graphic visualization of how the model works as well. You will need to change presets if you want to run parameters discussed in the paper. 

### Run.py

This will run a single interation of the model. 

## Running parameter sweeps

To run the model on multiple different settings use behavior_space.py. This will allow you to define both fixed and variable parameters for the model to iterate through. The setttings currently provided in this code are those which were presented in the paper. This will allow you to reproduce the results. 

**Warning Time Consuming:** Parameter sweeps can be extremely time consuming and range from hours to weeks depending on the parameters 

**Warning Distributed Processing:** This script takes advantage of distributed processing to ensure to decrease run time. Make sure that the *nr_proccesses* on line 25 is set to match the computing capacity of your computer. A failure to do so can crash your computer.

**Warning RAM Issue:** Keep in mind that the output of a single iteration can be extremely large. This means that each run potetially, requires a large amount of RAM. If you used the parallell processing option make sure your resources are allocated appropriately. 

## Output

The raw data of the model is bundled into an individual SQLite database. Each iteration is given its own database. Use the compile.py script to aggregate all of the runs into a single database. SQL is preferred over excel or csv files as the output of the models can be very large in size. This is paricularly the case when all iterations are bundled together. This allows the user to query the database for the specific data they need so that they do not have to load the entire dataset directly into memory during analysis.   

# Bugs, Errors, and Feedback

Feel free to message me with any issues you have using this code. I will do my best to rectify any issues that may arise. 

## Known bugs

1. In some instances behavior_space.py will give an error stating that the folder where the output should be saved already exists. If this occurs simply delete the contents of the folder but do not delete the folder and run it again.  