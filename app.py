import json
import sqlite3

from flask import Flask, render_template, jsonify, request

from utills import get_movie_title, get_movie_to_year, search_to_rating, movies_by_genre

app = Flask(__name__, )


@app.route("/")
def get_page():
    return ("ПРИВЕТ")


@app.route("/movies/<title>")
def search_by_title(title):
    """"Вьюшка поиска по названию"""
    # title = request.args.get('title')
    result = get_movie_title(title=title)

    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json"
    )


@app.route("/movies/<year1>/to/<year2>")
def search_by_year(year1, year2):
    """"Вьюшка поиска по диапазону лет выпуска"""
    result = get_movie_to_year(year1=year1, year2=year2)

    return jsonify(result)


@app.route("/rating/<rating>/")
def rating_children(rating):
    """"Вьюшка поиска по рейтингу"""
    result = search_to_rating(rating=rating)
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json"
    )


@app.route("/genre/<genre>")
def search_by_genre(genre):
    """"Вьюшка которая получает название жанра в качестве аргумента и возвращает
    10самых свежих фильмов в формате json"""
    result = movies_by_genre(genre=genre)
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json"
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=8000,
            debug=True)
