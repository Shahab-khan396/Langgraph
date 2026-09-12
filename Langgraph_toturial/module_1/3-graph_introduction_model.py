from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from typing import Literal , NotRequired
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("Set OPENROUTER_API_KEY in your .env file before running the app.")


# state
class state(TypedDict):
    graph_int:NotRequired[int]
    graph_str:str
 

model = ChatOpenAI(
    model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4.1-mini"),
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    max_tokens=1024,
    timeout=30,
    max_retries=0,
    temperature=0,
)    

# node 
def node1(state: state)-> state:
    """ take a state and ask our model to pick a  number between 1 and 2 """
    model_response = model.invoke([{"role": "user", "content": "Pick a number between 1 and 2. only respond with the number."}])

    try:
        selected_number = int(str(model_response.content).strip())
    except (TypeError, ValueError):
        selected_number = 0

    if selected_number not in (1, 2):
        selected_number = 0

    return {"graph_int": selected_number,
            "graph_str": state["graph_str"] + " passed through node 1!"}


def node2(state: state)-> state:

    return{"graph_int":state["graph_int"],
           "graph_str":state["graph_str"]+ " passed through node 2!"}

def node3(state: state)-> state:

    return{"graph_int":state["graph_int"],
           "graph_str":state["graph_str"]+ " passed through node 3!"}

# edges
def next_step(state: state)->Literal["node2", "node3"]:
    """guide the state to the next node based on the current state"""

    if state["graph_int"] == 1:
        return "node2"
    else:
        return "node3"

# putting our graph together

builder = StateGraph(state)

builder.add_node("node1", node1)
builder.add_node("node2", node2)
builder.add_node("node3", node3)

builder.add_edge(START, "node1")
builder.add_conditional_edges("node1", next_step)
builder.add_edge("node2", END)
builder.add_edge("node3", END)

graph = builder.compile()
