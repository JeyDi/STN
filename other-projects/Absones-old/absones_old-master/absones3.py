#!/usr/bin/env python3
import random as rd #non usare questo usa np
import scipy as sp
import pandas as pd
import numpy as np
import networkx as nx
import math
from copy import deepcopy
import argparse, sys, os
from user import User
from simulation import *

def main(users, ntype, max_steps, density, lucky):

	tweets = {}
	retweets = {}
	dtag = {}

	num_nodes = users

	#network = nx.gnm_random_graph(num_nodes, round((float(num_nodes)*((float(num_nodes)-1)/5))/2), directed=True)
	network = None
	parameters = None
	if ntype == 'sf': 
		parameters = '_' + str(num_nodes) + '_' + ntype + '_' + str(max_steps) + '_' + str(lucky)
		network = nx.scale_free_graph(num_nodes)
		network = nx.DiGraph(network)
	else:
		parameters = '_' + str(num_nodes) + '_rnd_' + str(max_steps) + '_' + str(density) + '_' + str(lucky)
		network = nx.gnm_random_graph(num_nodes, num_nodes*(num_nodes-1)*(density/100), directed=True)
	positions = nx.random_layout(network)
	sim = Simulation(10, num_nodes, network)

	attributes = {}

	print('Generation')
	print('=' * 20)
	for n in network.nodes():
		u1 = User(n, sim.topics)
		attributes[n] = np.argmax(u1.pi)
		sim.add_user(u1)
		for y in range(0,int(math.floor(20.0*network.in_degree().get(n)/max(network.in_degree().values())))):
			sim.post(sim.get_user(n),-y-1)

	nx.set_node_attributes(sim.network,'toptopic',attributes)

	# add follow
	print('Follow')
	print('=' * 20)
	for e in network.edges():
		sim.new_follow(e[0],e[1])

	evo = []

	for n in network.nodes():
		for y in range(0,int(math.floor(20.0*network.in_degree().get(n)/max(network.in_degree().values())))):
			sim.repost(sim.get_user(n),-y-1)

	print(sim.retweet)

	
	graph = open('graph_init' + parameters + '.csv','w')
	graph.write('id,weight\n')
	for n in sim.network.nodes():
		graph.write(str(n) + ',' + str(network.in_degree().get(n)) + '\n')
	graph.close()

	edg = open('edges_init' + parameters + '.csv','w')
	edg.write('Source,Target\n')
	for e in sim.network.edges():
		edg.write(str(e[0]) + ',' + str(e[1]) + '\n')
	edg.close()

	df = pd.DataFrame(columns=list(range(num_nodes)))

	for step in range(1, max_steps+1):

		classification = open('classification' + parameters + '.csv','a')
		dd = sim.network.in_degree()
		dds = sorted(dd, key=dd.get, reverse=True)
		classification.write(str(step) + ',' + ','.join(str(v) for v in dds[0:50]) + '\n')
		classification.close()

		dft = pd.DataFrame([list(sim.network.in_degree().values())], columns=list(range(num_nodes)))
		df = df.append(dft, ignore_index=True)

		evo = open('evolution' + parameters + '.csv','a')
		clust = open('clustering' + parameters + '.csv','a')
		assor = open('deg_assortativity' + parameters + '.csv','a')
		homo = open('homophily' + parameters + '.csv','a')
		spath = open('spath' + parameters + '.csv','a')
		print('')
		print("#" * 40)
		print('# Step ' + str(step))
		print('# Numero di archi ' + str(len(sim.network.edges())))
		print('# Grado di completamento ' + str(len(sim.network.edges())*100/(num_nodes**2 - num_nodes)))
		print('# Tweets = ' + str(len(sim.tweet)))
		print('# Retweets = ' + str(len(sim.retweet)))
		print("#" * 40)
		sim.personal_follow()
		sim.step_tweet()
		sim.step_retweet()
		sim.attachment_eval()
		sim.now = step
		evo.write(str(len(sim.network.edges()))+'\n')
		evo.close()
		clust.write(str(nx.transitivity(sim.network))+'\n')
		clust.close()
		assor.write(str(nx.degree_assortativity_coefficient(sim.network))+'\n')
		assor.close()
		homo.write(str(nx.attribute_assortativity_coefficient(sim.network,'toptopic'))+'\n')
		homo.close()
		if not 0 in list(sim.network.in_degree().values()):
			spath.write(str(nx.average_shortest_path_length(sim.network))+'\n')
		else:
			spath.write('nullo\n')	
		spath.close()

		if step == 200 and lucky == 1:
			top = dds[0]
			bottom = dds[-1]
			user = sim.get_user(top)
			j = np.random.choice(sim.topics, 1, p=user.pi)[0]
			sim.tweet[bottom, step] = [bottom, step, j, 1, 0, top]
			sim.retweet[top, step] = [bottom, step, j, 1, 0, top]

			with open("prescelto" + parameters + ".txt", "w") as f: 
				f.write(str(bottom) + "\n" + str(top)) 

	df.to_csv(path_or_buf='class_complete' + parameters + '.csv',sep=",",header=True, index=True)

	graph = open('graph_end' + parameters + '.csv','w')
	graph.write('id,weight\n')
	for n in sim.network.nodes():
		graph.write(str(n) + ',' + str(network.in_degree().get(n)) + '\n')
	graph.close()

	edg = open('edges_end' + parameters + '.csv','w')
	edg.write('Source,Target\n')
	for e in sim.network.edges():
		edg.write(str(e[0]) + ',' + str(e[1]) + '\n')
	edg.close()

def get_args():
	parser = argparse.ArgumentParser(description='ABSoNeS', add_help=True)
	#change all the defaults
	parser.add_argument('-u', '--users', action='store', type=int, default=1000,
		help='specifies the number of total users.')
	parser.add_argument('-t', '--ntype', action='store', type=str, default='sf',
		help='specifies the network type.')
	parser.add_argument('-s', '--steps', action='store', type=int, default=1080,
		help='specifies the number of maximum simulated steps.')
	parser.add_argument('-d', '--density', action='store', type=float, default=1,
		help='specifies the density of the network.')
	parser.add_argument('-l', '--lucky', action='store', type=int, default=0,
		help='specifies if one user is lucky at step 200.')
	ret = parser.parse_args()

	return ret

if __name__ == "__main__":
	args = get_args()
	main(args.users, args.ntype, args.steps, args.density, args.lucky)
