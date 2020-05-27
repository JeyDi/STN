import numpy as np
from user import User


class Simulation:
    def __init__(self, topics, total_users,network):
        self.topics = topics
        self.tweet = {}
        self.retweet = {}
        self.dtag = {}
        self.user_id = 1
        self.total_users = total_users
        self.users = {}
        self.now = 0
        self.network = network

        # Iper-parameters
        self.alpha = 0.8
        self.beta = 0.6
        self.gamma = 0.4

    def add_user(self, user):
        self.users[user.id] = user

    def post(self, user, time):
        j = np.random.choice(self.topics, 1, p=user.pi)[0]
        print(j)

        if user.pi[j] >= user.pi_average:
            likability = Simulation.random_high(0.7)
            dislakability = np.random.random()
        else:
            dislakability = Simulation.random_high(0.7)
            likability = np.random.random()

        dtag = self.generate_dtag(user)
        if dtag:
            self.get_user(dtag).add_dtag(self.now, user)

        self.tweet[user.id, time] = [user.id, time, j, likability, dislakability, dtag]

    def generate_dtag(self, user):
        # TODO
        return None

    def skl_d(self,p,q):
        kl1 = 0
        for i in range(0, len(p)):
            kl1 = kl1 + p[i]*np.log2(p[i]/q[i])
        kl2 = 0
        for j in range(0, len(q)):
            kl2 = kl2 + q[j]*np.log2(q[j]/p[j])
        return np.mean([kl1,kl2])

    def kl_d(self,p,q):
        kl1 = 0
        for i in range(0, len(p)):
            kl1 = kl1 + p[i]*np.log2(p[i]/q[i])
        return kl1

    def omofilia(self,p,q):
        somma = 0
        for z in range(0,len(p)):
            avg = (p[z]+q[z])/2
            somma = somma + ((np.power(p[z]-avg,2)+np.power(q[z]-avg,2))/2)*p[z]
        return 1-somma

    def repost(self, user, time):
        fov = user.generate_fov(time,self.tweet,self.retweet)
        if (not(not fov[0] and not fov[1] and not fov[2])):
            for t in fov[0]:
                avg = (user.pi[t[2]] + t[3]) / 2
                thresh = avg
                if np.random.random() <= thresh:
                    self.retweet[user.id, time] = t
            for t in fov[1]:
                avg = (user.pi[t[2]] + t[3]) / 2
                thresh = avg
                if np.random.random() <= thresh:
                    self.retweet[user.id, time] = t
                if t[0] not in user.followings:
                    print("#########################")
                    print("#                       #")
                    print("#                       #")
                    print("#        giggity        #")
                    print("#                       #")
                    print("#                       #")
                    print("#########################")
                    #e = 8/0
                    a = [self.tweet[key][2] for key in self.tweet.keys() if key[0] == t[0] and key[1] >= time-20]
                    print(a)
                    if a:
                        hist, bins=np.histogram(a,bins=list(range(0,self.topics+1)),density=True)
                        kl = self.omofilia(np.array(user.pi),np.array(hist))
                        if kl > 0.97:
                            self.new_follow(user.id,t[0])
                        # print(np.array(user.pi))
                        # print(np.array(hist))
                        # print(kl)


    # user1 -follow-> user2
    def new_follow(self, user1, user2):
        self.get_user(user1).add_following(user2)
        self.get_user(user2).add_follower(user1)

        # change attachment to random-high
        self.get_user(user1).attachment[user2] = Simulation.random_high(0.8)

        self.network.add_edge(u=user1,v=user2)
        # print('Edges: %d' % len(self.network.edges()))

    def get_user(self, id):
        return self.users[id]

    def step_tweet(self):
        l = self.users.keys()
        for u in l:
            # Calculate probability of TWEET
            user = self.get_user(u)
            p_rt = user.tz[self.now % 12] * \
				(float(len(user.followers)) / len(l))
            p_nrt = (1 - user.tz[self.now % 12]) * \
				(1 - (float(len(user.followers)) / len(l)))
            #print('probabbile: ' + str(user.followers))
            alpha = p_rt + p_nrt
            # prob = self.alpha * \
            # 	   user.tz[self.now % 12] * \
            # 	   len(user.followers) / \
            # 	   self.total_users
            prob = (user.tz[self.now % 12] *
                    len(user.followers) /
                    self.total_users) / alpha
            # print(prob)

            # Tweet if possibile
            if np.random.random() <= prob:
                print('%d tweets' % u)
                self.post(user, self.now)

    def step_retweet(self):
        print(self.users.keys())
        l = self.users.keys()
        for u in l:
            user = self.get_user(u)
            p_rt = user.tz[self.now % 12] * \
				(float(len(user.followings)) / len(l))
            p_nrt = (1 - user.tz[self.now % 12]) * \
				(1 - (float(len(user.followings)) / len(l)))
            alpha = p_rt + p_nrt
            prob = (user.tz[self.now % 12] *
                    len(user.followings) /
                    self.total_users) / alpha

            if np.random.random() <= prob:
                print('%d retweets' % u)
                self.repost(user, self.now)
        return True

    def step_evaluation(self):
        for u in self.users.keys():
            # Get FOV of U
            user = self.get_user(u)
            fov = user.generate_fov(self.now, self.tweet, self.retweet)
            print('fov:')
            print(fov)
            for twt in fov[0]:
                # Evaluate attachment
                print("TWEET EVALUATION")
                print(twt)

            for rtwt in fov[1]:
                print("RETWEET EVALUATION")
                print(rtwt)

            for dtag in fov[2]:
                # TODO EVALUATE DTAG
                pass

        return True

    @staticmethod
    def random_high(mean):
        return np.random.triangular(0.4, mean, 1)

    @staticmethod
    def random_low(mean):
        return np.random.triangular(0, mean, 0.6)


def test():
    import networkx as nx
    
    network = nx.gnm_random_graph(50,
                                  50,
                                  directed=True)
    sim = Simulation(10, 50, network)

    # generate users
    print('Generation')
    print('=' * 20)
    for n in network.nodes():
        u1 = User(n, sim.topics)
        sim.add_user(u1)
        print(sim.get_user(n))

    # add follow
    print('Follow')
    print('=' * 20)
    for e in network.edges():
        # sim.new_follow(n, (n + 1) % sim.total_users)
        # sim.new_follow(n, (n + 2) % sim.total_users)
        # sim.new_follow(n, (n + 3) % sim.total_users)
        # sim.new_follow(n, (n + 4) % sim.total_users)
        # sim.new_follow(n, (n + 5) % sim.total_users)
        # sim.new_follow(n, (n + 6) % sim.total_users)
        sim.new_follow(e[0],e[1])
        print(sim.get_user(e[0]).get_attachment(e[1]))
        

    print('Simulation')
    print('=' * 20)
    flag = 0
    while(flag>-1):
        print('Time: %d Edges: %d' % (sim.now, len(network.edges())))
        print('Tweets: %d' % len(sim.tweet))
        print('Retweets: %d' % len(sim.retweet))
        sim.step_tweet()
        sim.step_retweet()
        #sim.step_evaluation()
        sim.now += 1
        flag += 1

#	sim.get_user(0).generate_fov(0, sim.tweet, sim.retweet)


if __name__ == '__main__':
    test()
