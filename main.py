import sys
from dotenv import load_dotenv

load_dotenv()  # must run before importing agents, which read GROQ_API_KEY at import time

from agents.orchestrator import orchestrator


def main(company: str):
    prompt = f"Perform a fundamental analysis of {company} and give a balanced recommendation."

    result = orchestrator(prompt)   # Strands agents are called like functions
    print(result)


if __name__ == "__main__":
    company = " ".join(sys.argv[1:]).strip() or input("Enter company name or ticker: ").strip()
    main(company)
