from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from IPython.display import Image, display
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",  
    temperature=0
)

class LLMState(TypedDict):
    topic: str
    outline: str
    content: str

def llm_outline(state: LLMState) -> LLMState:
    
    # Take input
    topic = state['topic']

    # Form a prompt
    prompt = f"Create a detailed outline for an article about: {topic}"

    # Ask that question to the LLM
    response = llm.invoke(prompt)

    # update the answer in the state
    state['outline'] = response.content

    return state

def llm_content(state: LLMState) -> LLMState:
    
    # Take input
    outline = state['outline']

    # Form a prompt
    prompt = f"Write a detailed article based on the following outline: {outline}"

    # Ask that question to the LLM
    response = llm.invoke(prompt)

    # update the answer in the state
    state['content'] = response.content

    return state


# create graph
graph = StateGraph(LLMState)

# Add node to graph
graph.add_node("LLM_Outline", llm_outline)
graph.add_node("LLM_Content", llm_content)

# Add Edge to graph
graph.add_edge(START, "LLM_Outline")
graph.add_edge("LLM_Outline", "LLM_Content")
graph.add_edge("LLM_Content", END)

# Compile the graph
workflow = graph.compile()

# Execute the graph
initial_state = {
    "topic": "The benefits of renewable energy"
}

final_state = workflow.invoke(initial_state)

print(final_state)

# Get the image data (PNG bytes)
png_data = workflow.get_graph().draw_mermaid_png()

# 1. Save to a file
with open("04.png", "wb") as f:
    f.write(png_data)
    print("Graph saved as '04.png'")

# 2. Display in notebook (if applicable)
display(Image(png_data))