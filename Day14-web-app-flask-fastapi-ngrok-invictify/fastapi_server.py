from fastapi import FastAPI

from scrape import run as scraper
from logger import trigger_log_save


"""
NOTES:
    - With any API you want to return a DICT so can convert to JSON.
    - FastAPI meant to be an API so it returns JSON out-of-box.
    - Flask meant to be a web server so it returns HTML out-of-box.
    - chmod +x run_flask.sh
    - chmod +x run_fastapi.sh
    - Reverse Proxy is what Ngrok and Nginx both can do. Need to research.
    - Can remove __main__ call in scrape.py since we won't be running it
      by itself anymore. Using servers to run for us instead.
    - First use GET to test run scraper(). Then switch to POST for security.
      but you have to send a POST request to execute the endpoint. To do this,
      we created trigger.py module.
    - (Flask) Return r.text since server is set up to return HTML ("Done")
      instead of JSON. However, return a DICT and it returns JSON (FastAPI)
    - Webhooks - One program talking with another program and sending data.
    - Invictify is built on top of Celery (w/ Redis):
      Trigger <id: a38184a0-713d-417b-b2e7-e8894b21d74d> triggers http://a8a7ca3ccc62.ngrok.io/box-office-mojo-scraper every hour
    - Created logger.py for logging webhook history
    - MUST restart server after making changes (save logs)! No hot-reloading configured.
    - Could have it send emails on a schedule. Just change endpoint logic.
    - Ideally we set this up on a hosted server (instead of Ngrok)
"""
# Start server:  uvicorn fastapi_server:app
app = FastAPI()


@app.get("/")
def hello_world():
    return {"hello": "world"}


@app.get("/abc")
def abc_view():
    return {"data": [1, 2, 3]}


@app.post("/box-office-mojo-scraper")
def box_office_scraper_view():
    # Save the log file
    trigger_log_save()
    # Run the scaper for latest data refresh
    scraper()
    # return "Scrape complete! (FastAPI)" # Sending HTML (r.text)
    return {"data": "FastAPI data key"}  # Sending JSON (r.json())
