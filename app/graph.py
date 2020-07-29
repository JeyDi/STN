import networkx as nx
import pandas as pd


''' Import tweets dataset '''
df = pd.read_csv(r'./conte_followers.csv').iloc[:200]


''' Create graph '''
G = nx.Graph()
G.add_node('GiuseppeConteIT')

for u in df['username']:
    try: 
        level2 = pd.read_csv(r'./conte_followers/'+u+'_followers.csv')
        G.add_node(u)  
        G.add_edge(u, 'GiuseppeConteIT')
    
        for v in level2['username']:
            G.add_node(v)
            G.add_edge(v, u)
    except:
        print(u + ' Not downloaded')
    
#nx.draw(G)
#plt.savefig('graph.png')
nx.write_gml(G, './graph_200.gml')
G_int = nx.convert_node_labels_to_integers(G)
nx.write_gexf(G_int, './graph_200_int.gexf')
