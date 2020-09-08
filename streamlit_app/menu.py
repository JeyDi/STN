import streamlit as st
from scraper.twitter import config, download
from graph_builder.graph import create_graph
import pandas as pd
import networkx as nx
import os
from tqdm import tqdm
import soil
import yaml


def side_menu():
    """
    Streamlit side config menu
    """

    st.sidebar.markdown("**Configuration Pannel**")

    ###################################
    ###### SCRAPER CONFIGURATION ######
    ###################################
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

    ##############################
    ###### GRAPH GENERATION ######
    ##############################
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

    ##############################
    #### SIMULATION WITH SOIL ####
    ##############################

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
                soil.simulation.run_from_config(configurations)

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


def launch():
    """
    Main function to launch all the streamilit functionalities
    """
    try:
        # Launch the side menu for all the configurations
        result = side_menu()
        return True
    except Exception as message:
        print(f"Impossible to launch the streamlit functionalities: {message}")
        return False
