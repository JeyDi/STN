import numpy as np


class User:
	def __init__(self, node_id, topic):
		#node['id'] = self.id
		self.id = node_id
		self.attachment = {}
		#self.node = node

		#node['user'] = self

		# personal interest
		pi = np.random.random_integers(100, size=(1, topic))[0].tolist()
		sumpi = sum(pi)
		fpi = list(map(lambda x: float(x) / sumpi, pi))
		self.pi = fpi
		self.pi_average = np.average(fpi)

		# timezone (refer to documentation)
		tz = np.zeros(12)
		i = np.random.randint(13) + 4
		i = i % 12

		# low activity
		for k in range(4):
			tz[(k + i) % 12] = np.random.triangular(0, 0.25, 0.6)
		i = (i + 4) % 12

		# high activity
		for k in range(4):
			tz[(k + i) % 12] = np.random.triangular(0.4, 0.75, 1)

		self.tz = tz.tolist()
		self.followers = []
		self.followings = []
		self.dtag = {}

		interest = []
		for j in range(topic):
			if self.pi[j] > 0.5:
				interest.append(j)
		self.interest = interest

	def generate_fov(self, time, tweets, retweets, d_tags):
		fings = len(self.followings)
		fers = len(self.followers)
		#t = len(tweets)
		#r = len(retweets)
		
		# Generate tweets
		#usrs_choice = np.random.choice(f + 1, f/4)
		if time >= 0:
			## solo questa riga
			time_choice = np.random.choice(time + 1, 1)[0]
		else:
			time_choice = -1*np.random.choice(-time + 1, 1)[0]
		
		twts = []
		for i in range(fings):
			for t in range(time_choice, time + 1):
				try:
					twts.append(tweets[self.followings[i], t])
				except:
					pass

		# Generate retweets
		rtwts = []
		for i in range(fings):
			for t in range(time_choice, time + 1):
				try:
					rtwts.append(retweets[self.followings[i], t]+[self.followings[i]])
				except:
					pass

		# Generate DTAGs
		# TODO
		# for i in range(fings):
		#     for t in range(time_choice, time + 1):
		#         try:
		#             rtwts.append(self.d_tags[t])
		#         except:
		#             pass
		try:
			for x in self.dtags[time_choice]:
				rtwts.append(x)
		except:
			pass

		return (twts, rtwts)

	def add_follower(self, follower):
		self.followers.append(follower)

	def add_following(self, following):
		self.followings.append(following)

	def rm_follower(self, follower):
		self.followers.remove(follower)

	def rm_following(self, following):
		self.followings.remove(following)

	def get_attachment(self, u):
		try:
			return self.attachment[u]
		except:
			return -1

	def get_dtag(self, time):
		try:
			return self.dtag[time]
		except:
			return None

	def add_dtag(self, time, tweet):
		if self.get_dtag(time):
			self.dtag[time].append(tweet)
		else:
			self.dtag[time] = [tweet]

	def __str__(self):
		stri = ''
		stri += ('User id: %d\n' % self.id)
		stri += 'PI:\n'
		stri += str(self.pi)
		stri += '\nTZ:\n'
		stri += str(self.tz)
		stri += '\nFollowers:\n'
		stri += str(self.followers)
		stri += '\nFollowings:\n'
		stri += str(self.followings)
		return stri
