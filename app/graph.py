import networkx as nx
import pandas as pd

''' Import tweets dataset '''
df = pd.read_csv(r'./conte_followers.csv').iloc[:2000]


''' Create graph '''
G = nx.Graph()
G.add_node('GiuseppeConteIT', stato='s')

for u in df['username']:
    G.add_node(u, stato = 's')   #Add node and se attribute 'stato'
    G.add_edge(u, 'GiuseppeConteIT')
    try: 
        level2 = pd.read_csv(r'./conte_followers/'+u+'_followers.csv')
        for v in level2['username']:
            G.add_node(v, stato='s')
            G.add_edge(v, u)
    except:
        print(u + ' Not downloaded')
    
nx.draw(G)
#plt.savefig('graph.png')
nx.write_gml(G, './graph.gml')

''' Node color 
color_map=[]
for node in G:
    if G.nodes[node]['stato'] == 's':  #Set node color based on 'stato'
        color_map.append('green')  
    else: 
        color_map.append('blue')      
        
nx.draw(G, node_color=color_map)


'''