import networkx as nx
from matplotlib import pyplot as plt


def nudge(position, x_shift, y_shift):
    return {n: (x + x_shift, y + y_shift) for n, (x, y) in position.items()}


def plot_graph(graph, colour_map):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, with_labels=False, pos=pos, ax=ax, node_color=colour_map, arrowsize=20)  # default labeling
    pos_nodes = nudge(pos, 0, 0.1)
    nx.draw_networkx_labels(graph, pos=pos_nodes, ax=ax, font_size=16)
    plt.show()
    return


def plot_graphs_next_to_each_other(graph1, graph2, colours1, colours2, title1, title2):
    fig, ax = plt.subplots(1, 2, figsize=(15, 6))
    pos = nx.spring_layout(graph1)
    nx.draw_networkx(graph1, with_labels=False, pos=pos, ax=ax[0], node_color=colours1, arrowsize=20)  # default labeling
    # pos_nodes = nudge(pos, 0, 0.1)
    ax[0].set_title(title1, fontsize=16.5)
    nx.draw_networkx_labels(graph1, pos=pos, ax=ax[0], font_size=16)
    # pos = nx.spring_layout(graph2)
    nx.draw_networkx(graph2, with_labels=False, pos=pos, ax=ax[1], node_color=colours2, arrowsize=20)  # default labeling
    # pos_nodes = nudge(pos, 0, 0.1)
    nx.draw_networkx_labels(graph2, pos=pos, ax=ax[1], font_size=16)
    ax[1].set_title(title2, fontsize=16.5)
    plt.show()
    return

# Initial example of a digraph with a majority-weak-majority illusion.
def example_maj_ill_digraph():
    graph = nx.DiGraph()
    graph.add_nodes_from([1, 2, 3, 4])
    graph.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 1), (2, 4), (3, 4), (3, 2), (4, 2)])
    colour_map = ["blue", "red", "blue", "blue"]
    plot_graph(graph, colour_map)
    return


def example_no_ill_digraph():
    graph = nx.DiGraph()
    graph.add_nodes_from([0, 1, 2])
    graph.add_edges_from([(0, 1), (1, 2), (2, 0)])
    colour_map = ["blue", "blue", "blue"]
    colour_map2 = ["blue", "blue", "red"]
    plot_graph(graph, colour_map)
    plot_graphs_next_to_each_other(graph, graph, colour_map, colour_map2, "", "")
    return


def example_minimising_monochromatic_edges():
    graph1 = nx.DiGraph()
    graph1.add_nodes_from([0, 1, 2])
    graph1.add_edges_from([(0, 1), (1, 2), (2, 0)])
    colour_map1 = ["blue", "blue", "blue"]
    graph2 = nx.Graph()
    graph2.add_nodes_from([0, 1, 2])
    graph2.add_edges_from([(0, 1), (1, 2), (2, 0)])
    colour_map2 = ["blue", "blue", "blue"]
    plot_graphs_next_to_each_other(graph1, graph2, colour_map1, colour_map2, "Initial digraph.", "Initial undirected graph.")

    colour_map3 = ["blue", "blue", "red"] # Colour map after selecting a node to minimise monochromatic edges.
    colour_map4 = ["blue", "blue", "red"]
    plot_graphs_next_to_each_other(graph1, graph2, colour_map3, colour_map4, "Digraph with minimised monochromatic out-edges.", "Undirected graph with minimised monochromatic edges.")
    return


if __name__ == "__main__":
    example_minimising_monochromatic_edges()
