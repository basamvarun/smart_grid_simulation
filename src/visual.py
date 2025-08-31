# src/visualization.py
import matplotlib.pyplot as plt
import networkx as nx

def plot_grid_with_demand_and_failures(grid, demands, failed_nodes=None, flow_dict=None, connectivity=None):
    pos = nx.spring_layout(grid, seed=42)

    node_colors = []
    for node in grid.nodes:
        if failed_nodes and node in failed_nodes:
            node_colors.append('red')
        else:
            node_colors.append('green')

    edge_widths = []
    for u, v in grid.edges:
        flow = 0
        if flow_dict and u in flow_dict and v in flow_dict[u]:
            flow = flow_dict[u][v]
        # Scale edge width for visibility; min width 1
        edge_widths.append(max(1, flow/10))

    nx.draw(grid, pos, node_color=node_colors, edge_color='gray',
            width=edge_widths, with_labels=True, node_size=700, font_weight='bold')

    # Annotate demand
    for node, demand in demands.items():
        if node in pos:
            x, y = pos[node]
            plt.text(x, y - 0.1, f"Demand: {demand} MW",
                     horizontalalignment='center', fontsize=8, fontweight='bold', color='blue')

    # Mark blackouts
    if connectivity:
        for node, is_reachable in connectivity.items():
            if not is_reachable:
                x, y = pos[node]
                plt.scatter(x, y, s=500, marker='x', c='black', label='Blackout' if 'Blackout' not in plt.gca().get_legend_handles_labels()[1] else "")

    plt.title("Smart Grid: Demand, Failures, and Power Flow")
    plt.legend(loc='upper right')
    plt.show()
