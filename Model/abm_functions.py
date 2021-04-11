import sqlite3
import math
import random
import string


### Distribution Functions

def levy_number(l, u):

    return(l**(-u))

### Agent Functions

def ClosestAgent(pos, list):
    """

    :param pos: Current position of the Agent
    :param list: A list of agents with location whose distance from pos will be calculated
    :return: returns the index position of the object with the closest distance in the list.
    """
    pos_dists = []


    x1, y1 = pos


    for agent in list:
        x2, y2 = agent.pos

        distance = math.sqrt(((x1-x2)**2)+((y1-y2) **2))
        pos_dists.append([distance])

    return pos_dists.index(min(pos_dists))


### DataBase Functions

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


def create_DB(db_file):
    """creates a database where all of the ABM data will be stored"""
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        run_data_table = """ CREATE TABLE IF NOT EXISTS run_data (
                                run_id text PRIMARY KEY,
                                datetime text,
                                n_time_steps text,
                                num_agents integer,
                                num_sources integer,
                                num_trees integer,
                                treesdie integer,
                                tool_acq text,
                                search_rad integer,
                                tree_deaths integer); """

        source_data_table = """ CREATE TABLE IF NOT EXISTS sources (
                                run_id text,
                                id integer,
                                x integer,
                                y integer,
                                rm_quality); """

        tree_data_table = """ CREATE TABLE IF NOT EXISTS trees (
                                run_id text,
                                id integer,
                                x integer,
                                y integer,
                                ts_born text,
                                alive text,
                                ts_died text,
                                age text); """

        lithic_data_table = """ CREATE TABLE IF NOT EXISTS tools (
                                run_id text,
                                id text,
                                parent_id text,
                                source_id text,
                                x integer,
                                y integer,
                                Tool_size text,
                                original_size text,
                                active text,
                                rm_quality text,
                                ts_born text,
                                ts_died text,
                                n_uses text); """

        environment_table = """ CREATE TABLE IF NOT EXISTS environment (
                                run_id text,
                                time_step, integer,
                                trees_available text);
                                """

        c.execute(run_data_table)
        c.execute(source_data_table)
        c.execute(lithic_data_table)
        c.execute(tree_data_table)
        c.execute(environment_table)



    except sqlite3.Error as e:

        print(e)

    finally:

        pass
        #conn.close()

def connect_db(db_file):
    a = 0
    while a == 0:

        try:
            conn = sqlite3.connect(db_file)
            return conn
        except sqlite3.Error as e:
            print(e)

        return None

def add_run_data(conn, data):

    try:
        sql_run_dat = """ INSERT INTO run_data(run_id, datetime, n_time_steps, num_agents, num_sources, num_nutree, treessdie,
            tool_acq, search_rad, tree_deaths)

                              VALUES(?,?,?,?,?,?,?,?,?,?)
            """

        conn.execute(sql_run_dat, data)
        conn.commit()


    except sqlite3.Error as e:
        print(e)
        print("trying again")


def add_source_data(conn, data, commit_now=True):
    a = 0

    while a == 0:
        try:
            sql_run_dat = """ INSERT INTO sources(run_id, id, x, y, rm_quality)

                              VALUES(?,?,?,?,?)

            """
            conn.execute(sql_run_dat, data)
            if commit_now is True:
                conn.commit()
            else:
                pass
            a = 1

        except sqlite3.Error as e:
            print(e)
            print("trying again")


def add_tree_data(conn, data, commit_now=True):
    a = 0

    while a == 0:
        try:
            sql_run_dat = """ INSERT INTO trees(run_id, id, x, y, ts_born, alive, ts_died, age)

                              VALUES(?,?,?,?,?,?,?,?)

            """
            conn.execute(sql_run_dat, data)
            if commit_now is True:
                conn.commit()
            else:
                pass

            a = 1

        except sqlite3.Error as e:
            print(e)
            print("trying again")

def add_tool_data(conn, data, commit_now=True):
    a = 0

    while a == 0:
        try:
            sql_run_dat = """ INSERT INTO tools(
                                run_id,
                                id,
                                parent_id,
                                source_id,
                                x,
                                y,
                                tool_size,
                                original_size,
                                active,
                                rm_quality,
                                ts_born,
                                ts_died,
                                n_uses)

                              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)

            """
            conn.execute(sql_run_dat, data)
            if commit_now is True:
                conn.commit()
            else:
                pass
            a = 1

        except sqlite3.Error as e:
            print(e)
            print("trying again")

def add_env_data(conn, data, commit_now=True):
    a = 0

    while a == 0:
        try:
            sql_run_dat = """ INSERT INTO environment(
                                run_id,
                                trees_available,
                                trees_near_sources,
                                trees_near_pounding_tools)
                              
                              VALUES(?,?,?,?)
            """
            conn.execute(sql_run_dat, data)
            if commit_now is True:
                conn.commit()
            else:
                pass
            a = 1

        except sqlite3.Error as e:
            print(e)
            print("trying again")



def select_table(conn, table):

    cursor = conn.cursor()
    sql = """ SELECT * FROM %s """ % table
    cursor.execute(sql)
    records = cursor.fetchall()
    return(records)

