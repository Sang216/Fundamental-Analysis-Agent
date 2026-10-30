

import os

from strands import tool
from tavily import TavilyClient


def search_recent_news(symbol: str, max_results: int = 3) -> dict | str:
    """Search the web for recent news with Tavily and return the top 3 results.

    Args:
        symbol: Company symbol to search news for
        max_results: Maximum number of news results to return
    """
    try:
        client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
        return client.search(query=symbol, max_results=max_results, topic="news", time_range="month")
    except Exception as e:
        return f"Error searching news for {symbol}: {e}"


@tool
def web_search_tool(query: str) -> dict | str:
    """Search the web for recent news, risks and developments about a company.

    Args:
        query: What to search for (e.g. 'AAPL lawsuit regulatory risk')
    """
    return search_recent_news(query, max_results=3)


_finbert = None


def _get_finbert():
    """Load FinBERT lazily; returns None if transformers is not installed."""
    global _finbert
    if _finbert is None:
        try:
            from transformers import pipeline
            _finbert = pipeline("text-classification", model="ProsusAI/finbert")
        except ImportError:
            _finbert = False
    return _finbert or None


@tool
def analyze_sentiment(query: str) -> dict:
    """Analyze sentiment of the top 3 recent news articles.

    Args:
        query: Company name or ticker to search news for
    """
    news = search_recent_news(query, max_results=3)

    if not isinstance(news, dict):
        return {"news_sentiment": [], "error": str(news)}

    finbert = _get_finbert()
    results = []
    for article in news.get("results", [])[:3]:
        text = article.get("title", "")
        if not text:
            continue
        if finbert:
            prediction = finbert(text, truncation=True)[0]
            results.append({
                "title": text,
                "label": prediction["label"],
                "score": round(prediction["score"], 4)
            })
        else:
            # No FinBERT available: hand the headline + snippet to the LLM to judge.
            results.append({"title": text, "content": article.get("content", "")[:500]})

    return {"news_sentiment": results}
