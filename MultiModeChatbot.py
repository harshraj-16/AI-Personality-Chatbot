from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

model = ChatMistralAI(
    model="mistral-medium-3-5",
    temperature=0.9
)

st.title("AI Personality Chatbot")

choice = st.selectbox(
    "Choose AI Personality",
    ["Angry", "Funny", "Sad"]
)

if choice == "Angry":
    mode = "You are an angry AI agent. You respond aggressively and impatiently"

elif choice == "Funny":
    mode = "You are a very funny AI agent. You respond with humor and jokes."

elif choice == "Sad":
    mode = "You are a very sad AI agent. You respond in a depressed and emotional tone."

# Initialize current mode
if "current_mode" not in st.session_state:
    st.session_state.current_mode = choice

# Reset chat when mode changes
if st.session_state.current_mode != choice:
    st.session_state.current_mode = choice
    st.session_state.messages = [
        SystemMessage(content=mode)
    ]
    st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content=mode)
    ]

# Display chat messages
for msg in st.session_state.messages:

    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)

    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

# Chat input at bottom
prompt = st.chat_input("Type your message...")

if prompt:

    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    response = model.invoke(
        st.session_state.messages
    )

    st.session_state.messages.append(
        AIMessage(content=response.content)
    )

    st.rerun()
