
import os
from agents.system_prompts import FINANCIAL_DATA_SYSTEM_PROMPT
from tools.financial_tools import compute_key_ratios, get_balance_sheet, get_cash_flow_statement, get_income_statement
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

financial_agent = Agent(
    name = "Financial Data Agent",
    description = "Agent to fetch and analyze financial data for companies",
    model = model,
        system_prompt=FINANCIAL_DATA_SYSTEM_PROMPT,
    tools = [
        get_income_statement,
        get_balance_sheet,
        get_cash_flow_statement,
        compute_key_ratios
    ],
    callback_handler=None
)