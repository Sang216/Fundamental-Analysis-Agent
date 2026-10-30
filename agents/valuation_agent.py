

import os
from agents.system_prompts import VALUATION_SYSTEM_PROMPT
from strands import Agent

from tools.valuation_tools import get_peer_multiples, run_dcf_model
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

valuation_agent = Agent(
    name="Valuation Agent",
    description="Agent to evaluate financial models and assumptions",
    model=model,
    system_prompt=VALUATION_SYSTEM_PROMPT,
    tools=[run_dcf_model, get_peer_multiples],
    callback_handler=None
)