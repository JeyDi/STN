import streamlit as st
import base64
import menu as main_menu

if __name__ == "__main__":
    #create the dashboard heading
    st.title('STN Project')
    st.markdown('## Simulate news spreading info over a social network')
    st.markdown('Using data gathered from twitter and simulated')

    main_menu.launch()



