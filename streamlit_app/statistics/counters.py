def count_not_exposed(G):
    not_exposed = 0
    for node in G.nodes:
            if G.nodes[node]['state'] == 'not_exposed':
                not_exposed = not_exposed + 1
    return not_exposed


'''INFECTED'''

def count_infected(G):  #WHITHOUT OPINION LEADER AND BOT
    infected = 0
    for node in G.nodes:
        if G.nodes[node].get('type') == None and G.nodes[node]['state'] == 'infected':
            infected = infected + 1
    return infected

def count_infected_bot(G):
    infected_bot = 0
    for node in G.nodes:
        if G.nodes[node]['state'] == 'infected':
            if G.nodes[node].get('type') == None and  G.nodes[node].get('infected_type') == '2':
                infected_bot = infected_bot + 1
    return infected_bot


def count_infected_opinion_leader(G):
    infected_opinion_leader = 0
    for node in G.nodes:
        if G.nodes[node]['state'] == 'infected':
     
            if G.nodes[node].get('type') == None and  G.nodes[node].get('infected_type') == '1':
                infected_opinion_leader = infected_opinion_leader + 1

    return infected_opinion_leader


def count_infected_user(G):
    infected_user = 0
    for node in G.nodes:
        if G.nodes[node]['state'] == 'infected': 
            if G.nodes[node].get('type') == None and G.nodes[node].get('infected_type')== '0':
                infected_user = infected_user + 1
    return infected_user


def count_infected_directed(G):
    directed = 0
    undirected = 0
    for node in G.nodes:
        if G.nodes[node]['state'] == 'infected':
            if G.nodes[node].get('type') == None and G.nodes[node].get('directed') == '1':
                directed = directed + 1
            elif G.nodes[node].get('type') == None and G.nodes[node].get('directed') == '0':
                undirected = undirected + 1
    return directed, undirected


''' EXPOSED '''
def count_exposed(G):
    exposed = 0
    for node in G.nodes:
        if G.nodes[node]['state'] == 'exposed':
            exposed = exposed + 1
    return exposed


def count_exposed_bot(G):
    exposed_bot = 0
    for node in G.nodes:
        if G.nodes[node]['state'] == 'exposed':
            if G.nodes[node]['infected_type'] == '2':
                exposed_bot = exposed_bot + 1
    return exposed_bot


def count_exposed_opinion_leader(G):
    exposed_opinion_leader = 0
    for node in G.nodes:
        if G.nodes[node]['state'] == 'exposed':
            if G.nodes[node]['infected_type'] == '1':
                exposed_opinion_leader = exposed_opinion_leader + 1
    return exposed_opinion_leader


def count_exposed_user(G):
    exposed_user = 0
    for node in G.nodes:
        if G.nodes[node]['state'] == 'exposed':
            if G.nodes[node]['infected_type'] == '0':
                exposed_user = exposed_user + 1
    return exposed_user


def count_exposed_directed(G):
    directed = 0
    undirected = 0
    for node in G.nodes:
        if G.nodes[node]['state'] == 'exposed':
            if G.nodes[node].get('directed') == '1':
                directed = directed + 1
            elif G.nodes[node].get('directed') == '0':
                undirected = undirected + 1
    return directed, undirected
