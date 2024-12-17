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
    print(colouring)
    print(neighbours)
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


# Check for a graph whether there is a (weak)-1/k-(weak)-quota illusion.
def quota_illusion_graph(graph, graph_colouring, quota, k):
    quota_illusion_counter = 0
    weak_quota_illusion_counter = 0
    # Loop over the nodes and count the number of nodes under (weak-)quota illusion.
    for node in graph.nodes():
        quota_illusion_node, weak_quota_illusion_node = check_quota_illusion_node(graph, node, graph_colouring, quota)
        if quota_illusion_node:
            quota_illusion_counter = quota_illusion_counter + 1
        if weak_quota_illusion_node:
            weak_quota_illusion_counter = weak_quota_illusion_counter + 1
    # Determine the fraction of nodes that are under (weak)-quota illusion.
    quota_illusion_fraction = quota_illusion_counter / len(graph.nodes())
    weak_quota_illusion_fraction = weak_quota_illusion_counter / len(graph.nodes())
    k_fraction_quota_illusion = False
    weak_k_fraction_quota_illusion = False
    k_fraction_weak_quota_illusion = False
    weak_k_fraction_weak_quota_illusion = False
    # Check all instances where there is a (weak)-1/k-weak-quota illusion.
    if quota_illusion_fraction > 1 / k:
        k_fraction_quota_illusion = True
        weak_k_fraction_quota_illusion = True
    if quota_illusion_fraction == 1 / k:
        weak_k_fraction_quota_illusion = True
    if weak_quota_illusion_fraction > 1 / k:
        k_fraction_weak_quota_illusion = True
        weak_k_fraction_weak_quota_illusion = True
    if weak_quota_illusion_fraction == 1 / k:
        weak_k_fraction_weak_quota_illusion = True
    return k_fraction_quota_illusion, k_fraction_weak_quota_illusion, weak_k_fraction_quota_illusion, weak_k_fraction_weak_quota_illusion


# Check for a graph whether there is a (weak)-1/k-(weak)-plurality illusion.
def plurality_illusion_graph(graph, graph_colouring, k):
    plurality_illusion_counter = 0
    weak_plurality_illusion_counter = 0
    # Loop over the nodes and count the number of nodes under (weak-)quota illusion.
    for node in graph.nodes():
        plurality_illusion_node, weak_plurality_illusion_node = check_plurality_illusion_node(graph, node,
                                                                                              graph_colouring)
        if plurality_illusion_node:
            plurality_illusion_counter = plurality_illusion_counter + 1
        if weak_plurality_illusion_node:
            weak_plurality_illusion_counter = weak_plurality_illusion_counter + 1
    # Determine the fraction of nodes that are under (weak)-quota illusion.
    plurality_illusion_fraction = plurality_illusion_counter / len(graph.nodes())
    weak_plurality_illusion_fraction = weak_plurality_illusion_counter / len(graph.nodes())
    k_fraction_plurality_illusion = False
    weak_k_fraction_plurality_illusion = False
    k_fraction_weak_plurality_illusion = False
    weak_k_fraction_weak_plurality_illusion = False
    # Check all instances where there is a (weak)-1/k-weak-plurality illusion.
    if plurality_illusion_fraction > 1 / k:
        k_fraction_plurality_illusion = True
        weak_k_fraction_plurality_illusion = True
    if plurality_illusion_fraction == 1 / k:
        weak_k_fraction_plurality_illusion = True
    if weak_plurality_illusion_fraction > 1 / k:
        k_fraction_weak_plurality_illusion = True
        weak_k_fraction_weak_plurality_illusion = True
    if weak_plurality_illusion_fraction == 1 / k:
        weak_k_fraction_weak_plurality_illusion = True
    return k_fraction_plurality_illusion, k_fraction_weak_plurality_illusion, weak_k_fraction_plurality_illusion, weak_k_fraction_weak_plurality_illusion


# For each possible colouring of the graph, check if there exists a (weak-)1/k-(weak)-quota illusion.
# Stop if a 1/k-(weak)-quota illusion has been found.
def quota_illusion_check_per_colouring(graph, graph_colourings, quota, k):
    k_fraction_weak_quota = False
    time = 0
    # Check for each colouring if there is a (weak-)1/k-(weak)-quota illusion
    for colouring in graph_colourings:
        print(time, "/", len(graph_colourings))
        (k_fraction_quota_illusion, k_fraction_weak_quota_illusion, weak_k_fraction_quota_illusion,
         weak_k_fraction_weak_quota_illusion) = quota_illusion_graph(graph, colouring, quota, k)
        # Stop if a 1/k-weak-q illusion has been found.
        if k_fraction_weak_quota_illusion:
            k_fraction_weak_quota = True
            break
        time = time + 1
    if k_fraction_weak_quota:
        print("A 1/k-weak-quota illusion has been found.")
        plot_graph(graph, graph_colourings[time])
    else:
        print("There does not exist a 1/k-weak-quota illusion for any of the possible colourings of the graph.")
        plot_graph(graph, graph_colourings[0])
    return


# For each possible colouring of the graph, check if there exists a (weak-)1/k-(weak)-plurality illusion.
# Stop if a 1/k-(weak)-plurality illusion has been found.
def plurality_illusion_check_per_colouring(graph, graph_colourings, k):
    k_fraction_weak_plurality = False
    time = 0
    # For each colouring check is there is a (weak-)1/k-(weak)-plurality illusion.
    for colouring in graph_colourings:
        print(time, "/", len(graph_colourings))
        (k_fraction_plurality_illusion, k_fraction_weak_plurality_illusion, weak_k_fraction_plurality_illusion,
         weak_k_fraction_weak_plurality_illusion) = plurality_illusion_graph(graph, colouring, k)
        # Stop if a 1/k-weak-plurality illusion has been found.
        if k_fraction_weak_plurality_illusion:
            k_fraction_weak_plurality = True
            break
        time = time + 1
    if k_fraction_weak_plurality:
        print("A 1/k-weak-plurality illusion has been found.")
        # plot_graph(graph, graph_colourings[time])
    else:
        print("There does not exist a 1/k-weak-plurality illusion for any of the possible colourings of the graph.")
        # plot_graph(graph, graph_colourings[0])
    return k_fraction_weak_plurality


if __name__ == "__main__":
    check_plurality = True
    while check_plurality:
        digraph = create_random_directed_graph(7)
        colour_options = all_colour_options_graph(digraph)
        # print("Checking for quota illusions.")
        # quota_illusion_check_per_colouring(digraph, colour_options, 0.5, 4)
        print("Checking for plurality illusions.")
        k_fraction_weak_plur = plurality_illusion_check_per_colouring(digraph, colour_options, 4)
        if not k_fraction_weak_plur:
            check_plurality = False
            plot_graph(digraph, colour_options[0])
            print(digraph.nodes())
            print(digraph.edges())
