import os
from dotenv import load_dotenv #type: ignore
from langchain_groq import ChatGroq #type: ignore
from langchain_core.messages import HumanMessage, AIMessage #type: ignore
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder #type: ignore

# For Message History
from langchain_community.chat_message_histories import ChatMessageHistory #type: ignore
from langchain_core.chat_history import BaseChatMessageHistory #type: ignore
from langchain_core.runnables.history import RunnableWithMessageHistory #type: ignore

from langchain_core.runnables import RunnablePassthrough #type: ignore
from operator import itemgetter #type: ignore
from langchain_core.messages import trim_messages #type: ignore

# 1. Setup
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

model = ChatGroq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY)

# 2. History Store
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 3. Prompt Template 
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Answer the user's questions in {language}"),
        MessagesPlaceholder(variable_name="messages"), 
    ]
)

# print("AI:", response2.content)

trimmer = trim_messages(
    max_tokens=45, 
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human"
)

chain = (
    RunnablePassthrough.assign(history=itemgetter("messages") | trimmer)
    | prompt
    | model
)


with_message_history = RunnableWithMessageHistory(
    chain, 
    get_session_history,
    input_messages_key="messages"
)

config = {"configurable": {"session_id": "chat1"}}

response1 = with_message_history.invoke(
    {
        "messages": [
            HumanMessage(content="My name is Rachit. Can you tell me a joke?"),               
        ],
        "language": "english"
    },
    config=config
)

print(response1.content)

print("-------------------------------------------------------------------")

response2 = with_message_history.invoke(
    {
        "messages": [
            HumanMessage(content="What is my name"),               
        ],
        "language": "english"
    },
    config=config
)

print(response2.content)