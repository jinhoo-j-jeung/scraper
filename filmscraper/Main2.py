from filmscraper import DataHandler, PlotGraph


def main():
    g = DataHandler.parse_json_to_graph('data.json')
    hub_actors = DataHandler.find_hub_actors(g)
    grossing_by_ages = DataHandler.find_grossing_by_age(g)

    PlotGraph.plot_grossing_by_ages(grossing_by_ages)
    PlotGraph.plot_hub_actors(hub_actors)
    PlotGraph.plot_top_hub_actors(hub_actors, 10)


if __name__ == "__main__":
        main()