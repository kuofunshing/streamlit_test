import streamlit as st
import openai

# 設置 OpenAI API 金鑰
openai.api_key = 'YOUR_OPENAI_API_KEY'

st.title("ChatGPT 對話功能")
st.write("與 ChatGPT 進行對話。")

# 初始化聊天歷史記錄
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 獲取用戶輸入
user_input = st.text_input("你：", key="input")

# 當用戶輸入新消息時，將其添加到聊天歷史記錄中並獲取模型的響應
if user_input:
    st.session_state['chat_history'].append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=st.session_state['chat_history']
    )
    st.session_state['chat_history'].append({"role": "assistant", "content": response['choices'][0]['message']['content']})

# 顯示聊天歷史記錄
for message in st.session_state['chat_history']:
    role = "你" if message["role"] == "user" else "ChatGPT"
    st.write(f"{role}: {message['content']}")
