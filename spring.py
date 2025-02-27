import networkx as nx
import matplotlib.pyplot as plt
import sys
import numpy as np


def read_metis(filename):
    """Reads a METIS format graph file (assuming no weights, 1-indexed)."""
    with open(filename, "r") as f:
        header = f.readline().strip().split()
        n, m = int(header[0]), int(header[1])
        G = nx.Graph()
        G.add_nodes_from(range(1, n + 1))  # 1-indexed
        for i in range(1, n + 1):
            line = f.readline().strip()
            neighbors = [int(x) for x in line.split()] if line else []
            for neighbor in neighbors:
                if not G.has_edge(i, neighbor):
                    G.add_edge(i, neighbor)
    return G


def read_partition_file(partition_file):
    """Reads partition file where each line is a partition ID for corresponding vertex."""
    with open(partition_file, "r") as f:
        return [int(line.strip()) for line in f if line.strip()]


def group_layout(G, partitions):
    """Creates a layout where nodes of the same partition are closer together."""
    base_pos = nx.spring_layout(G, seed=42)  # Initial layout

    num_parts = max(partitions) + 1
    cluster_offsets = np.linspace(-1, 1, num_parts)  # Spread partitions along x-axis

    pos = {}
    for node, part in zip(G.nodes(), partitions):
        x, y = base_pos[node]
        pos[node] = (x + cluster_offsets[part], y)  # Shift nodes in the same partition

    return pos


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python script.py <graph_file> <num_parts> [optional_note] [--show]"
        )
        sys.exit(1)

    graph_filename = sys.argv[1]
    num_parts = int(sys.argv[2])
    note, show_image = "", False

    for arg in sys.argv[3:]:
        if arg == "--show":
            show_image = True
        else:
            note = arg

    partition_filename = f"{graph_filename}.parts.{num_parts}"
    save_filename = (
        f"{graph_filename}_partition_{num_parts}{'_' + note if note else ''}.png"
    )

    G = read_metis(graph_filename)
    partitions = read_partition_file(partition_filename)

    color_map = [partitions[node - 1] for node in G.nodes()]  # 1-indexed
    pos = group_layout(G, partitions)  # Improved layout

    plt.figure(figsize=(10, 8))

    # Draw edges, highlighting cuts
    edge_colors = [
        "red" if partitions[u - 1] != partitions[v - 1] else "gray"
        for u, v in G.edges()
    ]
    nx.draw_networkx_edges(G, pos, alpha=0.5, edge_color=edge_colors)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=color_map, cmap=plt.cm.jet, node_size=300)
    nx.draw_networkx_labels(G, pos, font_size=8, font_color="white")

    plt.title(f"Graph Partition Visualization ({num_parts} Parts)")
    plt.axis("off")

    plt.savefig(save_filename, dpi=300, bbox_inches="tight")
    print(f"Graph saved as {save_filename}")

    if show_image:
        plt.show()
