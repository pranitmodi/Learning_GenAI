import pip_system_certs.wrapt_requests
import requests
import streamlit as st

def get_openai_response(input_text):
    print("Open AI Request", input_text)
    try:
        response = requests.post("http://localhost:8000/essay/invoke", json={'log': input_text})
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No response received.")
    except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")

def get_llm_response(input_text):
    response = requests.post("http://localhost:8000/poem/invoke", json={"input": {'topic': input_text}})
    return response.json()['output']

st.title('Langchain Demo With LLAMA2 API and OpenAI API')
input_text = st.text_input("Write an essay on...")
input_text1 = st.text_input("Write a poem on...")

if input_text:
    st.write(get_openai_response(input_text))

if input_text1: 
    st.write(get_llm_response(input_text1))

