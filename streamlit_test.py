import streamlit as st
import os
import openai
from openai import OpenAI

# 使用环境变量设置 OpenAI API 金钥
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# 初始化 OpenAI 客户端
client = OpenAI(api_key=api_key)

st.title("ChatGPT 對話功能")
st.write("根据标签推荐 YouTube 影片。")

# 初始化聊天历史记录
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 获取用户输入的标签
user_input = st.text_input("输入标签：", key="input")

# 当用户输入标签时，生成 YouTube 视频推荐
if user_input:
    st.session_state['chat_history'].append({"role": "user", "content": user_input})
    try:
        # 假设模型理解根据标签推荐 YouTube 影片的任务
        prompt = f"根据以下标签推荐三个 YouTube 影片，只显示标题和链接，不需要详细说明：{user_input}"
        response = client.Completion.create(
            model="text-davinci-002",  # 使用一个适合文本生成的模型
            prompt=prompt,
            max_tokens=150
        )
        st.session_state['chat_history'].append({"role": "assistant", "content": response['choices'][0]['text']})
    except Exception as e:
        st.error(f"发生错误：{str(e)}")

# 显示聊天历史记录和推荐结果
for message in st.session_state['chat_history']:
    role = "你" if message["role"] == "user" else "ChatGPT"
    st.write(f"{role}: {message['content']}")
