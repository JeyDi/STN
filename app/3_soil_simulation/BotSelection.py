import networkx as nx
import pandas as pd
from community import community_louvain
from random import choice

G = nx.read_gexf('../2_graph_builder/graph_int_direct.gexf')
G_undirect = nx.read_gexf('../2_graph_builder/graph_int.gexf')

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

#Betweenness
def get_betweenness(G):
    return nx.betweenness_centrality(G)

#Communities
def get_communities(G_undirect):
    communities = partition_df(G_undirect)
    communities.rename(columns={0:'community'}, inplace=True)
    return communities

#Communities degree
def append_communities_degree(communities):
    degree = []
    for u in communities['user']:
        degree.append(G.in_degree[u])    
    communities['degree'] = degree
    return communities


if __name__ == '__main__':
    btw = get_betweenness(G)
    #print(btw)

    communities = get_communities(G_undirect)
    #print(communities)

    communities = append_communities_degree(communities)
    #print(communities)

    #User with max degree for each community
    communities_leader = max_degree_communitiy(communities)
    #print(communities_leader)

    #Random nodes
    random_nodes = []
    for i in range(10):
        random_nodes.append(choice(list(G.nodes)))
    print(random_nodes)