import multiprocessing
from simulation import Simulation
import numpy as np
import threading

def multi_chunks(l, n):
	for i in range(n):
		yield [i*int(l/n), (i+1)*int(l/n)]

def mp_start_process(target_name, sim, chunks):
	# manager = Manager()
	# counter = manager.Simulation(sim)
	# pool = multiprocessing.Pool(len(chunks))
	# for x in chunks:
	# 	pool.apply(func=target_name, args=(counter, x))
	# pool.close()
	# pool.join()

	# processes = [multiprocessing.Process(target=target_name, args=(sim, x)) for x in chunks]
	processes = [threading.Thread(target=target_name, args=(sim, x)) for x in chunks]
	for p in processes:
		p.start()
	for p in processes:
		p.join()
	return

def mp_personal_follow(sim, ind):
	s, e = ind
	sample = np.random.random(size=sim.total_users)
	for u in range(s, e):
		if sample[u] <= 0.005:
			# print("personal %d" % s)
			user = sim.get_user(u)
			target = np.random.choice(range(sim.total_users),size=1)[0]
			while target in user.followings or target == user.id:
				target = np.random.choice(range(sim.total_users),size=1)[0]
			sim.new_follow(u,target)

def mp_step_tweet(sim, ind):
	s, e = ind
	l = len(sim.users.keys())
	for u in range(s, e):
		# Calculate probability of TWEET
		user = sim.get_user(u)
		ratiof = (float(len(user.followings)) / l)
		p_rt = user.tz[sim.now % 12] * \
			(-(np.log(ratiof+4)/np.log(ratiof+2))+2)
		p_nrt = (1 - user.tz[sim.now % 12]) * \
			(1 - (-(np.log(ratiof+4)/np.log(ratiof+2))+2))
		alpha = p_rt + p_nrt

		prob = p_rt / alpha
		# Tweet if possibile
		if np.random.random() <= prob:
			# print("tweet %d" % s)
			sim.post(user, sim.now)

def mp_step_retweet(sim, ind):
	s, e = ind
	l = len(sim.users.keys())
	for u in range(s, e):
		user = sim.get_user(u)
		ratiof = (float(len(user.followings)) / l)
		p_rt = float(user.tz[sim.now % 12]) * \
			(-(np.log(ratiof+4)/np.log(ratiof+2))+2)
		p_nrt = (1 - user.tz[sim.now % 12]) * \
			(1 - (-(np.log(ratiof+4)/np.log(ratiof+2))+2))

		alpha = p_rt + p_nrt
		prob = p_rt / alpha
		if np.random.random() <= prob:
			# print('retweets %d' % s)
			sim.repost(user, sim.now)

def mp_attachment_eval(sim, ind):
	s, e = ind
	sample = np.random.random(size=sim.total_users)
	for u in range(s, e):
		if sample[u] <= 0.005:
			# print("unfollow %d" % s)
			user = sim.get_user(u)
			fov = user.generate_fov(sim.now, sim.tweet, sim.retweet, sim.dtag)
			for t in fov[0]:
				if user.pi[t[2]] >= user.pi_average:
					if t[0] in user.attachment:
						user.attachment[t[0]] = (user.attachment[t[0]] + t[3]) / 2
				else:
					if t[0] in user.attachment:
						user.attachment[t[0]] = (user.attachment[t[0]] + t[4]) / 2
			for t in fov[1]:
				if user.pi[t[2]] >= user.pi_average:
					if t[0] in user.attachment:
						user.attachment[t[0]] = (user.attachment[t[0]] + t[3]) / 2
					if t[6] in user.attachment:
						user.attachment[t[6]] = (user.attachment[t[6]] + t[3]) / 2
				else:
					if t[0] in user.attachment:
						user.attachment[t[0]] = (user.attachment[t[0]] + t[4]) / 2 
					if t[6] in user.attachment:
						user.attachment[t[6]] = (user.attachment[t[6]] + t[4]) / 2
		
			try:
				choosen = min(user.attachment, key=user.attachment.get)
				sim.network.remove_edge(u=user.id,v=choosen)
				user.attachment.pop(choosen,None)
				user.rm_following(choosen)
				sim.get_user(choosen).rm_follower(user.id)
			except:
				pass

def mp_simulation_step(sim, threads):
	chunks = list(multi_chunks(sim.total_users, threads))

	mp_start_process(mp_personal_follow, sim, chunks)
	mp_start_process(mp_step_tweet, sim, chunks)
	mp_start_process(mp_step_retweet, sim, chunks)
	mp_start_process(mp_attachment_eval, sim, chunks)



		