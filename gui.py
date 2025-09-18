import asyncio
import os
import time

import nest_asyncio
import streamlit as st

from app.agent import AgentManager

nest_asyncio.apply()

os.environ["API_KEY"] = st.secrets["API_KEY"]

agent_manager = AgentManager()
if os.environ.get("API_KEY") is None:
    st.markdown("Please provide an API key to continue...")

st.image("cat.jpg", width=100)
st.title("ChatDżiPiTi")

st.markdown(
    """
    ### Welcome to chatMCP. In this chat, you can:
      - query your apple-health data
      - talk to your new imaginary best friend
    """,
)

st.divider()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "human", "text": prompt})
    with st.chat_message("human"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            if not agent_manager.is_initialized():
                asyncio.run(agent_manager.initialize())

            with st.spinner("running...", show_time=True):
                response = asyncio.run(agent_manager.handle_message(prompt))
        except ConnectionError:
            st.warning("Connection refused.")


        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.04)
            placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "text": full_response})
