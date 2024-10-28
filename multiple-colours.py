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
            for edge in temp_graph.edges(): # Loop over the edges
                if edge == (node, neighbour): # Count how many times the current (node,neighbour) edge appears
                    counter = counter + 1
            while counter > 1: # While there is more than 1 of the same (node, neighbour) edge, remove the edge
                temp_graph.remove_edges_from([(node, neighbour)])
                counter = counter - 1
        if node in neighbours: # Remove self-loops
            temp_graph.remove_edges_from([(node, node)])
            neighbours.remove(node)
        graph = temp_graph.copy()
        # TODO remove this?
        if not neighbours: # Ensure every node has a neighbour
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
        print(temp_colours)
    return colour_list


# Change the position of node labels in the plot
def nudge(pos, x_shift, y_shift):
    return {n:(x + x_shift, y + y_shift) for n,(x,y) in pos.items()}


# Plot the graph
def plot_graph(graph, colour_map):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, with_labels=False, pos=pos, ax=ax, node_color=colour_map, arrowsize=20)  # default labeling
    pos_nodes = nudge(pos, 0, 0.1)
    nx.draw_networkx_labels(graph, pos=pos_nodes, ax=ax, font_size=16)
    plt.show()
    return

# TODO determine if plurality illusion

# TODO determine if quota illusion

# TODO loop through the different colourings and call the illusion functions for each colouring


# TODO create main function that calls other functions
if __name__ == "__main__":
    digraph = create_random_directed_graph(7)
    colour_options = all_colour_options_graph(digraph)
    # for colours in colour_options:
    #     plot_graph(digraph, colours)


