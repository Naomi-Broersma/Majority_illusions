from collections import Counter
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


def order_by_number_of_edges(graph, blue_nodes):
    counter_node1 = Counter(edge[0] for edge in graph.edges())
    counter_node2 = Counter(edge[1] for edge in graph.edges())
    node_and_occurrence = []
    for node in blue_nodes:
        edges_for_node = counter_node1[node] + counter_node2[node]
        node_and_occurrence.append((node, edges_for_node))
    node_sorted_by_occurrence = sorted(node_and_occurrence, key=lambda x: x[1])
    nodes = list(map(lambda x: x[0], node_sorted_by_occurrence))
    edges_per_node = list(map(lambda x: x[1], node_sorted_by_occurrence))
    return nodes, edges_per_node


# Algorithm 5 of Venema-Los et al. (2023)
def add_extra_blue_edges(graph, blue_nodes, degree, degree_blue):
    # Determine how many edges each blue node already has and sort from least to most edges.
    nodes, edges_per_node = order_by_number_of_edges(graph, blue_nodes)
    print(graph.edges())
    for index in range(0, len(nodes)):
        index_next = (index + 1) % len(nodes)
        # Check if the node has more than k blue open edges
        if (not (nodes[index], nodes[index_next]) in graph.edges() and edges_per_node[index] < degree - degree_blue and
                edges_per_node[index_next] < degree - degree_blue):
            # Add the edge and increase the amount of edges for the current and next node.
            graph.add_edge(nodes[index], nodes[index_next])
            edges_per_node[index] = edges_per_node[index] + 1
            edges_per_node[index_next] = edges_per_node[index_next] + 1
    print(graph.edges())
    return


# Algorithm 6 of Venema-Los et al. (2023).
def add_regular_subgraph(graph, coloured_nodes, colour_degree):
    for index in range(0, len(coloured_nodes)):
        if len(coloured_nodes) % 2 == 0:
            index_start = index + int(np.floor(len(coloured_nodes)/2) % len(coloured_nodes))
        else:
            index_start = index + len(coloured_nodes) / 2
        if len(coloured_nodes) % 2 == 0 and colour_degree % 2 == 1:
            graph.add_edge(coloured_nodes[index], coloured_nodes[index_start])
        # TODO how does this work when k_colour can be odd, but r needs to be an integer?
        r = colour_degree / 2
        print(len(coloured_nodes))
        if len(coloured_nodes) % 2 == 1 and colour_degree % 2 == 1:
            r = (colour_degree - 1) / 2
        print(colour_degree, r, int(r))
        for i in range(1, r+1):
            index_minus = int(np.ceil(index_start - i) % len(coloured_nodes))
            index_plus = int(np.floor(index_start + i) % len(coloured_nodes))
            graph.add_edge(coloured_nodes[index], coloured_nodes[index_minus])
            graph.add_edge(coloured_nodes[index], coloured_nodes[index_plus])
    return graph


def add_unconnected_less_than_k_edges(graph, nodes, k):
    for node in nodes:
        if node.neighbours() < k:
            for other_node in nodes:  # TODO does this include blue_1/red_c?
                if other_node != node and not (other_node, node) in graph.edges() and not (node, other_node) in graph.edges():
                    edge_counter = 0
                    for edge in graph.edges():
                        if edge[0] == other_node or edge[1] == other_node:
                            edge_counter = edge_counter + 1
                    if edge_counter < k:
                        graph.add_edge(node, other_node)
                        break
    return graph


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
    regular_graph = add_initial_edges(regular_graph, blue_nodes, red_nodes, k)
    add_extra_blue_edges(regular_graph, blue_nodes, k, k_blue_nodes)
    if k_red_nodes % 2 == 0 or num_red_nodes % 2 == 0:
        regular_graph = add_regular_subgraph(regular_graph, red_nodes, k_red_nodes)
    if k_blue_nodes % 2 == 0 or num_blue_nodes % 2 == 0:
        regular_graph = add_regular_subgraph(regular_graph, blue_nodes, k_blue_nodes)
    if k_red_nodes % 2 == 1 and num_red_nodes % 2 == 1:
        k_red_temp = k_red_nodes - 1
        regular_graph = add_regular_subgraph(regular_graph, red_nodes, k_red_temp)
        if k_blue_nodes > 0:
            k_blue_temp = k_blue_nodes - 1
            regular_graph = add_regular_subgraph(regular_graph, blue_nodes, k_blue_temp)
    ordered_blue_nodes = order_by_number_of_edges(regular_graph, blue_nodes)
    blue_least_edges = ordered_blue_nodes[0]
    red_without_unconnected_red = []
    for red_node in red_nodes:
        if not (blue_least_edges, red_node) in regular_graph.edges() and not (red_node, blue_least_edges) in regular_graph.edges():
            red_without_unconnected_red = red_nodes.copy()
            red_without_unconnected_red.remove(red_node)
            regular_graph.add_edge(blue_least_edges, red_node)
            break
    blue_without_blue_least_edges = blue_nodes.copy()
    blue_without_blue_least_edges.remove(blue_least_edges)
    if k_blue_nodes > 0:
        regular_graph = add_unconnected_less_than_k_edges(regular_graph, blue_without_blue_least_edges, k)
    regular_graph = add_unconnected_less_than_k_edges(regular_graph, red_without_unconnected_red, k)
    return


if __name__ == "__main__":
    create_regular_maj_maj_ill_graph(10, 3)