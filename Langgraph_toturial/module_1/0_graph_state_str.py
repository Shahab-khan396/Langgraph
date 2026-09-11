# import libraries 

from langgraph.graph import StateGraph, START, END

# state


# node 
def greeting(state:str)-> str:
      """ this is a simple greeting function """
      return state + " welcome to Langgraph!"




# edges



# langgraph putting our graph together

builder = StateGraph(str)

# add nodes to the graph
builder.add_node("greeting", greeting)


# add edges to the graph
builder.add_edge(START, "greeting")
builder.add_edge("greeting", END)

graph= builder.compile()