
import json

from strands import tool

import yfinance as yf
from tools.helpers import _extract_row, _cache

# FINANCE_URL = "https://financialmodelingprep.com/stable"

# FINANCE_API_KEY = os.getenv("FINANCIAL_MODELING_PREP_API_KEY")


@tool
def get_income_statement(symbol: str) -> str:
    """Get the annual income statement for a company.

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'TSLA')

    Returns:
        A dictionary containing revenue, cost of revenue, gross profit, operating income, net income, and EBITDA.
        values should be in millions. Currency in USD.
    """

    _key = _cache.get("get_income_statement", symbol)                 # cache key
    if _key is not None:
        return _key
    
    try:
        # url = f"{FINANCE_URL}/income-statement?symbol={symbol}&apikey={FINANCE_API_KEY}"
        stock = yf.Ticker(symbol)
        data = stock.financials
        if data is None or data.empty:
            return json.dumps({"error": f"No income statement data available for {symbol}"})

        result: dict = {
            "symbol": symbol,
            "company_name": stock.info.get('longName', symbol),
            "currency": stock.info.get('financialCurrency', 'USD'),
            "unit": "millions",
            "annual_data": {}
        }

        for col in data.columns[:4]:
            year = col.year
            result["annual_data"][year] = {
                "revenue": _extract_row(data, 'revenue', col),
                "costOfRevenue": _extract_row(data, 'costOfRevenue', col),
                "grossProfit": _extract_row(data, 'grossProfit', col),
                "operatingIncome": _extract_row(data, 'operatingIncome', col),
                "netIncome": _extract_row(data, 'netIncome', col),
                "ebitda": _extract_row(data, 'ebitda', col)
            }
            output = json.dumps(result, indent=4, default=str)
            _cache.set("get_income_statement", symbol, output)
        return output
    except Exception as e:
        return json.dumps({"error": f"Error fetching income statement for {symbol}: {e}"})


@tool
def get_balance_sheet(symbol: str) -> str:
    """Get the balance sheet for a company.

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'TSLA')

    Returns:
        A dictionary containing total assets, total liabilities, and total equity.
        values should be in millions. Currency in USD.
    """
    try:
        # url = f"{FINANCE_URL}/balance-sheet-statement?symbol={symbol}&apikey={FINANCE_API_KEY}"
        stock = yf.Ticker(symbol)
        data = stock.balance_sheet
        if data is None or data.empty:
            return json.dumps({"error": f"No balance sheet data available for {symbol}"})

        result: dict = {
                    "symbol": symbol,
                    "company_name": stock.info.get('longName', symbol),
                    "currency": stock.info.get('financialCurrency', 'USD'),
                    "unit": "millions",
                    "annual_data": {}
                }

        for col in data.columns[:4]:
            year = col.year
            result["annual_data"][year] = {
                "total_assets": _extract_row(data, 'totalAssets', col),
                "total_liabilities": _extract_row(data, 'totalLiabilities', col),
                "total_equity": _extract_row(data, 'totalStockholdersEquity', col)
            }
        output = json.dumps(result, indent=4, default=str)
        _cache.set("get_balance_sheet", symbol, output)
        return output
    except Exception as e:
        return json.dumps({"error": f"Error fetching balance sheet for {symbol}: {e}"})


@tool
def get_cash_flow_statement(symbol: str) -> str:
    """Get the cash flow statement for a company.

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'TSLA')

    Returns:
        A formatted string containing the cash flow statement details or an error message.
    """

    _key = _cache.get("get_cash_flow_statement", symbol)                 # cache key
    if _key is not None:
        return _key
            
    try:
        # url = f"{FINANCE_URL}/cash-flow-statement?symbol={symbol}&apikey={FINANCE_API_KEY}"
        stock = yf.Ticker(symbol)
        data = stock.cashflow
        if data is None or data.empty:
            return f"No cash flow statement data available for {symbol}"

        result: dict = {
                    "symbol": symbol,
                    "company_name": stock.info.get('longName', symbol),
                    "currency": stock.info.get('financialCurrency', 'USD'),
                    "unit": "millions",
                    "annual_data": {}
                }

        for col in data.columns[:4]:
            year = col.year
            result["annual_data"][year] = {
                "Operating Cash Flow": _extract_row(data, 'operatingCashFlow', col),
                "Investing Cash Flow": _extract_row(data, 'investingCashFlow', col),
                "Financing Cash Flow": _extract_row(data, 'financingCashFlow', col),
                "Net Cash Flow": _extract_row(data, 'netCashFlow', col)
            }
        output = json.dumps(result, indent=4, default=str)
        _cache.set("get_cash_flow_statement", symbol, output)
        return output
    except Exception as e:
        return f"Error fetching cash flow statement for {symbol}: {e}"


@tool
def compute_key_ratios(symbol: str) -> str:
    """Compute key fundamental ratios for a company.
    Calculating valuation, profitability, liquidity, debt, growth, and dividend-related ratios for the company.

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'TSLA')

    Returns:
        A formatted string containing key financial ratios or an error message.
    """

    _key = _cache.get("compute_key_ratios", symbol)                 # cache key
    if _key is not None:
        return _key
    
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        if info is None or not info:
            return f"No fundamental data available for {symbol}"

        fields = {
        "valuation": [
            "trailingPE",
            "forwardPE",
            "priceToBook",
            "priceToSalesTrailing12Months",
            "enterpriseToEbitda",
            "pegRatio",
        ],
        "profitability": [
            "returnOnEquity",
            "returnOnAssets",
            "profitMargins",
            "operatingMargins",
            "grossMargins",
        ],
        "liquidity": [
            "currentRatio",
            "quickRatio",
        ],
        "debt": [
            "debtToEquity",
            "totalDebt",
            "totalCash",
        ],
        "growth": [
            "revenueGrowth",
            "earningsGrowth",
        ],
        "dividend_and_risk": [
            "dividendYield",
            "beta",
        ],
        "company_metrics": [
            "marketCap",
            "enterpriseValue",
        ],
        }

        result = {
            "ticker": symbol,
            "company_name": info.get("longName"),
            "fundamentals": {
                category: {
                    key: info.get(key)
                    for key in keys
                }
                for category, keys in fields.items()
            }
        }

        output = json.dumps(result, indent=4, default=str)
        _cache.set("compute_key_ratios", symbol, output)
        return output
           
    except Exception as e:
        return f"Error computing key ratios for {symbol}: {e}"