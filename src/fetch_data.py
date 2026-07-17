import os
import requests
from dotenv import load_dotenv
import pandas as pd
import json

load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

movie_id = [
    0, 299534, 19995, 140607, 299536, 597, 135397,
    420818, 24428, 168259, 99861, 284054, 12445,
    181808, 330457, 351286, 109445, 321612, 260513
]


def fetch_movie(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": api_key, "append_to_response": "credits"}
    response = requests.get(url, params=params)
    return response.json()


movies = []

for one_id in movie_id:
    data = fetch_movie(one_id)
    if data.get("title") is None:
        print(f"Skipping id={one_id}, no data found")
    else:
        movies.append(data)

print(f"Collected {len(movies)} movies")

df = pd.DataFrame(movies)
print(df.shape)
print(df.columns.tolist())

with open("data/raw/movies_raw.json", "w", encoding="utf-8") as f:
    json.dump(movies, f, indent=2)

print("Saved to data/raw/movies_raw.json")