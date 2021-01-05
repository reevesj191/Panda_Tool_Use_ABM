library(DBI)
library(data.table)

conn <- DBI::dbConnect(RSQLite::SQLite(), "../../../Desktop/Exp2_master")

rundata <- dbGetQuery(conn, "SELECT * FROM run_data WHERE n_time_steps = 25000 AND num_sources != 1000")
fwrite(rundata, "EXP_2_25k_run_data.csv")
trees <- dbGetQuery(conn, "SELECT * FROM trees")
trees <- subset(trees, run_id %in% rundata$run_id)
fwrite(trees, "EXP_2_25K_trees.csv")
sources <- dbGetQuery(conn, "SELECT * FROM sources")
sources <- subset(sources, run_id %in% rundata$run_id)
fwrite(sources, "EXP_2_25K_sources.csv")

sql_select <- "SELECT * FROM tools WHERE run_id IN"
sql_in_query <- "(SELECT run_id FROM run_data WHERE n_time_steps = 25000 AND num_sources != 1000)"
query <- paste(sql_select, sql_in_query)

tools <- dbGetQuery(conn, query)
fwrite(tools, "EXP_2_25k_tools.csv")






rundata <- dbGetQuery(conn, "SELECT * FROM run_data WHERE num_sources = 10")
fwrite(rundata, "EXP_2_ns10_run_data.csv")

sql_select <- "SELECT * FROM trees WHERE run_id IN"
sql_in_query <- "(SELECT run_id FROM run_data WHERE num_sources = 10)"
query <- paste(sql_select, sql_in_query)

trees <- dbGetQuery(conn, query)
fwrite(trees, "EXP_2_ns10_trees.csv")

sql_select <- "SELECT * FROM sources WHERE run_id IN"
sql_in_query <- "(SELECT run_id FROM run_data WHERE num_sources = 10)"
query <- paste(sql_select, sql_in_query)

sources <- dbGetQuery(conn, query)
fwrite(sources, "EXP_2_ns10_sources.csv")

sql_select <- "SELECT * FROM tools WHERE run_id IN"
sql_in_query <- "(SELECT run_id FROM run_data WHERE num_sources = 10)"
query <- paste(sql_select, sql_in_query)

tools <- dbGetQuery(conn, query)
fwrite(tools, "EXP_2_ns10_tools.csv")

