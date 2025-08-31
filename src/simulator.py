import networkx as nx
import random

class Simulation:
    def __init__(self, smart_grid):
        self.grid = smart_grid.get_grid()
        self.failed_nodes = set()

    def simulate_power_flow(self, source, targets, demands):
        super_sink = 'super_sink'

        temp_graph = self.grid.copy()
        temp_graph.add_node(super_sink)

        # Connect homes to super_sink with edges weighted by demand
        for home in targets:
            demand = demands.get(home, 0)
            if temp_graph.has_node(home):  # Important: check node exists (not failed)
                temp_graph.add_edge(home, super_sink, capacity=demand)

        # Run max flow from source to super_sink
        flow_value, flow_dict = nx.maximum_flow(temp_graph, source, super_sink, capacity='capacity')

        # Check connectivity: homes reachable from source
        connectivity = {home: nx.has_path(temp_graph, source, home) for home in targets if temp_graph.has_node(home)}

        total_demand = sum(demands.values())

        success = flow_value >= total_demand and all(connectivity.values())

        return success, flow_value, flow_dict, connectivity

    def fail_node(self, node):
        if node in self.grid.nodes:
            self.grid.nodes[node]['status'] = 'failed'  # Mark node as failed
            self.failed_nodes.add(node)  # Track failed nodes
            return True
        return False

    def fail_edge(self, from_node, to_node):
        if self.grid.has_edge(from_node, to_node):
            self.grid[from_node][to_node]['status'] = 'failed'  # Mark edge as failed
            return True
        return False

    def repair_node(self, node):
        if node in self.grid.nodes:
            self.grid.nodes[node]['status'] = 'active'
            if node in self.failed_nodes:
                self.failed_nodes.remove(node)
            return True
        return False

    def repair_edge(self, from_node, to_node):
        if self.grid.has_edge(from_node, to_node):
            self.grid[from_node][to_node]['status'] = 'active'
            return True
        return False

    def repair_failed_nodes(self, repair_prob=0.3):
        repaired = []
        for node in list(self.failed_nodes):
            if random.random() < repair_prob:
                self.repair_node(node)
                repaired.append(node)
                print(f"Node {node} repaired.")
        return repaired
