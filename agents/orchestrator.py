
import os

from strands import Agent
from strands.models.openai import OpenAIModel
from agents.system_prompts import ORCHESTRATOR_SYSTEM_PROMPT

from agents.financial_data_agent import financial_agent
from agents.news_sentiment_agent import news_agent
from agents.report_writer_agent import report_writer_agent
from agents.risk_agent import risk_agent
from agents.valuation_agent import valuation_agent


# --------------------------------------------------
# 1. Configure the LLM
# --------------------------------------------------

model = OpenAIModel(
    client_args={
        "api_key": os.environ["GROQ_API_KEY"],
        "base_url": "https://api.groq.com/openai/v1",
    },
    model_id="openai/gpt-oss-120b",
    params={
        "temperature": 0.1,
        "extra_body": {
            "include_reasoning": False
        },
    },
)


# --------------------------------------------------
# 2. Define the Orchestrator
# --------------------------------------------------

orchestrator = Agent(
    name="Financial Analysis Orchestrator",
    model=model,

    system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,

    tools=[
        financial_agent.as_tool(
            name="financial_data_agent"
        ),

        # news_agent.as_tool(
        #     name="news_sentiment_agent"
        # ),

        # risk_agent.as_tool(
        #     name="risk_agent"
        # ),

        # valuation_agent.as_tool(
        #     name="valuation_agent"
        # ),

        # report_writer_agent.as_tool(
        #     name="report_writer_agent"
        # ),
    ],
)
