import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import random


# Create a random directed graph using a specified number of nodes.
def create_random_directed_graph(nodes):
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
        # TODO remove this?
        if not neighbours:  # Ensure every node has a neighbour
            temp_graph = graph.copy()
            random_node = random.randint(0, len(graph.nodes()))
            if random_node != node:
                temp_graph.add_edge(node, random_node)
    graph = temp_graph.copy()
    # nx.draw(graph)
    # plt.show()
    return graph


# Create all possible ways to colour a graph using four colours
def all_colour_options_graph(graph):
    colour_list = [[]]
    # Loop over the nodes
    for node in range(len(graph.nodes)):
        temp_colours = []
        # Loop over the colour lists so far
        for item in colour_list:
            # Add each of the 4 colours to all the colour lists so far
            for colour in ["blue", "red", "yellow", "green"]:
                temp_colour_list = item.copy()
                temp_colour_list.append(colour)
                temp_colours.append(temp_colour_list)
        # Update the colour lists so far using the temporary list
        colour_list = temp_colours
        # print(temp_colours)
    return colour_list


# Change the position of node labels in the plot
def nudge(pos, x_shift, y_shift):
    return {n: (x + x_shift, y + y_shift) for n, (x, y) in pos.items()}


# Plot the graph
def plot_graph(graph, colour_map):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, with_labels=False, pos=pos, ax=ax, node_color=colour_map, arrowsize=20)  # default labeling
    pos_nodes = nudge(pos, 0, 0.1)
    nx.draw_networkx_labels(graph, pos=pos_nodes, ax=ax, font_size=16)
    plt.show()
    return


# Returns the most frequently occurring colour or multiple colours.
def most_frequent(agent_colours):
    # Create a counter over the given list
    occurrence_count = Counter(agent_colours)
    most_common_elem_count = occurrence_count.most_common(1)[0]
    frequency_most_frequent = most_common_elem_count[1]
    # If there are multiple colours, compare the counter of the colours
    list_frequent_colours = []
    if len(occurrence_count) > 1:
        amount_of_colours = len(occurrence_count)
        # For each of the colours, add it to the list of most frequent colours if its frequency of appearing is the
        # same as the most frequently occurring colour.
        for colour in range(amount_of_colours):
            colour_occurrence = occurrence_count.most_common()[colour][1]
            if colour_occurrence == frequency_most_frequent:
                list_frequent_colours.append(occurrence_count.most_common()[colour][0])
    else:
        list_frequent_colours = [occurrence_count.most_common(1)[0][0]]
    return list_frequent_colours


# Check for a given node, graph and colouring whether there is a plurality illusion for that node.
def check_plurality_illusion_node(graph, node, colouring):
    # Determine the global opinion
    plurality_winner_global = most_frequent(colouring)
    neighbours = list(graph.neighbors(node))
    colours_neighbours = []
    for neighbour in neighbours:
        colours_neighbours.append(colouring[neighbour])
    if colours_neighbours:
        # Determine the local plurality winner
        plurality_winner_neighbours = most_frequent(colours_neighbours)
    else:
        plurality_winner_neighbours = []
    # print(plurality_winner_neighbours)
    # print(plurality_winner_global)
    # TODO double-check if this works for empty set of local winners.
    # If you require a strict plurality illusion, then there is no overlap between local and global plurality winners.
    plurality_illusion = True
    for winner in plurality_winner_neighbours:
        if winner in plurality_winner_global:
            plurality_illusion = False
            break
    # If you require a weak plurality illusion, then the local and global plurality winners cannot be exactly the same.
    weak_plurality_illusion = True
    if sorted(plurality_winner_global) == sorted(plurality_winner_neighbours):
        weak_plurality_illusion = False
    return plurality_illusion, weak_plurality_illusion


# Determine which colours appear more than a quota-fraction.
def determine_quota_winner(agent_colours, quota):
    quota_winner = []
    occurrence_count = Counter(agent_colours)
    # Loop over all colours and their counters.
    for item in occurrence_count.most_common():
        # Determine the fraction of agents that has this colour and if more than the quota, add the colour as a quota
        # winner.
        fraction = item[1] / len(agent_colours)
        if fraction > quota:
            quota_winner.append(item[0])
    return quota_winner


# Check for a given node, graph and colouring whether there is a quota illusion for that node.
def check_quota_illusion_node(graph, node, colouring, quota):
    # Determine the global quota winners.
    quota_winner_global = determine_quota_winner(colouring, quota)
    # Determine the neighbours of the node and which colour is the local quota winner.
    neighbours = list(graph.neighbors(node))
    colours_neighbours = []
    for neighbour in neighbours:
        colours_neighbours.append(colouring[neighbour])
    if colours_neighbours:
        # Determine the local quota winners.
        quota_winner_neighbours = determine_quota_winner(colours_neighbours, quota)
    else:
        quota_winner_neighbours = []

    # If you require a strict quota illusion, then there is no overlap between local and global quota winners and the
    # local quota winner and global winner cannot be empty sets.
    quota_illusion = True
    if not quota_winner_neighbours or not quota_winner_global:
        quota_illusion = False
    else:
        for winner in quota_winner_neighbours:
            if winner in quota_winner_global:
                quota_illusion = False
                break
    # If you require a weak quota illusion, then the local and global quota winners cannot be exactly the same.
    weak_quota_illusion = True
    if sorted(quota_winner_global) == sorted(quota_winner_neighbours):
        weak_quota_illusion = False
    return quota_illusion, weak_quota_illusion


# TODO loop through the different colourings and call the illusion functions for each colouring


if __name__ == "__main__":
    digraph = create_random_directed_graph(7)
    colour_options = all_colour_options_graph(digraph)
    # for colours in colour_options:
    #     plot_graph(digraph, colours)
    for agent in digraph.nodes():
        print("NEW node")
        plurality_ill, weak_plurality_ill = check_plurality_illusion_node(digraph, agent, colour_options[3])
        print(plurality_ill, weak_plurality_ill)
        quota_ill, weak_quota_ill = check_quota_illusion_node(digraph, agent, colour_options[3], 0.5)
        print(quota_ill, weak_quota_ill)
