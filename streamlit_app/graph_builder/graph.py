import networkx as nx
import pandas as pd
import os
from tqdm import tqdm
import time

GRAPH_PATH = "./data/graph"


def create_graph(df, follower_number, level2_path, graph_name, direct_graph=True):
    """Create Networkx Graph
    It's possible to create direct or not direct graphs.
    For now it's working only with 2 level of followers according to the project.
    Args:
        df (object): dataframe with all the followers (level 1) data
        follower_number (int): limit level 1 followers 
        level2_path (string): path of the second level (level 2) data for the graph
        graph_name (string): name of the output file (graph)
        direct_graph (bool, optional): If you want to generate a direct graph. Defaults to True.
    """
    # TODO: better error catching
    G = None

    if direct_graph == True:
        G = nx.DiGraph()
    elif direct_graph == False:
        G = nx.Graph()

    start_time = time.time()
    G.add_node("MainNode")

    print(f"Level 2 path: {level2_path}")
    print(f"Graph name: {graph_name}")

    # add the second level of nodes

    index = 0
    while len(G.edges("MainNode")) < follower_number:

        try:
            u = df["username"][index]
        except KeyError:
            print("Key Error in csv")

        try:
            if not G.has_node(u):
                G.add_node(u)

            G.add_edge("MainNode", u)

            level2 = pd.read_csv(os.path.join(level2_path, u + "_followers.csv"))
            for v in level2["username"]:
                if not G.has_node(v):
                    G.add_node(v)

                G.add_edge(u, v)

            index += 1
        except:
            print(u + " Not downloaded")
            index += 1

    print(f'Main Node has {len(G.edges("MainNode"))} edges')

    G_int = nx.convert_node_labels_to_integers(G)

    graph_filename = os.path.join(GRAPH_PATH, graph_name + ".gexf")
    nx.write_gexf(G_int, graph_filename)

    print("--- %s seconds ---" % (time.time() - start_time))
    print(f"Graph generated to: {graph_filename}")
    node_numbers = G.number_of_nodes()
    return node_numbers