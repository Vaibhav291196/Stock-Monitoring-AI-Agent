# 📈 AI Stock Monitoring Multi-Agent System

An AI-powered **Multi-Agent Stock Monitoring System** built using **LangGraph**, **FastAPI**, and **Groq Llama 3.3**. The application automatically analyzes publicly traded companies by collecting real-time market data, financial metrics, debt information, and news sentiment to generate AI-driven investment reports.

---

## 🚀 Features

- Multi-Agent workflow using **LangGraph**
- Company search and ticker resolution
- Real-time stock data using **Yahoo Finance**
- Financial and debt analysis
- News retrieval using **Google News RSS**
- AI-powered sentiment analysis using **Groq Llama 3.3**
- AI-generated **BUY / HOLD / SELL** recommendations
- FastAPI REST APIs
- Automatic monitoring using **APScheduler**
- Manual batch processing with **ThreadPoolExecutor**
- Professional reports in **Markdown** format

---

## 🏗️ System Architecture

```text
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
   Analyze Company                   Watchlist (Add/delete) 
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


```

---

## 🤖 Multi-Agent Workflow

### Company Agent
- Searches the company
- Resolves ticker symbol
- Retrieves company information

### Stock Agent
- Current price
- Market capitalization
- Trading volume
- 52-week high/low
- Previous close
- Last week's stock prices

### Financial Agent
- PE Ratio
- EPS
- Revenue Growth

### Debt Agent
- Debt-to-Equity Ratio
- Current Ratio
- Liquidity Analysis

### News Agent
- Retrieves latest company news
- Uses Google News RSS

### Sentiment Agent
- Uses Groq Llama 3.3
- Classifies news as:
  - Positive
  - Neutral
  - Negative

### Decision Agent
Generates a professional investment report including:

- Company Overview
- Market Position
- Stock Performance
- Financial Analysis
- Debt Risk Analysis
- News & Sentiment Analysis
- Risks
- Opportunities
- BUY / HOLD / SELL Recommendation
- Confidence Score
- AI-generated reasoning

---

## 📂 Project Structure

```text
stock_ai_agent/
│
├── app.py              # FastAPI APIs
├── agents.py           # LangGraph workflow
├── scheduler.py        # APScheduler jobs
├── storage.py          # Watchlist & reports

```

---

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|----------|----------------------------|----------------------------|
| POST | `/watchlist/{company}` | Add company to watchlist |
| DELETE | `/watchlist/{company}` | Remove company from watchlist |
| GET | `/reports` | View generated reports |

---

## 🛠️ Technology Stack

| Layer | Technology |
|--------|------------|
| Backend | FastAPI |
| Workflow | LangGraph |
| LLM | Groq Llama 3.3 |
| Financial Data | Yahoo Finance |
| News | Google News RSS |
| Scheduler | APScheduler |
| Parallel Processing | ThreadPoolExecutor |

---

## 🔮 Future Enhancements

- Technical Analysis Agent (RSI, MACD, Bollinger Bands)
- Competitor Analysis Agent
- Email / WhatsApp / Telegram notifications
- WebSocket-based real-time dashboard
- Retrieval-Augmented Generation (RAG)
- PostgreSQL support
- Redis caching
- Docker & Kubernetes deployment
- Multi-user authentication

---

