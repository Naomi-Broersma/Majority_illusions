import networkx as nx
from matplotlib import pyplot as plt

import regular_graph_maj_maj_illusion


def nudge(position, x_shift, y_shift):
    return {n: (x + x_shift, y + y_shift) for n, (x, y) in position.items()}


def plot_graph(graph, colour_map):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, with_labels=False, pos=pos, ax=ax, node_size=500, node_color=colour_map,
                     arrowsize=20)  # default labeling
    # pos_nodes = nudge(pos, 0, 0.1)
    nx.draw_networkx_labels(graph, pos=pos, ax=ax, font_size=20, font_color="white")
    plt.show()
    return


def plot_graphs_next_to_each_other(graph1, graph2, colours1, colours2, title1, title2, pos1, pos2):
    fig, ax = plt.subplots(1, 2, figsize=(15, 6))
    nx.draw_networkx(graph1, with_labels=False, pos=pos1, ax=ax[0], node_size=700, node_color=colours1,
                     arrowsize=25)  # default labeling
    # pos_nodes = nudge(pos, 0, 0.1)
    ax[0].set_title(title1, fontsize=16.5)
    # nx.draw_networkx_labels(graph1, pos=pos, ax=ax[0], font_size=24, font_color="white")
    nx.draw_networkx(graph2, with_labels=False, pos=pos2, ax=ax[1], node_size=700, node_color=colours2,
                     arrowsize=25)  # default labeling
    # pos_nodes = nudge(pos, 0, 0.1)
    # nx.draw_networkx_labels(graph2, pos=pos, ax=ax[1], font_size=24, font_color="white")
    ax[1].set_title(title2, fontsize=16.5)
    plt.show()
    return


def example_introduction_k_reg_and_high_degree():
    regular_graph, colours = regular_graph_maj_maj_illusion.create_regular_maj_maj_ill_graph(10, 3)
    position_regular_graph = nx.circular_layout(regular_graph)
    high_degree_graph = nx.Graph()
    high_degree_graph.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    high_degree_graph.add_edges_from(
        [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
         (1, 7), (1, 8), (1, 9)])
    colours_high_degree = ["blue", "blue", "red", "red", "red", "red", "red", "red", "red", "red"]
    position_high_degree = nx.circular_layout(high_degree_graph)
    plot_graphs_next_to_each_other(high_degree_graph, regular_graph, colours_high_degree, colours,
                                   "A degree-disassortative graph with 10 nodes", "A 3-regular graph "
                                                                                  "with 10 nodes.",
                                   position_high_degree,
                                   position_regular_graph)
    return


# Initial example of a digraph with a majority-weak-majority illusion.
def example_maj_ill_digraph():
    graph = nx.DiGraph()
    graph.add_nodes_from([1, 2, 3, 4])
    graph.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 1), (2, 4), (3, 4), (3, 2), (4, 2)])
    colour_map = ["blue", "red", "blue", "blue"]
    plot_graph(graph, colour_map)
    return


def example_min_no_weak_maj_colouring_digraph():
    graph = nx.DiGraph()
    graph.add_nodes_from([0, 1, 2])
    graph.add_edges_from([(0, 1), (1, 2), (2, 0)])
    colour_map = ["blue", "blue", "blue"]
    colour_map2 = ["blue", "blue", "red"]
    plot_graph(graph, colour_map)
    position = nx.spring_layout(graph)
    plot_graphs_next_to_each_other(graph, graph, colour_map, colour_map2, "", "", position, position)
    return


def example_no_maj_weak_maj_illusion():
    graph1 = nx.DiGraph()
    graph1.add_nodes_from([0, 1, 2])
    graph1.add_edges_from([(0, 1), (1, 2), (2, 0)])
    colour_map1 = ["blue", "blue", "blue"]
    colour_map2 = ["blue", "blue", "red"]
    position = nx.spring_layout(
        graph1)  #Options: nx.planar_layout(graph1),nx.random_layout(graph1),nx.spring_layout(graph1)
    plot_graphs_next_to_each_other(graph1, graph1, colour_map1, colour_map2, "", "", position)
    return


def example_minimising_monochromatic_edges2():
    graph1 = nx.Graph()
    graph1.add_nodes_from([0, 1, 2, 3, 4, 5])
    graph1.add_edges_from([(0, 3), (1, 3), (2, 3), (3, 4), (3, 5)])
    colour_map1 = ["red", "red", "red", "blue", "blue", "blue"]
    colour_map2 = ["red", "red", "red", "blue", "red", "blue"]
    position = nx.spring_layout(
        graph1)  #Options: nx.planar_layout(graph1),nx.random_layout(graph1),nx.spring_layout(graph1)
    plot_graphs_next_to_each_other(graph1, graph1, colour_map1, colour_map2,
                                   "Initial undirected graph.", "Undirected graph after colour-swap.", position,
                                   position)
    graph2 = nx.DiGraph()
    graph2.add_nodes_from([0, 1, 2, 3, 4, 5])
    graph2.add_edges_from([(0, 3), (1, 3), (2, 3), (3, 4), (3, 5)])
    colour_map3 = ["red", "red", "red", "red", "blue", "blue"]
    plot_graphs_next_to_each_other(graph2, graph2, colour_map1, colour_map3, "Initial digraph.",
                                   "Digraph after colour-swap.", position, position)
    return


def incorrect_colouring_min_monochromatic_edges():
    graph = nx.DiGraph()
    graph.add_nodes_from([0, 1, 2])
    graph.add_edges_from([(0, 1), (1, 2), (2, 0)])
    colour_map = ["blue", "blue", "red"]
    plot_graph(graph, colour_map)
    return


def example_weak_maj_4_colouring():
    digraph = nx.DiGraph()
    for index in range(0, 10):
        digraph.add_node(index, pos=(index, 0))
    digraph.add_edges_from([(0, 1), (2, 4), (3, 6), (4, 5), (7, 8), (9, 0), (8, 3), (6, 5)])
    colour = 10*["black"]
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    # pos = nx.spring_layout(graph)
    pos = nx.get_node_attributes(digraph, 'pos')
    nx.draw_networkx_nodes(digraph, pos=pos, ax=ax, node_size=500, node_color=colour)  # default labeling
    nx.draw_networkx_labels(digraph, pos=pos, ax=ax, font_size=20, font_color="white")
    for edge in digraph.edges():
        nx.draw_networkx_edges(digraph, pos, connectionstyle='arc3, rad = 0.5', edgelist=[edge], width=2, alpha=1, arrowsize=20)
    plt.axis('off')
    plt.show()
    return


if __name__ == "__main__":
    example_maj_ill_digraph()
    # example_no_maj_weak_maj_illusion()
    # example_minimising_monochromatic_edges2()
    # incorrect_colouring_min_monochromatic_edges()
    # example_introduction_k_reg_and_high_degree()
    # example_weak_maj_4_colouring()
