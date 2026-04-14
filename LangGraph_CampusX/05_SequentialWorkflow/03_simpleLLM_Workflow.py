from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from IPython.display import Image, display
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


llm = ChatOpenAI(
    model="gpt-4o-mini",  # or any model you want
    temperature=0
)
class LLMState(TypedDict):
    input_text: str
    output_text: str

def llm_qa(state: LLMState) -> LLMState:
    
    # Take input
    input_text = state['input_text']

    # Form a prompt
    prompt = f"Answer the following question: {input_text}"

    # Ask that question to the LLM
    response = llm.invoke(prompt)

    # update the answer in the state
    state['output_text'] = response.content

    return state

# create graph
graph = StateGraph(LLMState)

# Add node to graph
graph.add_node("LLM_QA", llm_qa)

# Add Edge to graph
graph.add_edge(START, "LLM_QA")
graph.add_edge("LLM_QA", END)

# Compile the graph
workflow = graph.compile()

# Execute the graph
initial_state = {
    "input_text": "What is the capital of France?",
}

final_state = workflow.invoke(initial_state)

print(final_state)

# Get the image data (PNG bytes)
png_data = workflow.get_graph().draw_mermaid_png()

# 1. Save to a file
with open("03.png", "wb") as f:
    f.write(png_data)
    print("Graph saved as '03.png'")

# 2. Display in notebook (if applicable)
display(Image(png_data))