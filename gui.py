import streamlit as st

from app.agent import AgentManager

agent_manager = AgentManager()


st.title("ChatDziPiTi")

st.markdown(
    """
    This is definitely chatgpt. pleasee chat with me
    """,
)


async def runner():
    await agent_manager.initialize()

    while True:
        user_input = st.text_input("Ask something!")
        response = await agent_manager.handle_message(user_input, verbose=True)
        st.write(response)

