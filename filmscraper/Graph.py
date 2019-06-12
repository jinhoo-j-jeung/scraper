import numpy as np


class Actor:
    def __init__(self, name, age, grossing, films, id):
        """
        Default constructor for Actor
        :param name: name of an actor
        :param age: age of an actor
        :param films:  filmography of an actor
        :param id: unique id in Graph
        """
        self.name = name
        self.age = age
        self.grossing = grossing
        self.films = films
        self.id = id

    def serialize(self):
        return {
            'name': self.name,
            'age': self.age,
            'total_gross': self.grossing,
            'movies': self.films
        }


class Movie:
    def __init__(self, title, year, grossing, cast, id):
        """
        Default constructor for Movie
        :param title: title of a movie
        :param year: released year of a movie
        :param grossing: box office of a movie
        :param cast: casts of a movie
        :param id: unique id in Graph
        """
        self.name = title
        self.year = year
        self.grossing = grossing
        self.cast = cast
        self.id = id

    def serialize(self):
        return {
            'name': self.name,
            'year': self.year,
            'box_office': self.grossing,
            'actors': self.cast
        }


class Graph:
    def __init__(self):
        """
        Default Constructor of a graph
        """
        self.vertices = {}
        self.adj_matrix = np.zeros((375, 375))
        self.num_vertices = 0

    def add_vertex(self, vertex):
        """
        add a movie or actor node to a graph
        :param vertex: a movie or an actor node
        :return:
        """
        self.vertices[vertex.name] = vertex
        self.num_vertices += 1

    def remove_vertex(self, name):
        del self.vertices[name]
        self.num_vertices -= 1

    def get_movie_grossing(self, title):
        """
        finds a grossing for a movie
        :param title: title of a movie
        :return: a grossing of a movie
        """
        movie = self.vertices.get(title)
        if movie is None:
            print(title, "is not found.")
        elif isinstance(movie, Actor):
            print(title, "is an actor.")
        else:
            grossing = movie.grossing
            if grossing is None:
                print("grossing for", title, "is not available")
                return None
            else:
                print("grossing for", title, "is", grossing, "million dollars.")
                return grossing

    def get_actor_filmography(self, name):
        """
        finds a filmogrphy of an actor
        :param name: name of an actor
        :return: a list of films that the actor has starred
        """
        actor = self.vertices.get(name)
        if actor is None:
            print(name, "is not found.")
        elif isinstance(actor, Movie):
            print(name, "is a movie.")
        else:
            films = actor.films
            if films is []:
                print("filmogrphy for", name, "is empty.")
            else:
                print("filmogrphy for", name, "is", films)
            return films

    def get_film_cast(self, title):
        """
        finds a cast of a movie
        :param title: title of a movie
        :return: a list of actors who have starred in the movie
        """
        movie = self.vertices.get(title)
        if movie is None:
            print(title, "is not found.")
        elif isinstance(movie, Actor):
            print(title, "is an actor.")
        else:
            cast = movie.cast
            if cast is []:
                print("casts for", title, "is not available")
            else:
                print("casts for", title, "is", cast)
            return cast

    def list_top_grossing_actors(self, num):
        """
        find top X actors with the biggest grossing
        :param num: number of X
        :return: list of top x actors with the largest grossing
        """
        actors = []
        for v in self.vertices:
            if isinstance(self.vertices.get(v), Actor):
                actor = self.vertices.get(v)
                films = actor.films
                if len(films) != 0:
                    grossing = 0
                    for f in films:
                        movie = self.vertices.get(f)
                        if movie is not None:
                            if movie.grossing is not None:
                                grossing += float(movie.grossing)
                    actors.append((actor.name, grossing))
        if num >= len(actors):
            ret = sorted(actors, key=lambda tup: tup[1], reverse=True)
        else:
            ret = sorted(actors, key=lambda tup: tup[1], reverse=True)[:num]

        print(num, "top grossing actors are :")
        for i in range(len(ret)):
            print(ret[i][0], "-", ret[i][1], "million dollar worth")
        return ret

    def list_oldest_actors(self, num):
        """
        finds X oldest actors
        :param num: number of X
        :return: a list of top X oldest actors
        """
        actors = []
        for v in self.vertices:
            actor = self.vertices.get(v)
            if isinstance(actor, Actor):
                if actor.age is not None:
                    actors.append((actor.name, actor.age))
        ret = sorted(actors, key=lambda tup: tup[1], reverse=True)[:num]
        print(num, "oldest actors are :")
        for i in range(len(ret)):
            print(ret[i][0], "-", ret[i][1], "years-old")
        return ret

    def list_movies_given_year(self, year):
        """
        finds movies released at the given year
        :param year: year
        :return: a list of movies released at the given year
        """
        movies = []
        for v in self.vertices:
            movie = self.vertices.get(v)
            if isinstance(movie, Movie):
                if movie.year is not None and movie.year == year:
                    movies.append(movie.name)

        if len(movies) == 0:
            print("In a given year", year, ", could not find any movie")
        else:
            print("In", year, ",", movies, "are found.")
        return movies

    def list_actors_given_year(self, year):
        """
        finds actors starred at movies released at the given year
        :param year: year
        :return: a list of actors who have starred at the movies released at the given year
        """
        actors = []
        for v in self.vertices:
            movie = self.vertices.get(v)
            if isinstance(movie, Movie):
                if movie.year is not None and movie.year == year:
                    cast = movie.cast
                    for c in cast:
                        actors.append(c)
        if len(actors) == 0:
            print("In a given year", year, ", could not find any actor")
        else:
            print("In", year, ",", actors, "are found.")
        return actors