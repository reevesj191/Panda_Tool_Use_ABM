#### ABM FUNCTIONS



dist2source <- function(tools = tools, sources = sources){
  
  ## Calculates the distance an artifact to its origin from a dataframe.
  ## Requires a dataframe of tools and a dataframe of sources from the PANDA Model
  
  sources$s_id <- paste(sources$run_id, sources$id)
  tools$s_id <- paste(tools$run_id, tools$source_id)
  source_join <- sources[,c("s_id", "x", "y")]
  colnames(source_join) <- c("s_id", "s_x", "s_y")
  tool_join <- left_join(tools, source_join, by = c("s_id" = "s_id"))
  d2source <- sqrt(((tool_join$x-tool_join$s_x)^2) + 
                     ((tool_join$y-tool_join$s_y)^2))
  return(d2source)
}










