import streamlit as st
import openai
from openai import OpenAI

# 设置 OpenAI API 金钥
openai.api_key = st.secrets["openai_api_key"]

st.title("ChatGPT 对话功能")
st.write("与 ChatGPT 进行对话。")

# 初始化聊天历史记录
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 获取用户输入
user_input = st.text_input("你：", key="input")

# 测试调用
try:
    
    client = OpenAI()

    # 进行一次测试调用
    test_response = client.completions.create(
      model="gpt-3.5-turbo-instruct",
      prompt="Say this is a test",
      max_tokens=7,
      temperature=0
    )
    st.write(f"测试调用成功: {test_response}")
except ImportError:
    st.write("OpenAI 类不存在或导入错误。请确认是否正确安装和导入 OpenAI 库。")

# 当用户输入新消息时，将其添加到聊天历史记录中并获取模型的响应
if user_input:
    st.session_state['chat_history'].append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 使用最新的模型名称，如 "gpt-3.5-turbo"
        messages=st.session_state['chat_history']
    )
    st.session_state['chat_history'].append({"role": "assistant", "content": response.choices[0].message['content']})

# 显示聊天历史记录
for message in st.session_state['chat_history']:
    role = "你" if message["role"] == "user" else "ChatGPT"
    st.write(f"{role}: {message['content']}")
