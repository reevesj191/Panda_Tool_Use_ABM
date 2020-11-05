import sqlite3
import math
import random
import string

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str




def ClosestAgent(pos, list):

    pos_dists = []


    x1, y1 = pos

    for agent in list:
        x2, y2 = agent.pos

        distance = math.sqrt(((x1-x2)**2)+((y1-y2) **2))
        pos_dists.append([distance])

    return pos_dists.index(min(pos_dists))










    pass


def create_DB(db_file):
    """creates a database where all of the ABM data will be stored"""
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        run_data_table = """ CREATE TABLE IF NOT EXISTS run_data (
                                run_id text PRIMARY KEY,
                                movement_type text,
                                nrounds integer,
                                nsources integer,
                                nattractors integer,
                                ncores integer,
                                core_drop_threshold text,
                                core_replacement text,
                                flake_probability text,
                                global_cortex_ratio
                                ); """


        flake_table = """ CREATE TABLE IF NOT EXISTS flakes (
                                run_id text,
                                movement_type text,
                                x integer,
                                y integer,
                                source_loc text,
                                core_id text,
                                cortex text,
                                dp_volume text,
                                flakes_made text,
                                timestep text
                                ); """

        cores_table = """ CREATE TABLE IF NOT EXISTS cores (
                                run_id text,
                                movement_type text,
                                x integer,
                                y integer,
                                source_loc text,
                                core_id text,
                                initial_volume text,
                                initial_cortex text,
                                volume text,
                                cortex text,
                                flakes_made text,
                                replaced text,
                                timestep text
                                );
                                """

        attractors_table = """ CREATE TABLE IF NOT EXISTS attractors (
                                run_id text,
                                movement_type text,
                                x integer,
                                y integer
                                );
                                """

        sources_table = """ CREATE TABLE IF NOT EXISTS sources (
                                run_id text text,
                                movement_type text,
                                x integer,
                                y integer
                                );
                                """

        c.execute(run_data_table)
        c.execute(flake_table)
        c.execute(cores_table)
        c.execute(attractors_table)
        c.execute(sources_table)

    except sqlite3.Error as e:

        print(e)

    finally:

        conn.close()

conn = create_DB("WABI.db")