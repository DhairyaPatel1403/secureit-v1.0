import streamlit as st

def logout():

    if st.session_state.username!='':
        if st.button('Log Out'):
            st.session_state.username = ''     