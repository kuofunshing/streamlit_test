import streamlit as st
import os
import openai
from openai import OpenAI
from PIL import Image

# 使用环境变量设置 OpenAI API 金钥
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# 初始化 OpenAI 客户端
client = OpenAI(api_key=api_key)

st.title("ChatGPT 对话功能")
st.write("与 ChatGPT 进行对话。")

# 初始化聊天历史记录
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 获取用户输入
user_input = st.text_input("你：", key="input")

# 当用户输入新消息时，将其添加到聊天历史记录中并获取模型的响应
if user_input:
    st.session_state['chat_history'].append({"role": "user", "content": user_input})
    try:
        chat_completion = client.chat.completions.create(
            messages=st.session_state['chat_history'],
            model="gpt-4o",
        )
        assistant_message = chat_completion.choices[0].message.content
        st.session_state['chat_history'].append({"role": "assistant", "content": assistant_message})
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# 显示聊天历史记录
for message in st.session_state['chat_history']:
    role = "你" if message["role"] == "user" else "ChatGPT"
    st.write(f"{role}: {message['content']}")
st.header("圖片")
st.write("這是圖片頁面。")
uploaded_file = st.file_uploader("選擇一個圖片文件", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 打開並顯示圖片
    image = Image.open(uploaded_file)
    st.image(image, caption='上傳的圖片', use_column_width=True)
    

else:
    st.write("請上載一個圖片文件。")
