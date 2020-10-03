import streamlit as st
import menu as main_menu

if __name__ == "__main__":
    #create the dashboard heading
    st.title('STN Project')
    st.markdown('## Simulate news spreading info over a social network')
    st.markdown('Using data gathered from twitter and simulated')
    st.markdown('<-- Open side menu to run functionalities')

    main_menu.launch()



