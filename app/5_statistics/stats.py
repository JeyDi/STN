import counters as cn
import networkx as nx

def print_stats(G):
    not_exposed = cn.count_not_exposed(G)
    exposed = cn.count_exposed(G)
    infected = cn.count_infected(G)
    print('Not exposed: ' + str(not_exposed))
    print('Exposed: ' + str(exposed))
    print('Infected: ' + str(infected))

for i in range(0,5):
    G = nx.read_gexf('./G_step' + str(i) + '.gexf')
    print('STEP ' + str(i) + ":")
    print_stats(G)
    print()