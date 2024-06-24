
import streamlit as st
import os
from PIL import Image
import json
import openai
from google.cloud import vision
from google.oauth2 import service_account
import io

# 使用环境变量设置 OpenAI API 密钥和 Google Cloud Vision API 密钥
open_api_key = os.getenv("OPENAI_API_KEY")
service_account_info = json.loads(os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON'))

if not open_api_key or not service_account_info:
    raise ValueError("Please set the OPENAI_API_KEY and GOOGLE_APPLICATION_CREDENTIALS_JSON environment variables.")

# 初始化 OpenAI 客户端
client = openai.OpenAI(api_key=open_api_key)

# Google Cloud Vision 客户端初始化
credentials = service_account.Credentials.from_service_account_info(service_account_info)
vision_client = vision.ImageAnnotatorClient(credentials=credentials)

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
            model="gpt-4",  # 使用正确的模型标识符
            prompt=user_input,
            max_tokens=150
        )
        assistant_message = chat_completion.choices[0].text.strip()
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
    with st.spinner("正在识别图片标签..."):
        content = io.BytesIO()
        image.save(content, format="JPEG")
        image_vision = vision.Image(content=content.getvalue())
        response = vision_client.label_detection(image=image_vision)
        labels = response.label_annotations
        result = "<br>".join([label.description for label in labels])
        st.write("识别结果:", result)

        try:
            description = generate_gpt_description(result)
            st.write("生成的描述：")
            st.write(description)
        except Exception as e:
            st.error(f"生成描述失败：{str(e)}")
            description = "生成描述失败"

def generate_gpt_description(result, use_gpt4=False):
    try:
        model = "gpt-4" if use_gpt4 else "gpt-3.5"
        messages = [
            {"role": "system", "content": "你是专业图片描述生成助手,以繁体中文回答,请确实地描述图片状况,不要用记录呈现的文字回答"},
            {"role": "user", "content": f"根据以下辨识结果生成一段描述：{result}"}
        ]
        response = client.Completion.create(
            model=model,
            prompt="\n".join([m["content"] for m in messages]),
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"生成描述失败: {str(e)}"

