import json
import pandas as pd

with open("data/raw/movies_raw.json", "r", encoding="utf-8") as f:
    movies = json.load(f)

df = pd.DataFrame(movies)
print(df.shape)

columns_to_drop = ['adult', 'imdb_id', 'original_title', 'video', 'homepage']
df = df.drop(columns=columns_to_drop)
print(df.shape)

print(df["genres"].iloc[0])
print(df["belongs_to_collection"].iloc[0])


def get_collection_name(cell):
    if isinstance(cell, dict):
        return cell["name"]
    else:
        return None


df["belongs_to_collection"] = df["belongs_to_collection"].apply(get_collection_name)
print(df["belongs_to_collection"].head())


def get_names(cell):
    if isinstance(cell, list):
        names = [item["name"] for item in cell if item["name"]]
        return "|".join(sorted(names))
    else:
        return None


df["genres"] = df["genres"].apply(get_names)
print(df["genres"].head())

df["spoken_languages"] = df["spoken_languages"].apply(get_names)
print(df["spoken_languages"].head())

df["production_countries"] = df["production_countries"].apply(get_names)
print(df["production_countries"].head())

df["production_companies"] = df["production_companies"].apply(get_names)
print(df["production_companies"].head())

print(df["spoken_languages"].value_counts())

print(df["genres"].value_counts())
print(df["production_countries"].value_counts())
print(df["production_companies"].value_counts())