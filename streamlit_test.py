import streamlit as st
import openai
import os
import asyncio

# 设置 OpenAI API 金钥
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# 初始化 OpenAI 客户端
openai.api_key = api_key

st.title("ChatGPT 对话功能")
st.write("与 ChatGPT 进行对话。")

# 初始化聊天历史记录
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 获取用户输入
user_input = st.text_input("你：", key="input")

# 定义异步函数进行消息流处理
async def get_response(messages):
    client = openai.OpenAI()
    stream = client.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
    )
    response = ""
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.get('content'):
            response += delta['content']
            st.write(delta['content'], end="")
    return response

# 当用户输入新消息时，将其添加到聊天历史记录中并获取模型的响应
if user_input:
    st.session_state['chat_history'].append({"role": "user", "content": user_input})
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        assistant_message = loop.run_until_complete(get_response(st.session_state['chat_history']))
        st.session_state['chat_history'].append({"role": "assistant", "content": assistant_message})
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# 显示聊天历史记录
for message in st.session_state['chat_history']:
    role = "你" if message["role"] == "user" else "ChatGPT"
    st.write(f"{role}: {message['content']}")
