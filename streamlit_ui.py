import streamlit as st
from agent.graph import a as agent
from langchain_openai import ChatOpenAI
import asyncio


st.title("Chat with AI")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("Say something")

if user_input:
    # Append user input to history
    st.session_state.history.append((user_input, ""))  # Placeholder for AI response

    # Show the chat messages so far
    for human, ai in st.session_state.history[:-1]:
        with st.chat_message("user"):
            st.markdown(human)
        with st.chat_message("ai"):
            st.markdown(ai)

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("ai"):
        #response_container = st.empty()
        tool_log = st.expander("Tool Activity", expanded=False)
        answer_container = st.empty()
        

        # Stream response using astream_events
        async def stream_response():
            full_response = ""
            async for event in agent.stream_bot_response(user_input, st.session_state.history[:-1]):
                if 'Tool Called:' in event:
                    with tool_log:
                        st.markdown(event)
                else:
                    full_response += event
                    answer_container.markdown(full_response)
            return full_response

        # Run async code inside Streamlit
        full_response = asyncio.run(stream_response())

        # Update last message with full AI response
        st.session_state.history[-1] = (user_input, full_response)
