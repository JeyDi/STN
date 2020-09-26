import networkx as nx
import pandas as pd
#from community import community_louvain
from random import choice
from multiprocessing import Pool
import itertools
import os


def import_graph(path):
    """
    Import and read a networkx graph to do some calculations

    Args:
        path (string): path of the networkx graph

    Returns:
        object: networkx graph object
    """
    try:
        G = nx.read_gexf(path)
        print(f"Graph imported succesfully: {path}")
        return G
    except Exception as e:
        print(f"Impossible to read the Networkx Graph, please check the path: {e}")
        return None


# Degree centrality
def get_in_degree_centrality(G):
    return pd.DataFrame.from_dict(nx.in_degree_centrality(G), orient="Index")


# Betweenness
def get_betweenness(G):
    return nx.betweenness_centrality(G)


# Eigenvector centrality
def get_eigenvector_centrality(G):
    return pd.DataFrame.from_dict(nx.eigenvector_centrality(G), orient="Index")


""" START Communities detection """
# Communities
def get_communities(G_undirect):
    communities = partition_df(G_undirect)
    communities.rename(columns={0: "community"}, inplace=True)
    return communities


# Communities & degree
def append_communities_degree(communities):
    degree = []
    for u in communities["user"]:
        degree.append(G.in_degree[u])
    communities["degree"] = degree
    return communities


def partition_df(G):
    partition = community_louvain.best_partition(G, random_state=42)
    partition_df = pd.DataFrame()
    partition_df = partition_df.from_dict(partition, orient="index")
    user = []

    for node in G:
        user.append(node)

    partition_df["user"] = user
    return partition_df


def max_degree_communitiy(df):
    n_comm = max(df["community"])

    communities_leader = pd.DataFrame(columns=["community", "user", "degree"])
    i = 0
    while i < n_comm:
        community_df = df[df["community"] == i]
        community_length = len(community_df)
        max_degree = max(community_df["degree"])
        user_max_degree = community_df[community_df["degree"] == max_degree][
            "user"
        ].reset_index(drop=True)
        communities_leader = communities_leader.append(
            {
                "community": i,
                "communitu_length": community_length,
                "user": user_max_degree[0],
                "degree": max_degree,
            },
            ignore_index=True,
        )
        i = i + 1

    return communities_leader


""" END Communities detection """


""" START Betweenness multiprocessing calculation """


def chunks(l, n):
    """Divide a list of nodes `l` in `n` chunks"""
    l_c = iter(l)
    while 1:
        x = tuple(itertools.islice(l_c, n))
        if not x:
            return
        yield x


def betweenness_centrality_parallel(G, processes=None):
    """Parallel betweenness centrality function"""
    p = Pool(processes=processes)  # if process = None use alla viable cores
    node_divisor = len(p._pool) * 4
    node_chunks = list(chunks(G.nodes(), int(G.order() / node_divisor)))
    num_chunks = len(node_chunks)
    bt_sc = p.starmap(
        nx.betweenness_centrality_subset,
        zip(
            [G] * num_chunks,
            node_chunks,
            [list(G)] * num_chunks,
            [True] * num_chunks,
            [None] * num_chunks,
        ),
    )

    # Reduce the partial solutions
    bt_c = bt_sc[0]
    for bt in bt_sc[1:]:
        for n in bt:
            bt_c[n] += bt[n]
    return pd.DataFrame.from_dict(bt_c, orient="Index")


""" END Betweenness multiprocessing """


"""Launch Function"""


def launch_calc_info(output_path, filename="500"):
    """
    Calc some usefull Graph info and properties
    The results are written in csv files into a given folder.

    Args:
        output_path (string): output files path where you want to save the results
        filename (str, optional): name of output file to save. Defaults to "500".

    Returns:
        bool: True if the execution is correct, false instead
    """
    # Do some calculations
    try:
        btw = betweenness_centrality_parallel(G)
        # print(btw)
        degree_centrality = get_in_degree_centrality(G)
        eigenvector_centrality = get_eigenvector_centrality(G)

        # communities = get_communities(G_undirect)
        # print(communities)

        # communities = append_communities_degree(communities)
        # print(communities)

        # User with max degree for each community
        # communities_leader = max_degree_communitiy(communities)
        # print(communities_leader)
    except Exception as message:
        print(
            "Impossible to calc some info about the graph, please check the code: {message} "
        )
        return False

    # Export the results to csv
    try:
        # Define the paths
        btw_path = os.path.join(output_path, "betweenness_" + filename + ".csv")
        dc_path = os.path.join(output_path, "degree_centrality_" + filename + ".csv")
        ec_path = os.path.join(
            output_path, "eigenvector_centrality_" + filename + ".csv"
        )

        btw.to_csv(btw_path)
        degree_centrality.to_csv(dc_path)
        eigenvector_centrality.to_csv(ec_path)
    except Exception as message:
        print(
            "impossible to export the csv for the calculation infos, please check the path: {message}"
        )
        return False

    try:
        # Random nodes
        random_nodes = []
        for i in range(10):
            random_nodes.append(choice(list(G.nodes)))
        print(random_nodes)
        return True
    except Exception as message:
        print(
            "Impossible to check random nodes infos, please check the code: {message}"
        )
        return False
