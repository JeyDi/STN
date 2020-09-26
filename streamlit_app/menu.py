import streamlit as st
from menus.side_menu import (
    menu_scraper,
    menu_graph_generator,
    menu_bot_selection,
    menu_soil_simulation_subroutine,
    menu_plot_generations,
    count_statistics,
)


def side_menu():
    """
    Streamlit side config menu
    """

    st.sidebar.markdown("**Configuration Panel**")

    #### SCRAPER CONFIGURATION ####

    menu_scraper()

    #### GRAPH GENERATION ####

    menu_graph_generator()

    #### BOT SELECTION ####
    menu_bot_selection()
    
    #### SIMULATION WITH SOIL ####
    # TODO: test e debug del codice che non funziona
    menu_soil_simulation_subroutine()

    #### PLOT GENERATIONS ####
    # TODO: printare i grafici risultati
    menu_plot_generations()

    #### COUNT STATISTICS ####
    # TODO: sistemare la parte di calcolo
    count_statistics()


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
