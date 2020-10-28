from Agents import *
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from numpy import random

class PrimToolModel(Model):
    def __init__(self, Na,Ns,Nn, height, width, treesdie):
        self.current_id = 0
        self.num_agents = Na
        self.num_sources = Ns
        self.num_nuttree = Nn
        self.treesdie = treesdie
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width=width,
                              height=height,
                              torus= False)
        self.timestep = 0
        self.running = True
        self.sql = "tool_tansport.db"

        #create agents

        for i in range(self.num_sources):
            source = StoneSource(self.next_id(), self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(source, (x, y))
            self.schedule.add(source)

        for i in range(self.num_agents):
            primate = PrimAgent(self.next_id(), self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(primate, (x,y))
            self.schedule.add(primate)

        for i in range(self.num_nuttree):
            tree = NutTree(self.next_id(), self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(tree, (x, y))
            self.schedule.add(tree)

    def Growtree(self):

        x = random.randint(1,1000)
        if x < 10:
            tree = NutTree(self.next_id(), self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(tree, (x, y))
            self.schedule.add(tree)

    def step(self):

        '''Advances the model by one step'''
        self.schedule.step()
        if self.treesdie is True:
            self.Growtree()
        else:
            pass
        self.timestep += 1
        #print(self.timestep)




