

import os
from strands import Agent
from strands.models.openai import OpenAIModel
from agents.system_prompts import REPORT_WRITER_SYSTEM_PROMPT


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

report_writer_agent = Agent(
    name="Report Writer Agent",
    description="Agent to write financial analysis reports",
    model=model,
    system_prompt=REPORT_WRITER_SYSTEM_PROMPT,
    tools=[],
    callback_handler=None
)