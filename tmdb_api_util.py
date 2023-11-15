"""Module providing utilities for pulling data from TMDB."""
from datetime import date
import os
from typing import Any

from dotenv import load_dotenv
import requests


load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY_AUTH")


def send_get_request(url: str, params: dict | None = None) -> requests.Response:
    """
    Sends a GET request to TMDB API.

    Args:
        url: The URL/endpoint to TMDB API.
        params: Dictionary of additional parameters for the request, if any.

    Returns:
        A requests.Response object containing the response to the request.

    Raises:
        RequestException: An error occurred while handling the GET request.
    """
    base_params = {"api_key": API_KEY, "language": "en-US"}
    if params:
        base_params.update(params)

    try:
        response = requests.get(url, params=base_params, timeout=60)
    except requests.exceptions.RequestException as error:
        raise SystemExit(error) from error

    return response


def fetch_upcoming_movies() -> list[tuple[str, date]]:
    """
    Fetches a list of upcoming movies from TMDB.

    Returns:
        A list containing tuples of strings. Each tuple contains the
        movie ID and its release date.
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
        response = send_get_request(url, {"page": page})
        data = response.json()

        # Add movies to list.
        for movie in data["results"]:
            movie_id = int(movie["id"])
            release_date = date.fromisoformat(movie["release_date"])
            upcoming_movie = (movie_id, release_date)
            upcoming_movies.append(upcoming_movie)

    return upcoming_movies


def get_movie_details(movie_id: int) -> dict[str, Any]:
    """
    Get top level details of a movie in TMDB by ID.

    Args:
        movie_id: Integer value of movie ID.
    
    Returns:
        Dictionary containing details about the movie.
    """
    url = "https://api.themoviedb.org/3/movie/"
    response = send_get_request(f"{url}{movie_id}")
    data = response.json()
    return data
