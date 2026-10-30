

import os
from tools import news_tools
from tools.news_tools import web_search_tool
from tools.financial_tools import get_balance_sheet, compute_key_ratios
from strands import Agent
from strands.models.openai import OpenAIModel
from agents.system_prompts import RISK_SYSTEM_PROMPT


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

risk_agent = Agent(
    name="Risk Agent",
    description="Agent to analyze the risk of news headlines",
    model=model,
    system_prompt=RISK_SYSTEM_PROMPT,
    tools=[news_tools, get_balance_sheet, compute_key_ratios],
    callback_handler=None
)