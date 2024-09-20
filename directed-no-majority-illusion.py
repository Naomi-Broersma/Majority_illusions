import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import random


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
        if not neighbours: # Ensure every node has a neighbour
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
    colours = [[]]
    # Loop over the nodes
    for node in range(len(graph.nodes)):
        temp_colours = []
        # Loop over the colour lists so far
        for item in colours:
            # For each colour list add blue and append that to a temporary list
            blue_temp = item.copy()
            blue_temp.append("blue")
            temp_colours.append(blue_temp)
            # For each colour list add red and append that to a temporary list
            red_temp = item.copy()
            red_temp.append("red")
            temp_colours.append(red_temp)
        # Update the colour lists so far using the temporary list
        colours = temp_colours
    return colours

# Returns the most frequent occurence or a tie. Only works for 2 different elements in the list.
def most_frequent(majority_list):
    # Create a counter over the given list
    occurence_count = Counter(majority_list)
    most_common_elem_count = occurence_count.most_common(1)[0]
    # If there are multiple elements, compare the counter of the two elements
    if len(occurence_count.most_common()) > 1:
        second_most_common_elem_count = occurence_count.most_common(2)[1]
        # Check if there is a tie
        if most_common_elem_count[1] == second_most_common_elem_count[1]:
            result = "tie"
        else: # The first element in the counter is the most common
            result = most_common_elem_count[0]
    else:
        result = most_common_elem_count[0]
    return result

# Check for a given node, graph and colouring whether there is a majority illusion for that node.
# Boolean weak is used to determine what should happen in cases with ties in the local or global opinion.
def check_majority_illusion_node(graph, node, colouring, weak):
    neigbours = list(graph.neighbors(node))
    # Determine the global opinion
    majority_colouring_global = most_frequent(colouring)
    colours_neighbours = []
    for neighbour in neigbours:
        colours_neighbours.append(colouring[neighbour])
    if colours_neighbours:
        # Determine the local opinion
        majority_colour_neighbours = most_frequent(colours_neighbours)
    else:
        # TODO what if there are no neighbours, currently return false
        return False
    # If you require a strict majority illusion, then there is no illusion if either globally or locally there is a tie
    if not weak and (majority_colour_neighbours == "tie" or majority_colouring_global == "tie"):
        illusion = False
        return illusion
    # If the global and local majority is the same, there is no majority illusion for this node
    if majority_colouring_global == majority_colour_neighbours:
        illusion = False
    else:
        illusion = True
    return illusion

# Check for graphs whether there is a majority-weak-majority illusion for each colouring.
# Prints the colourings for which this is the case or plots the graph if no such colouring exists.
def general_graph_check(graph, weak_illusion_node, weak_illusion_global):
    colour_majority_illusion = False
    colourings = all_colour_options_graph(graph)
    # For each colouring check which nodes are under majority illusion
    for col in colourings:
        majority_illusion_colouring = []
        for agent in graph.nodes():
            majority_illusion_node = check_majority_illusion_node(graph, agent, col, weak_illusion_node)
            majority_illusion_colouring.append(majority_illusion_node)
        majority_majority_illusion = most_frequent(majority_illusion_colouring)
        if majority_majority_illusion == "tie":
            if weak_illusion_global:
                print(col)
                print("There is a weak-majority-(weak)-majority illusion")
                colour_majority_illusion = True
            # else:
            #    print("There is NO weak-majority-(weak)-majority illusion")
        else:
            if majority_majority_illusion:
                print(col)
                print("There is a majority-(weak)-majority illusion")
                colour_majority_illusion = True
            # else:
            #    print("There is NO majority-(weak)-majority illusion")

    if colour_majority_illusion:
        print("For this graph, there exists some colouring that leads to a majority-weak-majority illusion")
    else:
        print("For this graph, there DOES NOT exist a colouring that leads to a majority-weak-majority illusion")
        print(graph.nodes)
        print(graph.edges)
        # Plot the graph using the first colour list
        plot_graph(graph, colourings[0])
    return colour_majority_illusion

def create_3_cycle():
    graph = nx.DiGraph()
    graph.add_nodes_from([0,1,2])
    graph.add_edges_from([(0,1),(1,2),(2,0)])
    return graph

# Change the position of node labels in the plot
def nudge(pos, x_shift, y_shift):
    return {n:(x + x_shift, y + y_shift) for n,(x,y) in pos.items()}

# Plot the network in a nice way.
def plot_graph(graph, colour_map):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, with_labels=False, pos=pos, ax=ax, node_color=colour_map, arrowsize=20)  # default labeling
    pos_nodes = nudge(pos, 0, 0.1)
    nx.draw_networkx_labels(graph, pos=pos_nodes, ax=ax, font_size=16)
    plt.show()
    return

if __name__ == "__main__":
    weak_node_illusion = True
    weak_global_illusion = False
    # cycle = create_3_cycle()
    # general_graph_check(cycle, weak_node_illusion, weak_global_illusion)

    # Keeps checking generated graphs until one has been found without a majority-weak-majority illusion.
    graph_majority_illusion = True
    while graph_majority_illusion:
        digraph = create_random_directed_graph(7)
        graph_majority_illusion = general_graph_check(digraph, weak_node_illusion, weak_global_illusion)





