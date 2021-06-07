from flask import Flask, render_template, request
from tmdb_client import get_movies, get_poster_url, get_single_movie, get_single_movie_cast, get_random_movie_picture

app = Flask(__name__)

def to_int(value):
    try:
        return int(value)
    except ValueError:
        return None

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}

@app.route('/list')
def homepage():
    selected_list = request.args.get('list_type', "popular")
    movies = get_movies(how_many=8, list_type=selected_list)
    return render_template("homepage.html", movies=movies , items={"Popular": "popular",
                                                                   "Now Playing": "now_playing",
                                                                    "Top Rated": "top_rated",
                                                                    "Upcoming": "upcoming" })



@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = get_single_movie(movie_id)
    cast = get_single_movie_cast(movie_id)
    picture = get_random_movie_picture(movie_id)
    return render_template("movie_details.html", movie=details, cast=cast, picture=picture)


if __name__ == '__main__':
    app.run(debug=True)