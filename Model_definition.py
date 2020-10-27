from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from numpy import random




class PrimAgent(Agent):

    '''A stupid monkey that does pounding tool activities'''

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.Has_tool = -1
        self.search_radius = 3
        self.NutTreeLoc = -1
        self.StoneLoc = -1
        self.Tool_size = -1
        self.Tool_id = -1
        self.Source_id = -1
        self.active = -1

    def CheckForTree(self):

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        tree = [obj for obj in this_cell if isinstance(obj, NutTree)]
        if len(tree) > 0:
            #print("I found a tree")
            self.NutTreeLoc = self.pos
        else:
            pass

    def BreakStone(self, stone):

        half = stone.Tool_size/2

        fragment = random.randint(50, int(half))

        stone.Tool_size = stone.Tool_size - fragment

        if stone.Tool_size < 200:

            stone.active = False

        else:
            pass

        if fragment >= 200:
            active = True
        else:
            active = False

        new_tool = PoundingTool(self.model.next_id(),
                                self,
                                fragment,
                                active,
                                stone.source_id)

        self.model.grid.place_agent(new_tool, self.pos)
        self.model.schedule.add(new_tool)

    def CheckForStone(self):

        neighborhood = self.model.grid.get_neighborhood(self.pos, radius=self.search_radius, moore=True)
        neighborhood = self.model.grid.get_cell_list_contents(neighborhood)
        stones = [obj for obj in neighborhood if isinstance(obj, StoneSource)]
        pounding = [obj for obj in neighborhood if isinstance(obj, PoundingTool)]
        pounding_filtered = []
        ### Remove objects with size less than 200

        for i in range(len(pounding)):
            subset = pounding[i]
            if subset.active is True:
                pounding_filtered.append(subset)
            else:
                pass

        stones = stones + pounding_filtered


        if len(stones) > 0:
            #print("I Found A Stone")
            stone = random.choice(stones)
            # reset stones
            #print(stone)

            if type(stone) is StoneSource:

                #print("this is from the source")
                self.StoneLoc = stone.pos
                self.Source_id = stone.unique_id
                self.Tool_size = 1000
                self.Has_tool = 1
                self.model.grid.move_agent(self, self.StoneLoc)

                ## Using the stone

                possible_steps = self.model.grid.get_neighborhood(self.NutTreeLoc, moore=True)
                new_position = self.random.choice(possible_steps)
                self.model.grid.move_agent(self, new_position)

                ### Dropstone
                size = self.Tool_size
                x, y = self.pos
                source_id = self.Source_id

                tool = PoundingTool(self.model.next_id(), self, tool_size=size, active=True, s_id=source_id)
                self.model.grid.place_agent(tool, (x, y))
                self.model.schedule.add(tool)

            elif type(stone) is PoundingTool:

                #print("this is a previously used stone")

                possible_steps = self.model.grid.get_neighborhood(self.NutTreeLoc, moore=True)
                new_position = self.random.choice(possible_steps)
                self.model.grid.move_agent(self, new_position)
                #print("moving stone")
                self.model.grid.move_agent(stone, new_position)
                Break_prob = random.randint(1,100)

                if Break_prob <= 25:

                    identifier = self.model.next_id()
                    self.BreakStone(stone)

                else:
                    pass


        else:
            #print("no stone")
            pass

        ### Reset everything
        self.NutTreeLoc = -1
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

        # if self.Has_tool == 1:
        #     print("Using Stone")
        #     self.UseStone()
        # else:
        #     pass

        self.move()

class StoneSource(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.ID = unique_id
        self.active = -1


class NutTree(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.ID = unique_id
        self.alive = True
        self.active = -1

    def doIdie(self):

        x = random.randint(1, 10000)
        if x <= 10:

            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            self.alive = False


    def step(self):

        if self.model.treesdie is True:
            self.doIdie()
        else:
            pass



class PoundingTool(Agent):
    def __init__(self, unique_id, model, tool_size, active, s_id):
        super().__init__(unique_id, model)
        self.Tool_size = tool_size
        self.active = active
        self.source_id = s_id


### Environemnt

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




