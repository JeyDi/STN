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
from mps import *

def main(users, topics, max_steps, opt_threads):

	# ========================
	# GENERATE INITIAL STUFF
	# ========================

	tweets = {}
	retweets = {}
	dtag = {}

	num_nodes = users

	network = nx.gnm_random_graph(num_nodes, round((float(num_nodes)*((float(num_nodes)-1)/5))/2), directed=True)
	positions = nx.random_layout(network)
	sim = Simulation(topics, num_nodes, network)

	print('Generation')
	print('=' * 20)
	for n in network.nodes():
		u1 = User(n, sim.topics)
		sim.add_user(u1)
		for y in range(0,int(math.floor(20.0*network.in_degree().get(n)/max(network.in_degree().values())))):
			sim.post(sim.get_user(n),-y-1)

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

	graph = open('graph_init.csv','w')
	graph.write('id,weight\n')
	for n in sim.network.nodes():
		graph.write(str(n) + ',' + str(network.in_degree().get(n)) + '\n')
	graph.close()

	edg = open('edges_init.csv','w')
	edg.write('Source,Target\n')
	for e in sim.network.edges():
		edg.write(str(e[0]) + ',' + str(e[1]) + '\n')
	edg.close()

	df = pd.DataFrame(columns=list(range(1000)))

	# ========================
	# SIMULATION GAME
	# ========================

	for step in range(1, max_steps):

		classification = open('classification.csv','a')
		dd = sim.network.in_degree()
		dds = sorted(dd, key=dd.get, reverse=True)
		classification.write(str(step) + ',' + ','.join(str(v) for v in dds[0:50]) + '\n')
		classification.close()

		dft = pd.DataFrame([list(sim.network.in_degree().values())], columns=list(range(1000)))
		df = df.append(dft, ignore_index=True)

		evo = open('evolution.csv','a')
		print('')
		print("#" * 40)
		print('# Step ' + str(step))
		print('# Numero di archi ' + str(len(sim.network.edges())))
		print('# Grado di completamento ' + str(len(sim.network.edges())*100/(num_nodes**2 - num_nodes)))
		print('# Tweets = ' + str(len(sim.tweet)))
		print('# Retweets = ' + str(len(sim.retweet)))
		print("#" * 40)
		mp_simulation_step(sim, opt_threads)
		# sim.personal_follow()
		# sim.step_tweet()
		# sim.step_retweet()
		# sim.attachment_eval()
		sim.now = step
		evo.write(str(len(sim.network.edges()))+'\n')
		evo.close()

	df.to_csv(path_or_buf='class_complete.csv',sep=",",header=True, index=True)

	graph = open('graph_end.csv','w')
	graph.write('id,weight\n')
	for n in sim.network.nodes():
		graph.write(str(n) + ',' + str(network.in_degree().get(n)) + '\n')
	graph.close()

	edg = open('edges_end.csv','w')
	edg.write('Source,Target\n')
	for e in sim.network.edges():
		edg.write(str(e[0]) + ',' + str(e[1]) + '\n')
	edg.close()

# ARGUMENTS' SHIT
def get_args():
	parser = argparse.ArgumentParser(description='ABSoNeS', add_help=True)
	#change all the defaults
	parser.add_argument('-u', '--users', action='store', type=int, default=1000,
		help='specifies the number of total users.')
	parser.add_argument('-t', '--topic', action='store', type=int, default=10,
		help='specifies the number of total topics.')
	parser.add_argument('-s', '--steps', action='store', type=int, default=1080,
		help='specifies the number of maximum simulated steps.')
	parser.add_argument('-d', '--threads', action='store', type=int, default=1,
		help='specifies the number of total threads used by the program.')
	ret = parser.parse_args()

	return ret

if __name__ == "__main__":
	args = get_args()
	main(args.users, args.topic, args.steps, args.threads)
