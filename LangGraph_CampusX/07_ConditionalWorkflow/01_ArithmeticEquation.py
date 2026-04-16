from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Literal
from IPython.display import Image, display
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openai import BaseModel
from pydantic import ConfigDict, ConfigDict, Field
import operator

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

class QuadState(TypedDict):
    a: int
    b: int
    c: int

    equation: str
    discriminant: float
    result: str

graph = StateGraph(QuadState)

def showEquation(state: QuadState):
    a = state["a"]
    b = state["b"]
    c = state["c"]

    equation = f"{a}x^2 + {b}x + {c} = 0"
    return {"equation":equation}

def calculateDiscriminant(state: QuadState):
    a = state["a"]
    b = state["b"]
    c = state["c"]

    discriminant = b ** 2 - 4 * a * c
    return {"discriminant":discriminant}

def realRoots(state: QuadState):
    a = state["a"]
    b = state["b"]
    discriminant = state["discriminant"]

    root1 = (-b + discriminant ** 0.5) / (2 * a)
    root2 = (-b - discriminant ** 0.5) / (2 * a)
    result = f"Two real roots: {root1} and {root2}"
    return {"result":result}

def repeatedRoots(state: QuadState):
    a = state["a"]
    b = state["b"]

    root = -b / (2 * a)
    result = f"One repeated root: {root}"
    return {"result":result}

def noRealRoots(state: QuadState):
    result = "No real roots"
    return {"result":result}

def check_condition(state: QuadState) -> Literal["realRoots", "repeatedRoots", "noRealRoots"]:
    discriminant = state["discriminant"]
    if discriminant > 0:
        return "realRoots"
    elif discriminant == 0:
        return "repeatedRoots"
    else:
        return "noRealRoots"

# Adding Nodes
graph.add_node("showEquation",showEquation)
graph.add_node("calculateDiscriminant",calculateDiscriminant)
graph.add_node("realRoots",realRoots)
graph.add_node("repeatedRoots",repeatedRoots)
graph.add_node("noRealRoots",noRealRoots)


# Adding Edges
graph.add_edge(START, "showEquation")
graph.add_edge("showEquation", "calculateDiscriminant")
graph.add_conditional_edges("calculateDiscriminant", check_condition)
graph.add_edge("realRoots", END)
graph.add_edge("repeatedRoots", END)
graph.add_edge("noRealRoots", END)


# Compile
workflow = graph.compile()


initial_state = {
    "a": 1,
    "b": 3,
    "c": 2
}

final_state = workflow.invoke(initial_state)

print(final_state)

# ------------------- Graph Image -------------------

from IPython.display import Image, display

png_data = workflow.get_graph().draw_mermaid_png()

with open("01.png", "wb") as f:
    f.write(png_data)
    print("Graph saved as '01.png'")

display(Image(png_data))