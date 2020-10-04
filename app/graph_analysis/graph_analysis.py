import networkx as nx
from pprint import pprint
import plotly.express as px
import pandas as pd

def getKey(neighbors):
    ret = ''

    if neighbors in range(0, 6):
        ret = '0-5'
    elif neighbors in range(6, 11):
        ret = '6-10'
    elif neighbors in range(11, 21):
        ret = '11-20'
    elif neighbors in range(21, 51):
        ret =  '21-50'
    elif neighbors in range(51, 101):
        ret =  '51-100'
    elif neighbors in range(101, 251):
        ret =  '101-250'
    elif neighbors in range(251, 501):
        ret = '251-500'
    elif neighbors > 500:
        ret = '500+'

    return ret

if __name__ == "__main__":

    data = dict()
    
    # counter = {
    #     '0-5' : 0,
    #     '6-10' : 0,
    #     '11-20' : 0,
    #     '21-50' : 0,
    #     '51-100' : 0,
    #     '101-250' : 0,
    #     '251-500' : 0,
    #     '500+' : 0
    # }

    # for graph in ['500-users', '1000-users', '1500-users', '2000-users']:
    #     data[graph] = counter.copy()
    #     G = nx.read_gexf(f'./{graph}.gexf')
    #     for node in G.nodes():
    #         neighbors = G.neighbors(node)
    #         key = getKey(len(list(neighbors)))
    #         data[graph][key] += 1
    # pprint(data, sort_dicts=False)

    # import json
    # with open("data_file.json", "w") as write_file:
    #     json.dump(data, write_file)


    graph_list = ['500-users', '1000-users', '1500-users', '2000-users']
    # graph_list = ['500-users']
    for graph in graph_list:
        data[graph] = dict()
        G = nx.read_gexf(f'./{graph}.gexf')
        for node in G.nodes():
            neighbors = G.neighbors(node)
            key = len(list(neighbors))

            if(data[graph].get(key) is None):
                data[graph][key] = 1
            else:
                data[graph][key] += 1
    

        df = pd.DataFrame({
            "Number of Nodes" : data[graph].values(),
            "Number of Links" : data[graph].keys()
        })
        print(df)

        # test with px.line
        fig = px.scatter(
            df,
            x="Number of Links",
            y="Number of Nodes"
        )
        fig.update_layout(title=f"{graph}-graph nodes distribution")
        fig.show()
        # fig.write_image(f"{graph}.pdf")

        del df
    