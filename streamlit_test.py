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
            response = client.chat.completions.create(
                model="gpt-4o",  # Use an appropriate model for text generation
                messages=[{"role": "system", "content": "你是影片搜尋助手,以繁體中文回答,請根據提供的標籤推薦youtube影片,僅顯示標題和連結,不要用記錄呈現的文字回答"},
                          {"role": "user", "content": prompt}]
            )
            assistant_message = response.choices[0].text  # Accessing the text directly
            st.session_state['chat_history'].append({"role": "assistant", "content": assistant_message})
        except Exception as e:
            st.error(f"发生错误：{str(e)}")

    # Display chat history and results
    for message in st.session_state['chat_history']:
        role = "你" if message["role"] == "user" else "ChatGPT"
        st.write(f"{role}: {message['content']}")
