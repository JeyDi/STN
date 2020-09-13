import networkx as nx
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot


def build_graph(G, G_node_pos, step):
    """
    Effettivamente si occupa della visualizzazione, setta la posizione, va a costruire i link tra i nodi (tutte le linee tra i nodi)
    Setta la posizione dei vari punti
    attenzione allo spring_layout del grafo (ci mette tanto)
    """
    nx.set_node_attributes(G, G_node_pos, "pos")

    edge_x, edge_y = build_edges_list(G)

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
        name="Links",
    )

    node_x, node_y, node_text, node_state = build_nodes_list(G)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        text=node_text,
        name="Overview",
        marker=dict(color=list(map(get_color, node_state)), size=10, line_width=2),
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="Conte followers - STEP " + str(step),
            titlefont_size=16,
            showlegend=True,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[
                dict(
                    text="",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.005,
                    y=-0.002,
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )
    return fig


def build_edges_list(G):
    """
    Crea le connessioni tra i nodi
    """
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]["pos"]
        x1, y1 = G.nodes[edge[1]]["pos"]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    return edge_x, edge_y


def build_nodes_list(G):
    """
    Crea e definisce i nodi del grafo
    """
    node_x = []
    node_y = []
    node_text = []
    node_state = []

    for node in G.nodes():
        x, y = G.nodes[node]["pos"]
        node_x.append(x)
        node_y.append(y)

        try:
            if G.nodes[node].get("type") != None:
                if G.nodes[node].get("type") == "1":
                    node_state.append(1)  # OPINION LEADER
                    node_text.append("OPINION LEADER")
                elif G.nodes[node].get("type") == "2":  # BOT
                    node_state.append(2)
                    node_text.append("BOT")

            elif G.nodes[node]["state"] == "not_exposed":  # NOT EXSPOSED
                node_state.append(0)
                node_text.append("NOT EXPOSED")

            elif G.nodes[node]["state"] == "exposed":  # EXPOSED
                if G.nodes[node]["infected_type"] == "1":  # EXPOSED BY OP LEAD
                    node_state.append(3)
                    node_text.append("EXPOSED BY OP LEAD")
                elif G.nodes[node]["infected_type"] == "2":  # EXPOSED BY BOT
                    node_state.append(4)
                    node_text.append("EXPOSED BY BOT")
                elif G.nodes[node]["infected_type"] == "0":  # EXPOSED BY USER
                    node_state.append(5)
                    node_text.append("EXPOSED BY USER")

            elif G.nodes[node]["state"] == "infected":
                if G.nodes[node]["infected_type"] == "1":  # INFECTED BY OP LEAD
                    node_state.append(6)
                    node_text.append("INFECTED BY OP LEAD")
                elif G.nodes[node]["infected_type"] == "2":  # INFECTED BY BOT
                    node_state.append(7)
                    node_text.append("INFECTED BY OP BOT")
                elif G.nodes[node]["infected_type"] == "0":  # INFECTED BY USER
                    node_state.append(8)
                    node_text.append("INFECTED BY USER")

        except Exception as e:
            print(f"Error on node: {G.nodes[node]}")
            print(e)

    return node_x, node_y, node_text, node_state


def get_color(elem):
    if elem == 0:
        return "green"
    elif (elem >= 1 and elem <= 2) or (elem >= 6 and elem <= 8):
        return "red"
    elif elem >= 3 and elem <= 5:
        return "orange"
