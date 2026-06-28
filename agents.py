import os
import yfinance as yf
import feedparser
from typing import TypedDict
from langgraph.graph import StateGraph
from langchain_groq import ChatGroq

# Initializing llama 3 model through groq.
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key="GROQ_KEY"  # Add groq api key here
)

# Defining agents and agent workflow
class AgentState(TypedDict):

    company:str

    ticker:str

    # Company agent
    company_info:dict

    # stock agent
    stock:dict

    # News agent
    news:list

    # finanace agent
    financials:dict

    # Debt agent
    debt:dict

    # Sentiment agent
    sentiment:str

    # Decision agent
    decision:str

# Company agent to get the company details from yahoo finance
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
        quotes[0]["shortname"], # Retrives companies short name from yahoo finance

        "exchange":
        quotes[0]["exchange"] # Retrieves stock exchange name from yahoo finance
    }

    return state

import yfinance as yf

# Stock agent to retrieve the details of company stock infromation from yahoo finance
def stock_agent(state):

    ticker = state["ticker"]

    stock = yf.Ticker(ticker)

    info = stock.info

    # Last 7 trading days
    history = stock.history(period="7d")

    week_close = []

    for date, row in history.iterrows():

        # weekly stock history 
        week_close.append({

            "date": date.strftime("%Y-%m-%d"),

            "open": round(row["Open"], 2),

            "high": round(row["High"], 2),

            "low": round(row["Low"], 2),

            "close": round(row["Close"], 2),

            "volume": int(row["Volume"])

        })

    # Company stock analysis current & historical.
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

# News agent to get company related news from google news
def news_agent(state):

    ticker = state["ticker"]

    feed = feedparser.parse(

        f"https://news.google.com/rss/search?q={ticker}" # google news to get the company news

    )

    headlines = [

        x.title

        for x in feed.entries[:10]

    ]

    state["news"] = headlines

    return state

# Financial agent to retrieve the publically available financial information about the company from yahoo finance
def financial_agent(state):

    info = yf.Ticker(
        state["ticker"]
    ).info

    state["financials"] = {
        # Price to earnings
        "PE":
        info.get("trailingPE"),
        
        # earnings per share
        "EPS":
        info.get("trailingEps"),

        # Revenue growth
        "RevenueGrowth":
        info.get("revenueGrowth")
    }

    return state

# Debt agent to retrieve debt details of company from yahoo finance
def debt_agent(state):

    info = yf.Ticker(
        state["ticker"]
    ).info

    state["debt"] = {
        # debt to equity in %
        "DebtToEquity":
        info.get("debtToEquity"),

        # Debt to equity ratio
        "CurrentRatio":
        info.get("currentRatio")
    }

    return state

# Sentiment agent to analyze companies recent news
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
    # Giving prompt to llm
    response = llm.invoke(prompt)

    state["sentiment"] = response.content

    return state

# Decision agent to generte detailed short report in markdown format
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

    # passing the outputs of all agents to llm to generate report
    response = llm.invoke(prompt)

    state["decision"] = response.content

    return state

# Creating workflow by using langgraph
workflow = StateGraph(AgentState)

# company node
workflow.add_node(
    "company",
    company_agent
)

# stock node
workflow.add_node(
    "stock",
    stock_agent
)

# news node
workflow.add_node(
    "news",
    news_agent
)

# Financial agent node
workflow.add_node(
    "financial",
    financial_agent
)

# Debt agent node
workflow.add_node(
    "debt",
    debt_agent
)

# sentiment agent node
workflow.add_node(
    "sentiment",
    sentiment_agent
)

# decision agent node
workflow.add_node(
    "decision",
    decision_agent
)

# Defining entry point of workflow
workflow.set_entry_point("company")

# Connecting all the agents.
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
