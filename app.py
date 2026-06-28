from fastapi import FastAPI
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from markdown import markdown
from scheduler import scheduler
from storage import REPORTS
from fastapi.responses import Response
from storage import WATCHLIST, REPORTS

# Initialize fast api
app = FastAPI()

# Addition of company to watchlist
@app.post("/watchlist/{company}")
def add_company(company: str):

    if company not in WATCHLIST:
        WATCHLIST.append(company)

        # Return success message to user and display new watchlist to user
        return {
            "status": "success",
            "message": f"{company} added to watchlist",
            "watchlist": WATCHLIST
        } 
    # Give warning if company name already exists
    return {
        "status": "warning",
        "message": f"{company} already exists",
        "watchlist": WATCHLIST
    }

# Removing company name from watchlist
@app.delete("/watchlist/{company}")
def remove_company(company: str):

    if company in WATCHLIST:

        WATCHLIST.remove(company)

        # Return sucess message and display new list to user
        return {
            "status": "success",
            "message": f"{company} removed from watchlist",
            "watchlist": WATCHLIST
        }

    # if company not found return error message
    return {
        "status": "error",
        "message": f"{company} not found",
        "watchlist": WATCHLIST
    }

# Returning generated report back to user by get command of fast api.
scheduler.start()
@app.get("/reports")
def reports():

    markdown = "\n\n".join(
        [r["report"] for r in REPORTS]
    )

    return Response(
        content=markdown,
        media_type="text/markdown"
    )

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
