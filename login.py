import streamlit as st

def login():

    st.write("Login")

    if 'username' in st.session_state:
        st.write(st.session_state.username)