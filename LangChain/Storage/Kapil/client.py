import streamlit as st
import requests

API_URL = "http://10.193.228.56:8000/query"

# Initialize session state for question and answer
if 'question' not in st.session_state:
    st.session_state.question = ""
if 'answer' not in st.session_state:
    st.session_state.answer = ""
if 'automation_issue' not in st.session_state:
    st.session_state.automation_issue = False

# Streamlit UI
st.title("GCNV Automation Triager")
st.write("Enter an error log to classify it!!")

st.session_state.question = st.text_input("Your Question", st.session_state.question)

if st.button("Get Answer"):
    if st.session_state.question:
        with st.spinner('Getting answer...'):
            try:
                response = requests.post(API_URL, json={"log": st.session_state.question})
                response.raise_for_status()
                data = response.json()
                st.session_state.answer = data.get("response", "No response received.")
                st.session_state.automation_issue = "Automation Issue" in st.session_state.answer
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a question.")

# Display the answer
if st.session_state.answer:
    st.write(st.session_state.answer)

# If an automation issue is detected, show the file uploader
if st.session_state.automation_issue:
    st.write("Upload the .robot file where the Automation Issue happens:")
    uploaded_file = st.file_uploader("Choose a .robot file", type="robot")
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        # Make another API call to process the .robot file
        with st.spinner('Analyzing the .robot file...'):
            try:
                response = requests.post(API_URL + "/analyze_robot", json={"log": st.session_state.question, "file_content": file_content})
                response.raise_for_status()
                data = response.json()
                analysis_result = data.get("response", "No response received.")
                st.write(analysis_result)
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred while analyzing the .robot file: {e}")
