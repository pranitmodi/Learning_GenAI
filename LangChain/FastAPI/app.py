from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
import ssl, httpx
import uvicorn

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")

# LangSmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "testing_using_FastAPI"

from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
app = FastAPI()

ssl_context = ssl.create_default_context()
ssl_context.load_default_certs()
httpx_client = httpx.Client(verify=ssl_context)

llm = ChatOpenAI(
    model_name="gpt-35-turbo",
    openai_api_base="https://llm-proxy-api.ai.openeng.netapp.com",
    openai_api_key=openai_api_key,
    model_kwargs={'user': 'pranitm'},
    http_client=httpx_client
)
output_parser = StrOutputParser()
prompt = ChatPromptTemplate([
    ('system', 'You are a helpful assistant who is an expert Essay Writer.'),
    ('user', 'Question:{abc}')
])

chain = prompt | llm | output_parser

class Query(BaseModel):
    question: str

@app.post("/invoke")
def handle_query(query: Query):
    question = query.question
    if not openai_api_key:
        return {"Error":"OPENAI_API_KEY not found. Please set it in the .env file."}
    else:
        try:
            response = chain.invoke({'abc': question})
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)