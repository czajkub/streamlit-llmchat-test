import asyncio
import time

import streamlit as st

from app.agent import AgentManager

agent_manager = AgentManager()


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
