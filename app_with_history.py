"""
Documentation :
https://ai.google.dev/gemini-api/docs/text-generation?lang=python

"""
from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

import streamlit as st
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_ID = "gemini-2.0-flash"

##initialize our streamlit app

st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# This is to store the chat history of all conversations in a format that Google API requires
if 'chat_history_model' not in st.session_state:
    st.session_state['chat_history_model'] = []

## function to load Gemini Pro model and get repsonses
chat = client.chats.create(model=MODEL_ID,history = st.session_state['chat_history_model'])

input=st.text_input("Input: ",key="input")
submit=st.button("Ask the question")

if submit and input:
    response=chat.send_message(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("user", input))
    st.session_state['chat_history_model'].append(types.Content(parts=[types.Part(text = input)], role = "user"))
    st.subheader("The Response is")
    st.write(response.text)
    st.session_state['chat_history'].append(("bot",response.text))
    st.session_state['chat_history_model'].append(types.Content(parts=[types.Part(text = response.text)], role = "model"))



st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role} : {text}")

