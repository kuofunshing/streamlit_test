import streamlit as st
import os
from PIL import Image
import openai
from google.cloud import vision
import io

# 设置环境变量和客户端初始化
api_key = os.getenv("OPENAI_API_KEY")
service_account_json = 'path_to_service_account.json'  # Google Cloud Vision JSON

if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# 初始化 OpenAI 和 Google Cloud Vision 客户端
openai.api_key = api_key
vision_client = vision.ImageAnnotatorClient.from_service_account_json(service_account_json)

st.title("ChatGPT 对话功能")
st.write("与 ChatGPT 进行对话和图片分析。")

uploaded_file = st.file_uploader("选择一个图片文件", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='上传的图片', use_column_width=True)

    # 图片处理和标签检测
    content = io.BytesIO()
    image.save(content, format="JPEG")
    image_vision = vision.Image(content=content.getvalue())
    response = vision_client.label_detection(image=image_vision)
    labels = response.label_annotations
    labels_text = ', '.join([label.description for label in labels])

    st.write("图片包含以下内容：", labels_text)

    # 使用 OpenAI GPT-4o 生成 YouTube 视频推荐
    if st.button('生成视频推荐'):
        try:
            prompt = f"根据以下内容推荐 YouTube 视频：{labels_text}"
            response = openai.Completion.create(
                engine="davinci-codex",
                prompt=prompt,
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.7
            )
            recommendations = response.choices[0].text.strip()
            st.write("推荐视频：", recommendations)
        except Exception as e:
            st.error(f"生成推荐时发生错误: {str(e)}")
else:
    st.write("请上传一个图片文件。")
