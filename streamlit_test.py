import streamlit as st
import os
from PIL import Image
import openai
from openai import OpenAI
from google.cloud import vision
import io

# 使用环境变量设置 OpenAI API 金钥和 Google Cloud Vision API 密钥
api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_CLOUD_VISION_API_KEY")

if not api_key or not google_api_key:
    raise ValueError("Please set the OPENAI_API_KEY and GOOGLE_CLOUD_VISION_API_KEY environment variables.")

# 初始化 OpenAI 客户端
client = OpenAI(api_key=api_key)

# 初始化 Google Cloud Vision 客户端
vision_client = vision.ImageAnnotatorClient.from_service_account_json('path_to_your_service_account.json')

st.title("ChatGPT 对话功能")
st.write("与 ChatGPT 进行对话。")

# 初始化聊天历史记录
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 获取用户输入
user_input = st.text_input("你：", key="input")

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

st.header("图片")
st.write("这是图片页面。")
uploaded_file = st.file_uploader("选择一个图片文件", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='上传的图片', use_column_width=True)
    
    # Perform label detection
    with st.spinner("正在识别图片标签..."):
        content = io.BytesIO()
        image.save(content, format="JPEG")
        image_vision = vision.Image(content=content.getvalue())
        response = vision_client.label_detection(image=image_vision)
        labels = response.label_annotations
        result = "<br>".join([label.description for label in labels])
        st.write("识别结果:", result)

else:
    st.write("请上传一个图片文件。")
