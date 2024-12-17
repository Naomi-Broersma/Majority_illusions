
import random
from collections import Counter
import networkx as nx
from matplotlib import pyplot as plt

import regular_graph_maj_maj_illusion
from regular_graph_maj_maj_illusion import create_regular_maj_maj_ill_graph


# Create a random directed graph using a specified number of nodes.
def create_random_directed_graph(nodes):
    # graph = nx.scale_free_graph(nodes)
    graph = nx.random_k_out_graph(nodes, 3, alpha=0.5, self_loops=False)
    temp_graph = graph.copy()
    for node in graph.nodes():
        neighbours = list(graph.neighbors(node))
        temp_graph = graph.copy()
        # Make sure the digraph does not contain multiple edges between 2 nodes
        for neighbour in neighbours:
            counter = 0
            for edge in temp_graph.edges():  # Loop over the edges
                if edge == (node, neighbour):  # Count how many times the current (node,neighbour) edge appears
                    counter = counter + 1
            while counter > 1:  # While there is more than 1 of the same (node, neighbour) edge, remove the edge
                temp_graph.remove_edges_from([(node, neighbour)])
                counter = counter - 1
        if node in neighbours:  # Remove self-loops
            temp_graph.remove_edges_from([(node, node)])
            neighbours.remove(node)
        graph = temp_graph.copy()
        if not neighbours:  # Ensure every node has a neighbour
            temp_graph = graph.copy()
            random_node = random.randint(0, len(graph.nodes()))
            if random_node != node:
                temp_graph.add_edge(node, random_node)
    graph = temp_graph.copy()
    # nx.draw(graph)
    # plt.show()
    return graph


# Create all possible ways to colour a graph using two colours
def all_colour_options_graph(graph):
    colour_list = [[]]
    # Loop over the nodes
    for node in range(len(graph.nodes)):
        temp_colours = []
        # Loop over the colour lists so far
        for item in colour_list:
            # Add each of the 2 colours to all the colour lists so far
            for colour in ["blue", "red"]:
                temp_colour_list = item.copy()
                temp_colour_list.append(colour)
                temp_colours.append(temp_colour_list)
        # Update the colour lists so far using the temporary list
        colour_list = temp_colours
    return colour_list


# Returns the most frequent occurrence or a tie. Only works for 2 different elements in the list.
def most_frequent(majority_list):
    # Create a counter over the given list
    occurrence_count = Counter(majority_list)
    most_common_elem_count = occurrence_count.most_common(1)[0]
    # If there are multiple elements, compare the counter of the two elements
    if len(occurrence_count.most_common()) > 1:
        second_most_common_elem_count = occurrence_count.most_common(2)[1]
        # Check if there is a tie
        if most_common_elem_count[1] == second_most_common_elem_count[1]:
            result = "tie"
        else:  # The first element in the counter is the most common
            result = most_common_elem_count[0]
    else:
        result = most_common_elem_count[0]
    return result


# Check for a given node, graph and colouring whether there is a majority illusion for that node.
def check_majority_illusion_node(graph, node, colouring):
    neighbours = list(graph.neighbors(node))
    # Determine the global opinion
    majority_colouring_global = most_frequent(colouring)
    colours_neighbours = []
    for neighbour in neighbours:  # Note: neighbour - 1, since the labels of nodes start at 1 here.
        colours_neighbours.append(colouring[neighbour - 1])
    if colours_neighbours:
        # Determine the local opinion
        majority_colour_neighbours = most_frequent(colours_neighbours)
    else:  # If there are no neighbours, the agent sees a tie.
        majority_colour_neighbours = "tie"
    # The node is not under majority illusion if either globally or locally there is a tie
    if majority_colour_neighbours == "tie" or majority_colouring_global == "tie":
        illusion = False
        return illusion
    # If the global and local majority is the same, there is no majority illusion for this node
    if majority_colouring_global == majority_colour_neighbours:
        illusion = False
    else:
        illusion = True
    return illusion


# Determine if there is a majority-majority illusion for some colouring
def check_majority_majority_illusion_graph(graph, colouring):
    list_maj_ill_node = []
    for agent in graph.nodes():
        maj_ill_node = check_majority_illusion_node(graph, agent, colouring)
        list_maj_ill_node.append(maj_ill_node)
    majority_majority_illusion = most_frequent(list_maj_ill_node)
    if majority_majority_illusion == "tie":
        majority_majority_illusion = False
    return majority_majority_illusion


# Update step using a majority threshold. The colours of the nodes will be changed to the local majority winner.
def majority_threshold_update(graph, colouring):
    new_colouring_graph = []
    for agent in graph.nodes():
        neighbours = list(graph.neighbors(agent))
        colours_neighbours = []
        for neighbour in neighbours:
            colours_neighbours.append(colouring[neighbour - 1])
        # Determine the local majority winner among the neighbours if there are neighbours.
        if colours_neighbours:
            majority_colour_neighbours = most_frequent(colours_neighbours)
        else:  # If there are no neighbours, the agents sees a tie.
            majority_colour_neighbours = "tie"
        if majority_colour_neighbours == "tie":  # The colour of the node remains the same.
            new_colouring_graph.append(colouring[agent])
        else:  # The colour of the node will be changed to the local majority winner.
            new_colouring_graph.append(majority_colour_neighbours)
    print("Old vs. new colouring:")
    print(colouring)
    print(new_colouring_graph)
    return new_colouring_graph


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


def check_for_randomly_created_graph():
    maj_maj_illusion = False
    graph = nx.empty_graph
    colour_options = []
    while not maj_maj_illusion:
        # Create a random regular graph with 10 nodes and 3 neighbours for each node.
        graph = nx.random_regular_graph(3, 14)
        colour_options = all_colour_options_graph(graph)
        # Check until a colouring with majority-majority illusion has been found
        for colouring_graph in colour_options:
            maj_maj_illusion = check_majority_majority_illusion_graph(graph, colouring_graph)
            # For that colouring do a majority threshold update step
            # if maj_maj_illusion:
            new_colouring = majority_threshold_update(graph, colouring_graph)
            print(maj_maj_illusion)
        # Check if the new graph has certain properties:
        # majority-majority illusion, what colour is global majority winner etc. How often do these properties occur
        # among colourings that are a majority-majority illusion?
    plot_graph(graph, colour_options[0])
    print(graph.nodes())
    print(graph.edges())
    return


# TODO generate a graph with a majority-majority illusion, instead of a random one and then checking for
#  majority-majority illusion.
# Potential approaches:
# - proposition 8 defines n and d for which it is possible to have maj-maj illusion for d-regular undirected graph.
# - theorem 2: for at least one such graph there is a maj-maj illusion, but not necessarily all of them.
if __name__ == "__main__":
    regular_graph, colours = regular_graph_maj_maj_illusion.create_regular_maj_maj_ill_graph(14, 4)
    maj_maj_ill = check_majority_majority_illusion_graph(regular_graph, colours)
    print(maj_maj_ill)
    new_colours = majority_threshold_update(regular_graph, colours)
    plot_graph(regular_graph, new_colours)
    updated_maj_maj_ill = check_majority_majority_illusion_graph(regular_graph, new_colours)
    print(updated_maj_maj_ill)
