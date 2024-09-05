from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
import ssl,httpx

load_dotenv()
ssl_context = ssl.create_default_context()
ssl_context.load_default_certs()
httpx_client = httpx.Client(verify=ssl_context)

llm = ChatOpenAI(model_name      = "gpt-35-turbo",
                 openai_api_base = "https://llm-proxy-api.ai.openeng.netapp.com",
                 openai_api_key  = os.getenv("OPENAI_API_KEY"),
                 model_kwargs    = {'user': 'pranitm' },
                 http_client = httpx_client)

prompt = ChatPromptTemplate(
    [('system','You are an code generator assistant who is well versed with PlayWright tool, and the user will give you english sentence as input and you should return a single line of code using PlayWright tool to perform the action mentioned in the sentence. For example, if the user asks you to click on a button, you should return a line of code that clicks on the button using PlayWright tool. Let\'s start!'),
    ('user','Navigate to google.com and click on the search button.'),
    ])
output_parser = StrOutputParser()

chain = prompt | llm | output_parser
completion = chain.invoke({})
print(completion)