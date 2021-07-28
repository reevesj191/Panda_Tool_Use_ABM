This is repository where the code for the agent-based model presented in "Modeling a primate technological niche" is kept and actively maintained.

DISCLAIMER: THIS WORK IS CURRENTLY UNDER REVIEW. PLEASE DO NOT CITE OR PUBLISH THE MODEL OR INFORMATION IN THE REPOSITORY WITHOUT THE APPROVED WRITTEN CONSENT OF THE AUTHORS

# Using This Code

Running this code is a simple as downloading the folder and running either the behavior_space.py or visualization.py from your terminal or prefered IDE. Ensure that all of the files associated with the respository remain in the same folder in order to ensure that the code runs properly. 

## Requirements and Dependencies

Running the model requries a fair amount of RAM. This is particularly the case when using the parallel processing option in behavior space. There is a memory_safe option that can be defined which will cut down on the amount of RAM any single iteration of the model will use. Even with this option set to true it is still RAM intensive. 

Make sure the following python libraries are installed.

1. Mesa
2. Numpy
3. Pandas 

## Running a single Model

To be written. I will provide this code soon.

In the meantime, a nice example for how to write the code to run a single iteration of the model can be found the the MESA website. 

## Running parameter sweeps

To run the model on multiple different settings use behavior_space.py. This will allow you to define both fixed and variable parameters for the model to iterate through. The setttings currently provided in this code are those which were presented in the paper. This will allow you to reproduce the results. 

### Parallel Processing

There is an option for taking advantage of the parallel prcoessing. However, the code necessary for this to work is operating system dependent. You will need to comment out the blocks of code that do not match your operating system. 

## Output

### Analyzing the Output




 
