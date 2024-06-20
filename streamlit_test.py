import streamlit as st
import openai
import requests

# OpenAI API密钥
OPENAI_API_KEY = 'openai_api_key'

# ChatCompletion API的URL
COMPLETION_API_URL = 'https://api.openai.com/v1/engines/davinci-codex/completions'

def get_response(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    data = {
        'prompt': prompt,
        'max_tokens': 60,
        'n': 1,
        'stop': None,
        'temperature': 0.5
    }
    response = requests.post(COMPLETION_API_URL, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()[0]['choices'][0]['text']
    else:
        return 'Error generating response.'

st.title('Simple Dialogue Bot')

user_input = st.text_input("Ask something:")
if st.button('Get Response'):
    response = get_response(user_input)
    st.write(response)
