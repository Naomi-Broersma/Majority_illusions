import networkx as nx
import matplotlib.pyplot as plt

def create_random_directed_graph(nodes):
    graph = nx.gn_graph(nodes)
    return graph

def all_colour_options_graph(graph):
    color_maps = [["NA" for _ in range(len(graph.nodes))] for _ in range(len(graph.nodes)^2)]
    for idx_row in range(len(graph.nodes)^2):
        for item in range(len(color_maps[idx_row])):
            if idx_row + item % 2 == 0:
                color_maps[idx_row][item] = "red"
            else:
                color_maps[idx_row][item] = "blue"

    print(color_maps)
    nx.draw(graph, node_color=color_maps[0])
    plt.show()
    return

if __name__ == "__main__":
    digraph = create_random_directed_graph(4)
    all_colour_options_graph(digraph)


