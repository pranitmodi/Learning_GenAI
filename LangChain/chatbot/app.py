from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv
import ssl, httpx

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")

ssl_context = ssl.create_default_context()
ssl_context.load_default_certs()
httpx_client = httpx.Client(verify=ssl_context)

# LangSmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "testing_langchain"

# Prompt Template
prompt = ChatPromptTemplate([
    ('system', 'You are a helpful assistant. Please respond to all the queries of the user.'),
    ('user', 'Question:{question}')
])

# Streamlit framework
st.title("Langchain Demo with OpenAI")
input_text = st.text_input("Enter your question here")

# OpenAI LLM
if not openai_api_key:
    st.error("OPENAI_API_KEY not found. Please set it in the .env file.")
else:
    llm = ChatOpenAI(
        model_name="gpt-35-turbo",
        openai_api_base="https://llm-proxy-api.ai.openeng.netapp.com",
        openai_api_key=openai_api_key,
        model_kwargs={'user': 'pranitm'},
        http_client=httpx_client
    )
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

if input_text:
    st.write(chain.invoke({'question': input_text}))