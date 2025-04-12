from __future__ import annotations
import json
import httpx
import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import streamlit as st

load_dotenv()

from agents import (
    Agent,
    Model,
    ModelProvider,
    OpenAIChatCompletionsModel,
    RunConfig,
    Runner,
    function_tool,
    set_tracing_disabled,
)

# App title and configuration
st.set_page_config(page_title="Hacker News Assistant", page_icon="📰")
st.title("Hacker News Assistant")

# Environment variable handling - make it more user-friendly
BASE_URL = os.getenv("BASE_URL") or st.secrets.get("BASE_URL", "") 
API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME") or st.secrets.get("MODEL_NAME", "")

# Allow users to input API details via the UI if not set in environment
with st.sidebar:
    st.header("API Configuration")
    
    if not BASE_URL:
        BASE_URL = st.text_input("API Base URL (e.g., https://api.groq.com/openai/v1)", key="base_url")
    else:
        st.success("✅ Base URL configured")
        
    if not API_KEY:
        API_KEY = st.text_input("API Key", type="password", key="api_key")
    else:
        st.success("✅ API Key configured")
        
    if not MODEL_NAME:
        MODEL_NAME = st.text_input("Model Name (e.g., llama-3.3-70b-versatile)", key="model_name")
    else:
        st.success("✅ Model configured")
    
    st.markdown("---")
    st.markdown("### About")
    st.info("This app uses a custom LLM provider to interact with Hacker News data.")

# Check if required configuration is provided
missing_config = []
if not BASE_URL:
    missing_config.append("Base URL")
if not API_KEY:
    missing_config.append("API Key")
if not MODEL_NAME:
    missing_config.append("Model Name")

if missing_config:
    missing_str = ", ".join(missing_config)
    st.warning(f"Please provide the missing configuration: {missing_str}")
else:
    # Configure the client and disable tracing
    client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
    set_tracing_disabled(disabled=True)

    class CustomModelProvider(ModelProvider):
        def get_model(self, model_name: str | None) -> Model:
            return OpenAIChatCompletionsModel(model=model_name or MODEL_NAME, openai_client=client)

    CUSTOM_MODEL_PROVIDER = CustomModelProvider()

    @function_tool
    def get_top_hackernews_stories(num_stories: int = 10) -> str:
        """
        Get top stories from Hacker News.

        Args:
            num_stories (int): Number of stories to return. Defaults to 10.

        Returns:
            str: JSON string of top stories.
        """
        with st.spinner("Fetching Hacker News stories..."):
            # Fetch top story IDs
            response = httpx.get('https://hacker-news.firebaseio.com/v0/topstories.json')
            story_ids = response.json()

            # Fetch story details
            stories = []
            for story_id in story_ids[:num_stories]:
                story_response = httpx.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json')
                story = story_response.json()
                if "text" in story:
                    story.pop("text", None)
                stories.append(story)
            return json.dumps(stories)

    # Create the agent
    agent = Agent(
        name="Hacker News Report Assistant", 
        instructions="You are a helpful news assistant who will answer users questions and provide the latest news on Hacker News.", 
        tools=[get_top_hackernews_stories]
    )

    # Initialize or get the chat history from session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get user input
    if prompt := st.chat_input("Ask about Hacker News..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Run the agent asynchronously
            async def run_agent():
                result = await Runner.run(
                    agent,
                    prompt,
                    run_config=RunConfig(model_provider=CUSTOM_MODEL_PROVIDER),
                )
                return result.final_output
            
            # Use asyncio to run the agent
            full_response = asyncio.run(run_agent())
            
            # Display the response
            message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
