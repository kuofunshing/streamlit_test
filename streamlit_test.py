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

# 初始化聊天历史记录和剩余服务次数
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'remaining_uses' not in st.session_state:
    st.session_state['remaining_uses'] = 10  # 假设初始服务次数为10

# 图片页面标题
st.header("圖片")
st.write("這是圖片頁面。")

# 检查剩余服务次数是否足够
if st.session_state['remaining_uses'] <= 0:
    st.warning("剩餘服務次數不足，請充值。")
    return

# 文件上傳
uploaded_file = st.file_uploader("選擇一個圖片文件", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 打開並顯示圖片
    image = Image.open(uploaded_file)
    st.image(image, caption='上傳的圖片', use_column_width=True)
    
    # 每次上傳成功後減少一次剩餘服務次數
    st.session_state['remaining_uses'] -= 1
    st.write(f"剩餘次數: {st.session_state['remaining_uses']}")
else:
    st.write("請上載一個圖片文件。")

# 聊天功能部分保持不变
if user_input:
    st.session_state['chat_history'].append({"role": "user", "content": user_input})
    try:
        chat_completion = client.chat.completions.create(
            messages=st.session_state['chat_history'],
            model="gpt-3.5-turbo",
        )
        assistant_message = chat_completion.choices[0].message.content
        st.session_state['chat_history'].append({"role": "assistant", "content": assistant_message})
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# 显示聊天历史记录
for message in st.session_state['chat_history']:
    role = "你" if message["role"] == "user" else "ChatGPT"
    st.write(f"{role}: {message['content']}")
