import unittest
from filmscraper import Graph


class TestGraph(unittest.TestCase):
    def test_add_vertex(self):
        g = Graph.Graph()
        actor = Graph.Actor("Jeremy", 28, ["a", "b"], 0)
        g.add_vertex(actor)
        self.assertEqual(g.vertices.get("Jeremy"), actor)

    def test_get_movie_grossing(self):
        g = Graph.Graph()
        movie = Graph.Movie("Gone with the wind", 1960, 20.0,["a", "b"], 0)
        g.add_vertex(movie)
        self.assertEqual(g.get_movie_grossing("Gone with the wind"), 20.0)

    def test_get_actor_filmography(self):
        g = Graph.Graph()
        actor = Graph.Actor("Jeremy", 28, ["a", "b"], 0)
        g.add_vertex(actor)
        self.assertEqual(g.get_actor_filmography("Jeremy"), ["a", "b"])

    def test_get_film_cast(self):
        g = Graph.Graph()
        movie = Graph.Movie("Gone with the wind", 1960, 20.0, ["a", "b"], 0)
        g.add_vertex(movie)
        self.assertEqual(g.get_film_cast("Gone with the wind"), ["a", "b"])

    def test_top_grossing_actors(self):
        g = Graph.Graph()
        actor1 = Graph.Actor("A", 28, ["a", "b"], 0)
        g.add_vertex(actor1)
        actor2 = Graph.Actor("B", 28, ["c", "d"], 1)
        g.add_vertex(actor2)

        movie1 = Graph.Movie("a", 1960, 10.0, ["A"], 2)
        g.add_vertex(movie1)
        movie2 = Graph.Movie("b", 1960, 20.0, ["A"], 3)
        g.add_vertex(movie2)
        movie3 = Graph.Movie("c", 1960, 5.0, ["B"], 4)
        g.add_vertex(movie3)
        movie4 = Graph.Movie("d", 1960, 10.0, ["B"], 5)
        g.add_vertex(movie4)

        self.assertEqual(g.list_top_grossing_actors(2), [("A", 30.0), ("B", 15.0)])

    def test_oldest_actors(self):
        g = Graph.Graph()
        actor1 = Graph.Actor("A", 55, ["a", "b"], 0)
        g.add_vertex(actor1)
        actor2 = Graph.Actor("B", 44, ["c", "d"], 1)
        g.add_vertex(actor2)
        actor3 = Graph.Actor("C", 33, ["a", "b"], 2)
        g.add_vertex(actor3)
        actor4 = Graph.Actor("D", 22, ["c", "d"], 3)
        g.add_vertex(actor4)

        self.assertEqual(g.list_oldest_actors(3), [("A", 55), ("B", 44), ("C", 33)])

    def test_movies_given_year(self):
        g = Graph.Graph()
        movie1 = Graph.Movie("a", 1990, 10.0, ["A"], 0)
        g.add_vertex(movie1)
        movie2 = Graph.Movie("b", 1930, 20.0, ["A"], 1)
        g.add_vertex(movie2)
        movie3 = Graph.Movie("c", 1960, 5.0, ["B"], 2)
        g.add_vertex(movie3)

        self.assertEqual(g.list_movies_given_year(1990), ["a"])

    def test_actors_given_year(self):
        g = Graph.Graph()
        actor1 = Graph.Actor("A", 55, ["a", "b"], 0)
        g.add_vertex(actor1)
        actor2 = Graph.Actor("B", 44, ["c", "d"], 1)
        g.add_vertex(actor2)
        actor3 = Graph.Actor("C", 33, ["a", "b"], 2)
        g.add_vertex(actor3)

        movie1 = Graph.Movie("a", 1991, 10.0, ["A"], 3)
        g.add_vertex(movie1)
        movie2 = Graph.Movie("b", 1990, 20.0, ["C"], 4)
        g.add_vertex(movie2)
        movie3 = Graph.Movie("c", 1960, 5.0, ["B"], 5)
        g.add_vertex(movie3)
        movie4 = Graph.Movie("d", 1970, 10.0, ["B"], 6)
        g.add_vertex(movie4)

        self.assertEqual(g.list_actors_given_year(1990), ["C"])


if __name__ == '__main__':
    unittest.main()