import requests
import pandas as pd

# TMDB API configuration
API_KEY = "806db2e521790686026dcdd857ede91d"
URL = "https://api.themoviedb.org/3/search/movie"

# Movies to search
MOVIES = [
    "The Shawshank Redemption",
    "The Godfather",
    "The Dark Knight",
    "Inception",
    "Interstellar",
    "Titanic",
    "Avatar",
    "Forrest Gump",
    "The Matrix",
    "Gladiator"
]


def get_movie_details(movie_name):
    """Retrieve movie details using the TMDB API."""

    params = {
        "api_key": API_KEY,
        "query": movie_name
    }

    try:
        response = requests.get(
            URL,
            params=params,
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])

        if not results:
            print(f"Movie not found: {movie_name}")
            return None

        # Select the first matching search result
        movie = results[0]

        return {
            "Movie Title": movie.get("title", "N/A"),
            "Release Date": movie.get("release_date", "N/A"),
            "TMDB Rating": movie.get("vote_average", "N/A"),
            "Vote Count": movie.get("vote_count", "N/A"),
            "Overview": movie.get("overview", "N/A"),
            "Language": movie.get("original_language", "N/A")
        }

    except requests.exceptions.RequestException as error:
        print(f"Network/API error for {movie_name}: {error}")
        return None

    except ValueError:
        print(f"Invalid response received for {movie_name}.")
        return None


def main():
    print("=" * 60)
    print("       MOVIE RATING SCRAPER USING TMDB API")
    print("=" * 60)

    if API_KEY == "YOUR_TMDB_API_KEY" or not API_KEY.strip():
        print("Please add your TMDB API key to the code.")
        return

    movie_data = []

    for movie_name in MOVIES:
        print(f"\nSearching for: {movie_name}")

        details = get_movie_details(movie_name)

        if details:
            movie_data.append(details)

            print(f"Title: {details['Movie Title']}")
            print(f"Release Date: {details['Release Date']}")
            print(f"TMDB Rating: {details['TMDB Rating']}")
            print(f"Vote Count: {details['Vote Count']}")

    if movie_data:
        df = pd.DataFrame(movie_data)

        df.to_csv(
            "movie_ratings.csv",
            index=False,
            encoding="utf-8-sig"
        )

        print("\n" + "=" * 60)
        print("MOVIE DATA COLLECTION COMPLETED")
        print("=" * 60)

        print(df.to_string(index=False))
        print("\nData saved successfully to movie_ratings.csv")

    else:
        print("\nNo movie data was collected.")
        print("Check your API key and internet connection.")


if __name__ == "__main__":
    main()
