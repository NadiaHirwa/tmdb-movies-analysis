# TMDB Movie Data Analysis

A data pipeline that fetches movie data from the TMDb API, cleans and transforms it with Pandas, calculates business KPIs, and visualizes key trends — built as part of a Data Engineering apprenticeship project.

## Project Structure

```
src/fetch_data.py       # Fetches raw movie data from the TMDb API
src/clean_data.py       # Cleans and transforms the raw data
analysis.ipynb          # KPI analysis and visualizations
data/raw/                # Raw API output (not tracked in git)
data/processed/          # Cleaned dataset (not tracked in git)
```

## How to Run

1. Clone this repo
2. Create a `.env` file (see `.env.example`) with your own TMDb API key
3. `pip install -r requirements.txt`
4. Run `python src/fetch_data.py` to fetch raw data
5. Run `python src/clean_data.py` to clean it
6. Open `analysis.ipynb` to explore the analysis and visualizations

## Methodology

**Data Extraction:** Fetched 19 movie IDs from the TMDb API, using `append_to_response=credits` to retrieve cast/crew data in the same request as movie details. One ID (`0`) was invalid and correctly excluded, leaving 18 movies.

**Data Cleaning:** Dropped irrelevant columns, extracted nested JSON fields (genres, collection, languages, countries, companies, cast, director) into flat pipe-separated strings, converted data types (numeric fields, datetime), replaced placeholder/zero values with NaN where appropriate, removed duplicates, and filtered to released movies only. Two real data quality issues were identified and fixed during this process: inconsistent ordering of multi-value fields (e.g., "Action|Adventure" vs "Adventure|Action" being treated as different categories) and empty-string entries producing malformed pipe-separated output.

**KPI Analysis:** Built a reusable ranking function (`rank_movies()`) to identify top/bottom performers across revenue, budget, profit, ROI, votes, and ratings. Performed text-based search queries, and compared franchise vs. standalone movie performance and franchise/director success using groupby aggregation.

**Visualization:** Created 5 charts (Revenue vs. Budget, ROI by Genre, Popularity vs. Rating, Yearly Box Office Trends, Franchise vs. Standalone comparison) using Matplotlib.

## Key Insights

- Budget and revenue show only a loose positive relationship — some lower-budget films (e.g., Avatar) outperformed higher-budget films on a per-dollar basis, suggesting factors beyond spend (franchise strength, timing, audience appeal) drive returns.
- ROI varies significantly by genre, though several genres in this dataset are represented by only 1-2 movies, limiting how generalizable these patterns are.
- Popularity and rating show a loose positive relationship, but are not strictly correlated — popularity likely reflects recency and franchise visibility as much as audience-perceived quality.
- Standalone movies outperformed franchise movies on revenue, ROI, popularity, and rating in this dataset — however, this is based on only 2 standalone movies vs. 16 franchise movies, and should not be read as a general claim about franchises vs. standalone films.
- The Avengers Collection leads in total franchise revenue; James Cameron leads among directors by total revenue (Titanic + Avatar).
- Two of the brief's specified search queries (Bruce Willis films, Uma Thurman/Tarantino films) returned no results — verified as correct, since neither actor/director appears in this project's fixed 19-movie dataset.

## Limitations

This analysis is based on a small, fixed set of 18 major blockbuster films specified by the project brief. Findings around genre, franchise vs. standalone performance, and yearly trends should be read as illustrative of the method rather than generalizable conclusions, given the limited and non-random sample.

## Tools

Python, Pandas, NumPy, Matplotlib, Requests, python-dotenv, Jupyter. Data pipeline scripts run in a standard pip-managed Python environment; the analysis notebook was developed and run using Anaconda's Jupyter Notebook.