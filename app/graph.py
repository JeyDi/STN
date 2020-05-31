import networkx as nx
import pandas as pd

''' Import tweets dataset '''
df = pd.read_csv(r'./df.csv')


''' Create graph '''
G = nx.Graph()
for u in df['username']:
    G.add_node(u, stato = 's')   #Add node and se attribute 'stato'
    
nx.draw(G)
#plt.savefig('graph.png')


''' Node color '''
color_map=[]
for node in G:
    if G.nodes[node]['stato'] == 's':  #Set node color based on 'stato'
        color_map.append('green')  
    else: 
        color_map.append('blue')      
        
nx.draw(G, node_color=color_map)


