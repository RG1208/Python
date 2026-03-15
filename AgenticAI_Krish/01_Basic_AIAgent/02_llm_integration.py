import os 
from dotenv import load_dotenv 
from langchain.agents import create_agent 
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")


# OPEN AI Model.
openAI_model = init_chat_model("gpt-4o")
response = openAI_model.invoke("What is the capital of France?")
print(response.content)

openAI_model = ChatOpenAI(model="gpt-4o")
response = openAI_model.invoke("What is the capital of France?")
print(response.content)

# Gemini Model.
gemini_model = init_chat_model("google_genai:gemini-2.5-flash-lite")
response = gemini_model.invoke("what is the capital of India?")
print(response.content)

gemini_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
response = gemini_model.invoke("what is the capital of India?")
print(response.content)

# Groq Model.
groq_model = init_chat_model("groq:qwen/qwen3-32b")
response = groq_model.invoke("What is the capital of USA?")
print(response.content)

groq_model = ChatGroq(model="qwen/qwen3-32b")
response = groq_model.invoke("What is the capital of USA?")
print(response.content)