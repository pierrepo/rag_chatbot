import streamlit as st

st.set_page_config(page_title="Logs", page_icon="🗞️")

st.title("Log Page")
for log_message in st.session_state.get("logs", []):
    st.markdown(log_message)
