#!/usr/bin/env python

import matplotlib
matplotlib.use('TkAgg')

import pylab as pl
import random as rd #non usare questo usa np
import scipy as sp
import numpy as np
import networkx as nx
import math
from copy import deepcopy
import argparse, sys, os
import pycxsimulator

### absones utilities
sys.path.append(os.path.abspath(os.getcwd() + '/utils'))
from simulation import *
from tweet import *

rd.seed()

tweets = {}
retweets = {}
dtag = {}

def init():
    global time, network, network_r, maxNodeID, positions, colors, colors_r, dims, sharing, ttmenouno
    global sim

    time = 0

    network = nx.gnm_random_graph(sim.total_users,sim.total_users*5,directed=True)
    network_r = nx.DiGraph()
    network_r.add_nodes_from(network)

    positions = nx.random_layout(network)
    colors = [network.degree().get(node) for node in network.nodes()]
    colors_r = ['white'] * len(network_r.nodes())
    dims = list(map(lambda x: float(x+1)*80, [network.in_degree().get(node) for node in network.nodes()]))

    sharing = []
    ttmenouno = []

    for n in network.nodes():
        sim.generate_new_user(network.node[n])
        ## genera tweet iniziali
        for y in range(0,int(math.floor(20.0*network.in_degree().get(n)/max(network.in_degree())))):
            pi = network.node[n]['pi']
            topic = np.random.choice(np.arange(0, len(pi)), p=pi) + 1
            if pi[topic-1] > network.node[n]['pi_average']:
                tweets[n,-y-1] = Tweet(topic,n,time,np.random.triangular(0.5, 0.75, 1),np.random.uniform(0,1))
            else:
                tweets[n,-y-1] = Tweet(topic,time,time,np.random.uniform(0,1),np.random.triangular(0.5, 0.75, 1))
        print(network.node[n])

def draw():
     colors = [network.degree().get(node) for node in network.nodes()]
     dims = list(map(lambda x: float(x+1)*80, [network.in_degree().get(node) for node in network.nodes()]))

     pl.subplot(1,2,1)
     pl.cla()
     nx.draw(network, pos = positions, node_color = colors, node_size = dims)
     pl.axis('image')
     pl.title('t = ' + str(time) + ' edges = ' + str(len(network.edges())))

     pl.subplot(1,2,2)
     pl.cla()
     nx.draw(network_r, pos = positions, node_color = colors_r, node_size = dims, with_labels=True)
     pl.axis('image')
     pl.title('t = ' + str(math.floor(time/12)))

def step():
    global network_r, network, sharing, time, colors_r, ttmenouno

#~#~#~# tweets #~#~#~#
    in_deg = network.in_degree()
    colors_r = []
    l = network.nodes()
    tt = []
    for nr in l:
        p_t = network.node[nr]['tz'][time%12]*(float(in_deg.get(nr))/len(l))
        p_nt = (1-network.node[nr]['tz'][time%12])*(1-(float(in_deg.get(nr))/len(l)))
        alfa = p_t + p_nt
        if np.random.uniform(0,1) < float(p_t)/alfa:
            tt.append(nr)
            colors_r.append('red')
            pi = network.node[nr]['pi']
            topic = np.random.choice(np.arange(0, len(pi)), p=pi) + 1
            if pi[topic-1] > network.node[nr]['pi_average']:
                tweets[nr,time] = Tweet(topic,nr,time,np.random.triangular(0.5, 0.75, 1),np.random.uniform(0,1))
            else:
                tweets[nr,time] = Tweet(topic,nr,time,np.random.uniform(0,1),np.random.triangular(0.5, 0.75, 1))
        else:
            colors_r.append('white')

#~#~#~# retweets #~#~#~#
    network_r.remove_edges_from(sharing)
    sharing = []
    out_deg = network.out_degree()
    for nr in l:
        p_rt = network.node[nr]['tz'][time%12]*(float(out_deg.get(nr))/len(l))
        p_nrt = (1-network.node[nr]['tz'][time%12])*(1-(float(out_deg.get(nr))/len(l)))
        alfa = p_rt + p_nrt
        if np.random.uniform(0,1) < float(p_rt)/alfa:
            mini = 20
            mini_n = -1
            for tn in ttmenouno:
                if tn != nr:
                    a = [tweets[key].get_topic() for key in tweets.keys() if key[0] == tn and key[1] >= time-20]
                    hist, bins=np.histogram(a,bins=list(range(1,sim.topic+2)),density=True)
                    kl = omofilia(np.array(network.node[nr]['pi']),np.array(hist))
                    if kl < mini:
                        mini = kl
                        mini_n = tn
            if mini_n >= 0:
                sharing.append((nr,mini_n))
    print(ttmenouno)
    ttmenouno = deepcopy(tt)
    time += 1

    for e in sharing:
        network_r.add_edge(u=e[0],v=e[1])

##=====================================
## Section 4: [Optional] Create Setter/Getter Functions for Model Parameters
##=====================================

def omofilia(p,q):
    somma = 0
    for z in range(0,len(p)):
        avg = (p[z]+q[z])/2
        somma = somma + ((np.power(p[z]-avg,2)+np.power(q[z]-avg,2))/2)*p[z]
    return 1-somma

def skl_d(p,q):
	kl1 = 0
	for i in range(0, len(p)):
		kl1 = kl1 + p[i]*np.log2(p[i]/q[i])
	kl2 = 0
	for j in range(0, len(q)):
		kl2 = kl2 + q[j]*np.log2(q[j]/p[j])
	return np.mean([kl1,kl2])

def kl_d(p,q):
	kl1 = 0
	for i in range(0, len(p)):
		kl1 = kl1 + p[i]*np.log2(p[i]/q[i])
	return kl1


##=====================================
## Section 5: Import and Run GUI
##=====================================
def get_args():
    parser = argparse.ArgumentParser(description='ABSoNeS', add_help=True)
    #change all the defaults
    parser.add_argument('-u', '--users', action='store', type=int, default=10,
        help='specifies the number of total users.')
    parser.add_argument('-t', '--topic', action='store', type=int, default=10,
        help='specifies the number of total topics.')
    parser.add_argument('-d', '--threads', action='store', type=int, default=2,
        help='specifies the number of total threads used by the program.')
    ret = parser.parse_args()

    return ret


def main():
    # global args
    pycxsimulator.GUI(title='SocialNetwork',interval=0, parameterSetters = []).start(func=[init,draw,step])
    # 'title', 'interval' and 'parameterSetters' are optional

if __name__ == "__main__":
    args = get_args()
    sim = Simulation(args.topic, args.users)
    print()
    main()
