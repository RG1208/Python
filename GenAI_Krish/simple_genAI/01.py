import os
from dotenv import load_dotenv #type: ignore
from langchain_community.document_loaders import PyMuPDFLoader #type: ignore
from langchain_text_splitters import RecursiveCharacterTextSplitter  #type: ignore
from langchain_openai import OpenAIEmbeddings #type: ignore
from langchain_community.vectorstores import FAISS #type: ignore
from langchain_classic.chains.combine_documents import create_stuff_documents_chain #type: ignore
from langchain_core.prompts import ChatPromptTemplate #type: ignore
from langchain_openai import ChatOpenAI #type: ignore
from langchain_classic.chains import create_retrieval_chain #type: ignore


# 1. Load Data 
# 2. Docs
# 3. Divide text into Chunks
# 4. Convert text into vectors using vector embeddings
# 5. Store vectors in a vector database
# 6. User asks a question
# 7. We search FAISS for relevant chunks (semantic search)
# 8. We send those chunks + a prompt to the LLM
# 9. The LLM answers using only that context

# Document chain:
    # Takes documents (chunks)
    # “Stuffs” them into {context}
    # Sends the final prompt to the LLM
    # Gets the answer

# A retriever is a wrapper around FAISS that:
    # Takes a user query
    # Runs similarity search
    # Returns relevant documents

# Retriever chain does:
    # Takes user input question
    # Sends it to retriever
    # Retriever fetches relevant chunks from FAISS
    # Passes those chunks to document_chain
    # document_chain puts them in prompt
    # LLM generates the final answer

# When you do:
    # retriever_chain.invoke({"input": "your question"})

# LangChain does:
    # 1. Converts your question to embedding
    # 2. Searches FAISS
    # 3. Gets top relevant chunks
    # 4. Inserts them into {context}
    # 5. Sends prompt + context to GPT-4o
    # 6. Gets answer
    # 7. Returns a dict like:
        # {
        #   "input": "...",
        #   "context": [docs...],
        #   "answer": "Final answer from LLM"
        # }
    # You print:
    # response["answer"]
    # That’s the final AI answer based on your PDF.

# create_retrieval_chain wires everything together
# This creates a bigger chain that does:

    # 1. Takes user input: "input": question
    # 2. Sends question to retriever
    # 3. Retriever fetches relevant chunks from FAISS
    # 4. Takes those chunks and passes them to document_chain
    # 5. document_chain:
        # Stuffs chunks into {context}
        # Calls LLM
    # 6. Returns final answer

    # So yes — retriever runs first, then document_chain runs.
    # You just don’t see it explicitly because LangChain composes them internally.

# retriver is responsible for retrieving relevant chunks from input query 
# once the retrived chunks are fetched they are pushed into the docuemnt chain using the retriever chain and 
# once the docuemnt chain has the retrived docs they are pushed in the prompt context and given to the llm 

# so if have written code in top to down but the process is getting executed in bottom to top approach

# retriever → gets relevant chunks
# retriever_chain → passes them to document_chain
# document_chain → stuffs them into {context}
# prompt + context → goes to LLM
# LLM → generates answer

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_AI_API_KEY")

# 1. Load Data 
loader = PyMuPDFLoader("ResQBridgeSIDD.pdf")
print(loader)
print("PDF loaded successfully!")

# 2. Docs
docs = loader.load()
print(f"Number of documents loaded: {len(docs)}")

# 3. Divide text into Chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
splitted_docs = text_splitter.split_documents(docs)
print(f"Text split into chunks successfully! Number of chunks: {len(splitted_docs)}")
print("Text splitting completed!")


# 4. Convert text into vectors using vector embeddings
embeddings = OpenAIEmbeddings()
print("Embeddings created successfully!")

# 5. Store vectors in a vector database
vectorstore = FAISS.from_documents(splitted_docs, embeddings)
print("Vectors stored in vector database successfully!")
print("-------------------------------------------------------------------------")

#Retrieval Chain
prompt = ChatPromptTemplate.from_template(
"""
Answer the follwoing questions based only on the provided context.
if you dont know the answer simply say "I Don't Know".

<context>
{context}
</context>

Question: {input}
"""
)
llm = ChatOpenAI(model="gpt-4o")
document_chain = create_stuff_documents_chain(llm,prompt)
print(f"Document chain created successfully!")
print("-------------------------------------------------------------------------")

retriever = vectorstore.as_retriever()
retriever_chain=create_retrieval_chain(retriever,document_chain)
print("Retrieval chain created successfully!")
print("-------------------------------------------------------------------------")

#Getting response from LLM
input_query = input("Enter your query: ")
response = retriever_chain.invoke({"input": input_query})
print(response["answer"])