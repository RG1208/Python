import os 
from dotenv import load_dotenv 
from langchain.agents import create_agent 

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def get_weather(city: str) -> str:
    """A mock function to get the weather for a given city."""
    return f"The weather is sunny in {city} with a high of 25°C."

agent = create_agent(
    "gpt-5", 
    tools=[get_weather],
    system_prompt="You are a helpful assistant that can answer questions about the weather"
)

# Print an ASCII representation of the graph
print(agent.get_graph().draw_ascii())

# Save the graph as an image file in your current folder
with open("graph.png", "wb") as f:
    f.write(agent.get_graph().draw_mermaid_png())

print("Graph saved as graph.png")


res=agent.invoke({"messages": [{"role": "user", "content": "What is the weather in New York?"}]})
print(res["messages"][-1].content)

print(agent.invoke({"messages":"what is the weather in New York?"})["messages"][-1].content)