from fastapi import FastAPI #type: ignore
import os
from dotenv import load_dotenv #type: ignore
from langchain_groq import ChatGroq #type: ignore
from langchain_core.messages import SystemMessage, HumanMessage #type: ignore
from langchain_core.output_parsers import StrOutputParser #type: ignore
from langserve import add_routes #type: ignore
from langchain_core.prompts import ChatPromptTemplate#type: ignore

load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

model=ChatGroq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY)

system_template = "Translate the following English text to {language}"
prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=system_template),
        HumanMessage(content="{text}"),
    ]
)   

parser = StrOutputParser()
chain = prompt_template | model | parser

app = FastAPI(
    title="LangServe with Groq and FastAPI",
    description="A simple FastAPI application that uses LangServe to serve a Groq model for language translation.",
    version="1.0.0",
) 

add_routes(app, chain, path="/chain")

if __name__ == "__main__":
    import uvicorn #type: ignore
    uvicorn.run(app, host="localhost", port=8000)