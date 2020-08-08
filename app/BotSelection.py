import networkx as nx
import pandas as pd
from community import community_louvain
from random import choice


G = nx.read_gexf('./graph_200_int.gexf')



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
        max_degree = max(community_df['degree'])
        user_max_degree = community_df[community_df['degree'] == max_degree]['user'].reset_index(drop=True)
        communities_leader = communities_leader.append({'community' : i, 
                                                        'user' : user_max_degree[0],
                                                        'degree' : max_degree}, ignore_index=True)
        i=i+1
        
    return communities_leader

    
#Betweenness
btw = nx.betweenness_centrality(G)


#Communities
communities = partition_df(G)
communities.rename(columns={0:'community'}, inplace=True)


#Communities && Degree
degree = []
for u in communities['user']:
    degree.append(G.degree[u])    
communities['degree'] = degree


#User with max degree for each community
communities_leader = max_degree_communitiy(communities)


#Random nodes
random_nodes = []
for i in range(10):
    random_nodes.append(choice(list(G.nodes)))
    
    


