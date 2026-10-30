

import json
import yfinance as yf
from strands import tool


def _dcf_verdict(upside: float) -> str:
    if upside >= 25:
        return "Potentially Undervalued"
    elif upside >= 10:
        return "Moderately Undervalued"
    elif upside >= -10:
        return "Fairly Valued"
    else:
        return "Potentially Overvalued"


def run_dcf_model(
    symbol: str,
    growth_rate: float,
    discount_rate: float,
    terminal_growth_rate: float
) -> str:
    """
    Estimate intrinsic value per share using a 5-year FCFF DCF model.
    """

    # Validate assumptions
    if not (0 <= growth_rate < 1):
        raise ValueError("Growth rate must be between 0 and 1.")

    if not (0 < terminal_growth_rate < discount_rate):
        raise ValueError(
            "Terminal growth must be positive and lower than discount rate."
        )

    stock = yf.Ticker(symbol)
    info = stock.info

    # Retrieve financial inputs
    current_fcf = info.get("freeCashflow")
    current_price = info.get("currentPrice") or info.get("regularMarketPrice")
    shares = info.get("sharesOutstanding")
    total_debt = info.get("totalDebt")
    total_cash = info.get("totalCash")

    if not all(v is not None and v > 0 for v in [
        current_fcf, current_price, shares
    ]):
        raise ValueError("Missing or invalid FCF, price, or shares data.")

    total_debt = total_debt or 0
    total_cash = total_cash or 0

    # Project and discount 5 years of FCF
    present_value = 0

    for year in range(1, 6):
        projected_fcf = current_fcf * (1 + growth_rate) ** year

        discounted_fcf = (
            projected_fcf / (1 + discount_rate) ** year
        )

        present_value += discounted_fcf

    # Calculate terminal value
    year_5_fcf = current_fcf * (1 + growth_rate) ** 5

    terminal_value = (
        year_5_fcf * (1 + terminal_growth_rate)
        / (discount_rate - terminal_growth_rate)
    )

    discounted_terminal_value = (
        terminal_value / (1 + discount_rate) ** 5
    )

    # Enterprise value
    enterprise_value = present_value + discounted_terminal_value

    # Convert enterprise value to equity value
    equity_value = enterprise_value + total_cash - total_debt

    # Intrinsic value per share
    intrinsic_value = equity_value / shares

    # Compare with market price
    upside = (
        (intrinsic_value - current_price) / current_price
    ) * 100

    result = {
        "symbol": symbol,
        "intrinsic_value": round(intrinsic_value, 2),
        "current_price": round(current_price, 2),
        "upside_pct": round(upside, 2),
        "verdict": _dcf_verdict(upside),
        "assumptions": {
            "growth_rate": growth_rate,
            "discount_rate": discount_rate,
            "terminal_growth_rate": terminal_growth_rate,
            "forecast_years": 5
        }
    }

    return json.dumps(result, indent=4)



@tool
def get_peer_multiples(peers_data: list[dict], multiple: str) -> list:
    """
    Get peer multiples for valuation.

    Args:
        peers_data: List of dictionaries containing peer company data.
        multiple: The multiple to extract (e.g., "EV/EBITDA", "P/E").

    Returns:
        List of multiples for the peer companies.
    """
    return [peer.get(multiple) for peer in peers_data if multiple in peer]
