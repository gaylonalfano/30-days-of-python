from flask import Flask
from scrape import run as scraper
from logger import trigger_log_save

# Start server command:  gunicorn flask_server:app
app = Flask(__name__)


# http://localhost:8000/
@app.route("/", methods=["GET"])
def hello_world():
    return "Hello, world. This is FLASK."


# http://localhost:8000/abc
@app.route("/abc", methods=["GET"])
def abc_view():
    return "This is the /abc route"


# http://localhost:8000/box-office-mojo-scraper
# Can leave as "GET" to test locally real quick before "POST"
@app.route("/box-office-mojo-scraper", methods=["POST"])
def box_office_scraper():
    # Save log file
    trigger_log_save()
    # Run scraper for latest data refresh
    scraper()
    # return "Scrape complete (Flask)!" # returns HTML/text (r.text)
    return {"data": "Flask data key"}  # returns JSON (r.json())
