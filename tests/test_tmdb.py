import pytest
import tmdb_client
from main import app
from unittest.mock import Mock

api_token = "ed25c0af7734be772dce97e510abaa71"
api_url = "https://api.themoviedb.org/3"


def test_get_single_movie():
    single_movie = tmdb_client.get_single_movie(movie_id=2)
    assert single_movie is not None


# def test_get_movie_images():
#     movie_images_path = ['https://image.tmdb.org/t/p/w780//nt21xmsQ8Jah6FJWE2MHGfyTJLg.jpg', 'backdrops']
#     expected_default_size = 'w780'
#     movie_url = tmdb_client.get_movie_images(movie_images_path)
#     assert expected_default_size in movie_url

def test_get_movie_images(monkeypatch):
    mock_movie_images = {"backdrops": [{}]}
    requests_mock = Mock()

    response = requests_mock.return_value
    response.json.return_value = mock_movie_images
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    movies_list = tmdb_client.get_movie_images(movie_id=637649)
    assert movies_list == mock_movie_images["backdrops"]


def test_get_single_movie_cast(monkeypatch):
    mock_single_movie_cast = {"cast": [{}]}
    requests_mock = Mock()

    response = requests_mock.return_value
    response.json.return_value = mock_single_movie_cast
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    movies_list = tmdb_client.get_single_movie_cast(movie_id=637649)
    assert movies_list == mock_single_movie_cast["cast"]


# @pytest.mark.parametrize("test_get_movies, expected", [("list_type", "popular"), ("response", 200)])
# #@pytest.mark.parametrize("test_get_movies, expected", [("list_type", "upcoming"), ("response", 200)])
# def test_homepage(test_get_movies, expected):
#    with app.test_client() as client:
#        expected = client.get(f'/list_type={expected[0]}')
#        assert eval(test_get_movies) == expected


@pytest.mark.parametrize("list_type, response_code", [("popular", 200), ("top_rated", 200), ("upcoming", 200)])
def test_homepage(list_type, response_code, monkeypatch):
    api_mock = Mock(return_value=8 * [{"id": 541, "poster_path": None, "title": "test"}])
    monkeypatch.setattr("tmdb_client.get_movies_list", api_mock)

    with app.test_client() as client:
        response = client.get(f'/list?list_type={list_type}')
        assert response.status_code == response_code
        api_mock.assert_called_once_with(list_type)


if __name__ == "__main__":
    pytest.main(["test_tmdb.py", "-s"])
