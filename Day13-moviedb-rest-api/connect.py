import typing as t
import requests
import pprint
import pandas as pd
import settings


# # === API VERSION 3 ===
"""
Example GET request:
    https://api.themoviedb.org/3/movie/550?api_key=e2f2bdf71dd0c6d39da9f7508688ca1a
"""
# API_KEY = settings.API_KEY
# API_READ_ACCESS_TOKEN = settings.API_READ_ACCESS_TOKEN

# API_VERSION = 3
# movie_id = 500
# API_BASE_URL = f"https://api.themoviedb.org/{API_VERSION}"
# ENDPOINT_PATH = f"/movie/{movie_id}"
# ENDPOINT = f"{API_BASE_URL}{ENDPOINT_PATH}?api_key={API_KEY}"


# # r = requests.get(ENDPOINT, data={"api_key": API_KEY}) # 403 error
# # r = requests.get(ENDPOINT, json={"api_key": API_KEY})  # 403
# r = requests.get(ENDPOINT)  # 200
# print(r.status_code)
# print(r.text)


# # === API VERSION 4 (using Bearer tokens) ===
# """
# curl --request GET \
#   --url 'https://api.themoviedb.org/3/movie/76341' \
#   --header 'Authorization: Bearer <<access_token>>' \
#   --header 'Content-Type: application/json;charset=utf-8'
# """
# API_READ_ACCESS_TOKEN = settings.API_READ_ACCESS_TOKEN
# API_VERSION = 4
# movie_id = 501
# API_BASE_URL = f"https://api.themoviedb.org/{API_VERSION}"
# ENDPOINT_PATH = f"/movie/{movie_id}"
# ENDPOINT = f"{API_BASE_URL}{ENDPOINT_PATH}"
# HEADERS = {
#     "Authorization": f"Bearer {API_READ_ACCESS_TOKEN}",
#     "Content-Type": "application/json;charset=utf-8",
# }

# r = requests.get(ENDPOINT, headers=HEADERS)  # 200
# print(r.status_code)
# print(r.text)


# === API VERSION 3 (search for movies) ===
API_KEY = settings.API_KEY
API_VERSION = 3
API_BASE_URL = f"https://api.themoviedb.org/{API_VERSION}"
ENDPOINT_PATH = "/search/movie"
ENDPOINT = f"{API_BASE_URL}{ENDPOINT_PATH}?api_key={API_KEY}"


query = "The Matrix"
r = requests.get(ENDPOINT, params={"query": query})  # 200
# print(r.status_code)
# pprint.pprint(r.text)
# pprint.pprint(r.json())

if r.status_code in range(200, 299):
    data: t.Dict = r.json()
    results: t.List[t.Dict] = data["results"]

    if len(results) > 0:
        movie_ids: t.Set[str] = {result["id"] for result in results}
        movie_titles: t.List[str] = [result["title"] for result in results]
        # print(list(zip(movie_ids, movie_titles)))


# print(
#     data.keys()
# )  # dict_keys(['page', 'total_results', 'total_pages', 'results'])

# print(results)  # List[Dict]

# print(
#     results[0].keys()
# )  # dict_keys(['popularity', 'vote_count', 'video', 'poster_path', 'id', 'adult', 'backdrop_path', 'original_language', 'original_title', 'genre_ids', 'title', 'vote_average', 'overview', 'release_date'])

# print(results[0]["id"])
# print(movie_ids, movie_titles)  # {684428, 684431, 604, ...}
# print(len(movie_ids), len(movie_titles))  # 20 20
# print(list(zip(movie_ids, movie_titles)))


# === After retrieving the movie ids from query we can loop through movie_ids
output = "movies.csv"
movie_data: t.List = []
for movie_id in movie_ids:
    API_KEY = settings.API_KEY
    API_VERSION = 3
    API_BASE_URL = f"https://api.themoviedb.org/{API_VERSION}"
    ENDPOINT_PATH = f"/movie/{movie_id}"
    ENDPOINT = f"{API_BASE_URL}{ENDPOINT_PATH}?api_key={API_KEY}"

    r = requests.get(ENDPOINT)
    if r.status_code in range(200, 299):
        data: t.Dict = r.json()
        movie_data.append(data)

df: pd.DataFrame = pd.DataFrame(data=movie_data)
print(df.head())
df.to_csv(output, index=False)
