import json
import re
from filmscraper import Graph


def main():
    g = Graph.Graph()

    with open('actor_output.json') as json_data:
        actors = json.load(json_data)
    with open('movie_output.json') as json_data:
        movies = json.load(json_data)

    for a in actors:
        json_a = json.loads(a)
        digitized_age = None
        if json_a['age'] is not None:
            digitized_age = int(json_a['age'])
        actor = Graph.Actor(json_a['name'], digitized_age, json_a['films'], g.num_vertices)
        g.add_vertex(actor)
        if g.num_vertices >= 250:
            break

    for m in movies:
        json_m = json.loads(m)
        digitized_year = None
        if json_m['year'] is not None:
            match = re.search('\d{4}', json_m['year'])
            if match:
                digitized_year = int(match.group(0))
        digitized_grossing = None
        if json_m['Grossing'] is not None:
            match = re.search('million', json_m['Grossing'])
            if match:
                temp1 = json_m['Grossing'].replace("million", "")
                digitized_grossing = temp1.replace("$", "").split()[0]
        movie = Graph.Movie(json_m['title'], digitized_year, digitized_grossing, json_m['cast'], g.num_vertices)
        g.add_vertex(movie)
        if g.num_vertices >= 375:
            break

    for v in g.vertices:
        vertex = g.vertices.get(v)
        if isinstance(vertex, Graph.Actor):
            r = vertex.id
            for f in vertex.films:
                if g.vertices.get(f) is not None:
                    c = g.vertices.get(f).id
                    g.adj_matrix[r][c] = 1
        else:
            r = vertex.id
            for c in vertex.cast:
                if g.vertices.get(c) is not None:
                    c = g.vertices.get(c).id
                    g.adj_matrix[r][c] = 1

    # g.get_movie_grossing("Sleepers")
    # g.get_actor_filmography("Morgan Freeman")
    # g.get_film_cast("Sleepers")
    # g.list_oldest_actors(3)
    # g.list_movies_given_year(2005)
    # g.list_actors_given_year(2005)
    # g.list_top_grossing_actors(5)
    # for i in range(0, 275):
    #     total = sum(g.adj_matrix[i])
    #     if total > 0:
    #         print("sum of column", i, "is", total)

    print("Please enter the number of queries you want to run(1~7):")
    user_input = input()
    while user_input != 'exit':
        if user_input == '1':
            print("To find how much a movie has grossed, please type the title:")
            user_input = input()
            g.get_movie_grossing(user_input)
        if user_input == '2':
            print("To find  which movies an actor has worked in, please type the name of an actor:")
            user_input = input()
            g.get_actor_filmography(user_input)
        if user_input == '3':
            print("To find which actors worked in a movie, please type the title:")
            user_input = input()
            g.get_film_cast(user_input)
        if user_input == '4':
            print("To find the top X actors with the most total grossing value, please type the number:")
            user_input = input()
            g.list_top_grossing_actors(int(user_input))
        if user_input == '5':
            print("To find the oldest X actors, please type the number:")
            user_input = input()
            g.list_oldest_actors(int(user_input))
        if user_input == '6':
            print("To find all the movies for a given year, please type the year:")
            user_input = input()
            g.list_movies_given_year(int(user_input))
        if user_input == '7':
            print("To find all the actors for a given year, please type the year:")
            user_input = input()
            g.list_actors_given_year(int(user_input))

        print("Please enter the number of queries you want to run(1~7):")
        user_input = input()


if __name__ == "__main__":
    main()