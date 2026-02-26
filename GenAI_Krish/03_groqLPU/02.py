import os
from dotenv import load_dotenv #type: ignore
from langchain_groq import ChatGroq #type: ignore
from langchain_core.messages import SystemMessage, HumanMessage #type: ignore
from langchain_core.output_parsers import StrOutputParser #type: ignore

load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

model=ChatGroq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY)

