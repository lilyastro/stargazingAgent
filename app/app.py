import streamlit as st
from agents.agent import create_sky_agent

st.set_page_config(page_title="Stargazing Chat", page_icon="🌌", layout="centered")
st.title("🌠 Stargazing Assistant")

# Initialize the agent
if "sky_agent" not in st.session_state:
    st.session_state.sky_agent = create_sky_agent()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
with st.container():
    for role, content in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(content)

# Input from user
user_input = st.chat_input("Ask about stargazing...")

if user_input:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))

    # Process with agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Create context from recent chat history
                context = ""
                if len(st.session_state.chat_history) > 1:
                    # Get last 6 messages (3 exchanges) for context
                    recent_history = st.session_state.chat_history[-7:-1]  # Exclude current user message
                    context = "Previous conversation:\n"
                    for role, content in recent_history:
                        context += f"{role}: {content}\n"
                    context += f"\nCurrent question: {user_input}"
                else:
                    context = user_input
                
                # Invoke agent with context
                result = st.session_state.sky_agent.invoke({"input": context})
                response = result["output"] if isinstance(result, dict) and "output" in result else str(result)
                st.markdown(response)
                st.session_state.chat_history.append(("assistant", response))
                
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.chat_history.append(("assistant", error_msg))

# Clear chat button
if st.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun()