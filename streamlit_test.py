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
st.write("与 ChatGPT 进行对话，获取基于标签的 YouTube 视频推荐。")

# 初始化聊天历史记录
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 获取用户输入
user_input = st.text_input("你：", key="input")

# 当用户输入新消息时，将其添加到聊天历史记录中并获取模型的响应
if user_input:
    st.session_state['chat_history'].append({"role": "user", "content": user_input})
    
    # 添加系统信息指导模型行为
    system_message = "你是影片搜尋助手,以繁體中文回答,請根據提供的標籤推薦2015年後的youtube影片,僅顯示標題和連結"
    st.session_state['chat_history'].append({"role": "system", "content": system_message})

    try:
        chat_completion = client.chat.completions.create(
            messages=st.session_state['chat_history'],
            model="gpt-4o",
            max_tokens=200  # 设置最大token数为200
        )
        assistant_message = chat_completion.choices[0].message.content
        st.session_state['chat_history'].append({"role": "assistant", "content": assistant_message})
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

st.header("圖片")
st.write("這是圖片頁面。")
options = ["Bus", "Car", "Cheetah", "Penguins", "Pig", "Scooter", "cat", "rabbit", "zebra"]
animal = st.selectbox("選擇一個項目", options)

# Display image and text based on selection
if animal:
    image_path = f'label/{animal}.jpg'
    text_path = f'label/{animal}.txt'

    if os.path.exists(image_path) and os.path.exists(text_path):
        image = Image.open(image_path)
        st.image(image, caption=f'顯示的是: {animal}', use_column_width=True)

        with open(text_path, 'r') as file:
            text_content = file.read()
        st.write(text_content)
    else:
        st.error("文件不存在，請確保路徑和文件名正確。")

uploaded_file = st.file_uploader("選擇一個圖片文件", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='上傳的圖片', use_column_width=True)
else:
    st.write("請上傳一個圖片文件。")

# 显示聊天历史记录
for message in st.session_state['chat_history']:
    role = "你" if message["role"] == "user" else "ChatGPT"
    st.write(f"{role}: {message['content']}")
