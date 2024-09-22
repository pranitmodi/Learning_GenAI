from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

import streamlit as st
import os
from dotenv import load_dotenv  
load_dotenv()

# Load environment variables from .env file
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")

# LangSmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "testing_langchain_ollama"

# Prompt Template
prompt = ChatPromptTemplate([
    ('system', 'You are a helpful assistant. Please respond to all the queries of the user.'),
    ('user', 'Question:{question}')
])

# Streamlit framework
st.title("Langchain Demo with Ollama using Llama3.1")
input_text = st.text_input("Enter your question here")

# Ollama Llama2  LLM
llm = Ollama(model="llama3.1")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_text:
    st.write(chain.invoke({'question': input_text}))