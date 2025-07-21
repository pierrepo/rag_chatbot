import os
import time
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st


load_dotenv()

llm = ChatOpenAI(
    model=os.environ.get("OPENROUTER_MODEL_NAME"),
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

st.set_page_config(page_title="RAG Chatbot", page_icon=":robot:")
st.title("Basic RAG chatbot")

# configure sidebar with settings
st.sidebar.header("Settings")
api_key = st.sidebar.text_input(
    "OpenRouter API key",
    type="password",
    help="You can get an OpenRouter API key from https://openrouter.ai",
    value=os.environ.get("OPENROUTER_API_KEY", None)
)
uploaded_files = st.sidebar.file_uploader("Upload your documentation files here", accept_multiple_files=True)
if st.sidebar.button("Build knowledge base", type="primary", icon="🔨"):
    if not api_key:
        st.error("Please provide an OpenRouter API key.")
        st.stop()
    if not uploaded_files:
        st.error("Please upload at least one documentation file.")
        st.stop()
    st.sidebar.write("Building knowledge base... (this may take a while)")
    for up_file in uploaded_files:
        # Here you would typically process the file and build your knowledge base
        # For demonstration purposes, we will just show the file name
        st.sidebar.write(f"Processing file: {up_file.name}")
        time.sleep(1)  # Simulate a time-consuming process

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

    context = ""
    for message in st.session_state["messages"]:
        context += (
            f"{message['role'].capitalize()}: "
            f"{message['content']}\n"
        )

    response = llm.invoke(
        context
    )

    st.session_state["messages"].append(
        {
            "role": "assistant",
            "content": response.content
        }
    )

    with st.chat_message(name="assistant"):
        st.markdown(response.content)
