AI Stock Monitoring Multi-Agent System
System Design Document
________________________________________
1. Project Overview
Objective
The AI Stock Monitoring Multi-Agent System automatically analyzes publicly traded companies and generates AI-powered investment reports.
The system integrates:
•	FastAPI
•	LangGraph
•	Groq Llama 3.3 70B
•	Yahoo Finance
•	Google News RSS
•	APScheduler
The system continuously monitors companies in a watchlist and periodically generates professional stock analysis reports.
________________________________________
2. Overall System Architecture
                         User
                           │
                           │
                   HTTP REST Request
                           │
                           ▼
                    FastAPI Application
                           │
          ┌────────────────┴─────────────────┐
          │                                  │
          ▼                                  ▼
   Analyze Company API               Watchlist APIs
          │                                  │
          │                         
          │                                  │
          └────────────────┬─────────────────┘
                           │
                           ▼
                  LangGraph Workflow Engine
                           │
                           ▼
                     Company Agent
                           │
                           ▼
               ┌──────────┬───────────┬───────────┬
               │          │           │           │
               ▼          ▼           ▼           ▼
             Stock     Financial      Debt      News
             Agent       Agent        Agent     Agent
                                                  │
               |          |           |           ▼
               |          |           |      Sentiment Agent
               |          |           |           |
               │          │           │           │
               └──────────┴───────────┴───────────┘
                           │
                           ▼
                     Decision Agent
                           │
                           ▼
              Markdown Investment Report
                           │
                           ▼
                    FastAPI Response
________________________________________
3. Complete Workflow
User enters company name

        │

        ▼

FastAPI receives request

        │

        ▼

Company Agent

        │

        ▼

Find ticker

Find exchange

Find company information

        │

        ▼

═══════════════════════════════════════════════
      PARALLEL AGENT EXECUTION
═══════════════════════════════════════════════

      ┌──────────────┐
      │ Stock Agent  │
      └──────────────┘
             │
             ▼
Current Price
52 Week High
52 Week Low
Volume
Market Cap
Weekly Prices

──────────────────────────────────────────────

      ┌─────────────────┐
      │ Financial Agent │
      └─────────────────┘
             │
             ▼
PE Ratio
EPS
Revenue Growth

──────────────────────────────────────────────

      ┌─────────────┐
      │ Debt Agent  │
      └─────────────┘
             │
             ▼
Debt to Equity
Current Ratio
Liquidity

──────────────────────────────────────────────

      ┌─────────────┐
      │ News Agent  │
      └─────────────┘
             │
             ▼
Latest Headlines
Google News RSS

═══════════════════════════════════════════════

        │

        ▼

Sentiment Agent

        │

Analyzes all retrieved news

        │

Returns

Positive

Neutral

Negative

        │

        ▼

═══════════════════════════════════════

        Decision Agent

═══════════════════════════════════════

Receives

✓ Company Information

✓ Stock Information

✓ Financial Information

✓ Debt Information

✓ News Headlines

✓ Sentiment Analysis

↓

Groq Llama 3.3

↓

Professional Markdown Report

↓

BUY

HOLD

SELL

↓

Confidence Score

↓

Detailed Reasoning
________________________________________
4. Component Architecture
stock_ai_agent/

│

├── app.py
│
│   FastAPI REST APIs
│
│   • Analyze Company
│   • Watchlist APIs
│   • Reports APIs
│

├── agents.py
│
│   LangGraph Workflow
│
│   • Company Agent
│   • Stock Agent
│   • Financial Agent
│   • Debt Agent
│   • News Agent
│   • Sentiment Agent
│   • Decision Agent
│

├── scheduler.py
│
│   APScheduler
│
│   Daily Monitoring
│
│   Manual Batch Processing
│

├── storage.py
│
│   Watchlist
│
│   Reports
│

________________________________________
5. Agent Responsibilities
Company Agent
Purpose
•	Search company
•	Identify ticker
•	Exchange
•	Company information
Input
Apple
Output
AAPL

Apple Inc.

NASDAQ
________________________________________
Stock Agent
Collects
•	Current Price
•	Previous Close
•	Day High
•	Day Low
•	52 Week High
•	52 Week Low
•	Market Capitalization
•	Trading Volume
•	Average Volume
•	Dividend Yield
•	Beta
•	Weekly Closing Prices
________________________________________
Financial Agent
Collects
•	PE Ratio
•	EPS
•	Revenue Growth
________________________________________
Debt Agent
Collects
•	Debt to Equity
•	Current Ratio
•	Liquidity
________________________________________
News Agent
Collects
Latest news using
Google News RSS
Returns
Top 10 Headlines
________________________________________
Sentiment Agent
Uses
Groq Llama 3.3
Input
News Headlines
Output
Positive
Neutral
Negative
________________________________________
Decision Agent
Receives outputs from every previous agent.
Creates
•	Company Overview
•	Market Position
•	Financial Analysis
•	Debt Analysis
•	News Analysis
•	Opportunities
•	Risks
•	BUY/HOLD/SELL Recommendation
•	Confidence Score
•	Detailed Explanation
________________________________________
6. Parallel Agent Design
The Company Agent is the only mandatory first step because every other agent requires the ticker symbol.
After retrieving the ticker, the remaining retrieval agents work independently.
                Company Agent
                      │
                      ▼
               Company Details
                      │
                      ▼
     ┌──────────┬───────────┬───────────┬
     │          │           │           │
     ▼          ▼           ▼           ▼
  Stock     Financial      Debt        News
  Agent       Agent        Agent       Agent
                                        │
     |          |           |           ▼
     |          |           |      Sentiment Agent
     |          |           |           |
     │          │           │           │
     └──────────┴───────────┴───────────┘
                      
                      │
                      ▼
                Decision Agent
These agents do not depend on each other, making them ideal candidates for parallel execution.
________________________________________
7. Scheduler Design
The scheduler automatically analyzes companies in the watchlist.
APScheduler

      │

Runs every day

      │

Read Watchlist

      │

Manual Batch Creation

      │

───────────────

Batch 1

Apple

Microsoft

───────────────

Batch 2

Tesla

Nvidia

───────────────

      │

ThreadPoolExecutor

      │

Run LangGraph

      │

Generate Reports

      │

Store Reports

      │

FastAPI /reports
________________________________________
8. Manual Batch Handling
Instead of
Apple

↓

Microsoft

↓

Tesla

↓

Nvidia
The scheduler creates batches.
Batch Size = 2

↓

Apple
Microsoft

↓

Tesla
Nvidia
Each batch executes using
ThreadPoolExecutor
Benefits
•	Faster execution
•	Better scalability
•	Lower API latency
•	Controlled concurrenc
9. API Endpoints
Add Company
POST /watchlist/{company}
________________________________________
Remove Company
DELETE /watchlist/{company}
________________________________________
View Reports
GET /reports
________________________________________
11. Technology Stack
Layer	Technology
Backend	FastAPI
Workflow	LangGraph
LLM	Groq Llama 3.3 70B
Financial Data	Yahoo Finance
News	Google News RSS
Scheduler	APScheduler
Parallel Processing	ThreadPoolExecutor
________________________________________
12. Future Enhancements
•	Real parallel execution using LangGraph fan-out/fan-in.
•	Technical Analysis Agent (RSI, MACD, Bollinger Bands, Moving Averages).
•	Portfolio Management Agent.
•	Email and Telegram alert notifications.
•	WebSocket-based real-time dashboard updates.
•	PostgreSQL for production deployments.
•	Redis caching for market data and reports.
•	Historical report storage with vector databases for RAG-based querying.
•	Docker and Kubernetes deployment.
•	Multi-user authentication and role-based access control.
________________________________________
13. Conclusion
The AI Stock Monitoring Multi-Agent System follows a modular, extensible architecture where each agent specializes in a single responsibility. The Company Agent first resolves the company identity, after which the Stock, Financial, Debt, and News agents can execute in parallel to gather independent information. The Sentiment Agent analyzes the collected news, and finally the Decision Agent aggregates all outputs to produce a comprehensive Markdown investment report with a BUY, HOLD, or SELL recommendation.
This design supports scalable data retrieval, periodic monitoring through APScheduler, manual batch processing with ThreadPoolExecutor, and clean separation of responsibilities, making it well suited for future enhancements such as real-time alerts, technical analysis, portfolio management, and production deployment.

