import streamlit as st
from scraper.twitter import config, download


def side_menu():
    """
    Streamlit side config menu
    """
    st.sidebar.markdown("**Configuration Pannel**")
    
    #Column selection
    st.sidebar.markdown("**Set parameters for the twitter scraper**")
    username = st.sidebar.text_input('Twitter username',value='@GiuseppeConteIT')
    store_info = st.sidebar.checkbox('Store the informations?',value=True)
    output_file = st.sidebar.text_input('Output result file path', value='./conte_followers.csv')
    download_level = st.sidebar.number_input('Level of graph distance',min_value=1,max_value=2,value=1)
    
    if st.sidebar.button('Launch the twitter scraper'):
        c = config(username, store_info, output_file)
        download(c,download_level)
        return True
    else:
        st.sidebar.markdown("Please compile the fields and press the button to download the twitter info")
        return False


def launch():
    """
    Main function to launch all the streamilit functionalities
    """
    try:
        #Launch the side menu for all the configurations
        result = side_menu()
        return True
    except Exception as message:
        print(f"Impossible to launch the streamlit functionalities: {message}")
        return False
    