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
        
        if G.nodes[node]['state'] == 'not_exposed':
            node_state.append(0)
        elif G.nodes[node]['state'] == 'exposed':
            node_state.append(1)
        elif G.nodes[node]['state'] == 'infected':
            node_state.append(2)

    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
                    showscale=False,
                    # colorscale options
                    #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                    #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                    #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                    #colorscale='Rainbow',
                    reversescale=True,
                    color=['rgb(255, 0, 0)','rgb(0, 239, 0)', 'rgb(0, 9, 253)'],
                    size=10,  #noze size
                    
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
    df = df[df['key'] == 'id' ].reset_index()
    i=0
    #node_dict = {}
    while i<=step:
        step_df = df[df['t_step']== i].drop(['index', 'key', 't_step' ], axis=1)
        step_df['agent_id'] = step_df['agent_id'].astype(int)
        step_df = step_df.sort_values(by=['agent_id'])
        step_df['agent_id'] = step_df['agent_id'].astype(str)
        step_df = step_df.set_index('agent_id')
        node_dict = step_df.to_dict()
        #node_dict.update(step_df.to_dict())
        
        nx.set_node_attributes(G, node_dict['value'], 'state')
        
        i = i+1    #INTERVAL IN AGENT PARAMETER
        
        
    
    #plot(visualize_graph(G))
    return G.copy()

G = nx.read_gexf('./soil/graph_200_int.gexf')
df = pd.read_csv('./soil/soil_output/MyExampleSimulation/MyExampleSimulation_trial_0.csv')

#Visualize
G_node_pos = nx.spring_layout(G)
step = 0
G0 = step_graph(G, df, step)
plot(visualize_graph(G0,G_node_pos, step))

step=1
G1 = step_graph(G, df, step)
plot(visualize_graph(G1,G_node_pos, step))

step=2
G2 = step_graph(G, df, step)
plot(visualize_graph(G2,G_node_pos, step))

step=3
G3 = step_graph(G, df, step)
plot(visualize_graph(G3, G_node_pos, step))

step=4
G4 = step_graph(G, df, step)
plot(visualize_graph(G4, G_node_pos, step))