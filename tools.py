import logging
import requests
import feedparser
from livekit.agents import function_tool, RunContext
import pyperclip
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_community.tools import DuckDuckGoSearchRun
import yfinance as yf

@function_tool
async def tell_news(context: RunContext, query: str) -> str:
    try:
        url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}"
        feed = feedparser.parse(url)

        if not feed.entries:
            return f"No news found for '{query}'."

        news = ""
        for i, entry in enumerate(feed.entries[:3]):
            news += f"{i+1}. {entry.title}\n{entry.link}\n\n"

        return f"Top news for **{query}**:\n\n{news.strip()}"

    except Exception as e:
        return f"Could not fetch news: {str(e)}"
@function_tool
async def search(context:RunContext,query:str)->str:
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"search result with {query}")
        return results
    except Exception as e:
        logging.error(f"errror searching the {query}")
        return f"an eroor occured while searching{query}"
@function_tool
async def get_news(context: RunContext, query: str) -> str:
    try:
        tool = YahooFinanceNewsTool()
        result = tool.run(tool_input=query)  # It's a synchronous call
        logging.info(f"The results for stock price for '{query}': {result}")
        return result
    except Exception as e:
        logging.error(f"Error occurred while searching '{query}': {str(e)}")
        return f"An error occurred while searching '{query}': {str(e)}"
@function_tool
async def get_stock_price(context: RunContext, query: str) -> str:
    try:
        ticker = yf.Ticker(query.upper())
        price = ticker.info.get("currentPrice")
        if price:
            response = f"The current stock price of {query.upper()} is {price} USD."
        else:
            response = f"Could not retrieve the stock price for {query.upper()}."
        logging.info(response)
        return response
    except Exception as e:
        logging.error(f"Error retrieving stock price for {query}: {str(e)}")
        return f"Error retrieving stock price for {query}: {str(e)}"
@function_tool
async def describe_clipboard(context: RunContext, query: str = "") -> str:
    try:
        clipboard_data = pyperclip.paste()

        if not clipboard_data.strip():
            return "The clipboard is empty."

        logging.info(f"Clipboard content retrieved: {clipboard_data[:100]}...")

        # You can modify this prompt to suit your use case
        return f"You copied this text:\n\n\"{clipboard_data}\"\n\nWould you like me to explain or summarize it?"

    except Exception as e:
        logging.error(f"Error accessing clipboard: {str(e)}")
        return "Failed to access clipboard."