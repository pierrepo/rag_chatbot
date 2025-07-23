import os

from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import streamlit as st

st.set_page_config(page_title="RAG Chatbot", page_icon="🧠")

st.title("RAG Chatbot 🧠")

chromadb_directory = st.session_state.get("chromadb_directory")

if not chromadb_directory:
    st.error("Please build the knowledge base first.")
    st.stop()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vectordb = Chroma(
    embedding_function=embeddings,
    persist_directory=chromadb_directory
)

st.write(f"{vectordb._collection.count()} documents found in the knowledge base 📦.")

llm = ChatOpenAI(
    model=os.environ.get("OPENAI_MODEL_NAME"),
    api_key=os.environ.get("OPENAI_API_KEY"),
)

with st.chat_message(name="assistant"):
    st.markdown("""
Hello! I'm RAG chatbot helping you with your documentation
""")

# Initialize session state for messages
st.session_state.setdefault("messages", [])

for message in st.session_state["messages"]:
    with st.chat_message(name=message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask me a question...")

if prompt:
    st.session_state["messages"].append(
        {
            "role": "human",
            "content": prompt
        }
    )

    with st.chat_message(name="human"):
        st.markdown(prompt)

    chat_history = ""
    for message in st.session_state["messages"][:-1]:
        chat_history += (
            f"{message['role'].capitalize()}: "
            f"{message['content']}\n"
        )

    docs = vectordb.similarity_search_with_score(prompt, k=3)
    context_rag = f"HUMAN: {prompt}\n"
    context_rag += "You are a helpful assistant. Answer the question based on the context provided.\n"
    context_rag += "CONTEXT:\n" 
    for doc, score in docs:
        context_rag += f"{doc.page_content}\n"
        context_rag += "---\n"
    context_rag += "QUESTION:\n"
    context_rag += f"{prompt}\n"
    context_rag += "ANSWER:\n"
    st.session_state["logs"].append(f"{context_rag}")
    response = llm.invoke(
        chat_history + context_rag
    )

    st.session_state["messages"].append(
        {
            "role": "assistant",
            "content": response.content
        }
    )

    with st.chat_message(name="assistant"):
        st.markdown(response.content)
