import streamlit as st
import os
import openai
from openai import OpenAI

# 使用環境變數設置 OpenAI API 金鑰
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("請設定 OPENAI_API_KEY 環境變數。")

# 初始化 OpenAI 客戶端
client = OpenAI(api_key=api_key)

# 設定頁面佈局
st.set_page_config(layout="wide")
tab1, tab2 = st.tabs(["ChatGPT 對話功能", "圖片處理"])

# ChatGPT 對話功能
with tab1:
    st.title("ChatGPT 對話功能")
    st.write("輸入標籤獲取推薦的 YouTube 影片連結。")
    
    # 初始化聊天歷史記錄
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # 獲取用戶輸入
    user_input = st.text_input("你：", key="input")

    # 當用戶輸入新消息時，將其添加到聊天歷史記錄中並獲取模型的響應
    if user_input:
        st.session_state['chat_history'].append({"role": "user", "content": user_input})
        try:
            chat_completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "你是影片搜尋助手,以繁體中文回答,請根據提供的標籤推薦youtube影片,僅顯示標題和連結,不要用記錄呈現的文字回答"},
                    {"role": "user", "content": user_input}
                ]
            )
            assistant_message = chat_completion.choices[0].message['content']
            st.session_state['chat_history'].append({"role": "assistant", "content": assistant_message})
        except Exception as e:
            st.error(f"發生錯誤：{str(e)}")

    # 顯示聊天歷史記錄
    for message in st.session_state['chat_history']:
        role = "你" if message["role"] == "user" else "ChatGPT"
        st.write(f"{role}: {message['content']}")

with tab2:
    st.header("圖片處理")
    st.write("這是圖片處理頁面。")

    animal = st.selectbox("選擇一個動物", ['cat', 'Pig', 'Bus', 'Cheetah', 'Penguins', 'Car', 'rabbit', 'zebra', 'Scooter'])

    # 根據選擇顯示圖片和文本
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

    # Additional image processing with file uploader
    uploaded_file = st.file_uploader("選擇一個圖片文件", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='上傳的圖片', use_column_width=True)
    else:
        st.write("請上傳一個圖片文件。")
