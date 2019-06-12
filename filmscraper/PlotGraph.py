import matplotlib.pyplot as plt
import jgraph


def plot_grossing_by_ages(dict):
    """
    Plot a grossing_by_ages graph
    :param dict: Dictionary of actors' grossing by ages
    :return:
    """
    age_groups = sorted(list(dict.keys()))
    print(age_groups)
    x_axis = list()
    y_axis = list()
    for age_group in age_groups:
        x_axis.append('<'+str(age_group))
        y_axis.append(dict.get(age_group))
    plt.plot(x_axis, y_axis)
    plt.xlabel('Age Groups')
    plt.ylabel('Total Grossing Values')
    plt.title('Grossing Values By Age groups')
    plt.show()


def plot_hub_actors(dict):
    """
    Plot actors and their connections
    :param dict: Dictionary of hub actors
    :return:
    """
    actors = list(dict.keys())
    num_connections = list(dict.values())
    plt.bar(actors, num_connections)
    plt.xlabel('Actor')
    plt.ylabel('Number of Connections')
    plt.title('Hub Actors')
    plt.show()


def plot_top_hub_actors(dict, num):
    """
    Plot top X actors with the most connections
    :param dict: Dictionary of hub actors
    :param num: The number of top actors
    :return:
    """
    tuples = list()
    for item in list(dict.keys()):
        tuples.append((item, dict.get(item)))
    tuples = sorted(tuples, key=lambda tuples: tuples[1], reverse=True)[:num]
    actors = list()
    connections = list()
    for tup in tuples:
        actors.append(tup[0])
        connections.append(tup[1])

    plt.bar(actors, connections)
    plt.xticks(actors, rotation=45)
    plt.xlabel('Actor')
    plt.ylabel('Number of Connections')
    title = 'Top '+str(num)+' Hub Actors'
    plt.title(title)
    plt.show()
