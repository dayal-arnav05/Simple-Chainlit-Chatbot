import streamlit as st
import os
from openai import OpenAI

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Check if API key is available
if not api_key:
    st.error("Please set the OPENAI_API_KEY environment variable")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Set page config
st.set_page_config(page_title="ChatGPT", page_icon="🤖")
st.title("ChatGPT")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get ChatGPT response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.write(reply)
    
    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": reply})