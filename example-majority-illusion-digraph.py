import networkx as nx
from matplotlib import pyplot as plt


def nudge(position, x_shift, y_shift):
    return {n: (x + x_shift, y + y_shift) for n, (x, y) in position.items()}


if __name__ == "__main__":
    graph = nx.DiGraph()
    graph.add_nodes_from([1, 2, 3, 4])
    graph.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 1), (2, 4), (3, 4), (3, 2), (4, 2)])
    colour_map = ["blue", "red", "blue", "blue"]
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, with_labels=False, pos=pos, ax=ax, node_color=colour_map, arrowsize=20)  # default labeling
    pos_nodes = nudge(pos, 0, 0.1)
    nx.draw_networkx_labels(graph, pos=pos_nodes, ax=ax, font_size=16)
    plt.show()
