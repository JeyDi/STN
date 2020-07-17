import twint
import nest_asyncio
import os
import time

nest_asyncio.apply()

from csv import reader

users=[]
with open('Followers_MinisteroSalute.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    for row in csv_reader:
        users.append(row)
users.pop(0) #to delete the header
for u in users:
    user= ""+u[0]
    print(user)
    file_name= "Followers_"+user
    path="./FollowersMinisteroSalute1/"+file_name+".csv"
    print(path)
    if not os.path.exists(path):
        c = twint.Config()
        c.Username = user
        c.Output=(path)
        c.Limit = 5000
        c.Store_csv = True
        try:
            twint.run.Followers(c)
        except Exception as e:
            print(e)
            print("Continue in 1 sec")
            time.sleep(1)
