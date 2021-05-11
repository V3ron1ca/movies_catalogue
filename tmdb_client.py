import requests
from random import shuffle

api_token = "ed25c0af7734be772dce97e510abaa71"
api_url = "https://api.themoviedb.org/3"

def get_movies_list(list_type):
    endpoint = f"{api_url}/movie/{list_type}?api_key={api_token}"
    response = requests.get(endpoint)
    return response.json()["results"]


def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"


def get_movies(how_many, list_type = "popular"):
    data = get_movies_list(list_type)
    shuffle(data)
    return data[:8]


def get_single_movie(movie_id):
    endpoint = f"{api_url}/movie/{movie_id}?api_key={api_token}"
    response = requests.get(endpoint)
    return response.json()


def get_single_movie_cast(movie_id):
    endpoint = f"{api_url}/movie/{movie_id}/credits?api_key={api_token}"
    response = requests.get(endpoint)
    return response.json()["cast"]


def get_movie_images(movie_id):
    endpoint = f"{api_url}/movie/{movie_id}/images?api_key={api_token}"
    response = requests.get(endpoint)
    print(response.json())
    return response.json()["backdrops"]


def get_random_movie_picture(movie_id):
    pictures = get_movie_images(movie_id)
    shuffle(pictures)
    return pictures[0]["file_path"]

