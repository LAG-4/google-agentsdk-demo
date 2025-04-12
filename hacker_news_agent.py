import json
import httpx
import os
from agents import Agent, Runner, function_tool
from agents.models import GroqResponsesModel

@function_tool
def get_top_hackernews_stories(num_stories: int = 10) -> str:
    """
    Get top stories from Hacker News.

    Args:
        num_stories (int): Number of stories to return. Defaults to 10.

    Returns:
        str: JSON string of top stories.
    """
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

# Configure Groq model
groq_model = GroqResponsesModel(
    model="llama-3.3-70b-versatile",
    api_key=os.environ.get("GROQ_API_KEY")
)

# Create an agent with the function tool and Groq model
agent = Agent(
    name="Hacker News Assistant",
    instructions="You are a helpful assistant that can fetch top stories from Hacker News. When asked about news or tech stories, use the get_top_hackernews_stories function to retrieve information.",
    tools=[get_top_hackernews_stories],
    model=groq_model,
)

# Example of how to run the agent
if __name__ == "__main__":
    # Run the agent synchronously with a user query
    result = Runner.run_sync(agent, "What are the top stories on Hacker News right now?")
    print(result.final_output)

    # Alternatively, run asynchronously
    # import asyncio
    # async def main():
    #     result = await Runner.run(agent, "What are the top stories on Hacker News right now?")
    #     print(result.final_output)
    # asyncio.run(main()) 