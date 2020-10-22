from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from numpy import random
import random
import string

#### Aux Functions

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

#### Agents

class PrimAgent(Agent):

    '''A stupid monkey that does pounding tool activities'''

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.Has_tool = -1
        self.search_radius = 5
        self.NutTreeLoc = -1
        self.StoneLoc = -1
        self.Tool_size = -1
        self.Tool_id = -1
        self.Source_id = -1



    def CheckForTree(self):

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        tree = [obj for obj in this_cell if isinstance(obj, NutTree)]
        if len(tree) > 0:
            print("I found a tree")
            self.NutTreeLoc = self.pos
        else:
            pass

    def CheckForStone(self):

        neighborhood = self.model.grid.get_neighborhood(self.pos, radius=self.search_radius, moore=True)
        neighborhood = self.model.grid.get_cell_list_contents(neighborhood)
        stones = [obj for obj in neighborhood if isinstance(obj, StoneSource)]
        pounding = [obj for obj in neighborhood if isinstance(obj, PoundingTool)]

        stones = stones + pounding

        if len(stones) > 0:
            print("I Found A Stone")
            stone = random.choice(stones)
            print(stone)

            if type(stone) is StoneSource:

                print("this is from the source")
                self.StoneLoc = stone.pos
                self.Source_id = stone.unique_id
                self.Tool_size = 1000
                self.Has_tool = 1
                self.model.grid.move_agent(self, self.StoneLoc)


            elif type(stone) is PoundingTool:

                print("this is a previously used stone")
                print("copying stone")
                self.StoneLoc = stone.pos
                self.Tool_id = stone.unique_id
                self.Source_id = stone.source_id
                self.Tool_size = stone.Tool_size
                self.model.grid.move_agent(self, self.StoneLoc)
                print("deleting stone")
                self.model.grid._remove_agent(stone.pos,stone)
                self.model.schedule.remove(stone)

        else:
            print("no stone")
            self.NutTreeLoc = -1

    def UseStone(self):

        possible_steps = self.model.grid.get_neighborhood(self.NutTreeLoc, moore=True)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        ### Need to add information about how these things break

        ### Dropstone
        size = self.Tool_size
        x,y = self.pos
        source_id = self.Source_id

        if self.Tool_size == -1:
            ident = self.model.next_id()

        else:
            ident = self.Tool_id

        tool = PoundingTool(ident, self, tool_size= size, active= True, s_id= source_id)
        self.model.grid.place_agent(tool, (x, y))
        self.model.schedule.add(tool)

        self.Tool_size = -1
        self.Tool_id = -1
        self.StoneLoc = -1
        self.NutTreeLoc = -1
        self.Has_tool = -1

    def move(self):

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)

        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)


    def step(self):

        self.CheckForTree()

        if self.NutTreeLoc != -1:
            self.CheckForStone()
        else:
            pass

        if self.Has_tool == 1:
            print("Using Stone")
            self.UseStone()
        else:
            pass

        self.move()

class StoneSource(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.ID = unique_id


class NutTree(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.ID = unique_id
        self.alive = True

    def doIdie(self):

        x = random.randint(1, 10000)
        if x <= 10:

            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            self.alive = False


    def step(self):

        self.doIdie()

class PoundingTool(Agent):
    def __init__(self, unique_id, model, tool_size, active, s_id):
        super().__init__(unique_id, model)
        self.Tool_size = tool_size
        self.active = active
        self.source_id = s_id



### Environemnt

class PrimToolModel(Model):
    def __init__(self, Na,Ns,Nn, height, width):
        self.current_id = 0
        self.num_agents = Na
        self.num_sources = Ns
        self.num_nuttree = Nn
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width=width,
                              height=height,
                              torus= False)
        self.timestep = 0
        self.running = True


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
        self.Growtree()
        self.timestep =+ 1
        print(self.timestep)




