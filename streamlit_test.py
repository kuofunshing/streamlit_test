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

# 设置页面布局
st.set_page_config(layout="wide")
tab1, tab2 = st.tabs(["ChatGPT 对话功能", "图片处理"])

# ChatGPT 对话功能
with tab1:
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
                model="gpt-4o",  # 假设这是正确的模型名称
            )
            assistant_message = chat_completion.choices[0].message.content
            st.session_state['chat_history'].append({"role": "assistant", "content": assistant_message})
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # 显示聊天历史记录
    for message in st.session_state['chat_history']:
        role = "你" if message["role"] == "user" else "ChatGPT"
        st.write(f"{role}: {message['content']}")

# 图片处理
with tab2:
    st.header("图片处理")
    st.write("这是图片处理页面。")

    animal = st.selectbox("选择一个动物", ['cat', 'Pig', 'Bus', 'Cheetah', 'Penguins', 'Car', 'rabbit', 'zebra', 'Scooter'])

    # 根据选择显示图片和文本
    if animal:
        image_path = f'label/{animal}.jpg'
        text_path = f'label/{animal}.txt'

        if os.path.exists(image_path) and os.path.exists(text_path):
            image = Image.open(image_path)
            st.image(image, caption=f'显示的是: {animal}', use_column_width=True)

            with open(text_path, 'r') as file:
                text_content = file.read()
            st.write(text_content)
        else:
            st.error("文件不存在，请确保路径和文件名正确。")

    uploaded_file = st.file_uploader("选择一个图片文件", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='上传的图片', use_column_width=True)
    else:
        st.write("请上传一个图片文件。")
