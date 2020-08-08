import os
import datetime

BASE_DIR: str = os.path.dirname(__file__)
log_dir: str = os.path.join(BASE_DIR, "logs")
os.makedirs(log_dir, exist_ok=True)


def trigger_log_save():
    """
    Saves a log file each time our web hook
    is triggered to re-run the web scraper.
    """
    filename: str = f"{datetime.datetime.now()}.txt"
    filepath: str = os.path.join(log_dir, filename)
    with open(filepath, "w+") as f:
        f.write("")
