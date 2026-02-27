import os
from dotenv import load_dotenv #type: ignore
from langchain_groq import ChatGroq #type: ignore
from langchain_core.messages import SystemMessage, HumanMessage #type: ignore
from langchain_core.output_parsers import StrOutputParser #type: ignore
from langserve import add_routes #type: ignore
from langchain_core.prompts import ChatPromptTemplate#type: ignore

# For Message History
from langchain_community.chat_message_histories import ChatMessageHistory #type: ignore
from langchain_core.chat_history import BaseChatMessageHistory #type: ignore
from langchain_core.runnables.history import RunnableWithMessageHistory #type: ignore


load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

model=ChatGroq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY)

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory(session_id=session_id)
    return store[session_id]

with_message_history = RunnableWithMessageHistory(model, get_session_history)

config={"configurable": {"session_id": "chat1"}}

response = with_message_history.invoke(
    [
        HumanMessage(content="hello, My Name is Rachit")
    ],
    config=config
)

print(response.content)
config={"configurable": {"session_id": "chat2"}}
response = with_message_history.invoke(
    [
        HumanMessage(content="Whats my name?")
    ],
    config=config
)

print(response.content)