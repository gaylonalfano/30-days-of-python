import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
# print(load_dotenv())  # True

# # Or, explicitly provide path to '.env'
# from pathlib import Path

# env_path = Path(".") / ".env"
# load_dotenv(dotenv_path=env_path)

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_SECRET = os.getenv("TWILIO_SECRET")
SEND_TO_NUMBER = os.getenv("SEND_TO_NUMBER")
SEND_FROM_NUMBER = os.getenv("SEND_FROM_NUMBER")
