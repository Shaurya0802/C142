from operator import itruediv
from demographic_filtering import output
from content_filtering import get_recommendations
from storage import all_movies, liked_movies, unliked_movies, did_not_watch_movie
from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

@app.route("/get-movie")
def get_movie():
    movie_data = {
        "title": all_movies[0][19],
        "poster_link": all_movies[0][27],
        "release_data": all_movies[0][13] or "N/A",
        "duration": all_movies[0][15],
        "rating": all_movies[0][20],
        "overview": all_movies[0][9]
    }
    return jsonify({
        "data": movie_data,
        "status": "Success"
    })

@app.route("/liked-movie", methods=["POST"])
def liked_movie():
    movie = all_movies[0]
    liked_movies.append(movie)
    all_movies.pop(0)

    return jsonify({
        "status": "Success"
    }), 201

@app.route("/unliked-movie", methods=["POST"])
def unliked_movie():
    movie = all_movies[0]
    unliked_movies.append(movie)
    all_movies.pop(0)

    return jsonify({
        "status": "Success"
    }), 201

@app.route("/did-not-watch1", methods=["POST"])
def did_not_watch():
    movie = all_movies[0]
    did_not_watch_movie.append(movie)
    all_movies.pop(0)

    return jsonify({
        "status": "Success"
    }), 201

@app.route("/popular-movies") 
def popular_movies():
    movie_data = []
    for movie in output:
        _d = {
            "title": movie[0],
            "poster_link": movie[1],
            "release_date": movie[2] or "N/A",
            "duration": movie[3],
            "rating": movie[4],
            "overview": movie[5]
        }

        movie_data.append(_d)
        
    return jsonify({
        "data": movie_data,
        "status": "Success"
    }), 200

@app.route("/recommended-movies")
def recommended_movies():
    all_recommend = []
    for liked_movie in liked_movies:
        output = get_recommendations(liked_movie[19])
        for data in output:
            all_recommend.append(data)
    
    import itertools

    all_recommend.sort()
    all_recommend = list(all_recommend for all_recommend, _ in itertools.groupby(all_recommend))

    movie_data = []

    for recommended in all_recommend:
        _d = {
            "title": recommended[0],
            "poster_link": recommended[1],
            "release_date": recommended[2] or "N/A",
            "duration": recommended[3],
            "rating": recommended[4],
            "overview": recommended[5]
        }

        movie_data.append(_d)

    return jsonify({
        "data": movie_data,
        "status": "Success"
    }), 200

if __name__ == "__main__":
    app.run()