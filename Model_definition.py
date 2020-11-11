from datetime import datetime
from Agents import *
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from numpy import random
from abm_functions import create_DB, add_run_data, add_source_data, add_tree_data, add_tool_data, connect_db



class PrimToolModel(Model):
    def __init__(self, Na,Ns,Nn, height, width, treesdie, max_ts, search_rad = 5, tool_acq="nearest" , db_name="pyMate_Panda_ABM.db"):
        self.current_id = 0
        self.run_id = get_random_alphanumeric_string(6)
        self.datetime = datetime.now()
        self.num_agents = Na
        self.num_sources = Ns
        self.num_nuttree = Nn
        self.treesdie = treesdie
        self.tool_acquistion = tool_acq
        self.search_radius = search_rad
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width=width,
                              height=height,
                              torus= False)
        self.timestep = 0
        self.max_ts = max_ts
        self.running = True
        self.sql = db_name

        create_DB(self.sql)

        print("update Run Data table")
        conn = connect_db(self.sql)

        rundat = (self.run_id,
                  self.datetime,
                  self.num_agents,
                  self.num_sources,
                  self.num_nuttree,
                  self.treesdie,
                  self.tool_acquistion,
                  self.search_radius)

        add_run_data(conn, rundat)

        #create agents
        print("Generating Agents")
        for i in range(self.num_sources):
            source = StoneSource(self.next_id(), self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(source, (x, y))
            self.schedule.add(source)
            row = [self.run_id, source.unique_id, x, y]
            add_source_data(conn, row)

        for i in range(self.num_agents):
            primate = PrimAgent(self.next_id(), self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(primate, (x, y))
            self.schedule.add(primate)

        for i in range(self.num_nuttree):
            tree = NutTree(self.next_id(), self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(tree, (x, y))
            self.schedule.add(tree)


    def Growtree(self):

        tree_list = []
        for agent in self.schedule.agents:
            if type(agent) is NutTree:
                tree_list.append(agent)
        tree = self.random.choice(tree_list)
        new_loc = self.grid.get_neighborhood(tree.pos, moore=True, include_center=False, radius= 15)
        new_loc = self.random.choice(new_loc)
        new_tree = NutTree(self.next_id(), self, ts_born= self.timestep)
        self.grid.place_agent(new_tree, new_loc)
        self.schedule.add(new_tree)



    def step(self):

        '''Advances the model by one step'''
        self.schedule.step()

        if self.treesdie is True:
            x = random.randint(1,10000)
            if x <= 1:
                self.Growtree()
            else:
                pass
        else:
            pass

        if self.timestep == self.max_ts:
            print("Run Finished updating db with tool Data")
            conn = connect_db(self.sql)
            for agent in self.schedule.agents:

                if type(agent) is PoundingTool:
                    row = [self.run_id,
                           agent.tool_id,
                           agent.parent_id,
                           agent.source_id,
                           agent.pos[0],
                           agent.pos[1],
                           agent.Tool_size,
                           agent.active]

                    add_tool_data(conn=conn, data=row)
            self.running = False

        else:
            pass

        self.timestep += 1







