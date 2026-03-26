from ollama import Image
from typing_extensions import Annotated
from langgraph.graph import StateGraph,START,END
from IPython.display import Image,display
from langchain_openai import ChatOpenAI

#Reducers
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

import os 
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


llm_openai = ChatOpenAI(model="gpt-4o")

def super_bot(state: State) -> str:
    return {"messages": llm_openai.invoke(state["messages"])}

graph= StateGraph(State)

graph.add_node("Super Bot",super_bot)

graph.add_edge(START, "Super Bot")
graph.add_edge("Super Bot", END)  

graph_builder = graph.compile()

# Get the image data (PNG bytes)
png_data = graph_builder.get_graph().draw_mermaid_png()

# 1. Save to a file
with open("02_Chatbot.png", "wb") as f:
    f.write(png_data)
    print("Graph saved as '02_Chatbot.png'")

# 2. Display in notebook (if applicable)
display(Image(png_data))

result=graph_builder.invoke({"graph_info":"what is the real meaning of life?"})
print("graph_info: ",result["graph_info"])
