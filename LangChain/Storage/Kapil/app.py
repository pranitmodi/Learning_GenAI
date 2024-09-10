from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import ssl, httpx, os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
app = FastAPI()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Setup SSL context
ssl_context = ssl.create_default_context()
ssl_context.load_default_certs()
httpx_client = httpx.Client(verify=ssl_context)

prompt = ChatPromptTemplate([ 
    ("system",""""Write me an essay about {topic} with 100 words."""), 
    ("human","Error Log is : {log}"), 
])

# Create the LLM instance
llm = ChatOpenAI(
    model_name="gpt-4o",
    openai_api_base="https://llm-proxy-api.ai.openeng.netapp.com",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_kwargs={'user': 'pranitm'},
    http_client=httpx_client
)

# Define the output parser
output_parser = StrOutputParser()

class Query(BaseModel):
    log: str

class RobotFileAnalysis(BaseModel):
    log: str
    file_content: str

@app.post("/query")
def handle_query(query: Query):
    question = query.log
    try:
        # Create and execute the chain
        chain = prompt | llm | output_parser
        response = chain.invoke({"log": question})
        return{"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query/analyze_robot")
def analyze_robot_file(analysis: RobotFileAnalysis):
    log = analysis.log
    file_content = analysis.file_content
    try:
        analyze_prompt = ChatPromptTemplate([
            ("system", """give 5 points about AI""")
        ])

        # Create and execute the chain for analyzing the .robot file
        chain = analyze_prompt | llm | output_parser
        response = chain.invoke({"log": log, "file_content": file_content})
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)