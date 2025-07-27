from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from agents.tools import fetch_weather, fetch_moon_phase, fetch_sky_events, fetch_satellite_passes
import os
from dotenv import load_dotenv
from langchain.schema.messages import SystemMessage
from agents.prompt import SYSTEM_PROMPT
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
import streamlit as st

load_dotenv(override=True)


# Retrive OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


# Define the Agent creation function
def create_sky_agent():
    """Create the sky agent with Streamlit-integrated memory"""
    
    try:
        system_prompt = SystemMessage(content=SYSTEM_PROMPT)
        
        # Use StreamlitChatMessageHistory for proper integration
        message_history = StreamlitChatMessageHistory(key="langchain_messages")
        
        memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            chat_memory=message_history,
            return_messages=True,
            k=10  # Keep last 10 turns
        )

        tools = [fetch_weather, fetch_moon_phase, fetch_sky_events, fetch_satellite_passes]
        
        llm = ChatOpenAI(
            model="gpt-4", 
            temperature=0.7, 
            openai_api_key=OPENAI_API_KEY,
            request_timeout=60,
            max_retries=2
        )

        # Agent and executor
        agent = OpenAIFunctionsAgent.from_llm_and_tools(
            llm=llm,
            tools=tools,
            system_message=system_prompt,
        )

        sky_agent = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=tools,
            memory=memory,
            verbose=True,
            handle_parsing_errors=True
        )
        
        return sky_agent
        
    except Exception as e:
        st.error(f"Failed to create agent: {str(e)}")
        return None