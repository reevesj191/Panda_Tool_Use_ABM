library(sp)
library(data.table)
library(doParallel)


tools_sum <- fread("../Data/EXP_PNAS_tool_sum_ns_100_nt_2000.csv")
tools_sum_no_space <- tools_sum
trees <- fread("../Data/EXP_PNAS_trees.csv")
sources <- fread("../Data/EXP_PNAS_sources.csv")

trees$life <- "Dead"
trees$life[trees$ts_died == -1] <- "Alive"


coordinates(trees) <- c('x', 'y')
coordinates(tools_sum) <- c('x', 'y')

cl <- makeCluster(50)
registerDoParallel(cl)

results <- foreach(i = 1:nrow(tools_sum), .combine = rbind, .packages= c('sp', 'rgeos')) %dopar% {
  
  site <- tools_sum[i,]
  sub_trees  <- subset(trees, run_id == site$run_id)
  sub_trees$near_site<-gWithinDistance(spgeom1 = site, spgeom2 = sub_trees, dist = 1.5, byid = TRUE)[,1]
  close_trees <- subset(sub_trees@data, near_site == TRUE)
  if(nrow(close_trees) == 0){ print("No Trees WTF")}
  c("Alive" %in% close_trees, nrow(close_trees))
}


colnames(results) <- c("Tree_Status", "N_Trees")
tools_sum <- cbind(tools_sum_no_space, results)


fwrite(tools_sum, "../Data/EXP_PNAS_tool_sum_ns_100_nt_2000_updated.csv")

library(ggplot2)
library(dplyr)

tools_sum <- left_join(tools_sum, run_data)

ggplot(tools_sum,aes(x = as.factor(Tree_Status), y = n_pounding, fill = as.factor(treessdie)))+
  scale_y_log10()+
  geom_boxplot()
  
