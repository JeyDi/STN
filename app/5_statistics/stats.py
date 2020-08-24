import counters as cn
import networkx as nx

def print_stats(G):
    not_exposed = cn.count_not_exposed(G)

    exposed = cn.count_exposed(G)
    exposed_opinion_leader = cn.count_exposed_opinion_leader(G)
    exposed_bot = cn.count_exposed_bot(G)
    exposed_user = cn.count_exposed_user(G)

    infected = cn.count_infected(G)
    infected_opinion_leader = cn.count_infected_opinion_leader(G)
    infected_bot = cn.count_infected_bot(G)
    infected_user = cn.count_infected_user(G)

    print(f'Not exposed: {not_exposed}')
    print(f'Exposed: {exposed}')
    print(f'\tFrom Opinion Leader: {exposed_opinion_leader}, from BOT: {exposed_bot}, from users: {exposed_user}')
    print(f'Infected: {infected}')
    print(f'\tFrom Opinion Leader: {infected_opinion_leader}, from BOT: {infected_bot}, from users: {infected_user}')

for i in range(0,5):
    G = nx.read_gexf(f'./G_step{i}.gexf')
    print('STEP ' + str(i) + ":")
    print_stats(G)
    print()