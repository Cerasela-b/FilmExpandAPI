import requests
import pandas as pd
import time

API_KEY = 'b1bb4320'  
OMDB_URL = 'http://www.omdbapi.com/'

df = pd.read_csv('movies.csv')

df['imdb_rating'] = None
df['main_actors'] = None
df['imdb_nb_votes'] = None

def get_movie_data(title, year=None):
    params = {
        't': title,
        'apikey': API_KEY
    }
    if year:
        params['y'] = str(year)

    try:
        response = requests.get(OMDB_URL, params=params)
        data = response.json()

        if data.get("Response") == "False":
            print(f"[WARN] {data.get('Error')} for title: {title}")
            return {
                "imdb_rating": None,
                "main_actors": None,
                "imdb_nb_votes": None
            }

        print(f"[INFO] Found data for: {title}")

        return {
            "imdb_rating": data.get("imdbRating"),
            "main_actors": data.get("Actors"),
            "imdb_nb_votes": data.get("imdbVotes")
        }

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return {
            "imdb_rating": None,
            "main_actors": None,
            "imdb_nb_votes": None
        }

for index, row in df.iterrows():
    title = row['title']
    year = row['release_year'] if 'release_year' in df.columns else None

    print(f"[INFO] Procesare: {title} ({year})")
    movie_data = get_movie_data(title, year)

    if movie_data:
        df.at[index, 'imdb_rating'] = movie_data['imdb_rating']
        df.at[index, 'main_actors'] = movie_data['main_actors']
        
        votes = movie_data['imdb_nb_votes']
        if votes:
            df.at[index, 'imdb_nb_votes'] = votes.replace(',', '')

    time.sleep(1)  

df['imdb_rating'] = pd.to_numeric(df['imdb_rating'], errors='coerce')
df['imdb_nb_votes'] = pd.to_numeric(df['imdb_nb_votes'], errors='coerce')

df.to_xml('movies_extended_top.xml', index=False, root_name='movies', row_name='movie', parser='etree')

top_10 = df.sort_values(by='imdb_rating', ascending=False).head(10)

print("\n Top 10 filme după evaluarea IMDB:\n")
print(top_10[['title', 'release_year', 'imdb_rating', 'imdb_nb_votes']].to_string(index=False))

top_10.to_xml('top_10_movies.xml', index=False, root_name='top_movies', row_name='movie', parser='etree')
  
top_10.to_csv('top_10_movies.csv', index=False)
