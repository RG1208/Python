from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from IPython.display import Image, display

class BMI (TypedDict):
    weight_kg : float
    height_m : float
    bmi : float
    category : str

graph = StateGraph(BMI)


# Add node to graph
# Add Edge to graph
# Compile the graph
# Execute the graph

def calculateBMI(state: BMI) -> BMI:
    weight_kg = state['weight_kg']
    height_m = state['height_m']
    bmi = weight_kg / (height_m ** 2)
    state['bmi'] = round(bmi, 2)
    return state

def labelBMI(state: BMI) -> BMI:
    bmi = state['bmi']
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obesity"
    
    state['category'] = category
    return state

# Add node to graph
graph.add_node("CalculateBMI", calculateBMI)
graph.add_node("labelBMI", labelBMI)

# Add Edge to graph
graph.add_edge(START, "CalculateBMI")
graph.add_edge("CalculateBMI", "labelBMI")
graph.add_edge("labelBMI", END)

# Compile the graph
workflow = graph.compile()

# Execute the graph
initial_state = {
    'weight_kg': 70,
    'height_m': 1.75
}

final_state = workflow.invoke(initial_state)

print(final_state)

# Get the image data (PNG bytes)
png_data = workflow.get_graph().draw_mermaid_png()

# 1. Save to a file
with open("02.png", "wb") as f:
    f.write(png_data)
    print("Graph saved as '02.png'")

# 2. Display in notebook (if applicable)
display(Image(png_data))