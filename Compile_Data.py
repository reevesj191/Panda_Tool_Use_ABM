import os
from abm_functions import create_DB, select_table, add_run_data, add_source_data, add_tree_data, add_tool_data, connect_db


pathway = "Experiment_1_25k_50k_iterations"
db_name = "master"
db_path = os.path.join(pathway,db_name)

## Create Master Data Base
if not os.path.exists(db_path):
    create_DB(db_path)

runs = os.listdir(pathway)
runs.remove(db_name)

master_conn = connect_db(db_path)

for run in runs:
    run_path = os.path.join(pathway, run)
    run_conn = connect_db(run_path)

    ### compile run_data
    run_data = select_table(run_conn, "run_data")
    add_run_data(master_conn, run_data[0])
    ### Add Tree_data
    trees = select_table(run_conn, "trees")
    for tree in trees:
        add_tree_data(master_conn, tree, commit_now=False)
    ### Add Source_data
    sources = select_table(run_conn, "sources")
    for source in sources:
        add_source_data(master_conn, source, commit_now= False)
    ### Add tool_data

    tools = select_table(run_conn, "tools")
    for tool in tools:
        add_tool_data(master_conn, tool, commit_now=False)

    master_conn.commit()
