"""Dummy tools that return random data until real retrieval tools exist.

Each tool sleeps for a random interval to stand in for the latency of a real
external call.
"""
import asyncio
import random

from langchain.tools import tool

_CONDITIONS = ["sunny", "cloudy", "rainy", "windy", "snowy"]


async def _simulate_latency() -> None:
    await asyncio.sleep(random.uniform(0.5, 2.0))


@tool(parse_docstring=True)
async def get_stock_price(ticker: str) -> dict:
    """Get the current price of a stock.

    Args:
        ticker: Stock ticker symbol, e.g. "AAPL".
    """
    await _simulate_latency()
    return {
        "ticker": ticker.upper(),
        "price": round(random.uniform(20, 900), 2),
        "currency": "USD",
    }


@tool(parse_docstring=True)
async def get_weather(city: str) -> dict:
    """Get the current weather in a city.

    Args:
        city: City name, e.g. "Zagreb".
    """
    await _simulate_latency()
    return {
        "city": city,
        "temperature_c": random.randint(-5, 35),
        "condition": random.choice(_CONDITIONS),
    }


TOOLS = [get_stock_price, get_weather]
