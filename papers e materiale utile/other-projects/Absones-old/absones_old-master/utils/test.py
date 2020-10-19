import sqlite3
import random, sys, datetime

tweet = {}

for i in range(5000):
	for j in range(360):
		tweet[i,j] = [random.random(),random.random(),i, j]

print(sys.getsizeof(tweet)/1048576)

start = datetime.datetime.now()
a = [tweet[key] for key in tweet.keys() if key[0] == 21]

print(datetime.datetime.now() - start)
print(len(a))