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

# Look at the credits structure first
print(df["credits"].iloc[0].keys())
print(df["credits"].iloc[0]["cast"][0])

# Extract cast names, sorted by billing order


def get_cast_names(credits_cell):
    cast_list = credits_cell["cast"]
    sorted_cast = sorted(cast_list, key=lambda person: person["order"])
    names = [person["name"] for person in sorted_cast]
    return "|".join(names)


df["cast"] = df["credits"].apply(get_cast_names)
print(df["cast"].head())

# cast_size — how many total cast members
df["cast_size"] = df["credits"].apply(lambda c: len(c["cast"]))
print(df["cast_size"].head())

# director — search the whole crew list, don't assume position


def get_director(credits_cell):
    crew_list = credits_cell["crew"]
    directors = [person["name"] for person in crew_list if person["job"] == "Director"]
    return "|".join(sorted(directors))


df["director"] = df["credits"].apply(get_director)
print(df["director"].head())

# crew_size
df["crew_size"] = df["credits"].apply(lambda c: len(c["crew"]))
print(df["crew_size"].head())

#  Drop the original credits column
df = df.drop(columns=["credits"])
print(df.shape)

# Reorder columns
final_columns = ['id', 'title', 'tagline', 'release_date', 'genres', 'belongs_to_collection',
 'original_language', 'budget_musd', 'revenue_musd', 'production_companies',
 'production_countries', 'vote_count', 'vote_average', 'popularity', 'runtime',
 'overview', 'spoken_languages', 'poster_path', 'cast', 'cast_size', 'director', 'crew_size']

df = df[final_columns]
print(df.shape)
print(df.columns.tolist())

# Reset index
df = df.reset_index(drop=True)
print(df.index)

# Save the cleaned DataFrame
df.to_csv("data/processed/movies_clean.csv", index=False)
print("Saved to data/processed/movies_clean.csv")