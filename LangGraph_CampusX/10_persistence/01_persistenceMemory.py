
from sre_parse import State

from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
load_dotenv()

llm = ChatOpenAI()
class JokeState(TypedDict):

    topic: str
    joke: str
    explanation: str
def generate_joke(state: JokeState):

    prompt = f'generate a joke on the topic {state["topic"]}'
    response = llm.invoke(prompt).content

    return {'joke': response}
def generate_explanation(state: JokeState):

    prompt = f'write an explanation for the joke - {state["joke"]}'
    response = llm.invoke(prompt).content

    return {'explanation': response}

graph = StateGraph(JokeState)

graph.add_node('generate_joke', generate_joke)
graph.add_node('generate_explanation', generate_explanation)

graph.add_edge(START, 'generate_joke')
graph.add_edge('generate_joke', 'generate_explanation')
graph.add_edge('generate_explanation', END)

checkpointer = InMemorySaver()
workflow = graph.compile(checkpointer=checkpointer)

config1 = {"configurable": {"thread_id": "1"}}
workflow.invoke({'topic':'pizza'}, config=config1)
# To get the state of the workflow after invocation
# Includes the Joke and the explanation
workflow.get_state(config1)

# To get the history of states for the workflow execution
# Includes the state before each node execution
list(workflow.get_state_history(config1))


# Reinvocation with the same thread_id will resume from the last checkpoint

# Invocating LLM with new Thread ID will start a fresh execution
config2 = {"configurable": {"thread_id": "2"}}
workflow.invoke({'topic':'pasta'}, config=config2)
workflow.get_state(config1)
list(workflow.get_state_history(config1))


workflow.get_state({"configurable": {"thread_id": "1", "checkpoint_id": "1f06cc6e-7232-6cb1-8000-f71609e6cec5"}})
workflow.invoke(None, {"configurable": {"thread_id": "1", "checkpoint_id": "1f06cc6e-7232-6cb1-8000-f71609e6cec5"}})
list(workflow.get_state_history(config1))

# ------------------- Graph Image -------------------

from IPython.display import Image, display

png_data = workflow.get_graph().draw_mermaid_png()

with open("01.png", "wb") as f:
    f.write(png_data)
    print("Graph saved as '01.png'")

display(Image(png_data))

