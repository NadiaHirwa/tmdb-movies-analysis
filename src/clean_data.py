import json
import pandas as pd
import numpy as np

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

# Handling Missing & Incorrect Data

print(df[["budget", "id", "popularity", "release_date"]].dtypes)

df["budget"] = pd.to_numeric(df["budget"], errors="coerce")
df["id"] = pd.to_numeric(df["id"], errors="coerce")
df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce")

print(df[["budget", "id", "popularity"]].dtypes)

df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
print(df["release_date"].dtype)
print(df["release_date"].head())

# Replace unrealistic values

df["budget"] = df["budget"].replace(0, np.nan)
df["revenue"] = df["revenue"].replace(0, np.nan)
df["runtime"] = df["runtime"].replace(0, np.nan)

print(df[["budget", "revenue", "runtime"]].isnull().sum())

df["budget_musd"] = df["budget"] / 1_000_000
df["revenue_musd"] = df["revenue"] / 1_000_000

print(df[["budget_musd", "revenue_musd"]].head())

print(df["vote_count"].describe())
print((df["vote_count"] == 0).sum())

print(df["overview"].isnull().sum())
print(df["tagline"].isnull().sum())
print(df[["overview", "tagline"]].head())

print(df[df["overview"] == "No Data"])
print(df[df["tagline"] == "No Data"])

df["overview"] = df["overview"].replace("No Data", np.nan)
df["tagline"] = df["tagline"].replace("No Data", np.nan)

# Remove duplicates and drop rows with unknown 'id' or 'title'
print(df["id"].duplicated().sum())

print(df["id"].isnull().sum())
print(df["title"].isnull().sum())

# Keep only rows where at least 10 columns have non-NaN values
print(df.notnull().sum(axis=1))
df = df[df.notnull().sum(axis=1) >= 10]
print(df.shape)

# Filter to include only 'Released' movies, then drop 'status'
print(df["status"].value_counts())
df = df[df["status"] == "Released"]
df = df.drop(columns=["status"])
print(df.shape)