from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated

# Reducer function (takes latest value)
def latest(x, y):
    return y

# State with reducers for parallel updates
class BatsmanState(TypedDict):
    runs: int
    balls: int
    numOfFours: int
    numOfSixes: int

    sr: Annotated[float, latest]
    bpb: Annotated[float, latest]
    boundaryPercentage: Annotated[float, latest]
    summary: Annotated[str, latest]

# Create graph
graph = StateGraph(BatsmanState)

# ------------------- Nodes -------------------

def calculate_sr(state: BatsmanState) -> dict:
    runs = state['runs']
    balls = state['balls']
    sr = (runs / balls) * 100 if balls > 0 else 0
    return {"sr": sr}

def calculate_bpb(state: BatsmanState) -> dict:
    numOfFours = state['numOfFours']
    numOfSixes = state['numOfSixes']
    balls = state['balls']
    bpb = balls / (numOfFours + numOfSixes) if (numOfFours + numOfSixes) > 0 else 0
    return {"bpb": bpb}

def calculate_boundary_percentage(state: BatsmanState) -> dict:
    numOfFours = state['numOfFours']
    numOfSixes = state['numOfSixes']
    runs = state['runs']
    boundaryPercentage = ((numOfFours * 4) + (numOfSixes * 6)) / runs * 100 if runs > 0 else 0
    return {"boundaryPercentage": boundaryPercentage}

def summary(state: BatsmanState) -> dict:
    summary_text = (
        f"Batsman scored {state['runs']} runs off {state['balls']} balls, "
        f"with {state['numOfFours']} fours and {state['numOfSixes']} sixes. "
        f"Strike Rate: {state['sr']:.2f}, "
        f"Balls per Boundary: {state['bpb']:.2f}, "
        f"Boundary Percentage: {state['boundaryPercentage']:.2f}%."
    )
    return {"summary": summary_text}

# ------------------- Graph -------------------

# Add nodes
graph.add_node('calculate_sr', calculate_sr)
graph.add_node('calculate_bpb', calculate_bpb)
graph.add_node('calculate_boundary_percentage', calculate_boundary_percentage)
graph.add_node('summary', summary)

# Parallel edges
graph.add_edge(START, 'calculate_sr')
graph.add_edge(START, 'calculate_bpb')
graph.add_edge(START, 'calculate_boundary_percentage')

# Fan-in to summary
graph.add_edge('calculate_sr', 'summary')
graph.add_edge('calculate_bpb', 'summary')
graph.add_edge('calculate_boundary_percentage', 'summary')

# End
graph.add_edge('summary', END)

# Compile
workflow = graph.compile()

# ------------------- Run -------------------

initial_state = {
    "runs": 120,
    "balls": 80,
    "numOfFours": 10,
    "numOfSixes": 5
}

final_state = workflow.invoke(initial_state)

print(final_state)

# ------------------- Graph Image -------------------

from IPython.display import Image, display

png_data = workflow.get_graph().draw_mermaid_png()

with open("parallel_graph.png", "wb") as f:
    f.write(png_data)
    print("Graph saved as 'parallel_graph.png'")

display(Image(png_data))