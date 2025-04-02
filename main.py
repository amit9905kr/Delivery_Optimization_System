# main.py
from algorithms.dijkstra import dijkstra
from algorithms.bellman_ford import bellman_ford
from algorithms.knapsack import knapsack_01
from algorithms.divide_and_conquer import divide_regions, merge_solutions
import json

def load_data():
    with open('data/graph_data.json') as f:
        graph = json.load(f)
    with open('data/packages.json') as f:
        packages = json.load(f)
    return graph, packages

def main():
    # Load data
    graph, packages = load_data()
    capacity = 50  # Vehicle capacity
    
    # Divide regions
    regions = divide_regions(list(graph.keys()))
    
    regional_solutions = []
    for region in regions:
        # Route optimization (choose Dijkstra or Bellman-Ford)
        if any(weight < 0 for node in graph for _, weight in graph[node].items()):
            distances = bellman_ford(graph, region[0])
        else:
            distances = dijkstra(graph, region[0])
        
        # Package selection using Knapsack
        weights = [p['weight'] for p in packages]
        values = [p['value'] for p in packages]
        max_value, selected = knapsack_01(weights, values, capacity)
        
        regional_solutions.append({
            'route': distances,
            'packages': [packages[i] for i in selected]
        })
    
    # Merge solutions
    global_solution = merge_solutions(regional_solutions)
    print("Optimized Solution:", global_solution)

if __name__ == "__main__":
    main()