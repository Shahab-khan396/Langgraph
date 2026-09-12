from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from typing import Literal


#state
class state(TypedDict):
    graph_str: str



# nodes
def node1(state: state)-> state:
    return {"graph_str": state["graph_str"] + " from node 1!"}

def node2(state: state)-> state:
    return {"graph_str": state["graph_str"] + " from node 2!"}

def node3(state: state)-> state:
    return {"graph_str": state["graph_str"] + " from node 3!"}  


# edges
def next_step(state: state)->Literal["node2", "node3"]:
    """guide the state to the next node based on the current state"""
    
    state_str = state["graph_str"]
    array_state_str= state_str.split(" ")
    if array_state_str[0] == "Hello!":
        return "node2"
    else:
        return "node3"    

#putting our graph together
builder = StateGraph(state)

builder.add_node("node1", node1)
builder.add_node("node2", node2)
builder.add_node("node3", node3)


builder.add_edge(START, "node1")
builder.add_conditional_edges("node1", next_step)
builder.add_edge("node2", END)
builder.add_edge("node3", END)

graph = builder.compile()


