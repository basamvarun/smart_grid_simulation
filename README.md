SmartGridSim: Renewable Energy Distribution and Resilience Simulator
Project Overview
SmartGridSim is a Python-based simulation platform modeling a smart electrical grid integrating renewable energy sources, dynamic demand, and grid failures. It enables detailed analysis of power flow, renewable generation variability, and pricing strategies to optimize grid reliability and economics.

Features
Simulation of energy distribution between 1 generator, 2 substations, and 5 residential homes.

Utilizes 504+ hours of historical household electricity demand data.

Models solar and wind renewable generation affecting available supply dynamically.

Implements stochastic failure and probabilistic repair of substations to test grid resilience.

Calculates real-time dynamic pricing based on demand thresholds.

Employs NetworkX for graph-based max-flow power flow simulations.

Modular and extensible architecture to support future grid expansions and more complex scenarios.

Detailed hourly simulation reports on demand, generation, power flow success, pricing, failures, and repairs.

Technologies Used
Python 3.x

NetworkX (Graph modeling)

Pandas (Data processing)

NumPy (Numerical operations)

Matplotlib (Optional for visualization)

Files Description
main.py — Main simulation driver, sets up grid topology, runs hourly simulations.

smartgrid.py — SmartGrid class managing graph topology and nodes/edges.

simulator.py — Simulation class handling power flow, failures, and repairs.

renewables.py — Models solar and wind power generation profiles.

pricing.py — Implements dynamic pricing logic based on demand.

data/data_hist.csv — Historical hourly electricity demand data for homes.

How to Run
Install dependencies:

text
pip install -r requirements.txt
Run the simulation:

text
python main.py
Observe hourly output logs for demand, renewable generation, power flow status, pricing, and node failures/repairs.

Customization
Modify grid topology in main.py by adding nodes and edges.

Adjust renewable generation parameters in renewables.py.

Change pricing strategy thresholds and rates in pricing.py.

Tune failure and repair probabilities in the simulation loop inside main.py.

Use Cases
Studying the impact of renewable integration on grid stability.

Analyzing grid resilience under random failures and repairs.

Evaluating dynamic pricing strategies to manage peak loads.

Educational tool for power systems and smart grid concepts.

License
This project is released under the MIT License.
