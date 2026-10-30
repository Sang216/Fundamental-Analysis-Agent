
import math as Math

def _safe_float(value: float) -> float:
    """Convert a value to float safely."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0

def _millions(value: float) -> float:
    """Convert a Raw dollar value to millions. Example: 416161000000-> 416161.00"""
    if value is None or Math.isnan(value):
        return 0
    safe_float = _safe_float(value)
    return round(safe_float / 1_000_000, 2) if safe_float is not None else 0


def _extract_row(data, row, col):
    """Value of the rows should return in millions."""
    try:
        return _millions(data.at[row, col])
    except KeyError:
        return None


def _cache(tool_name: str, symbol: str) -> str:
    """Generate a cache key for a given tool and symbol."""
    return f"{tool_name}_{symbol}"