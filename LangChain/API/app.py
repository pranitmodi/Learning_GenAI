from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv
import ssl, httpx

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")

ssl_context = ssl.create_default_context()
ssl_context.load_default_certs()
httpx_client = httpx.Client(verify=ssl_context)

# LangSmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "langchain_fastAPI"
 
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server"
)

model = ChatOpenAI(
    model_name="gpt-35-turbo",
    openai_api_base="https://llm-proxy-api.ai.openeng.netapp.com",
    openai_api_key=openai_api_key,
    model_kwargs={'user': 'pranitm'},
    http_client=httpx_client
)
llm = Ollama(model="llama3.1")

prompt1 = ChatPromptTemplate.from_template("Write me an essay about {topic} with 100 words.")
prompt2 = ChatPromptTemplate.from_template("Write me a poem about {topic} with 100 words.")

add_routes(
    app,
    prompt1|model,
    path="/essay"
) 

add_routes(
    app,
    prompt2|llm,
    path="/poem"
) 

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)