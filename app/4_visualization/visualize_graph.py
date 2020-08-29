import networkx as nx
import plotly.graph_objects as go
from plotly.offline import plot

def visualize_graph(G, G_node_pos, step):
   # G_node_pos = nx.spring_layout(G)
    nx.set_node_attributes(G,G_node_pos, 'pos' )

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

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    node_state = []

    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

        node_text.append(node)

        try:
            if G.nodes[node].get('type') != None:
                if G.nodes[node].get('type') == '1':
                    node_state.append(1)                #OPINION LEADER
                elif G.nodes[node].get('type') == '2': #BOT
                    node_state.append(2)
        
            elif G.nodes[node]['state'] == 'not_exposed': #NOT EXSPOSED
                node_state.append(0)
        
            elif G.nodes[node]['state'] == 'exposed':  #EXPOSED
                if G.nodes[node]['infected_type'] == '1':  #EXPOSED BY OP LEAD
                    node_state.append(3)
                elif G.nodes[node]['infected_type'] == '2': #EXPOSED BY BOT
                    node_state.append(4)
                elif G.nodes[node]['infected_type'] == '0': #EXPOSED BY USER
                    node_state.append(5)
        
            elif G.nodes[node]['state'] == 'infected':
                if G.nodes[node]['infected_type'] == '1':  #INFECTED BY OP LEAD
                    node_state.append(6)
                elif G.nodes[node]['infected_type'] == '2': #INFECTED BY BOT
                    node_state.append(7)
                elif G.nodes[node]['infected_type'] == '0': #INFECTED BY USER
                    node_state.append(8)
        except:
            print("Error on node: " + str(G.nodes[node]))

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
                    showscale=True,
                    # colorscale options
                    #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                    #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                    #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                    colorscale='Rainbow',
                    reversescale=True,
                    #color=['rgb(255, 0, 0)','rgb(0, 239, 0)', 'rgb(0, 9, 253)'],
                    size=10,  #noze size
                    colorbar=dict(
                        thickness=15,
                        title='',
                        xanchor='left',
                        titleside='right'
                    ),
                    line_width=2))

    node_trace.text = node_text
    node_trace.marker.color = node_state

    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='Conte followers - STEP ' + str(step),
                titlefont_size=16,
                showlegend=False,
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



import pandas as pd


def step_graph(G, df, step):
    df_id = df[df['key'] == 'id' ].reset_index()

    df_infected_type = df[df['key'] == 'infected_type' ].reset_index()
    
    df_type = df[df['key'] == 'type' ]   # DF with opinion leader and bot
    df_type['agent_id'] = df_type['agent_id'].astype('str')
    df_type = df_type.set_index('agent_id')
    nx.set_node_attributes(G, df_type['value'].to_dict(), 'type') 

    i=0
    #node_dict = {}
    while i<=step:

        step_df = df_id[df_id['t_step'] == i]
        step_df['agent_id'] = step_df['agent_id'].astype('str')
        step_df = step_df.set_index('agent_id')
        nx.set_node_attributes(G, step_df['value'].to_dict(), 'state')

        step_infected_type = df_infected_type[df_infected_type['t_step'] == i]
        step_infected_type['agent_id'] = step_infected_type['agent_id'].astype('str')
        step_infected_type = step_infected_type.set_index('agent_id')
        nx.set_node_attributes(G, step_infected_type['value'].to_dict(), 'infected_type')


        i = i+1    #INTERVAL IN AGENT PARAMETER

    #plot(visualize_graph(G))
    return G.copy()

G = nx.read_gexf('../2_graph_builder/graph_500_int_direct.gexf')
df = pd.read_csv('../3_soil_simulation/soil_output/top_eigenvector_500/top_eigenvector_500_trial_0.csv')

#Visualize
#G_node_pos = nx.spring_layout(G)


step = 0
G0 = step_graph(G, df, step)
nx.write_gexf(G0, '../5_statistics/G_eigenvector_step0.gexf')
#plot(visualize_graph(G0,G_node_pos, step))

step=1
G1 = step_graph(G, df, step)
nx.write_gexf(G1, '../5_statistics/G_eigenvector_step1.gexf')
#plot(visualize_graph(G1,G_node_pos, step))

step=2
G2 = step_graph(G, df, step)
nx.write_gexf(G2, '../5_statistics/G_eigenvector_step2.gexf')
#plot(visualize_graph(G2,G_node_pos, step))

step=3
G3 = step_graph(G, df, step)
nx.write_gexf(G3, '../5_statistics/G_eigenvector_step3.gexf')
#plot(visualize_graph(G3, G_node_pos, step))

step=4
G4 = step_graph(G, df, step)
nx.write_gexf(G4, '../5_statistics/G_eigenvector_step4.gexf')
#plot(visualize_graph(G4, G_node_pos, step))
