from mesa import Agent
from numpy import random
from abm_functions import  ClosestAgent, get_random_alphanumeric_string, add_tree_data, connect_db

class PrimAgent(Agent):

    '''Analogous to a chimpanzee in the real world.'''

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.Has_tool = -1 #For debuging purposes
        self.search_radius = self.model.search_radius # user defined, it determines the area that the agent will search for a tool
        self.NutTreeLoc = -1 #records the location of the chosen nut tree to crack nuts at
        self.StoneLoc = -1   #the location of the closest stone tool the agent
        self.Tool_size = -1  #The size of the tool acquired
        self.Tool_id = -1    #The id of the tool acquired
        self.Source_id = -1  #The id of the source of the tool
        self.rm_qual = -1    #The quality of the tool acquired
        self.active = -1     #Whether or not the tool is active.

    def CheckForTree(self):

        ''''PrimAgent checks to see if there is a tree at its location or in one of its neighboring cells. If yes,
        then the attribute NutTreeLoc is updated with the location of the tree. If there is more than one tree present
         then the agent will randomly choose a tree within the neighborhood'''

        neighborhood = self.model.grid.get_neighborhood(self.pos,
                                                        radius=1,
                                                        moore=True,
                                                        include_center=True) ## Returns a list of grid cells neighboring the agent
        print(neighborhood)
        neighborhood = self.model.grid.get_cell_list_contents(neighborhood) ## Returns a list of objects that are in the cells in the neighborhood
        trees = [obj for obj in neighborhood if isinstance(obj, NutTree)] ## Subsets the list object to those only of the nutree class

        if len(trees) > 0: # Double checks to make sure the list of trees is not empty
            tree = random.choice(trees) # this chooses a tree. If there is more than one in the neighborhood, it randomly chooses.
            self.NutTreeLoc = tree.pos # this updates the agents nutTree location with the position of the selected tree.
                                       # This will be the location where agent will bring a stone if there is any.

        else:
            pass

    def CheckForStone(self):
        """
        Determines whether a stone is in the defined search radius.
        """
        neighborhood = self.model.grid.get_neighborhood(self.pos, radius=self.search_radius, moore=True)  # Defines the
        # neighborhood around the agent
        neighborhood = self.model.grid.get_cell_list_contents(
            neighborhood)  # Returns a list of the objects in the neighborhood

        # Subsets out all of the stone sources and pounding tools. This way tree agents are not accidentally selected
        # as stones.
        sources = [obj for obj in neighborhood if isinstance(obj, StoneSource)]  # Subsets out stones
        pounding = [obj for obj in neighborhood if isinstance(obj, PoundingTool)]  # Subsets out Pounding tools

        # Remove objects that are not active.
        pounding_filtered = []
        for i in range(len(pounding)):
            subset = pounding[i]
            if subset.active is True:
                pounding_filtered.append(subset)
            else:
                pass

        # Combines pounding tools and sources together
        stone_list = sources + pounding_filtered

        return (stone_list)

    def BreakStone(self, stone):

        """
        This will simulate the effect of the stone breaking during a nut cracking event.
        :return:
        """

        fragment = stone.Tool_size #Sets the maximum size of the peice that breaks off.

        # A random expontial distribution is drawn from to determine the size of the piece that breaks off
        # This ensures that fragmentation will prefer small over large pieces. A while loop is used to ensure that the
        # size of the fragment is not larger than half the size of the tool. This means that  fragmentation can only split
        # the tool in half at best

        while fragment >= stone.Tool_size/2:
            fragment = random.exponential(200, 1)[0] # This is eyeballed at best.

        stone.Tool_size = stone.Tool_size - fragment ## The size of the fragment is subtracted from the size to the tool.
        parent_id = stone.tool_id ## Saves the tool id as the paraent id for the fragment

        ## if the tool size remains larger than 2000 then it remains active as a useable tool.
        if stone.Tool_size < 2000:
            ## if it is less than 2000 it is considered exhausted and becomes no longer useable
            stone.active = False ## Switching this from True to False stops the tool from being used again.
            stone.ts_died = self.model.timestep ## Records the time step at which the tool became in active.
        else:
            pass

        ## This true false statement determines whether the fragment will also be active as a tool or not
        if fragment >= 2000:
            active = True
        else:
            active = False

        # Creates the fragment as an agent of the poundingtool class
        new_tool = PoundingTool(self.model.next_id(),
                                self.model,
                                fragment,
                                active,
                                stone.source_id,
                                parent_id=parent_id,
                                q=stone.rm_quality,
                                born=self.model.timestep)

        # If the new cannot be used as a pounding tool, the time step that it is discarded is recorded. This ensures
        # that there is a way track when the fragment was created.

        if new_tool.active is False:
            new_tool.ts_died = self.model.timestep
        else:
            pass

        # Adds the new fragment to the model space.
        self.model.grid.place_agent(new_tool, self.pos)
        self.model.schedule.add(new_tool)

    def SelectStone(self, stone_list, selection_method):
        '''
        :param stone_list: a list of locations of stones or sources generated by the CheckForStone method
        :param selection_method: a string determining the way in which PrimAgents selects a stone. Two options random or
        nearest
        :return:
        '''

        # If statement to determine the function used select the stone. Can be random or nearest.
        if selection_method == 'random':

            stone = random.choice(stone_list) # It randomly chooses from the list

        elif selection_method == 'nearest':

            # The closest agent function is extremely clunky. There must be a more pythonic way to do this.

            nearest = ClosestAgent(self.pos,list=stone_list) # It determine the index position of the object that is
                                                             # located closest to the PrimAgents

            stone = stone_list[nearest] # Uses indexing to select the closest stone/source
            print(stone)
        else:
            pass

        return(stone)

    def UseStone(self, stone):
        '''
        This function executes the transport and use of the pounding tool.

        :param stone: An object of the pounding tool or source class
        :return:
        '''

        # Logical statements determine how to handle a source or a pounding tool.
        if type(stone) is StoneSource:
            # If the selected object is a Source then a new pounding tool must be created.
            #print("this is from the source") # For debugging
            self.StoneLoc = stone.pos
            self.Source_id = stone.unique_id
            self.rm_qual = stone.rm_quality

            # Determining the size of the tool
            # A while loop is used to ensure that generated tools have a size of greater than 2000 grams.

            while self.Tool_size < 2000:
                self.Tool_size = random.normal(7400,3900,1)[0] # Size of the tool is randomly drawn from a normal distribution
                                                               # with the mean and sd of tools found in the Tai forest

            self.Has_tool = 1 # For Debugging purposes.

            #This part is really clunky it can probably be stream lined since everything is happening within one timestep
            # Agent goes to the location of the selected source

            self.model.grid.move_agent(self, self.StoneLoc)
            # Then randomly the location of the encountered tree or one of its eight neighbors.
            possible_steps = self.model.grid.get_neighborhood(self.NutTreeLoc, moore=True, include_center=True)
            new_position = self.random.choice(possible_steps)
            # Moves to the new location around the tree.
            self.model.grid.move_agent(self, new_position)

            # A new pounding tool is created at the chosen location around the encountered tree.
            size = self.Tool_size
            x, y = self.pos
            source_id = self.Source_id
            ts = self.model.timestep
            tool = PoundingTool(self.model.next_id(), self.model, tool_size=size, active=True, s_id=source_id, q=self.rm_qual,born=ts)
            tool.n_uses += 1 # make sure n uses in the pounding tool class begins @ 0 and not 1
            self.model.grid.place_agent(tool, (x, y))
            self.model.schedule.add(tool)

        # Handling transport and use when a the object is a prexisting pounding tool.

        elif type(stone) is PoundingTool:

            #print("this is a previously used stone") # Debug only.

            possible_steps = self.model.grid.get_neighborhood(self.NutTreeLoc,
                                                              moore=True,
                                                              include_center=True) # Same as above.

            new_position = self.random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)

            #print("moving stone") # debug only
            stone.n_uses += 1 # make sure n uses in the pounding tool class begins @ 0 and not 1
            self.model.grid.move_agent(stone, new_position) ## Moves the selected stone to the new location as above.

            # determines whether a stone will break or not.

            Break_prob = random.randint(1,100) # randomly draw an integer from 1 to 0

            # All stones have a 25% chance to break plus the qualifier they get from there raw material quality. If the
            # the break prob is less than or equal to 25 + the stone's rm quality then the stone breaks.

            if Break_prob <= 25 + stone.rm_quality:

                self.BreakStone(stone)

            else:

                #print("Stone does not break!") # Debug only
                pass
        else:
            #print("no stone")
            pass

        ### Reset everything
        self.NutTreeLoc = -1 #records the location of the chosen nut tree to crack nuts at
        self.StoneLoc = -1   #the location of the closest stone tool the agent
        self.Tool_size = -1  #The size of the tool acquired
        self.Tool_id = -1    #The id of the tool acquired
        self.Source_id = -1  #The id of the source of the tool
        self.rm_qual = -1    #The quality of the tool acquired
        self.active = -1     #Whether or not the tool is active.

    def move(self):
        ### Move in brownian motion moore
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)


    def step(self):

        # Agent searches for trees
        self.CheckForTree()

        # If the agent has found a tree then the NutTreeLoc attribute will be updated with a set of coordinates and is
        # no longer -1.
        if self.NutTreeLoc != -1:
            #print("I found a tree") # debug only

            # if this  is the case the agent will execute the check of stone function to see if a stone/source is within
            # the search radius of the agent.

            stones = self.CheckForStone()

            # if there is then the length of the list returned by the CheckForStone function will be greater than 0
            if len(stones) > 0:
                #print("There are stones")
                # If this is the case then the agent will execute the SelectStone function.
                stone = self.SelectStone(stones, selection_method=self.model.tool_acquistion)

                # The selected stone is then used by executing the UseStone function.
                self.UseStone(stone)

            else:

                # print("No stones reseting tree loc") # Debugging only

                # If there are no stones in the list then then NutTreeLoc is set back to negative -1 to stop the agent
                # from continously searching for stone and transporting a stone a distance greater than its search
                # radius
                self.NutTreeLoc = -1
        else:

            #print("No Tree Encountered") # Debug only

            pass

        self.move()

class StoneSource(Agent):

    def __init__(self, unique_id, model, qual):
        super().__init__(unique_id, model)
        self.ID = unique_id # Id allows it to be paired with the stones that acquired from this source.
        self.active = -1 # For debugging
        self.rm_quality = qual # Attribute that determines the quality of the stones that come from a source. I.e. how
                               # likely a tool is break during use. Inherited from Model_Definition.py(lines 51 and 52)


class NutTree(Agent):

    def __init__(self, unique_id, model, ts_born = 0, ts_died = -1):
        super().__init__(unique_id, model)
        self.ID = unique_id # Id
        self.ts_born = ts_born # The time step that the tree was grown.
        self.ts_died = ts_died # The time step at which a tree is removed from the model.
        self.age = 0 #How the tree is
        self.alive = True # For debugging
        self.active = -1 # For debugging

    def agedieGrow(self):

        """
        This function ages the tree agent. It is also responsible the tree 'dieing' and growing a new tree in a new
        location. A tree can live for 10000 time steps after which a tree dies regrows somewhere else.
        :return: NA
        """

        self.age += 1 # Ages the tree

        # Tree death.
        # A Tree dies when it reaches an age of 10,000 time steps.
        if self.age == 10000:
            #print('a tree dies') # debugging only
            ### Killing Tree

            self.ts_died = self.model.timestep #The time-step at which the tree dies is recorded.
            self.alive = False # The alive attribute is then set to false. Mostly for debugging.

            # Preparing the row of information to be added to the SQL database. Ensure that the order of the variables
            # is the same as the appear in the SQL DB.

            row = [self.model.run_id,
                   self.unique_id,
                   self.pos[0],
                   self.pos[1],
                   self.ts_born,
                   self.alive,
                   self.ts_died,
                   self.age]

            conn = connect_db(self.model.sql) # Open connection with SQL database
            add_tree_data(conn, row) # Add data to the trees table.

            # Growing Tree
            # Once the tree is dead a new location is within a 10 grid-cell radius of its location is chosen as the
            # location to grow a new tree
            new_loc = self.model.grid.get_neighborhood(self.pos,
                                                       moore=True,
                                                       include_center=False,
                                                       radius=10) # Determines the cells within a 10 grid-cell radius

            new_loc = self.random.choice(new_loc) # Randomly chooses a grid cell from this neighborhood.
            new_tree = NutTree(self.model.next_id(), self.model, ts_born=self.model.timestep) #Generates a new NutTree
            self.model.grid.place_agent(new_tree, new_loc) # places the agent in space
            self.model.schedule.add(new_tree) # addeds the agent to the model.

            ## Remove dead Tree from Model
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            self.model.tree_growth_deaths += 1 # addes a tally to the tree growth/deaths attribute. See model definition

        else:

            #print(self.unique_id) # debug only
            #print("remains alive") # debug only

            pass




    def step(self):
        # Trees only age die and grow if the global variable treesdie is True.
        if self.model.__getattribute__("treesdie") is True:
            self.agedieGrow()

        else:
            pass

class PoundingTool(Agent):
    def __init__(self, unique_id, model, tool_size, active, s_id, parent_id="OG", q=-1, born=-1):
        super().__init__(unique_id, model)
        self.parent_id = parent_id
        self.tool_id = get_random_alphanumeric_string(8)
        self.Tool_size = tool_size
        self.original_size = tool_size
        self.active = active
        self.source_id = s_id
        self.rm_quality = q
        self.ts_born = born
        self.ts_died = -1
        self.n_uses = 0

