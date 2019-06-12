import unittest
from filmscraper.app import *
import json


class TestFlask(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        self.assertEqual(self.app.get("/").status_code, 200)

    def test_get_actor_by_name(self):
        self.assertEqual(self.app.get("/actors/Bruce_Willis").status_code, 200)

    def test_get_actors(self):
        self.assertEqual(self.app.get("/actors?name=Bruce").status_code, 200)
        self.assertEqual(self.app.get("/actors?ne=Bruce").status_code, 400)

    def test_get_movie_by_name(self):
        self.assertEqual(self.app.get("/movies/The Bye Bye Man").status_code, 200)

    def test_get_movies(self):
        self.assertEqual(self.app.get("/movies?name=Bye").status_code, 200)
        self.assertEqual(self.app.get("/movies?ne=Bye").status_code, 400)

    def test_update_actor(self):
        data = {"total_gross": 300}
        headers ={'content-type': 'application/json'}
        self.assertEqual(self.app.put('/update/actors/Faye_Dunaway', data=json.dumps(data), headers=headers).status_code, 200)
        self.assertEqual(self.app.put('/update/actors/Brdfadfs', data=json.dumps(data), headers=headers).status_code, 400)

    def test_update_movie(self):
        data = {"box_office": 200}
        headers ={'content-type': 'application/json'}
        self.assertEqual(self.app.put('/update/movies/Chairman_of_the_Board', data=json.dumps(data), headers=headers).status_code, 200)
        self.assertEqual(self.app.put('/update/movies/Brkjlkafdaj', data=json.dumps(data), headers=headers).status_code, 400)

    def test_create_actor(self):
        data = {'name': 'A', 'age': 10, 'total_gross': 30, 'movies': []}
        headers = {'content-type': 'application/json'}
        incomplete_data = {'name': 'B'}
        self.assertEqual(self.app.post('/create/actors', data=json.dumps(data), headers=headers).status_code, 201)
        self.assertEqual(self.app.post('/create/actors', data=json.dumps(data), headers=headers).status_code, 400)
        self.assertEqual(self.app.post('/create/actors', data=json.dumps(incomplete_data), headers=headers).status_code, 400)

    def test_create_movie(self):
        data = {'name': 'M', 'year': 2018, 'box_office': 3000, 'actors': []}
        incomplete_data = {'name': 'N'}
        headers = {'content-type': 'application/json'}
        self.assertEqual(self.app.post('/create/movies', data=json.dumps(data), headers=headers).status_code, 201)
        self.assertEqual(self.app.post('/create/movies', data=json.dumps(data), headers=headers).status_code, 400)
        self.assertEqual(self.app.post('/create/movies', data=json.dumps(incomplete_data), headers=headers).status_code, 400)

    def test_delete_actor(self):
        self.assertEqual(self.app.delete('/delete/actors/Bruce_Willis').status_code, 200)
        self.assertEqual(self.app.delete('/delete/actors/Bruce_lis').status_code, 400)

    def test_delete_movie(self):
        self.assertEqual(self.app.delete('/delete/movies/The_Bye_Bye_Man').status_code, 200)
        self.assertEqual(self.app.delete('/delete/movies/The B').status_code, 400)


if __name__ == '__main__':
    unittest.main()


