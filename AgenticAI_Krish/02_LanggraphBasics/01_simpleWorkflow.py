from typing_extensions import TypedDict

class state(TypedDict):
    graph_info:str

def start_play(state: state):
    print("start play has been called")
    return {"graph_info":state["graph_info"] + " I am planning to play "}

def cricket(state: state):
    print("cricket has been called")
    return {"graph_info":state["graph_info"] + "cricket."}

def badminton(state: state):
    print("badminton has been called")
    return {"graph_info":state["graph_info"] + "badminton."}

import random
from typing import Literal

def randomPlay(state: state) -> Literal["cricket", "badminton"]:
    print("random play has been called")
    graph_info = state["graph_info"]
    if random.random() > 0.5:
        return "cricket"
    else:
        return "badminton"
    
from IPython.display import Image,display
from langgraph.graph import StateGraph, START, END

#Build Graph

graph=StateGraph(state)

#Adding Nodes
graph.add_node("start_play",start_play)
graph.add_node("cricket",cricket)
graph.add_node("badminton",badminton)

#schedule the flow of the graph
graph.add_edge(START,"start_play")
graph.add_conditional_edges("start_play",randomPlay)
graph.add_edge("cricket",END)
graph.add_edge("badminton",END)

#Compile the graph
graph_builder = graph.compile()

# --- SAVE AND VIEW THE GRAPH ---

# Get the image data (PNG bytes)
png_data = graph_builder.get_graph().draw_mermaid_png()

# 1. Save to a file
with open("01_simpleWorkflow.png", "wb") as f:
    f.write(png_data)
    print("Graph saved as '01_simpleWorkflow.png'")

# 2. Display in notebook (if applicable)
display(Image(png_data))



#Execute the graph
result = graph_builder.invoke({"graph_info":"My name is Rachit."})
print("graph_info: ",result["graph_info"])
