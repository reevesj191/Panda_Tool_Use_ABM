import os
from abm_functions import create_DB, select_table, add_run_data, add_source_data,\
    add_tree_data, add_tool_data, add_env_data, connect_db

pathway = "C:/Users/jonathan_reeves/Documents/GitHub/Panda_Tool_Use_ABM/Model/Experiment_14_pounding_tool_priority_iterations"
db_name = "0000_Run_Compiled"
db_path = os.path.join(pathway,db_name)


## Create Master Data Base
if not os.path.exists(db_path):
    create_DB(db_path)

runs = os.listdir(pathway)
runs.remove(db_name)
runs = [run for run in runs if not run.endswith("-journal")]
#runs.remove('.DS_Store')


master_conn = connect_db(db_path)
c = master_conn.cursor()
sql_exp = """ALTER TABLE run_data ADD n_trees_available_start integer """
c.execute(sql_exp)
sql_exp = """ALTER TABLE run_data ADD n_trees_available_end integer """
c.execute(sql_exp)


for run in runs:
    print(run)
    run_path = os.path.join(pathway, run)
    run_conn = connect_db(run_path)

    ### compile run_data

    run_data = select_table(run_conn, "run_data")

    # Add two columns
    if len(run_data) > 0:

        ## Add Tree_data
        trees = select_table(run_conn, "trees")
        for tree in trees:
            add_tree_data(master_conn, tree, commit_now=False)
        ### Add Source_data
        sources = select_table(run_conn, "sources")
        for source in sources:
            add_source_data(master_conn, source, commit_now=False)
        ### Add tool_data

        tools = select_table(run_conn, "tools")
        for tool in tools:
            add_tool_data(master_conn, tool, commit_now=False)

        ### Environment Data
        env = select_table(run_conn, "environment")
        for row in env:
            add_env_data(master_conn, row, commit_now=False)


        start = env[1]
        start = start[1]

        end = env[len(env)-1]
        end = end[1]

        add_run_data(master_conn, run_data[0])

        sql_exp = """ 
        UPDATE run_data 
        SET n_trees_available_start = {start}
        WHERE run_id = '{run_id}'
        """.format(start=start, run_id=run)

        c.execute(sql_exp)

        sql_exp = """ 
        UPDATE run_data 
        SET n_trees_available_end = {start}
        WHERE run_id = '{run_id}'
        """.format(start=end, run_id=run)

        c.execute(sql_exp)


    else:
        print("no data to add")

    master_conn.commit()
