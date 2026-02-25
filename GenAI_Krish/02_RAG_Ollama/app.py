from langchain_core.prompts import ChatPromptTemplate #type: ignore
from langchain_ollama import OllamaLLM #type:ignore
from langchain_core.output_parsers import StrOutputParser #type: ignore
import streamlit as st #type: ignore

prompt = ChatPromptTemplate.from_template(
"""
you are a helpful assistant that answers questions based on the provided context.
if you dont know the answer simply say "I Don't Know".
Question: {question}
"""
)

#Streamlit UI
st.title("RAG with Ollama and Streamlit")
input_query = st.text_input("Enter your query:")

#LLM
llm = OllamaLLM(model="llama3.1:8b")
output_parser=StrOutputParser()

chain= prompt | llm | output_parser
if input_query:
    response=chain.invoke({"question": input_query})
    st.write(response)