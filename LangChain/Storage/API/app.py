from fastapi import FastAPI, HTTPException
from langserve import add_routes
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import ssl, httpx, os
from dotenv import load_dotenv
import uvicorn
from langchain_community.llms import Ollama

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
os.environ["LANGCHAIN_PROJECT"] = "langchain_fastAPI"
 
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server"
)

model = ChatOpenAI(
    model_name="gpt-4o",
    openai_api_base="https://llm-proxy-api.ai.openeng.netapp.com",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_kwargs={'user': 'pranitm'},
    http_client=httpx_client
)
output_parser = StrOutputParser()

llm = Ollama(model="llama3.1")

prompt1 = ChatPromptTemplate([("system","""You are an expert essay writer."""),
    ("human","Write me an essay about {log} with 100 words.")])
prompt2 = ChatPromptTemplate.from_template("Write me a poem about {topic} with 100 words.")

# add_routes(
#     app,
#     prompt1|model|output_parser,
#     path="/essay"
# ) 

class Query(BaseModel):
    log: str

@app.post("/query")
def handle_query(query: Query):
    question = query.log
    try:
        # Create and execute the chain
        chain = prompt1 | llm | output_parser
        response = chain.invoke({"log": question})
        return{"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

add_routes(
    app,
    prompt2|llm,
    path="/poem"
) 

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)