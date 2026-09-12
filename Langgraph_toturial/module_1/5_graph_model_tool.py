from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.tools import tool
from langgraph.prebuilt import ToolNode

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


@tool
def search(query: str):
    """Call to surf the web."""
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."

tools = [search]
tool_node = ToolNode(tools)

model_llm_with_tools = model.bind_tools([tool_node])


# node
def chat_with_tools(state: MessagesState)-> MessagesState:
    return {"messages": [model_llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(MessagesState)

builder.add_node("chat_with_tools", chat_with_tools)
builder.add_edge(START, "chat_with_tools")
builder.add_edge("chat_with_tools", END)

graph = builder.compile()