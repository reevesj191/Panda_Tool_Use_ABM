
from datetime import datetime
from Agents import *
from mesa import Model
import random as rand
import os
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from numpy import random
from abm_functions import create_DB, add_run_data, add_source_data, add_tree_data, add_tool_data, connect_db




class PrimToolModel(Model):
    def __init__(self, Na,Ns,Nn, height, width, treesdie, max_ts, search_rad=2, tool_acq="nearest" , db_name="pyMate_Panda_ABM.db"):
        self.current_id = 0
        self.run_id = get_random_alphanumeric_string(6)
        self.datetime = datetime.now()
        self.num_agents = Na
        self.num_sources = Ns
        self.num_nuttree = Nn
        self.treesdie = treesdie
        self.max_ts = max_ts
        self.tool_acquistion = tool_acq
        self.search_radius = search_rad
        self.exp_name = db_name
        self.runs_path = "%s_iterations" % self.exp_name
        self.sql = os.path.join(self.runs_path, self.run_id)

        ### Space, Scheduling
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width=width,
                              height=height,
                              torus= False)
        ### Recorded Variables
        self.timestep = 0
        self.tree_growth_deaths = 0
        self.running = True

        if not os.path.exists(self.runs_path):
            os.mkdir(self.runs_path)

        create_DB(self.sql)

        #create agents

        conn = connect_db(self.sql)
        # Adding Sources
        for i in range(self.num_sources):
            q = rand.choice([0,25,50,75])
            source = StoneSource(self.next_id(), self, qual=q)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(source, (x, y))
            self.schedule.add(source)
            row = [self.run_id, source.unique_id, x, y, source.rm_quality] # Line to be added the SQL-DB
            add_source_data(conn, row) # Adds source data to SQL DB

        for i in range(self.num_agents):
            primate = PrimAgent(self.next_id(), self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(primate, (x, y))
            self.schedule.add(primate)

        for i in range(self.num_nuttree):
            tree = NutTree(self.next_id(), self)
            tree.age = random.randint(1,10000)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(tree, (x, y))
            self.schedule.add(tree)

    def step(self):

        '''Advances the model by one step'''
        self.schedule.step()

        if self.timestep == self.max_ts:
            print("Run Finished updating db with tool Data")
            conn = connect_db(self.sql)

            # Writing Rundata

            print("update Run Data table")
            conn = connect_db(self.sql)

            rundat = (self.run_id,
                      self.datetime,
                      self.max_ts,
                      self.num_agents,
                      self.num_sources,
                      self.num_nuttree,
                      self.treesdie,
                      self.tool_acquistion,
                      self.search_radius,
                      self.tree_growth_deaths)

            add_run_data(conn, rundat)

            stone_list = [obj for obj in self.schedule.agents if isinstance(obj, PoundingTool)]

            for agent in stone_list:
                row = [self.run_id,
                       agent.tool_id,
                       agent.parent_id,
                       agent.source_id,
                       agent.pos[0],
                       agent.pos[1],
                       agent.Tool_size,
                       agent.original_size,
                       agent.active,
                       agent.rm_quality,
                       agent.ts_born,
                       agent.ts_died,
                       agent.n_uses]
                add_tool_data(conn=conn, data=row, commit_now=False)

            ### Adding Living Trees

            tree_list = [obj for obj in self.schedule.agents if isinstance(obj, NutTree)]
            for agent in tree_list:
                row = [agent.model.run_id,
                       agent.unique_id,
                       agent.pos[0], agent.pos[1],
                       agent.ts_born,
                       agent.alive,
                       agent.ts_died,
                       agent.age]
                conn = connect_db(self.sql)
                add_tree_data(conn, row, commit_now=False)

            conn.commit()
            self.running = False

        else:
            pass

        self.timestep += 1







