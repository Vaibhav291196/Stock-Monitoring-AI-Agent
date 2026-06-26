from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from agents import graph
from storage import WATCHLIST, REPORTS

scheduler = BackgroundScheduler()

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


def daily_monitor():

    for batch in batch_watchlist(WATCHLIST, 2):

        with ThreadPoolExecutor(max_workers=2) as executor:

            reports = executor.map(
                analyze_company,
                batch
            )

            REPORTS.extend(reports)

scheduler.add_job(
    daily_monitor,
    "interval",
    days=1
)
