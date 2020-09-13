import statistics.counters as cn
import networkx as nx
import pandas as pd
import plotly.express as px
from plotly.offline import plot
import streamlit as st


def print_stats(G, step, graph_name):
    not_exposed = cn.count_not_exposed(G)

    exposed = cn.count_exposed(G)
    exposed_opinion_leader = cn.count_exposed_opinion_leader(G)
    exposed_bot = cn.count_exposed_bot(G)
    exposed_user = cn.count_exposed_user(G)

    infected = cn.count_infected(G)
    infected_opinion_leader = cn.count_infected_opinion_leader(G)
    infected_bot = cn.count_infected_bot(G)
    infected_user = cn.count_infected_user(G)

    # Print informations for debug purpose on terminal
    print("---------------------------------------")
    print(f"\nSTEP {step}:")
    print(f"Not exposed: {not_exposed}")
    print(f"Exposed: {exposed}")
    print(
        f"\tFrom Opinion Leader: {exposed_opinion_leader}, from BOT: {exposed_bot}, from users: {exposed_user}"
    )
    print(f"Infected: {infected}")
    print(
        f"\tFrom Opinion Leader: {infected_opinion_leader}, from BOT: {infected_bot}, from users: {infected_user}"
    )

    # Print on GUI
    st.markdown("---------------")
    st.markdown(f"**STEP: {step} results of: {graph_name}**")
    st.markdown(f"Not exposed: {not_exposed}")
    st.markdown(f"Exposed: {exposed}")
    st.markdown(
        f"\tFrom Opinion Leader: {exposed_opinion_leader}, from BOT: {exposed_bot}, from users: {exposed_user}"
    )
    st.markdown(f"Infected: {infected}")
    st.markdown(
        f"\tFrom Opinion Leader: {infected_opinion_leader}, from BOT: {infected_bot}, from users: {infected_user}"
    )


def generate_plots(graph_name, graph_steps):
    """
    Generate the final plots and call the statistics print function
    Args:
        graph_name (str): number of the result graph saved in the previos logical step
        graph_steps (int): number of steps you want to execute (depend on the steps are inside the graph)

    Returns:
        [list]: List of plotly plots
    """
    df_final_exposed = pd.DataFrame(columns=["bot", "exposed"])
    df_step = pd.DataFrame(columns=["type", "step", "value"])
    df_exposed = pd.DataFrame(columns=["step", "type", "value"])

    st.markdown("")

    for i in range(graph_steps):
        # read graph and print stats
        graph_result_path = "./data/output/"
        G = nx.read_gexf(f"{graph_result_path}G_{graph_name}_step{i}.gexf")
        print_stats(G, i, graph_name)

        # LINE CHART (append informations into dataframe)
        df_step = df_step.append(
            {"type": "not_exposed", "step": i, "value": cn.count_not_exposed(G)},
            ignore_index=True,
        )
        df_step = df_step.append(
            {"type": "exposed", "step": i, "value": cn.count_exposed(G)},
            ignore_index=True,
        )
        df_step = df_step.append(
            {"type": "infected", "step": i, "value": cn.count_infected(G)},
            ignore_index=True,
        )
        line_chart = px.line(
            df_step,
            x="step",
            y="value",
            color="type",
            title=f"Infection overall: {graph_name} step: {i}",
        )

        # BAR CHART (append informations into dataframe)
        df_exposed = df_exposed.append(
            {
                "step": i,
                "type": "opinion_leader",
                "value": cn.count_exposed_opinion_leader(G),
            },
            ignore_index=True,
        )
        df_exposed = df_exposed.append(
            {"step": i, "type": "bot", "value": cn.count_exposed_bot(G)},
            ignore_index=True,
        )
        df_exposed = df_exposed.append(
            {"step": i, "type": "user", "value": cn.count_exposed_user(G)},
            ignore_index=True,
        )
        bar_chart = px.bar(
            df_exposed,
            x="step",
            y="value",
            color="type",
            title=f"Type of agents exposed: {graph_name} step: {i}",
        )

        # Define final dataframe with all plots and results
        df_final_exposed = df_final_exposed.append(
            {"bot": graph_name, "exposed": cn.count_exposed(G)}, ignore_index=True
        )

        #### CREATE THE PLOTS
        ##Uncomment plot(..) to save the plots to disk in html format

        plot_folder = "./data/plots/"

        # Plotly Line Plot
        # plot(line_chart, filename=f"{plot_folder}steps_{graph_name}.html")
        st.plotly_chart(line_chart, use_container_width=True)

        # Plotly bar plot
        # plot(bar_chart, filename=f"{plot_folder}exposed_type_{graph_name}.html")
        st.plotly_chart(bar_chart, use_container_width=True)

    # Plotly final bar chart
    final_bar_chart = px.bar(
        df_final_exposed, x="bot", y="exposed", title=f"Final bot plot of: {graph_name}"
    )
    # plot(final_bar_chart, filename=f"{plot_folder}final_exposed.html")
    st.plotly_chart(final_bar_chart, use_container_width=True)

    print("\nstatistics calculated succesfully")

    return True
