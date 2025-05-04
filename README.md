# FilmExpandAPI
Python script that automatically enriches a local movie archive with IMDb data (rating, actors, votes) using the OMDb API and exports the results to XML and CSV.

## Features

- Fetch IMDb rating, vote count, and main actors for each movie title.
- Optional support for specifying the release year to improve lookup accuracy.
- Handles missing or incomplete data gracefully.
- Creates enriched XML and CSV outputs.
- Generates a "Top 10 Movies" list based on IMDb ratings.

---

## Input Format

The script expects a `movies.csv` file with at least the following column:

- `title` — the movie title  
- Optionally: `release_year`

Example:

```csv
title,release_year
Inception,2010
The Matrix,1999
