import os

from dotenv import load_dotenv
import streamlit as st

pages = {
    "RAG chatbot": [
        st.Page("knowledge.py", title="Build knowledge base", icon="🏠"),
        st.Page("chatbot.py", title="Chatbot", icon="🤖"),
        st.Page("log.py", title="Logs", icon="🗞️")
    ]
}
pg = st.navigation(pages)
pg.run()

# Initialize session state for logs
st.session_state.setdefault("logs", [])

load_dotenv()

# configure sidebar with settings
st.sidebar.header("Settings")
api_key = st.sidebar.text_input(
    "OpenRouter API key",
    type="password",
    help="You can get an OpenRouter API key from https://openrouter.ai",
    value=os.environ.get("OPENROUTER_API_KEY", None)
)
if api_key:
    os.environ["OPENROUTER_API_KEY"] = api_key


