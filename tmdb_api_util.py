"""Module providing utilities for pulling data from TMDB."""
import os

from dotenv import load_dotenv
import requests


load_dotenv()
AUTH = os.getenv("TMDB_ACCESS_TOKEN_AUTH")
HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {AUTH}"
}


def send_get_request(url):
    """
    Sends a GET request to TMDB API.

    Returns:
        A requests.Response object containing the response to the request.

    Raises:
        RequestException: An error occurred while handling the GET request.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=60)
    except requests.exceptions.RequestException as error:
        raise SystemExit(error) from error

    return response


def fetch_upcoming_movies():
    """
    Fetches a list of upcoming movies from TMDB.

    Returns:
        A list containing tuples of strings. Each tuple contains the
        movie title (in English) and its release date (in YYYY-MM-DD) format.
    """
    url = "https://api.themoviedb.org/3/movie/upcoming"

    # Retrieve number of pages.
    response = send_get_request(url)
    data = response.json()
    num_pages = data["total_pages"]

    # Build a list of upcoming movies.
    upcoming_movies = []
    for page in range(1, num_pages + 1):
        # Request upcoming movies on each page.
        response = send_get_request(f"{url}?page={page}")
        data = response.json()

        # Add movies to list.
        for movie in data["results"]:
            upcoming_movie = (movie["title"], movie["release_date"])
            upcoming_movies.append(upcoming_movie)

    return upcoming_movies
