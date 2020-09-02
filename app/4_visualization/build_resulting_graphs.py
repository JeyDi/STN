import networkx as nx
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

def step_graph(G, df, step):
    df_id = df[df['key'] == 'id' ].reset_index()

    df_infected_type = df[df['key'] == 'infected_type' ].reset_index()

    df_type = df[df['key'] == 'type' ]   # DF with opinion leader and bot
    df_type['agent_id'] = df_type['agent_id'].astype('str')
    df_type = df_type.set_index('agent_id')
    nx.set_node_attributes(G, df_type['value'].to_dict(), 'type') 

    i = 0
    while i <= step:
        step_df = df_id[df_id['t_step'] == i]
        step_df['agent_id'] = step_df['agent_id'].astype('str')
        step_df = step_df.set_index('agent_id')
        nx.set_node_attributes(G, step_df['value'].to_dict(), 'state')

        step_infected_type = df_infected_type[df_infected_type['t_step'] == i]
        step_infected_type['agent_id'] = step_infected_type['agent_id'].astype('str')
        step_infected_type = step_infected_type.set_index('agent_id')
        nx.set_node_attributes(G, step_infected_type['value'].to_dict(), 'infected_type')

        i = i + 1    #INTERVAL IN AGENT PARAMETER

    return G.copy()

def build_graph(G, G_node_pos, step):
    nx.set_node_attributes(G, G_node_pos, 'pos')

    edge_x, edge_y = build_edges_list(G)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines',
        name='Links')


    node_x, node_y, node_text, node_state = build_nodes_list(G)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text = node_text,
        name='Overview',
        marker=dict(
                    color=list(map(get_color, node_state)),
                    size=10,
                    line_width=2))

    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='Conte followers - STEP ' + str(step),
                titlefont_size=16,
                showlegend=True,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    return fig

def build_edges_list(G):
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
      
    return edge_x, edge_y

def build_nodes_list(G):
    node_x = []
    node_y = []
    node_text = []
    node_state = []

    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

        try:
            if G.nodes[node].get('type') != None:
                if G.nodes[node].get('type') == '1':
                    node_state.append(1)                #OPINION LEADER
                    node_text.append('OPINION LEADER')
                elif G.nodes[node].get('type') == '2': #BOT
                    node_state.append(2)
                    node_text.append('BOT')
    
            elif G.nodes[node]['state'] == 'not_exposed': #NOT EXSPOSED
                node_state.append(0)
                node_text.append('NOT EXPOSED')
    
            elif G.nodes[node]['state'] == 'exposed':  #EXPOSED
                if G.nodes[node]['infected_type'] == '1':  #EXPOSED BY OP LEAD
                    node_state.append(3)
                    node_text.append('EXPOSED BY OP LEAD')
                elif G.nodes[node]['infected_type'] == '2': #EXPOSED BY BOT
                    node_state.append(4)
                    node_text.append('EXPOSED BY BOT')
                elif G.nodes[node]['infected_type'] == '0': #EXPOSED BY USER
                    node_state.append(5)
                    node_text.append('EXPOSED BY USER')
                    
            elif G.nodes[node]['state'] == 'infected':
                if G.nodes[node]['infected_type'] == '1':  #INFECTED BY OP LEAD
                    node_state.append(6)
                    node_text.append('INFECTED BY OP LEAD')
                elif G.nodes[node]['infected_type'] == '2': #INFECTED BY BOT
                    node_state.append(7)
                    node_text.append('INFECTED BY OP BOT')
                elif G.nodes[node]['infected_type'] == '0': #INFECTED BY USER
                    node_state.append(8)
                    node_text.append('INFECTED BY USER')
                    
        except Exception as e:
                print(f'Error on node: {G.nodes[node]}')
                print(e)

    return node_x, node_y, node_text, node_state

def get_color(elem):
    if elem == 0:
        return 'green'
    elif (elem >= 1 and elem <= 2) or (elem >= 6 and elem <= 8):
        return 'red'
    elif (elem >= 3 and elem <= 5):
        return 'orange'

if __name__ == '__main__':    
    # Main graph
    G = nx.read_gexf('../2_graph_builder/graph_500_int_direct.gexf')

    # Simulations' data
    df_random = pd.read_csv('../3_soil_simulation/soil_output/random_500/random_500_trial_0.csv')
    
    df_top_btw = pd.read_csv('../3_soil_simulation/soil_output/top_btw_500/top_btw_500_trial_0.csv')

    df_top_eigenvector = pd.read_csv('../3_soil_simulation/soil_output/top_eigenvector_500/top_eigenvector_500_trial_0.csv')

    # Shared layout
    G_node_pos = nx.spring_layout(G)
    
    for val in ['random', 'btw', 'eigenvector']:
        df = None
        
        if val == 'random':
            df = df_random
        elif val == 'btw':
            df = df_top_btw
        elif val == 'eigenvector':
            df = df_top_eigenvector
            
        for i in range(5):
            G_step = None
            G_step = step_graph(G, df, i)
    
            nx.write_gexf(G_step, f'./output_graph/{val}/G_{val}_step{i}.gexf')
            plot(build_graph(G_step , G_node_pos, i), filename=f'./output_html/{val}/{val}_step{i}.html')
            print(f"{val} - STEP {i} DONE")