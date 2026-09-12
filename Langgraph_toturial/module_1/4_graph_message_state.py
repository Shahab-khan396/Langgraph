from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("Set OPENROUTER_API_KEY in your .env file before running the app.")




# state

model = ChatOpenAI(
    model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4.1-mini"),
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    max_tokens=1024,
    timeout=30,
    max_retries=0,
    temperature=0,
)



# Nodes

def chat(state: MessagesState)-> MessagesState:
    return {"messages":[model.invoke(state["messages"])]}


# edges

# putting our graph together
builder = StateGraph(MessagesState)

builder.add_node("chat", chat)

builder.add_edge(START, "chat")
builder.add_edge("chat", END)

graph= builder.compile()
