library(DBI)
library(data.table)

con <- DBI::dbConnect(RSQLite::SQLite(), "Model/Experiment_PNAS_iterations/0000_Run_Compiled")

run_data = dbGetQuery(con,'
  SELECT * 
  from run_data')

fwrite(run_data, "Data/EXP_PNAS_run_data.csv")


env_data <- dbGetQuery(con,'SELECT * 
                           FROM environment 
                           WHERE run_id
                           IN (
                           SELECT run_id
                           FROM run_data
                           WHERE num_sources = 500 
                           AND num_nutree = 2000)')

fwrite(env_data,"Data/EXP_PNAS_Env_Data_ns_500_nt_2000.csv")


OG_data <- dbGetQuery(con,"SELECT * 
                           FROM tools 
                           WHERE parent_id = 'OG'")

fwrite(OG_data,"Data/EXP_PNAS_All_OG.csv")


tools <- dbGetQuery(con,'SELECT * 
                           FROM tools')


fwrite(tools, "Data/EXP_PNAS_tools.csv")

sources <- dbGetQuery(con,'SELECT * 
                           FROM sources')

fwrite(sources, "Data/EXP_PNAS_sources.csv")

trees <- dbGetQuery(con, 'SELECT * 
                    FROM trees')

fwrite(trees, "Data/EXP_PNAS_trees.csv")
