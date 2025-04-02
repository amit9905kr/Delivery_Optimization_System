import streamlit as st
from algorithms.dijkstra import dijkstra
from algorithms.bellman_ford import bellman_ford
from algorithms.knapsack import knapsack_01
from algorithms.divide_and_conquer import divide_regions, merge_solutions
from utils import load_data, simulate_traffic, plot_graph
import time

def main():
    st.title("🚚 Delivery Optimization System")
    graph, packages = load_data()
    capacity = st.sidebar.slider("Vehicle Capacity (kg)", 10, 100, 50)
    live_mode = st.sidebar.checkbox("Enable Live Traffic Updates")

    if 'graph' not in st.session_state:
        st.session_state.graph = graph

    placeholder = st.empty()
    
    while True:
        with placeholder.container():
            if live_mode:
                st.session_state.graph = simulate_traffic(st.session_state.graph)
            
            regions = divide_regions(list(st.session_state.graph.keys()))
            regional_solutions = []
            
            for region in regions:
                try:
                    distances = bellman_ford(st.session_state.graph, region[0])
                except ValueError:
                    distances = dijkstra(st.session_state.graph, region[0])
                
                weights = [p['weight'] for p in packages]
                values = [p['value'] for p in packages]
                max_val, selected = knapsack_01(weights, values, capacity)
                
                regional_solutions.append({
                    'route': distances,
                    'packages': [packages[i] for i in selected]
                })
            
            global_solution = merge_solutions(regional_solutions)
            
            st.subheader("Network Graph")
            fig = plot_graph(st.session_state.graph)
            st.pyplot(fig)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Optimized Routes")
                st.json(global_solution['route'])
            with col2:
                st.subheader("Selected Packages")
                for p in global_solution['packages']:
                    st.write(f"📦 Package {p['id']} (Weight: {p['weight']}kg, Value: ${p['value']})")
            
            if live_mode:
                time.sleep(5)
                st.experimental_rerun()
            else:
                break

if __name__ == "__main__":
    main()