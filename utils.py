import json
import random
import copy
import matplotlib.pyplot as plt
import networkx as nx

def load_data():
    with open('data/graph_data.json') as f:
        graph = json.load(f)
    with open('data/packages.json') as f:
        packages = json.load(f)
    return graph, packages

def simulate_traffic(graph):
    new_graph = copy.deepcopy(graph)
    for node in new_graph:
        for neighbor in new_graph[node]:
            change = random.choice([-0.2, 0, 0.2])
            new_graph[node][neighbor] = round(new_graph[node][neighbor] * (1 + change), 2)
    return new_graph

def plot_graph(graph, path=None):
    G = nx.DiGraph()
    for node in graph:
        G.add_node(node)
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=800)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    return plt