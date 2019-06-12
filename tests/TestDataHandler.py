import unittest
from filmscraper import DataHandler, PlotGraph


class TestDataHandler(unittest.TestCase):
    def test_get_hub_actors(self):
        g = DataHandler.parse_json_to_graph('test_data.json')
        hub_actors = DataHandler.find_hub_actors(g)
        self.assertEqual(len(hub_actors), 13)

    def test_find_grossing_by_age(self):
        g = DataHandler.parse_json_to_graph('test_data.json')
        grossing_by_age = DataHandler.find_grossing_by_age(g)
        self.assertNotEqual(grossing_by_age[70], 0)


if __name__ == '__main__':
    unittest.main()