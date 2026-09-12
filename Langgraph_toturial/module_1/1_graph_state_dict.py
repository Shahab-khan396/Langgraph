from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# STATE
class state(TypedDict):
    graph_str: str

# NODE
def greeting(state: state) -> state:
    """ this is a simple greeting function """
    
    return {"graph_str": state["graph_str"] + " welcome to Langgraph!"}
#EDGES


# PUTTING OUR GRAPH TOGETHER
builder = StateGraph(state)


builder.add_node("greeting", greeting)


builder.add_edge(START, "greeting")
builder.add_edge("greeting", END)

graph = builder.compile()

result = graph.invoke({"graph_str": "Hello!"})

print(result)