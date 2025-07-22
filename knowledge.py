import time
import os
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document

st.set_page_config(page_title="Build knowledge base", page_icon="📦")

st.title("Build knowledge base")


uploaded_files = st.file_uploader(
    "Upload your documentation files here",
    accept_multiple_files=True,
    type=["txt", "md", "html"],
)
if not st.button("Build knowledge base", type="primary", icon="🔨"):
    st.stop()

if not os.environ.get("OPENROUTER_API_KEY"):
    st.error("Please provide an OpenRouter API key.")
    st.stop()

if not uploaded_files:
    st.error("Please upload at least one documentation file.")
    st.stop()


# Define the text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,    # target chunk size in characters 
    chunk_overlap=100,  # overlap to maintain context between chunks
    separators=["\n\n", "\n", " ", ""]
)

# Intialize chunks list
document_chunks = []

st.write("Building knowledge base... (this may take a while)")
for uploaded_file in uploaded_files:
    # Here you would typically process the file and build your knowledge base
    # For demonstration purposes, we will just show the file name
    msg = f"Processing file: {uploaded_file.name}"
    st.write(msg)
    st.session_state["logs"].append(msg)
    document = uploaded_file.read().decode("utf-8")

    chunks = text_splitter.split_text(document)
    st.write(f"Created {len(chunks)} chunks.")

    for idx, chunk in enumerate(chunks, start=1):
        doc = Document(
            page_content=chunk,
            metadata={
                "chunk": idx,
                "source": f"{uploaded_file.name}",
                },
            )
        document_chunks.append(doc)
    st.write("First chunk:")
    st.write(document_chunks[0].page_content)
