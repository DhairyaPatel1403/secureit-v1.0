import streamlit as st
from flask import Flask, request
import requests
import socket
import platform
import netifaces

# Function to render different pages
def render_page(page_name):
    if page_name == 'Login':
        # Import and execute code from page1.py
        from login import login
        login()
    if page_name == 'Signup':
        # Import and execute code from page1.py
        from signup import signup
        signup()
    if page_name == 'Log Out':
        # Import and execute code from page1.py
        from logout import logout
        logout()
    if page_name == 'Interface':
        # Import and execute code from page1.py
        from interface import interface
        interface()
    if page_name == 'History':
        # Import and execute code from page1.py
        from history import history
        history()
    if page_name == 'LockFile':
        # Import and execute code from page1.py
        from lockfile import lockfile
        lockfile()
    if page_name == 'UnlockFile':
        # Import and execute code from page1.py
        from unlockfile import unlockfile
        unlockfile()



# Streamlit app
def main():

    if 'userip' not in st.session_state:
        ## getting the hostname by socket.gethostname() method
        hostname = socket.gethostname()
        ## getting the IP address using socket.gethostbyname() method
        ip_address = socket.gethostbyname(hostname)

        user_ip = ip_address
        user_device = platform.node()
        interfaces = netifaces.interfaces()


        # Make a request to the Flask API to log in the user
        api_url = 'http://localhost:8002/login'  # Adjust the URL if necessary
        response = requests.post(api_url, json={"ip_address": user_ip, "user_device":user_device, "network_interfaces":interfaces})

        # Check if the login was successful
        if response.status_code == 200:
            
            # Store the user's IP address in the session state
            st.session_state.userip = user_ip
        else:
            pass


    st.title(''' Secure:orange[It] ''')


    # Create a navigation bar
    pages = ['Login', 'Signup', 'Log Out', 'Main', 'Encrypt', 'File', 'Interface', 'Decrypt', 'Face', 'History', 'LockFile', 'UnlockFile']
    selected_page = st.sidebar.selectbox('Select Page', pages)

    # Render the selected page
    render_page(selected_page)

if __name__ == '__main__':
    
    main()
