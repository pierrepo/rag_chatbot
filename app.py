import os

from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Initialize session state for logs
st.session_state.setdefault("logs", [])

# configure sidebar with settings
st.sidebar.header("Settings")
api_key = st.sidebar.text_input(
    "OpenAI API key",
    type="password",
    help="You can get an OpenAI API key from https://platform.openai.com/api-keys",
    value=os.environ.get("OPENAI_API_KEY", None)
)
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

pages = {
    "RAG chatbot": [
        st.Page("chatbot_basic.py", title="Basic chatbot", icon="🤖"),
        st.Page("knowledge.py", title="Build knowledge base", icon="📦"),
        st.Page("chatbot_rag.py", title="RAG chatbot", icon="🧠"),
        st.Page("log.py", title="Logs", icon="🗞️")
    ]
}
pg = st.navigation(pages)
pg.run()





