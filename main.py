import pandas as pd
import random
from src.smartgrid import SmartGrid
from src.simulator import Simulation
from src.pricing import Pricing
from src.renewables import Renewables



def load_hourly_demand(csv_path, hour, grid):
    df = pd.read_csv(csv_path)
    active_homes = [n for n in grid.grid.nodes if grid.grid.nodes[n].get('status', 'active') == 'active' and grid.grid.nodes[n]['type'] == 'home']
    demand = {}
    for home in active_homes:
        if home in df.columns:
            demand[home] = df.loc[df['Hour'] == hour, home].values[0]
    return demand


def print_simulation_results(hour, demands, solar_gen, wind_gen, available_power, success, flow_value, price, failed_nodes, repaired_nodes):
    print(f"\n=== Hour {hour}:00 Simulation ===")
    print("\nDemands (MW):")
    for home, demand in demands.items():
        print(f"  {home:<6}: {demand:.2f}")
    print(f"Total Demand     : {sum(demands.values()):.2f} MW")
    print(f"Renewable Output : Solar = {solar_gen:.2f} MW, Wind = {wind_gen:.2f} MW")
    print(f"Available Power  : {available_power:.2f} MW")
    print(f"Power Flow       : {'Success' if success else 'Failure'}")
    print(f"Total Flow       : {flow_value:.2f} MW")
    print(f"Pricing          : ${price:.2f} per MW")
    if failed_nodes:
        print(f"Failed Nodes     : {', '.join(failed_nodes)}")
    else:
        print("Failed Nodes     : None")
    if repaired_nodes:
        print(f"Repaired Nodes   : {', '.join(repaired_nodes)}")
    else:
        print("Repaired Nodes   : None")
    print("-" * 40)


def main():
    csv_path = "data/data_hist.csv"

    # Initialize grid
    grid = SmartGrid()

    # Add nodes
    grid.add_node('Gen1', 'generator')
    grid.add_node('Sub1', 'substation')
    grid.add_node('Sub2', 'substation')
    grid.add_node('Home1', 'home')
    grid.add_node('Home2', 'home')
    grid.add_node('Home3', 'home')
    grid.add_node('Home4', 'home') 
    grid.add_node('Home5', 'home')  

    # Helper to add edges and set as active
    def add_active_edge(u, v, capacity):
        grid.add_edge(u, v, capacity_mw=capacity, resistance=0.005)
        grid.grid[u][v]['status'] = 'active'

    # Add edges
    add_active_edge('Gen1', 'Sub1', 100)
    add_active_edge('Gen1', 'Sub2', 100)
    add_active_edge('Sub1', 'Home1', 50)
    add_active_edge('Sub1', 'Home2', 50)
    add_active_edge('Sub2', 'Home3', 50)
    add_active_edge('Sub2', 'Home4', 50) 
    add_active_edge('Sub2', 'Home5', 50)   
    sim = Simulation(grid)
    renewables = Renewables()
    pricing = Pricing()

    for hour in range(500):
        print(f"\n=== Hour {hour}:00 ===")

        # Repair failed nodes probabilistically
        repair_prob = 0.3
        repaired_nodes = sim.repair_failed_nodes(repair_prob)

        # Fail a random active substation probabilistically
        fail_prob = 0.2
        substations = [
            n for n in grid.grid.nodes
            if grid.grid.nodes[n]['type'] == 'substation' and grid.grid.nodes[n].get('status', 'active') == 'active'
        ]
        failed_nodes = []
        if substations and random.random() < fail_prob:
            node_to_fail = random.choice(substations)
            sim.fail_node(node_to_fail)
            failed_nodes.append(node_to_fail)

        # Load demands only for active homes
        demands = load_hourly_demand(csv_path, hour, grid)
        total_demand = sum(demands.values())

        # Calculate renewable generation (solar + wind)
        solar_gen = renewables.solar_power(hour)
        wind_gen = renewables.wind_power()
        available_power = 100 + solar_gen + wind_gen

        # Update Gen1 edge capacities, ignore failed edges
        for u, v, data in grid.grid.edges(data=True):
            if u == 'Gen1' and data.get('status', 'active') == 'active':
                data['capacity'] = available_power / 2  # split for two edges

        # Simulate power flow on active homes
        active_homes = list(demands.keys())
        success, flow_value, flow_dict, connectivity = sim.simulate_power_flow('Gen1', active_homes, demands)

        # Compute dynamic pricing
        peak_threshold = 80
        price = pricing.get_price(total_demand, peak_threshold)

        # Print structured simulation results
        print_simulation_results(
            hour, demands, solar_gen, wind_gen, available_power,
            success, flow_value, price, failed_nodes, repaired_nodes
        )


if __name__ == "__main__":
    main()
