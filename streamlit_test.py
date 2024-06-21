import streamlit as st
import openai

openai.api_key = YOUR_OPENAI_API_KEY

def chat_gpt(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1000,
    )
    return response["choices"][0]["text"]

st.title("ChatGPT Demo")

user_prompt = st.text_input("Enter your prompt:")
if st.button("Send"):
    chat_response = chat_gpt(user_prompt)
    st.write(chat_response)
