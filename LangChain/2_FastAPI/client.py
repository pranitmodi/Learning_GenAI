import requests
import streamlit as st

def get_openai_response(text):
    # print("Open AI Request", text)
    try:
        response = requests.post("http://localhost:8000/invoke", json={'question': text})
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")

st.title('Langchain + FastAPI Demo With OpenAI API')
input_text = st.text_input("Write an essay on...")

if input_text:
    st.write(get_openai_response(input_text))