import streamlit as st
from scraper.twitter import config, download
from graph_builder.graph import create_graph
import pandas as pd
import networkx as nx
import os
from tqdm import tqdm
import soil
import yaml
from visualize.build_plot import generate_plot


def menu_scraper():
    """
    Side menu: generate a new csv file launching the twitter scraping functionalities
    Used into menu.py file
    """
    # Column selection
    st.sidebar.markdown("--------------")
    st.sidebar.markdown("**Set parameters for the twitter scraper**")
    username = st.sidebar.text_input("Twitter username", value="@GiuseppeConteIT")
    store_info = st.sidebar.checkbox("Store the informations?", value=True)
    output_file = st.sidebar.text_input(
        "Output result file path", value="./data/conte_followers.csv"
    )
    download_level = st.sidebar.number_input(
        "Level of graph distance", min_value=1, max_value=2, value=1
    )

    if st.sidebar.button("Launch the twitter scraper"):
        c = config(username, store_info, output_file)
        download(c, output_file, download_level)
        return True


def menu_graph_generator():
    """
    Side menu configurations for graph generator
    Used into menu.py file
    """
    st.sidebar.markdown("--------------")
    st.sidebar.markdown("**Generate a new Graph**")
    dataset_path = st.sidebar.text_input(
        "Dataset Path", value="./data/conte_followers.csv"
    )
    follower_number = st.sidebar.number_input(
        "Level of graph distance", min_value=1, max_value=1000, value=500
    )
    level2_path = st.sidebar.text_input(
        "Level 2 followers path", value="./data/conte_followers"
    )
    graph_name = st.sidebar.text_input("Graph name", value="500-users")
    graph_direct = st.sidebar.checkbox(
        "Check the box if you want to generate a direct graph", True
    )

    if st.sidebar.button("Launch the Graph generator"):

        try:
            # load the dataframe
            st.sidebar.markdown("Start creating the graph...please be patient..")
            df = pd.read_csv(dataset_path).iloc[:follower_number]
            # create the graph
            result = create_graph(df, level2_path, graph_name, graph_direct)
            st.sidebar.markdown(f"Graph {graph_name} created succesfully")
            return True
        except Exception as message:
            print(
                "Impossible to read the csv file, please check the path or the code and retry..",
                message,
            )
            st.sidebar.markdown(
                "WARNING: Impossible to read the csv file, check the path"
            )
            return False


def menu_soil_simulation():
    """
    Side menu functionalities for soil simulation
    used into menu.py file
    """

    # configure the simulation parameters: user input
    st.sidebar.markdown("--------------")
    st.sidebar.markdown("**Set parameters for the SOIL Simulation**")
    soil_config_path = st.sidebar.text_input(
        "Soil Configuration Path", value="./simulation/spread_config.yml"
    )
    simulation_name = st.sidebar.text_input("Simulation name", value="random_500")
    dir_path = st.sidebar.text_input("Main directory path", value="./simulation")

    max_time = st.sidebar.number_input(
        "Max iteration time", min_value=1, max_value=20, value=5
    )
    num_trials = st.sidebar.number_input(
        "Number of trials", min_value=1, max_value=10, value=1
    )
    network_params_path = st.sidebar.text_input(
        "Network parameters file path", value="./data/graph/500-user.gexf"
    )
    soil_config_path = os.path.abspath(soil_config_path)
    dir_path = os.path.abspath(dir_path)
    network_params_path = os.path.abspath(network_params_path)

    # launch the simulation
    if st.sidebar.button("Launch the simulation"):
        status = False
        with st.spinner("Launching the simulation...please wait..."):
            try:
                # read the existing config in the YAML file
                print("\nreading the configurations")
                with open(soil_config_path, "r") as stream:
                    configurations = yaml.safe_load(stream)

                # adapt the config with user preferences
                configurations["name"] = simulation_name
                configurations["max_time"] = max_time
                configurations["num_trials"] = num_trials
                configurations["dir_path"] = dir_path
                configurations["network_params"]["path"] = network_params_path
                print("New configuration inserted")

                print(f"Configuration: \n {configurations}")  # just for debug

                # run the simulation
                ### NON FUNZIONA E NON SO COME MAI!!!!!!
                # soil.simulation.run_from_config(configurations)

                ################################ INIZIO DEBUG
                for (
                    config_def
                ) in configurations:  # CICLA SU STRINGHE (entry del dizionario)
                    print(f"entry: {config_def}")
                    # logger.info("Found {} config(s)".format(len(ls)))
                    for config, path in load_config(
                        config_def
                    ):  # COPIATA FUNZIONE SOTTO, SCROLLA
                        name = config.get("name", "unnamed")
                        # logger.info("Using config(s): {name}".format(name=name))

                        dir_path = config.pop(
                            "dir_path", os.path.dirname(path)
                        )  # CODICE CHE VA IN ERRORE
                    """
                    sim = Simulation(dir_path=dir_path,
                                    **config)
                    sim.run_simulation(**kwargs)
                    """

                ################################ FINE DEBUG

                status = True
                st.success(f"Simulation completed succesfully")
                return status

            except Exception as message:
                print(
                    f"Impossible to run the simulation, please check the code: {message}"
                )
                status = False
                st.write(configurations)
                st.error(f"Simulation not completed: {message}")
                st.exception(message)
                return status


def menu_plot_generations():
    """
    side menu to configure and generate new plots based on data obtained from simulation
    used into menu.py file
    """
    st.sidebar.markdown("--------------")
    st.sidebar.markdown("**Configure Plots and Results**")

    G_path = st.sidebar.text_input("Graph path:", "./data/graph/500-users.gexf")
    simulation_data_path = st.sidebar.text_input(
        "Simulation data path:", "./data/simulations/betweenness_centrality_500.csv"
    )
    simulation_name = st.sidebar.text_input("Simulation name:", "test-simulation")
    G_step = st.sidebar.number_input(
        "Number of Graph step:", min_value=1, max_value=10, value=5, step=1
    )
    sprint_layout_calc = st.sidebar.checkbox("Calc the Graph Layout", False)

    if st.sidebar.button("Launch the plot generation"):
        status = False
        with st.spinner("Start calculating Graph prop and plots...please wait..."):
            result_plots = generate_plot(
                G_path,
                simulation_data_path,
                simulation_name,
                G_step,
                sprint_layout_calc,
            )
            print(result_plots)
            st.success(f"Graph and Plot succesfully calculated")
            # TODO: Print Plotly Graph


def count_statistics():
    pass
