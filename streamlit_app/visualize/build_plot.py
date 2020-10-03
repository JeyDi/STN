import networkx as nx
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import pickle
from visualize.layout import build_graph
import streamlit as st


def step_graph(G, df, step):
    """
    Prende il grafo e per ogni step della simulazione prende i risultati della simulazione di quello step e aggiunge gli attributi ai nodi
    """
    try:
        print("Start editing the plot for the step: {step}")
        df_id = df[df["key"] == "id"].reset_index()
        df_infected_type = df[df["key"] == "infected_type"].reset_index()
        df_directed = df[df['key'] == 'directed' ].reset_index()

        df_type = df[df["key"] == "type"]  # DF with opinion leader and bot
        df_type["agent_id"] = df_type["agent_id"].astype("str")
        df_type = df_type.set_index("agent_id")
        nx.set_node_attributes(G, df_type["value"].to_dict(), "type")

        i = 0
        while i <= step:
            step_df = df_id[df_id["t_step"] == i]
            step_df["agent_id"] = step_df["agent_id"].astype("str")
            step_df = step_df.set_index("agent_id")
            nx.set_node_attributes(G, step_df["value"].to_dict(), "state")

            step_infected_type = df_infected_type[df_infected_type["t_step"] == i]
            step_infected_type["agent_id"] = step_infected_type["agent_id"].astype(
                "str"
            )
            step_infected_type = step_infected_type.set_index("agent_id")
            nx.set_node_attributes(
                G, step_infected_type["value"].to_dict(), "infected_type"
            )

            step_directed = df_directed[df_directed['t_step'] == i]
            step_directed['agent_id'] = step_directed['agent_id'].astype(
                "str"
            )
            step_directed = step_directed.set_index('agent_id')
            nx.set_node_attributes(
                G, step_directed['value'].to_dict(), 'directed'
            )

            i = i + 1  # INTERVAL IN AGENT PARAMETER
        result = G.copy()
        print(f"Graph fixed for the step: {step}")
        return result
    except Exception as message:
        print(f"Impossible to edit the graph: {message}")
        return None


def generate_graph_plot(
    G_path,
    simulation_data_path,
    simulation_name,
    G_step_iterations=5,
    sprint_layout_calc=False,
):
    # Import data
    try:
        G = nx.read_gexf(G_path)
        df = pd.read_csv(simulation_data_path)
        print("data succesfully loaded")

    except Exception as message:
        print(f"Impossibile to read data: {message}")

    try:
        if is_simulation_based_on_500(simulation_name):
            layout_pickle_filename = "./data/serialization/G_node_poss_layout.pkl"

            # Shared layout
            if sprint_layout_calc:
                G_node_pos = nx.spring_layout(G)
                with open(layout_pickle_filename, "wb") as output:
                    pickle.dump(G_node_pos, output, pickle.HIGHEST_PROTOCOL)
                load = False
                print("Spring graph layout calcolated and stored")
            else:
                ##load pickle object
                with open(layout_pickle_filename, "rb") as input:
                    G_node_pos = pickle.load(input)
                load = True
                print("Spring graph layout loaded from pickle file")
    except Exception as message:
        if load:
            print(f"Impossibile to load the pickle file: {message}")
        elif not load:
            print(f"Impossible to calc and save the pickle file: {message}")

    for i in range(G_step_iterations):
        print(f"Start generating the plot: {G_step_iterations}")
        G_step = None
        G_step = step_graph(G, df, i)

        nx.write_gexf(G_step, f"./data/output/G_{simulation_name}_step{i}.gexf")

        if is_simulation_based_on_500(simulation_name):
            result_graph = build_graph(G_step, G_node_pos, i)
            st.plotly_chart(result_graph, use_container_width=True)

        print(f"{simulation_name} - STEP {i} DONE")

    print("\nGraph plot and statistics calculated succesfully")
    return True

def is_simulation_based_on_500(simulation_name):
    return simulation_name.split("_")[1] == "500"
