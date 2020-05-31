import twint
import nest_asyncio
nest_asyncio.apply()

c = twint.Config()
#c.Username = "GiuseppeConteIT"

c.Search = "covid AND conte"
c.Since = "2020-05-03"
c.Until = "2020-05-04"
c.Lang = "it"
c.limit= 20
c.Store_csv = True
c.Output=("./df.csv")

#Run
twint.run.Search(c)
