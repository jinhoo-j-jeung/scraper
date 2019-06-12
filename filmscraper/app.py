from flask import Flask, jsonify, request, Response, testing
from filmscraper import DataHandler
from filmscraper import Graph


app = Flask(__name__)

graph = DataHandler.parse_json_to_graph('data.json')
actors = DataHandler.read_json('data.json')[0]
movies = DataHandler.read_json('data.json')[1]


@app.route('/')
def index():
    return "CS242"


# Get
@app.route('/actors/<actor_name>')
def get_actor_by_name(actor_name):
    actor_name = actor_name.replace("_", " ")
    return jsonify(actors.get(actor_name))


@app.route('/actors', methods=['GET'])
def get_actors():
    ret = list()

    name = request.args.get('name')
    age = request.args.get('age')
    total_gross = request.args.get('total_gross')

    for a in actors:
        actor = actors.get(a)
        if (name is not None and name in actor['name']) or (age is not None and int(age) == actor['age']) or (total_gross is not None and int(total_gross) <= actor['total_gross']):
                ret.append(actor)

    if name is None and age is None and total_gross is None:
        return Response("Wrong Arguments", status=400)
    return jsonify(ret)


@app.route('/movies/<movie_name>')
def get_movie_by_name(movie_name):
    movie_name = movie_name.replace("_", " ")
    return jsonify(movies.get(movie_name))


@app.route('/movies', methods=['GET'])
def get_movies():
    ret = list()

    name = request.args.get('name')
    year = request.args.get('year')
    box_office = request.args.get('box_office')

    for m in movies:
        movie = movies.get(m)
        if (name is not None and name in movie['name']) or (year is not None and int(year) == movie['year']) or (box_office is not None and int(box_office) <= movie['box_office']):
                ret.append(movie)
    if name is None and year is None and box_office is None:
        return Response("Wrong Arguments", status=400)
    return jsonify(ret)


# Put
@app.route('/update/actors/<actor_name>', methods=['PUT'])
def update_actor(actor_name):
    actor_name = actor_name.replace("_", " ")
    try:
        actor = actors[actor_name]
        actor['age'] = request.json.get('age', actor['age'])
        actor['total_gross'] = request.json.get('total_gross', actor['total_gross'])
        actor['movies'] = request.json.get('movies', actor['movies'])
        actors[actor_name] = actor
        a = graph.vertices.get(actor_name)
        #print(a.grossing)
        a.age = actor['age']
        a.grossing = actor['total_gross']
        a.films = actor['movies']
        # print(movies[movie_name])
        #print(a.grossing)
        return Response("Actor updated\n", status=200)
    except KeyError:
        return Response("Actor does not exist\n", status=400)


@app.route('/update/movies/<movie_name>', methods=['PUT'])
def update_movie(movie_name):
    movie_name = movie_name.replace("_", " ")
    try:
        movie = movies[movie_name]
        #print(movie)
        movie['year'] = request.json.get('year', movie['year'])
        movie['box_office'] = request.json.get('box_office', movie['box_office'])
        movie['actors'] = request.json.get('actors', movie['actors'])
        movies[movie_name] = movie
        m = graph.vertices.get(movie_name)
        #print(m.grossing)
        m.year = movie['year']
        m.grossing = movie['box_office']
        m.cast = movie['actors']
        #print(movies[movie_name])
        #print(m.grossing)
        return Response("Movie updated\n", status=200)
    except KeyError:
        return Response("Movie does not exist\n", status=400)


# POST
@app.route('/create/actors', methods=['POST'])
def create_actor():
    try:
        name = request.json['name']
        if actors.get(name) is not None:
            return Response("Already Exists\n", status=400)
        age = request.json['age']
        total_gross = request.json['total_gross']
        films = request.json['movies']
        actor = Graph.Actor(name, age, total_gross, films, len(actors))
    except KeyError:
        return Response("Missing Arguments\n", status=400)

    graph.add_vertex(actor)
    actors[name] = actor.serialize()

    return Response("Actor Created\n", status=201)


@app.route('/create/movies', methods=['POST'])
def create_movie():
    try:
        name = request.json['name']
        if movies.get(name) is not None:
            return Response("Already Exists\n", status=400)
        year = request.json['year']
        box_office = request.json['box_office']
        casts = request.json['actors']
        movie = Graph.Movie(name, year, box_office, casts, len(movies))
    except KeyError:
        return Response("Missing Arguments\n", status=400)

    graph.add_vertex(movie)
    movies[name] = movie.serialize()

    return Response("Movie Created\n", status=201)


# Delete
@app.route('/delete/actors/<name>', methods=['Delete'])
def delete_actor(name):
    name = name.replace("_", " ")
    try:
        actor = actors[name]
        del actor
    except KeyError:
        return Response("Actor does not exist\n", status=400)

    del actors[name]
    graph.remove_vertex(name)
    return Response("Actor Deleted\n", status=200)


@app.route('/delete/movies/<name>', methods=['Delete'])
def delete_movie(name):
    name = name.replace("_", " ")
    try:
        movie = movies[name]
        del movie
    except KeyError:
        return Response("Movie does not exist\n", status=400)

    del movies[name]
    graph.remove_vertex(name)
    return Response("Movie Deleted\n", status=200)


if __name__ == '__main__':
    app.run(debug=True)
