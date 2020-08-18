import networkx as nx
import pandas as pd

''' Import followers dataset '''
df = pd.read_csv(r'../1_scraper/conte_followers.csv').iloc[:200]

print('Direct graph? y/n')
val = str(input())

''' Create graph '''
try:
    G = None

    if val == 'y':
        G = nx.DiGraph()
    elif val == 'n':
        G = nx.Graph()
        
    G.add_node('GiuseppeConteIT')

    for u in df['username']:
        try: 
            level2 = pd.read_csv(r'../1_scraper/conte_followers/'+ u +'_followers.csv')
            G.add_node(u)  
            G.add_edge(u, 'GiuseppeConteIT')
        
            for v in level2['username']:
                G.add_node(v)
                G.add_edge(v, u)
        except:
            print(u + ' Not downloaded')
        
    G_int = nx.convert_node_labels_to_integers(G)

    if val == 'y':
        nx.write_gexf(G_int, './graph_200_int_direct.gexf')
    elif val == 'n':
        nx.write_gexf(G_int, './graph_200_int.gexf')
    
except:
    print('INPUT ERROR')