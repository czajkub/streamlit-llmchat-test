import asyncio
import os
import time

import nest_asyncio
import streamlit as st

from app.agent import AgentManager

# nest_asyncio.apply()

os.environ["API_KEY"] = st.secrets["API_KEY"]

agent_manager = AgentManager()
if os.environ.get("API_KEY") is None:
    st.markdown("Please provide an API key to continue...")

st.title("ChatDziPiTi")

st.markdown(
    """
    This is definitely chatgpt. pleasee chat with me
    """,
)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "text": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        if not agent_manager.is_initialized():
            asyncio.run(agent_manager.initialize())
        response = asyncio.run(agent_manager.handle_message(prompt))

        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "text": full_response})
