from collections import Counter
import networkx as nx
import numpy as np
from iteration_utilities import random_combination
from matplotlib import pyplot as plt


# Venema-Los, M., Christoff, Z., & Grossi, D. (2023). On the Graph Theory of Majority Illusions.
# In V. Malvone & A. Murano (Eds.), Multi-Agent Systems (pp. 17–31). Cham: Springer Nature
# Switzerland.


# Change the position of node labels in the plot
def nudge(pos, x_shift, y_shift):
    return {n: (x + x_shift, y + y_shift) for n, (x, y) in pos.items()}


# Plot the network in a nice way.
def plot_graph(graph, colour_map):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, with_labels=False, pos=pos, ax=ax, node_color=colour_map, arrowsize=20)  # default labeling
    pos_nodes = nudge(pos, 0, 0.1)
    nx.draw_networkx_labels(graph, pos=pos_nodes, ax=ax, font_size=16)
    plt.show()
    return


# Initialisation step from algorithm 3 of Venema-Los et al. (2023)
# k_blue and k_red are the degrees of the regular subgraphs.
def initialise_degree_of_regular_subgraph(num_nodes, k):
    if num_nodes % 2 == 0:
        if k % 2 == 0:
            k_blue = k / 2 - 3
            k_red = k / 2 - 1
        else:
            k_blue = (k - 5) / 2
            k_red = (k - 1) / 2
        if k_blue < 0:
            k_blue = 0
    else:
        k_blue = k / 2 - 2
        k_red = (k - 2) / 2
    return k_blue, k_red


# Algorithm 4 of Venema-Los et al. (2023)
def add_initial_edges(graph, blue_nodes, red_nodes, degree):
    x = 0
    if degree % 2 == 0:
        num_edges = int(np.floor(len(red_nodes) * (degree + 2) / 2))
    else:
        num_edges = int(np.floor(len(red_nodes) * (degree + 1) / 2))
    for i in range(0, num_edges):
        index_red = i % len(red_nodes)
        index_blue = (x + i) % len(blue_nodes)
        node_red = red_nodes[index_red]
        node_blue = blue_nodes[index_blue]
        if (node_red, node_blue) in graph.edges() or (node_blue, node_red) in graph.edges():
            x = 1
            index_blue = (x + i) % len(blue_nodes)
            node_blue = blue_nodes[index_blue]
        graph.add_edge(node_red, node_blue)
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
    for index in range(0, len(nodes)):
        index_next = (index + 1) % len(nodes)
        # Check if the node has more than k blue open edges
        if (not (nodes[index], nodes[index_next]) in graph.edges() and edges_per_node[index] < degree - degree_blue and
                edges_per_node[index_next] < degree - degree_blue):
            # Add the edge and increase the amount of edges for the current and next node.
            graph.add_edge(nodes[index], nodes[index_next])
            edges_per_node[index] = edges_per_node[index] + 1
            edges_per_node[index_next] = edges_per_node[index_next] + 1
    return


# Algorithm 6 of Venema-Los et al. (2023).
def add_regular_subgraph(graph, coloured_nodes, colour_degree):
    for index in range(0, len(coloured_nodes)):
        if len(coloured_nodes) % 2 == 0:
            index_start = (index + int(np.floor(len(coloured_nodes) / 2))) % len(coloured_nodes)
        else:
            index_start = index + len(coloured_nodes) / 2
        if len(coloured_nodes) % 2 == 0 and colour_degree % 2 == 1:
            graph.add_edge(coloured_nodes[index], coloured_nodes[index_start])
        r = colour_degree / 2
        if len(coloured_nodes) % 2 == 1 and colour_degree % 2 == 1:
            r = (colour_degree - 1) / 2
        for i in range(1, int(np.floor(r)) + 1):
            index_minus = int(np.ceil(index_start - i) % len(coloured_nodes))
            index_plus = int(np.floor(index_start + i) % len(coloured_nodes))
            graph.add_edge(coloured_nodes[index], coloured_nodes[index_minus])
            graph.add_edge(coloured_nodes[index], coloured_nodes[index_plus])
    return graph


def add_unconnected_less_than_k_edges(graph, nodes, k):
    for node in nodes:
        if len(list(graph.neighbors(node))) < k:
            for other_node in nodes:
                if other_node != node and not (other_node, node) in graph.edges() and not (node,
                                                                                           other_node) in graph.edges():
                    edge_counter = 0
                    for edge in graph.edges():
                        if edge[0] == other_node or edge[1] == other_node:
                            edge_counter = edge_counter + 1
                    if edge_counter < k:
                        graph.add_edge(node, other_node)
                        break
    return graph


# There will always be two connected red nodes in a subgraph.
def find_two_connected_red_nodes_in_subgraph(regular_graph, subgraph, colours):
    connected_red_nodes_found = False
    for node in subgraph:
        if connected_red_nodes_found:
            break
        if colours[node - 1] == "red":
            red_node = node
            # Find a red node connected to red_node
            for (node1, node2) in regular_graph.edges():
                if connected_red_nodes_found:
                    break
                if node1 == red_node and colours[node2 - 1] == "red" and node2 in subgraph:
                    red_node2 = node2
                    regular_graph.remove_edge(node1, node2)
                    connected_red_nodes_found = True
                if node2 == red_node and colours[node1 - 1] == "red" and node1 in subgraph:
                    red_node2 = node1
                    regular_graph.remove_edge(node1, node2)
                    connected_red_nodes_found = True
    return regular_graph, red_node, red_node2


# Algorithm 3 of Venema-Los et al. (2023)
# Input: the number of nodes in the graph and the degree k of the k-regular graph.
# Output: a k-regular graph that is under majority-majority illusion.
def create_regular_maj_maj_ill_graph(num_nodes, k):
    num_red_nodes = int(np.floor(num_nodes / 2 + 1))
    num_blue_nodes = int(np.ceil(num_nodes / 2 - 1))
    k_blue_nodes, k_red_nodes = initialise_degree_of_regular_subgraph(num_nodes, k)
    regular_graph = nx.Graph()
    regular_graph.add_nodes_from(list(range(1, num_nodes + 1)))
    colours = []
    red_nodes = list(range(1, num_red_nodes + 1))
    blue_nodes = list(range(num_red_nodes + 1, num_nodes + 1))
    for node_index in range(0, num_red_nodes):
        colours.append("red")
    for node_index in range(num_red_nodes, num_nodes):
        colours.append("blue")
    # red_nodes = list(random_combination(regular_graph.nodes(), num_red_nodes))
    # blue_nodes = list(set(regular_graph.nodes()) - set(red_nodes))
    # colours = []
    # for node_index in range(1, num_nodes + 1):
    #     if node_index in red_nodes:
    #         colours.append("red")
    #     else:
    #         colours.append("blue")
    regular_graph = add_initial_edges(regular_graph, blue_nodes, red_nodes, k)
    plot_graph(regular_graph, colours)
    add_extra_blue_edges(regular_graph, blue_nodes, k, k_blue_nodes)
    plot_graph(regular_graph, colours)
    if k_red_nodes % 2 == 0 or num_red_nodes % 2 == 0:
        regular_graph = add_regular_subgraph(regular_graph, red_nodes, k_red_nodes)
        plot_graph(regular_graph, colours)
    if k_blue_nodes % 2 == 0 or num_blue_nodes % 2 == 0:
        regular_graph = add_regular_subgraph(regular_graph, blue_nodes, k_blue_nodes)
        plot_graph(regular_graph, colours)
    if k_red_nodes % 2 == 1 and num_red_nodes % 2 == 1:
        k_red_temp = k_red_nodes - 1
        regular_graph = add_regular_subgraph(regular_graph, red_nodes, k_red_temp)
        plot_graph(regular_graph, colours)
        if k_blue_nodes > 0:
            k_blue_temp = k_blue_nodes - 1
            regular_graph = add_regular_subgraph(regular_graph, blue_nodes, k_blue_temp)
            plot_graph(regular_graph, colours)
        ordered_blue_nodes = order_by_number_of_edges(regular_graph, blue_nodes)
        blue_least_edges = ordered_blue_nodes[0][0]
        red_without_unconnected_red = []
        for red_node in red_nodes:
            if not (blue_least_edges, red_node) in regular_graph.edges() and not (red_node,
                                                                                  blue_least_edges) in regular_graph.edges():
                red_without_unconnected_red = red_nodes.copy()
                red_without_unconnected_red.remove(red_node)
                regular_graph.add_edge(blue_least_edges, red_node)
                break
        blue_without_blue_least_edges = blue_nodes.copy()
        blue_without_blue_least_edges.remove(blue_least_edges)
        if k_blue_nodes > 0:
            regular_graph = add_unconnected_less_than_k_edges(regular_graph, blue_without_blue_least_edges, k)
            plot_graph(regular_graph, colours)
        regular_graph = add_unconnected_less_than_k_edges(regular_graph, red_without_unconnected_red, k)
    plot_graph(regular_graph, colours)
    if not nx.is_k_regular(regular_graph, k):
        print("The construction of the graph went wrong, the graph is not k-regular.")
    # Check if the graph is connected or exists of multiple subgraphs.
    if len(list(nx.connected_components(regular_graph))) > 1:
        print("There are multiple subgraphs.")
        # Find two connected red nodes per subgraph and remove the edge between those nodes.
        connected_red_nodes_per_subgraph = []
        for subgraph in list(nx.connected_components(regular_graph)):
            regular_graph, red_node, red_node2 = find_two_connected_red_nodes_in_subgraph(regular_graph, subgraph,
                                                                                          colours)
            connected_red_nodes_per_subgraph.append([red_node, red_node2])
            print("connected red nodes per subgraph:", connected_red_nodes_per_subgraph)
        # Connect node 2 of subgraph i to node 1 of subgraph i + 1  where i \in [0,
        # len(connected_red_nodes_per_subgraph) - 1]
        for index in range(len(connected_red_nodes_per_subgraph)):
            regular_graph.add_edge(connected_red_nodes_per_subgraph[index][1],
                                   connected_red_nodes_per_subgraph[
                                       (index + 1) % len(connected_red_nodes_per_subgraph)][0])
            print("Added edge:", connected_red_nodes_per_subgraph[index][1],
                  connected_red_nodes_per_subgraph[(index + 1) % len(connected_red_nodes_per_subgraph)][0])
        if nx.is_k_regular(regular_graph, k) and len(list(nx.connected_components(regular_graph))) == 1:
            print("A k-regular graph has been found.")
        plot_graph(regular_graph, colours)
    return regular_graph, colours


#
# # The values of the number of nodes n and the degree d need to meet the requirements of prop. 7 & 8 of Venema-Los et al. (2023)
# def create_values_n_d_according_to_requirements():
#     nodes_list = []
#     degree_list = []
#     deg = 3  # Lowest possible degree.
#     n = 2 * (3 * deg + 1) / (deg - 1)  # Lowest possible number of nodes for degree 3.
#     return nodes_list, degree_list


if __name__ == "__main__":
    # nodes, degree = create_values_n_d_according_to_requirements()
    create_regular_maj_maj_ill_graph(14, 4)
