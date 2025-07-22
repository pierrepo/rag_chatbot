import time
import os
import streamlit as st

st.set_page_config(page_title="Build knowledge base", page_icon="🧠")

st.title("Build knowledge base")


uploaded_files = st.file_uploader("Upload your documentation files here", accept_multiple_files=True)
if st.button("Build knowledge base", type="primary", icon="🔨"):
    if not os.environ.get("OPENROUTER_API_KEY"):
        st.error("Please provide an OpenRouter API key.")
        st.stop()
    if not uploaded_files:
        st.error("Please upload at least one documentation file.")
        st.stop()
    st.write("Building knowledge base... (this may take a while)")
    for up_file in uploaded_files:
        # Here you would typically process the file and build your knowledge base
        # For demonstration purposes, we will just show the file name
        st.session_state["logs"].append(f"Processing file: {up_file.name}")
        time.sleep(1)  # Simulate a time-consuming process