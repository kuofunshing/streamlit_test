import streamlit as st
import openai
import requests

# Replace 'your_openai_api_key_here' with your actual OpenAI API key
OPENAI_API_KEY = 'your_openai_api_key_here'

# ChatCompletion API's URL
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
    try:
        response = requests.post(COMPLETION_API_URL, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()[0]['choices'][0]['text']
        else:
            # Improved error handling to display the status code
            return f'Error generating response. Status Code: {response.status_code}.'
    except Exception as e:
        # Catching exceptions to handle network errors or other issues
        return f'An error occurred: {str(e)}'

st.title('Simple Dialogue Bot')

user_input = st.text_input("Ask something:")
if st.button('Get Response'):
    response = get_response(user_input)
    st.write(response)
