from collections import Counter

from venv import create

import networkx as nx
import numpy as np
from iteration_utilities import random_combination

# Venema-Los, M., Christoff, Z., & Grossi, D. (2023). On the Graph Theory of Majority Illusions.
# In V. Malvone & A. Murano (Eds.), Multi-Agent Systems (pp. 17–31). Cham: Springer Nature
# Switzerland.


# Initialisation step from algorithm 3 of Venema-Los et al. (2023)
# k_blue and k_red are the degrees of the regular subgraphs.
def initialise_degree_of_regular_subgraph(num_nodes, k):
    if num_nodes % 2 == 0:
        if k % 2 == 0:
            k_blue = k/2 - 3
            k_red = k/2 - 1
        else:
            k_blue = (k - 5)/2
            k_red = (k - 1)/2
        if k_blue < 0:
            k_blue = 0
    else:
        k_blue = k/2 - 2
        k_red = (k - 2)/2
    return k_blue, k_red


# Algorithm 4 of Venema-Los et al. (2023)
def add_initial_edges(graph, blue_nodes, red_nodes, degree):
    x = 0
    if degree % 2 == 0:
        num_edges = int(np.floor(len(red_nodes)*(degree + 2)/2))
    else:
        num_edges = int(np.floor(len(red_nodes) * (degree + 1) / 2))
    for i in range(0, num_edges):
        index_red = i % len(red_nodes)
        index_blue = (x + i) % len(blue_nodes)
        node_red = red_nodes[index_red]
        node_blue = blue_nodes[index_blue]
        if (node_red, node_blue) in graph.edges():
            x = 1
            index_blue = (x + i) % len(blue_nodes)
            node_blue = blue_nodes[index_blue]
        graph.add_edge(node_red, node_blue)
    print(graph.edges())
    return graph


# Algorithm 5 of Venema-Los et al. (2023)
def add_extra_blue_edges(graph, blue_nodes, degree, degree_blue):
    # Determine how many edges each blue node already has and sort from least to most edges.
    counter_node1 = Counter(edge[0] for edge in graph.edges())
    counter_node2 = Counter(edge[1] for edge in graph.edges())
    node_and_occurrence = []
    for node in blue_nodes:
        edges_for_node = counter_node1[node] + counter_node2[node]
        node_and_occurrence.append((node, edges_for_node))
    node_sorted_by_occurrence = sorted(node_and_occurrence, key=lambda x: x[1])
    nodes = list(map(lambda x: x[0], node_sorted_by_occurrence))
    occurrence_nodes = list(map(lambda x: x[1], node_sorted_by_occurrence))
    print("here")
    print(nodes, occurrence_nodes)
    # for index in range(0, len(node_sorted_by_occurrence)):
    #     index_next = (index + 1) % len(node_sorted_by_occurrence)
    #     # Check if the node has more than k blue open edges
    #     print(node_sorted_by_occurrence[index][0], node_sorted_by_occurrence[index][1])
    #     if (not (node_sorted_by_occurrence[index][0], node_sorted_by_occurrence[index_next][0]) in graph.edges() and
    #             node_sorted_by_occurrence[index][1] < degree - degree_blue and node_sorted_by_occurrence[index_next][1]
    #             < degree - degree_blue):
    #         # Add the edge and increase the amount of edges for the current and next node.
    #         graph.add_edge(node_sorted_by_occurrence[index][0], node_sorted_by_occurrence[index_next][0])
    #         node_sorted_by_occurrence[index][1] = node_sorted_by_occurrence[index][1] + 1
    #         node_sorted_by_occurrence[index_next][1] = node_sorted_by_occurrence[index_next][1] + 1
    print(graph.edges())
    return

# Algorithm 3 of Venema-Los et al. (2023)
# Input: the number of nodes in the graph and the degree k of the k-regular graph.
# Output: a k-regular graph that is under majority-majority illusion.
def create_regular_maj_maj_ill_graph(num_nodes, k):
    num_red_nodes = int(np.floor(num_nodes/2 + 1))
    num_blue_nodes = int(np.ceil(num_nodes/2 - 1))
    k_blue_nodes, k_red_nodes = initialise_degree_of_regular_subgraph(num_nodes, k)
    regular_graph = nx.Graph()
    regular_graph.add_nodes_from(list(range(1, num_nodes+1)))
    red_nodes = list(random_combination(regular_graph.nodes(), num_red_nodes))
    blue_nodes = list(set(regular_graph.nodes()) - set(red_nodes))
    # regular_graph = add_initial_edges(regular_graph, blue_nodes, red_nodes, k)
    add_extra_blue_edges(regular_graph, blue_nodes, k, k_blue_nodes)
    return


if __name__ == "__main__":
    create_regular_maj_maj_ill_graph(10, 3)