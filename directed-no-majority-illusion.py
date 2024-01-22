import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import random


# Create a random directed graph using a specified number of nodes.
def create_random_directed_graph(nodes):
    graph = nx.scale_free_graph(nodes)
    temp_graph = graph.copy()
    for node in graph.nodes():
        neigbours = list(graph.neighbors(node))
        if not neigbours:
            temp_graph = graph.copy()
            temp_graph.add_edge(node, random.randint(0, len(graph.nodes())))
    graph = temp_graph.copy()
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

if __name__ == "__main__":
    colour_majority_illusion = True
    while colour_majority_illusion:
        digraph = create_random_directed_graph(6)
        colourings = all_colour_options_graph(digraph)
        # For each colouring check which nodes are under majority illusion
        weak_node_illusion = True
        weak_global_illusion = False
        for col in colourings:
            print(col)
            majority_illusion_colouring = []
            for agent in digraph.nodes():
                majority_illusion_node = check_majority_illusion_node(digraph, agent, col, weak_node_illusion)
                majority_illusion_colouring.append(majority_illusion_node)
            majority_majority_illusion = most_frequent(majority_illusion_colouring)
            if majority_majority_illusion == "tie":
                if weak_global_illusion:
                    print("There is a majority-(weak)-majority illusion")
                    colour_majority_illusion = True
                else:
                    print("There is NO majority-(weak)-majority illusion")
            else:
                if majority_majority_illusion:
                    print("There is a majority-(weak)-majority illusion")
                    colour_majority_illusion = True
                else:
                    print("There is NO majority-(weak)-majority illusion")

        print(colour_majority_illusion)
        if colour_majority_illusion:
            print("For this graph, there exists some colouring that leads to a majority-weak-majority illusion")
        else:
            print("For this graph, there DOES NOT exist a colouring that leads to a majority-weak-majority illusion")
            print(digraph.nodes)
            print(digraph.edges)
            # Plot the graph using the first colour list
            nx.draw(digraph, node_color=colourings[0])
            plt.show()




