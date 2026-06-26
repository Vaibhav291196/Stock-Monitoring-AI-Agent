import os
import yfinance as yf
import feedparser

from typing import TypedDict

from langgraph.graph import StateGraph
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key="GROQ_KEY"
)

class AgentState(TypedDict):

    company:str

    ticker:str

    company_info:dict

    stock:dict

    news:list

    financials:dict

    debt:dict

    sentiment:str

    decision:str

def company_agent(state):

    company = state["company"]

    search = yf.Search(company)

    quotes = search.quotes

    if len(quotes) == 0:

        state["ticker"] = None

        return state

    state["ticker"] = quotes[0]["symbol"]

    state["company_info"] = {

        "name":
        quotes[0]["shortname"],

        "exchange":
        quotes[0]["exchange"]
    }

    return state

import yfinance as yf

def stock_agent(state):

    ticker = state["ticker"]

    stock = yf.Ticker(ticker)

    info = stock.info

    # Last 7 trading days
    history = stock.history(period="7d")

    week_close = []

    for date, row in history.iterrows():

        week_close.append({

            "date": date.strftime("%Y-%m-%d"),

            "open": round(row["Open"], 2),

            "high": round(row["High"], 2),

            "low": round(row["Low"], 2),

            "close": round(row["Close"], 2),

            "volume": int(row["Volume"])

        })

    state["stock"] = {

        # Current Price
        "current_price": info.get("currentPrice"),

        "previous_close": info.get("previousClose"),

        # Daily Range
        "day_high": info.get("dayHigh"),

        "day_low": info.get("dayLow"),

        # 52 Week Performance
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),

        "fifty_two_week_low": info.get("fiftyTwoWeekLow"),

        # Market Information
        "market_cap": info.get("marketCap"),

        "volume": info.get("volume"),

        "average_volume": info.get("averageVolume"),

        # Risk
        "beta": info.get("beta"),

        # Dividend
        "dividend_yield": info.get("dividendYield"),

        # Valuation
        "forward_pe": info.get("forwardPE"),

        "trailing_pe": info.get("trailingPE"),

        # Weekly History
        "last_week_prices": week_close

    }

    return state
def news_agent(state):

    ticker = state["ticker"]

    feed = feedparser.parse(

        f"https://news.google.com/rss/search?q={ticker}"

    )

    headlines = [

        x.title

        for x in feed.entries[:10]

    ]

    state["news"] = headlines

    return state

def news_agent(state):

    ticker = state["ticker"]

    feed = feedparser.parse(

        f"https://news.google.com/rss/search?q={ticker}"

    )

    headlines = [

        x.title

        for x in feed.entries[:10]

    ]

    state["news"] = headlines

    return state

def financial_agent(state):

    info = yf.Ticker(
        state["ticker"]
    ).info

    state["financials"] = {

        "PE":
        info.get("trailingPE"),

        "EPS":
        info.get("trailingEps"),

        "RevenueGrowth":
        info.get("revenueGrowth")
    }

    return state

def debt_agent(state):

    info = yf.Ticker(
        state["ticker"]
    ).info

    state["debt"] = {

        "DebtToEquity":
        info.get("debtToEquity"),

        "CurrentRatio":
        info.get("currentRatio")
    }

    return state

def sentiment_agent(state):

    prompt = f"""

    Analyze the sentiment
    of these headlines.

    {state['news']}

    Return:

    Positive
    Neutral
    Negative

    """

    response = llm.invoke(prompt)

    state["sentiment"] = response.content

    return state

def decision_agent(state):

    prompt = f"""
    Create a professional stock monitoring report
    in MARKDOWN format.

    Company:
    {state['company_info']}

    Stock:
    {state['stock']}

    Financials:
    {state['financials']}

    Debt:
    {state['debt']}

    News:
    {state['news']}

    Sentiment:
    {state['sentiment']}

    Include:

    # Company Overview

    # Market Position

    # Stock Performance

    # Financial Analysis

    # Debt Risk Analysis

    # News & Sentiment Analysis

    # Risks

    # Opportunities

    # Investment Recommendation

    Return:
    BUY / HOLD / SELL

    Confidence %

    Detailed reasoning.
    """

    response = llm.invoke(prompt)

    state["decision"] = response.content

    return state

workflow = StateGraph(AgentState)

workflow.add_node(
    "company",
    company_agent
)

workflow.add_node(
    "stock",
    stock_agent
)

workflow.add_node(
    "news",
    news_agent
)

workflow.add_node(
    "financial",
    financial_agent
)

workflow.add_node(
    "debt",
    debt_agent
)

workflow.add_node(
    "sentiment",
    sentiment_agent
)

workflow.add_node(
    "decision",
    decision_agent
)

workflow.set_entry_point("company")

workflow.add_edge(
    "company",
    "stock"
)

workflow.add_edge(
    "stock",
    "news"
)

workflow.add_edge(
    "news",
    "financial"
)

workflow.add_edge(
    "financial",
    "debt"
)

workflow.add_edge(
    "debt",
    "sentiment"
)

workflow.add_edge(
    "sentiment",
    "decision"
)

graph = workflow.compile()
