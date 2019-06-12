import json
import numpy as np
from filmscraper import Graph


def read_json(file):
    """
    Read json file
    :param file: String of file name
    :return: parsed json data
    """
    with open(file) as json_data:
        data = json.load(json_data)
    return data


def parse_json_to_graph(file):
    """
    Convert json file into a graph
    :param file: String of file name
    :return: graph data structure
    """
    data = read_json(file)

    actors = data[0]
    movies = data[1]
    g = Graph.Graph()
    g.adj_matrix = np.zeros((len(actors), len(movies)))

    actor_count = 0
    for actor_name in actors:
        a = actors[actor_name]
        actor = Graph.Actor(actor_name, a['age'], a['total_gross'], a['movies'], actor_count)
        g.add_vertex(actor)
        actor_count += 1

    movie_count = 0
    for movie_name in movies:
        m = movies[movie_name]
        movie = Graph.Movie(movie_name, m['year'], m['box_office'], m['actors'], movie_count)
        g.add_vertex(movie)
        movie_count += 1

    for v in g.vertices:
        vertex = g.vertices.get(v)
        if isinstance(vertex, Graph.Actor):
            a = vertex.id
            for f in vertex.films:
                movie = g.vertices.get(f)
                if movie is not None and isinstance(movie, Graph.Movie):
                    m = movie.id
                    if len(movie.cast) is not 0:
                        g.adj_matrix[a][m] = int(movie.grossing / len(movie.cast))
                    else:
                        g.adj_matrix[a][m] = 0

    return g


def find_hub_actors(g):
    """
    Find actors and their connections with each other
    :param g: graph of all actors and movies
    :return: dictionary
    """
    hub_actors = {}
    for v in g.vertices:
        vertex = g.vertices.get(v)
        if isinstance(vertex, Graph.Actor):
            for film in vertex.films:
                movie = g.vertices.get(film)
                if movie is not None and isinstance(movie, Graph.Movie):
                    if len(movie.cast) is not 0:
                        try:
                            hub_actors[vertex.name] += len(movie.cast) - 1
                        except KeyError:
                            hub_actors[vertex.name] = len(movie.cast) - 1
                    else:
                        try:
                            continue
                        except KeyError:
                            hub_actors[vertex.name] = 0
    return hub_actors


def find_grossing_by_age(g):
    """
    Find the total grossing value of actors by age groups
    :param g: a graph of all actors and movies
    :return: dictionary
    """
    grossing_by_age = {i : 0 for i in range(10, 120, 10)}
    for v in g.vertices:
        vertex = g.vertices.get(v)
        if isinstance(vertex, Graph.Actor):
            age = vertex.age
            if 0 < age < 10:
                grossing_by_age[10] += vertex.grossing
            elif age < 20:
                grossing_by_age[20] += vertex.grossing
            elif age <= 30:
                grossing_by_age[30] += vertex.grossing
            elif age <= 40:
                grossing_by_age[40] += vertex.grossing
            elif age <= 50:
                grossing_by_age[50] += vertex.grossing
            elif age <= 60:
                grossing_by_age[60] += vertex.grossing
            elif age <= 70:
                grossing_by_age[70] += vertex.grossing
            elif age <= 80:
                grossing_by_age[80] += vertex.grossing
            elif age <= 90:
                grossing_by_age[90] += vertex.grossing
            elif age <= 100:
                grossing_by_age[100] += vertex.grossing
            elif age <= 110:
                grossing_by_age[110] += vertex.grossing
    return grossing_by_age
