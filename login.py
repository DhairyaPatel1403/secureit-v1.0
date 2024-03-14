import streamlit as st

def login():
    st.write("Login")

    # Check if username is already stored in session
    if not st.session_state.get('username'):
        # If not, ask user to enter their name
        username = st.text_input("Enter your name:")
        
        # Store username in session
        st.session_state['username'] = username
    else:
        # If username is already stored in session, display it
        st.write("Welcome back, " + st.session_state['username'])

# Run the login function
login()
