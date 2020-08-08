import os
import typing as t
import pandas as pd
from fastapi import FastAPI

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)  # /17-data-pipeline
CACHE_DIR = os.path.join(BASE_DIR, "cache")
# print(os.path.abspath(__file__))  # .../main.py
# print(BASE_DIR)  # /Users.../17-data-pipeline-jupyter-pandas-fastapi
# print(CACHE_DIR)  # /Users/.../17-data-pipeline-jupyter-pandas-fastapi/cache
dataset = os.path.join(CACHE_DIR, "movies-box-office-dataset-cleaned.csv")

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/box-office")
def read_box_office_data():
    """
    Retrieve box office dataset using Pandas.
    """
    df = pd.read_csv(dataset)
    # Return a DICT of the Rank column in our CSV:
    # {'Rank': 7095, 'Release_Group': 'Rififi 2000 Re-release', 'Worldwide': 463593, 'Domesti
    # c': 460226, 'Domestic_%': 0.992737163848462, 'Foreign': 3367, 'Foreign_%': 0.007262836151538094, 'Year': 2000
    # , 'Filename': '2000.csv'}
    return df.to_dict("Rank")


# test_df = pd.read_csv(dataset)
# print(test_df.to_dict("Rank"))
# {'Rank': 7095, 'Release_Group': 'Rififi 2000 Re-release', 'Worldwide': 463593, 'Domesti
# c': 460226, 'Domestic_%': 0.992737163848462, 'Foreign': 3367, 'Foreign_%': 0.007262836151538094, 'Year': 2000
# , 'Filename': '2000.csv'}

# run.sh (chmod +x run.sh)
# uvicorn main:app --reload
# main: the file 'main.py' (the Python 'module')
# app: the objected created inside of main.py with the line app = FastAPI()
# --reload: make the server restart after code changes.
# NOTE: Need to ./run.sh from INSIDE /server directory
# Otherwise, need to modify to: server.main:app --reload
