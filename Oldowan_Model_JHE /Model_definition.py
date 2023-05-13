from datetime import datetime
from Agents import *
from mesa import Model
import random as rand
import os
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from numpy import random
from abm_functions import create_DB, add_run_data, add_source_data, add_tree_data, add_tool_data, add_env_data, connect_db

def compute_trees_available(model):

    trees = [obj.available for obj in model.schedule.agents if isinstance(obj,NutTree)]
    return sum(trees)

class PrimToolModel(Model):
    def __init__(self, Na, Ns, Nn, height, width, treesdie, max_ts, max_uses, 
                 scenario = "Panda",
                 search_rad=2, 
                 tool_acq="nearest",
                 db_name="Final_JHE_Dataset",
                  mem_safe=True):

        self.exp_name = db_name
        self.runs_path = "%s_iterations" % self.exp_name

        if not os.path.exists(self.runs_path):
            os.mkdir(self.runs_path)

        self.current_id = 0
        self.run_id = get_random_alphanumeric_string(6)
        self.datetime = datetime.now()
        self.condition = scenario
        self.num_agents = Na
        self.num_sources = Ns
        self.num_nuttree = Nn
        self.treesdie = treesdie
        self.max_ts = max_ts
        self.max_uses_per_move = max_uses # JHE Revision.
        self.tool_acquistion = tool_acq 
        self.search_radius = search_rad
        self.sql = os.path.join(self.runs_path, self.run_id)
        self.mem_safe = mem_safe

        create_DB(self.sql)

        ### Space, Scheduling
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width=width,
                              height=height,
                              torus= False)
        ### Recorded Variables
        self.timestep = 0
        self.tree_growth_deaths = 0
        self.running = True

        for i in range(self.num_agents):
            primate = PrimAgent(self.next_id(), self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(primate, (x, y))
            self.schedule.add(primate)

        conn = connect_db(self.sql)
        for i in range(self.num_sources):
            q = rand.choice([0,25,50,75])
            source = StoneSource(self.next_id(), self, qual=q)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(source, (x, y))
            self.schedule.add(source)
            row = [self.run_id, source.unique_id, x, y, source.rm_quality] # Line to be added the SQL-DB
            add_source_data(conn, row) # Adds source data to SQL DB
        conn.commit()
        conn.close

        for i in range(self.num_nuttree):
            tree = NutTree(self.next_id(), self)
            if self.treesdie is True:
                tree.age = random.randint(1,10000)
            else:
                tree.age = 0
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(tree, (x, y))
            self.schedule.add(tree)

        self.datacollector = DataCollector(
            model_reporters={"Trees Available": compute_trees_available}

        )


    def step(self):
        self.datacollector.collect(self)
        '''Advances the model by one step'''
        self.schedule.step()

        if self.timestep == self.max_ts:
            print("Run Finished updating db with tool Data")

            conn = connect_db(self.sql)

            # Writing Rundata
            print("update Run Data table")
            rundat = (self.run_id,
                      self.datetime,
                      self.max_ts,
                      self.num_agents,
                      self.num_sources,
                      self.num_nuttree,
                      self.condition,
                      self.treesdie,
                      self.tool_acquistion,
                      self.search_radius,
                      self.tree_growth_deaths,
                      self.max_uses_per_move)
            add_run_data(conn, rundat)
            conn.commit()

            print("update tools data table")
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
                       agent.n_uses,
                       agent.sequence]
                add_tool_data(conn=conn, data=row, commit_now=False)
            conn.commit()

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
                add_tree_data(conn, row, commit_now=False)
            conn.commit()

            environment_data = self.datacollector.get_model_vars_dataframe()

            #conn = connect_db(self.sql)
            for index, row in environment_data.iterrows():
                run_id = self.run_id
                a = int(row['Trees Available'])
                sql_row = [run_id, a]
                add_env_data(conn, sql_row, commit_now=False)

            conn.commit()
            conn.close()

            self.running = False
        else:
            self.timestep += 1









