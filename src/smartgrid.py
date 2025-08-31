import networkx as nx

class SmartGrid:
    def __init__(self):
        self.grid = nx.DiGraph()

    def add_edge(self, from_node, to_node, capacity_mw, resistance):
        self.grid.add_edge(from_node, to_node, capacity=capacity_mw, resistance=resistance, flow=0.0)

    def add_node(self, node, node_type, **attrs):
        self.grid.add_node(node, type=node_type, **attrs)

    def get_grid(self):
        return self.grid