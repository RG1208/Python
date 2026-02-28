import os
from dotenv import load_dotenv #type: ignore
from langchain_groq import ChatGroq #type: ignore
from langchain_core.messages import HumanMessage #type: ignore
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder #type: ignore

# For Message History
from langchain_community.chat_message_histories import ChatMessageHistory #type: ignore
from langchain_core.chat_history import BaseChatMessageHistory #type: ignore
from langchain_core.runnables.history import RunnableWithMessageHistory #type: ignore

# 1. Setup
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

model = ChatGroq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY)

# 2. History Store
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        # Note: ChatMessageHistory() takes no arguments
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 3. Prompt Template 
# IMPORTANT: 'history' MUST come before 'messages'
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Answer the user's questions in {language}"),
        MessagesPlaceholder(variable_name="history"),  # Past Conversation
        MessagesPlaceholder(variable_name="messages"), # Current Question
    ]
)

chain = prompt | model

# 4. Runnable with History
with_message_history = RunnableWithMessageHistory(
    chain, 
    get_session_history,
    input_messages_key="messages",
    history_messages_key="history",  # This key is required for history tracking

)

# 5. Execution
config = {"configurable": {"session_id": "chat1"}}

# --- FIRST INTERACTION ---
print("--- Sending First Message ---")
response1 = with_message_history.invoke(
    {
        "messages": [HumanMessage(content="hello, My Name is Rachit")],
        "language": "english"
    },
    config=config
)
print("AI:", response1.content)

print("\n" + "-"*30 + "\n")

# --- SECOND INTERACTION ---
print("--- Sending Second Message ---")
response2 = with_message_history.invoke(
    {
        "messages": [HumanMessage(content="what is my name?")],
        "language": "english"
    },
    config=config
)
print("AI:", response2.content)