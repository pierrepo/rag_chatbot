import os

from langchain_openai import ChatOpenAI
import streamlit as st

st.set_page_config(page_title="Basic Chatbot", page_icon="🤖")

st.title("Basic Chatbot 🤖")


llm = ChatOpenAI(
    model=os.environ.get("OPENAI_MODEL_NAME"),
    api_key=os.environ.get("OPENAI_API_KEY"),
)


with st.chat_message(name="assistant"):
    st.markdown("""
Hello! I'm basic chatbot. How can I help you?
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
