import os
from dotenv import load_dotenv 
from langchain.agents import create_agent 
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain.tools import tool
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

# model = init_chat_model("google_genai:gemini-2.5-flash-lite")
model = ChatGroq(model="qwen/qwen3-32b")
@tool
def get_weather(location: str) -> str:
    """Get the current weather for a given location."""
    # In a real implementation, you would call a weather API here.
    return f"The current weather in {location} is sunny with a temperature of 25°C."

model_with_tools = model.bind_tools([get_weather])

# Step 1: Model generates tool calls
messages = [{"role": "user", "content": "What's the weather in Boston?"}]
ai_msg = model_with_tools.invoke(messages)
print("AI Message:", ai_msg)
print("/n")
messages.append(ai_msg)

# Step 2: Execute tools and collect results
for tool_call in ai_msg.tool_calls:
    # Execute the tool with the generated arguments
    tool_result = get_weather.invoke(tool_call)
    messages.append(tool_result)

# Step 3: Pass results back to model for final response
final_response = model_with_tools.invoke(messages)
print(final_response.text)
print("/n")

# "The current weather in Boston is 72°F and sunny."
print("--------------------Coversation History--------------------")
print(messages)


with open("graph1.png", "wb") as f:
    f.write(messages.get_graph().draw_mermaid_png())

print("Graph saved as graph1.png")