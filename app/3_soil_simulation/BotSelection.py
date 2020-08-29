import networkx as nx
import pandas as pd
from community import community_louvain
from random import choice
from multiprocessing import Pool
import itertools


G = nx.read_gexf('../2_graph_builder/graph_500_int_direct.gexf')
G_undirect = nx.read_gexf('../2_graph_builder/graph_500_int.gexf')



#Degree centrality
def get_in_degree_centrality(G):
    return pd.DataFrame.from_dict(nx.in_degree_centrality(G), orient='Index')

#Betweenness
def get_betweenness(G):
    return nx.betweenness_centrality(G)

#Eigenvector centrality
def get_eigenvector_centrality(G):
    return pd.DataFrame.from_dict(nx.eigenvector_centrality(G), orient='Index')


''' START Communities detection '''
#Communities
def get_communities(G_undirect):
    communities = partition_df(G_undirect)
    communities.rename(columns={0:'community'}, inplace=True)
    return communities

#Communities & degree
def append_communities_degree(communities):
    degree = []
    for u in communities['user']:
        degree.append(G.in_degree[u])    
    communities['degree'] = degree
    return communities

def partition_df (G):
    partition = community_louvain.best_partition(G, random_state=42)
    partition_df = pd.DataFrame()
    partition_df = partition_df.from_dict(partition, orient='index')
    user = []
    
    for node in G:
        user.append(node)
    
    partition_df['user'] = user
    return partition_df

def max_degree_communitiy(df): 
    n_comm = max(df['community'])
    
    communities_leader=pd.DataFrame(columns=['community', 'user', 'degree'])
    i=0
    while i<n_comm:
        community_df = df[df['community']==i]
        community_length = len(community_df)
        max_degree = max(community_df['degree'])
        user_max_degree = community_df[community_df['degree'] == max_degree]['user'].reset_index(drop=True)
        communities_leader = communities_leader.append({'community' : i, 
                                                        'communitu_length' : community_length,
                                                        'user' : user_max_degree[0],
                                                        'degree' : max_degree}, ignore_index=True)
        i=i+1
        
    return communities_leader

''' END Communities detection'''




''' START Betweenness multiprocessing '''

def chunks(l, n):
    """Divide a list of nodes `l` in `n` chunks"""
    l_c = iter(l)
    while 1:
        x = tuple(itertools.islice(l_c, n))
        if not x:
            return
        yield x


def betweenness_centrality_parallel(G, processes=None):
    """Parallel betweenness centrality  function"""
    p = Pool(processes=processes) #if process = None use alla viable cores
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

''' END Betweenness multiprocessing '''


if __name__ == '__main__':
    btw = betweenness_centrality_parallel(G)
    btw.to_csv('./betweenness_centrality_500.csv')
    # print(btw)
    
    degree_centrality = get_in_degree_centrality(G)
    degree_centrality.to_csv('./degree_centrality_500.csv')
    
    eigenvector_centrality = get_eigenvector_centrality(G)
    eigenvector_centrality.to_csv('./eigenvector_centrality_500.csv')
    
    # communities = get_communities(G_undirect)
    # print(communities)

    # communities = append_communities_degree(communities)
    # print(communities)

    # User with max degree for each community
    # communities_leader = max_degree_communitiy(communities)
    # print(communities_leader)

    # Random nodes
    random_nodes = []
    for i in range(10):
        random_nodes.append(choice(list(G.nodes)))
    print(random_nodes)
    