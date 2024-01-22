import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter


# Create a random directed graph using a specified number of nodes.
def create_random_directed_graph(nodes):
    graph = nx.gn_graph(nodes)
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

    print(colours)
    # Plot the graph using the first colour list
    nx.draw(graph, node_color=colours[0])
    plt.show()
    return colours

# Returns the most frequent occurence or a tie. Only works for 2 different results.
def most_frequent(majority_list):
    occurence_count = Counter(majority_list)
    print(occurence_count)
    most_common_elem_count = occurence_count.most_common(2)[0]
    second_most_common_elem_count = occurence_count.most_common(2)[1]
    if most_common_elem_count[1] == second_most_common_elem_count[1]:
        print("tie")
        result = "tie"
    else:
        result = most_common_elem_count[0]
    return result

def check_majority_illusion_node(graph, node, colouring):
    illusion = False
    neigbours = list(graph.neighbors(node))
    # print(neigbours)
    # majority_colouring_global = mode(colouring)
    majority_colouring_global, count = Counter(colouring).most_common(1)[0]
    # TODO what if the majority is a tie?
    if len(majority_colouring_global) == 2:
        majority_colouring_global = "tie"
    print(majority_colouring_global)
    colours_neighbours = []
    for neighbour in neigbours:
        colours_neighbours.append(colouring[neighbour])
    # print(colours_neighbours)
    if colours_neighbours:
        # Find most frequent colour.
        majority_colour_neighbours, count = Counter(colours_neighbours).most_common(1)[0]
        # TODO what if the majority is a tie?
        if len(majority_colour_neighbours) == 2:
            majority_colour_neighbours = "tie"
        # majority_colour_neighbours = mode(colours_neighbours)
    else:
        # TODO what if there are no neighbours, currently return false
        return False
    print(majority_colour_neighbours)
    if majority_colouring_global == majority_colour_neighbours:
        illusion = False
    else:
        illusion = True
    print(illusion)
    return illusion

if __name__ == "__main__":
    most_frequent([])
    digraph = create_random_directed_graph(4)
    colourings = all_colour_options_graph(digraph)
    # For each colouring check which nodes are under majority illusion
    # for col in colourings:
    #     majority_illusion_colouring = []
    #     for agent in digraph.nodes():
    #         majority_illusion_node = check_majority_illusion_node(digraph, agent, col)
    #         majority_illusion_colouring.append(majority_illusion_node)
    #     print(majority_illusion_colouring)
    #     majority_majority_illusion = mode(majority_illusion_colouring)
    #     majority_majority_illusion = max(set(majority_illusion_colouring), key=majority_illusion_colouring.count)
    #     # TODO what if the majority is a tie?
    #     # if len(majority_majority_illusion) == 2:
    #     #    majority_colouring_global = "tie"
    #     print(majority_majority_illusion)



