import counters as cn
import networkx as nx
import pandas as pd
import plotly.express as px
from plotly.offline import plot


def print_stats(G):
    not_exposed = cn.count_not_exposed(G)

    exposed = cn.count_exposed(G)
    exposed_opinion_leader = cn.count_exposed_opinion_leader(G)
    exposed_bot = cn.count_exposed_bot(G)
    exposed_user = cn.count_exposed_user(G)

    infected = cn.count_infected(G)
    infected_opinion_leader = cn.count_infected_opinion_leader(G)
    infected_bot = cn.count_infected_bot(G)
    infected_user = cn.count_infected_user(G)

    print(f'Not exposed: {not_exposed}')
    print(f'Exposed: {exposed}')
    print(f'\tFrom Opinion Leader: {exposed_opinion_leader}, from BOT: {exposed_bot}, from users: {exposed_user}')
    print(f'Infected: {infected}')
    print(f'\tFrom Opinion Leader: {infected_opinion_leader}, from BOT: {infected_bot}, from users: {infected_user}')
  





if __name__ == '__main__':
    
    df_final_exposed = pd.DataFrame(columns=['bot', 'exposed'])
    for val in ['random', 'btw', 'eigenvector']:
        print(f'PRINTING {val} GRAPH STATS')
        df_step = pd.DataFrame(columns=['type', 'step', 'value'])
        df_exposed = pd.DataFrame(columns=['step', 'type' , 'value'])
        for i in range(5): 
            G = nx.read_gexf(f'../4_visualization/output_graph/{val}/G_{val}_step{i}.gexf')
            print(f'STEP {i}:')
            print_stats(G)
            print()     
            
            # Line chart
            df_step = df_step.append({'type':'not_exposed', 'step' : i, 'value' : cn.count_not_exposed(G)}, ignore_index=True)
            df_step = df_step.append({'type':'exposed', 'step' : i, 'value' : cn.count_exposed(G)}, ignore_index=True)
            df_step = df_step.append({'type':'infected', 'step' : i, 'value' : cn.count_infected(G)}, ignore_index=True)            
            line_chart = px.line(df_step, x='step', y='value', color='type', title=val)
            
            #Bar chart
            df_exposed = df_exposed.append({'step' : i, 'type' : 'opinion_leader', 'value' : cn.count_exposed_opinion_leader(G)}, ignore_index=True)
            df_exposed = df_exposed.append({'step' : i, 'type' : 'bot', 'value' : cn.count_exposed_bot(G)}, ignore_index=True)
            df_exposed = df_exposed.append({'step' : i, 'type' : 'user', 'value' : cn.count_exposed_user(G)}, ignore_index=True)
            bar_chart = px.bar(df_exposed, x='step', y = 'value', color = 'type', title = val )
            
        df_final_exposed = df_final_exposed.append({'bot' : val, 'exposed' : cn.count_exposed(G)}, ignore_index=True)
        plot(line_chart,   filename=f'./charts/steps/{val}.html')
        plot(bar_chart,   filename=f'./charts/exposed_type/{val}.html')

        print()
        
    bar_chart = px.bar(df_final_exposed, x='bot', y='exposed')
    plot(bar_chart, filename=f'./charts/final_exposed/final_exposed.html')

        
