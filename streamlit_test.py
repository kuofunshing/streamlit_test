import streamlit as st
import os
import openai
from openai import OpenAI
from PIL import Image

# Set up OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Configure page layout
st.set_page_config(layout="wide")
tab1, tab2 = st.tabs(["ChatGPT 對話功能", "圖片處理"])

# ChatGPT Dialogue Functionality
with tab1:
    st.title("ChatGPT 對話功能")
    st.write("根据标签推荐 YouTube 影片。")

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Get user input for tags
    user_input = st.text_input("輸入標籤：", key="input")

    # When user inputs tags, generate YouTube video recommendations
    if user_input:
        st.session_state['chat_history'].append({"role": "user", "content": user_input})
        try:
            # Assuming the model understands the task to recommend YouTube videos based on tags
            prompt = f"根据以下標籤推薦三個 YouTube 影片，只顯示標題和連結，不需要詳細說明：{user_input}"
            response = client.Completion.create(
                model="text-davinci-002",  # Use an appropriate model for text generation
                prompt=prompt,
                max_tokens=150
            )
            st.session_state['chat_history'].append({"role": "assistant", "content": response.choices[0].text})
        except Exception as e:
            st.error(f"发生错误：{str(e)}")

    # Display chat history and results
    for message in st.session_state['chat_history']:
        role = "你" if message["role"] == "user" else "ChatGPT"
        st.write(f"{role}: {message['content']}")

# Image Processing
with tab2:
    st.header("圖片處理")
    st.write("这是图片处理页面。")

    # User selects an animal for image display
    animal = st.selectbox("選擇一個動物", ['cat', 'Pig', 'Bus', 'Cheetah', 'Penguins', 'Car', 'rabbit', 'zebra', 'Scooter'])

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

    # File uploader for additional image processing
    uploaded_file = st.file_uploader("選擇一個圖片文件", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='上傳的圖片', use_column_width=True)
    else:
        st.write("請上傳一個圖片文件。")
