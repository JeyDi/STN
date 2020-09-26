import streamlit as st
from scraper.twitter import config, download
from graph_builder.graph import create_graph
import pandas as pd
import networkx as nx
import os
from tqdm import tqdm
import soil
import yaml
import subprocess
from visualize.build_plot import generate_graph_plot
from statistics.visualizations import generate_statistics_plots
import ntpath


def path_head(path):
    # obtain foldername from a path, os independent
    head, tail = ntpath.split(path)

    return head


def path_tail(path):
    # obtain filename from a path, os independent
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


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

    button_scraper = st.sidebar.button("Launch the twitter scraper", key="b1")
    if button_scraper:
        with st.spinner(
            "Downloding twitter data...please be patient, it's required long time..."
        ):
            c = config(username, store_info, output_file)
            download(c, output_file, download_level)
            st.success(f"Download completed created succesfully")
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
        "Level of graph distance", min_value=1, max_value=2000, value=500
    )
    level2_path = st.sidebar.text_input(
        "Level 2 followers path", value="./data/conte_followers"
    )
    graph_name_list = ["500-users", "1000-users", "1500-users", "2000-users"]
    graph_name = st.sidebar.selectbox("Graph name", graph_name_list)

    graph_direct = st.sidebar.checkbox(
        "Check the box if you want to generate a direct graph", True
    )

    button_graph_generator = st.sidebar.button("Launch the Graph generator", key="b2")
    if button_graph_generator:

        try:
            # load the dataframe
            with st.spinner("Start creating the graph...please be patient.."):

                df = pd.read_csv(dataset_path)
                # create the graph
                result = create_graph(
                    df, follower_number, level2_path, graph_name, graph_direct
                )

                st.success(
                    f"Graph: **{graph_name}** created succesfully with: **{result}** number of nodes"
                )

            print("\nSimulation completed")
            return True
        except Exception as message:
            st.error(
                f"Impossible to read the csv file, please check the path or the code and retry.. {message}"
            )
            st.exception("WARNING: Impossible to read the csv file, check the path")
            print("\nImpossible to complete the simulation")
            return False


def menu_soil_simulation_subroutine():
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
        "Network parameters file path", value="./data/graph/500-users.gexf"
    )
    soil_config_path = os.path.abspath(soil_config_path)

    # config the new path with user gui config yaml
    config_path = path_head(soil_config_path)
    soil_new_config_path = os.path.join(config_path, "soil_config.yml")

    dir_path = os.path.abspath(dir_path)
    network_params_path = os.path.abspath(network_params_path)

    # launch the simulation
    button_simulation = st.sidebar.button("Launch the simulation", key="b3")
    if button_simulation:
        status = False
        with st.spinner("Launching the simulation...please wait..."):
            try:
                # read the existing config in the YAML file
                print(f"\nreading the configurations on: {soil_config_path}")
                with open(soil_config_path, "r") as stream:
                    configurations = yaml.safe_load(stream)

                # copy the file configurations before modify them
                configurations_old = configurations.copy()

                # # adapt the config with user preferences
                configurations["name"] = simulation_name
                configurations["max_time"] = max_time
                configurations["num_trials"] = num_trials
                # configurations["dir_path"] = dir_path
                configurations["network_params"]["path"] = network_params_path

                # Write a new yaml configuration for the subroutine launch

                ## LAUNCH THE SIMULATION SUBPROCESS
                # This is because the soil python libraries doesn't work alone and the only way it's to launch a subprocess with terminal
                print(f"Writing new configurations to: {soil_new_config_path}")
                with open(soil_new_config_path, "w") as file:
                    documents = yaml.dump(configurations, file)

                print(
                    f"New configuration inserted and saved to disk: {soil_new_config_path}"
                )

                print(f"Configuration: \n {configurations}")  # just for debug

                # Launch the subproces with the command
                command_launch = f"soil {soil_new_config_path} --csv"

                subprocess.call(command_launch, shell=True)

                status = True
                print(
                    f"Simulation completed succesfully with configs: {soil_new_config_path}"
                )
                st.success(f"Simulation completed succesfully")

                return status

            except Exception as message:
                print(
                    f"Impossible to run the simulation, please check the code: {message}"
                )
                status = False

                st.markdown(f"Soil subroutine command launched: {command_launch}")

                st.markdown("Errors")
                st.error(f"Simulation not completed: {message}")

                st.markdown("Error log")
                st.exception(message)

                st.markdown("User configurations in the GUI")
                st.write(configurations)

                st.markdown("Old configurations")
                st.write(configurations_old)

                return status


def menu_plot_generations():
    """
    side menu to configure and generate new plots based on data obtained from simulation
    used into menu.py file
    """
    st.sidebar.markdown("--------------")
    st.sidebar.markdown("**Configure Plots and Results**")

    G_path = st.sidebar.text_input("Graph path:", "./data/graph/500-users.gexf")
    simulation_data_path_list = [
        "./data/simulations/soil_result_random.csv",
        "./data/simulations/soil_result_btw.csv",
        "./data/simulations/soil_result_eigenvector.csv",
    ]
    simulation_data_path = st.sidebar.selectbox(
        "Simulation data path:", simulation_data_path_list
    )
    simulation_name_list = ["random", "btw", "eigenvector"]
    simulation_name = st.sidebar.selectbox("Simulation name:", simulation_name_list)
    G_step = st.sidebar.number_input(
        "Number of Graph step:", min_value=1, max_value=10, value=5, step=1
    )
    sprint_layout_calc = st.sidebar.checkbox("Calc the Graph Layout", False)

    button_plot_generation = st.sidebar.button("Launch the plot generation", key="b4")
    if button_plot_generation:
        status = False
        with st.spinner("Start calculating Graph prop and plots...please wait..."):
            result = generate_graph_plot(
                G_path,
                simulation_data_path,
                simulation_name,
                G_step,
                sprint_layout_calc,
            )
            st.success(f"Graph and Plot succesfully calculated")


def count_statistics():
    """
    side menu to configure and generate new plots based on data obtained from simulation
    used into menu.py file
    """
    st.sidebar.markdown("--------------")
    st.sidebar.markdown("**Final Statistics**")
    simulation_name_list = ["random", "btw", "eigenvector"]
    stats_simulation = st.sidebar.selectbox(
        "Simulation name:", simulation_name_list, key="s1"
    )
    stats_graph_steps = st.sidebar.number_input(
        "Number of steps into the graph:",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
        key="s2",
    )

    ##Generate plots and visualize results
    # WARNING: this function automatically display information in the main GUI tab
    button_stats = st.sidebar.button("Calc the final statistics", key="b5")
    if button_stats:
        status = False
        with st.spinner("Start calculating Graph prop and plots...please wait..."):
            plots = generate_statistics_plots(stats_simulation, stats_graph_steps)

            st.success(f"Graph and Plot succesfully calculated")
            # st.plotly_chart(
            #     plots[0], use_container_width=True
            # )  # try to print the plotly graph
