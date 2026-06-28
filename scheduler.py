from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from agents import graph
from storage import WATCHLIST, REPORTS

scheduler = BackgroundScheduler()

# Gruping the companies in batches.
def batch_watchlist(watchlist, batch_size):

    for i in range(0, len(watchlist), batch_size):

        yield watchlist[i:i + batch_size]


def analyze_company(company):

    result = graph.invoke({

        "company": company

    })

    return {

        "company": company,

        "report": result["decision"]

    }

# Setting scheduler to define how many times agent will run and generate reports of companies in watchlist.
def daily_monitor():

    for batch in batch_watchlist(WATCHLIST, 2): # batch size of 2

        with ThreadPoolExecutor(max_workers=2) as executor: # threadpoolexecutor for efficient agent execution

            reports = executor.map(
                analyze_company,
                batch
            )

            REPORTS.extend(reports)

# Setting agent to run once every day
scheduler.add_job(
    daily_monitor,
    "interval",
    days=1
)
