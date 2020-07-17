import twint
import nest_asyncio

nest_asyncio.apply()

user= "MinisteroSalute"
file_name= "Followers_"+user
path="./"+file_name+".csv"
print(path)
c = twint.Config()
c.Username = user
c.Output=(path)
c.Limit = 10000
c.Store_csv = True
twint.run.Followers(c)
