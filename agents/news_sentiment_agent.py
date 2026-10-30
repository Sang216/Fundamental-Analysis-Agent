

import os
from agents.system_prompts import NEWS_SENTIMENT_SYSTEM_PROMPT
from tools.news_tools import analyze_sentiment
from strands import Agent
from strands.models.openai import OpenAIModel


model = OpenAIModel(
    client_args={
        "api_key": os.environ["GROQ_API_KEY"],
        "base_url": "https://api.groq.com/openai/v1",
    },
    model_id="openai/gpt-oss-120b",
    params={
        "temperature": 0.1,
        "extra_body": {"include_reasoning": False},  # Groq: skip reasoning blocks Strands can't replay
    },
)

news_agent = Agent(
    name="News Sentiment Agent",
    description="Agent to analyze the sentiment of news headlines",
    model=model,
    system_prompt=NEWS_SENTIMENT_SYSTEM_PROMPT,
    tools=[analyze_sentiment],
    callback_handler=None
)