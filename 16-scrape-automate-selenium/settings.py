import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
# print(load_dotenv())  # True

# # Or, explicitly provide path to '.env'
# from pathlib import Path

# env_path = Path(".") / ".env"
# load_dotenv(dotenv_path=env_path)

INSTA_USERNAME = os.getenv("INSTA_USERNAME")
INSTA_PASSWORD = os.getenv("INSTA_PASSWORD")
