import counters as cn
import networkx as nx

G0 = nx.read_gexf('./G_step0.gexf')

not_exposed = cn.count_not_exposed(G0)
exposed = cn.count_infected(G0)
infected = cn.count_infected(G0)
