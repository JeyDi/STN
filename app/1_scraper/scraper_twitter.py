import twint
import nest_asyncio
import pandas as pd
nest_asyncio.apply()

c = twint.Config()
c.Username = "GiuseppeConteIT"
c.Store_csv = True
c.Output=("./conte_followers.csv")
#twint.run.Followers(c)

conte_df = pd.read_csv('./conte_followers.csv').iloc[1950:2000]


error_list=[]
c = twint.Config()
for user in conte_df['username']:
    try:
        c.Username = user
        c.Store_csv = True
        c.Output=("./conte_followers/"+user+"_followers.csv")
        twint.run.Followers(c)
        print(user + " downloaded") 
    except:
        print(user + " ERROR")
        error_list.append(user)  
        
    
   