import json
import sqlite3
from pprint import pprint as pp




def get_netflix(sql):

    with sqlite3.connect("./netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(sql).fetchall()
        return result


def get_movie_title(title: str):
    sql = f"""select title, country, release_year, description 
           FROM netflix 
           WHERE title = '{title}'
           AND `type`='Movie'
           ORDER BY release_year desc LIMIT 1
           """

    result = get_netflix(sql)
    for item in result:
        return dict(item)


def get_movie_to_year(year1, year2):
    sql = f"""select title, release_year
            from netflix
            where release_year between '{year1}' and '{year2}'
            AND `type`='Movie'
            limit 100
           """
    respons = []
    result = get_netflix(sql)
    for item in result:
        respons.append(dict(item))
    return respons


def search_to_rating(rating):
    my_dict = {
        "children": ("G", ""),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17)")
    }
    sql = f"""select rating, title, description
                from netflix
                where rating in {my_dict.get(rating, ("R"))}
                """
    respons = []
    result = get_netflix(sql)
    for item in result:
        respons.append(dict(item))
    return respons


def movies_by_genre(genre):
    sql = f"""select title, description, release_year
            from netflix
            where listed_in like '%{genre}%' 
            ORDER BY release_year desc
            limit 10
            """
    respons = []
    result = get_netflix(sql)
    for item in result:
        respons.append(dict(item))
    return respons


def cast_dabl(cast1, cast2):
    """Функция, которая получает в качестве аргумента имена двух актеров,
    сохраняет всех актеров из колонки cast и возвращает список тех,
     кто играет с ними в паре больше 2 раз"""
    sql = f"""select "cast"                                                      
            from netflix                                                       
            where "cast" like '%{cast1}%' and "cast" like '%{cast2}%'
            """
    all_actors = []
    result = get_netflix(sql)
    for item in result:
        actors = item[0].split(", ")
        all_actors.extend(actors)

    actors_seen_twice = {actor for actor in all_actors if all_actors.count(actor) > 2} - {cast1, cast2}
    return actors_seen_twice


def search_movie(genre, year, typ):
    """Функция, с помощью которой можно будет передавать тип картины (фильм или сериал),
    год выпуска и ее жанр и получать на выходе список названий картин с их описаниями в JSON"""
    sql = f"""select title                                                   
            from netflix                                                          
            where  listed_in like '%{genre}%'
            and release_year = '{year}'
            and type = '{typ}'
            """
    #par_ = (listed_in, release_year, type)
    films = []
    #result = con.execute(sql, par_)
    #result = cur.fetchall()
    result = get_netflix(sql)
    for item in result:
        films.append(dict(item))
    return json.dumps(films, indent=2)

#pp(search_movie('Dramas', '1999', 'Movie'))
