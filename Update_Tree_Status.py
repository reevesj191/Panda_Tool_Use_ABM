import pandas as pd
from scipy.spatial import KDTree

trees = pd.read_csv("Data/EXP_PNAS_trees.csv")
tools_sum = pd.read_csv("Data/EXP_PNAS_tool_sum_ns_100_nt_2000.csv", low_memory=False)


for i in range(len(tools_sum)):
    print(i)
    site = tools_sum.iloc[i]
    r_id = site["run_id"]
    run_trees = trees.loc[trees["run_id"] < r_id]
    run_trees_xy = run_trees[["x", "y"]]
    run_trees_xy = run_trees_xy[["x","y"]].to_numpy()

    tree = KDTree(run_trees_xy)
    d, idx = tree([site["x"], site["y"]], r=1.5)

    print(idx)


