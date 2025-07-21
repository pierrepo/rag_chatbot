import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model=os.environ.get("OPENROUTER_MODEL_NAME"),
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

response = llm.invoke("What is the capital of France?")

print(response.content)

