from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid


class PrimAgent(Agent):

    '''A stupid monkey that does pounding tool activities'''

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.Has_tool = 0

    def step(self):

        #print("Hi, I am agent " + str(self.unique_id) +".")



class PrimToolModel(Model):
    def __init__(self, N, height, width):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width=width,
                              height=height,
                              torus= False)

        #create agents
        for i in range(self.num_agents):
            a = PrimAgent(i, self)
            self.schedule.add(a)


    def step(self):

        '''Advances the model by one step'''
        self.schedule.step()




